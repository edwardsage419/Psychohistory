"""Minimal Phase 6A identity and future human-import contracts; no semantic scoring."""
from datetime import datetime,timezone
from html.parser import HTMLParser
import json
import re
from urllib.parse import urlsplit,urljoin
import gkg_semantics as s
import retrieve_gkg_semantics as old

STATES=('identity_confirmed','identity_probable_manual_review_required','identity_unresolved','identity_mismatch')

def uri(url):
    u=urlsplit(url)
    return ((u.hostname or '').lower().removeprefix('www.'),u.path.rstrip('/'),u.query)

def archive_locator(url,original,stamp):
    u=urlsplit(url);m=re.fullmatch(r'/web/(\d{14})(?:id_)?/(https?://.+)',u.path+('?' +u.query if u.query else ''))
    s.require(u.scheme in ('http','https') and u.hostname=='web.archive.org' and m is not None,'archive_locator_mismatch')
    s.require(m[1]==stamp and uri(m[2])==uri(original),'archive_locator_mismatch')
    return m[2]

class Metadata(HTMLParser):
    def __init__(self):super().__init__();self.canonical=[];self.dates=[];self.article=False;self.in_json=False;self.parts=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='link' and 'canonical' in a.get('rel','').lower().split() and a.get('href'):self.canonical.append(a['href'])
        if tag=='meta':
            key=a.get('property',a.get('name','')).lower()
            if key in ('article:published_time','datepublished') and a.get('content'):self.dates.append(a['content'])
            if key=='og:type' and a.get('content','').lower()=='article':self.article=True
        if tag=='script' and a.get('type','').lower()=='application/ld+json':self.in_json=True;self.parts=[]
    def handle_data(self,data):
        if self.in_json:self.parts.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self.in_json:
            self.in_json=False
            try:self.scan(json.loads(''.join(self.parts)))
            except (ValueError,RecursionError):pass
    def scan(self,v):
        if isinstance(v,list):
            for x in v:self.scan(x)
        elif isinstance(v,dict):
            types=v.get('@type',[]);types=[types] if isinstance(types,str) else types
            if isinstance(types,list) and any(x in ('NewsArticle','Article','ReportageNewsArticle') for x in types):
                self.article=True
                if isinstance(v.get('datePublished'),str):self.dates.append(v['datePublished'])
            if '@graph' in v:self.scan(v['@graph'])

def identify(case,receipt,blob,prior,*,method,capture=None):
    result={'identity_status':'identity_unresolved','identity_reason':'no_usable_response','publication_date':None,'capture_date':capture,
        'canonical_urls':[],'article_metadata':False,'content_changed_from_phase5':None,'title':'','excerpt':'','evidence_locator':None}
    if blob is None or receipt['status']!=200:return result
    if receipt['content_type'] not in ('text/html','application/xhtml+xml'):
        result['identity_reason']='unsupported_content_type';return result
    try:
        s.require(s.sha(blob)==receipt['content_sha256'],'source_hash_mismatch')
        text=blob.decode(receipt['charset'],errors='strict');meta=Metadata();meta.feed(text)
        context=old.extract_context(blob,case['token'],receipt['charset'])
        old.validate_extraction(blob,case['token'],context,content_hash=receipt['content_sha256'],charset=receipt['charset'])
    except (ValueError,UnicodeError,LookupError,RecursionError):
        result['identity_reason']='invalid_or_unverified_content';return result
    result.update(title=context['title'],canonical_urls=[urljoin(case['DocumentIdentifier'],u) for u in meta.canonical],article_metadata=meta.article)
    if old.blocked_context(context):result['identity_reason']='block_or_error_page';return result
    original=case['DocumentIdentifier'];final=receipt['final_url']
    if method=='dated_wayback_capture':
        try:archive_locator(final,original,capture)
        except s.Invalid:result.update(identity_status='identity_mismatch',identity_reason='archive_locator_mismatch');return result
    elif uri(final)!=uri(original):
        result.update(identity_status='identity_mismatch',identity_reason='publisher_path_changed');return result
    if any(uri(u)!=uri(original) for u in result['canonical_urls']):
        result.update(identity_status='identity_mismatch',identity_reason='canonical_identity_conflict');return result
    result.update(identity_status='identity_probable_manual_review_required',identity_reason='identity_metadata_incomplete')
    batch=datetime.strptime(case['batch_id'],'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
    dates=[]
    for date in meta.dates:
        try:
            parsed=datetime.fromisoformat(date.replace('Z','+00:00'))
            if parsed.tzinfo is None:parsed=parsed.replace(tzinfo=timezone.utc)
            dates.append(parsed)
        except ValueError:pass
    if dates:result['publication_date']=dates[0].isoformat()
    date_ok=bool(dates) and all(-7*86400<=(d-batch).total_seconds()<=86400 for d in dates)
    same=prior.get('source_hash_scope')=='complete_response_body' and prior.get('content_sha256')==receipt['content_sha256']
    if prior.get('content_sha256'):result['content_changed_from_phase5']=not same
    if method=='dated_wayback_capture':
        capture_ok=abs((datetime.strptime(capture,'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)-batch).total_seconds())<=7*86400
    else:capture_ok=same
    if result['canonical_urls'] and meta.article and date_ok and capture_ok:
        result.update(identity_status='identity_confirmed',identity_reason='canonical_dated_article_and_'+('dated_archive_locator' if method=='dated_wayback_capture' else 'prior_response_hash'),excerpt=context['excerpt'],evidence_locator=context['locator'])
    elif result['content_changed_from_phase5'] and method!='dated_wayback_capture':result['identity_reason']='publisher_content_changed_requires_review'
    return result

def validate_evidence(evidence,cases,*,trusted_hashes):
    s.require(len(evidence)==len(cases) and len({e['case_id'] for e in evidence})==len(cases),'evidence_cardinality')
    cm={c['case_id']:c for c in cases};s.require(set(trusted_hashes)==set(cm),'evidence_trust_set')
    for e in evidence:
        s.require(e['case_id'] in cm,'unknown_case');s.authenticate(e,trusted_hashes[e['case_id']],'recovery_evidence');c=cm[e['case_id']]
        for key in ('token','year','cohort'):s.require(e[key]==c[key],'frozen_metadata')
        s.require(e['original_url']==c['DocumentIdentifier'] and e['identity_status'] in STATES,'identity_contract')
        s.require(e['excerpt']=='' or e['identity_status']=='identity_confirmed','unconfirmed_excerpt')
        s.require(len(e['title'].split())+len(e['excerpt'].split())<=25,'quote_bound')
    return evidence

def packet(evidence):
    keys=('case_id','token','year','source','original_url','recovered_url','identity_status','title','excerpt')
    return [{**{k:e[k] for k in keys},'evidence_sha256':s.digest(e),'human_label':None,'reviewer_id':None} for e in evidence]

def import_humans(annotations,registry,cases,evidence,*,registry_root,evidence_hashes,review_protocol,review_protocol_root):
    s.authenticate(registry,registry_root,'human_registry')
    s.authenticate(review_protocol,review_protocol_root,'review_protocol')
    s.require(isinstance(review_protocol.get('version'),str) and review_protocol['version'],'review_protocol_version')
    validate_evidence(evidence,cases,trusted_hashes=evidence_hashes)
    for key in ('reviewer_id','person_id','independence_group'):
        s.require(all(r.get(key) for r in registry) and len({r[key] for r in registry})==len(registry),'duplicate_or_missing_reviewer')
    for r in registry:s.require(r.get('reviewer_type')=='human' and r.get('human_attestation_reference'),'human_attestation')
    rm={r['reviewer_id']:r for r in registry};em={e['case_id']:e for e in evidence};seen=set()
    required={'case_id','token','year','cohort','original_url','evidence_sha256','human_label','reviewer_id','reviewer_type','reviewed_at','review_protocol_version','review_protocol_sha256'}
    for a in annotations:
        s.require(set(a)==required and a['case_id'] in em and a['reviewer_id'] in rm,'annotation_contract')
        key=(a['case_id'],a['reviewer_id']);s.require(key not in seen,'duplicate_annotation');seen.add(key)
        e=em[a['case_id']]
        s.require(a['reviewer_type']=='human','not_human')
        s.require(a['review_protocol_version']==review_protocol['version'] and a['review_protocol_sha256']==review_protocol_root,'stale_review_protocol')
        for k in ('token','year','cohort','original_url'):s.require(a[k]==e[k],'frozen_metadata')
        s.require(a['evidence_sha256']==s.digest(e),'stale_evidence')
        s.require(a['human_label'] in s.LABELS,'invalid_label')
        s.require(e['identity_status']=='identity_confirmed' and e['excerpt'],'not_ready_for_semantic_review')
        s.require(datetime.fromisoformat(a['reviewed_at'].replace('Z','+00:00')).tzinfo is not None,'review_timestamp')
    return annotations
