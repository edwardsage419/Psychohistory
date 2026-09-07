"""Post-review Phase 6A integrity bindings; offline only."""
import json
from pathlib import Path
import subprocess
import unittest
import gkg_semantics as s

ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'studies/gkg-semantics-v2'

class Phase6ARepairIntegrity(unittest.TestCase):
    def git_blob(self,path):
        return subprocess.check_output(['git','hash-object',path],cwd=ROOT,text=True).strip()

    def test_historical_manifest_artifacts_remain_bound(self):
        manifest=json.loads((STUDY/'assessment-manifest.json').read_text(encoding='utf-8-sig'))
        self.assertTrue(manifest['implementation'])
        for name,expected in manifest['artifacts'].items():
            self.assertEqual(s.sha((STUDY/name).read_bytes()),expected,name)

    def test_current_context_correction_binds_corrected_implementation_and_semantics(self):
        manifest=json.loads((STUDY/'assessment-manifest.json').read_text(encoding='utf-8-sig'))
        correction=json.loads((STUDY/'context-sufficiency-correction.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(correction['version'],'1.0.1')
        self.assertEqual(correction['historical_assessment_manifest']['git_blob_sha'],'4ca5034e2080ba4b1430dc07787028fabd4ae5eb')
        self.assertEqual(correction['authenticated_inputs']['evidence_file_sha256'],manifest['artifacts']['evidence.json'])
        self.assertEqual(correction['authenticated_inputs']['phase6a1_triage_file_sha256'],manifest['artifacts']['phase6a1-triage.json'])
        self.assertEqual(correction['authenticated_inputs']['phase6a1_protocol_file_sha256'],manifest['artifacts']['phase6a1-protocol.json'])
        self.assertEqual(correction['evidence_sufficiency']['version'],'1.0.1')
        semantic_paths={
            'studies/gkg-semantics-v1/preregistration.json':correction['authenticated_inputs']['phase5_preregistration_git_blob_sha'],
            'studies/gkg-semantics-v2/phase6a-protocol.json':correction['authenticated_inputs']['phase6a_protocol_git_blob_sha'],
            'studies/gkg-semantics-v2/phase6a1-protocol.json':correction['authenticated_inputs']['phase6a1_protocol_git_blob_sha'],
        }
        for path,expected in semantic_paths.items():
            self.assertEqual(self.git_blob(path),expected,path)
        for path,expected in correction['corrected_implementation_git_blobs'].items():
            self.assertEqual(self.git_blob(path),expected,path)

    def test_review_import_contract_requires_protocol_binding(self):
        contract=json.loads((STUDY/'review-import-contract.json').read_text(encoding='utf-8-sig'))
        self.assertEqual(contract['version'],'1.0.1')
        required=set(contract['required'])
        self.assertIn('review_protocol_version',required)
        self.assertIn('review_protocol_sha256',required)

if __name__=='__main__':unittest.main()
