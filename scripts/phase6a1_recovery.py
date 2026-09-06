"""Phase 6A.1: fixed 26-case delta, provider circuit, no semantic judgments."""
import argparse
from collections import Counter
import copy
import csv
import io
import json
from pathlib import Path
import subprocess
from urllib.parse import urlencode
import gkg_semantics as s
import gkg_recovery as r
from recovery_transport import fetch
from study_gkg_semantics import ROOT,read,write
from assess_gkg_semantics import verify_artifacts

BASE='f7073ab51e4eb0195fa740a38e96c2a945453602'
DIR=ROOT/'studies/gkg-semantics-v2'
TARGET_STATES=('identity_probable_manual_review_required','identity_mismatch')

def pinned(name):return json.loads(subprocess.check_output(['git','show',BASE+':studies/gkg-semantics-v2/'+name],cwd=ROOT))
def level(e):
    if e['identity_status']!='identity_confirmed':return 'E0'
    if not e['excerpt']:return 'E1'
    if e['retrieval_method'] in ('original_publisher','same_path_https_candidate','canonical_publisher'):return 'E3'
    if e['retrieval_method']=='dated_wayback_capture':return 'E2'
    return 'E0' # Similar syndicated content has no authenticated equivalence anchor here.

def resolve(base,delta,*,base_root,delta_root):
    s.authenticate(base,base_root,'baseline_evidence');s.authenticate(delta,delta_root,'triage_delta')
    expected={e['case_id'] for e in base if e['identity_status'] in TARGET_STATES}
    s.require(len(delta)==len(expected) and {e['case_id'] for e in delta}==expected,'target_case_set')
    dm={e['case_id']:e for e in delta};result=[]
    for old in base:
        e=copy.deepcopy(dm.get(old['case_id'],old))
        for k in ('case_id','token','year','cohort','original_url'):s.require(e[k]==old[k],'frozen_metadata_changed')
        e['evidence_sufficiency_version']='1.0.0';e['evidence_sufficiency']=level(e);result.append(e)
    return result

def import_reviews(annotations,registry,cases,evidence,**trust):
    r.validate_evidence(evidence,cases,trusted_hashes=trust['evidence_hashes'])
    em={e['case_id']:e for e in evidence}
    for a in annotations:
        s.require(a['case_id'] in em,'unknown_case');e=em[a['case_id']]
        s.require(e.get('evidence_sufficiency')==level(e) and level(e) in ('E2','E3'),'insufficient_semantic_evidence')
    return r.import_humans(annotations,registry,cases,evidence,**trust)

class ProviderCircuit:
    def __init__(self,budget=1):self.remaining=budget;self.failed=False
    def request(self,url,cfg,fetcher=fetch):
        if self.failed or self.remaining<=0:return {'requested_url':url,'failure':'provider_budget_or_circuit_open','content_sha256':None},None
        self.remaining-=1;receipt,blob=fetcher(url,cfg)
        if receipt.get('failure') or blob is None:self.failed=True
        return receipt,blob

def identity(case,old,receipt,blob,method):
    prior={'content_sha256':old['content_sha256'],'source_hash_scope':'complete_response_body'}
    result=r.identify(case,receipt,blob,prior,method='original_publisher')
    # Resolve only objective same-publisher canonical relocation with exact captured-body continuity.
    # A similar title, domain, timing, or new URL without that body binding cannot upgrade identity.
    final=receipt.get('final_url')
    if (blob is not None and receipt['content_sha256']==old['content_sha256'] and final and
        r.uri(final)[0]==r.uri(case['DocumentIdentifier'])[0] and
        final in old.get('canonical_urls',[]) and
        method=='original_publisher' and receipt.get('requested_url')==case['DocumentIdentifier']):
        adjusted=dict(case,DocumentIdentifier=final)
        check=r.identify(adjusted,receipt,blob,prior,method='original_publisher')
        if check['identity_status']=='identity_confirmed':
            result=check;result['identity_reason']='original_publisher_redirect_canonical_date_and_prior_exact_body'
    return result

def run(cases,base,p,fetcher=fetch):
    targets=[e for e in base if e['identity_status'] in TARGET_STATES]
    s.require(len(targets)==26 and [e['case_id'] for e in targets]==p['target_case_ids'],'target_set')
    cm={c['case_id']:c for c in cases};attempts=[];delta=[];cache={};cache_hits=0
    cfg={'max_bytes':p['max_bytes'],'socket_timeout_seconds':p['socket_timeout_seconds'],'request_deadline_seconds':p['request_deadline_seconds'],'max_redirects':p['max_redirects']}
    circuit=ProviderCircuit(p['wayback_probe_budget'])
    # One bounded independent provider probe; failures are not multiplied by 26.
    first=targets[0];probe_url='https://archive.org/wayback/available?'+urlencode({'url':first['original_url'],'timestamp':cm[first['case_id']]['batch_id']})
    probe,discovery=circuit.request(probe_url,cfg,fetcher);probe.update(case_id=first['case_id'],method='wayback_discovery_probe')
    if discovery is not None:
        # Locate only: no capture or syndicated article is accepted from discovery alone.
        try:probe['discovery']=json.loads(discovery)
        except ValueError:probe['discovery_failure']='invalid_json'
    attempts.append(probe)
    for old in targets:
        c=cm[old['case_id']];options=[(old['original_url'],'original_publisher')]
        for u in old.get('canonical_urls',[])+[old.get('recovered_url')]:
            if u and s.public_reference(u) and r.uri(u)[0]==r.uri(old['original_url'])[0] and u not in [v for v,_ in options]:options.append((u,'canonical_publisher'))
        best=copy.deepcopy(old);observed=[]
        for url,method in options[:p['publisher_fetches_per_case']]:
            if url in cache:
                receipt,ident=copy.deepcopy(cache[url]);cache_hits+=1
                # Cached identity is case-specific: a URL cache must not substitute another case's proof.
                if ident['case_id']!=c['case_id']:continue
                candidate=ident['result']
            else:
                receipt,blob=fetcher(url,cfg)
                candidate=identity(c,old,receipt,blob,method)
                if receipt.get('content_sha256'):cache[url]=(copy.deepcopy(receipt),{'case_id':c['case_id'],'result':copy.deepcopy(candidate)})
            receipt.update(case_id=c['case_id'],method=method,identity=candidate)
            attempts.append(receipt);observed.append({'url':url,'receipt_sha256':s.digest(receipt),'identity_status':candidate['identity_status'],'reason':candidate['identity_reason']})
            if candidate['identity_status']=='identity_confirmed':
                best.update(candidate,recovered_url=receipt['final_url'],retrieval_method=method,content_sha256=receipt['content_sha256'],retrieved_at=receipt['retrieved_at'],attempt_sha256=s.digest(receipt));break
        best['phase6a1']={'version':'1.0.0','baseline_evidence_sha256':s.digest(old),'attempts':observed,'provider_probe_sha256':s.digest(probe),
            'conflict_reason':old['identity_reason'],'final_machine_identity_state':best['identity_status'],'unchanged_reason':None if best['identity_status']=='identity_confirmed' else 'No sufficient objective identity upgrade; retain accepted baseline evidence, failures remain visible.'}
        delta.append(best)
    return delta,attempts,cache_hits

def publish(base,delta,attempts,review_protocol,out):
    evidence=resolve(base,delta,base_root=s.digest(base),delta_root=s.digest(delta)) # generation, not external authentication claim
    packet=r.packet(evidence)
    for row,e in zip(packet,evidence):row.update(evidence_sufficiency=e['evidence_sufficiency'],evidence_sufficiency_version='1.0.0',provenance={'baseline':BASE,'attempt_sha256':e['attempt_sha256']},review_protocol_version=review_protocol['version'],review_protocol_sha256=s.digest(review_protocol))
    stats={'version':'1.0.0','targeted':26,'original_references':120,'before':dict(Counter(e['identity_status'] for e in base)),'after':dict(Counter(e['identity_status'] for e in evidence)),
        'levels':dict(Counter(e['evidence_sufficiency'] for e in evidence)),'attempts':len(attempts),'failures':dict(Counter(a['failure'] for a in attempts if a.get('failure'))),'human_semantic_reviews':0,
        'recommendation':'ready_for_targeted_human_identity_review' if any(e['identity_status']=='identity_probable_manual_review_required' for e in delta) else 'continue_evidence_recovery'}
    for name,value in [('phase6a1-triage.json',delta),('phase6a1-attempts.json',attempts),('phase6a1-availability.json',stats)]:write(out/name,value)
    # User-authorized updated packet; old packet recoverable from accepted baseline commit.
    (out/'human-review-packet.json').write_bytes(s.canonical(packet)+b'\n')
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=list(packet[0]),lineterminator='\n');writer.writeheader()
    for row in packet:
        converted={k:json.dumps(v,sort_keys=True) if isinstance(v,dict) else v for k,v in row.items()}
        writer.writerow({k:("'"+v if isinstance(v,str) and v.startswith(('=','+','-','@','\t','\r')) else v) for k,v in converted.items()})
    (out/'human-review-packet.csv').write_text(stream.getvalue(),encoding='utf-8',newline='\n')
    return stats

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--network-integration',action='store_true',required=True);args=ap.parse_args()
    s.require(not (DIR/'phase6a1-triage.json').exists() and not (ROOT/'artifacts/gkg-phase6a1/capture.json').exists(),'recovery_already_captured')
    base=pinned('evidence.json');s.require(base==read(DIR/'evidence.json'),'baseline_evidence_changed')
    manifest=pinned('assessment-manifest.json');verify_artifacts(DIR,read(DIR/'assessment-manifest.json'),trusted_manifest_hash=s.digest(manifest))
    cases=read(ROOT/'studies/gkg-semantics-v1/sample.json')['cases'];s.authenticate(read(ROOT/'studies/gkg-semantics-v1/sample.json'),'3a8710caabb8d571edbbd5f80276e00f25cec26c9622655d3b3db8d7045b9a46','frozen_sample')
    p=read(DIR/'phase6a1-protocol.json');original=json.loads(subprocess.check_output(['git','show','262d09d:studies/gkg-semantics-v2/phase6a1-protocol.json'],cwd=ROOT));s.require(p==original,'triage_protocol_changed')
    delta,attempts,hits=run(cases,base,p)
    local=ROOT/'artifacts/gkg-phase6a1';local.mkdir(parents=True,exist_ok=True)
    write(local/'capture.json',{'delta':delta,'attempts':attempts,'cache_hits':hits})
    stats=publish(base,delta,attempts,pinned('review-import-contract.json'),DIR)
    print(json.dumps({'statistics':stats,'cache_hits':hits}))

if __name__=='__main__':main()
