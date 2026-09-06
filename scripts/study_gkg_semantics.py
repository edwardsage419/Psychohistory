"""Offline Phase 5 sample builder from original authenticated archives."""
import argparse
import json
from pathlib import Path
import subprocess
import gkg_lossless as core
import gkg_indicator_metrics as metrics
import gkg_semantics as sem

ROOT=Path(__file__).resolve().parents[1]
BASELINE='046a43f299f56c7122e9cc488a86732e295dc00d'
STUDY=ROOT/'studies/gkg-semantics-v1'

def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,value):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(sem.canonical(value)+b'\n')

def baseline_json(path):
    b=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
    original=json.loads(b)
    sem.require(original==read(ROOT/path),'baseline_changed_'+path)
    return original

def candidates_from_corpus():
    manifest=baseline_json('studies/gkg-continuity-v1/manifest.json')
    published=baseline_json('studies/gkg-lossless-v1/results/study.json')
    acquisitions=baseline_json('studies/gkg-lossless-v1/results/provenance.json')['batches']
    pins=baseline_json('studies/gkg-indicators-v1/integrity-review/baseline-trust.json')['source_metric_hashes']
    sem.require(core.digest(manifest)==published['manifest_sha256'],'original_manifest')
    pmap={b['source']['batch_id']:b for b in published['batches']}
    amap={b['batch_id']:b for b in acquisitions}
    slots=manifest['batches']
    sem.require(len(slots)==len(pmap)==len(amap)==len(pins)==96,'original_96_cardinality')
    candidates=[]; outcomes=[]
    for slot in slots:
        bid=slot['batch_id']
        try:
            ledger=read(ROOT/'artifacts/gkg-phase3-run3'/f'{bid}.json')
            blob=core.read_snapshot(ROOT/'artifacts/gkg-study-96-v1/raw'/f"{amap[bid]['archive_sha256']}.zip")
            m=metrics.extract(blob,ledger,amap[bid],pmap[bid])
            sem.require(m['semantic_sha256']==pins[bid],'original_metric_pin')
            member,payload=core.verified_member(blob,ledger['source'])
            for row in ledger['rows']:
                if row['disposition']!='accepted':continue
                fields=core.body(payload[row['start']:row['end']]).decode('utf-8').split('\t')
                tokens=sorted(set(t for t in fields[7].split(';') if t))
                if not any(t in tokens for t in sem.TOKENS):continue
                candidates.append({'row_id':row['row_id'],'batch_id':bid,'year':int(bid[:4]),'cohort':slot['cohort'],
                    'line':row['line'],'start':row['start'],'end':row['end'],'raw_row_sha256':row['raw_sha256'],
                    'archive_sha256':ledger['source']['archive_sha256'],'member':member,'ledger_sha256':ledger['semantic_sha256'],
                    'source_metric_sha256':m['semantic_sha256'],'source_reference':ledger['source']['source_url'],
                    'source_name':fields[3],'DocumentIdentifier':fields[4],'record_id':fields[0],
                    'theme_count':len(tokens),'tokens':tokens})
            outcomes.append({'batch_id':bid,'status':'authenticated','archive_sha256':ledger['source']['archive_sha256'],
                'archive_bytes':len(blob),'source_metric_sha256':m['semantic_sha256']})
        except (ValueError,OSError,KeyError,core.Rejection) as exc:
            outcomes.append({'batch_id':bid,'status':'failed','failure':getattr(exc,'code',type(exc).__name__)})
    write(ROOT/'artifacts/gkg-phase5/corpus-verification.json',outcomes)
    sem.require(all(o['status']=='authenticated' for o in outcomes),'corpus_failure_see_outcomes')
    return candidates,outcomes

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--freeze-sample',action='store_true');args=parser.parse_args()
    if args.freeze_sample:
        p=read(STUDY/'preregistration.json')
        frozen=json.loads(subprocess.check_output(['git','show','5ddf7e3:studies/gkg-semantics-v1/preregistration.json'],cwd=ROOT))
        sem.require(p==frozen,'preregistration_modified')
        candidates,outcomes=candidates_from_corpus()
        sample=sem.select_sample(candidates,p,protocol_hash=sem.digest(frozen))
        sem.validate_sample(sample,p,protocol_hash=sem.digest(frozen),sample_hash=sem.digest(sample),candidates=list(reversed(candidates)))
        write(ROOT/'artifacts/gkg-phase5/candidates.json',candidates)
        write(STUDY/'sample.json',sample)
        write(STUDY/'corpus-verification.json',outcomes)
        write(STUDY/'sample-trust.json',{'protocol_sha256':sem.digest(frozen),'sample_sha256':sem.digest(sample),
            'origin':'Trusted raw/ledger replay against accepted baseline; commit this root before retrieval.',
            'baseline':BASELINE,'preregistration_commit':'5ddf7e3'})
        print(json.dumps({'selected':len(sample['cases']),'sample_sha256':sem.digest(sample),'corpus_batches':len(outcomes)}))

if __name__=='__main__':main()
