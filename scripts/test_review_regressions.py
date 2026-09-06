"""Regressions found during post-Issue-2 self-review."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from contracts import ContractError, validate_contract
import validate_gkg as gkg
from test_validate_gkg import fixture, STAMP, URL
import test_contracts


class ReviewRegressions(unittest.TestCase):
    def test_report_path_cannot_overwrite_input(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            source = Path(directory) / 'batch.zip'
            original = fixture()
            source.write_bytes(original)
            code = gkg.main(['--input', str(source), '--output', str(source)])
            self.assertEqual(source.read_bytes(), original)
            self.assertNotEqual(code, 0)

    def test_oversized_metadata_number_returns_failure(self):
        metadata = f'{"9" * 5000} {"0" * 32} {URL}'.encode()
        with patch.object(gkg, 'fetch_bytes', return_value=metadata):
            report = gkg.run_validation(integration=True, run_at=STAMP)
        self.assertEqual(report['status'], 'failed')
        self.assertEqual(report['errors'][0]['code'], 'metadata_invalid')

    def test_invalid_offset_minutes_rejected(self):
        observation = test_contracts.FoundationContractTests().observation()
        observation['retrieved_at'] = '2026-09-06T00:00:00+00:99'
        with self.assertRaises(ContractError):
            validate_contract('observation', observation)

    def test_partial_local_read_not_labeled_as_archive_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'large.zip'
            source.write_bytes(fixture())
            with patch.object(gkg, 'MAX_ZIP_BYTES', 10):
                report = gkg.run_validation(input_path=source, run_at=STAMP)
        self.assertEqual(report['errors'][0]['code'], 'resource_limit')
        self.assertIsNone(report['sha256'])
        self.assertIsNone(report['zip_bytes'])


if __name__ == '__main__':
    unittest.main()
