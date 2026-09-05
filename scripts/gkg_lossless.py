#!/usr/bin/env python3
"""Offline, lossless GKG row disposition. No source data are repaired."""
from __future__ import annotations

import base64
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import zipfile
import zlib

import validate_gkg as legacy

PARSER_VERSION = '1.0.0'
CONTRACT_VERSION = '1.0.0'
MAX_ZIP_BYTES = 64 * 1024 * 1024
MAX_MEMBER_BYTES = 512 * 1024 * 1024
MAX_ROW_BYTES = 8 * 1024 * 1024
MAX_ROWS = 100_000
MAX_INVALID_SEQUENCES = 256
DISPOSITIONS = ('accepted', 'quarantined_encoding', 'quarantined_schema',
                'quarantined_timestamp', 'quarantined_resource', 'quarantined_other')


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def digest(value):
    return sha(canonical(value))


def error(code, detail):
    return {'code': code, 'detail': detail}


class Rejection(Exception):
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(code)


def read_snapshot(path):
    # A single descriptor/read produces immutable bytes. Even a concurrently
    # mutated file must match the externally pinned whole-archive SHA-256.
    with Path(path).open('rb') as stream:
        blob = stream.read(MAX_ZIP_BYTES + 1)
    if len(blob) > MAX_ZIP_BYTES:
        raise Rejection('archive_resource', 'ZIP exceeds configured byte bound')
    return blob


def _verified_member(blob, source):
    if sha(blob) != source['archive_sha256'] or len(blob) != source['archive_bytes']:
        raise Rejection('source_revision_mismatch', 'Archive hash or size differs from Phase 2')
    if source['acquisition'] != 'passed':
        raise Rejection('acquisition_not_passed', 'No successful source acquisition evidence')
    if source['source_url'] != legacy.BASE_URL + source['batch_id'] + '.gkg.csv.zip':
        raise Rejection('source_identity_mismatch', 'Batch URL differs from scheduled identity')
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        entries = archive.infolist()
        if len(entries) != 1 or entries[0].is_dir():
            raise Rejection('archive_member_count', 'Exactly one data member is required')
        member = entries[0]
        if member.filename != source['batch_id'] + '.gkg.csv':
            raise Rejection('archive_member_name', 'Member differs from scheduled batch')
        if member.flag_bits & 1:
            raise Rejection('archive_encrypted', 'Encrypted member is unsupported')
        if member.file_size > MAX_MEMBER_BYTES:
            raise Rejection('archive_resource', 'Expanded member exceeds configured byte bound')
        with archive.open(member) as stream:
            payload = stream.read(MAX_MEMBER_BYTES + 1)
        if len(payload) > MAX_MEMBER_BYTES:
            raise Rejection('archive_resource', 'Actual expanded bytes exceed bound')
        if len(payload) != member.file_size:
            raise Rejection('archive_size', 'Expanded size mismatch')
        if not payload:
            raise Rejection('empty_member', 'No physical rows')
        return member.filename, payload


def verified_member(blob, source):
    try:
        return _verified_member(blob, source)
    except (NotImplementedError, RuntimeError) as exc:
        raise Rejection('unsupported_archive', type(exc).__name__) from exc


def ranges(payload):
    start = 0
    while start < len(payload):
        end = payload.find(b'\n', start)
        end = len(payload) if end == -1 else end + 1
        yield start, end
        start = end


def body(raw):
    if raw.endswith(b'\n'):
        raw = raw[:-1]
        if raw.endswith(b'\r'):
            raw = raw[:-1]
    return raw


def encoding_errors(raw):
    errors, cursor = [], 0
    while cursor < len(raw):
        try:
            raw[cursor:].decode('utf-8', errors='strict')
            break
        except UnicodeDecodeError as exc:
            start, end = cursor + exc.start, cursor + exc.end
            errors.append({'start': start, 'end': end, 'bytes_hex': raw[start:end].hex(),
                           'field': raw[:start].count(b'\t') + 1, 'reason': exc.reason})
            cursor = end
            if len(errors) > MAX_INVALID_SEQUENCES:
                raise Rejection('row_diagnostic_resource', 'Invalid-sequence count exceeds diagnostic bound')
    return errors


def row_identity(record):
    return digest({k: record[k] for k in ('schema_version', 'parser_version', 'source',
                   'member', 'line', 'start', 'end', 'raw_sha256')})


def classify(raw, source, member, line, start, duplicate_ids):
    r = {'schema_version': CONTRACT_VERSION, 'parser_version': PARSER_VERSION,
         'source': source, 'member': member, 'line': line, 'start': start,
         'end': start + len(raw), 'raw_sha256': sha(raw), 'row_id': '',
         'disposition': 'accepted', 'reasons': [], 'invalid_sequences': [],
         'timestamp': None, 'fields_sha256': None, 'raw_base64': None}
    r['row_id'] = row_identity(r)
    fields = body(raw).split(b'\t')
    if len(fields) > 1:
        try:
            stamp = fields[1].decode('ascii')
            if legacy.valid_date(stamp):
                r['timestamp'] = stamp
        except UnicodeDecodeError:
            pass
    if len(raw) > MAX_ROW_BYTES:
        r['disposition'] = 'quarantined_resource'
        r['reasons'] = [error('row_resource', 'Physical row exceeds configured bound')]
    else:
        try:
            r['invalid_sequences'] = encoding_errors(raw)
        except Rejection as exc:
            r['disposition'] = 'quarantined_resource'
            r['reasons'] = [error(exc.code, exc.detail)]
        if r['disposition'] == 'quarantined_resource':
            pass
        elif r['invalid_sequences']:
            r['disposition'] = 'quarantined_encoding'
            r['reasons'] = [error('invalid_utf8', 'Strict UTF-8 rejected; no alternative decoding')]
        elif not raw.endswith(b'\n') or len(fields) != 27 or not fields[0]:
            r['disposition'] = 'quarantined_schema'
            r['reasons'] = ([error('unterminated_row', 'Final row has no LF terminator')] if not raw.endswith(b'\n') else [])
            if len(fields) != 27:
                r['reasons'].append(error('field_count', str(len(fields))))
            if not fields[0]:
                r['reasons'].append(error('missing_record_id', 'Empty record identifier'))
        elif r['timestamp'] != source['batch_id']:
            r['disposition'] = 'quarantined_timestamp'
            r['reasons'] = [error('timestamp_mismatch', 'Invalid, unknown or off-batch timestamp')]
        elif fields[0] in duplicate_ids:
            r['disposition'] = 'quarantined_other'
            r['reasons'] = [error('duplicate_record_id', 'All occurrences of repeated record ID quarantined')]
        else:
            r['fields_sha256'] = digest([f.decode('utf-8', errors='strict') for f in fields])
    if r['disposition'] != 'accepted':
        r['raw_base64'] = base64.b64encode(raw).decode('ascii')
    return r


def seal(result):
    result['semantic_sha256'] = digest({k: v for k, v in result.items() if k != 'semantic_sha256'})
    return result


def ingest(path, source):
    result = {'schema_version': CONTRACT_VERSION, 'parser_version': PARSER_VERSION,
              'source': source, 'observed_archive_sha256': None, 'archive_state': 'failed',
              'state': 'rejected', 'member': None, 'member_sha256': None,
              'member_bytes': 0, 'physical_rows': 0, 'accepted_rows': 0,
              'quarantined_rows': 0, 'quarantine_fraction': None,
              'disposition_counts': {}, 'rows': [], 'errors': [], 'semantic_sha256': ''}
    try:
        blob = read_snapshot(path)
        result['observed_archive_sha256'] = sha(blob)
        member, payload = verified_member(blob, source)
        result.update(archive_state='passed', member=member, member_sha256=sha(payload), member_bytes=len(payload))
        locators = []
        ids = Counter()
        for start, end in ranges(payload):
            if len(locators) >= MAX_ROWS:
                raise Rejection('batch_row_resource', 'Physical row count exceeds configured bound')
            locators.append((start, end))
            record_id = body(payload[start:end]).split(b'\t', 1)[0]
            if record_id:
                ids[record_id] += 1
        duplicate_ids = {key for key, count in ids.items() if count > 1}
        rows = [classify(payload[a:b], source, member, i, a, duplicate_ids)
                for i, (a, b) in enumerate(locators, 1)]
        counts = Counter(r['disposition'] for r in rows)
        accepted = counts['accepted']
        result.update(rows=rows, physical_rows=len(rows), accepted_rows=accepted,
                      quarantined_rows=len(rows) - accepted, disposition_counts=dict(sorted(counts.items())),
                      quarantine_fraction=(len(rows) - accepted) / len(rows),
                      state='clean_parse' if accepted == len(rows) else 'parse_with_quarantine')
        if not accepted:
            result['state'] = 'rejected'
            result['errors'] = [error('no_accepted_rows', 'No row eligible for partial acceptance')]
        seal(result)
        validate_batch(result, payload)
    except Rejection as exc:
        result['errors'] = [error(exc.code, exc.detail)]
    except (zipfile.BadZipFile, EOFError, zlib.error):
        result['errors'] = [error('invalid_archive', 'Malformed ZIP or CRC failure')]
    except OSError:
        result['errors'] = [error('source_io', 'Unable to read pinned source')]
    except Exception as exc:
        # Explicit machine-readable failure, never accept partial state. Do not
        # catch KeyboardInterrupt/SystemExit; a killed run cannot be certified.
        result['errors'] = [error('unexpected_exception', type(exc).__name__)]
    if result['errors'] and result['errors'][0]['code'] != 'no_accepted_rows':
        result.update(state='rejected', rows=[], physical_rows=0, accepted_rows=0,
                      quarantined_rows=0, quarantine_fraction=None, disposition_counts={})
    return seal(result)


def validate_batch(result, payload=None):
    """Recompute semantic evidence; never trust a status Boolean on its own."""
    from gkg_lossless_contracts import validate_record
    validate_record('batch', result)
    if result['semantic_sha256'] != digest({k: v for k, v in result.items() if k != 'semantic_sha256'}):
        raise Rejection('semantic_hash_mismatch', 'Batch semantic fingerprint contradicts content')
    rows = result['rows']
    accepted = sum(r['disposition'] == 'accepted' for r in rows)
    if (result['physical_rows'] != len(rows) or result['accepted_rows'] != accepted
            or result['quarantined_rows'] != len(rows) - accepted
            or result['disposition_counts'] != dict(sorted(Counter(r['disposition'] for r in rows).items()))):
        raise Rejection('row_accounting', 'Disposition counts contradict ledger')
    if result['quarantine_fraction'] != ((len(rows) - accepted) / len(rows) if rows else None):
        raise Rejection('row_accounting', 'Quarantine fraction contradicts ledger')
    if result['state'] == 'rejected':
        if not result['errors'] or accepted:
            raise Rejection('inconsistent_state', 'Rejected batch needs errors and zero accepted rows')
    elif result['errors'] or not rows or not accepted or result['archive_state'] != 'passed':
        raise Rejection('inconsistent_state', 'Eligible batch contradicts its evidence')
    if result['state'] == 'clean_parse' and accepted != len(rows):
        raise Rejection('inconsistent_state', 'Clean batch has quarantine')
    if result['state'] == 'parse_with_quarantine' and accepted == len(rows):
        raise Rejection('inconsistent_state', 'Quarantine batch has no quarantine')
    if result['archive_state'] == 'passed' and (result['source']['acquisition'] != 'passed'
            or result['source']['source_url'] != legacy.BASE_URL + result['source']['batch_id'] + '.gkg.csv.zip'
            or result['observed_archive_sha256'] != result['source']['archive_sha256']
            or not result['member_sha256'] or result['member'] != result['source']['batch_id'] + '.gkg.csv'):
        raise Rejection('source_revision_mismatch', 'Integrity state contradicts source identity')
    duplicate_ids = set()
    if payload is not None:
        ids = Counter(body(payload[a:b]).split(b'\t', 1)[0] for a, b in ranges(payload))
        duplicate_ids = {key for key, count in ids.items() if key and count > 1}
    end = 0
    for i, r in enumerate(rows, 1):
        if r['source'] != result['source'] or r['member'] != result['member'] or r['line'] != i or r['start'] != end or r['end'] <= r['start'] or r['row_id'] != row_identity(r):
            raise Rejection('row_provenance', 'Invalid row identity or byte range')
        end = r['end']
        if r['disposition'] == 'accepted':
            if r['reasons'] or r['invalid_sequences'] or r['raw_base64'] is not None or r['fields_sha256'] is None or r['timestamp'] != result['source']['batch_id']:
                raise Rejection('inconsistent_row', 'Accepted row contradicts evidence')
        else:
            validate_record('quarantine', r)
            if not r['reasons'] or r['fields_sha256'] is not None:
                raise Rejection('missing_failure_code', 'Quarantine needs reasons and no accepted field hash')
            raw = base64.b64decode(r['raw_base64'], validate=True)
            if sha(raw) != r['raw_sha256'] or len(raw) != r['end'] - r['start']:
                raise Rejection('quarantine_bytes', 'Quarantine bytes contradict row fingerprint')
        if payload is not None:
            raw = payload[r['start']:r['end']]
            if r != classify(raw, result['source'], result['member'], i, r['start'], duplicate_ids):
                raise Rejection('row_provenance', 'Disposition differs from verified bytes')
            if sha(raw) != r['raw_sha256']:
                raise Rejection('row_provenance', 'Row differs from verified member')
            if r['disposition'] == 'accepted' and digest([f.decode('utf-8') for f in body(raw).split(b'\t')]) != r['fields_sha256']:
                raise Rejection('row_provenance', 'Accepted fields contradict verified bytes')
    if rows and end != result['member_bytes']:
        raise Rejection('row_accounting', 'Ledger does not cover entire member')
    return result
