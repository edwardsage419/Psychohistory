import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import zipfile

import validate_gkg as gkg

STAMP = '2026-09-06T00:00:00Z'
URL = gkg.BASE_URL + '20260906000000.gkg.csv.zip'


def row(record='record-1', date='20260906000000', themes='TEST_A;TEST_B;'):
    return '\t'.join([record, date, '1', 'example.org', 'https://example.org/a', '', '', themes] + [''] * 19) + '\n'


def fixture(payload=None, names=('sample.gkg.csv',)):
    payload = row().encode() if payload is None else payload
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_STORED) as archive:
        for name in names:
            archive.writestr(zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0)), payload)
    return buffer.getvalue()


class ValidatorTests(unittest.TestCase):
    def code(self, blob):
        return gkg.validate_zip(blob)['errors'][0]['code']

    def test_valid_and_repeatable(self):
        blob = fixture((row() + row('record-2', themes='TEST_A;')).encode())
        first = gkg.validate_zip(blob)
        self.assertEqual(first, gkg.validate_zip(blob))
        self.assertEqual(first['errors'], [])
        self.assertEqual(first['statistics']['theme_counts'], {'TEST_A': 2, 'TEST_B': 1})
        self.assertEqual(first['statistics']['field_count_distribution'], {'27': 2})
        self.assertTrue(first['statistics']['complete'])
        self.assertEqual(blob, fixture((row() + row('record-2', themes='TEST_A;')).encode()))

    def test_bad_zip(self):
        self.assertEqual(self.code(b'not a zip'), 'invalid_zip')

    def test_truncated_zip(self):
        self.assertEqual(self.code(fixture()[:-20]), 'invalid_zip')

    def test_crc_failure(self):
        blob = bytearray(fixture())
        blob[blob.index(b'record-1')] ^= 1
        self.assertEqual(self.code(bytes(blob)), 'invalid_zip')

    def test_member_cardinality(self):
        for names in [(), ('a.gkg.csv', 'b.gkg.csv')]:
            with self.subTest(names=names):
                self.assertEqual(self.code(fixture(names=names)), 'zip_member_count')

    def test_directory_ignored(self):
        self.assertEqual(gkg.validate_zip(fixture(names=('folder/', 'a.gkg.csv')))['errors'], [])

    def test_wrong_member(self):
        self.assertEqual(self.code(fixture(names=('a.txt',))), 'zip_member_name')

    def test_empty(self):
        self.assertEqual(self.code(fixture(b'')), 'empty_data')

    def test_field_counts(self):
        for count in (1, 8, 12, 26, 28):
            with self.subTest(count=count):
                result = gkg.validate_zip(fixture(('\t'.join(['x'] * count) + '\n').encode()))
                self.assertEqual(result['statistics']['bad_rows'], 1)
                self.assertEqual(result['statistics']['row_error_counts'], {'field_count': 1})
                self.assertEqual(result['statistics']['theme_counts'], {})

    def test_invalid_dates(self):
        for date in ('20260230000000', '20260906240000', '20260906', '', '2026090600000x'):
            with self.subTest(date=date):
                result = gkg.validate_zip(fixture(row(date=date).encode()))
                self.assertEqual(result['statistics']['row_error_counts'], {'invalid_date': 1})

    def test_unknown_date_and_leap_day(self):
        for date in ('0', '20240229000000'):
            with self.subTest(date=date):
                result = gkg.validate_zip(fixture(row(date=date).encode()))
                self.assertEqual(result['errors'], [])
                self.assertEqual(result['statistics']['unknown_date_rows'], int(date == '0'))

    def test_empty_themes_valid(self):
        result = gkg.validate_zip(fixture(row(themes='').encode()))
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['statistics']['empty_theme_rows'], 1)

    def test_theme_presence_and_literal_codes(self):
        result = gkg.validate_zip(fixture(row(themes='TEST_A;TEST_A; TEST_A;').encode()))
        self.assertEqual(result['statistics']['theme_counts'], {' TEST_A': 1, 'TEST_A': 1})

    def test_invalid_utf8(self):
        self.assertEqual(self.code(fixture(row().encode() + b'\xff')), 'invalid_encoding')

    def test_unicode_quotes_and_large_field(self):
        payload = row(themes='测试;').rstrip('\n').split('\t')
        payload[26] = '"' + 'x' * 150000
        result = gkg.validate_zip(fixture(('\t'.join(payload) + '\n').encode()))
        self.assertEqual(result['errors'], [])
        self.assertEqual(result['statistics']['rows'], 1)

    def test_duplicate_and_missing_ids(self):
        result = gkg.validate_zip(fixture((row() + row() + row(record='')).encode()))
        self.assertEqual(result['statistics']['bad_rows'], 2)
        self.assertEqual(result['statistics']['valid_rows'], 1)
        self.assertEqual(result['statistics']['row_error_counts'], {'duplicate_record_id': 1, 'missing_record_id': 1})

    def test_resource_limits(self):
        for setting in ('MAX_ZIP_BYTES', 'MAX_UNCOMPRESSED_BYTES', 'MAX_LINE_BYTES'):
            with self.subTest(setting=setting), patch.object(gkg, setting, 10):
                self.assertEqual(self.code(fixture()), 'resource_limit')

    def test_network_opt_in(self):
        with patch.object(gkg, 'fetch_bytes') as fetch:
            report = gkg.run_validation(run_at=STAMP)
            self.assertEqual(report['errors'][0]['code'], 'integration_required')
            fetch.assert_not_called()

    def test_metadata_failures(self):
        for metadata, expected in [(b'\xff', 'metadata_encoding'), (b'', 'metadata_invalid'),
                                   (b'wrong.gkg.csv.zip', 'metadata_invalid'),
                                   (b'1 xx ' + URL.encode(), 'metadata_invalid')]:
            with self.subTest(metadata=metadata), patch.object(gkg, 'fetch_bytes', return_value=metadata):
                report = gkg.run_validation(integration=True, run_at=STAMP)
                self.assertEqual(report['errors'][0]['code'], expected)
                self.assertEqual(report['errors'][0]['stage'], 'discovery')

    def test_http_and_network_failures(self):
        for url, stage in [(None, 'discovery'), (URL, 'acquisition')]:
            for error, code in [(urllib.error.HTTPError(URL, 429, 'limit', {}, None), 'http_error'),
                                (urllib.error.URLError('offline'), 'network_error'),
                                (TimeoutError('timeout'), 'network_error')]:
                with self.subTest(stage=stage, code=code), patch.object(gkg, 'fetch_bytes', side_effect=error):
                    report = gkg.run_validation(url=url, integration=True, run_at=STAMP)
                    self.assertEqual(report['errors'][0]['code'], code)
                    self.assertEqual(report['errors'][0]['stage'], stage)

    def test_discovery_integrity_and_determinism(self):
        blob = fixture()
        metadata = f'{len(blob)} {hashlib.md5(blob).hexdigest()} {URL}'.encode()
        reports = []
        for _ in range(2):
            with patch.object(gkg, 'fetch_bytes', side_effect=[metadata, blob]):
                reports.append(gkg.run_validation(integration=True, run_at=STAMP))
        self.assertEqual(reports[0]['status'], 'passed')
        self.assertEqual(gkg.encode_report(reports[0]), gkg.encode_report(reports[1]))
        with patch.object(gkg, 'fetch_bytes', side_effect=[metadata, blob + b'x']):
            self.assertEqual(gkg.run_validation(integration=True)['errors'][0]['code'], 'metadata_mismatch')

    def test_ambiguous_metadata(self):
        line = f'1 {"0" * 32} {URL}\n'
        with patch.object(gkg, 'fetch_bytes', return_value=(line * 2).encode()):
            self.assertEqual(gkg.run_validation(integration=True)['errors'][0]['code'], 'metadata_invalid')

    def test_local_cli_report_success_failure_and_replace(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            source = Path(directory) / 'batch.zip'
            output = Path(directory) / 'report.json'
            source.write_bytes(fixture())
            with patch.object(gkg, 'fetch_bytes') as fetch:
                self.assertEqual(gkg.main(['--input', str(source), '--output', str(output)]), 0)
                self.assertEqual(json.loads(output.read_text())['status'], 'passed')
                source.write_bytes(b'bad')
                self.assertEqual(gkg.main(['--input', str(source), '--output', str(output)]), 3)
                self.assertEqual(json.loads(output.read_text())['errors'][0]['code'], 'invalid_zip')
                fetch.assert_not_called()

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            report = gkg.run_validation(input_path=Path(directory) / 'missing', run_at=STAMP)
            self.assertEqual(report['errors'][0]['code'], 'io_error')

    def test_write_failure_is_json(self):
        with patch.object(gkg, 'write_report', side_effect=OSError('denied')), contextlib.redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(gkg.main([]), 4)
            self.assertEqual(json.loads(stderr.getvalue())['errors'][-1]['code'], 'report_write_error')

    def test_invalid_url(self):
        with patch.object(gkg, 'fetch_bytes') as fetch:
            report = gkg.run_validation(url='https://example.org/x.zip', integration=True)
            self.assertEqual(report['errors'][0]['code'], 'invalid_url')
            fetch.assert_not_called()


if __name__ == '__main__':
    unittest.main()
