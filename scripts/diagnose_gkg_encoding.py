#!/usr/bin/env python3
"""Offline byte diagnostics for rejected study archives; no decoding fallback."""
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import zipfile
import sys

import study_gkg as study
import validate_gkg as gkg


def diagnose(path, expected_hash):
    blob = study.local_read(path)
    if hashlib.sha256(blob).hexdigest() != expected_hash:
        raise study.StudyError('raw_hash_mismatch', 'Diagnostic source differs from acquired bytes')
    result = {'sha256': expected_hash, 'lines': 0, 'utf8_rejected_lines': 0,
              'raw_field_count_distribution': {}, 'invalid_byte_samples': [], 'samples_truncated': False}
    fields = Counter()
    offset = 0
    with zipfile.ZipFile(io.BytesIO(blob)) as archive:
        members = [m for m in archive.infolist() if not m.is_dir()]
        if len(members) != 1 or members[0].file_size > gkg.MAX_UNCOMPRESSED_BYTES:
            raise study.StudyError('diagnostic_limit', 'Expected one bounded data member')
        with archive.open(members[0]) as stream:
            while True:
                raw = stream.readline(gkg.MAX_LINE_BYTES + 1)
                if not raw:
                    break
                if len(raw) > gkg.MAX_LINE_BYTES or offset + len(raw) > gkg.MAX_UNCOMPRESSED_BYTES:
                    raise study.StudyError('diagnostic_limit', 'Expanded input exceeds limit')
                result['lines'] += 1
                fields[str(len(raw.rstrip(b'\r\n').split(b'\t')))] += 1
                try:
                    raw.decode('utf-8')
                except UnicodeDecodeError as exc:
                    result['utf8_rejected_lines'] += 1
                    if len(result['invalid_byte_samples']) < 100:
                        result['invalid_byte_samples'].append({'line_number': result['lines'],
                            'uncompressed_byte_offset': offset + exc.start,
                            'field_number': raw[:exc.start].count(b'\t') + 1,
                            'invalid_bytes_hex': raw[exc.start:exc.end].hex(), 'reason': exc.reason})
                    else:
                        result['samples_truncated'] = True
                offset += len(raw)
    result['raw_field_count_distribution'] = dict(sorted(fields.items()))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    args = parser.parse_args()
    report = study.read_json(args.root / 'study.json')
    diagnostics = []
    for batch in report['batches']:
        if any(error['code'] == 'invalid_encoding' for error in batch['errors']):
            try:
                diagnostic = diagnose(args.root / 'raw' / (batch['sha256'] + '.zip'), batch['sha256'])
                diagnostics.append({'batch_id': batch['batch_id'], 'status': 'passed', 'errors': [], **diagnostic})
            except (OSError, ValueError, study.StudyError, zipfile.BadZipFile) as exc:
                diagnostics.append({'batch_id': batch['batch_id'], 'status': 'failed',
                                    'errors': [study.failure(getattr(exc, 'code', 'diagnostic_io_error'), 'study', exc)]})
    gkg.write_report({'schema_version': '1.0.0', 'scope': 'encoding-failed batches only; byte-level diagnostics, not normalized observations',
                      'manifest_sha256': report['manifest_sha256'], 'batches': diagnostics}, args.root / 'encoding-diagnostics.json')
    print([(b['batch_id'], b.get('lines'), b.get('utf8_rejected_lines')) for b in diagnostics])
    return 0 if all(b['status'] == 'passed' for b in diagnostics) else 2


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'failed', 'error': study.failure('diagnostic_io_error', 'study', exc)}), file=sys.stderr)
        raise SystemExit(3)
