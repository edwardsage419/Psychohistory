"""Versioned JSON contracts using only the standard library.

This validates the deliberately small JSON Schema subset used in schemas/;
it is not a general JSON Schema implementation. Unknown keywords fail closed.
"""
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re

SCHEMAS = Path(__file__).resolve().parents[1] / 'schemas'
KEYWORDS = {'$schema', '$id', 'title', 'description', 'type', 'properties', 'required',
            'additionalProperties', 'items', 'enum', 'const', 'minimum', 'minLength',
            'pattern', 'format', 'anyOf'}


class ContractError(ValueError):
    def __init__(self, path, code):
        self.path, self.code = path, code
        super().__init__(f'{path}: {code}')


def validate(value, schema, path='$'):
    if set(schema) - KEYWORDS:
        raise ContractError(path, 'unsupported_schema_keyword')
    if 'anyOf' in schema:
        for branch in schema['anyOf']:
            try:
                validate(value, branch, path)
                return
            except ContractError:
                pass
        raise ContractError(path, 'any_of')
    kind = schema.get('type')
    matches = {'object': isinstance(value, dict), 'array': isinstance(value, list),
               'string': isinstance(value, str), 'integer': type(value) is int,
               'number': type(value) in (int, float), 'boolean': type(value) is bool,
               'null': value is None}
    if kind and not matches.get(kind, False):
        raise ContractError(path, 'type')
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError(path, 'non_finite')
    if 'const' in schema and value != schema['const']:
        raise ContractError(path, 'const')
    if 'enum' in schema and value not in schema['enum']:
        raise ContractError(path, 'enum')
    if kind == 'object':
        for field in schema.get('required', []):
            if field not in value:
                raise ContractError(path + '.' + field, 'required')
        properties = schema.get('properties', {})
        for field, child in value.items():
            if not isinstance(field, str):
                raise ContractError(path, 'non_string_key')
            if field in properties:
                validate(child, properties[field], path + '.' + field)
            elif schema.get('additionalProperties') is False:
                raise ContractError(path + '.' + field, 'unknown_field')
            elif isinstance(schema.get('additionalProperties'), dict):
                validate(child, schema['additionalProperties'], path + '.' + field)
    if kind == 'array':
        for i, child in enumerate(value):
            validate(child, schema.get('items', {}), f'{path}[{i}]')
    if kind == 'string':
        if len(value) < schema.get('minLength', 0):
            raise ContractError(path, 'min_length')
        if 'pattern' in schema and not re.search(schema['pattern'], value):
            raise ContractError(path, 'pattern')
        if schema.get('format') == 'date-time':
            try:
                parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
                if parsed.tzinfo is None or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-](?:[01][0-9]|2[0-3]):[0-5][0-9])', value):
                    raise ValueError()
            except ValueError:
                raise ContractError(path, 'date_time') from None
    if 'minimum' in schema and value < schema['minimum']:
        raise ContractError(path, 'minimum')


def validate_contract(name, value):
    schema = json.loads((SCHEMAS / f'{name}.v1.schema.json').read_text(encoding='utf-8'))
    validate(value, schema)
    if name == 'validation-report':
        stats = value['statistics']
        if stats['rows'] != stats['valid_rows'] + stats['bad_rows'] or sum(stats['field_count_distribution'].values()) != stats['rows']:
            raise ContractError('$.statistics', 'row_totals')
        if sum(stats['date_counts'].values()) != stats['valid_rows']:
            raise ContractError('$.statistics.date_counts', 'date_totals')
        if any(count > stats['valid_rows'] for count in stats['theme_counts'].values()):
            raise ContractError('$.statistics.theme_counts', 'theme_denominator')
        if any(stats[key] > stats['valid_rows'] for key in ('empty_theme_rows', 'unknown_date_rows')):
            raise ContractError('$.statistics', 'missingness_denominator')
        if (value['status'] == 'passed') != (not value['errors']):
            raise ContractError('$.status', 'error_status')
        if value['status'] == 'passed' and (not stats['complete'] or not stats['rows'] or stats['bad_rows'] or value['sha256'] is None):
            raise ContractError('$.status', 'incomplete_success')
    elif name == 'source-registry':
        ids = [source['source_id'] for source in value['sources']]
        if len(ids) != len(set(ids)):
            raise ContractError('$.sources', 'duplicate_source_id')
    elif name == 'observation':
        if (value['value'] is None) != (value['quality_status'] == 'missing'):
            raise ContractError('$.value', 'missing_value_status')
        if value['observation_id'] != observation_id(value):
            raise ContractError('$.observation_id', 'identity_mismatch')
    return value


def observation_id(observation):
    # Retrieval time is run metadata; identical observations across runs share identity.
    payload = {k: v for k, v in observation.items() if k not in ('observation_id', 'retrieved_at')}
    encoded = json.dumps(payload, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(encoded.encode('utf-8')).hexdigest()
