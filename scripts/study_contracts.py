"""Offline contract and accounting checks for study publications."""
from collections import Counter
from contracts import SCHEMAS, ContractError, validate
import study_gkg as study


def check_publication(manifest, report, replay=False):
    study.check_manifest(manifest)
    name = 'gkg-study-replay' if replay else 'gkg-study'
    validate(report, study.read_json(SCHEMAS / (name + '.v1.schema.json')))
    if report['manifest_sha256'] != study.digest(manifest) or report['study_id'] != manifest['study_id']:
        raise ContractError('$', 'manifest_mismatch')
    if [b['batch_id'] for b in report['batches']] != [b['batch_id'] for b in manifest['batches']]:
        raise ContractError('$.batches', 'sample_accounting')
    if replay:
        if dict(Counter(b['status'] for b in report['batches'])) != report['counts']:
            raise ContractError('$.counts', 'replay_accounting')
        for b in report['batches']:
            if b['status'] == 'passed' and (not all(b[k] for k in ('semantic_equal', 'hash_matches_acquisition', 'matches_original_semantics'))
                                          or b['first_semantic_sha256'] != b['second_semantic_sha256']
                                          or b['first_raw_sha256'] != b['second_raw_sha256']):
                raise ContractError('$.batches', 'false_replay_success')
    else:
        counts = report['summary']['counts']
        acquired = sum(b['acquisition'] == 'passed' for b in report['batches'])
        if counts['scheduled'] != len(manifest['batches']) or counts['acquired'] != acquired:
            raise ContractError('$.summary.counts', 'acquisition_accounting')
        if report['summary']['acquisition_success_rate'] != acquired / len(manifest['batches']):
            raise ContractError('$.summary.acquisition_success_rate', 'rate_accounting')
        for expected, actual in zip(manifest['batches'], report['batches']):
            if any(actual[k] != expected[k] for k in expected):
                raise ContractError('$.batches', 'batch_reference_mismatch')
            if actual.get('replay') and actual['replay']['status'] == 'passed':
                r = actual['replay']
                if not r['semantic_equal'] or not r['hash_matches_acquisition'] or r['first_raw_sha256'] != r['second_raw_sha256'] or r['first_raw_sha256'] != actual['sha256']:
                    raise ContractError('$.batches', 'false_replay_success')
    return report
