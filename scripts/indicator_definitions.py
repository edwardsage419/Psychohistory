"""Source-independent definition contract and append-only identity checks."""
import json
from pathlib import Path
from contracts import validate, ContractError
from gkg_lossless import digest

SCHEMA = Path(__file__).resolve().parents[1] / 'schemas/indicator-definition.v1.schema.json'


def validate_definition(d):
    validate(d, json.loads(SCHEMA.read_text(encoding='utf-8')))
    for k in ('quality_requirements', 'known_biases', 'limitations', 'provenance_requirements', 'documentation'):
        if not d[k] or len(d[k]) != len(set(d[k])):
            raise ContractError(k, 'empty_or_duplicate_evidence')
    return d


def validate_registry(definitions, history, previous_history=None):
    if not definitions or not isinstance(history, dict):
        raise ContractError('$', 'empty_registry')
    if previous_history is not None and any(history.get(k) != v for k, v in previous_history.items()):
        raise ContractError('$', 'history_rewrite')
    seen = set()
    for d in definitions:
        validate_definition(d)
        key = d['indicator_id'] + '@' + d['version']
        if key in seen:
            raise ContractError('$', 'duplicate_definition')
        seen.add(key)
        if history.get(key) != digest(d):
            raise ContractError(key, 'definition_version_reuse')
    return definitions


def require_gkg_prevalence(d):
    validate_definition(d)
    # This adapter implements one declared capability; the definition model remains general.
    expected = {'source_family': 'GDELT', 'source_dataset': 'GKG 2.1 English-file family',
        'source_field': 'V1THEMES', 'unit': 'fraction', 'temporal_granularity': 'configurable UTC window',
        'geographic_scope': 'sampled collection; no geographic attribution', 'entity_scope': 'document rows',
        'normalization_method': 'numerator / denominator', 'denominator': 'all accepted rows',
        'aggregation_method': 'ratio of sums', 'missing_data_policy': 'null if any expected batch missing or denominator zero',
        'duplicate_policy': 'deduplicate tokens within row; retain repeated document identifiers',
        'smoothing_policy': 'none', 'lag_policy': 'batch timestamp; no inferred event or publication time',
        'status': 'experimental'}
    if any(d[k] != v for k, v in expected.items()):
        raise ContractError('$', 'unsupported_adapter_policy')
    t = d['transformation']
    if (t['method'] != 'exact_token_document_prevalence' or t['version'] != '1.0.0'
            or set(t['parameters']) != {'token'} or not t['parameters']['token'] or ';' in t['parameters']['token']):
        raise ContractError('transformation', 'unsupported_transform')
    return d
