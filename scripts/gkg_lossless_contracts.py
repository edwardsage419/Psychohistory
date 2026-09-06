"""Phase 3 contracts, separate names from immutable Phase 2 contracts."""
import json
from contracts import SCHEMAS, validate


def validate_record(kind, record):
    validate(record, json.loads((SCHEMAS / ('gkg-lossless-' + kind + '.v1.schema.json')).read_text(encoding='utf-8')))
    return record
