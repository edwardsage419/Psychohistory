"""Phase 6A evidence recovery contracts. Missing evidence never becomes a judgment."""
from datetime import datetime,timezone
from html.parser import HTMLParser
import hashlib
import json
import re
from urllib.parse import urljoin,urlsplit
import gkg_semantics as s
import retrieve_gkg_semantics as old

IDENTITY=('identity_confirmed','identity_probable_manual_review_required','identity_mismatch','identity_unresolved')

class Meta(HTMLParser):
    def __init__(self):super().__init__(convert_charrefs=True);self.canon=[];self.meta={};self.title=[];self.stack=[]
    def handle_starttag(self,t,a):
        d=dict(a)
        if t=='link' and 'canonical' in d.get('rel','').lower() and d.get('href'):self.canon.append(d['href'])
        if t=='meta':
            k=d.get('property') or d.get('name');v=d.get('content')
            if k and v:self.meta.setdefault(k.lower(),v)
        if t not in ('br','img','meta','link','hr','input','source','wbr','area','base','embed','param','track'):self.stack.append(t)
    def handle_endtag(self,t):
        if t in self.stack:self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(t)]
    def handle_data(self,x):
        if 'title' in self.stack:self.title.append(x)

def meta(blob,charset,base):
    try:text=blob.decode(charset or 'utf-8','strict')
    except (UnicodeError,LookupError):return {'canonical_urls':[],'publication_dates':[],'article_metadata':False,'html_title':''}
    p=Meta();p.feed(text)
    canon=[]
    for x in p.canon:
        u=urljoin(base,x)
        if u.startswith(('http://','https://')) and u not in canon:canon.append(u)
    dates=[]
    for k in ('article:published_time','datepublished','date','pubdate','publishdate','datepublished'):
        if p.meta.get(k):dates.append(p.meta[k])
    article=p.meta.get('og:type','').lower()=='article' or any(k in p.meta for k in ('article:published_time','datepublished','pubdate','publishdate'))
    return {'canonical_urls':canon,'publication_dates':dates,'article_metadata':article,'html_title':' '.join(''.join(p.title).split())}

def uri(url):
    """URI identity that permits normal HTTP→HTTPS/default-port equivalence only."""
    u=urlsplit(url)
    scheme=u.scheme.lower()
    port=u.port
    default_port={'http':80,'https':443}.get(scheme)
    port_key=None if port is None or port==default_port else port
    return ((u.hostname or '').lower().removeprefix('www.'),port_key,u.path.rstrip('/'),u.query)

def date(v):
    try:
        d=datetime.fromisoformat(v.replace('Z','+00:00'));return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
    except (ValueError,TypeError):return None

def archive_locator(url,original,capture):
    u=urlsplit(url);s.require(u.hostname=='web.archive.org','archive_provider')
    m=re.match(r'^/web/(\d{14})(?:id_)?/(https?://.+)$',u.path+('?' +u.query if u.query else ''))
    s.require(m is not None and m.group(1)==capture and uri(m.group(2))==uri(original),'archive_locator_identity')

def reviewable_context(e):
    """True only for the frozen Phase 5 token-cue context path, never generic fallback text."""
    token=e.get('token');excerpt=e.get('excerpt') or '';locator=e.get('evidence_locator')
    cue=old.CUES.get(token)
    return bool(locator and excerpt and cue and re.search(cue,excerpt,re.I))

def identify(case,receipt,blob,prior,method,capture=None):
    result={'identity_status':'identity_unresolved','identity_reason':'no_usable_response','evidence_locator':None,'excerpt':'','title':'',
        'publication_date':None,'article_metadata':False,'canonical_urls':[],'content_changed_from_phase5':None,'capture_date':capture}
    if blob is None or receipt.get('status')!=200:return result
    m=meta(blob,receipt.get('charset'),'https://'+(urlsplit(receipt['final_url']).netloc or urlsplit(case['DocumentIdentifier']).netloc)+'/')
    result.update(article_metadata=m['article_metadata'],canonical_urls=m['canonical_urls'],title=m['html_title'])
    original=case['DocumentIdentifier'];final=receipt['final_url']
    if method=='dated_wayback_capture':
        try:archive_locator(final,original,capture)
        except s.Invalid:
            result.update(identity_status='identity_mismatch',identity_reason='archive_locator_mismatch');return result
    else:
        if uri(final)!=uri(original) and all(uri(x)!=uri(original) for x in m['canonical_urls']):
            result.update(identity_status='identity_mismatch',identity_reason='publisher_path_changed');return result
        if any(uri(x)!=uri(original) for x in m['canonical_urls']):
            result.update(identity_status='identity_mismatch',identity_reason='canonical_identity_conflict');return result
    dates=[d for d in (date(x) for x in m['publication_dates']) if d]
    batch=datetime.strptime(case['batch_id'],'%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
    date_ok=bool(dates) and all(-7*86400 <= (d-batch).total_seconds() <= 86400 for d in dates)
    prior_complete=prior.get('source_hash_scope')=='complete_response_body' and prior.get('content_sha256')
    same_hash=bool(prior_complete and receipt.get('content_sha256')==prior['content_sha256'])
    result['content_changed_from_phase5']=False if same_hash else True if prior_complete else None
    confirmed=(method=='dated_wayback_capture' and capture is not None) or (method!='dated_wayback_capture' and date_ok and same_hash and m['article_metadata'])
    if confirmed:
        try:
            context=old.extract_context(blob,case['token'],receipt.get('charset') or 'utf-8')
            old.validate_extraction(blob,case['token'],context,content_hash=receipt['content_sha256'],charset=receipt.get('charset') or 'utf-8')
            reviewable=not context['manual_context_required']
            result.update(identity_status='identity_confirmed',identity_reason='verified_archive_capture' if method=='dated_wayback_capture' else 'canonical_dated_article_and_prior_response_hash',
                evidence_locator=context['locator'] if reviewable else None,excerpt=context['excerpt'] if reviewable else '',title=context['title'],
                publication_date=dates[0].isoformat() if dates else None)
        except (UnicodeError,LookupError,s.Invalid):
            result.update(identity_status='identity_confirmed',identity_reason='identity_confirmed_context_unavailable')
    else:
        reason='identity_metadata_incomplete' if not date_ok or not m['article_metadata'] else 'publisher_content_changed_requires_review'
        result.update(identity_status='identity_probable_manual_review_required',identity_reason=reason,publication_date=dates[0].isoformat() if dates else None)
    return result

def validate_evidence(evidence,cases,*,trusted_hashes):
    cs={c['case_id']:c for c in cases};s.require(len(evidence)==len(cs) and set(trusted_hashes)==set(cs),'evidence_set')
    seen=set()
    for e in evidence:
        s.require(e['case_id'] in cs and e['case_id'] not in seen,'evidence_case');seen.add(e['case_id']);s.authenticate(e,trusted_hashes[e['case_id']],'evidence')
        c=cs[e['case_id']]
        for a,b in (('token','token'),('year','year'),('cohort','cohort')):s.require(e[a]==c[b],'evidence_sample_binding')
        s.require(e['original_url']==c['DocumentIdentifier'] and e['identity_status'] in IDENTITY,'evidence_identity')
        if e['identity_status']=='identity_confirmed':s.require(bool(e['excerpt'])==bool(e['evidence_locator']),'confirmed_context_pair')
    return evidence

def packet(evidence):
    return [{'case_id':e['case_id'],'token':e['token'],'year':e['year'],'cohort':e['cohort'],'original_url':e['original_url'],'recovered_url':e.get('recovered_url'),
        'identity_status':e['identity_status'],'identity_reason':e['identity_reason'],'evidence_sufficiency':'E3' if e['identity_status']=='identity_confirmed' and reviewable_context(e) else 'E1' if e['identity_status']=='identity_confirmed' else 'E0',
        'title':e['title'] if e['identity_status']=='identity_confirmed' else '','excerpt':e['excerpt'] if e['identity_status']=='identity_confirmed' else '',
        'content_sha256':e.get('content_sha256'),'evidence_sha256':s.digest(e),'human_label':None,'reviewer_id':None,'reviewed_at':None} for e in evidence]

def import_humans(annotations,registry,cases,evidence,*,registry_root,evidence_hashes,review_protocol,review_protocol_root):
    """No UI/model output can manufacture human status; trust roots are supplied externally."""
    s.authenticate(registry,registry_root,'human_registry');s.authenticate(review_protocol,review_protocol_root,'review_protocol')
    s.require(review_protocol.get('version')=='1.0.0','review_protocol_version')
    s.require(len({r['reviewer_id'] for r in registry})==len(registry),'duplicate_reviewer_id')
    humans={r['reviewer_id']:r for r in registry if r.get('reviewer_type')=='human'}
    for r in humans.values():s.require(r.get('person_id') and r.get('independence_group') and r.get('human_attestation_reference'),'human_attestation')
    s.require(len({r['person_id'] for r in humans.values()})==len(humans),'duplicate_human_identity')
    validate_evidence(evidence,cases,trusted_hashes=evidence_hashes);es={e['case_id']:e for e in evidence};cs={c['case_id']:c for c in cases};seen=set()
    allowed=set(s.LABELS[:5])
    for a in annotations:
        s.require(a['case_id'] in cs and a['reviewer_id'] in humans,'human_annotation_reference')
        key=(a['case_id'],a['reviewer_id']);s.require(key not in seen,'duplicate_human_annotation');seen.add(key)
        c,e=cs[a['case_id']],es[a['case_id']]
        s.require(e['identity_status']=='identity_confirmed' and reviewable_context(e),'insufficient_identity_for_semantic_review')
        s.require(a.get('human_label') in allowed and a.get('reviewer_type')=='human','human_label_or_type')
        s.require(a.get('review_protocol_version')==review_protocol['version'] and a.get('review_protocol_sha256')==review_protocol_root,'review_protocol_binding')
        s.require(a.get('evidence_sha256')==evidence_hashes[a['case_id']],'human_evidence_binding')
        for k,ck in (('token','token'),('year','year'),('cohort','cohort'),('original_url','DocumentIdentifier')):s.require(a.get(k)==c[ck],'human_sample_binding')
        datetime.fromisoformat(a['reviewed_at'].replace('Z','+00:00'))
    return annotations
