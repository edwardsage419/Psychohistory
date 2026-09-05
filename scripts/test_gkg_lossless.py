import base64
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import gkg_lossless as core
from gkg_lossless_contracts import validate_record
import replay_gkg_lossless as runner
import study_gkg as study
from test_validate_gkg import fixture, row
from test_study_gkg import manifest, fake_download


STAMP = '20260904000000'


def raw_row(record='a', date=STAMP):
    return row(record=record, date=date).encode()


class LosslessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def store(self, payload=None, blob=None):
        if blob is None:
            blob = fixture(payload if payload is not None else raw_row(), names=(STAMP + '.gkg.csv',))
        path = self.root / 'source.zip'
        path.write_bytes(blob)
        source = {'source_id': 'gdelt-gkg-2.1', 'batch_id': STAMP,
                  'source_url': core.legacy.BASE_URL + STAMP + '.gkg.csv.zip',
                  'archive_sha256': core.sha(blob), 'archive_bytes': len(blob), 'acquisition': 'passed'}
        return path, source

    def ingest(self, payload=None, blob=None):
        path, source = self.store(payload, blob)
        result = core.ingest(path, source)
        core.validate_batch(result)
        return result

    def test_clean_provenance_and_schema(self):
        result = self.ingest()
        self.assertEqual(result['state'], 'clean_parse')
        r = result['rows'][0]
        self.assertEqual(r['raw_sha256'], core.sha(raw_row()))
        self.assertEqual(r['start'], 0)
        self.assertEqual(r['end'], len(raw_row()))
        self.assertEqual(r['timestamp'], STAMP)
        validate_record('row', r)
        validate_record('batch', result)

    def test_invalid_encoding_in_different_fields(self):
        for field in (0, 1, 7, 26):
            fields = core.body(raw_row('bad')).split(b'\t')
            fields[field] = b'\xffx\xa0'
            raw = b'\t'.join(fields) + b'\n'
            result = self.ingest(raw_row('good') + raw)
            self.assertEqual(result['state'], 'parse_with_quarantine')
            q = result['rows'][1]
            self.assertEqual(q['disposition'], 'quarantined_encoding')
            self.assertEqual(len(q['invalid_sequences']), 2)
            self.assertEqual(q['invalid_sequences'][0]['field'], field + 1)
            self.assertEqual(base64.b64decode(q['raw_base64']), raw)
            validate_record('quarantine', q)

    def test_invalid_utf8_keeps_safe_prefix_timestamp(self):
        result = self.ingest(raw_row('good') + raw_row('bad').replace(b'TEST_A', b'\xff'))
        self.assertEqual(result['rows'][1]['timestamp'], STAMP)

    def test_no_replacement_or_codec_fallback(self):
        result = self.ingest(raw_row().replace(b'TEST_A', b'\xe9'))
        self.assertEqual(result['state'], 'rejected')
        self.assertEqual(result['rows'][0]['fields_sha256'], None)
        self.assertIn(b'\xe9', base64.b64decode(result['rows'][0]['raw_base64']))

    def test_field_counts(self):
        for data in (b'a\tb\n', raw_row()[:-1] + b'\textra\n'):
            result = self.ingest(data)
            self.assertEqual(result['rows'][0]['disposition'], 'quarantined_schema')
            self.assertIn('field_count', [e['code'] for e in result['rows'][0]['reasons']])

    def test_unterminated_final_row(self):
        result = self.ingest(raw_row('first') + raw_row('last').rstrip(b'\n'))
        self.assertEqual(result['accepted_rows'], 1)
        self.assertEqual(result['rows'][1]['reasons'][0]['code'], 'unterminated_row')

    def test_invalid_unknown_and_off_batch_timestamps(self):
        for stamp in ('0', '20260230000000', '20260904001500'):
            result = self.ingest(raw_row(date=stamp))
            self.assertEqual(result['rows'][0]['disposition'], 'quarantined_timestamp')

    def test_duplicate_rows_all_occurrences_quarantined(self):
        result = self.ingest(raw_row('dupe') + raw_row('good') + raw_row('dupe'))
        self.assertEqual(result['accepted_rows'], 1)
        self.assertEqual([r['disposition'] for r in result['rows']], ['quarantined_other', 'accepted', 'quarantined_other'])

    def test_duplicate_id_with_different_bytes(self):
        result = self.ingest(raw_row('dupe') + raw_row('dupe').replace(b'TEST_A', b'OTHER'))
        self.assertEqual(result['accepted_rows'], 0)
        self.assertEqual(result['errors'][0]['code'], 'no_accepted_rows')

    def test_deterministic_ids_and_replay(self):
        path, source = self.store(raw_row() + raw_row('bad').replace(b'TEST_A', b'\xff'))
        first, second = core.ingest(path, source), core.ingest(path, source)
        self.assertEqual(first, second)
        self.assertNotEqual(first['rows'][0]['row_id'], first['rows'][1]['row_id'])

    def test_crlf_preserved(self):
        data = raw_row().replace(b'\n', b'\r\n')
        result = self.ingest(data)
        self.assertEqual(result['state'], 'clean_parse')
        self.assertEqual(result['rows'][0]['raw_sha256'], core.sha(data))

    def test_source_replacement_after_snapshot(self):
        path, source = self.store()
        original = core.read_snapshot
        def swap(p):
            blob = original(p)
            path.write_bytes(b'replaced')
            return blob
        with patch.object(core, 'read_snapshot', side_effect=swap):
            result = core.ingest(path, source)
        self.assertEqual(result['state'], 'clean_parse')
        self.assertEqual(result['observed_archive_sha256'], source['archive_sha256'])
        self.assertEqual(core.ingest(path, source)['errors'][0]['code'], 'source_revision_mismatch')

    def test_truncation_and_content_mutation_fail_closed(self):
        path, source = self.store()
        original = path.read_bytes()
        for blob in (original[:-5], original[:20] + b'changed' + original[27:]):
            path.write_bytes(blob)
            result = core.ingest(path, source)
            self.assertEqual(result['accepted_rows'], 0)
            self.assertEqual(result['errors'][0]['code'], 'source_revision_mismatch')

    def test_replay_different_archive_revision(self):
        path, source = self.store()
        old = core.ingest(path, source)
        path.write_bytes(fixture(raw_row('different'), names=(STAMP + '.gkg.csv',)))
        changed = core.ingest(path, source)
        self.assertNotEqual(old['semantic_sha256'], changed['semantic_sha256'])
        self.assertEqual(changed['state'], 'rejected')

    def test_hard_link_mutation(self):
        path, source = self.store()
        alias = self.root / 'hard.zip'
        os.link(path, alias)
        alias.write_bytes(b'mutated')
        result = core.ingest(path, source)
        self.assertEqual(result['errors'][0]['code'], 'source_revision_mismatch')

    def test_symlink_switch_after_snapshot(self):
        path, source = self.store()
        alternate = self.root / 'other.zip'
        alternate.write_bytes(b'changed')
        alias = self.root / 'link.zip'
        try:
            alias.symlink_to(path)
        except OSError as exc:
            self.skipTest('OS does not permit symlink creation: ' + type(exc).__name__)
        original = core.read_snapshot
        def switch(p):
            blob = original(p)
            alias.unlink()
            alias.symlink_to(alternate)
            return blob
        with patch.object(core, 'read_snapshot', side_effect=switch):
            result = core.ingest(alias, source)
        self.assertEqual(result['state'], 'clean_parse')
        self.assertEqual(core.ingest(alias, source)['state'], 'rejected')

    def test_missing_archive_is_recorded(self):
        path, source = self.store()
        path.unlink()
        result = core.ingest(path, source)
        self.assertEqual(result['errors'][0]['code'], 'source_io')

    def test_bad_zip_and_crc(self):
        self.assertEqual(self.ingest(blob=b'bad')['errors'][0]['code'], 'invalid_archive')
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_STORED) as archive:
            archive.writestr(STAMP + '.gkg.csv', raw_row())
        blob = buf.getvalue().replace(b'TEST_A', b'TEST_Z', 1)
        result = self.ingest(blob=blob)
        self.assertEqual(result['errors'][0]['code'], 'invalid_archive')
        self.assertEqual(result['rows'], [])

    def test_member_count_name_and_empty(self):
        for blob, code in [(fixture(names=('wrong.gkg.csv',)), 'archive_member_name'),
                           (fixture(names=('a', 'b')), 'archive_member_count'),
                           (fixture(b'', names=(STAMP + '.gkg.csv',)), 'empty_member')]:
            self.assertEqual(self.ingest(blob=blob)['errors'][0]['code'], code)

    def test_whole_archive_resource_limits(self):
        for name, value in [('MAX_ZIP_BYTES', 1), ('MAX_MEMBER_BYTES', 1), ('MAX_ROWS', 0)]:
            with patch.object(core, name, value):
                result = self.ingest()
            self.assertEqual(result['state'], 'rejected')
            self.assertEqual(result['accepted_rows'], 0)
            self.assertIn('resource', result['errors'][0]['code'])

    def test_row_resource_has_full_byte_identity(self):
        with patch.object(core, 'MAX_ROW_BYTES', 1):
            result = self.ingest()
        q = result['rows'][0]
        self.assertEqual(q['disposition'], 'quarantined_resource')
        self.assertEqual(base64.b64decode(q['raw_base64']), raw_row())

    def test_oversize_row_is_not_split_into_fields(self):
        _, source = self.store()
        raw = b'a\t' + STAMP.encode() + b'\t' * 100
        with patch.object(core, 'MAX_ROW_BYTES', 20), patch.object(core, 'body', side_effect=AssertionError('oversize field split')):
            result = core.classify(raw, source, STAMP + '.gkg.csv', 1, 0, set())
        self.assertEqual(result['disposition'], 'quarantined_resource')
        self.assertEqual(result['timestamp'], STAMP)
        self.assertEqual(base64.b64decode(result['raw_base64']), raw)

    def test_diagnostic_resource_bound_preserves_row(self):
        raw = raw_row().replace(b'TEST_A', b'\xff' * 10)
        with patch.object(core, 'MAX_INVALID_SEQUENCES', 2):
            result = self.ingest(raw)
        self.assertEqual(result['rows'][0]['disposition'], 'quarantined_resource')
        self.assertEqual(base64.b64decode(result['rows'][0]['raw_base64']), raw)

    def test_unexpected_exception_does_not_release_rows(self):
        with patch.object(core, 'classify', side_effect=RuntimeError('injected')):
            result = self.ingest()
        self.assertEqual(result['accepted_rows'], 0)
        self.assertEqual(result['rows'], [])
        self.assertEqual(result['errors'][0]['code'], 'unexpected_exception')

    def test_semantic_hash_mismatch(self):
        result = self.ingest()
        result['semantic_sha256'] = '0' * 64
        with self.assertRaises(core.Rejection): core.validate_batch(result)

    def test_false_clean_state_and_missing_reason(self):
        result = self.ingest(raw_row() + b'bad\n')
        result['state'] = 'clean_parse'
        core.seal(result)
        with self.assertRaises(core.Rejection): core.validate_batch(result)
        result['state'] = 'parse_with_quarantine'
        result['rows'][1]['reasons'] = []
        core.seal(result)
        with self.assertRaises(core.Rejection): core.validate_batch(result)

    def test_quarantine_bytes_tampering(self):
        result = self.ingest(b'bad\n')
        result['rows'][0]['raw_base64'] = base64.b64encode(b'fake').decode()
        core.seal(result)
        with self.assertRaises(core.Rejection): core.validate_batch(result)

    def test_supplied_member_payload_hash_is_verified(self):
        result = self.ingest()
        result['member_sha256'] = '0' * 64
        core.seal(result)
        with self.assertRaises(core.Rejection):
            core.validate_batch(result, raw_row())

    def test_quarantine_diagnostics_cannot_contradict_embedded_bytes(self):
        original = self.ingest(raw_row().replace(b'TEST_A', b'\xff'))
        for change in ('span', 'reason', 'category'):
            result = copy.deepcopy(original)
            q = result['rows'][0]
            if change == 'span': q['invalid_sequences'][0]['bytes_hex'] = '00'
            if change == 'reason': q['reasons'][0]['code'] = 'unrelated_failure'
            if change == 'category':
                q['disposition'] = 'quarantined_timestamp'
                result['disposition_counts'] = {'quarantined_timestamp': 1}
            core.seal(result)
            with self.subTest(change=change), self.assertRaises(core.Rejection):
                core.validate_batch(result)

    def test_output_collision_and_exclusive_write(self):
        path, _ = self.store()
        for output in (path, self.root, self.root / 'nested'):
            with self.assertRaises((core.Rejection, OSError)):
                runner.create_output(output, [self.root])
        alias = self.root / 'hard.json'
        os.link(path, alias)
        with self.assertRaises(FileExistsError): runner.write_new(alias, {})
        self.assertNotEqual(path.read_bytes(), b'{}')


class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.corpus = self.root / 'corpus'
        self.manifest = self.root / 'manifest.json'
        self.manifest.write_text(json.dumps(manifest()))
        self.patch = patch.object(study, 'SAMPLE_SIZE', 2)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        with contextlib.redirect_stdout(io.StringIO()):
            study.run_study(manifest(), self.corpus, True, fake_download)
            for name in ('one', 'two'):
                runner.run(self.manifest, self.corpus / 'study.json', self.corpus, self.root / name)

    def test_two_independent_replays_and_assessment(self):
        replay = runner.compare(manifest(), self.root / 'one', self.root / 'two')
        self.assertEqual(replay['passed'], 2)
        _, batches = runner.read_run(self.root / 'one', manifest())
        assessment = runner.assess(manifest(), batches, replay, regression_passed=True)
        self.assertEqual(assessment['recommendation'], 'promote_to_ingestion_candidate')
        self.assertEqual(runner.assess(manifest(), batches, replay)['recommendation'], 'continue_validation')

    def test_contradictory_success_cannot_promote(self):
        replay = runner.compare(manifest(), self.root / 'one', self.root / 'two')
        _, batches = runner.read_run(self.root / 'one', manifest())
        replay['batches'][0]['second_semantic_sha256'] = '0' * 64
        replay['semantic_sha256'] = core.digest({k: v for k, v in replay.items() if k not in ('created_at', 'semantic_sha256')})
        result = runner.assess(manifest(), batches, replay, True)
        self.assertEqual(result['recommendation'], 'continue_validation')
        self.assertFalse(result['gates']['independent_replay'])

    def test_missing_failure_code(self):
        replay = runner.compare(manifest(), self.root / 'one', self.root / 'two')
        replay['batches'][0]['status'] = 'failed'
        replay['passed'], replay['failed'] = 1, 1
        replay['semantic_sha256'] = core.digest({k: v for k, v in replay.items() if k not in ('created_at', 'semantic_sha256')})
        with self.assertRaises(core.Rejection): runner.validate_replay(replay)

    def test_changed_stored_semantics_fail_comparison(self):
        path = self.root / 'two' / (STAMP + '.json')
        result = study.read_json(path)
        result['accepted_rows'] += 1
        path.write_text(json.dumps(result))
        replay = runner.compare(manifest(), self.root / 'one', self.root / 'two')
        self.assertEqual(replay['failed'], 1)
        self.assertTrue(replay['batches'][0]['errors'])

    def test_duplicate_batches_block_admission(self):
        replay = runner.compare(manifest(), self.root / 'one', self.root / 'two')
        _, batches = runner.read_run(self.root / 'one', manifest())
        batches[1]['source']['archive_sha256'] = batches[0]['source']['archive_sha256']
        result = runner.assess(manifest(), batches, replay, True)
        self.assertFalse(result['gates']['no_duplicate_batches'])
        self.assertEqual(result['recommendation'], 'continue_validation')

    def test_runtime_metadata_excluded_only(self):
        replay = runner.compare(manifest(), self.root / 'one', self.root / 'two')
        replay['created_at'] = 'different runtime'
        runner.validate_replay(replay)
        replay['code_hashes']['fake'] = '0' * 64
        with self.assertRaises(core.Rejection): runner.validate_replay(replay)

    def test_storage_measurements_and_receipt_provenance(self):
        _, batches = runner.read_run(self.root / 'one', manifest())
        raw = (self.corpus / 'study.json').read_bytes()
        receipts = runner.provenance_receipts(json.loads(raw), core.sha(raw))
        self.assertEqual(receipts['phase2_report_sha256'], core.sha(raw))
        self.assertEqual(receipts['batches'][0]['transport']['status'], 200)
        profile = runner.storage_profile(manifest(), batches, receipts)
        self.assertEqual(profile['measured_totals_bytes']['raw_archives'], sum(b['source']['archive_bytes'] for b in batches))
        self.assertEqual(profile['measured_totals_bytes']['quarantine_evidence'], 0)
        self.assertFalse(profile['normalized_field_records']['created'])
        self.assertEqual(profile['recent_extrapolations']['raw_archives']['extrapolated_bytes_per_365_days'], batches[0]['source']['archive_bytes'] * 35040)

    def test_same_run_cannot_count_as_independent_replay(self):
        with self.assertRaises(core.Rejection) as caught:
            runner.compare(manifest(), self.root / 'one', self.root / 'one' / '.')
        self.assertEqual(caught.exception.code, 'replay_not_independent')

    def test_hard_linked_ledgers_cannot_count_as_independent(self):
        right = self.root / 'two' / (STAMP + '.json')
        right.unlink()
        os.link(self.root / 'one' / (STAMP + '.json'), right)
        with self.assertRaises(core.Rejection) as caught:
            runner.compare(manifest(), self.root / 'one', self.root / 'two')
        self.assertEqual(caught.exception.code, 'replay_not_independent')

    def test_malformed_assessment_evidence_fails_without_crashing(self):
        replay = runner.compare(manifest(), self.root / 'one', self.root / 'two')
        _, batches = runner.read_run(self.root / 'one', manifest())
        for supplied_batches, supplied_replay in [(batches, {}), ([{}], replay)]:
            result = runner.assess(manifest(), supplied_batches, supplied_replay, True)
            self.assertEqual(result['recommendation'], 'continue_validation')
            self.assertTrue(result['errors'])
            validate_record('assessment', result)

    def test_existing_output_cannot_overwrite_evidence(self):
        with self.assertRaises(FileExistsError):
            runner.run(self.manifest, self.corpus / 'study.json', self.corpus, self.root / 'one')


if __name__ == '__main__':
    unittest.main()
