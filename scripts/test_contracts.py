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

class FoundationContractTests(unittest.TestCase):
    def observation(self):
        from contracts import observation_id
        value = {'schema_version': '1.0.0', 'source_id': 'fixture-provider',
                 'source_version': None, 'metric_id': 'fixture.count',
                 'observed_at': None, 'retrieved_at': STAMP, 'value': 0,
                 'unit': 'count', 'geography': None, 'entity': None,
                 'quality_status': 'valid', 'quality_note': 'Synthetic contract fixture; scope and time unknown',
                 'source_record_reference': 'fixture:record-1', 'source_snapshot_sha256': 'a' * 64,
                 'transformation_version': 'fixture/1'}
        value['observation_id'] = observation_id(value)
        return value

    def test_registry(self):
        import json
        from contracts import SCHEMAS
        registry = json.loads((SCHEMAS.parent / 'registry/sources.v1.json').read_text(encoding='utf-8'))
        validate_contract('source-registry', registry)
        registry['sources'].append(copy.deepcopy(registry['sources'][0]))
        with self.assertRaises(ContractError):
            validate_contract('source-registry', registry)

    def test_registry_required_metadata(self):
        import json
        from contracts import SCHEMAS
        original = json.loads((SCHEMAS.parent / 'registry/sources.v1.json').read_text(encoding='utf-8'))
        for key in original['sources'][0]:
            registry = copy.deepcopy(original)
            del registry['sources'][0][key]
            with self.subTest(key=key), self.assertRaises(ContractError):
                validate_contract('source-registry', registry)

    def test_zero_and_missing_observations(self):
        from contracts import observation_id
        value = self.observation()
        validate_contract('observation', value)
        value.update(value=None, quality_status='missing')
        value['observation_id'] = observation_id(value)
        validate_contract('observation', value)

    def test_identity_replay_and_revision(self):
        from contracts import observation_id
        value = self.observation()
        initial = value['observation_id']
        value['retrieved_at'] = '2026-09-07T00:00:00Z'
        self.assertEqual(observation_id(value), initial)
        validate_contract('observation', value)
        for field, replacement in [('value', 1), ('transformation_version', 'fixture/2'),
                                   ('source_snapshot_sha256', 'b' * 64)]:
            changed = {**value, field: replacement}
            self.assertNotEqual(observation_id(changed), initial)
            with self.assertRaises(ContractError):
                validate_contract('observation', changed)

    def test_invalid_observation_fields(self):
        for field, value in [('value', float('nan')), ('value', float('inf')), ('value', True),
                             ('value', None), ('quality_status', 'missing'),
                             ('retrieved_at', '2026-09-06T00:00:00'),
                             ('observed_at', '2026-02-30T00:00:00Z'),
                             ('geography', {'code': 'US'}), ('source_record_reference', ''),
                             ('source_snapshot_sha256', 'unverified'), ('schema_version', '2.0.0')]:
            with self.subTest(field=field, value=value), self.assertRaises(ContractError):
                validate_contract('observation', {**self.observation(), field: value})

    def test_observation_requires_all_fields(self):
        for field in self.observation():
            value = self.observation()
            del value[field]
            with self.subTest(field=field), self.assertRaises(ContractError):
                validate_contract('observation', value)

    def test_named_geography_and_timezone(self):
        from contracts import observation_id
        value = self.observation()
        value.update(geography={'scheme': 'ISO-3166-1-alpha2', 'code': 'US'},
                     observed_at='2026-09-06T08:00:00+08:00')
        value['observation_id'] = observation_id(value)
        validate_contract('observation', value)
