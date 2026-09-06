"""Coherently resealed adversarial bundles must fail against external source pins."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import indicator_engine as engine
import gkg_indicator_metrics as gm
from gkg_lossless import digest
from contracts import ContractError
from test_indicators import metric, ROOT
import study_gkg_indicators as runner


def reseal(bundle, source_change=None):
    """Propagate all attacker-controlled IDs/hashes while retaining receipt pins."""
    changed={}
    for o in bundle['normalized_observations']:
        old=o['observation_id']
        if source_change: source_change(o)
        o['observation_id']=engine.observation_id(o);changed[old]=o['observation_id']
    for q in bundle['quality']:
        q['observation_id']=changed.get(q['observation_id'],q['observation_id'])
    normalized={o['observation_id']:o for o in bundle['normalized_observations']}
    for v in bundle['indicator_values']:
        o=v['observation'];old=o['observation_id']
        p=next(p for p in bundle['provenance'] if p['observation_id']==old)
        q=next(q for q in bundle['quality'] if q['observation_id']==old)
        p['source_observation_ids']=[changed.get(h,h) for h in p['source_observation_ids']]
        n=sum(normalized[h]['value'] for h in p['source_observation_ids'])
        v['sampled_numerator']=n
        v['sampled_all_accepted_prevalence']=n/v['sampled_denominator'] if v['sampled_denominator'] else None
        v['sampled_nonempty_prevalence']=n/v['nonempty_theme_denominator'] if v['nonempty_theme_denominator'] else None
        if o['value'] is not None:o['value']=v['sampled_all_accepted_prevalence']
        p['provenance_sha256']=digest({k:x for k,x in p.items() if k not in ('observation_id','provenance_sha256')})
        o['source_record_reference']='provenance:'+p['provenance_sha256']
        o['quality_note']=';'.join(q['flags']);o['observation_id']=engine.observation_id(o)
        p['observation_id']=q['observation_id']=o['observation_id']
    return bundle


class Integrity(unittest.TestCase):
    def setUp(self):
        self.metrics=[metric(themes=('PROTEST;','FOOD_SECURITY;','FOOD_SECURITY;'),bad=False)]
        self.definitions=[json.loads((ROOT/'studies/gkg-indicators-v1/definitions.json').read_text(encoding='utf-8'))[0]]
        self.history={d['indicator_id']+'@'+d['version']:digest(d) for d in self.definitions}
        self.pins={m['batch_id']:m['semantic_sha256'] for m in self.metrics}
        self.bundle=engine.build(self.metrics,self.definitions,self.history,'a'*64,'2026-09-05T00:00:01Z',windows=(15,),trusted_metric_hashes={m['batch_id']:m['semantic_sha256'] for m in self.metrics})

    def validate(self,bundle,metrics=None,definitions=None):
        return engine.validate_bundle(bundle,definitions or self.definitions,
            source_metrics=self.metrics if metrics is None else metrics, trusted_metric_hashes=self.pins,
            history=self.history, implementation_sha256='a'*64)

    def reject(self,bundle,**kwargs):
        with self.assertRaises((ContractError,gm.core.Rejection)):
            self.validate(bundle,**kwargs)

    def test_valid_authenticated_bundle(self):
        self.validate(self.bundle)

    def test_resealed_normalized_count(self):
        b=copy.deepcopy(self.bundle);o=b['normalized_observations'][0];o['value']=2;o['observation_id']=engine.observation_id(o)
        self.reject(b)

    def test_coherently_resealed_entire_chain(self):
        b=copy.deepcopy(self.bundle);receipts=copy.deepcopy(b['batch_receipts'])
        reseal(b,lambda o:o.update(value=2))
        self.assertEqual(b['batch_receipts'],receipts)
        self.assertEqual(b['indicator_values'][0]['observation']['value'],2/3)
        self.reject(b)

    def test_valid_count_from_wrong_token(self):
        b=copy.deepcopy(self.bundle)
        reseal(b,lambda o:o.update(value=self.metrics[0]['theme_counts']['FOOD_SECURITY']))
        self.reject(b)

    def test_absent_token_cannot_claim_plausible_positive(self):
        ds=copy.deepcopy(self.definitions);ds[0]['transformation']['parameters']['token']='ABSENT'
        h={d['indicator_id']+'@'+d['version']:digest(d) for d in ds}
        b=engine.build(self.metrics,ds,h,'a'*64,'2026-09-05T00:00:01Z',windows=(15,),trusted_metric_hashes={m['batch_id']:m['semantic_sha256'] for m in self.metrics})
        self.definitions=ds;self.history=h
        reseal(b,lambda o:o.update(value=1));self.reject(b)

    def test_source_metric_hash_mismatch(self):
        ms=copy.deepcopy(self.metrics);ms[0]['theme_counts']['PROTEST']=2
        self.reject(self.bundle,metrics=ms)

    def test_replaced_metric_even_with_valid_internal_hash(self):
        ms=copy.deepcopy(self.metrics)
        for entries in ms[0]['documents'].values():
            if entries[0]==['FOOD_SECURITY']:
                entries[0]=['FOOD_SECURITY','PROTEST'];break
        ms[0]['theme_counts']['PROTEST']=2;gm.seal(ms[0]);gm.validate_metric(ms[0])
        b=engine.build(ms,self.definitions,self.history,'a'*64,'2026-09-05T00:00:01Z',windows=(15,),trusted_metric_hashes={m['batch_id']:m['semantic_sha256'] for m in ms})
        self.reject(b,metrics=ms)

    def test_orphan_source_metric_evidence(self):
        self.reject(self.bundle,metrics=self.metrics+[metric('20260904001500',bad=False)])

    def test_duplicate_source_metric_evidence(self):
        self.reject(self.bundle,metrics=self.metrics*2)

    def test_missing_source_metric_evidence(self):
        self.reject(self.bundle,metrics=[])

    def test_orphan_receipt(self):
        b=copy.deepcopy(self.bundle);r=copy.deepcopy(b['batch_receipts'][0]);r['extra']='orphan'
        r['receipt_sha256']=digest({k:v for k,v in r.items() if k!='receipt_sha256'});b['batch_receipts'].append(r)
        self.reject(b)

    def test_duplicate_diagnostic_must_match_source(self):
        b=copy.deepcopy(self.bundle);q=b['quality'][-1];q['duplicate_diagnostic']['distinct_identifiers']=2
        self.reject(b)

    def test_source_quality_flags_and_identity(self):
        b=copy.deepcopy(self.bundle);o=b['normalized_observations'][0];o['source_id']='unrelated-source'
        reseal(b);self.reject(b)

    def test_definition_policy_resealed(self):
        ds=copy.deepcopy(self.definitions);ds[0]['denominator']='nonempty rows'
        b=copy.deepcopy(self.bundle)
        b['indicator_values'][0]['definition_sha256']=digest(ds[0]);b['provenance'][0]['definition_sha256']=digest(ds[0])
        reseal(b);self.reject(b,definitions=ds)

    def test_duplicate_definition_input(self):
        self.reject(self.bundle,definitions=self.definitions*2)

    def test_downstream_only_coherent_value_change(self):
        b=copy.deepcopy(self.bundle);v=b['indicator_values'][0];o=v['observation'];old=o['observation_id']
        v.update(sampled_numerator=2,sampled_all_accepted_prevalence=2/3,sampled_nonempty_prevalence=2/3)
        o['value']=2/3;o['observation_id']=engine.observation_id(o)
        for records in (b['quality'],b['provenance']):
            for r in records:
                if r['observation_id']==old:r['observation_id']=o['observation_id']
        self.reject(b)

    def test_receipt_source_hash_is_not_its_own_trust_anchor(self):
        b=copy.deepcopy(self.bundle);r=b['batch_receipts'][0];r['source_metric_sha256']='b'*64
        r['receipt_sha256']=digest({k:v for k,v in r.items() if k!='receipt_sha256'})
        self.reject(b)

    def test_unsupported_policy_even_with_explicit_definition_pin(self):
        ds=copy.deepcopy(self.definitions);ds[0]['denominator']='nonempty rows'
        self.history={d['indicator_id']+'@'+d['version']:digest(d) for d in ds}
        b=copy.deepcopy(self.bundle)
        b['indicator_values'][0]['definition_sha256']=digest(ds[0]);b['provenance'][0]['definition_sha256']=digest(ds[0])
        reseal(b);self.reject(b,definitions=ds)

    def test_source_quality_flag_removed_and_resealed(self):
        self.metrics=[metric()];self.pins={m['batch_id']:m['semantic_sha256'] for m in self.metrics}
        b=engine.build(self.metrics,self.definitions,self.history,'a'*64,'2026-09-05T00:00:01Z',windows=(15,),trusted_metric_hashes=self.pins)
        q=b['quality'][0];q['flags']=[]
        o=b['normalized_observations'][0];o['quality_status']='valid';o['quality_note']='verified source row count'
        reseal(b);self.reject(b)

    def test_wrong_implementation_pin(self):
        with self.assertRaises(ContractError):
            engine.validate_bundle(self.bundle,self.definitions,source_metrics=self.metrics,
                trusted_metric_hashes=self.pins,history=self.history,implementation_sha256='b'*64)

    def test_import_requires_authenticated_context(self):
        with self.assertRaises(TypeError):engine.validate_bundle(self.bundle,self.definitions)

    def test_normalized_token_label_swap(self):
        b=copy.deepcopy(self.bundle)
        def change(o):
            o['metric_id']='gkg.literal_token_row_count:FOOD_SECURITY'
            o['source_record_reference']=o['source_record_reference'].replace('#V1THEMES:PROTEST','#V1THEMES:FOOD_SECURITY')
            o['value']=2
        reseal(b,change);self.reject(b)

    def test_mismatched_provenance_definition_id(self):
        b=copy.deepcopy(self.bundle);b['provenance'][0]['indicator_id']='some.other.indicator'
        reseal(b);self.reject(b)

    def test_metric_evidence_order_is_irrelevant(self):
        ms=self.metrics+[metric('20260904001500')];pins={m['batch_id']:m['semantic_sha256'] for m in ms}
        b=engine.build(ms,self.definitions,self.history,'a'*64,'2026-09-05T00:00:01Z',windows=(60,),trusted_metric_hashes=pins)
        engine.validate_bundle(b,self.definitions,source_metrics=list(reversed(ms)),trusted_metric_hashes=pins,
                               history=self.history,implementation_sha256='a'*64)

    def test_known_available_batch_cannot_be_labeled_missing(self):
        # Build a legitimate out-of-window observation, then ask the validator to
        # treat it as in-window availability by changing the trusted context is
        # prohibited: its source hash/batch identity would change. The concrete
        # attack below omits an available second batch from the aggregate only.
        ms=self.metrics+[metric('20260904001500')];pins={m['batch_id']:m['semantic_sha256'] for m in ms}
        full=engine.build(ms,self.definitions,self.history,'a'*64,'2026-09-05T00:00:01Z',windows=(60,),trusted_metric_hashes=pins)
        partial=engine.build(ms[:1],self.definitions,self.history,'a'*64,'2026-09-05T00:00:01Z',windows=(60,),trusted_metric_hashes={ms[0]['batch_id']:ms[0]['semantic_sha256']})
        full['indicator_values']=partial['indicator_values'];full['provenance']=partial['provenance']
        full['quality']=[q for q in full['quality'] if q['layer']=='source_metric']+[q for q in partial['quality'] if q['layer']=='indicator']
        with self.assertRaises(ContractError):
            engine.validate_bundle(full,self.definitions,source_metrics=ms,trusted_metric_hashes=pins,history=self.history,implementation_sha256='a'*64)

    def test_manifest_resealed_artifacts_rejected_by_external_roots(self):
        with tempfile.TemporaryDirectory() as td:
            roots=[Path(td)/'a',Path(td)/'b'];pins=[]
            for r in roots:
                r.mkdir();runner.write(r/'x.json',{'claim':1});runner.write(r/'execution.json',{'status':'passed'})
                files={'x.json':gm.core.sha((r/'x.json').read_bytes())}
                manifest={'files':files,'semantic_sha256':digest(files)}
                runner.write(r/'semantic-manifest.json',manifest);pins.append(digest(manifest))
            self.assertEqual(runner.compare_runs(*roots,trusted_manifest_hashes=pins)['status'],'passed')
            for r in roots:
                (r/'x.json').write_bytes(gm.core.canonical({'claim':2}))
                files={'x.json':gm.core.sha((r/'x.json').read_bytes())}
                (r/'semantic-manifest.json').write_bytes(gm.core.canonical({'files':files,'semantic_sha256':digest(files)}))
            with self.assertRaises(ContractError):runner.compare_runs(*roots,trusted_manifest_hashes=pins)

    def test_manifest_removed_artifact_cannot_redefine_coverage(self):
        with tempfile.TemporaryDirectory() as td:
            roots=[Path(td)/'a',Path(td)/'b'];pins=[]
            for r in roots:
                r.mkdir();runner.write(r/'x.json',{'claim':1});runner.write(r/'execution.json',{'status':'passed'})
                files={'x.json':gm.core.sha((r/'x.json').read_bytes())}
                manifest={'files':files,'semantic_sha256':digest(files)}
                runner.write(r/'semantic-manifest.json',manifest);pins.append(digest(manifest))
            # Only temporary fixtures are removed; research evidence is read-only.
            for r in roots:
                (r/'x.json').unlink();(r/'semantic-manifest.json').write_bytes(gm.core.canonical({'files':{},'semantic_sha256':digest({})}))
            with self.assertRaises(ContractError):runner.compare_runs(*roots,trusted_manifest_hashes=pins)
