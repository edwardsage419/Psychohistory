import copy
import unittest
from unittest.mock import patch

from contracts import ContractError, validate_contract
import validate_gkg as gkg
from test_validate_gkg import fixture, row, STAMP, URL


class ReportContractTests(unittest.TestCase):
    def report(self, blob=None):
        with patch.object(gkg, 'fetch_bytes', return_value=fixture() if blob is None else blob):
            return gkg.run_validation(url=URL, integration=True, run_at=STAMP)

    def test_success_and_all_fixture_failure_reports(self):
        for blob in (fixture(), b'bad', fixture(b''), fixture(row(date='bad').encode()), fixture(b'\xff')):
            with self.subTest(blob_size=len(blob)):
                validate_contract('validation-report', self.report(blob))
        validate_contract('validation-report', gkg.run_validation(run_at=STAMP))

    def test_invalid_reports(self):
        original = self.report()
        for key, value in [('schema_version', '2.0.0'), ('sha256', 'wrong'), ('validated_at', '2026-02-30T00:00:00Z'), ('status', 'failed')]:
            with self.subTest(key=key):
                report = copy.deepcopy(original)
                report[key] = value
                with self.assertRaises(ContractError):
                    validate_contract('validation-report', report)

    def test_count_and_boolean_invariants(self):
        for key, value in [('rows', 2), ('valid_rows', True), ('bad_rows', -1), ('empty_theme_rows', 3)]:
            report = self.report()
            report['statistics'][key] = value
            with self.assertRaises(ContractError):
                validate_contract('validation-report', report)

    def test_unknown_and_missing_fields(self):
        for operation in ('add', 'remove'):
            report = self.report()
            if operation == 'add':
                report['undocumented'] = 1
            else:
                del report['source_id']
            with self.assertRaises(ContractError):
                validate_contract('validation-report', report)


if __name__ == '__main__':
    unittest.main()
