#!/usr/bin/env python3
"""Isolated GKG 2.1 structure validator. Network access requires --integration."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
import zlib

BASE_URL = 'https://data.gdeltproject.org/gdeltv2/'
LASTUPDATE_URL = BASE_URL + 'lastupdate.txt'
VERSION = '1.0.0'
EXPECTED_FIELDS = 27
MAX_ZIP_BYTES = 64 * 1024 * 1024
MAX_UNCOMPRESSED_BYTES = 512 * 1024 * 1024
MAX_LINE_BYTES = 8 * 1024 * 1024
URL_PATTERN = r'https?://data\.gdeltproject\.org/gdeltv2/[0-9]{14}\.gkg\.csv\.zip'


class Failure(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def fetch_bytes(url, limit=MAX_ZIP_BYTES):
    request = urllib.request.Request(url, headers={'User-Agent': 'Psychohistory-GKG/' + VERSION})
    with urllib.request.urlopen(request, timeout=60) as response:
        blob = response.read(limit + 1)
    if len(blob) > limit:
        raise Failure('resource_limit', 'Download exceeds byte limit')
    return blob


def discover_latest():
    raw = fetch_bytes(LASTUPDATE_URL, 1024 * 1024)
    try:
        text = raw.decode('utf-8')
    except UnicodeError as exc:
        raise Failure('metadata_encoding', 'Metadata is not UTF-8') from exc
    candidates = []
    for line in text.splitlines():
        if '.gkg.csv.zip' not in line:
            continue
        parts = line.split()
        if (len(parts) != 3 or not parts[0].isascii() or not parts[0].isdigit()
                or int(parts[0]) <= 0 or not re.fullmatch(r'[a-fA-F0-9]{32}', parts[1])
                or not re.fullmatch(URL_PATTERN, parts[2])):
            raise Failure('metadata_invalid', 'Invalid GKG metadata entry')
        candidates.append({'line': line, 'url': parts[2], 'bytes': int(parts[0]),
                           'md5': parts[1].lower(), 'sha256': hashlib.sha256(raw).hexdigest()})
    if len(candidates) != 1:
        raise Failure('metadata_invalid', 'Expected exactly one GKG metadata entry')
    return candidates[0]


def valid_date(value):
    if not re.fullmatch(r'[0-9]{14}', value):
        return False
    try:
        datetime.strptime(value, '%Y%m%d%H%M%S')
    except ValueError:
        return False
    return True


def parse_theme_field(value):
    # Preserve literal codes; only delimiters are removed. No ontology mapping.
    return [token for token in value.split(';') if token]


def new_statistics():
    return {'complete': False, 'rows': 0, 'valid_rows': 0, 'bad_rows': 0,
            'unknown_date_rows': 0, 'empty_theme_rows': 0,
            'field_count_distribution': {}, 'date_counts': {}, 'theme_counts': {},
            'row_error_counts': {}}


def validate_zip(blob):
    result = {'zip_bytes': len(blob), 'sha256': hashlib.sha256(blob).hexdigest(),
              'members': [], 'statistics': new_statistics(), 'errors': []}
    stats = result['statistics']
    fields, dates, themes, row_errors = Counter(), Counter(), Counter(), Counter()
    seen = set()
    try:
        if len(blob) > MAX_ZIP_BYTES:
            raise Failure('resource_limit', 'Archive exceeds byte limit')
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            members = [member for member in archive.infolist() if not member.is_dir()]
            result['members'] = [{'name': m.filename, 'compressed_bytes': m.compress_size,
                                  'uncompressed_bytes': m.file_size} for m in members]
            if len(members) != 1:
                raise Failure('zip_member_count', 'Expected one data member')
            member = members[0]
            if not member.filename.endswith('.gkg.csv'):
                raise Failure('zip_member_name', 'Expected a .gkg.csv member')
            if member.file_size > MAX_UNCOMPRESSED_BYTES:
                raise Failure('resource_limit', 'Uncompressed member exceeds byte limit')
            if member.flag_bits & 1:
                raise Failure('zip_encrypted', 'Encrypted archives are unsupported')
            total = 0
            with archive.open(member) as stream:
                while True:
                    raw = stream.readline(MAX_LINE_BYTES + 1)
                    if not raw:
                        break
                    total += len(raw)
                    if len(raw) > MAX_LINE_BYTES or total > MAX_UNCOMPRESSED_BYTES:
                        raise Failure('resource_limit', 'Expanded input exceeds byte limit')
                    line = raw.decode('utf-8')
                    row = line.rstrip('\r\n').split('\t')
                    stats['rows'] += 1
                    fields[str(len(row))] += 1
                    errors = []
                    if len(row) != EXPECTED_FIELDS:
                        errors.append('field_count')
                    else:
                        if not row[0]:
                            errors.append('missing_record_id')
                        elif row[0] in seen:
                            errors.append('duplicate_record_id')
                        seen.add(row[0])
                        if row[1] != '0' and not valid_date(row[1]):
                            errors.append('invalid_date')
                    if errors:
                        stats['bad_rows'] += 1
                        row_errors.update(errors)
                        continue
                    stats['valid_rows'] += 1
                    dates[row[1]] += 1
                    stats['unknown_date_rows'] += row[1] == '0'
                    codes = set(parse_theme_field(row[7]))
                    stats['empty_theme_rows'] += not codes
                    themes.update(codes)
            stats['complete'] = True
            if not stats['rows']:
                raise Failure('empty_data', 'Member has no rows')
            if stats['bad_rows']:
                raise Failure('invalid_rows', 'One or more rows failed structural validation')
    except Failure as exc:
        result['errors'].append({'code': exc.code, 'stage': 'validation', 'message': str(exc)})
    except UnicodeError:
        result['errors'].append({'code': 'invalid_encoding', 'stage': 'validation', 'message': 'Input is not UTF-8'})
    except (zipfile.BadZipFile, EOFError, zlib.error):
        result['errors'].append({'code': 'invalid_zip', 'stage': 'validation', 'message': 'Malformed archive or CRC failure'})
    except (NotImplementedError, RuntimeError):
        result['errors'].append({'code': 'unsupported_zip', 'stage': 'validation', 'message': 'Unsupported ZIP feature'})
    for name, counter in [('field_count_distribution', fields), ('date_counts', dates),
                          ('theme_counts', themes), ('row_error_counts', row_errors)]:
        stats[name] = dict(sorted(counter.items()))
    return result


def run_validation(*, input_path=None, url=None, integration=False, run_at=None):
    report = {'schema_version': '1.0.0', 'validator_version': VERSION,
              'validated_at': run_at or datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
              'source_id': 'gdelt-gkg-2.1', 'source_reference': str(input_path) if input_path else url,
              'discovery': None, 'status': 'failed', 'zip_bytes': None, 'sha256': None,
              'members': [], 'statistics': new_statistics(), 'errors': []}
    stage = 'acquisition'
    try:
        if input_path is not None:
            if url or integration:
                raise Failure('invalid_arguments', 'Local input cannot be combined with network options')
            with open(input_path, 'rb') as stream:
                blob = stream.read(MAX_ZIP_BYTES + 1)
        else:
            if not integration:
                raise Failure('integration_required', 'Use --input offline or --integration for live acquisition')
            if url is None:
                stage = 'discovery'
                report['discovery'] = discover_latest()
                url = report['discovery']['url']
            if not re.fullmatch(URL_PATTERN, url):
                raise Failure('invalid_url', 'Expected a GDELT GKG batch URL')
            report['source_reference'] = url
            stage = 'acquisition'
            blob = fetch_bytes(url)
        report['zip_bytes'] = len(blob)
        report['sha256'] = hashlib.sha256(blob).hexdigest()
        if len(blob) > MAX_ZIP_BYTES:
            raise Failure('resource_limit', 'Archive exceeds byte limit')
        if report['discovery']:
            meta = report['discovery']
            if len(blob) != meta['bytes'] or hashlib.md5(blob).hexdigest() != meta['md5']:
                raise Failure('metadata_mismatch', 'Downloaded bytes disagree with discovery size or MD5')
        stage = 'validation'
        report.update(validate_zip(blob))
        report['status'] = 'failed' if report['errors'] else 'passed'
    except Failure as exc:
        report['errors'].append({'code': exc.code, 'stage': stage, 'message': str(exc)})
    except urllib.error.HTTPError as exc:
        report['errors'].append({'code': 'http_error', 'stage': stage, 'message': f'HTTP {exc.code}'})
    except (urllib.error.URLError, TimeoutError, http.client.HTTPException) as exc:
        report['errors'].append({'code': 'network_error', 'stage': stage, 'message': str(exc)})
    except OSError as exc:
        report['errors'].append({'code': 'io_error', 'stage': stage, 'message': str(exc)})
    return report


def encode_report(report):
    return json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n'


def write_report(report, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='\n',
                                         dir=path.parent, delete=False) as stream:
            temporary = stream.name
            stream.write(encode_report(report))
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='Local ZIP; no network')
    parser.add_argument('--url', help='Explicit integration batch URL')
    parser.add_argument('--integration', action='store_true')
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('gkg_validation_report.json'))
    args = parser.parse_args(argv)
    report = run_validation(input_path=args.input, url=args.url, integration=args.integration)
    try:
        write_report(report, args.output)
    except OSError as exc:
        report['status'] = 'failed'
        report['errors'].append({'code': 'report_write_error', 'stage': 'report', 'message': str(exc)})
        print(encode_report(report), file=sys.stderr)
        return 4
    print(encode_report(report))
    if report['status'] == 'passed':
        return 0
    return 3 if any(e['stage'] == 'validation' for e in report['errors']) else 2


if __name__ == '__main__':
    raise SystemExit(main())
