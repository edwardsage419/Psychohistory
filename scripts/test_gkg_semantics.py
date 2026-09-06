"""Fully synthetic/offline semantic-audit regressions; no retained corpus needed."""
import copy
import io
import json
from pathlib import Path
import unittest
from email.message import Message
import urllib.error
from unittest.mock import patch

import gkg_semantics as s
import retrieve_gkg_semantics as net

ROOT=Path(__file__).resolve().parents[1]

def protocol():return json.loads((ROOT/'studies/gkg-semantics-v1/preregistration.json').read_text(encoding='utf-8-sig'))

def candidates():
    rows=[]
    for token in s.TOKENS:
        for cohort in protocol()['sampling']['allocations'][token]:
            year=2026 if cohort=='recent' else int(cohort[-4:])
            if token.startswith('WB') and year==2015:continue
            for i in range(12):
                rows.append({'row_id':s.digest([token,cohort,i]),'batch_id':str(year)+'0904000000','year':year,'cohort':cohort,'line':i+1,
                    'DocumentIdentifier':f'https://example.org/{token}/{cohort}/{i}', 'tokens':[token],
                    'theme_count':i+1,'source_reference':'https://data.gdeltproject.org/example.zip','source_name':'example.org'})
    return rows

def fixture():
    p=protocol();sample=s.select_sample(candidates(),p,protocol_hash=s.digest(p));es=[]
    for c in sample['cases']:
        e={'case_id':c['case_id'],'original_url':c['DocumentIdentifier'],'final_url':c['DocumentIdentifier'],
            'protocol_sha256':s.digest(p),'title':'Example','excerpt':'People discussed unemployment today.',
            'locator':{'paragraph_index':0,'start':0,'end':35},'extractor_version':'1.0.0','context_level':'complete_sentence_context',
            'manual_context_required':False,'identity_review_required':False,'content_sha256':s.digest(c),
            'source_hash_scope':'complete_response_body','download_bytes':100,'http_status':200,'availability':'retrieved_context','attempts':1,'retrieved_at':'2026-09-06T00:00:00Z'}
        e['context_sha256']=s.context_hash(e);es.append(e)
    return p,sample,es

def reviewers():return [{'reviewer_id':r,'reviewer_type':'human','human_attestation_reference':'test-only fictional human fixture','independence_group':r} for r in ('a','b')]

def annotation(c,e,r='a',label='direct_topic_match'):
    a={k:c[k] for k in ('case_id','token','batch_id','year','cohort','source_reference','DocumentIdentifier')}
    a.update(title=e['title'],evidence_locator=e['locator'],content_sha256=e['content_sha256'],evidence_sha256=s.digest(e),label=label,
        reviewer_type='human',reviewer_id=r,reviewed_at='2026-09-06T01:00:00Z',protocol_version='1.0.0',confidence='high',reason_code=sorted(s.REASONS[label])[0])
    return a

class SamplingTests(unittest.TestCase):
    def setUp(self):self.p=protocol();self.c=candidates();self.h=s.digest(self.p);self.sample=s.select_sample(self.c,self.p,protocol_hash=self.h)
    def test_deterministic_reversed_population(self):self.assertEqual(self.sample,s.select_sample(self.c[::-1],self.p,protocol_hash=self.h))
    def test_seed_stable_and_changed_seed_changes_selection(self):
        p=copy.deepcopy(self.p);p['sampling']['seed']='different'
        self.assertNotEqual(self.sample['cases'],s.select_sample(self.c,p,protocol_hash=s.digest(p))['cases'])
    def test_exact_allocations_and_cap(self):
        self.assertEqual(len(self.sample['cases']),120)
        self.assertTrue(all(x['selected']==x['allocated'] for x in self.sample['populations']))
    def test_edge_metadata_coverage(self):
        edges=[c for c in self.sample['cases'] if c['selection_role'].endswith('edge')]
        self.assertTrue(all(c['theme_count'] in (1,12) for c in edges))
    def test_duplicate_reference_prevention(self):
        self.c[1]['DocumentIdentifier']=self.c[0]['DocumentIdentifier']
        sample=s.select_sample(self.c,self.p,protocol_hash=self.h)
        self.assertEqual(len(sample['cases']),len({c['DocumentIdentifier'] for c in sample['cases']}))
    def test_duplicate_row_rejected(self):
        with self.assertRaises(s.Invalid):s.select_sample(self.c+[self.c[0]],self.p,protocol_hash=self.h)
    def test_missing_year_not_negative(self):
        cell=next(x for x in self.sample['populations'] if x['token'].startswith('WB') and x['year']==2015)
        self.assertEqual(cell['selected'],0);self.assertTrue(cell['absent_token_not_negative'])
    def test_shortfalls_not_reallocated(self):
        sample=s.select_sample(self.c[:1],self.p,protocol_hash=self.h)
        self.assertEqual(len(sample['cases']),1);self.assertTrue(any(x['unfilled'] for x in sample['populations']))
    def test_replacement_rejected(self):
        self.sample['replacements']=[{'reason':'unavailable'}]
        with self.assertRaises(s.Invalid):s.validate_sample(self.sample,self.p,protocol_hash=self.h,sample_hash=s.digest(self.sample))
    def test_posthoc_protocol_rejected(self):
        self.p['gates']['positive_consistency']['direct_plus_contextual_min']=0.1
        with self.assertRaises(s.Invalid):s.validate_protocol(self.p,trusted_hash=self.h)
    def test_coherently_rehashed_sample_replacement_rejected(self):
        h=s.digest(self.sample);self.sample['cases'][0]['DocumentIdentifier']='https://example.org/replaced'
        with self.assertRaises(s.Invalid):s.validate_sample(self.sample,self.p,protocol_hash=self.h,sample_hash=h)
    def test_year_cherry_picking_rejected(self):
        self.sample['cases'].pop()
        with self.assertRaises(s.Invalid):s.validate_sample(self.sample,self.p,protocol_hash=self.h,sample_hash=s.digest(self.sample))
    def test_recall_positive_only_rejected(self):
        self.sample['recall']='estimated'
        with self.assertRaises(s.Invalid):s.validate_sample(self.sample,self.p,protocol_hash=self.h,sample_hash=s.digest(self.sample))

class EvidenceTests(unittest.TestCase):
    def setUp(self):self.p,self.sample,self.es=fixture();self.roots={e['case_id']:s.digest(e) for e in self.es}
    def check(self):return s.validate_evidence(self.es,self.sample,trusted_hashes=self.roots,protocol_hash=s.digest(self.p))
    def test_valid_evidence(self):self.check()
    def test_coherent_self_rehash_rejected(self):
        self.es[0]['excerpt']='Forged source sentence.';self.es[0]['context_sha256']=s.context_hash(self.es[0])
        with self.assertRaises(s.Invalid):self.check()
    def test_orphan_duplicate_evidence(self):
        self.es[-1]=self.es[0]
        with self.assertRaises(s.Invalid):self.check()
    def test_missing_unavailable_not_skipped(self):
        self.es.pop()
        with self.assertRaises(s.Invalid):self.check()
    def test_context_hash_mismatch(self):
        self.es[0]['context_sha256']='0'*64;self.roots[self.es[0]['case_id']]=s.digest(self.es[0])
        with self.assertRaises(s.Invalid):self.check()
    def test_receipt_source_mismatch(self):
        self.es[0]['original_url']='https://example.org/wrong';self.roots[self.es[0]['case_id']]=s.digest(self.es[0])
        with self.assertRaises(s.Invalid):self.check()
    def test_replacement_page_not_reviewable(self):
        self.es[0]['identity_review_required']=True;self.roots[self.es[0]['case_id']]=s.digest(self.es[0])
        with self.assertRaises(s.Invalid):self.check()
    def test_extraction_source_binding(self):
        blob=b'<html><title>Test</title><p>People discussed unemployment today. Its effects are serious.</p></html>'
        e=net.extract_context(blob,'WB_2747_UNEMPLOYMENT')
        net.validate_extraction(blob,'WB_2747_UNEMPLOYMENT',e,content_hash=s.sha(blob))
        e['excerpt']='Invented.'
        with self.assertRaises(s.Invalid):net.validate_extraction(blob,'WB_2747_UNEMPLOYMENT',e,content_hash=s.sha(blob))
    def test_source_content_hash_mismatch(self):
        with self.assertRaises(s.Invalid):net.validate_extraction(b'changed','PROTEST',{},content_hash='0'*64)
    def test_keyword_only_does_not_manufacture_context(self):
        e=net.extract_context(b'<p>protest</p>','PROTEST');self.assertTrue(e['manual_context_required'])
    def test_script_and_navigation_excluded(self):
        e=net.extract_context(b'<script>People protest in the city.</script><nav><p>People protest in the city.</p></nav>','PROTEST');self.assertEqual(e['excerpt'],'')
    def test_no_blinding_claim_or_leaked_analytics(self):
        packet=s.packet(self.sample,self.es,self.p)
        self.assertTrue(all(not row['blinded'] and 'prevalence' not in row and 'expected_conclusion' not in row for row in packet))
    def test_changed_redirect_identity(self):
        self.assertTrue(net.identity_requires_review('http://a.test/2015/article','https://a.test/'))
        self.assertFalse(net.identity_requires_review('http://a.test/story','https://www.a.test/story/'))

class AnnotationTests(unittest.TestCase):
    def setUp(self):self.p,self.sample,self.es=fixture();self.rs=reviewers();self.a=annotation(self.sample['cases'][0],self.es[0])
    def check(self,annotations=None):return s.validate_annotations([self.a] if annotations is None else annotations,self.sample,self.es,self.rs,self.p,reviewer_hash=s.digest(reviewers()))
    def test_valid_annotation(self):self.check()
    def test_invalid_label(self):
        self.a['label']='ground_truth'
        with self.assertRaises(s.Invalid):self.check()
    def test_missing_schema_field(self):
        del self.a['evidence_locator']
        with self.assertRaises(s.Invalid):self.check()
    def test_unknown_reviewer(self):
        self.a['reviewer_id']='unknown'
        with self.assertRaises(s.Invalid):self.check()
    def test_model_mislabeled_human(self):
        self.rs[0]['reviewer_type']='llm'
        with self.assertRaises(s.Invalid):self.check()
    def test_duplicate_annotation(self):
        with self.assertRaises(s.Invalid):self.check([self.a,self.a])
    def test_protocol_binding(self):
        self.a['protocol_version']='2.0.0'
        with self.assertRaises(s.Invalid):self.check()
    def test_excerpt_binding(self):
        self.a['evidence_sha256']='0'*64
        with self.assertRaises(s.Invalid):self.check()
    def test_wrong_token_plausible_label(self):
        self.a['token']='FOOD_SECURITY'
        with self.assertRaises(s.Invalid):self.check()
    def test_mismatch_hidden_as_ambiguous_reason(self):
        self.a['label']='ambiguous';self.a['reason_code']='lexical_collision'
        with self.assertRaises(s.Invalid):self.check()
    def test_unavailable_cannot_be_positive(self):
        self.es[0]['availability']='document_unavailable';self.a['evidence_sha256']=s.digest(self.es[0])
        with self.assertRaises(s.Invalid):self.check()

class StatsTests(unittest.TestCase):
    def setUp(self):self.p,self.sample,self.es=fixture()
    def test_no_human_null_semantic_rates(self):
        out=s.summary(self.sample['cases'],self.es,[])
        self.assertIsNone(out['sampled_positive_semantic_match_rates']['direct']['among_selected'])
    def test_denominators_and_unavailable(self):
        cs=self.sample['cases'][:3];es=self.es[:3];es[2]['availability']='document_unavailable'
        a=[annotation(cs[0],es[0])];out=s.summary(cs,es,a,'a')
        self.assertEqual((out['selected'],out['reviewable_unique'],out['semantic_reviewed']),(3,2,1))
        self.assertAlmostEqual(out['unavailable_rate_selected'],1/3)
        self.assertEqual(out['sampled_positive_semantic_match_rates']['direct']['among_unique_reviewable'],.5)
    def test_duplicate_content_not_reviewed_twice(self):
        cs=self.sample['cases'][:2];es=self.es[:2];es[1]['content_sha256']=es[0]['content_sha256']
        out=s.summary(cs,es,[annotation(c,e) for c,e in zip(cs,es)],'a');self.assertEqual(out['semantic_reviewed'],1)
    def test_agreement_confusion_and_exclusions(self):
        cs=self.sample['cases'][:3];es=self.es[:3];aa=[]
        for c,e in zip(cs,es):aa.extend([annotation(c,e,'a'),annotation(c,e,'b')])
        aa[1]=annotation(cs[0],es[0],'b','semantic_mismatch');aa[-1]=annotation(cs[-1],es[-1],'b','insufficient_context')
        ag=s.agreement(cs,es,aa,reviewers());self.assertEqual(ag['pairs'][0]['paired'],2);self.assertEqual(ag['pairs'][0]['raw_agreement'],.5)
        self.assertTrue(ag['pairs'][0]['by_token']);self.assertTrue(ag['pairs'][0]['by_year'])
    def test_no_independent_reviews(self):
        self.assertEqual(s.agreement(self.sample['cases'],self.es,[],reviewers())['status'],'not_estimated')
    def test_gate_pending_not_forced_promotion(self):
        t=[{'id':'unknown','category':'unresolved','claim':'extractor history unknown','limitations':'bounded search','tokens':list(s.TOKENS)}]
        trust={'protocol':s.digest(self.p),'sample':s.digest(self.sample),'receipts':{e['case_id']:s.digest(e) for e in self.es},'reviewers':s.digest([]),'annotations':s.digest([]),'taxonomy':s.digest(t)}
        a=s.assess(self.sample,self.p,self.es,[],[],t,trust=trust)
        self.assertEqual(a['recommendation'],'continue_semantic_validation');self.assertEqual(a['tokens'][2]['unobserved_years'],[2015])
    def test_taxonomy_invalid_category(self):
        t=[{'id':'a','category':'assumed','claim':'stable','limitations':'none'}]
        with self.assertRaises(s.Invalid):s.validate_taxonomy(t,trusted_hash=s.digest(t))
    def test_taxonomy_no_documentation_is_not_stability(self):
        t=[{'id':'a','category':'unresolved','claim':'no changelog','limitations':'unknown','proves_historical_stability':True}]
        with self.assertRaises(s.Invalid):s.validate_taxonomy(t,trusted_hash=s.digest(t))

class CacheTests(unittest.TestCase):
    def test_cache_stable_and_configuration_bound(self):
        args=dict(content_hash='a'*64,context_hash='b'*64,token='PROTEST',protocol_hash='c'*64,model='test-model-v1',prompt_hash='d'*64,settings={'temperature':0})
        key=s.cache_key(**args);self.assertEqual(key,s.cache_key(**args))
        record={'cache_key':key,'label':'ambiguous'}
        for field in ('content_hash','context_hash','token','protocol_hash','model','prompt_hash','settings'):
            altered=dict(args);altered[field]={'temperature':1} if field=='settings' else str(args[field])+'changed'
            with self.subTest(field=field),self.assertRaises(s.Invalid):s.validate_cache(record,trusted_hash=s.digest(record),expected_key=s.cache_key(**altered))

class RetrievalTests(unittest.TestCase):
    def test_http_failure_offline(self):
        class Opener:
            def open(self,*a,**kw):raise urllib.error.HTTPError('https://example.org/story',404,'missing',{},None)
        c={'case_id':'a','DocumentIdentifier':'https://example.org/story','token':'PROTEST'}
        e=net.retrieve(c,protocol(),opener_factory=lambda _:Opener())
        self.assertEqual(e['availability'],'document_unavailable');self.assertEqual(e['http_status'],404);self.assertEqual(e['attempts'],1)
    def test_public_url_guard(self):
        self.assertFalse(s.public_reference('file:///etc/passwd'));self.assertFalse(s.public_reference('https://user:pass@example.org/a'))
        with patch('socket.getaddrinfo',return_value=[(2,1,6,'',('127.0.0.1',80))]),self.assertRaises(s.Invalid):net.check_public('http://example.org/a')

if __name__=='__main__':unittest.main()

class AdversarialReviewTests(unittest.TestCase):
    def test_block_page_with_topic_text_not_reviewable(self):
        class Response(io.BytesIO):
            status=200
            headers=Message()
            headers['Content-Type']='text/html; charset=utf-8'
            def geturl(self):return 'https://example.org/story'
        class Opener:
            def open(self,*a,**kw):return Response(b'<title>Access Denied</title><p>People discussed unemployment today.</p>')
        e=net.retrieve({'case_id':'a','DocumentIdentifier':'https://example.org/story','token':'WB_2747_UNEMPLOYMENT'},protocol(),opener_factory=lambda _:Opener())
        self.assertNotEqual(e['availability'],'retrieved_context')
    def test_hash_scope_prefix_not_exact_article_duplicate(self):
        p,sample,es=fixture();cs=sample['cases'][:2];es=es[:2]
        for e in es:e.update(content_sha256='a'*64,source_hash_scope='bounded_prefix',availability='document_unavailable')
        self.assertEqual(len(s.unique_cases(cs,es)),2)
    def test_untrusted_blinded_flag_not_accepted(self):
        p,sample,es=fixture();packet=s.packet(sample,es,p)
        packet[0]['blinded']=True
        # Review packets are derived evidence too, and must compare with pinned inputs.
        with self.assertRaises(s.Invalid):s.validate_packet(packet,sample,es,p)
    def test_stale_model_registry_configuration_rejected(self):
        p,sample,es=fixture();r=[{'reviewer_id':'a','reviewer_type':'llm'}]
        a=annotation(sample['cases'][0],es[0]);a['reviewer_type']='llm'
        with self.assertRaises(s.Invalid):s.validate_annotations([a],sample,es,r,p,reviewer_hash=s.digest(r))
    def test_eligible_year_not_dropped_after_selection_shortfall(self):
        p=protocol();cs=candidates()
        # Shared references are allocated to earlier panel; food-year candidates exist but cannot be selected.
        for c in cs:
            if c['cohort']=='historical_2015':c['tokens']=list(s.TOKENS[:2])
        sample=s.select_sample(cs,p,protocol_hash=s.digest(p))
        # Force genuine exhausted global URL population in one positive stratum through allocation-sized population.
        cs=[c for c in cs if c['cohort']!='historical_2015']+cs[:6]
        sample=s.select_sample(cs,p,protocol_hash=s.digest(p))
        self.assertTrue(any(x['token']=='FOOD_SECURITY' and x['year']==2015 and x['unique_references']>0 and x['selected']==0 for x in sample['populations']))
        self.assertIn(2015,s.required_years(sample,p,'FOOD_SECURITY'))
