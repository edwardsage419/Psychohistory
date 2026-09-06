#!/usr/bin/env python3
"""Offline Phase 4 study. Raw archives and ledgers are read-only inputs."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import json
import math
from pathlib import Path
import time

from contracts import ContractError
import gkg_lossless as core
import gkg_indicator_metrics as gm
from indicator_engine import build, checked_metrics
from indicator_definitions import validate_registry

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / 'studies/gkg-indicators-v1'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    with Path(path).open('xb') as f:
        f.write(core.canonical(value) + b'\n')


def code_hashes():
    paths = [*sorted((ROOT / 'scripts').glob('*indicator*.py')),
             *(ROOT / 'scripts' / name for name in ('gkg_lossless.py', 'gkg_lossless_contracts.py', 'validate_gkg.py', 'contracts.py')),
             *sorted((ROOT / 'schemas').glob('*.json'))]
    # Tests do not change transformation identity. They have separate execution evidence.
    return {p.relative_to(ROOT).as_posix(): core.sha(p.read_bytes()) for p in paths if not p.name.startswith('test_')}


def correlation(a, b):
    if len(a) < 2: return None
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sa, sb = sum((x - ma)**2 for x in a), sum((y - mb)**2 for y in b)
    return sum((x-ma)*(y-mb) for x,y in zip(a,b)) / math.sqrt(sa*sb) if sa and sb else None


def evaluate(inv, metrics, definitions):
    entries = {e['token']: e for e in inv['entries']}
    results = []
    for d in definitions:
        token = d['transformation']['parameters']['token']
        e = entries.get(token)
        if e is None:
            raise ContractError(token, 'candidate_unobserved')
        passed = e['batch_coverage'] >= 12 and len(e['years_present']) >= 3
        if not passed:
            raise ContractError(token, 'preregistered_candidate_gate')
        sensitivity = [m['theme_counts'].get(token, 0) / m['nonempty_theme_rows'] - m['theme_counts'].get(token, 0) / m['accepted_rows'] for m in metrics if m['nonempty_theme_rows']]
        counts = [m['theme_counts'].get(token, 0) for m in metrics]
        volume = [m['accepted_rows'] for m in metrics]
        prevalence = [n/v if v else 0 for n,v in zip(counts,volume)]
        recent = [m for m in metrics if m['batch_id'].startswith('20260904')]
        results.append({'token': token, 'selected': passed, 'status': 'experimental',
            'selection_rule': 'provider example plus >=12 batches and >=3 years; semantic diversity',
            'rows': e['rows'], 'batch_coverage': e['batch_coverage'], 'years_present': e['years_present'],
            'zero_cohorts': [k for k,v in e['cohorts'].items() if not v['rows']], 'cohorts': e['cohorts'],
            'primary_prevalence': e['prevalence'], 'documentation': d['documentation'],
            'documentation_quality': 'provider use example; lexical matching rules and historic versions unavailable',
            'semantic_clarity': d['semantic_interpretation'],
            'denominator_sensitivity_max_absolute': max(sensitivity, default=None),
            'denominator_sensitivity_mean_absolute': sum(sensitivity)/len(sensitivity) if sensitivity else None,
            'batch_count_vs_volume_pearson': correlation(counts,volume),
            'batch_prevalence_vs_volume_pearson': correlation(prevalence,volume),
            'recent_count_vs_volume_pearson': correlation([m['theme_counts'].get(token,0) for m in recent],[m['accepted_rows'] for m in recent]),
            'batch_count_prevalence_rank_disagreements': sum((counts[i]-counts[j])*(prevalence[i]-prevalence[j]) < 0 for i in range(len(metrics)) for j in range(i)),
            'correlation_scope': 'descriptive convenience sample; no significance or causal test',
            'duplicate_reporting': gm.duplicate_diagnostic(metrics,token),
            'cross_source_suitability': 'media-tag prevalence could be compared with a separately validated media series; no direct equivalence to event or outcome series',
            'geographic_ambiguity': 'collection scope only; no source/mentioned/event/subject geography equivalence',
            'biases': d['known_biases'], 'structural_break_assessment': 'cohort differences observable; sparse sample cannot distinguish topic volume, outlet mix or taxonomy/extractor changes',
            'historical_interpretability': 'retrospective literal-token rule only; cross-year conceptual equivalence unvalidated'})
    return results


def study(manifest_path, raw_root, ledger_root, output, reverse=False):
    manifest_path, raw_root, ledger_root, output = map(lambda p: Path(p).resolve(), (manifest_path,raw_root,ledger_root,output))
    inputs = [manifest_path,raw_root,ledger_root,STUDY.resolve(),(ROOT/'studies/gkg-lossless-v1').resolve()]
    if any(output == p or output in p.parents or p in output.parents for p in inputs):
        raise ContractError('output', 'input_output_overlap')
    output.mkdir(parents=True,exist_ok=False)
    start = time.perf_counter()
    run_started = datetime.now(timezone.utc).isoformat()
    manifest = read(manifest_path)
    batches = manifest['batches']
    ids = [b['batch_id'] for b in batches]
    if len(ids) != 96 or len(set(ids)) != 96:
        raise ContractError('manifest', 'requires_96_distinct_batches')
    published = read(ROOT/'studies/gkg-lossless-v1/results/study.json')
    if core.digest(manifest) != published['manifest_sha256']:
        raise ContractError('manifest','phase3_manifest_binding')
    pmap = {b['source']['batch_id']:b for b in published['batches']}
    acquisitions = read(ROOT/'studies/gkg-lossless-v1/results/provenance.json')['batches']
    amap = {b['batch_id']:b for b in acquisitions}
    if len(pmap) != 96 or len(amap) != 96 or set(pmap) != set(ids) or set(amap) != set(ids):
        raise ContractError('inputs','batch_set_mismatch')
    definitions, history = read(STUDY/'definitions.json'),read(STUDY/'definition-history.json')
    validate_registry(definitions,history)
    code = code_hashes()
    metrics, outcomes = [], []
    cache = output/'local-source-metrics'; cache.mkdir()
    for i,b in enumerate(sorted(batches,key=lambda b:b['batch_id'],reverse=reverse),1):
        batch_id = b['batch_id']
        try:
            a = amap[batch_id]
            if b['url'] != a['source_url']:
                raise ContractError(batch_id,'manifest_source_url')
            ledger = read(ledger_root/(batch_id+'.json'))
            blob = core.read_snapshot(raw_root/(a['archive_sha256']+'.zip'))
            m = gm.extract(blob,ledger,a,pmap[batch_id])
            metrics.append(m)
            (cache/(batch_id+'.json.gz')).write_bytes(gzip.compress(core.canonical(m),mtime=0))
            outcomes.append({'batch_id':batch_id,'status':'passed','source_metric_sha256':m['semantic_sha256']})
        except (core.Rejection,ContractError,OSError,ValueError,KeyError,TypeError) as exc:
            outcomes.append({'batch_id':batch_id,'status':'failed','code':getattr(exc,'code',type(exc).__name__)})
        if i % 12 == 0: print(f'verified {i}/96',flush=True)
    outcomes.sort(key=lambda b:b['batch_id'])
    write(output/'batch-outcomes.json',outcomes)
    if any(b['status']=='failed' for b in outcomes):
        write(output/'failure.json',{'status':'failed','code':'batch_verification_failed','failed_batches':sum(b['status']=='failed' for b in outcomes)})
        return False
    metrics = checked_metrics(metrics)
    inv = gm.inventory(metrics,{b['batch_id']:b['cohort'] for b in batches},read(STUDY/'candidate-sources.json'))
    invbytes = core.canonical(inv)+b'\n'
    (output/'inventory.json.gz').write_bytes(gzip.compress(invbytes,mtime=0))
    candidates = evaluate(inv,metrics,definitions)
    write(output/'candidate-evaluation.json',candidates)
    selected={d['transformation']['parameters']['token'] for d in definitions}
    write(output/'deferred-candidates.json',{'selected':sorted(selected),
        'unregistered_observed_tokens':len(inv['entries'])-len(selected),
        'policy':'source metrics only; no automatic indicator registration',
        'reason':'outside bounded official-example panel; extraction meaning and historical semantic validity unresolved',
        'examples':[{ 'token':e['token'],'rows':e['rows'],'status':'deferred',
            'reason':'not needed for panel diversity; no classifier or historical semantic validation'}
            for e in inv['entries'] if e['token'] in ('ELECTION','ARMEDCONFLICT','WB_1406_DISEASES')],
        'rejected_interpretations':['event count','risk','severity','public opinion','economic magnitude','conflict intensity'],
        'external_comparison':'deferred; no comparable complete daily geographic series in this corpus'})
    write(output/'cooccurrence.json',gm.cooccurrence(metrics,[d['transformation']['parameters']['token'] for d in definitions]))
    bundle = build(metrics,definitions,history,core.digest(code),max(a['finished_at'] for a in acquisitions))
    for name,records in bundle.items():
        with (output/(name+'.jsonl')).open('xb') as f:
            for record in records: f.write(core.canonical(record)+b'\n')
    compact_metrics = [{k:v for k,v in m.items() if k not in ('documents','theme_counts','provenance','source_name_counts')} for m in metrics]
    write(output/'batch-metrics.json',compact_metrics)
    outlets = Counter()
    for m in metrics: outlets.update(m['source_name_counts'])
    vocabulary = {k: {e['token'] for e in inv['entries'] if e['cohorts'][k]['rows']} for k in sorted(set(b['cohort'] for b in batches))}
    historical = {'cohorts': {k:{'distinct_tokens':len(v),'batches':sum(b['cohort']==k for b in batches),
                'accepted_rows':sum(m['accepted_rows'] for m in metrics if next(b['cohort'] for b in batches if b['batch_id']==m['batch_id'])==k)} for k,v in vocabulary.items()},
        'cohort_vocabulary_jaccard': [{'left':a,'right':b,'jaccard':len(vocabulary[a]&vocabulary[b])/len(vocabulary[a]|vocabulary[b])} for a in vocabulary for b in vocabulary if a<b],
        'interpretation':'lexical differences only; sample volume and provider taxonomy/extractor drift are confounded'}
    write(output/'historical-assessment.json',historical)
    summary = {'schema_version':'1.0.0','batches':96,'accepted_rows':inv['accepted_rows'],'quarantined_rows':inv['quarantined_rows'],
        'distinct_tokens':len(inv['entries']),'empty_theme_rows':inv['empty_theme_rows'],
        'empty_theme_fraction':inv['empty_theme_rows']/inv['accepted_rows'],
        'within_row_repeated_tokens':sum(m['within_row_repeated_tokens'] for m in metrics),
        'empty_delimiter_segments':sum(m['empty_delimiter_segments'] for m in metrics),
        'lexical_families':dict(sorted(Counter(e['lexical_family'] for e in inv['entries']).items())),
        'exact_identifier_diagnostic':gm.duplicate_diagnostic(metrics),
        'distinct_source_names':len(outlets),'top_source_names':outlets.most_common(10),
        'complete_hourly_values':sum(v['window_minutes']==60 and v['observation']['value'] is not None for v in bundle['indicator_values']),
        'missing_daily_values':sum(v['window_minutes']==1440 and v['observation']['value'] is None for v in bundle['indicator_values']),
        'recommendation':'continue_semantic_validation',
        'reason':'engineering foundation is testable; historical semantic stability and classifier validity are not established',
        'external_validation':{'status':'deferred','series_acquired':0,'reason':'no paired complete daily series or defensible geographic/outcome-equivalence mapping in this sparse corpus'},
        'source_time':'batch timestamp only','spatial_scope':'collection only; null observation geography',
        'next_issue':'Preregister bounded human semantic audits and provider-version evidence for selected media tokens; extend temporal sampling only with an explicit continuity study.'}
    write(output/'assessment.json',summary)
    sizes = {p.name: p.stat().st_size for p in sorted(output.iterdir()) if p.is_file()}
    rawbytes = sum(a['archive_bytes'] for a in acquisitions)
    metricbytes = sum(p.stat().st_size for p in cache.iterdir())
    storage = {'measurement':'actual UTF-8 serialization bytes; gzip mtime=0; no storage engine or paid dependency',
        'sample_batches':96,'raw_archives_bytes':rawbytes,'local_full_source_metrics_gzip_bytes':metricbytes,
        'inventory_uncompressed_bytes':len(invbytes),'artifact_bytes':sizes,
        'definition_and_history_bytes':sum((STUDY/f).stat().st_size for f in ('definitions.json','definition-history.json')),
        'quarantine_evidence_bytes':(ROOT/'studies/gkg-lossless-v1/results/quarantine.json').stat().st_size,
        'extrapolations':{},'limitations':'96 batches equal 24 hours of batch slots but span seven dates; forecasts of future volume are not measurements; compression and taxonomy size may change',
        'retention':'retain corpus and irreplaceable quarantine/provenance permanently; derived records normally retained; ordinary public raw archives only future configurable policy, no deletion implemented'}
    for label,n in {'raw_archives':rawbytes,'local_full_source_metrics_gzip':metricbytes,
        'normalized_observations':sizes['normalized_observations.jsonl'],
        'batch_receipts':sizes['batch_receipts.jsonl'],
        'source_quality':sum(len(core.canonical(q))+1 for q in bundle['quality'] if q['layer']=='source_metric')}.items():
        storage['extrapolations'][label]={'basis':'measured bytes / 96 batches * 96 slots/day','day_bytes':n,'30_day_bytes':n*30,'365_day_bytes':n*365}
    # Indicator output is window-shaped, so extrapolate per observed window type, not per sampled day.
    for minutes,per_day in ((60,24),(1440,1)):
        vs=[v for v in bundle['indicator_values'] if v['window_minutes']==minutes]
        value_ids={v['observation']['observation_id'] for v in vs}
        groups={'indicator_values':vs,'indicator_quality':[q for q in bundle['quality'] if q['observation_id'] in value_ids],
                'indicator_provenance':[p for p in bundle['provenance'] if p['observation_id'] in value_ids]}
        for name,rows in groups.items():
            measured=sum(len(core.canonical(r))+1 for r in rows)
            daily=measured/len(rows)*len(definitions)*per_day
            storage['extrapolations'][name+'_'+str(minutes)+'m']={'measured_bytes':measured,'measured_records':len(rows),
                'basis':'bytes/record * 7 indicators * windows/day; daily samples are incomplete and may overstate missing-list storage',
                'day_bytes':daily,'30_day_bytes':daily*30,'365_day_bytes':daily*365}
    write(output/'storage.json',storage)
    if code_hashes() != code:
        raise ContractError('code','implementation_changed_during_run')
    files = {p.name:core.sha(p.read_bytes()) for p in sorted(output.iterdir()) if p.is_file()}
    write(output/'semantic-manifest.json',{'schema_version':'1.0.0','input_manifest_sha256':core.digest(manifest),
        'phase3_study_sha256':core.sha((ROOT/'studies/gkg-lossless-v1/results/study.json').read_bytes()),
        'definitions_sha256':core.digest(definitions),'definition_history_sha256':core.digest(history),
        'code_hashes':code,'files':files,'semantic_sha256':core.digest(files)})
    write(output/'execution.json',{'started_at':run_started,'finished_at':datetime.now(timezone.utc).isoformat(),
        'duration_seconds':time.perf_counter()-start,'reverse_input':reverse,'semantic_comparison_excludes':['execution.json'],
        'status':'passed'})
    return True


def compare_runs(first, second):
    first,second=Path(first).resolve(),Path(second).resolve()
    if first==second or (first/'semantic-manifest.json').samefile(second/'semantic-manifest.json'):
        raise ContractError('replay','same_evidence')
    manifests=[]
    for root in (first,second):
        manifest=read(root/'semantic-manifest.json')
        if manifest['semantic_sha256']!=core.digest(manifest['files']):
            raise ContractError('replay','manifest_hash')
        expected=set(manifest['files'])|{'semantic-manifest.json','execution.json'}
        if {p.name for p in root.iterdir() if p.is_file()}!=expected:
            raise ContractError('replay','artifact_set')
        for name,h in manifest['files'].items():
            if Path(name).name!=name or core.sha((root/name).read_bytes())!=h:
                raise ContractError('replay','artifact_hash')
        if read(root/'execution.json')['status']!='passed':
            raise ContractError('replay','incomplete_run')
        manifests.append(manifest)
    if manifests[0]!=manifests[1]:
        raise ContractError('replay','semantic_mismatch')
    return {'schema_version':'1.0.0','status':'passed','distinct_runs':True,
        'semantic_sha256':manifests[0]['semantic_sha256'],'compared_files':sorted(manifests[0]['files']),
        'excluded':['execution.json'],'rule':'all stable output bytes and input/code/definition pins equal'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',type=Path,default=ROOT/'studies/gkg-continuity-v1/manifest.json')
    p.add_argument('--raw',type=Path,default=ROOT/'artifacts/gkg-study-96-v1/raw')
    p.add_argument('--ledgers',type=Path,default=ROOT/'artifacts/gkg-phase3-run3')
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--reverse',action='store_true')
    a=p.parse_args()
    try:
        return 0 if study(a.manifest,a.raw,a.ledgers,a.output,a.reverse) else 2
    except (ContractError,core.Rejection,OSError,ValueError,KeyError,TypeError) as exc:
        failure={'status':'failed','code':getattr(exc,'code',type(exc).__name__)}
        print(json.dumps(failure),flush=True)
        return 2


if __name__=='__main__':
    raise SystemExit(main())
