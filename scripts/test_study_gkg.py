import contextlib
import copy
import io
import json
from pathlib import Path
import ssl
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import study_gkg as study
import validate_gkg as gkg
from test_validate_gkg import fixture, row


def manifest():
    return {'schema_version': '1.0.0', 'study_id': 'fixture-study', 'batches': [
        {'batch_id': stamp, 'cohort': cohort, 'url': gkg.BASE_URL + stamp + '.gkg.csv.zip'}
        for stamp, cohort in [('20260904000000', 'recent'), ('20150302000000', 'historical_2015')]]}


def fake_download(url):
    stamp = url.rsplit('/', 1)[1].split('.')[0]
    blob = fixture(row(record=stamp + '-1', date=stamp).encode(), names=(stamp + '.gkg.csv',))
    return blob, {'status': 200, 'effective_url': url, 'content_length': str(len(blob)),
                  'content_type': 'application/zip', 'last_modified': None, 'etag': None}


class StudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.batch = manifest()['batches'][0]

    def run_fixture(self, fetch=fake_download):
        with patch.object(study, 'SAMPLE_SIZE', 2), contextlib.redirect_stdout(io.StringIO()):
            return study.run_study(manifest(), self.root, integration=True, fetch=fetch)

    def test_exact_committed_sample(self):
        m = study.check_manifest(study.read_json(study.DEFAULT_MANIFEST))
        self.assertEqual(len(m['batches']), 96)
        self.assertEqual(sum(b['cohort'] == 'recent' for b in m['batches']), 72)
        self.assertEqual(len({b['batch_id'] for b in m['batches']}), 96)
        self.assertEqual(m['batches'][71]['batch_id'], '20260904174500')

    def test_manifest_rejections(self):
        for change in ('duplicate', 'url', 'timestamp', 'cohort', 'version', 'count'):
            m = manifest()
            if change == 'duplicate': m['batches'][1] = m['batches'][0]
            if change == 'url': m['batches'][0]['url'] = 'http://example.org/file'
            if change == 'timestamp': m['batches'][0]['batch_id'] = '20260904000100'
            if change == 'cohort': m['batches'][0]['cohort'] = '../raw'
            if change == 'version': m['schema_version'] = '2.0.0'
            if change == 'count': m['batches'].pop()
            with self.subTest(change=change), patch.object(study, 'SAMPLE_SIZE', 2), self.assertRaises(study.StudyError):
                study.check_manifest(m)

    def test_network_opt_in(self):
        with patch.object(study, 'SAMPLE_SIZE', 2), self.assertRaises(study.StudyError) as caught:
            study.run_study(manifest(), self.root)
        self.assertEqual(caught.exception.code, 'integration_required')

    def test_success_and_raw_preservation(self):
        result = study.attempt(self.batch, self.root, fake_download)
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['replay']['status'], 'passed')
        self.assertTrue((self.root / result['raw_path']).is_file())
        self.assertEqual(result['analysis']['integrity']['status'], 'passed')
        self.assertGreaterEqual(result['processing_seconds'], 0)

    def test_http_failure_taxonomy(self):
        for status, code in [(404, 'unavailable'), (410, 'unavailable'), (429, 'http_error'), (503, 'http_error')]:
            def fail(url): raise urllib.error.HTTPError(url, status, 'fixture', {}, None)
            result = study.attempt(self.batch, self.root, fail)
            self.assertEqual(result['errors'][0]['code'], code)
            self.assertEqual(result['errors'][0]['http_status'], status)
            self.assertEqual(result['acquisition'], 'failed')

    def test_network_and_tls_errors(self):
        for error, code in [(TimeoutError('fixture'), 'network_error'), (urllib.error.URLError('offline'), 'network_error'),
                            (urllib.error.URLError(ssl.SSLError('tls')), 'tls_error')]:
            def fail(url): raise error
            result = study.attempt(self.batch, self.root, fail)
            self.assertEqual(result['errors'][0]['code'], code)

    def test_bad_archive_retained_and_rejection_reproducible(self):
        result = study.attempt(self.batch, self.root, lambda url: (b'bad', {}))
        self.assertEqual(result['acquisition'], 'passed')
        self.assertEqual(result['analysis']['integrity']['status'], 'failed')
        self.assertEqual(result['replay']['status'], 'passed')
        self.assertIn('invalid_zip', [e['code'] for e in result['errors']])
        self.assertEqual((self.root / result['raw_path']).read_bytes(), b'bad')

    def test_timestamp_mismatch(self):
        blob = fixture(row(date='20260903000000').encode(), names=('wrong.gkg.csv',))
        result = study.attempt(self.batch, self.root, lambda url: (blob, {}))
        self.assertEqual(result['analysis']['timestamp_consistency']['mismatched_rows'], 1)
        self.assertIn('timestamp_mismatch', [e['code'] for e in result['errors']])

    def test_missing_theme_and_unknown_date(self):
        blob = fixture(row(date='0', themes='').encode(), names=(self.batch['batch_id'] + '.gkg.csv',))
        result = study.attempt(self.batch, self.root, lambda url: (blob, {}))
        self.assertEqual(result['analysis']['timestamp_consistency']['unknown_rows'], 1)
        self.assertEqual(result['analysis']['validation']['statistics']['empty_theme_rows'], 1)

    def test_replay_hash_mismatch(self):
        blob, _ = fake_download(self.batch['url'])
        path, _ = study.persist_raw(self.root, blob)
        _, result = study.replay(path, self.batch, '0' * 64)
        self.assertEqual(result['status'], 'failed')
        self.assertFalse(result['hash_matches_acquisition'])

    def test_cache_corruption_never_overwritten(self):
        blob, _ = fake_download(self.batch['url'])
        path, _ = study.persist_raw(self.root, blob)
        path.write_bytes(b'corrupt')
        with self.assertRaises(study.StudyError): study.persist_raw(self.root, blob)
        self.assertEqual(path.read_bytes(), b'corrupt')

    def test_storage_failure_remains_visible(self):
        with patch.object(study, 'persist_raw', side_effect=OSError('disk full')):
            result = study.attempt(self.batch, self.root, fake_download)
        self.assertEqual(result['acquisition'], 'passed')
        self.assertEqual(result['errors'][0]['stage'], 'storage')
        self.assertEqual(result['errors'][0]['code'], 'io_error')

    def test_duplicate_archives_count_without_dropping_slots(self):
        result = study.attempt(self.batch, self.root, fake_download)
        other = {**result, 'batch_id': '20260904001500'}
        summary = study.summarize([result, other])
        self.assertEqual(summary['counts']['scheduled'], 2)
        self.assertEqual(len(summary['duplicate_archive_hashes']), 1)
        self.assertEqual(len(summary['duplicate_member_hashes']), 1)

    def test_summary_denominators_and_storage(self):
        result = study.attempt(self.batch, self.root, fake_download)
        summary = study.summarize([result, study.pending(manifest()['batches'][1])])
        self.assertEqual(summary['acquisition_success_rate'], 0.5)
        self.assertEqual(summary['counts']['pending'], 1)
        self.assertEqual(summary['counts']['acquisition_failed'], 0)
        self.assertEqual(summary['storage_by_cohort']['recent']['extrapolated_bytes_per_365_days'], result['download_bytes'] * 96 * 365)
        self.assertIsNone(summary['storage_by_cohort']['historical_2015']['mean_zip_bytes'])

    def test_partial_counts_excluded_from_aggregate(self):
        blob = fixture(row().encode() + b'\xff', names=(self.batch['batch_id'] + '.gkg.csv',))
        result = study.attempt(self.batch, self.root, lambda url: (blob, {}))
        summary = study.summarize([result])
        self.assertEqual(summary['counts']['complete_scans'], 0)
        self.assertEqual(summary['counts']['rows'], 0)
        self.assertEqual(result['analysis']['validation']['statistics']['rows'], 1)

    def test_run_resume_and_offline_replay(self):
        first = self.run_fixture()
        def forbid(url): self.fail('resume must not redownload')
        second = self.run_fixture(forbid)
        self.assertEqual(first['summary'], second['summary'])
        with patch.object(study, 'SAMPLE_SIZE', 2), patch.object(study, 'download', side_effect=AssertionError('offline')):
            replay = study.replay_study(manifest(), self.root)
        self.assertEqual(replay['counts'], {'passed': 2})
        self.assertTrue(all(r['matches_original_semantics'] for r in replay['batches']))

    def test_interrupted_attempt_not_silently_retried(self):
        self.run_fixture()
        path = self.root / 'attempts' / (self.batch['batch_id'] + '.json')
        gkg.write_report({**study.pending(self.batch), 'state': 'started'}, path)
        report = self.run_fixture(lambda url: self.fail('must not retry'))
        self.assertEqual(report['summary']['counts']['interrupted'], 1)
        self.assertEqual(report['batches'][0]['errors'][0]['code'], 'interrupted')

    def test_resume_wrong_manifest(self):
        self.run_fixture()
        altered = manifest()
        altered['study_id'] = 'different'
        with patch.object(study, 'SAMPLE_SIZE', 2), self.assertRaises(study.StudyError):
            study.run_study(altered, self.root, True, fake_download)

    def test_replay_missing_raw(self):
        report = self.run_fixture()
        (self.root / report['batches'][0]['raw_path']).unlink()
        with patch.object(study, 'SAMPLE_SIZE', 2):
            result = study.replay_study(manifest(), self.root)
        self.assertEqual(result['counts'], {'failed': 1, 'passed': 1})

    def test_compaction_preserves_fingerprint(self):
        result = study.attempt(self.batch, self.root, fake_download)
        compact = study.compact(result)
        stats = compact['analysis']['validation']['statistics']
        self.assertEqual(stats['distinct_theme_tokens'], 2)
        self.assertEqual(stats['theme_counts_sha256'], study.digest({'TEST_A': 1, 'TEST_B': 1}))
        self.assertIn('theme_counts', result['analysis']['validation']['statistics'])

    def test_transport_length_failures(self):
        class Response(io.BytesIO):
            status = 200
            def geturl(self): return self_url
        self_url = self.batch['url']
        for header, body, expected in [('bogus', b'x', 'invalid_content_length'), ('10', b'x', 'truncated_response'),
                                       (str(gkg.MAX_ZIP_BYTES + 1), b'', 'resource_limit')]:
            response = Response(body)
            response.headers = {'Content-Length': header}
            with patch.object(study.urllib.request, 'build_opener') as opener:
                opener.return_value.open.return_value = response
                with self.assertRaises(study.StudyError) as caught: study.download(self_url)
            self.assertEqual(caught.exception.code, expected)

    def test_redirect_policy(self):
        for url in ('http://data.gdeltproject.org/gdeltv2/20260904000000.gkg.csv.zip', 'https://example.org/other'):
            with self.assertRaises(study.StudyError):
                study.StrictRedirect().redirect_request(None, None, 302, '', {}, url)

    def test_semantic_digest_excludes_runtime(self):
        one = study.attempt(self.batch, self.root, fake_download)
        two = study.attempt(self.batch, self.root, fake_download)
        self.assertEqual(one['replay']['first_semantic_sha256'], two['replay']['first_semantic_sha256'])
        self.assertEqual(one['analysis'], two['analysis'])


if __name__ == '__main__':
    unittest.main()
