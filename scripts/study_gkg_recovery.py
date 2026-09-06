"""Phase 6A bounded recovery / offline export. Original studies remain read-only."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import csv
import io
import json
from pathlib import Path
import subprocess
from urllib.parse import urlencode,urlsplit
from datetime import datetime
import gkg_semantics as s
import gkg_recovery as r
from recovery_transport import fetch
from study_gkg_semantics import ROOT,read,write
from assess_gkg_semantics import verify_artifacts

BASELINE='b3eb34bdc789bef6a48615639948707e71353ba0'
PROTOCOL_COMMIT='0eba083'
STUDY=ROOT/'studies/gkg-semantics-v2'

def git_json(commit,path):return json.loads(subprocess.check_output(['git','show',commit+':'+path],cwd=ROOT))
def frozen():
    ref=git_json(PROTOCOL_COMMIT,'studies/gkg-semantics-v2/frozen-sample-reference.json')
    s.require(read(STUDY/'frozen-sample-reference.json')==ref,'frozen_reference_changed')
    data={}
    for name,h in ref['files'].items():
        path='studies/gkg-semantics-v1/'+name;value=read(ROOT/path)
        s.authenticate(value,h,'frozen_'+name);s.require(value==git_json(BASELINE,path),'baseline_input_changed');data[name]=value
    sample=data['sample.json'];s.require(len(sample['cases'])==120 and s.digest([c['case_id'] for c in sample['cases']])==ref['case_ids_sha256'],'frozen_cases_changed')
    p=read(STUDY/'phase6a-protocol.json');s.require(p==git_json(PROTOCOL_COMMIT,'studies/gkg-semantics-v2/phase6a-protocol.json'),'protocol_changed')
    return sample['cases'],{e['case_id']:e for e in data['retrieval.json']},p

def recover(case,prior,p,fetcher=fetch):
    attempts=[];candidates=[]
    def attempt(url,method,capture=None):
        receipt,blob=fetcher(url,p['network']);receipt.update(case_id=case['case_id'],method=method,capture=capture)
        if method!='wayback_availability_discovery':
            identity=r.identify(case,receipt,blob,prior,method=method,capture=capture);receipt['identity']=identity
            candidates.append(receipt)
        attempts.append(receipt);return receipt,blob
    original=case['DocumentIdentifier']
    a,_=attempt(original,'original_publisher')
    good=lambda a:a.get('identity',{}).get('identity_status')=='identity_confirmed' and bool(a['identity']['excerpt'])
    if not good(a) and original.startswith('http://'):
        a,_=attempt('https://'+original[7:],'same_path_https_candidate')
    if not good(a):
        discovery,blob=attempt(p['archive']['lookup']+'?'+urlencode({'url':original,'timestamp':case['batch_id']}),'wayback_availability_discovery')
        if blob is not None:
            try:
                response=json.loads(blob);s.require(isinstance(response,dict),'invalid_discovery')
                closest=response.get('archived_snapshots',{}).get('closest')
                if closest and closest.get('available') is True and str(closest.get('status'))=='200':
                    url=closest['url'];stamp=closest['timestamp'];r.archive_locator(url,original,stamp)
                    delta=abs((datetime.strptime(stamp,'%Y%m%d%H%M%S')-datetime.strptime(case['batch_id'],'%Y%m%d%H%M%S')).total_seconds())
                    s.require(delta<=p['archive']['max_capture_distance_days']*86400,'capture_outside_bound')
                    discovery['candidate']={'url':url,'timestamp':stamp}
                    attempt('https://'+url.split('://',1)[1],'dated_wayback_capture',stamp)
                else:discovery['discovery_result']='no_available_capture'
            except (ValueError,KeyError,TypeError,AttributeError) as exc:
                discovery['discovery_result']=str(exc) if isinstance(exc,s.Invalid) else 'invalid_discovery_response'
    s.require(len(attempts)<=p['network']['max_requests_per_case'],'attempt_bound')
    order={'identity_confirmed':0,'identity_probable_manual_review_required':1,'identity_mismatch':2,'identity_unresolved':3}
    chosen=min(candidates,key=lambda a:(order[a['identity']['identity_status']],not bool(a['identity']['excerpt']),a['content_sha256'] is None,attempts.index(a)))
    e={k:case[k] for k in ('case_id','token','year','cohort')}
    e.update(source=case['source_name'],publisher=case['source_name'],original_url=original,recovered_url=chosen['final_url'],
        retrieval_method=chosen['method'],retrieved_at=chosen['retrieved_at'],content_sha256=chosen['content_sha256'],
        archive_locator=chosen['final_url'] if chosen['method']=='dated_wayback_capture' else None,
        attempt_sha256=s.digest(chosen),**chosen['identity'])
    return attempts,e

def outputs(cases,attempts,evidence,out,*,input_commit):
    s.require(len(evidence)==120 and [e['case_id'] for e in evidence]==[c['case_id'] for c in cases],'frozen_output_cases')
    bycase={c['case_id']:[] for c in cases}
    for a in attempts:s.require(a['case_id'] in bycase,'orphan_attempt');bycase[a['case_id']].append(a)
    for e in evidence:
        aa=bycase[e['case_id']];s.require(aa and len(aa)<=4,'attempt_cardinality')
        match=[a for a in aa if s.digest(a)==e['attempt_sha256']];s.require(len(match)==1,'evidence_attempt_binding')
        a=match[0]
        for k,v in a['identity'].items():s.require(e[k]==v,'identity_claim_binding')
        s.require(e['content_sha256']==a['content_sha256'] and e['recovered_url']==a['final_url'],'source_claim_binding')
    packet=r.packet(evidence)
    counts=dict(Counter(e['identity_status'] for e in evidence));ready=[e for e in evidence if e['identity_status']=='identity_confirmed' and e['excerpt']]
    available=sum(e['content_sha256'] is not None for e in evidence)
    gates=all(sum(e['token']==t for e in ready)>=24 for t in s.TOKENS)
    for t in s.TOKENS:
        for y in sorted({c['year'] for c in cases if c['token']==t}):gates &= sum(e['token']==t and e['year']==y for e in ready)>=4
    stats={'version':'1.0.0','original_references':120,'recovered_body_count':available,'identity_counts':counts,'reviewable_evidence_count':len(ready),'unavailable_count':sum(all(a.get('content_sha256') is None for a in bycase[c['case_id']] if a['method']!='wayback_availability_discovery') for c in cases),
        'attempt_count':len(attempts),'failures':dict(Counter(a['failure'] for a in attempts if a['failure'])),
        'by_year':{str(y):dict(Counter(e['identity_status'] for e in evidence if e['year']==y)) for y in sorted({c['year'] for c in cases})},
        'human_semantic_reviews_completed':0,'recommendation':'ready_for_independent_human_review' if gates else 'continue_evidence_recovery'}
    files={'retrieval-attempts.json':attempts,'evidence.json':evidence,'human-review-packet.json':packet,'availability.json':stats,
        'evidence-trust.json':{'version':'1.0.0','origin':'Trusted recovery capture; independently pin its committed manifest before import. Not self-authenticated.','evidence_hashes':{e['case_id']:s.digest(e) for e in evidence},'attempts_sha256':s.digest(attempts)}}
    for n,v in files.items():write(out/n,v)
    buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=list(packet[0]),lineterminator='\n');writer.writeheader()
    for row in packet:
        # Spreadsheet formula injection is not a review operation.
        writer.writerow({k:("'"+v if isinstance(v,str) and v.startswith(('=','+','-','@','\t','\r')) else v) for k,v in row.items()})
    with (out/'human-review-packet.csv').open('xb') as f:f.write(buf.getvalue().encode('utf-8'))
    names=list(files)+['human-review-packet.csv']
    manifest={'version':'1.0.0','baseline':BASELINE,'protocol_commit':PROTOCOL_COMMIT,'input_commit':input_commit,
        'frozen_sample_sha256':'3a8710caabb8d571edbbd5f80276e00f25cec26c9622655d3b3db8d7045b9a46',
        'implementation':{n:s.sha((ROOT/'scripts'/n).read_bytes().replace(b'\r\n',b'\n').removeprefix(b'\xef\xbb\xbf')) for n in ('gkg_recovery.py','recovery_transport.py','study_gkg_recovery.py')},
        'artifacts':{n:s.sha((out/n).read_bytes()) for n in names}}
    write(out/'assessment-manifest.json',manifest)
    return stats,manifest

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--network-integration',action='store_true');ap.add_argument('--replay-commit');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    cases,priors,p=frozen();args.output.mkdir(parents=True,exist_ok=True)
    if args.network_integration:
        s.require(not args.replay_commit,'mode_conflict')
        local=ROOT/'artifacts/gkg-phase6a/captures';local.mkdir(parents=True,exist_ok=False)
        def task(c):
            a,e=recover(c,priors[c['case_id']],p);write(local/(c['case_id']+'.json'),{'attempts':a,'evidence':e});return a,e
        with ThreadPoolExecutor(max_workers=p['network']['concurrency']) as pool:result=list(pool.map(task,cases))
        stats,m=outputs(cases,[a for aa,_ in result for a in aa],[e for _,e in result],args.output,input_commit=PROTOCOL_COMMIT)
    else:
        s.require(args.replay_commit,'external_replay_commit_required')
        original=git_json(args.replay_commit,'studies/gkg-semantics-v2/assessment-manifest.json')
        verify_artifacts(STUDY,read(STUDY/'assessment-manifest.json'),trusted_manifest_hash=s.digest(original))
        attempts=read(STUDY/'retrieval-attempts.json');evidence=read(STUDY/'evidence.json')
        r.validate_evidence(evidence,cases,trusted_hashes=git_json(args.replay_commit,'studies/gkg-semantics-v2/evidence-trust.json')['evidence_hashes'])
        stats,m=outputs(cases,attempts,evidence,args.output,input_commit=PROTOCOL_COMMIT)
        s.require(m==original,'deterministic_replay_mismatch')
        verify_artifacts(args.output,m,trusted_manifest_hash=s.digest(original))
    print(json.dumps({'statistics':stats,'manifest_sha256':s.digest(m)}))

if __name__=='__main__':main()
