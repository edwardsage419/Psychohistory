#!/usr/bin/env python3
"""Phase 3 offline corpus replay; new exclusive output roots protect evidence."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

import gkg_lossless as core
from gkg_lossless_contracts import validate_record
import study_gkg as study
from study_contracts import check_publication


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def code_hashes():
    paths = [Path(__file__), Path(core.__file__), Path(study.__file__),
             Path(core.legacy.__file__), Path(__file__).with_name('gkg_lossless_contracts.py'),
             Path(__file__).with_name('contracts.py'), Path(__file__).with_name('study_contracts.py')]
    paths += sorted((Path(__file__).resolve().parents[1] / 'schemas').glob('gkg-lossless-*.schema.json'))
    return {p.name: core.sha(p.read_bytes()) for p in paths}


def write_new(path, value):
    # Never truncate an existing file, including aliases/hard links to inputs.
    with Path(path).open('xb') as stream:
        stream.write(core.canonical(value) + b'\n')


def create_output(output, inputs):
    resolved = Path(output).resolve()
    for path in inputs:
        path = Path(path).resolve()
        if resolved == path or path in resolved.parents or resolved in path.parents:
            raise core.Rejection('output_input_collision', 'Output overlaps source evidence')
    resolved.mkdir(exist_ok=False)
    return resolved


def source_for(batch):
    return {'source_id': 'gdelt-gkg-2.1', 'batch_id': batch['batch_id'],
            'source_url': batch['url'], 'archive_sha256': batch['sha256'],
            'archive_bytes': batch['download_bytes'], 'acquisition': batch['acquisition']}


def duplicates(results, key):
    groups = defaultdict(list)
    for b in results:
        value = b['source']['archive_sha256'] if key == 'archive' else b['member_sha256']
        if value:
            groups[value].append(b['source']['batch_id'])
    return {k: v for k, v in groups.items() if len(v) > 1}


def compact(batch):
    return {**{k: v for k, v in batch.items() if k != 'rows'},
            'row_ledger_sha256': core.digest(batch['rows']),
            'quarantine': [r for r in batch['rows'] if r['disposition'] != 'accepted']}


def summary(batches):
    total = sum(b['physical_rows'] for b in batches)
    accepted = sum(b['accepted_rows'] for b in batches)
    q = Counter()
    for b in batches:
        q.update({k: v for k, v in b['disposition_counts'].items() if k != 'accepted'})
    return {'scheduled': len(batches), 'acquisition_passed': sum(b['source']['acquisition'] == 'passed' for b in batches),
            'archive_verified': sum(b['archive_state'] == 'passed' for b in batches),
            'source_hash_consistent': sum(b['source']['archive_sha256'] == b['observed_archive_sha256'] for b in batches),
            'physical_rows': total, 'accepted_rows': accepted, 'quarantined_rows': total - accepted,
            'quarantine_percentage': (total - accepted) * 100 / total if total else None,
            'quarantine_categories': dict(sorted(q.items())),
            'affected_batches': sum(b['quarantined_rows'] > 0 for b in batches),
            'batch_states': dict(Counter(b['state'] for b in batches)),
            'duplicate_archives': duplicates(batches, 'archive'), 'duplicate_members': duplicates(batches, 'member'),
            'failure_categories': dict(Counter(e['code'] for b in batches for e in b['errors']))}


def run(manifest_path, phase2_path, corpus, output):
    manifest = study.check_manifest(study.read_json(manifest_path))
    phase2_bytes = Path(phase2_path).read_bytes()
    phase2 = json.loads(phase2_bytes)
    check_publication(manifest, phase2)
    # Pin original recorded revisions; no interpretation of old partial counts.
    for b in phase2['batches']:
        if b['acquisition'] != 'passed' or not b.get('sha256') or not b.get('analysis') or b['analysis']['validation']['sha256'] != b['sha256']:
            raise core.Rejection('phase2_identity', 'Missing or contradictory acquisition evidence')
    output = create_output(output, [corpus, manifest_path, phase2_path])
    metadata = {'schema_version': '1.0.0', 'manifest_sha256': core.digest(manifest),
                'phase2_report_sha256': core.sha(phase2_bytes), 'code_hashes': code_hashes(), 'created_at': now()}
    write_new(output / 'run.json', metadata)
    batches = []
    for batch in phase2['batches']:
        source = source_for(batch)
        result = core.ingest(Path(corpus) / 'raw' / (source['archive_sha256'] + '.zip'), source)
        core.validate_batch(result)
        write_new(output / (batch['batch_id'] + '.json'), result)
        batches.append(result)
        print(f"{len(batches)}/{len(phase2['batches'])} {batch['batch_id']}: {result['state']}", flush=True)
    report = {**metadata, 'summary': summary(batches), 'batches': [compact(b) for b in batches]}
    write_new(output / 'study.json', report)
    return report


def read_run(root, manifest):
    metadata = study.read_json(Path(root) / 'run.json')
    if metadata['manifest_sha256'] != core.digest(manifest) or metadata['code_hashes'] != code_hashes():
        raise core.Rejection('run_identity', 'Manifest or evaluator bytes differ from stored run')
    results = []
    for batch in manifest['batches']:
        result = study.read_json(Path(root) / (batch['batch_id'] + '.json'))
        if result['source']['batch_id'] != batch['batch_id'] or result['source']['source_url'] != batch['url']:
            raise core.Rejection('source_identity', 'Stored result differs from scheduled slot')
        results.append(result)
    return metadata, results


def validate_replay(report):
    validate_record('replay', report)
    semantic = {k: v for k, v in report.items() if k not in ('created_at', 'semantic_sha256')}
    if core.digest(semantic) != report['semantic_sha256']:
        raise core.Rejection('semantic_hash_mismatch', 'Replay fingerprint contradicts content')
    counts = Counter(b['status'] for b in report['batches'])
    if report['passed'] != counts['passed'] or report['failed'] != counts['failed']:
        raise core.Rejection('replay_accounting', 'Replay counts contradict slots')
    ids = [b['batch_id'] for b in report['batches']]
    if len(set(ids)) != len(ids):
        raise core.Rejection('sample_accounting', 'Duplicate replay slot')
    for b in report['batches']:
        equivalent = (b['first_semantic_sha256'] == b['second_semantic_sha256'] and
                      b['first_archive_sha256'] == b['second_archive_sha256'] == b['expected_archive_sha256'])
        if b['status'] == 'passed' and (not equivalent or b['errors']):
            raise core.Rejection('inconsistent_success', 'Replay success contradicts evidence')
        if b['status'] == 'failed' and not b['errors']:
            raise core.Rejection('missing_failure_code', 'Replay failure lacks reason')
    return report


def compare(manifest, first, second):
    m1, a = read_run(first, manifest)
    m2, b = read_run(second, manifest)
    if m1['phase2_report_sha256'] != m2['phase2_report_sha256']:
        raise core.Rejection('run_identity', 'Different Phase 2 references')
    items = []
    for left, right in zip(a, b):
        errors = []
        for record in (left, right):
            try:
                core.validate_batch(record)
            except (ValueError, core.Rejection) as exc:
                errors.append(core.error(getattr(exc, 'code', 'contract_failure'), 'Stored batch validation failed'))
        if left['source'] != right['source']:
            errors.append(core.error('source_revision_mismatch', 'Different source revisions'))
        if left['semantic_sha256'] != right['semantic_sha256']:
            errors.append(core.error('semantic_hash_mismatch', 'Independent batch semantics differ'))
        expected = left['source']['archive_sha256']
        if left['observed_archive_sha256'] != right['observed_archive_sha256'] or left['observed_archive_sha256'] != expected:
            errors.append(core.error('source_revision_mismatch', 'Independent source hashes disagree'))
        items.append({'batch_id': left['source']['batch_id'], 'status': 'failed' if errors else 'passed',
                      'first_semantic_sha256': left['semantic_sha256'], 'second_semantic_sha256': right['semantic_sha256'],
                      'first_archive_sha256': left['observed_archive_sha256'], 'second_archive_sha256': right['observed_archive_sha256'],
                      'expected_archive_sha256': expected, 'errors': errors})
    report = {'schema_version': '1.0.0', 'manifest_sha256': m1['manifest_sha256'],
              'phase2_report_sha256': m1['phase2_report_sha256'], 'code_hashes': m1['code_hashes'],
              'created_at': now(), 'batches': items, 'passed': sum(i['status'] == 'passed' for i in items),
              'failed': sum(i['status'] == 'failed' for i in items)}
    report['semantic_sha256'] = core.digest({k: v for k, v in report.items() if k != 'created_at'})
    validate_replay(report)
    return report


def assess(manifest, batches, replay, regression_passed=False):
    errors = []
    try:
        validate_replay(replay)
    except (ValueError, core.Rejection) as exc:
        errors.append(core.error(getattr(exc, 'code', 'contract_failure'), 'Replay evidence invalid'))
    valid = True
    for b in batches:
        try:
            core.validate_batch(b)
        except (ValueError, core.Rejection):
            valid = False
    expected_ids = [b['batch_id'] for b in manifest['batches']]
    s = summary(batches)
    gates = {
        'exact_sample_identity': (len(expected_ids) == study.SAMPLE_SIZE and
            [b['source']['batch_id'] for b in batches] == expected_ids and
            [b['batch_id'] for b in replay['batches']] == expected_ids and
            replay['manifest_sha256'] == core.digest(manifest) and s['acquisition_passed'] == len(expected_ids)),
        'archive_identity_integrity': s['archive_verified'] == s['source_hash_consistent'] == len(expected_ids),
        'no_duplicate_batches': not s['duplicate_archives'] and not s['duplicate_members'],
        'disposition_provenance_complete': valid and all(b['rows'] and b['rows'][-1]['end'] == b['member_bytes'] for b in batches),
        'independent_replay': not errors and replay['passed'] == len(expected_ids) and replay['failed'] == 0,
        'mutation_and_failure_regressions': regression_passed,
        'batch_transparency_usability': valid and all(b['state'] != 'rejected' and b['accepted_rows'] > 0 for b in batches),
        'zero_unexpected_exceptions': not s['failure_categories'].get('unexpected_exception', 0),
        'encoding_ambiguity_contained': valid and all(not r['invalid_sequences'] for b in batches for r in b['rows'] if r['disposition'] == 'accepted')}
    # The replay must attest these exact ledgers, not another successful run.
    if len(batches) != len(replay['batches']) or any(b['semantic_sha256'] != r['first_semantic_sha256'] or b['source']['archive_sha256'] != r['expected_archive_sha256'] for b, r in zip(batches, replay['batches'])):
        gates['independent_replay'] = False
        errors.append(core.error('replay_binding', 'Replay does not attest assessed ledgers'))
    for name, passed in gates.items():
        if not passed:
            errors.append(core.error('gate_failed', name))
    result = {'schema_version': '1.0.0', 'scope': 'raw acquisition, archive verification, lossless parsing, quarantine and provenance only',
              'recommendation': 'promote_to_ingestion_candidate' if all(gates.values()) else 'continue_validation',
              'gates': gates, 'replay_sha256': replay['semantic_sha256'], 'errors': errors,
              'limitations': ['English-feed bounded retrospective corpus only; no operational SLA',
                              'Unknown invalid-byte origin remains quarantined; no codec guessed',
                              'Accepted means syntactic/provenance eligibility, not theme or indicator validity',
                              'Regression gate is supplied from separately recorded offline test evidence']}
    validate_record('assessment', result)
    return result


def provenance_receipts(phase2, phase2_hash):
    return {'schema_version': '1.0.0', 'phase2_report_sha256': phase2_hash,
            'batches': [{**source_for(b), 'started_at': b['started_at'], 'finished_at': b['finished_at'],
                         'transport': b['transport'], 'parser_version': core.PARSER_VERSION,
                         'contract_version': core.CONTRACT_VERSION} for b in phase2['batches']]}


def storage_profile(manifest, batches, receipts):
    """Measure logical serialized payloads; no guessed compression/storage engine."""
    refs = {r['batch_id']: r for r in receipts['batches']}
    by_id = {b['source']['batch_id']: b for b in batches}
    measurements = []
    for slot in manifest['batches']:
        b = by_id[slot['batch_id']]
        q = [r for r in b['rows'] if r['disposition'] != 'accepted']
        accepted = [r for r in b['rows'] if r['disposition'] == 'accepted']
        measurements.append({'batch_id': slot['batch_id'], 'cohort': slot['cohort'],
            'raw_archives': b['source']['archive_bytes'],
            'quarantine_evidence': sum(len(core.canonical(r)) + 1 for r in q),
            'derived_accepted_row_ledger': sum(len(core.canonical(r)) + 1 for r in accepted),
            'manifests_provenance': len(core.canonical(slot)) + len(core.canonical(refs[slot['batch_id']])) + 2})
    keys = ('raw_archives', 'quarantine_evidence', 'derived_accepted_row_ledger', 'manifests_provenance')
    recent = [b for b in measurements if b['cohort'] == 'recent']
    scenarios = {}
    for key in keys:
        mean = sum(b[key] for b in recent) / len(recent) if recent else None
        scenarios[key] = {'measured_recent_batches': len(recent), 'mean_bytes_per_batch': mean,
                          'extrapolated_bytes_per_day': mean * 96 if mean is not None else None,
                          'extrapolated_bytes_per_30_days': mean * 2880 if mean is not None else None,
                          'extrapolated_bytes_per_365_days': mean * 35040 if mean is not None else None}
    return {'schema_version': '1.0.0', 'measurement': 'Canonical UTF-8 JSONL record payload bytes; raw ZIP sizes from verified acquisition',
            'measured_totals_bytes': {key: sum(b[key] for b in measurements) for key in keys},
            'normalized_field_records': {'created': False, 'bytes': None, 'estimate': None},
            'recent_extrapolations': scenarios, 'batches': measurements,
            'limitations': ['18-hour convenience sample, not full periods or confidence intervals',
                           'Accepted-row ledgers contain hashes/locators, not normalized field values',
                           'Excludes report wrappers, schema/code files, backups, indexes and Git history',
                           'Quarantine bytes are permanently retained; future rates may differ']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=study.DEFAULT_MANIFEST)
    parser.add_argument('--phase2', type=Path, default=Path('studies/gkg-continuity-v1/results/study.json'))
    parser.add_argument('--corpus', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = run(args.manifest, args.phase2, args.corpus, args.output)
        return 2 if report['summary']['batch_states'].get('rejected') else 0
    except Exception as exc:
        print(json.dumps({'status': 'failed', 'errors': [core.error(getattr(exc, 'code', 'study_error'), type(exc).__name__)]}), file=sys.stderr)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
