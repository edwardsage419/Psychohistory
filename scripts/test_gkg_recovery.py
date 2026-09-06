"""High-value Phase 6A regressions; synthetic bodies, no network/corpus dependency."""
import copy
from datetime import datetime
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch,Mock
import gkg_semantics as s
import gkg_recovery as r
import recovery_transport as net
import study_gkg_recovery as study
from assess_gkg_semantics import verify_artifacts

ROOT=Path(__file__).resolve().parents[1]
def protocol():return json.loads((ROOT/'studies/gkg-semantics-v2/phase6a-protocol.json').read_text(encoding='utf-8-sig'))
def case():return {'case_id':'case1','token':'PROTEST','year':2020,'cohort':'historical_2020','batch_id':'20200905120000','source_name':'example.org','DocumentIdentifier':'https://example.org/article'}
def body():return b'<title>Example article</title><link rel="canonical" href="https://example.org/article"><meta property="og:type" content="article"><meta property="article:published_time" content="2020-09-05T10:00:00Z"><p>People protest against the policy.</p>'
def receipt(blob=None):
    blob=body() if blob is None else blob
    return {'status':200,'failure':None,'content_type':'text/html','charset':'utf-8','content_sha256':s.sha(blob),'final_url':'https://example.org/article','retrieved_at':'2026-09-06T00:00:00Z'}
def evidence():
    c=case();x=r.identify(c,receipt(),body(),{'source_hash_scope':'complete_response_body','content_sha256':s.sha(body())},method='original_publisher')
    return {**{k:c[k] for k in ('case_id','token','year','cohort')},'source':c['source_name'],'original_url':c['DocumentIdentifier'],'recovered_url':c['DocumentIdentifier'],**x}
def registry():return [{'reviewer_id':'human-a','reviewer_type':'human','person_id':'person-a','independence_group':'group-a','human_attestation_reference':'fictional offline fixture only'}]
def annotation(e):
    p=protocol();return {**{k:e[k] for k in ('case_id','token','year','cohort','original_url')},'evidence_sha256':s.digest(e),'human_label':'direct_topic_match','reviewer_id':'human-a','reviewer_type':'human','reviewed_at':'2026-09-06T01:00:00Z','review_protocol_version':p['version'],'review_protocol_sha256':s.digest(p)}
def import_args(e,reg=None):
    p=protocol();reg=registry() if reg is None else reg
    return dict(registry_root=s.digest(reg),evidence_hashes={'case1':s.digest(e)},review_protocol=p,review_protocol_root=s.digest(p))

class FrozenTests(unittest.TestCase):
    def test_frozen_120_case_ids_and_metadata_no_resampling(self):
        sample=json.loads((ROOT/'studies/gkg-semantics-v1/sample.json').read_text(encoding='utf-8'))
        root='3a8710caabb8d571edbbd5f80276e00f25cec26c9622655d3b3db8d7045b9a46'
        self.assertEqual(len(sample['cases']),120);s.authenticate(sample,root,'sample')
        for transform in ('remove','replace','retoken','reyear'):
            bad=copy.deepcopy(sample)
            if transform=='remove':bad['cases'].pop()
            elif transform=='replace':bad['cases'][0]['case_id']='new'
            elif transform=='retoken':bad['cases'][0]['token']='FOOD_SECURITY'
            else:bad['cases'][0]['year']=1999
            with self.subTest(transform=transform),self.assertRaises(s.Invalid):s.authenticate(bad,root,'sample')

class NetworkTests(unittest.TestCase):
    def test_private_dns_rejected_before_connect(self):
        with patch('socket.getaddrinfo',return_value=[(2,1,6,'',('127.0.0.1',443))]),patch('socket.create_connection') as connect:
            result,_=net.fetch('https://example.org/a',protocol()['network'])
        self.assertEqual(result['failure'],'nonpublic_address');connect.assert_not_called()
    def test_pinned_peer_mismatch_rejected_before_request(self):
        sock=Mock();sock.getpeername.return_value=('1.1.1.1',443)
        conn=net.PinnedConnection('example.org',443,{'93.184.216.34'},2,False)
        with patch('socket.create_connection',return_value=sock) as connect,self.assertRaises(s.Invalid):conn.connect()
        self.assertEqual(connect.call_args.args[0][0],'93.184.216.34');sock.close.assert_called()
    def test_redirect_private_is_revalidated(self):
        response=Mock();response.status=302;response.getheader.return_value='http://127.0.0.1/a';response.headers.get_content_type.return_value='text/html'
        conn=Mock();conn.peer='93.184.216.34';conn.getresponse.return_value=response
        with patch.object(net,'check_public',side_effect=[{'93.184.216.34'},s.Invalid('nonpublic_address')]),patch.object(net,'PinnedConnection',return_value=conn):
            result,_=net.fetch('https://example.org/a',protocol()['network'])
        self.assertEqual(result['failure'],'nonpublic_address');self.assertEqual(conn.request.call_count,1)
    def test_oversize_and_timeout_are_recorded(self):
        for failure in ('size','timeout'):
            conn=Mock();conn.peer='93.184.216.34';response=Mock();response.status=200;response.fp=None;response.headers.get_content_type.return_value='text/html';response.headers.get_content_charset.return_value='utf-8';response.read1.return_value=b'12345';conn.getresponse.return_value=response
            if failure=='timeout':conn.connect.side_effect=socket.timeout()
            cfg=dict(protocol()['network'],max_bytes=4)
            with patch.object(net,'check_public',return_value={'93.184.216.34'}),patch.object(net,'PinnedConnection',return_value=conn):result,blob=net.fetch('https://example.org/a',cfg)
            self.assertIsNone(blob);self.assertIn(result['failure'],('response_size_limit','TimeoutError'))

class IdentityTests(unittest.TestCase):
    def test_confirmed_requires_dates_canonical_and_independent_hash(self):self.assertEqual(evidence()['identity_status'],'identity_confirmed')
    def test_unrelated_article_and_same_title(self):
        for blob,expected in ((body().replace(b'/article',b'/unrelated'),'identity_mismatch'),(b'<title>Example article</title><p>People protest against the policy.</p>','identity_probable_manual_review_required')):
            result=r.identify(case(),receipt(blob),blob,{},method='original_publisher');self.assertEqual(result['identity_status'],expected);self.assertEqual(result['excerpt'],'')
    def test_changed_content_requires_manual_review(self):
        changed=body()+b'changed'
        result=r.identify(case(),receipt(changed),changed,{'source_hash_scope':'complete_response_body','content_sha256':s.sha(body())},method='original_publisher')
        self.assertTrue(result['content_changed_from_phase5']);self.assertNotEqual(result['identity_status'],'identity_confirmed')
    def test_archive_locator_mismatch(self):
        for url in ('https://web.archive.org/web/20200905120000/https://example.org/wrong','https://web.archive.org/web/20200906120000/https://example.org/article','https://evil.example/web/20200905120000/https://example.org/article'):
            with self.subTest(url=url),self.assertRaises(s.Invalid):r.archive_locator(url,case()['DocumentIdentifier'],'20200905120000')
    def test_discovery_alone_not_identity_evidence(self):
        def fake(url,cfg):return {**receipt(), 'status':404,'content_sha256':None,'failure':'http_404'},None
        attempts,e=study.recover(case(),{},protocol(),fetcher=fake)
        self.assertEqual(e['identity_status'],'identity_unresolved');self.assertEqual(len(attempts),2)

class ImportTests(unittest.TestCase):
    def test_altered_excerpt_and_stale_hash(self):
        e=evidence();root=s.digest(e);bad=copy.deepcopy(e);bad['excerpt']='Altered.'
        with self.assertRaises(s.Invalid):r.validate_evidence([bad],[case()],trusted_hashes={'case1':root})
        a=annotation(e);a['evidence_sha256']='0'*64
        with self.assertRaises(s.Invalid):r.import_humans([a],registry(),[case()],[e],**import_args(e))
    def test_human_identity_attestation_duplicate_and_case_guards(self):
        for mutation in ('machine','llm','attestation','duplicate_person','duplicate_annotation','fake_case','metadata','invalid_label','stale_protocol_version','stale_protocol_hash'):
            e=evidence();a=annotation(e);reg=registry();aa=[a]
            if mutation in ('machine','llm'):reg[0]['reviewer_type']=mutation
            elif mutation=='attestation':reg[0]['human_attestation_reference']=''
            elif mutation=='duplicate_person':reg.append({**reg[0],'reviewer_id':'alias','independence_group':'alias-group'})
            elif mutation=='duplicate_annotation':aa.append(a)
            elif mutation=='fake_case':a['case_id']='fake'
            elif mutation=='metadata':a['year']=2015
            elif mutation=='invalid_label':a['human_label']='made_up'
            elif mutation=='stale_protocol_version':a['review_protocol_version']='0.9.0'
            else:a['review_protocol_sha256']='0'*64
            with self.subTest(mutation=mutation),self.assertRaises(s.Invalid):r.import_humans(aa,reg,[case()],[e],**import_args(e,reg))
    def test_genuine_attested_fixture_and_blank_packet(self):
        e=evidence();self.assertEqual(len(r.import_humans([annotation(e)],registry(),[case()],[e],**import_args(e)),1)
        p=r.packet([e])[0];self.assertIsNone(p['human_label']);self.assertIsNone(p['reviewer_id']);self.assertNotIn('recommendation',p)

class TrustTests(unittest.TestCase):
    def test_external_root_mandatory_and_coherent_reseal_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp);(path/'evidence.json').write_bytes(b'[]');m={'artifacts':{'evidence.json':s.sha(b'[]')}};root=s.digest(m)
            with self.assertRaises(TypeError):verify_artifacts(path,m)
            verify_artifacts(path,m,trusted_manifest_hash=root)
            (path/'evidence.json').write_bytes(b'{}');m['artifacts']['evidence.json']=s.sha(b'{}')
            with self.assertRaises(s.Invalid):verify_artifacts(path,m,trusted_manifest_hash=root)

if __name__=='__main__':unittest.main()
