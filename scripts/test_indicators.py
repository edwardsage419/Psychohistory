"""Offline synthetic fixtures exercise measurement rules, never call GDELT."""
import copy
from datetime import timedelta
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import gkg_lossless as core
import gkg_indicator_metrics as gm
from contracts import ContractError, validate_contract
import indicator_definitions as defs
import indicator_engine as engine
import study_gkg_indicators as runner

ROOT = Path(__file__).resolve().parents[1]
# Frozen initial release pins: additions allowed, existing version identities cannot change.
INITIAL_HISTORY = {'gkg.media_prevalence.protest@0.1.0': 'e22d1a2cdb2d50fbcd84b3e9d34a1964bf75710f56df34eb8431c241f825a8e0', 'gkg.media_prevalence.econ_taxation@0.1.0': '75993ceb6e7aa948c658a47ca8e303501f85dd9a2bd9c54c73b9e77cdaf8a161', 'gkg.media_prevalence.food_security@0.1.0': '8734cf10b82659340f99ea84801efa39b2040ead1cd5dc87480f063dece9f068', 'gkg.media_prevalence.wb_345_sovereign_wealth_funds@0.1.0': '1e7bc65191b3204032c2bdce51049442e6818125fb533fd309896b4460075d2d', 'gkg.media_prevalence.wb_2747_unemployment@0.1.0': '970cd8ced614e6cb7d2cc956ab846dfb3e5cb8d9eba81bdb84f362dc57a0b84d', 'gkg.media_prevalence.natural_disaster_landslide@0.1.0': 'c1c80727777aa991d7b059d7761466b9a3e076b32e05e289840325341f129b39', 'gkg.media_prevalence.aviation_incident@0.1.0': '34262755b6f73798d1e98617957140d612b1ef9f8c31225ee1093e1905e83436'}


def fixture(batch='20260904000000', themes=('PROTEST;PROTEST;',''), bad=True, identifiers=None):
    rows=[]
    for i,t in enumerate(themes):
        f=['']*27
        f[0]=batch+'-'+str(i); f[1]=batch; f[2]='1'; f[3]='example.test'
        f[4]=identifiers[i] if identifiers is not None else 'https://example.test/'+batch+'/'+str(i)
        f[7]=t; f[8]='WRONG_V2_FIELD,7;'
        rows.append(('\t'.join(f)+'\n').encode())
    if bad:
        f=['']*27;f[0]=batch+'-bad';f[1]=batch;f[7]='PROTEST';f[26]='bad'
        rows.append(('\t'.join(f)+'\n').encode().replace(b'bad\n',b'\xff\n'))
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr(batch+'.gkg.csv',b''.join(rows))
    blob=stream.getvalue()
    source={'source_id':'gdelt-gkg-2.1','batch_id':batch,'source_url':'https://data.gdeltproject.org/gdeltv2/'+batch+'.gkg.csv.zip',
            'archive_sha256':core.sha(blob),'archive_bytes':len(blob),'acquisition':'passed'}
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'source.zip';p.write_bytes(blob);ledger=core.ingest(p,source)
    acquisition={**source,'started_at':'2026-09-05T00:00:00Z','finished_at':'2026-09-05T00:00:01Z',
                 'parser_version':'1.0.0','contract_version':'1.0.0','transport':{'status':200}}
    published={'semantic_sha256':ledger['semantic_sha256'],'row_ledger_sha256':core.digest(ledger['rows'])}
    return blob,ledger,acquisition,published


def metric(*args,**kwargs):
    return gm.extract(*fixture(*args,**kwargs))


class Indicators(unittest.TestCase):
    def setUp(self):
        self.definition=json.loads((ROOT/'studies/gkg-indicators-v1/definitions.json').read_text(encoding='utf-8'))[0]
        self.m=metric()

    def run_engine(self,metrics=None,definition=None,**kwargs):
        d=definition or self.definition
        return engine.build(metrics if metrics is not None else [self.m],[d],{d['indicator_id']+'@'+d['version']:core.digest(d)},
            'a'*64,'2026-09-05T00:00:01Z',**kwargs)

    def test_exact_token_presence_and_quarantine(self):
        self.assertEqual(self.m['theme_counts'],{'PROTEST':1})
        self.assertEqual((self.m['accepted_rows'],self.m['quarantined_rows'],self.m['empty_theme_rows']),(2,1,1))
        self.assertEqual(self.m['within_row_repeated_tokens'],1)

    def test_no_case_alias_substring_or_whitespace_repair(self):
        m=metric(themes=('PROTESTER;protest; PROTEST;','PROTEST'),bad=False)
        self.assertEqual(m['theme_counts'],{' PROTEST':1,'PROTEST':1,'PROTESTER':1,'protest':1})

    def test_integrity_failure(self):
        b,l,a,p=fixture()
        with self.assertRaises(core.Rejection):gm.extract(b+b'x',l,a,p)

    def test_ledger_tampering(self):
        b,l,a,p=fixture(); l['rows'][0]['start']=1;core.seal(l)
        with self.assertRaises(core.Rejection):gm.extract(b,l,a,p)

    def test_resealed_disposition_not_authoritative(self):
        b,l,a,p=fixture(); l['rows'][0]['fields_sha256']='a'*64;core.seal(l)
        p={'semantic_sha256':l['semantic_sha256'],'row_ledger_sha256':core.digest(l['rows'])}
        with self.assertRaises(core.Rejection):gm.extract(b,l,a,p)

    def test_acquisition_source_mismatch(self):
        b,l,a,p=fixture();a['archive_bytes']+=1
        with self.assertRaises(core.Rejection):gm.extract(b,l,a,p)

    def test_rejected_batch_fails_closed(self):
        b,l,a,p=fixture(themes=())
        with self.assertRaises(core.Rejection):gm.extract(b,l,a,p)

    def test_all_required_definition_fields(self):
        defs.validate_definition(self.definition)
        for key in self.definition:
            with self.subTest(key=key):
                d=copy.deepcopy(self.definition);del d[key]
                with self.assertRaises(ContractError):defs.validate_definition(d)

    def test_definition_unknown_fields_status_version(self):
        for key,value in [('unknown','x'),('status','production'),('version','1'),('documentation',[])]:
            d=copy.deepcopy(self.definition);d[key]=value
            with self.assertRaises(ContractError):defs.validate_definition(d)

    def test_generic_non_gkg_definition(self):
        d=copy.deepcopy(self.definition);d.update(source_family='Climate',source_dataset='future monthly series',source_field='temperature',unit='kelvin')
        d['transformation']={'method':'monthly_mean','version':'1.0.0','parameters':{'field':'temperature'}}
        defs.validate_definition(d)
        with self.assertRaises(ContractError):defs.require_gkg_prevalence(d)

    def test_semantic_version_reuse_rejected(self):
        d=copy.deepcopy(self.definition); history={d['indicator_id']+'@'+d['version']:core.digest(d)}
        d['description']='changed meaning'
        with self.assertRaises(ContractError):defs.validate_registry([d],history)

    def test_new_version_and_append_only_history(self):
        d=copy.deepcopy(self.definition);history={d['indicator_id']+'@'+d['version']:core.digest(d)}
        d['version']='0.2.0';new={**history,d['indicator_id']+'@'+d['version']:core.digest(d)}
        defs.validate_registry([d],new,history)
        with self.assertRaises(ContractError):defs.validate_registry([d],{d['indicator_id']+'@'+d['version']:core.digest(d)},history)

    def test_duplicate_definitions(self):
        d=self.definition;h={d['indicator_id']+'@'+d['version']:core.digest(d)}
        with self.assertRaises(ContractError):defs.validate_registry([d,d],h)

    def test_unsupported_policy_not_silently_ignored(self):
        for key,value in [('denominator','nonempty rows'),('aggregation_method','mean'),('smoothing_policy','moving average')]:
            d=copy.deepcopy(self.definition);d[key]=value
            with self.assertRaises(ContractError):self.run_engine(definition=d)

    def test_partial_window_null_with_visible_counts(self):
        b=self.run_engine(windows=(60,));v=b['indicator_values'][0]
        self.assertIsNone(v['observation']['value']);self.assertEqual(v['sampled_numerator'],1)
        q=[q for q in b['quality'] if q['layer']=='indicator'][0]
        self.assertEqual(q['coverage'],.25);self.assertEqual(len(q['missing_batches']),3)
        self.assertIn('incomplete_window',q['flags'])

    def test_weighted_ratio_not_mean_of_ratios(self):
        ms=[metric('2026090400'+mm+'00',themes=t,bad=False) for mm,t in [('00',('PROTEST',)),('15',('','','')),('30',('PROTEST','')),('45',('',''))]]
        v=self.run_engine(ms,windows=(60,))['indicator_values'][0]
        self.assertEqual(v['observation']['value'],2/8)
        self.assertEqual(v['sampled_nonempty_prevalence'],1)

    def test_entirely_missing_window(self):
        b=self.run_engine([],windows=(60,),requested={60:['20150302000000']})
        self.assertIsNone(b['indicator_values'][0]['observation']['value'])
        self.assertEqual(b['quality'][0]['coverage'],0)

    def test_zero_denominator(self):
        m=copy.deepcopy(self.m)
        for key in ('accepted_rows','empty_theme_rows','nonempty_theme_rows','missing_document_rows','within_row_repeated_tokens','empty_delimiter_segments'):m[key]=0
        for key in ('theme_counts','documents','source_collection_counts','source_name_counts'):m[key]={}
        gm.seal(m)
        b=self.run_engine([m],windows=(15,));self.assertIsNone(b['indicator_values'][0]['observation']['value'])
        self.assertIn('zero_denominator',b['quality'][-1]['flags'])

    def test_absent_literal_token_is_zero(self):
        b=self.run_engine([metric(themes=('',),bad=False)],windows=(15,))
        self.assertEqual(b['indicator_values'][0]['observation']['value'],0)
        self.assertIn('historical_semantics_unvalidated',b['quality'][-1]['flags'])

    def test_quarantine_and_empty_quality_flags(self):
        q=self.run_engine(windows=(15,))['quality'][-1]
        self.assertEqual(q['quarantined_rows'],1)
        self.assertIn('quarantined_rows_excluded',q['flags'])
        self.assertIn('empty_theme_rows_in_denominator',q['flags'])

    def test_duplicate_batch_rejected(self):
        with self.assertRaises(ContractError):self.run_engine([self.m,self.m])

    def test_duplicate_archive_rejected(self):
        m=copy.deepcopy(self.m);m['batch_id']='20260904001500'
        m['provenance']['source']['batch_id']=m['batch_id'];m['provenance']['acquisition']['batch_id']=m['batch_id']
        m['provenance']['member']=m['batch_id']+'.gkg.csv'
        for k in ('source','acquisition'):m['provenance'][k]['source_url']='https://data.gdeltproject.org/gdeltv2/'+m['batch_id']+'.gkg.csv.zip'
        gm.seal(m)
        with self.assertRaises((ContractError,core.Rejection)):self.run_engine([self.m,m])

    def test_exact_identifier_repetition_diagnostic(self):
        m=metric(themes=('PROTEST','',''),bad=False,identifiers=['same','same','other'])
        d=gm.duplicate_diagnostic([m],'PROTEST')
        self.assertEqual(d['unique_identifier_prevalence'],.5)
        self.assertEqual(d['excess_identifier_rows'],1)
        b=self.run_engine([m],windows=(15,));self.assertEqual(b['indicator_values'][0]['observation']['value'],1/3)
        self.assertIn('repeated_document_identifiers',b['quality'][-1]['flags'])

    def test_repeat_across_batches(self):
        ms=[metric(b,themes=('PROTEST',),bad=False,identifiers=['same']) for b in ['20260904000000','20260904001500']]
        self.assertEqual(gm.duplicate_diagnostic(ms,'PROTEST')['excess_identifier_rows'],1)

    def test_empty_identifier_not_merged(self):
        m=metric(themes=('PROTEST',''),bad=False,identifiers=['',''])
        self.assertEqual(gm.duplicate_diagnostic([m])['distinct_identifiers'],0)
        self.assertEqual(m['missing_document_rows'],2)

    def test_midnight_halfopen_boundaries(self):
        ms=[metric(b,bad=False) for b in ['20251231234500','20260101000000']]
        vs=self.run_engine(ms,windows=(60,))['indicator_values']
        self.assertEqual([v['window_start'] for v in vs],['2025-12-31T23:00:00Z','2026-01-01T00:00:00Z'])
        self.assertTrue(all(v['sampled_denominator']==2 for v in vs))

    def test_invalid_window_and_grid(self):
        for n in [True,0,14,17,105,1500,60.0]:
            with self.subTest(n=n),self.assertRaises(ContractError):self.run_engine(windows=(n,))
        for b in ['20260904000100','20260904001501','20260230000000']:
            with self.assertRaises(ContractError):engine.utc(b)
        with self.assertRaises(ContractError):self.run_engine(windows=(60,),requested={60:['20260904001500']})

    def test_historical_fixtures_all_years(self):
        ms=[metric(str(year)+'0302000000',bad=False) for year in (2015,2016,2020,2023,2025,2026)]
        b=self.run_engine(ms,windows=(15,))
        self.assertEqual(len(b['indicator_values']),6)
        self.assertTrue(all(v['observation']['value']==.5 for v in b['indicator_values']))
        self.assertTrue(all(p['retrospective_rule'] for p in b['provenance']))

    def test_order_determinism(self):
        ms=[self.m,metric('20260904001500')]
        self.assertEqual(self.run_engine(ms),self.run_engine(list(reversed(ms))))

    def test_identity_sensitive_to_definition_version(self):
        d=copy.deepcopy(self.definition);d['version']='0.2.0'
        a=self.run_engine(windows=(15,))['indicator_values'][0]['observation']['observation_id']
        b=self.run_engine(definition=d,windows=(15,))['indicator_values'][0]['observation']['observation_id']
        self.assertNotEqual(a,b)

    def test_retrieval_clock_excluded_from_observation_identity(self):
        o=self.run_engine(windows=(15,))['indicator_values'][0]['observation']
        o['retrieved_at']='2027-01-01T00:00:00Z';validate_contract('observation',o)

    def test_provenance_links(self):
        b=self.run_engine(windows=(15,));o=b['indicator_values'][0]['observation'];p=b['provenance'][0]
        self.assertEqual(o['source_record_reference'],'provenance:'+p['provenance_sha256'])
        self.assertEqual(p['definition_sha256'],core.digest(self.definition))
        self.assertEqual(p['source_observation_ids'],[b['normalized_observations'][0]['observation_id']])
        self.assertIsNone(o['geography'])
        self.assertEqual(b['batch_receipts'][0]['source']['archive_sha256'],self.m['provenance']['source']['archive_sha256'])

    def test_malformed_counts_hash_and_document_accounting(self):
        for key,value in [('accepted_rows',True),('empty_theme_rows',9),('theme_counts',{'PROTEST':3}),('theme_counts',{'PROTEST':float('nan')}),('documents',{})]:
            m=copy.deepcopy(self.m);m[key]=value
            with self.subTest(key=key),self.assertRaises((core.Rejection,ValueError)):
                gm.seal(m);gm.validate_metric(m)
        m=copy.deepcopy(self.m);m['accepted_rows']+=1
        with self.assertRaises(core.Rejection):gm.validate_metric(m)

    def test_inventory_distribution_and_cohort_absence(self):
        ms=[metric('20150302000000',themes=('',),bad=False),self.m]
        inv=gm.inventory(ms,{m['batch_id']:m['batch_id'][:4] for m in ms},{'PROTEST':['official']})
        e=inv['entries'][0]
        self.assertEqual(e['years_present'],['2026']);self.assertEqual(e['batch_counts_in_batch_order'],[0,1])
        self.assertEqual(e['batch_prevalence_in_batch_order'],[0,.5])
        self.assertEqual(e['cohorts']['2015']['rows'],0)

    def test_zero_variance_correlation_is_null(self):
        self.assertIsNone(runner.correlation([1,1],[1,2]))
        self.assertAlmostEqual(runner.correlation([1,2,3],[3,2,1]),-1)

    def test_offline_suite_forbids_network(self):
        with patch('urllib.request.urlopen',side_effect=AssertionError('network forbidden')):
            self.run_engine(windows=(15,))


    # Dedicated adversarial review regressions: these failed on e0710fa.
    def test_review_nonempty_denominator_matches_document_rows(self):
        m=copy.deepcopy(self.m);m['empty_theme_rows']=0;m['nonempty_theme_rows']=2;gm.seal(m)
        with self.assertRaises((core.Rejection,ContractError)):gm.validate_metric(m)

    def test_review_acquisition_chronology(self):
        m=copy.deepcopy(self.m);m['provenance']['acquisition']['started_at']='2027-01-01T00:00:00Z';gm.seal(m)
        with self.assertRaises((core.Rejection,ContractError)):gm.validate_metric(m)

    def test_review_provenance_parser_contradiction(self):
        m=copy.deepcopy(self.m);m['provenance']['parser_version']='2.0.0';gm.seal(m)
        with self.assertRaises((core.Rejection,ContractError)):gm.validate_metric(m)

    def test_review_source_url_batch_contradiction(self):
        m=copy.deepcopy(self.m)
        for key in ('source','acquisition'):m['provenance'][key]['source_url']='https://data.gdeltproject.org/gdeltv2/20150302000000.gkg.csv.zip'
        gm.seal(m)
        with self.assertRaises((core.Rejection,ContractError)):gm.validate_metric(m)

    def test_review_numerator_must_match_normalized_inputs(self):
        b=self.run_engine(windows=(15,));v=b['indicator_values'][0];v['sampled_numerator']=0
        v['sampled_all_accepted_prevalence']=0;v['sampled_nonempty_prevalence']=0
        o=v['observation'];old=o['observation_id'];o['value']=0;o['observation_id']=engine.observation_id(o)
        for records in (b['quality'],b['provenance']):
            for r in records:
                if r['observation_id']==old:r['observation_id']=o['observation_id']
        with self.assertRaises(ContractError):engine.validate_bundle(b,[self.definition])

    def test_review_required_quality_flags_cannot_disappear(self):
        b=self.run_engine(windows=(15,));o=b['indicator_values'][0]['observation'];old=o['observation_id']
        q=b['quality'][-1];q['flags'].remove('quarantined_rows_excluded')
        o['quality_note']=';'.join(q['flags']);o['observation_id']=engine.observation_id(o)
        q['observation_id']=o['observation_id'];b['provenance'][0]['observation_id']=o['observation_id']
        with self.assertRaises(ContractError):engine.validate_bundle(b,[self.definition])

    def test_review_source_observation_quality_accounting(self):
        b=self.run_engine(windows=(15,));b['quality'][0]['accepted_rows']=0
        with self.assertRaises(ContractError):engine.validate_bundle(b,[self.definition])

    def test_committed_initial_history_is_append_only(self):
        initial = INITIAL_HISTORY
        history=runner.read(ROOT/'studies/gkg-indicators-v1/definition-history.json')
        definitions=runner.read(ROOT/'studies/gkg-indicators-v1/definitions.json')
        defs.validate_registry(definitions,history,initial)

    def test_bundle_tampered_hash_denominator_and_scope(self):
        for field,value in [('definition_sha256','b'*64),('sampled_denominator',99),('sampled_all_accepted_prevalence',.99)]:
            b=self.run_engine(windows=(15,));b['indicator_values'][0][field]=value
            with self.assertRaises(ContractError):engine.validate_bundle(b,[self.definition])

    def test_replay_integrity_and_alias_checks(self):
        with tempfile.TemporaryDirectory() as td:
            roots=[Path(td)/'a',Path(td)/'b']
            for r in roots:
                r.mkdir();runner.write(r/'x.json',{'stable':1});runner.write(r/'execution.json',{'status':'passed','clock':r.name})
                files={'x.json':core.sha((r/'x.json').read_bytes())}
                runner.write(r/'semantic-manifest.json',{'files':files,'semantic_sha256':core.digest(files)})
            self.assertEqual(runner.compare_runs(*roots)['status'],'passed')
            with self.assertRaises(ContractError):runner.compare_runs(roots[0],roots[0])
            (roots[1]/'x.json').write_text('{}',encoding='utf-8')
            with self.assertRaises(ContractError):runner.compare_runs(*roots)

    def test_runner_96_offline_batches_and_machine_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);raw=root/'raw';ledgers=root/'ledgers';raw.mkdir();ledgers.mkdir()
            prior=root/'studies/gkg-lossless-v1/results';prior.mkdir(parents=True)
            batches=[];published=[];acquisitions=[]
            start=engine.utc('20260904000000')
            for i in range(96):
                batch=(start+i*engine.STEP).strftime('%Y%m%d%H%M%S')
                blob,ledger,acquisition,pub=fixture(batch,themes=('PROTEST;',),bad=False)
                (raw/(acquisition['archive_sha256']+'.zip')).write_bytes(blob)
                runner.write(ledgers/(batch+'.json'),ledger)
                batches.append({'batch_id':batch,'cohort':'test','url':acquisition['source_url']})
                published.append({**pub,'source':ledger['source']});acquisitions.append(acquisition)
            manifest={'batches':batches};runner.write(root/'manifest.json',manifest)
            runner.write(prior/'study.json',{'manifest_sha256':core.digest(manifest),'batches':published})
            runner.write(prior/'provenance.json',{'batches':acquisitions});runner.write(prior/'quarantine.json',[])
            # The real corpus selection gate is independently tested; this fixture has one year.
            with patch.object(runner,'ROOT',root),patch.object(runner,'code_hashes',return_value={'fixture':'a'*64}),patch.object(runner,'evaluate',return_value=[]),patch('builtins.print'):
                self.assertTrue(runner.study(root/'manifest.json',raw,ledgers,root/'run-a'))
                self.assertTrue(runner.study(root/'manifest.json',raw,ledgers,root/'run-b',True))
                self.assertEqual(runner.compare_runs(root/'run-a',root/'run-b')['status'],'passed')
                # Corrupt only this temporary synthetic input; the retained research corpus is untouched.
                (raw/(acquisitions[0]['archive_sha256']+'.zip')).write_bytes(b'broken fixture')
                self.assertFalse(runner.study(root/'manifest.json',raw,ledgers,root/'run-c'))
                outcomes=runner.read(root/'run-c/batch-outcomes.json')
                self.assertEqual(len(outcomes),96);self.assertEqual(sum(o['status']=='failed' for o in outcomes),1)
                self.assertFalse((root/'run-c/semantic-manifest.json').exists())


if __name__=='__main__':unittest.main()
