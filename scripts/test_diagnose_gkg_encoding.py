import tempfile
from pathlib import Path
import unittest

import diagnose_gkg_encoding as diagnostics
import study_gkg as study
from test_validate_gkg import fixture, row


class EncodingDiagnosticTests(unittest.TestCase):
    def test_strict_counts_and_byte_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            payload = row().encode() + row(record='x\ufffd').encode().replace(b'\xef\xbf\xbd', b'\xff')
            path, checksum = study.persist_raw(Path(directory), fixture(payload))
            result = diagnostics.diagnose(path, checksum)
            self.assertEqual(result['lines'], 2)
            self.assertEqual(result['utf8_rejected_lines'], 1)
            self.assertEqual(result['raw_field_count_distribution'], {'27': 2})
            self.assertEqual(result['invalid_byte_samples'][0]['field_number'], 1)
            self.assertEqual(result['invalid_byte_samples'][0]['invalid_bytes_hex'], 'ff')
            self.assertEqual(result['invalid_byte_samples'][0]['line_number'], 2)

    def test_changed_raw_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            path, checksum = study.persist_raw(Path(directory), fixture())
            path.write_bytes(b'changed')
            with self.assertRaises(study.StudyError): diagnostics.diagnose(path, checksum)

    def test_valid_unicode_is_not_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path, checksum = study.persist_raw(Path(directory), fixture(row(themes='测试;').encode()))
            result = diagnostics.diagnose(path, checksum)
            self.assertEqual(result['utf8_rejected_lines'], 0)


if __name__ == '__main__':
    unittest.main()
