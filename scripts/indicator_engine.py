"""Deterministic experimental indicators; no network, imputation or event claims."""
from datetime import datetime, timedelta, timezone
import re

from contracts import ContractError, observation_id, validate_contract
from indicator_definitions import require_gkg_prevalence, validate_registry
from gkg_lossless import digest
from gkg_indicator_metrics import validate_metric, duplicate_diagnostic

VERSION = '1.0.0'
STEP = timedelta(minutes=15)


def utc(stamp):
    if not isinstance(stamp, str) or not re.fullmatch(r'[0-9]{14}', stamp):
        raise ContractError('batch_id', 'timestamp')
    try:
        d = datetime.strptime(stamp, '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
    except ValueError:
        raise ContractError('batch_id', 'timestamp') from None
    if d.minute % 15 or d.second:
        raise ContractError('batch_id', 'off_grid')
    return d


def iso(d):
    return d.isoformat().replace('+00:00', 'Z')


def window_size(minutes):
    if type(minutes) is not int or minutes < 15 or minutes > 1440 or minutes % 15 or 1440 % minutes:
        raise ContractError('window', 'unsupported_window')
    return timedelta(minutes=minutes)


def floor_window(d, minutes):
    window_size(minutes)
    return d.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(minutes=((d.hour * 60 + d.minute) // minutes) * minutes)


def checked_metrics(metrics):
    ids, hashes = set(), set()
    for m in metrics:
        validate_metric(m)
        utc(m['batch_id'])
        if m['batch_id'] in ids:
            raise ContractError('batch_id', 'duplicate_batch')
        h = m['provenance']['source']['archive_sha256']
        if h in hashes:
            raise ContractError('source', 'duplicate_archive')
        ids.add(m['batch_id']); hashes.add(h)
        if m['source_id'] != 'gdelt-gkg-2.1' or m['source_field'] != 'V1THEMES' or m['source_dataset'] != 'GKG 2.1 English-file family':
            raise ContractError('source', 'unsupported_metric_source')
    return sorted(metrics, key=lambda m: m['batch_id'])


def observation(metric_id, at, retrieved, value, unit, snapshot, reference, flags):
    o = {'schema_version': '1.0.0', 'observation_id': '', 'source_id': 'gdelt-gkg-2.1',
         'source_version': '2.1', 'metric_id': metric_id, 'observed_at': at, 'retrieved_at': retrieved,
         'value': value, 'unit': unit, 'geography': None, 'entity': None,
         'quality_status': 'missing' if value is None else ('suspect' if flags else 'valid'),
         'quality_note': ';'.join(flags) if flags else 'verified source row count',
         'source_record_reference': reference, 'source_snapshot_sha256': snapshot,
         'transformation_version': VERSION}
    o['observation_id'] = observation_id(o)
    return validate_contract('observation', o)


def build(metrics, definitions, history, code_sha256, retrieved_at, windows=(60, 1440), requested=None):
    """Requested window starts allow entirely missing windows to be represented.

    The default evaluates only calendar windows touched by the bounded sample;
    this is explicitly not a continuous history across the sample's many years.
    """
    metrics = checked_metrics(metrics)
    validate_registry(definitions, history)
    definitions = sorted((require_gkg_prevalence(d) for d in definitions), key=lambda d: (d['indicator_id'], d['version']))
    if not re.fullmatch('[a-f0-9]{64}', code_sha256):
        raise ContractError('code', 'hash')
    if not windows or len(set(windows)) != len(windows):
        raise ContractError('windows', 'empty_or_duplicate')
    for minutes in windows:
        window_size(minutes)
    if requested is not None and set(requested) != set(windows):
        raise ContractError('requested', 'window_configuration')
    receipts, normalized, quality, values, provenance = [], [], [], [], []
    source_ids = {}
    for m in metrics:
        receipt = {'schema_version': VERSION, 'batch_id': m['batch_id'], **m['provenance'],
                   'source_metric_sha256': m['semantic_sha256'], 'transformation_version': VERSION,
                   'implementation_sha256': code_sha256}
        receipt['receipt_sha256'] = digest(receipt)
        receipts.append(receipt)
        for token in sorted({d['transformation']['parameters']['token'] for d in definitions}):
            flags = ['quarantined_rows_excluded'] if m['quarantined_rows'] else []
            if m['empty_theme_rows']:
                flags.append('empty_theme_rows_in_denominator')
            reference = 'receipt:' + receipt['receipt_sha256'] + '#V1THEMES:' + token
            o = observation('gkg.literal_token_row_count:' + token, iso(utc(m['batch_id'])),
                m['provenance']['acquisition']['finished_at'], m['theme_counts'].get(token, 0),
                'accepted_document_rows', m['provenance']['source']['archive_sha256'], reference, flags)
            normalized.append(o)
            source_ids[m['batch_id'], token] = o['observation_id']
            quality.append({'observation_id': o['observation_id'], 'layer': 'source_metric',
                'flags': flags, 'accepted_rows': m['accepted_rows'], 'quarantined_rows': m['quarantined_rows'],
                'empty_theme_rows': m['empty_theme_rows'], 'coverage': 1.0})
    by_id = {m['batch_id']: m for m in metrics}
    receipt_ids = {r['batch_id']: r['receipt_sha256'] for r in receipts}
    for minutes in sorted(windows):
        duration = window_size(minutes)
        if requested is None:
            starts = sorted({floor_window(utc(m['batch_id']), minutes) for m in metrics})
        else:
            starts = [utc(s) for s in requested[minutes]]
            if len(set(starts)) != len(starts) or any(floor_window(s, minutes) != s for s in starts):
                raise ContractError('requested', 'duplicate_or_unaligned_window')
            starts.sort()
        for start in starts:
            expected = [(start + i * STEP).strftime('%Y%m%d%H%M%S') for i in range(minutes // 15)]
            present = [by_id[b] for b in expected if b in by_id]
            missing = [b for b in expected if b not in by_id]
            accepted = sum(m['accepted_rows'] for m in present)
            nonempty = sum(m['nonempty_theme_rows'] for m in present)
            quarantine = sum(m['quarantined_rows'] for m in present)
            inputs = [receipt_ids[m['batch_id']] for m in present]
            for d in definitions:
                token = d['transformation']['parameters']['token']
                numerator = sum(m['theme_counts'].get(token, 0) for m in present)
                repeats = duplicate_diagnostic(present, token)
                flags = ['experimental_definition', 'historical_semantics_unvalidated', 'collection_scope_only']
                if missing: flags.append('incomplete_window')
                if not accepted: flags.append('zero_denominator')
                if quarantine: flags.append('quarantined_rows_excluded')
                if accepted != nonempty: flags.append('empty_theme_rows_in_denominator')
                if repeats['excess_identifier_rows']: flags.append('repeated_document_identifiers')
                if repeats['missing_identifier_rows']: flags.append('missing_document_identifiers')
                value = numerator / accepted if not missing and accepted else None
                binding = {'schema_version': VERSION, 'definition_sha256': digest(d),
                    'indicator_id': d['indicator_id'], 'indicator_version': d['version'],
                    'implementation_sha256': code_sha256, 'transformation_version': VERSION,
                    'window_minutes': minutes, 'window_start': iso(start), 'window_end': iso(start + duration),
                    'expected_batches': expected, 'source_receipts': inputs,
                    'source_observation_ids': [source_ids[m['batch_id'], token] for m in present],
                    'retrospective_rule': True}
                phash = digest(binding)
                o = observation(d['indicator_id'] + '@' + d['version'] + '/' + str(minutes) + 'm', iso(start),
                    retrieved_at, value, 'fraction', digest(inputs), 'provenance:' + phash, flags)
                oid = o['observation_id']
                provenance.append({'observation_id': oid, 'provenance_sha256': phash, **binding})
                quality.append({'observation_id': oid, 'layer': 'indicator', 'flags': flags,
                    'expected_batches': expected, 'observed_batches': [m['batch_id'] for m in present],
                    'missing_batches': missing, 'coverage': len(present) / len(expected),
                    'accepted_rows': accepted, 'quarantined_rows': quarantine, 'empty_theme_rows': accepted - nonempty,
                    'duplicate_diagnostic': repeats})
                values.append({'schema_version': VERSION, 'indicator_id': d['indicator_id'], 'indicator_version': d['version'],
                    'definition_sha256': digest(d), 'observation': o,
                    'window_start': iso(start), 'window_end': iso(start + duration), 'window_minutes': minutes,
                    'sampled_numerator': numerator, 'sampled_denominator': accepted,
                    'nonempty_theme_denominator': nonempty,
                    'sampled_all_accepted_prevalence': numerator / accepted if accepted else None,
                    'sampled_nonempty_prevalence': numerator / nonempty if nonempty else None,
                    'diagnostics_are_partial_when_incomplete': bool(missing)})
    bundle = {'normalized_observations': normalized, 'indicator_values': values,
              'quality': quality, 'provenance': provenance, 'batch_receipts': receipts}
    validate_bundle(bundle, definitions)
    return bundle


def validate_bundle(bundle, definitions):
    """Reject broken identities, numerical claims and provenance links on import."""
    def need(condition, code):
        if not condition: raise ContractError('bundle', code)
    dmap={(d['indicator_id'],d['version']):d for d in definitions}
    quality={q['observation_id']:q for q in bundle['quality']}
    prov={p['observation_id']:p for p in bundle['provenance']}
    need(len(quality)==len(bundle['quality']), 'duplicate_quality')
    need(len(prov)==len(bundle['provenance']), 'duplicate_provenance')
    for q in quality.values(): validate_contract('indicator-quality',q)
    receipts={r['receipt_sha256']:r for r in bundle['batch_receipts']}
    need(len(receipts)==len(bundle['batch_receipts']),'duplicate_receipt')
    for h,r in receipts.items():
        need(h==digest({k:v for k,v in r.items() if k!='receipt_sha256'}),'receipt_hash')
    normalized={o['observation_id']:o for o in bundle['normalized_observations']}
    need(len(normalized)==len(bundle['normalized_observations']),'duplicate_observation')
    for o in normalized.values():
        validate_contract('observation',o)
        need(o['observation_id'] in quality,'missing_quality')
        ref=o['source_record_reference'].split('#',1)[0].removeprefix('receipt:')
        need(ref in receipts,'source_receipt_link')
        need(o['source_snapshot_sha256']==receipts[ref]['source']['archive_sha256'],'source_hash_link')
    ids=[]
    for v in bundle['indicator_values']:
        validate_contract('indicator-value',v)
        o=v['observation'];validate_contract('observation',o);oid=o['observation_id'];ids.append(oid)
        need(oid in quality and oid in prov,'missing_sidecar')
        q,p=quality[oid],prov[oid]
        validate_contract('indicator-provenance',p)
        need(p['provenance_sha256']==digest({k:x for k,x in p.items() if k not in ('observation_id','provenance_sha256')}),'provenance_hash')
        need(o['source_record_reference']=='provenance:'+p['provenance_sha256'],'provenance_link')
        key=(v['indicator_id'],v['indicator_version'])
        need(key in dmap,'definition_missing')
        need(v['definition_sha256']==p['definition_sha256']==digest(dmap[key]),'definition_binding')
        need(all(h in receipts for h in p['source_receipts']),'receipt_missing')
        need(all(h in normalized for h in p['source_observation_ids']),'normalized_input_missing')
        need(o['source_snapshot_sha256']==digest(p['source_receipts']),'aggregate_snapshot_hash')
        expected=q['expected_batches'];observed=q['observed_batches'];missing=q['missing_batches']
        need(expected==p['expected_batches'] and len(expected)==len(set(expected)),'expected_batches')
        need(sorted(observed+missing)==sorted(expected) and len(set(observed+missing))==len(expected),'coverage_partition')
        need(observed==[receipts[h]['batch_id'] for h in p['source_receipts']],'observed_receipts')
        need(q['coverage']==len(observed)/len(expected),'coverage_ratio')
        need(p['window_start']==v['window_start']==o['observed_at'] and p['window_end']==v['window_end'] and p['window_minutes']==v['window_minutes'],'window_binding')
        start=datetime.fromisoformat(v['window_start'].replace('Z','+00:00'))
        end=datetime.fromisoformat(v['window_end'].replace('Z','+00:00'))
        need(start.utcoffset()==timedelta(0) and floor_window(start,v['window_minutes'])==start and end-start==window_size(v['window_minutes']),'window_bounds')
        need(expected==[(start+i*STEP).strftime('%Y%m%d%H%M%S') for i in range(v['window_minutes']//15)],'expected_grid')
        n,den,nonempty=v['sampled_numerator'],v['sampled_denominator'],v['nonempty_theme_denominator']
        need(n<=nonempty<=den and q['accepted_rows']==den and q['empty_theme_rows']==den-nonempty,'denominator')
        need(v['sampled_all_accepted_prevalence']==(n/den if den else None) and v['sampled_nonempty_prevalence']==(n/nonempty if nonempty else None),'diagnostic_ratio')
        need(o['value']==(n/den if den and not missing else None),'indicator_ratio')
        need(v['diagnostics_are_partial_when_incomplete']==bool(missing),'partial_diagnostic')
        need(('incomplete_window' in q['flags'])==bool(missing),'missing_flag')
        need(('zero_denominator' in q['flags'])==(den==0),'denominator_flag')
        need(o['quality_note']==';'.join(q['flags']),'quality_binding')
    need(len(ids)==len(set(ids)),'duplicate_indicator_value')
    need(set(quality)==set(ids)|set(normalized) and set(prov)==set(ids),'orphan_sidecar')
    return bundle
