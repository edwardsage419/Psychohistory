"""Regression tests for the final Phase 5 integrity repair."""
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

import assess_gkg_semantics as audit
import gkg_semantics as s
import retrieve_gkg_semantics as net
from test_gkg_semantics import fixture, reviewers, annotation


class PeerBindingTests(unittest.TestCase):
    class Peer:
        def __init__(self,address):self.address=address
        def getpeername(self):return (self.address,443)

    class Wrapped:
        def __init__(self,address):self.fp=PeerBindingTests.Peer(address)

    def test_preapproved_public_peer_passes(self):
        self.assertEqual(net.verify_public_peer(self.Wrapped('93.184.216.34'),frozenset({'93.184.216.34'})),'93.184.216.34')

    def test_dns_rebinding_to_unapproved_public_peer_fails(self):
        with self.assertRaisesRegex(s.Invalid,'peer_address_not_preapproved'):
            net.verify_public_peer(self.Wrapped('1.1.1.1'),frozenset({'93.184.216.34'}))

    def test_rebinding_to_private_peer_fails(self):
        with self.assertRaisesRegex(s.Invalid,'nonpublic_peer_address'):
            net.verify_public_peer(self.Wrapped('127.0.0.1'),frozenset({'127.0.0.1'}))

    def test_missing_peer_fails_closed(self):
        with self.assertRaisesRegex(s.Invalid,'peer_address_unavailable'):
            net.verify_public_peer(object(),frozenset({'93.184.216.34'}))

    def test_redirect_source_must_have_been_preapproved(self):
        handler=net.Redirects(5)
        class Request:
            full_url='https://example.org/start'
        with self.assertRaisesRegex(s.Invalid,'redirect_source_not_preapproved'):
            handler.redirect_request(Request(),self.Wrapped('93.184.216.34'),302,'found',{},'https://example.org/next')


class ManifestTrustBoundaryTests(unittest.TestCase):
    def data(self):
        p,sample,es=fixture();rs=reviewers()
        aa=[annotation(c,e,r['reviewer_id']) for c,e in zip(sample['cases'],es) for r in rs]
        taxonomy=[{'id':'synthetic-only','category':'authoritative_provider_statement','claim':'Synthetic regression evidence only',
            'limitations':'test fixture','url':'https://blog.gdeltproject.org/synthetic-test-only/','source_sha256':'a'*64,
            'supports_topic':list(s.TOKENS),'tokens':list(s.TOKENS),'proves_historical_stability':True,
            'version_interval_evidence':'synthetic fixture covering test cohorts'}]
        trust={'protocol_sha256':s.digest(p),'sample_sha256':s.digest(sample)}
        receipts={e['case_id']:s.digest(e) for e in es}
        return {'preregistration.json':p,'sample.json':sample,'sample-trust.json':trust,
            'retrieval.json':es,'retrieval-trust.json':{'receipt_hashes':receipts,'sample_sha256':trust['sample_sha256']},
            'annotations.json':aa,'reviewers.json':rs,'taxonomy-evidence.json':taxonomy,
            'annotation-protocol.json':{'preregistration_sha256':trust['protocol_sha256']}}

    def test_generation_does_not_self_authenticate_manifest(self):
        with tempfile.TemporaryDirectory() as tmp,patch.object(audit,'verify_artifacts',wraps=audit.verify_artifacts) as verify:
            out=Path(tmp)/'generated';out.mkdir()
            _,manifest=audit.export(self.data(),out,evidence_revision='synthetic')
            self.assertFalse(verify.called)
            self.assertEqual(s.digest(manifest),s.digest(manifest))

    def test_second_pass_can_authenticate_against_external_root(self):
        data=self.data()
        with tempfile.TemporaryDirectory() as tmp:
            first=Path(tmp)/'first';second=Path(tmp)/'second';first.mkdir();second.mkdir()
            _,manifest=audit.export(data,first,evidence_revision='synthetic')
            external_root=s.digest(manifest)
            audit.export(data,second,evidence_revision='synthetic',trusted_manifest_hash=external_root)

    def test_coherent_reseal_cannot_replace_external_root(self):
        data=self.data()
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out';out.mkdir()
            _,manifest=audit.export(data,out,evidence_revision='synthetic')
            external_root=s.digest(manifest)
            (out/'assessment.json').write_text('{}',encoding='utf-8')
            manifest['artifacts']['assessment.json']=s.sha(b'{}')
            self.assertNotEqual(s.digest(manifest),external_root)
            with self.assertRaises(s.Invalid):
                audit.verify_artifacts(out,manifest,trusted_manifest_hash=external_root)


if __name__=='__main__':unittest.main()
