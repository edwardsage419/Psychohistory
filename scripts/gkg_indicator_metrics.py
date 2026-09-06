"""Offline source metrics from authenticated Phase 3 bytes, never an ontology."""
from collections import Counter, defaultdict
from itertools import combinations
import json
import re

import gkg_lossless as core
from contracts import validate_contract

VERSION = '1.0.0'


def fail(code):
    raise core.Rejection(code, 'Phase 4 source metric validation failed')


def seal(value):
    value['semantic_sha256'] = core.digest({k: v for k, v in value.items() if k != 'semantic_sha256'})
    return value


def extract(blob, ledger, acquisition, published):
    source = ledger['source']
    if any(acquisition.get(k) != v for k, v in source.items()):
        fail('acquisition_binding')
    if (published['semantic_sha256'] != ledger['semantic_sha256'] or
            published['row_ledger_sha256'] != core.digest(ledger['rows'])):
        fail('published_ledger_binding')
    member, payload = core.verified_member(blob, source)
    core.validate_batch(ledger, payload)
    if ledger['state'] == 'rejected':
        fail('rejected_batch')
    counts, documents, collections, outlets = Counter(), defaultdict(list), Counter(), Counter()
    empty = repeated_tokens = empty_segments = no_document = 0
    for row in ledger['rows']:
        if row['disposition'] != 'accepted':
            continue
        fields = core.body(payload[row['start']:row['end']]).decode('utf-8').split('\t')
        # V1THEMES is column 8; V2ENHANCEDTHEMES (column 9) has mention offsets.
        parts = fields[7].split(';') if fields[7] else []
        tokens = sorted(set(p for p in parts if p != ''))
        empty += not tokens
        empty_segments += sum(p == '' for p in parts)
        repeated_tokens += len([p for p in parts if p]) - len(tokens)
        counts.update(tokens)
        collections[fields[2]] += 1
        outlets[fields[3]] += 1
        if fields[4]:
            # Diagnostic identity only: exact bytes, no URL normalization or event inference.
            documents[core.sha(fields[4].encode('utf-8'))].append(tokens)
        else:
            no_document += 1
    result = {'schema_version': VERSION, 'transformation_version': VERSION,
              'batch_id': source['batch_id'], 'source_id': source['source_id'],
              'source_dataset': 'GKG 2.1 English-file family', 'source_field': 'V1THEMES',
              'accepted_rows': ledger['accepted_rows'], 'quarantined_rows': ledger['quarantined_rows'],
              'empty_theme_rows': empty, 'nonempty_theme_rows': ledger['accepted_rows'] - empty,
              'theme_counts': dict(sorted(counts.items())), 'documents': dict(sorted(documents.items())),
              'missing_document_rows': no_document, 'within_row_repeated_tokens': repeated_tokens,
              'empty_delimiter_segments': empty_segments,
              'source_collection_counts': dict(sorted(collections.items())),
              'source_name_counts': dict(sorted(outlets.items())),
              'provenance': {'source': source, 'acquisition': acquisition, 'member': member,
                  'member_sha256': core.sha(payload), 'ledger_semantic_sha256': ledger['semantic_sha256'],
                  'row_ledger_sha256': published['row_ledger_sha256'],
                  'parser_version': ledger['parser_version'], 'contract_version': ledger['schema_version']}}
    return validate_metric(seal(result))


def validate_metric(m):
    validate_contract('gkg-source-metric', m)
    if m.get('schema_version') != VERSION or m.get('transformation_version') != VERSION:
        fail('metric_version')
    if m.get('semantic_sha256') != core.digest({k: v for k, v in m.items() if k != 'semantic_sha256'}):
        fail('metric_hash')
    for key in ('accepted_rows', 'quarantined_rows', 'empty_theme_rows', 'nonempty_theme_rows',
                'missing_document_rows', 'within_row_repeated_tokens', 'empty_delimiter_segments'):
        if type(m[key]) is not int or m[key] < 0:
            fail('metric_count')
    if m['accepted_rows'] != m['empty_theme_rows'] + m['nonempty_theme_rows']:
        fail('metric_denominator')
    observed = Counter()
    rows = 0
    for doc, entries in m['documents'].items():
        if not re.fullmatch('[a-f0-9]{64}', doc) or not entries:
            fail('document_identity')
        for tokens in entries:
            if not isinstance(tokens, list) or any(not isinstance(t, str) or not t or ';' in t for t in tokens) or tokens != sorted(set(tokens)):
                fail('document_tokens')
            rows += 1
            observed.update(tokens)
    if rows + m['missing_document_rows'] != m['accepted_rows']:
        fail('document_accounting')
    for token, count in m['theme_counts'].items():
        if not isinstance(token, str) or not token or ';' in token or type(count) is not int or not 0 < count <= m['nonempty_theme_rows']:
            fail('theme_count')
    if not m['missing_document_rows'] and dict(observed) != m['theme_counts']:
        fail('document_theme_accounting')
    if any(v > m['theme_counts'].get(k, 0) for k, v in observed.items()):
        fail('document_theme_accounting')
    for key in ('source_collection_counts', 'source_name_counts'):
        if any(type(v) is not int or v < 1 for v in m[key].values()) or sum(m[key].values()) != m['accepted_rows']:
            fail('source_count')
    p = m['provenance']
    if (p['source']['batch_id'] != m['batch_id'] or p['source']['source_id'] != m['source_id']
            or any(p['acquisition'].get(k) != v for k, v in p['source'].items())):
        fail('metric_source_binding')
    return m


def duplicate_diagnostic(metrics, token=None):
    documents = defaultdict(list)
    missing = 0
    for m in metrics:
        missing += m['missing_document_rows']
        for key, rows in m['documents'].items():
            documents[key].extend(rows)
    n = len(documents)
    matched = sum(any(token in row for row in rows) for rows in documents.values()) if token else None
    return {'identified_rows': sum(map(len, documents.values())), 'missing_identifier_rows': missing,
            'distinct_identifiers': n, 'repeated_identifiers': sum(len(v) > 1 for v in documents.values()),
            'excess_identifier_rows': sum(len(v) - 1 for v in documents.values()),
            'unique_identifier_token_numerator': matched,
            'unique_identifier_prevalence': matched / n if token and n else None,
            'method': 'exact identifier; union of token presence across repeats; diagnostic only'}


def inventory(metrics, cohorts, documented):
    metrics = sorted(metrics, key=lambda m: m['batch_id'])
    total = sum(m['accepted_rows'] for m in metrics)
    tokens = sorted(set().union(*(m['theme_counts'] for m in metrics)))
    cohort_ids = sorted(set(cohorts.values()))
    result = []
    panel_pairs = defaultdict(Counter)
    for m in metrics:
        for rows in m['documents'].values():
            for row_tokens in rows:
                panel = set(row_tokens) & set(documented)
                for token in row_tokens:
                    panel_pairs[token].update(panel - {token})
    for token in tokens:
        distribution = [m['theme_counts'].get(token, 0) for m in metrics]
        present = [m['batch_id'] for m, n in zip(metrics, distribution) if n]
        by_cohort = {}
        for cohort in cohort_ids:
            subset = [m for m in metrics if cohorts[m['batch_id']] == cohort]
            count = sum(m['theme_counts'].get(token, 0) for m in subset)
            denom = sum(m['accepted_rows'] for m in subset)
            by_cohort[cohort] = {'rows': count, 'accepted_rows': denom, 'prevalence': count / denom if denom else None,
                                 'batches_present': sum(token in m['theme_counts'] for m in subset)}
        result.append({'token': token, 'rows': sum(distribution), 'batch_coverage': len(present),
            'prevalence': sum(distribution) / total if total else None,
            'first_sampled_batch': present[0], 'last_sampled_batch': present[-1],
            'years_present': sorted(set(b[:4] for b in present)), 'cohorts': by_cohort,
            'batch_counts_in_batch_order': distribution,
            'batch_prevalence_in_batch_order': [n / m['accepted_rows'] if m['accepted_rows'] else None for m,n in zip(metrics,distribution)],
            'top_panel_cooccurrences': sorted(panel_pairs[token].items(), key=lambda p: (-p[1],p[0]))[:3],
            'cooccurrence_scope': 'candidate panel only; rows with nonempty exact document identifier',
            'lexical_family': token.split('_', 1)[0] if '_' in token else '(unprefixed)',
            'semantic_status': 'provider_example_unvalidated_extraction' if token in documented else 'unresolved',
            'documentation': documented.get(token, []),
            'historical_semantics': 'not established; zero is literal sampled absence only'})
    return {'schema_version': VERSION, 'batch_order': [m['batch_id'] for m in metrics],
            'batch_accepted_rows': [m['accepted_rows'] for m in metrics],
            'batch_empty_theme_rows': [m['empty_theme_rows'] for m in metrics],
            'accepted_rows': total, 'quarantined_rows': sum(m['quarantined_rows'] for m in metrics),
            'empty_theme_rows': sum(m['empty_theme_rows'] for m in metrics),
            'empty_field_rule': 'exclude empty delimiter fragments; retain all other exact strings without trimming',
            'entries': result}


def cooccurrence(metrics, panel):
    counts = Counter()
    for m in metrics:
        for rows in m['documents'].values():
            for tokens in rows:
                counts.update(combinations(sorted(set(tokens) & set(panel)), 2))
    return {'scope': 'selected panel, accepted rows with nonempty document identifier only',
            'pairs': [{'left': a, 'right': b, 'rows': counts[a, b]} for a, b in combinations(sorted(panel), 2)]}
