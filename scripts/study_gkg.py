#!/usr/bin/env python3
"""Bounded GKG study. Acquisition needs --integration; replay never uses network."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import http.client
import io
import json
from pathlib import Path
import platform
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
import zipfile
import zlib

import validate_gkg as gkg

VERSION = '1.0.0'
SAMPLE_SIZE = 96
DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / 'studies/gkg-continuity-v1/manifest.json'


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':'), allow_nan=False).encode('utf-8')).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def failure(code, stage, message, http_status=None):
    return {'code': code, 'stage': stage, 'message': str(message), 'http_status': http_status}


class StudyError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def check_manifest(manifest):
    if not isinstance(manifest, dict) or set(manifest) != {'schema_version', 'study_id', 'batches'} or manifest['schema_version'] != VERSION:
        raise StudyError('invalid_manifest', 'Unsupported manifest shape/version')
    if not isinstance(manifest['study_id'], str) or not re.fullmatch(r'[a-z0-9-]+', manifest['study_id']):
        raise StudyError('invalid_manifest', 'Invalid study ID')
    if not isinstance(manifest['batches'], list) or len(manifest['batches']) != SAMPLE_SIZE:
        raise StudyError('invalid_manifest', f'Expected {SAMPLE_SIZE} batches')
    seen = set()
    for batch in manifest['batches']:
        if not isinstance(batch, dict) or set(batch) != {'batch_id', 'cohort', 'url'}:
            raise StudyError('invalid_manifest', 'Invalid batch fields')
        stamp = batch['batch_id']
        if not isinstance(stamp, str) or not gkg.valid_date(stamp) or stamp[12:] != '00' or int(stamp[10:12]) % 15:
            raise StudyError('invalid_manifest', 'Batch timestamp must be a quarter hour')
        if stamp in seen or batch['url'] != gkg.BASE_URL + stamp + '.gkg.csv.zip':
            raise StudyError('invalid_manifest', 'Duplicate timestamp or mismatched HTTPS URL')
        if not isinstance(batch['cohort'], str) or not re.fullmatch(r'[a-z0-9_]+', batch['cohort']):
            raise StudyError('invalid_manifest', 'Invalid cohort')
        seen.add(stamp)
    return manifest


class StrictRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Never silently change provider or downgrade TLS.
        if not re.fullmatch(gkg.URL_PATTERN.replace('https?', 'https'), newurl):
            raise StudyError('unsafe_redirect', 'Redirect left the GDELT HTTPS batch endpoint')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(url):
    """One bounded request. Complete bodies only; no retries or HTTP fallback."""
    request = urllib.request.Request(url, headers={'User-Agent': 'Psychohistory-GKG-Study/' + VERSION})
    opener = urllib.request.build_opener(StrictRedirect())
    with opener.open(request, timeout=30) as response:
        metadata = {'status': response.status, 'effective_url': response.geturl(),
                    'content_length': response.headers.get('Content-Length'),
                    'content_type': response.headers.get('Content-Type'),
                    'last_modified': response.headers.get('Last-Modified'),
                    'etag': response.headers.get('ETag')}
        if response.status != 200:
            raise StudyError('unexpected_http_status', f'HTTP {response.status}')
        size = metadata['content_length']
        if size is not None and (not re.fullmatch(r'[0-9]{1,20}', size)):
            raise StudyError('invalid_content_length', 'Malformed Content-Length')
        if size is not None and int(size) > gkg.MAX_ZIP_BYTES:
            raise StudyError('resource_limit', 'Declared response exceeds ZIP limit')
        blob = response.read(gkg.MAX_ZIP_BYTES + 1)
        if len(blob) > gkg.MAX_ZIP_BYTES:
            raise StudyError('resource_limit', 'Response exceeds ZIP limit')
        if size is not None and int(size) != len(blob):
            raise StudyError('truncated_response', 'Body size disagrees with Content-Length')
    return blob, metadata


def integrity(blob):
    """Hash decompressed bytes while checking CRC without trusting ZIP sizes alone."""
    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as archive:
            members = [m for m in archive.infolist() if not m.is_dir()]
            if len(members) != 1:
                return {'status': 'not_checked', 'content_sha256': None, 'code': 'zip_member_count'}
            member = members[0]
            if member.file_size > gkg.MAX_UNCOMPRESSED_BYTES or member.flag_bits & 1:
                return {'status': 'not_checked', 'content_sha256': None, 'code': 'resource_or_encryption'}
            total, hashed = 0, hashlib.sha256()
            with archive.open(member) as stream:
                while True:
                    chunk = stream.read(1024 * 1024)
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > gkg.MAX_UNCOMPRESSED_BYTES:
                        return {'status': 'not_checked', 'content_sha256': None, 'code': 'resource_limit'}
                    hashed.update(chunk)
            return {'status': 'passed', 'content_sha256': hashed.hexdigest(), 'code': None}
    except (zipfile.BadZipFile, EOFError, zlib.error):
        return {'status': 'failed', 'content_sha256': None, 'code': 'invalid_zip'}
    except (NotImplementedError, RuntimeError, OSError):
        return {'status': 'not_checked', 'content_sha256': None, 'code': 'unsupported_zip'}


def analyze(blob, batch):
    validation = gkg.validate_zip(blob)
    stats = validation['statistics']
    mismatches = sum(count for stamp, count in stats['date_counts'].items()
                     if stamp not in (batch['batch_id'], '0'))
    member_matches = (len(validation['members']) == 1 and
                      validation['members'][0]['name'] == batch['batch_id'] + '.gkg.csv')
    return {'validator_version': gkg.VERSION, 'validation': validation, 'integrity': integrity(blob),
            'timestamp_consistency': {'scope': 'valid_rows_only', 'complete': stats['complete'],
                                      'unknown_rows': stats['unknown_date_rows'],
                                      'mismatched_rows': mismatches, 'member_name_matches': member_matches}}


def local_read(path):
    with Path(path).open('rb') as stream:
        blob = stream.read(gkg.MAX_ZIP_BYTES + 1)
    if len(blob) > gkg.MAX_ZIP_BYTES:
        raise StudyError('resource_limit', 'Local archive exceeds ZIP limit')
    return blob


def replay(path, batch, expected_hash):
    first_blob = local_read(path)
    first = analyze(first_blob, batch)
    second_blob = local_read(path)
    second = analyze(second_blob, batch)
    raw_first = hashlib.sha256(first_blob).hexdigest()
    raw_second = hashlib.sha256(second_blob).hexdigest()
    first_hash, second_hash = digest(first), digest(second)
    return first, {'status': 'passed' if raw_first == raw_second == expected_hash and first_hash == second_hash else 'failed',
                   'first_raw_sha256': raw_first, 'second_raw_sha256': raw_second,
                   'first_semantic_sha256': first_hash, 'second_semantic_sha256': second_hash,
                   'hash_matches_acquisition': raw_first == raw_second == expected_hash,
                   'semantic_equal': first_hash == second_hash}


def persist_raw(root, blob):
    checksum = hashlib.sha256(blob).hexdigest()
    path = root / 'raw' / (checksum + '.zip')
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if hashlib.sha256(local_read(path)).hexdigest() != checksum:
            raise StudyError('raw_cache_corrupt', 'Existing content-addressed archive is corrupt')
    else:
        # Exclusive creation prevents replacement of existing evidence.
        with path.open('xb') as stream:
            stream.write(blob)
    return path, checksum


def attempt(batch, root, fetch=download):
    result = {**batch, 'state': 'complete', 'acquisition': 'failed', 'started_at': now(),
              'finished_at': None, 'download_seconds': None, 'processing_seconds': None,
              'transport': None, 'raw_path': None, 'sha256': None, 'download_bytes': None,
              'analysis': None, 'replay': None, 'errors': []}
    started = time.perf_counter()
    processing_start = None
    stage = 'acquisition'
    try:
        blob, result['transport'] = fetch(batch['url'])
        result['download_seconds'] = time.perf_counter() - started
        result['acquisition'] = 'passed'
        result['download_bytes'] = len(blob)
        result['sha256'] = hashlib.sha256(blob).hexdigest()
        stage = 'storage'
        processing_start = time.perf_counter()
        path, checksum = persist_raw(root, blob)
        result['raw_path'] = path.relative_to(root).as_posix()
        stage = 'replay'
        result['analysis'], result['replay'] = replay(path, batch, checksum)
        result['processing_seconds'] = time.perf_counter() - processing_start
        for error in result['analysis']['validation']['errors']:
            result['errors'].append(failure(error['code'], 'validation', error['message']))
        if result['analysis']['integrity']['status'] != 'passed':
            result['errors'].append(failure('integrity_not_passed', 'validation', result['analysis']['integrity']['code']))
        timestamps = result['analysis']['timestamp_consistency']
        if timestamps['mismatched_rows'] or not timestamps['member_name_matches']:
            result['errors'].append(failure('timestamp_mismatch', 'validation', 'Unexpected row timestamp or member name'))
        if result['replay']['status'] != 'passed':
            result['errors'].append(failure('replay_mismatch', 'replay', 'Raw or semantic comparison disagrees'))
    except urllib.error.HTTPError as exc:
        code = 'unavailable' if exc.code in (404, 410) else 'http_error'
        result['errors'].append(failure(code, stage, f'HTTP {exc.code}', exc.code))
    except urllib.error.URLError as exc:
        code = 'tls_error' if isinstance(exc.reason, ssl.SSLError) else 'network_error'
        result['errors'].append(failure(code, stage, exc.reason))
    except ssl.SSLError as exc:
        result['errors'].append(failure('tls_error', stage, exc))
    except (TimeoutError, http.client.HTTPException) as exc:
        result['errors'].append(failure('network_error', stage, exc))
    except StudyError as exc:
        result['errors'].append(failure(exc.code, stage, exc))
    except OSError as exc:
        result['errors'].append(failure('io_error', stage, exc))
    finally:
        if processing_start is not None and result['processing_seconds'] is None:
            result['processing_seconds'] = time.perf_counter() - processing_start
        if result['download_seconds'] is None:
            result['download_seconds'] = time.perf_counter() - started
        result['finished_at'] = now()
    return result


def pending(batch):
    return {**batch, 'state': 'pending', 'acquisition': 'not_attempted', 'errors': []}


def run_identity(manifest):
    return {'manifest_sha256': digest(manifest), 'study_version': VERSION, 'validator_version': gkg.VERSION,
            'study_code_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'validator_code_sha256': hashlib.sha256(Path(gkg.__file__).read_bytes()).hexdigest()}


def compact(result):
    result = json.loads(json.dumps(result))
    analysis = result.get('analysis')
    if analysis:
        tokens = analysis['validation']['statistics'].pop('theme_counts')
        analysis['validation']['statistics']['distinct_theme_tokens'] = len(tokens)
        analysis['validation']['statistics']['theme_counts_sha256'] = digest(tokens)
    return result


def summarize(results):
    counts = Counter()
    failures, fields, dates, themes = Counter(), Counter(), Counter(), Counter()
    cohorts = defaultdict(list)
    raw_hashes, content_hashes = defaultdict(list), defaultdict(list)
    for r in results:
        counts['scheduled'] += 1
        counts[r['state']] += 1
        counts['acquired'] += r['acquisition'] == 'passed'
        cohorts[r['cohort']].append(r)
        failures.update({error['code'] for error in r['errors']})
        if r.get('sha256'):
            raw_hashes[r['sha256']].append(r['batch_id'])
        analysis = r.get('analysis')
        if not analysis:
            continue
        stats = analysis['validation']['statistics']
        counts['integrity_passed'] += analysis['integrity']['status'] == 'passed'
        counts['parsing_passed'] += not analysis['validation']['errors']
        counts['replay_passed'] += r['replay']['status'] == 'passed'
        counts['timestamp_mismatch_batches'] += bool(analysis['timestamp_consistency']['mismatched_rows'] or not analysis['timestamp_consistency']['member_name_matches'])
        if analysis['integrity']['content_sha256']:
            content_hashes[analysis['integrity']['content_sha256']].append(r['batch_id'])
        if stats['complete']:
            counts['complete_scans'] += 1
            for key in ('rows', 'valid_rows', 'bad_rows', 'empty_theme_rows', 'unknown_date_rows'):
                counts[key] += stats[key]
            fields.update(stats['field_count_distribution'])
            dates.update(stats['date_counts'])
            themes.update(stats['theme_counts'])
    for key in ('complete', 'pending', 'interrupted', 'acquired', 'integrity_passed', 'parsing_passed',
                'replay_passed', 'complete_scans', 'rows', 'valid_rows', 'bad_rows', 'empty_theme_rows',
                'unknown_date_rows', 'timestamp_mismatch_batches'):
        counts.setdefault(key, 0)
    counts['acquisition_failed'] = counts['complete'] - counts['acquired']
    duplicates = {key: ids for key, ids in raw_hashes.items() if len(ids) > 1}
    content_duplicates = {key: ids for key, ids in content_hashes.items() if len(ids) > 1}
    volumes = {}
    for cohort, records in sorted(cohorts.items()):
        sizes = [r['download_bytes'] for r in records if r['acquisition'] == 'passed']
        mean = sum(sizes) / len(sizes) if sizes else None
        volumes[cohort] = {'scheduled': len(records), 'acquired': len(sizes),
                           'total_measured_zip_bytes': sum(sizes),
                           'mean_zip_bytes': mean, 'min_zip_bytes': min(sizes) if sizes else None,
                           'max_zip_bytes': max(sizes) if sizes else None,
                           'extrapolated_bytes_per_day': mean * 96 if mean is not None else None,
                           'extrapolated_bytes_per_30_days': mean * 96 * 30 if mean is not None else None,
                           'extrapolated_bytes_per_365_days': mean * 96 * 365 if mean is not None else None}
    return {'counts': dict(counts), 'acquisition_success_rate': counts['acquired'] / len(results) if results else None,
            'failure_batches_by_code': dict(sorted(failures.items())),
            'unavailable_batch_ids': [r['batch_id'] for r in results if any(e['code'] == 'unavailable' for e in r['errors'])],
            'duplicate_archive_hashes': duplicates, 'duplicate_member_hashes': content_duplicates,
            'field_count_distribution_complete_scans': dict(sorted(fields.items())),
            'date_counts_valid_rows_complete_scans': dict(sorted(dates.items())),
            'theme_counts_valid_rows_complete_scans': dict(sorted(themes.items())),
            'distinct_theme_tokens_complete_scans': len(themes),
            'empty_theme_fraction_valid_rows': counts['empty_theme_rows'] / counts['valid_rows'] if counts['valid_rows'] else None,
            'storage_by_cohort': volumes}


def run_study(manifest, root, integration=False, fetch=download):
    check_manifest(manifest)
    if not integration:
        raise StudyError('integration_required', 'Acquisition requires --integration')
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    identity = run_identity(manifest)
    metadata_path = root / 'run.json'
    if metadata_path.exists():
        metadata = read_json(metadata_path)
        if metadata['identity'] != identity:
            raise StudyError('resume_mismatch', 'Manifest or code version differs from existing run')
    else:
        metadata = {'identity': identity, 'started_at': now(), 'python': platform.python_version(),
                    'platform': platform.platform(), 'policy': 'one HTTPS attempt per slot; no retries',
                    'socket_timeout_seconds': 30, 'max_zip_bytes': gkg.MAX_ZIP_BYTES}
        gkg.write_report(metadata, metadata_path)
    (root / 'attempts').mkdir(exist_ok=True)
    results = []
    for batch in manifest['batches']:
        path = root / 'attempts' / (batch['batch_id'] + '.json')
        if path.exists():
            result = read_json(path)
            if any(result.get(k) != batch[k] for k in batch):
                raise StudyError('resume_mismatch', 'Attempt does not match scheduled batch')
            if result['state'] == 'started':
                result = {**pending(batch), 'state': 'interrupted',
                          'errors': [failure('interrupted', 'acquisition', 'Previous attempt did not finish; no silent retry')]}
                gkg.write_report(result, path)
        else:
            gkg.write_report({**pending(batch), 'state': 'started'}, path)
            result = attempt(batch, root, fetch)
            gkg.write_report(result, path)
        results.append(result)
        report = {'schema_version': VERSION, 'study_id': manifest['study_id'], 'manifest_sha256': digest(manifest),
                  'run': metadata, 'finished_at': now(), 'summary': summarize(results + [pending(b) for b in manifest['batches'][len(results):]]),
                  'batches': [compact(r) for r in results] + [pending(b) for b in manifest['batches'][len(results):]]}
        gkg.write_report(report, root / 'study.json')
        print(f'{len(results)}/{SAMPLE_SIZE} {batch["batch_id"]}: {result["acquisition"]}; errors={[e["code"] for e in result["errors"]]}', flush=True)
    return report


def replay_study(manifest, root):
    check_manifest(manifest)
    root = Path(root)
    metadata = read_json(root / 'run.json')
    if metadata['identity'] != run_identity(manifest):
        raise StudyError('resume_mismatch', 'Replay manifest/code version differs')
    comparisons = []
    for batch in manifest['batches']:
        item = {'batch_id': batch['batch_id'], 'status': 'not_available', 'errors': []}
        try:
            previous = read_json(root / 'attempts' / (batch['batch_id'] + '.json'))
            if not previous.get('raw_path') or not previous.get('analysis'):
                item['errors'].append(failure('raw_unavailable', 'replay', 'No complete stored analysis for this slot'))
            else:
                raw_path = root / 'raw' / (previous['sha256'] + '.zip')
                analysis, check = replay(raw_path, batch, previous['sha256'])
                item.update(check)
                item['matches_original_semantics'] = digest(analysis) == digest(previous['analysis'])
                if not item['matches_original_semantics']:
                    item['status'] = 'failed'
                    item['errors'].append(failure('replay_mismatch', 'replay', 'Stored analysis differs from replay'))
        except (OSError, ValueError, StudyError) as exc:
            item['status'] = 'failed'
            item['errors'].append(failure(getattr(exc, 'code', 'replay_io_error'), 'replay', exc))
        comparisons.append(item)
    return {'schema_version': VERSION, 'study_id': manifest['study_id'], 'manifest_sha256': digest(manifest),
            'replayed_at': now(), 'counts': dict(Counter(c['status'] for c in comparisons)), 'batches': comparisons}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument('--root', type=Path, required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--integration', action='store_true')
    group.add_argument('--replay', action='store_true')
    args = parser.parse_args(argv)
    try:
        manifest = read_json(args.manifest)
        if args.replay:
            report = replay_study(manifest, args.root)
            gkg.write_report(report, args.root / 'replay.json')
            print(json.dumps(report['counts']))
            return 0 if report['counts'].get('passed') == SAMPLE_SIZE else 2
        report = run_study(manifest, args.root, args.integration)
        return 0 if all(b['state'] == 'complete' and not b['errors'] for b in report['batches']) else 2
    except (OSError, ValueError, StudyError) as exc:
        print(json.dumps({'status': 'failed', 'error': failure(getattr(exc, 'code', 'study_io_error'), 'study', exc)}), file=sys.stderr)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())
