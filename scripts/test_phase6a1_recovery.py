"""Only new Phase 6A.1 boundaries; existing protocol/manifest tests remain intact."""
from collections import Counter
import copy
import json
import unittest
import gkg_semantics as s
import phase6a1_recovery as t
from test_gkg_recovery import ROOT,evidence,annotation,registry,case,import_args

E1_IDS={
    '61c7c1dd513d1d62021d93228f909aef8a2d961f3e850dca97c21ac2b45a3642',
    '9443d204438f5a3213b4c7b39aec856ba8ae66e5a2d383b5e89817bb4a6b1cc5',
    'a6140896cd33c01e2e14e4fd8f9a44331ddc16f739648a5ffc945d5daa4fb1dc',
}
E3_IDS={
    '374a5d91e1d48f34c1c096ce025537660995161964315da7473ebfd68cf8d2ca',
    '544d11e2fe2d02e978eb4f6c4e4910a4ca5acd309033e115b587195de2e5b7a1',
    '3971850d00836d8a487c96f2128ac0ebd040bd5cee818d70c42939f90c377d57',
}

class TriageTests(unittest.TestCase):
    def test_levels_require_identity_and_reviewable_context(self):
        e=evidence();e['retrieval_method']='original_publisher';self.assertEqual(t.level(e),'E3')
        e['retrieval_method']='dated_wayback_capture';self.assertEqual(t.level(e),'E2')
        e['excerpt']='';self.assertEqual(t.level(e),'E1')
        e=evidence();e.update(excerpt='Generic four word fallback.',evidence_locator={'kind':'normalized_html_paragraph'},retrieval_method='original_publisher');self.assertEqual(t.level(e),'E1')
        e['identity_status']='identity_probable_manual_review_required';self.assertEqual(t.level(e),'E0')
    def test_e0_e1_cannot_be_semantic_positive(self):
        for state in ('identity_confirmed','identity_unresolved'):
            e=evidence();e.update(identity_status=state,excerpt='',retrieval_method='original_publisher');e['evidence_sufficiency']=t.level(e)
            with self.assertRaises(s.Invalid):t.import_reviews([annotation(e)],registry(),[case()],[e],**import_args(e))
    def test_similar_syndicated_copy_not_equivalence(self):
        e=evidence();e.update(retrieval_method='syndicated_similar',evidence_sufficiency='E2')
        self.assertEqual(t.level(e),'E0')
        with self.assertRaises(s.Invalid):t.import_reviews([annotation(e)],registry(),[case()],[e],**import_args(e))
    def test_stale_evidence_and_review_protocol_roots(self):
        e=evidence();e.update(retrieval_method='original_publisher',evidence_sufficiency='E3');a=annotation(e)
        for k in ('evidence_sha256','review_protocol_sha256'):
            bad=copy.deepcopy(a);bad[k]='0'*64
            with self.subTest(k=k),self.assertRaises(s.Invalid):t.import_reviews([bad],registry(),[case()],[e],**import_args(e))
    def test_failed_wayback_budget_terminates(self):
        calls=[]
        def fail(url,cfg):calls.append(url);return {'failure':'TimeoutError'},None
        circuit=t.ProviderCircuit(1)
        for _ in range(26):circuit.request('https://archive.org/probe',{},fail)
        self.assertEqual(len(calls),1)
    def test_overlay_no_replacement_or_metadata_change(self):
        e=evidence();e['identity_status']='identity_probable_manual_review_required';e['retrieval_method']='original_publisher';base=[e]
        for key,value in [('case_id','fake'),('year',2015),('token','FOOD_SECURITY')]:
            delta=[copy.deepcopy(e)];delta[0][key]=value
            with self.subTest(key=key),self.assertRaises(s.Invalid):t.resolve(base,delta,base_root=s.digest(base),delta_root=s.digest(delta))
    def test_coherent_reseal_rejected_against_external_root(self):
        e=evidence();e['identity_status']='identity_probable_manual_review_required';e['retrieval_method']='original_publisher';base=[e];delta=copy.deepcopy(base);root=s.digest(delta)
        delta[0]['excerpt']='forged'
        with self.assertRaises(s.Invalid):t.resolve(base,delta,base_root=s.digest(base),delta_root=root)
    def test_current_frozen_view_recomputes_corrected_sufficiency(self):
        directory=ROOT/'studies/gkg-semantics-v2'
        manifest=json.loads((directory/'assessment-manifest.json').read_text(encoding='utf-8-sig'))
        base_bytes=(directory/'evidence.json').read_bytes();delta_bytes=(directory/'phase6a1-triage.json').read_bytes()
        self.assertEqual(s.sha(base_bytes),manifest['artifacts']['evidence.json'])
        self.assertEqual(s.sha(delta_bytes),manifest['artifacts']['phase6a1-triage.json'])
        base=json.loads(base_bytes);delta=json.loads(delta_bytes)
        current=t.resolve(base,delta,base_root=s.digest(base),delta_root=s.digest(delta))
        self.assertEqual(len(current),120)
        self.assertEqual(Counter(e['identity_status'] for e in current),Counter({'identity_unresolved':92,'identity_probable_manual_review_required':15,'identity_mismatch':7,'identity_confirmed':6}))
        self.assertEqual(Counter(e['evidence_sufficiency'] for e in current),Counter({'E0':114,'E1':3,'E3':3}))
        self.assertEqual({e['case_id'] for e in current if e['evidence_sufficiency']=='E1'},E1_IDS)
        self.assertEqual({e['case_id'] for e in current if e['evidence_sufficiency']=='E3'},E3_IDS)
        self.assertTrue(all(e['evidence_sufficiency_version']==t.EVIDENCE_SUFFICIENCY_VERSION for e in current))

if __name__=='__main__':unittest.main()
