"""Post-review Phase 6A integrity bindings; offline only."""
import json
from pathlib import Path
import unittest
import gkg_semantics as s

ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'studies/gkg-semantics-v2'

class Phase6ARepairIntegrity(unittest.TestCase):
    def test_manifest_binds_current_implementation_and_artifacts(self):
        manifest=json.loads((STUDY/'assessment-manifest.json').read_text(encoding='utf-8-sig'))
        for name,expected in manifest['implementation'].items():
            payload=(ROOT/'scripts'/name).read_bytes().replace(b'\r\n',b'\n').removeprefix(b'\xef\xbb\xbf')
            self.assertEqual(s.sha(payload),expected,name)
        for name,expected in manifest['artifacts'].items():
            self.assertEqual(s.sha((STUDY/name).read_bytes()),expected,name)

    def test_review_import_contract_requires_protocol_binding(self):
        contract=json.loads((STUDY/'review-import-contract.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(contract['version'],'1.0.1')
        required=set(contract['required'])
        self.assertIn('review_protocol_version',required)
        self.assertIn('review_protocol_sha256',required)

if __name__=='__main__':unittest.main()
