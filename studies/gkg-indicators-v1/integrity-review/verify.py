"""Offline, exact numerical comparison against the immutable b3627a0 Git revision."""
import argparse
import gzip
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'scripts'))
import gkg_lossless as core
import indicator_engine as engine
import study_gkg_indicators as study

BASE='b3627a059ecf4332291f58cd744941978bb45838'
BASE_PATH='studies/gkg-indicators-v1/results/'
KINDS=('normalized_observations','indicator_values','quality','provenance','batch_receipts')


def git_bytes(path):
    return subprocess.check_output(['git','show',BASE+':'+path],cwd=ROOT)


def git_json(path):
    return json.loads(git_bytes(path))


def identity_map(bundle):
    result={}
    observations=bundle['normalized_observations']+[v['observation'] for v in bundle['indicator_values']]
    for o in observations:
        key=(o['metric_id'],o['observed_at'])
        if o['observation_id'] in result or key in result.values():raise ValueError('duplicate_identity')
        result[o['observation_id']]=key
    return result


def observation_projection(o, aggregate=False):
    ignored={'observation_id','source_record_reference'}
    if aggregate:ignored.add('source_snapshot_sha256')
    return {k:v for k,v in o.items() if k not in ignored}


def numerical_projection(bundle):
    ids=identity_map(bundle)
    normalized={ids[o['observation_id']]:observation_projection(o) for o in bundle['normalized_observations']}
    values={}
    for v in bundle['indicator_values']:
        value={**v,'observation':observation_projection(v['observation'],True)}
        values[ids[v['observation']['observation_id']]]=value
    quality={ids[q['observation_id']]:{k:v for k,v in q.items() if k!='observation_id'} for q in bundle['quality']}
    return normalized,values,quality


def verify(first,second,trusted_manifest_hash,output):
    replay=study.compare_runs(first,second,trusted_manifest_hashes=[trusted_manifest_hash]*2)
    baseline_manifest=git_json(BASE_PATH+'semantic-manifest.json')
    baseline_bytes={name:git_bytes(BASE_PATH+name) for name in baseline_manifest['files']}
    if any(core.sha(blob)!=baseline_manifest['files'][name] for name,blob in baseline_bytes.items()):
        raise ValueError('baseline_git_artifact_hash')
    original={k:[json.loads(line) for line in baseline_bytes[k+'.jsonl'].splitlines()] for k in KINDS}
    current={k:[json.loads(line) for line in (first/(k+'.jsonl')).read_bytes().splitlines()] for k in KINDS}
    metrics=[json.loads(gzip.decompress(p.read_bytes())) for p in sorted((first/'local-source-metrics').glob('*.gz'))]
    outcomes=json.loads(baseline_bytes['batch-outcomes.json'])
    pins={b['batch_id']:b['source_metric_sha256'] for b in outcomes}
    if len(metrics)!=96 or len(pins)!=96:raise ValueError('requires_original_96')
    definitions=git_json('studies/gkg-indicators-v1/definitions.json')
    history=git_json('studies/gkg-indicators-v1/definition-history.json')
    old_code=core.digest(baseline_manifest['code_hashes'])
    new_code=core.digest(study.read(first/'semantic-manifest.json')['code_hashes'])
    for bundle,code in ((original,old_code),(current,new_code)):
        engine.validate_bundle(bundle,definitions,source_metrics=metrics,trusted_metric_hashes=pins,history=history,implementation_sha256=code)
    left,right=numerical_projection(original),numerical_projection(current)
    if left!=right:raise ValueError('legitimate_output_changed')
    unchanged=[name for name,blob in baseline_bytes.items() if (first/name).read_bytes()==blob]
    scientific=('assessment.json','batch-metrics.json','batch-outcomes.json','candidate-evaluation.json','cooccurrence.json','deferred-candidates.json','historical-assessment.json','inventory.json.gz')
    if not set(scientific)<=set(unchanged):raise ValueError('scientific_evidence_changed')
    protected=['app.js','index.html','style.css','data/gdelt.json','scripts/update_gdelt.py','.github/workflows/update-gdelt.yml']
    preserved=[]
    for name in protected:
        old=git_bytes(name);new=(ROOT/name).read_bytes()
        if old!=new.replace(b'\r\n',b'\n'):raise ValueError('protected_file_changed')
        preserved.append({'path':name,'baseline_git_sha256':core.sha(old),'working_sha256':core.sha(new),'content_unchanged':True})
    for folder in ('studies/gkg-continuity-v1','studies/gkg-lossless-v1'):
        if subprocess.check_output(['git','diff',BASE,'--',folder],cwd=ROOT):raise ValueError('prior_evidence_changed')
    result={'schema_version':'1.0.0','baseline_commit':BASE,'replay':replay,'trusted_replay_manifest_sha256':trusted_manifest_hash,
        'source_metrics_matching_original_pins':len(metrics),'original_bundle_passed_authenticated_validation':True,
        'normalized_observations_unchanged':len(left[0]),'indicator_values_unchanged':len(left[1]),'quality_records_unchanged':len(left[2]),
        'numerical_projection_sha256':core.digest([sorted(d.items()) for d in left]),'byte_identical_scientific_files':unchanged,
        'changed_metadata':'Implementation fingerprints and dependent receipt/provenance/observation IDs change; numerical, quality, definition and acquisition fields are equal.',
        'raw_archives':{'count':96,'bytes':sum(m['provenance']['source']['archive_bytes'] for m in metrics),'verified_by':'Both replay runs read every ZIP and authenticate its original source hash, CRC, member and Phase 3 row ledger before extraction.'},
        'source_evidence_gzip_bytes':sum(p.stat().st_size for p in (first/'local-source-metrics').glob('*.gz')),
        'additional_source_evidence_format':'none; existing full metrics resolved externally, no extra bundle payload',
        'protected_files':preserved,'phase2_phase3_evidence_unchanged':True,
        'recommendation':'continue_semantic_validation','runs':[study.read(p/'execution.json') for p in (first,second)]}
    study.write(output,result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('first',type=Path);p.add_argument('second',type=Path)
    p.add_argument('--trusted-manifest-sha256',required=True,help='Root from independently trusted completed execution; never derive it from a candidate being audited.')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=verify(a.first,a.second,a.trusted_manifest_sha256,a.output)
    print(json.dumps({k:result[k] for k in ('source_metrics_matching_original_pins','normalized_observations_unchanged','indicator_values_unchanged','quality_records_unchanged','recommendation')}))
