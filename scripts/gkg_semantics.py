"""Phase 5 deterministic contracts. No network or model calls in this module."""
from collections import Counter, defaultdict
from datetime import datetime
import hashlib
import json
import re
from urllib.parse import urlsplit

VERSION = '1.0.0'
TOKENS = ('PROTEST', 'FOOD_SECURITY', 'WB_2747_UNEMPLOYMENT')
LABELS = ('direct_topic_match', 'contextual_topic_match', 'incidental_or_weak_match',
          'semantic_mismatch', 'ambiguous', 'insufficient_context', 'document_unavailable')
SEMANTIC = LABELS[:5]
CATEGORIES = ('authoritative_provider_statement', 'empirical_repository_observation',
              'engineering_inference', 'unresolved')
ANNOTATION_KEYS = {'case_id','token','batch_id','year','cohort','source_reference',
    'DocumentIdentifier','title','evidence_locator','content_sha256','evidence_sha256',
    'label','reviewer_type','reviewer_id','reviewed_at','protocol_version','confidence','reason_code'}
REASONS = {'direct_topic_match': {'explicit_topic_reference'},
    'contextual_topic_match': {'meaningful_context'},
    'incidental_or_weak_match': {'passing_reference'},
    'semantic_mismatch': {'lexical_collision','different_subject'},
    'ambiguous': {'competing_readings'}, 'insufficient_context': {'missing_context'},
    'document_unavailable': {'retrieval_failed'}}

class Invalid(ValueError):
    pass

def require(condition, code):
    if not condition:
        raise Invalid(code)

def canonical(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')

def sha(blob):
    return hashlib.sha256(blob).hexdigest()

def digest(value):
    return sha(canonical(value))

def authenticate(value, trusted_hash, kind):
    require(isinstance(trusted_hash,str) and bool(re.fullmatch('[a-f0-9]{64}',trusted_hash)), kind+'_missing_trust')
    require(digest(value)==trusted_hash,kind+'_trust_mismatch')
    return value

def validate_protocol(p, *, trusted_hash):
    authenticate(p,trusted_hash,'protocol')
    require(p['schema_version']==VERSION and p['protocol_version']==VERSION,'protocol_version')
    require(p['token_order']==list(TOKENS) and set(p['tokens'])==set(TOKENS),'token_panel')
    require(p['sampling']['replacement_policy']=='never','replacement_policy')
    require(p['sampling']['recall']=='recall_not_estimated','positive_only_recall')
    require(sum(sum(v.values()) for v in p['sampling']['allocations'].values())<=120,'sample_cap')
    require(set(p['labels'])==set(LABELS),'label_set')
    return p

def public_reference(url):
    try:
        u=urlsplit(url)
        return u.scheme in ('http','https') and bool(u.hostname) and not u.username and not u.password and u.port in (None,80,443)
    except ValueError:
        return False

def select_sample(candidates,p,*,protocol_hash):
    validate_protocol(p,trusted_hash=protocol_hash)
    require(len({c['row_id'] for c in candidates})==len(candidates),'duplicate_candidate_row')
    require(all(c['year']==int(c['batch_id'][:4]) and c['cohort'] in p['sampling']['allocations']['PROTEST'] for c in candidates),'candidate_cohort')
    selected=[]; used=set(); populations=[]
    for token in p['token_order']:
        # Canonical occurrence before selection prevents repeated references improving rank.
        unique={}
        eligible=[c for c in candidates if token in c['tokens'] and public_reference(c['DocumentIdentifier'])]
        for c in sorted(eligible,key=lambda c:(c['batch_id'],c['line'],c['row_id'])):
            unique.setdefault(c['DocumentIdentifier'],c)
        for cohort,allocation in sorted(p['sampling']['allocations'][token].items()):
            population=[c for c in unique.values() if c['cohort']==cohort]
            available=[c for c in population if c['DocumentIdentifier'] not in used]
            def rank(c):
                return digest([p['sampling']['seed'],token,cohort,c['DocumentIdentifier'],c['row_id']])
            ranked=sorted(available,key=lambda c:(rank(c),c['row_id']))
            chosen=[]
            if allocation and ranked:
                chosen.append(min(ranked,key=lambda c:(c['theme_count'],rank(c))))
            if allocation>1 and len(ranked)>1:
                chosen.append(min((c for c in ranked if c not in chosen),key=lambda c:(-c['theme_count'],rank(c))))
            chosen.extend([c for c in ranked if c not in chosen][:max(0,allocation-len(chosen))])
            populations.append({'token':token,'cohort':cohort,'year':2026 if cohort=='recent' else int(cohort[-4:]),
                'eligible_rows':sum(c['cohort']==cohort for c in eligible),'unique_references':len(population),
                'excluded_prior_panel_duplicates':len(population)-len(available),'allocated':allocation,
                'selected':len(chosen),'unfilled':allocation-len(chosen),
                'absent_token_not_negative':not population})
            for i,c in enumerate(chosen):
                case={k:v for k,v in c.items() if k!='tokens'}
                case.update(token=token,selection_rank=rank(c),selection_role=('low_theme_count_edge' if i==0 else 'high_theme_count_edge' if i==1 else 'seeded_rank'))
                case['case_id']=digest(case)
                selected.append(case);used.add(c['DocumentIdentifier'])
    return {'schema_version':VERSION,'protocol_sha256':protocol_hash,'candidate_sha256':digest(sorted(candidates,key=lambda c:c['row_id'])),
        'candidate_count':len(candidates),'excluded_non_http_rows':sum(not public_reference(c['DocumentIdentifier']) for c in candidates),
        'algorithm':p['sampling']['algorithm'],'populations':populations,'cases':selected,'replacements':[],
        'recall':'recall_not_estimated'}

def validate_sample(sample,p,*,protocol_hash,sample_hash,candidates=None):
    validate_protocol(p,trusted_hash=protocol_hash)
    authenticate(sample,sample_hash,'sample')
    require(sample['protocol_sha256']==protocol_hash and sample['replacements']==[],'sample_protocol_or_replacement')
    require(sample['recall']=='recall_not_estimated','positive_only_recall')
    cases=sample['cases']
    require(len(cases)<=120 and len({c['case_id'] for c in cases})==len(cases),'sample_ids')
    require(len({c['DocumentIdentifier'] for c in cases})==len(cases),'duplicate_reference')
    for c in cases:
        require(c['case_id']==digest({k:v for k,v in c.items() if k!='case_id'}),'case_identity')
        require(c['token'] in TOKENS and c['year']==int(c['batch_id'][:4]),'case_year_token')
    for cell in sample['populations']:
        require(cell['allocated']==p['sampling']['allocations'][cell['token']][cell['cohort']],'cohort_allocation')
        require(cell['selected']==sum(c['token']==cell['token'] and c['cohort']==cell['cohort'] for c in cases),'cohort_count')
        require(cell['selected']+cell['unfilled']==cell['allocated'],'cohort_shortfall')
    if candidates is not None:
        require(sample==select_sample(candidates,p,protocol_hash=protocol_hash),'selection_replay')
    return sample

def context_hash(e):
    return digest({k:e[k] for k in ('title','excerpt','locator','extractor_version','context_level','manual_context_required')})

def cache_key(*,content_hash,context_hash,token,protocol_hash,model,prompt_hash,settings):
    return digest([content_hash,context_hash,token,protocol_hash,model,prompt_hash,settings])

def validate_cache(record,*,trusted_hash,expected_key):
    authenticate(record,trusted_hash,'review_cache')
    require(record['cache_key']==expected_key,'stale_review_cache')
    return record

def validate_evidence(records,sample,*,trusted_hashes,protocol_hash):
    cases={c['case_id']:c for c in sample['cases']}
    require(len(records)==len(cases) and len({e['case_id'] for e in records})==len(records),'evidence_cardinality')
    require(set(trusted_hashes)==set(cases),'evidence_trust_set')
    for e in records:
        require(e['case_id'] in cases,'orphan_evidence')
        authenticate(e,trusted_hashes[e['case_id']],'evidence')
        c=cases[e['case_id']]
        require(e['original_url']==c['DocumentIdentifier'] and e['protocol_sha256']==protocol_hash,'evidence_source_binding')
        require(e['context_sha256']==context_hash(e),'context_hash')
        require(e['availability'] in ('retrieved_context','insufficient_context','document_unavailable'),'availability')
        require(len(e['excerpt'].split())+len(e['title'].split())<=25,'excerpt_word_bound')
        require(e['attempts']==1,'retrieval_attempts')
        datetime.fromisoformat(e['retrieved_at'].replace('Z','+00:00'))
        if e['content_sha256'] is not None:
            require(bool(re.fullmatch('[a-f0-9]{64}',e['content_sha256'])) and e['download_bytes']>0,'content_hash')
        if e['availability']=='retrieved_context':
            require(e['http_status']==200 and e['content_sha256'] and e['excerpt'] and not e['manual_context_required'] and not e['identity_review_required'],'reviewability')
        if e['identity_review_required']:
            require(e['availability']!='retrieved_context','replacement_article')
    return records

def validate_annotations(annotations,sample,evidence,reviewers,p,*,reviewer_hash):
    authenticate(reviewers,reviewer_hash,'reviewer_registry')
    require(len({r['reviewer_id'] for r in reviewers})==len(reviewers),'duplicate_reviewer')
    registry={r['reviewer_id']:r for r in reviewers}
    for r in reviewers:
        require(r['reviewer_type'] in ('human','llm','machine') and r['reviewer_id'],'reviewer_identity')
        if r['reviewer_type']=='llm':
            require(all(r.get(k) for k in ('model_version','prompt_sha256','protocol_sha256')) and isinstance(r.get('settings'),dict),'llm_review_configuration')
            require(r['protocol_sha256']==digest(p),'llm_registry_protocol')
        if r['reviewer_type']=='human':
            require(r.get('human_attestation_reference') and r.get('independence_group'),'human_attestation')
    cases={c['case_id']:c for c in sample['cases']}; es={e['case_id']:e for e in evidence}; seen=set()
    for a in annotations:
        require(set(a)==ANNOTATION_KEYS,'annotation_schema')
        require(a['case_id'] in cases and a['reviewer_id'] in registry,'annotation_reference')
        c,e,r=cases[a['case_id']],es[a['case_id']],registry[a['reviewer_id']]
        key=(a['case_id'],a['reviewer_id']);require(key not in seen,'duplicate_annotation');seen.add(key)
        require(a['reviewer_type']==r['reviewer_type'],'reviewer_type')
        require(a['label'] in LABELS,'annotation_label')
        require(a['reason_code'] in REASONS[a['label']],'reason_label_binding')
        require(a['confidence'] in p['review']['confidence'],'confidence')
        require(a['protocol_version']==p['protocol_version'],'annotation_protocol')
        stamp=datetime.fromisoformat(a['reviewed_at'].replace('Z','+00:00'));require(stamp.tzinfo is not None,'review_time_zone')
        for k in ('token','batch_id','year','cohort','DocumentIdentifier','source_reference'):
            require(a[k]==c[k],'annotation_source_binding')
        require(a['content_sha256']==e['content_sha256'] and a['evidence_sha256']==digest(e) and a['title']==e['title'] and a['evidence_locator']==e['locator'],'annotation_evidence_binding')
        if e['availability']=='document_unavailable':
            require(a['label']=='document_unavailable','unavailable_label')
        if e['availability']=='insufficient_context':
            require(a['label']=='insufficient_context','insufficient_label')
        if a['reviewer_type']=='machine':
            require(a['label'] in LABELS[5:],'machine_semantic_judgment')
    # Exact duplicate bodies cannot carry contradictory labels from one reviewer for the same concept.
    duplicate_labels={}
    for a in annotations:
        e=es[a['case_id']]
        key=(a['reviewer_id'],a['token'],content_identity(e))
        require(key not in duplicate_labels or duplicate_labels[key]==a['label'],'duplicate_content_label_conflict')
        duplicate_labels[key]=a['label']
    return annotations

def validate_taxonomy(findings,*,trusted_hash):
    authenticate(findings,trusted_hash,'taxonomy')
    require(len({f['id'] for f in findings})==len(findings),'taxonomy_duplicate')
    for f in findings:
        require(f['category'] in CATEGORIES,'taxonomy_category')
        require(f['claim'] and f['limitations'],'taxonomy_scope')
        if f['category']=='authoritative_provider_statement':
            require(f.get('url','').startswith(('https://blog.gdeltproject.org/','https://data.gdeltproject.org/')) and re.fullmatch('[a-f0-9]{64}',f.get('source_sha256','')),'taxonomy_provider_source')
        if f.get('proves_historical_stability'):
            require(f['category']=='authoritative_provider_statement' and f.get('version_interval_evidence'),'taxonomy_stability_overclaim')
    return findings

def content_identity(e):
    return (e['content_sha256'] if e.get('source_hash_scope')=='complete_response_body' else None) or e['case_id']

def unique_cases(cases,evidence):
    es={e['case_id']:e for e in evidence}; seen=set(); result=[]
    for c in sorted(cases,key=lambda x:x['case_id']):
        e=es[c['case_id']]
        # Only exact source-content duplicates. Error pages never supply reviewed counts.
        key=content_identity(e)
        if key not in seen:
            result.append(c);seen.add(key)
    return result

def summary(cases,evidence,annotations,reviewer_id=None):
    es={e['case_id']:e for e in evidence}; selected=len(cases)
    raw=Counter(es[c['case_id']]['availability'] for c in cases)
    unique=unique_cases(cases,evidence); ids={c['case_id'] for c in unique}
    scope={c['case_id']:c for c in cases}
    canonical_groups={(c['token'],content_identity(es[c['case_id']])) for c in unique}
    grouped_labels={}
    for a in annotations:
        if a['case_id'] in scope and a['reviewer_id']==reviewer_id:
            key=(a['token'],content_identity(es[a['case_id']]))
            if key in canonical_groups:
                require(key not in grouped_labels or grouped_labels[key]==a['label'],'duplicate_content_label_conflict')
                grouped_labels[key]=a['label']
    labels=Counter(grouped_labels.values())
    n=sum(labels[x] for x in SEMANTIC)
    reviewable=sum(es[c['case_id']]['availability']=='retrieved_context' for c in unique)
    def rate(n,d):return n/d if d else None
    rates={}
    for name,count in [('direct',labels['direct_topic_match']),('direct_plus_contextual',labels['direct_topic_match']+labels['contextual_topic_match']),('mismatch',labels['semantic_mismatch']),('ambiguity',labels['ambiguous'])]:
        rates[name]={'among_semantically_reviewed':rate(count,n),'among_unique_reviewable':rate(count,reviewable) if n else None,'among_selected':rate(count,selected) if n else None}
    return {'selected':selected,'unique_content_or_reference':len(unique),'duplicate_content_excess':selected-len(unique),
        'retrieved_context_raw':raw['retrieved_context'],'reviewable_unique':reviewable,'unavailable':raw['document_unavailable'],
        'insufficient_context':raw['insufficient_context'],'unavailable_rate_selected':rate(raw['document_unavailable'],selected),
        'semantic_reviewed':n,'reviewer_id':reviewer_id,'label_counts':dict(labels),'sampled_positive_semantic_match_rates':rates}

def agreement(cases,evidence,annotations,reviewers):
    humans=[r for r in reviewers if r['reviewer_type']=='human']; pairs=[]
    unique=unique_cases(cases,evidence); bycase={c['case_id']:c for c in unique}
    es={e['case_id']:e for e in evidence}
    scope={c['case_id']:c for c in cases}
    index={}
    for a in annotations:
        if a['case_id'] in scope:
            key=(a['token'],content_identity(es[a['case_id']]),a['reviewer_id'])
            require(key not in index or index[key]==a['label'],'duplicate_content_label_conflict')
            index[key]=a['label']
    for i,r in enumerate(humans):
        for s in humans[i+1:]:
            if r['independence_group']==s['independence_group']:continue
            values=[]
            for cid,c in bycase.items():
                key=(c['token'],content_identity(es[cid]))
                a,b=index.get((*key,r['reviewer_id'])),index.get((*key,s['reviewer_id']))
                if a in SEMANTIC and b in SEMANTIC: values.append((c,a,b))
            def counts(rows):
                matrix=Counter((a,b) for _,a,b in rows)
                return {'paired':len(rows),'raw_agreement':sum(a==b for _,a,b in rows)/len(rows) if rows else None,
                    'confusion_matrix':[{'a':a,'b':b,'count':n} for (a,b),n in sorted(matrix.items())]}
            pairs.append({'reviewers':[r['reviewer_id'],s['reviewer_id']],**counts(values),
                'by_token':{t:counts([v for v in values if v[0]['token']==t]) for t in sorted({c['token'] for c in cases})},
                'by_year':{str(y):counts([v for v in values if v[0]['year']==y]) for y in sorted({c['year'] for c in cases})}})
    return {'status':'estimated' if any(p['paired'] for p in pairs) else 'not_estimated',
        'reason':None if any(p['paired'] for p in pairs) else 'fewer_than_two_independent_human_reviews_on_shared_reviewable_cases',
        'pairs':pairs,'excluded_labels':list(LABELS[5:]),'kappa':'not_estimated; bounded descriptive audit'}

def packet(sample,evidence,p):
    es={e['case_id']:e for e in evidence}
    return [{'case_id':c['case_id'],'source':c['source_name'],'year':c['year'],'token':c['token'],
        'concept':p['tokens'][c['token']]['concept'],'url':c['DocumentIdentifier'],
        'title':es[c['case_id']]['title'],'excerpt':es[c['case_id']]['excerpt'],
        'availability':es[c['case_id']]['availability'],'label_choices':list(LABELS),
        'label':None,'reviewer_id':None,'blinded':False} for c in sample['cases']]

def assess(sample,p,evidence,annotations,reviewers,taxonomy,*,trust):
    """Only public assessment entry point: all upstream evidence externally pinned."""
    validate_sample(sample,p,protocol_hash=trust['protocol'],sample_hash=trust['sample'])
    validate_evidence(evidence,sample,trusted_hashes=trust['receipts'],protocol_hash=trust['protocol'])
    validate_annotations(annotations,sample,evidence,reviewers,p,reviewer_hash=trust['reviewers'])
    authenticate(annotations,trust['annotations'],'annotations')
    validate_taxonomy(taxonomy,trusted_hash=trust['taxonomy'])
    humans=[r for r in reviewers if r['reviewer_type']=='human']
    results=[]
    for token in TOKENS:
        cases=[c for c in sample['cases'] if c['token']==token]
        totals=summary(cases,evidence,annotations)
        years=required_years(sample,p,token)
        yearly={str(y):summary([c for c in cases if c['year']==y],evidence,annotations) for y in years}
        perhuman={r['reviewer_id']:summary(cases,evidence,annotations,r['reviewer_id']) for r in humans}
        peryearhuman={r['reviewer_id']:{str(y):summary([c for c in cases if c['year']==y],evidence,annotations,r['reviewer_id']) for y in years} for r in humans}
        ag=agreement(cases,evidence,annotations,reviewers)
        availability=bool(cases) and totals['reviewable_unique']/len(cases)>=p['gates']['availability']['min_pooled_reviewable_fraction'] and all(s['reviewable_unique']>=p['gates']['availability']['min_reviewable_per_eligible_year'] for s in yearly.values())
        documentation=any(f['category']=='authoritative_provider_statement' and token in f.get('supports_topic',[]) for f in taxonomy)
        taxonomy_pass=any(f.get('proves_historical_stability') and token in f.get('tokens',[]) for f in taxonomy)
        segmentation=any(f['category']=='authoritative_provider_statement' and token in f.get('invalidating_dated_change',[]) for f in taxonomy)
        uncertainty=not any(f['category']=='unresolved' and token in f.get('tokens',[]) and f.get('material',True) for f in taxonomy)
        pairs=[a for a in ag['pairs'] if a['paired']>=p['gates']['reviewer_quality']['min_paired']]
        reviewer_pass=bool(pairs) and all(a['raw_agreement']>=p['gates']['reviewer_quality']['min_agreement'] for a in pairs)
        eligible=[]
        for r in humans:
            rid=r['reviewer_id'];s=perhuman[rid];ys=peryearhuman[rid]
            if s['semantic_reviewed']>=p['gates']['positive_consistency']['min_reviewed_per_human'] and all(v['semantic_reviewed']>=p['gates']['cross_year']['min_reviewed_per_eligible_year_per_human'] for v in ys.values()):eligible.append(rid)
        positive={rid:(perhuman[rid]['sampled_positive_semantic_match_rates']['direct_plus_contextual']['among_semantically_reviewed']>=p['gates']['positive_consistency']['direct_plus_contextual_min'] and perhuman[rid]['sampled_positive_semantic_match_rates']['mismatch']['among_semantically_reviewed']<=p['gates']['positive_consistency']['mismatch_max']) for rid in eligible}
        cross={rid:max(v['sampled_positive_semantic_match_rates']['direct_plus_contextual']['among_semantically_reviewed'] for v in peryearhuman[rid].values())-min(v['sampled_positive_semantic_match_rates']['direct_plus_contextual']['among_semantically_reviewed'] for v in peryearhuman[rid].values())<=p['gates']['cross_year']['max_year_match_rate_spread'] for rid in eligible}
        # Require every sufficiently reviewed independent human, not a cherry-picked favorable pair.
        enough=len({r['independence_group'] for r in humans if r['reviewer_id'] in eligible})>=2
        gates={'documentation':'pass' if documentation else 'unresolved','positive_consistency':('pass' if all(positive.values()) else 'fail') if enough else 'pending_human_review',
            'cross_year':('pass' if all(cross.values()) else 'fail') if enough else 'pending_human_review',
            'availability':'pass' if availability else 'fail','taxonomy_stability':'pass' if taxonomy_pass else 'requires_segmentation' if segmentation else 'unresolved',
            'auditability':'pass','reviewer_quality':'pass' if reviewer_pass else 'pending_human_review' if not pairs else 'fail',
            'uncertainty':'pass' if uncertainty else 'unresolved'}
        if all(v=='pass' for v in gates.values()):decision='historically_usable_experimental'
        elif segmentation:decision='requires_version_segmentation'
        elif enough and positive and not any(positive.values()) and availability:decision='reject_for_historical_indicator_use'
        else:decision='continue_semantic_validation'
        results.append({'token':token,'decision':decision,'gates':gates,'totals':totals,'by_year':yearly,
            'by_human_reviewer':perhuman,'by_human_reviewer_year':peryearhuman,'agreement':ag,
            'semantic_status':'human_validation_not_completed' if not enough else 'bounded_human_sample',
            'unobserved_years':[y for y in (2015,2016,2020,2023,2025,2026) if y not in years],
            'absence_interpretation':'unobserved tagged-year is not a semantic negative','recall':'recall_not_estimated'})
    return {'schema_version':VERSION,'protocol_sha256':trust['protocol'],'sample_sha256':trust['sample'],
        'tokens':results,'recommendation':'promote_selected_tokens_to_history_pilot' if any(t['decision']=='historically_usable_experimental' for t in results) else 'continue_semantic_validation',
        'agreement':agreement(sample['cases'],evidence,annotations,reviewers),'recall':'recall_not_estimated',
        'human_validation':'human_validation_not_completed' if any(t['semantic_status']=='human_validation_not_completed' for t in results) else 'completed_bounded_review'}


def required_years(sample,p,token):
    # Allocated strata cannot disappear from gates because all references collided or failed.
    return sorted({cell['year'] for cell in sample['populations']
        if cell['token']==token and p['sampling']['allocations'][token][cell['cohort']]>0})

def validate_packet(candidate,sample,evidence,p):
    require(candidate==packet(sample,evidence,p),'packet_derivation_or_blinding')
    return candidate
