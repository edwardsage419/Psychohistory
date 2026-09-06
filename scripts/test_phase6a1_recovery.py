"""Only new Phase 6A.1 boundaries; existing protocol/manifest tests remain intact."""
import copy
import unittest
import gkg_semantics as s
import phase6a1_recovery as t
from test_gkg_recovery import evidence,annotation,registry,case,import_args

class TriageTests(unittest.TestCase):
    def test_levels_require_identity_and_context(self):
        e=evidence();e['retrieval_method']='original_publisher';self.assertEqual(t.level(e),'E3')
        e['retrieval_method']='dated_wayback_capture';self.assertEqual(t.level(e),'E2')
        e['excerpt']='';self.assertEqual(t.level(e),'E1')
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

if __name__=='__main__':unittest.main()
