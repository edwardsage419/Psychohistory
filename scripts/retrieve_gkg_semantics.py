"""Explicit opt-in, bounded public article retrieval; no full article retention."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.client import HTTPException
import ipaddress
import json
from pathlib import Path
import re
import socket
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit

import gkg_semantics as sem
from study_gkg_semantics import ROOT, STUDY, read, write

CUES={'PROTEST':r'\b(protest\w*|demonstrat\w*|dissent)\b',
      'FOOD_SECURITY':r'\b(food secur\w*|food insecur\w*|hunger|hungry|starv\w*|famine|food access)\b',
      'WB_2747_UNEMPLOYMENT':r'\b(unemploy\w*|jobless\w*)\b'}

class Paragraphs(HTMLParser):
    """Conservative complete paragraph text; no script/style/nav context."""
    def __init__(self):
        super().__init__(convert_charrefs=True);self.stack=[];self.paragraphs=[];self.parts=[];self.title_parts=[]
    def handle_starttag(self,tag,attrs):
        if tag not in ('br','img','meta','link','hr','input','source','wbr','area','base','embed','param','track'):
            self.stack.append(tag)
        if tag=='p':self.parts=[]
    def handle_endtag(self,tag):
        if tag=='p' and self.parts:
            text=' '.join(''.join(self.parts).split())
            if text:self.paragraphs.append(text)
            self.parts=[]
        if tag in self.stack:
            self.stack=self.stack[:len(self.stack)-1-self.stack[::-1].index(tag)]
    def handle_data(self,text):
        if 'title' in self.stack:self.title_parts.append(text)
        if 'p' in self.stack and not set(self.stack)&{'script','style','nav','footer','header','aside','noscript','template'}:
            self.parts.append(text)

def extract_context(blob,token,charset='utf-8'):
    # Strict decode: a guessed fallback could fabricate source evidence.
    text=blob.decode(charset,errors='strict')
    parser=Paragraphs();parser.feed(text)
    full_title=' '.join(''.join(parser.title_parts).split())
    title=full_title if len(full_title.split())<=8 else ''
    budget=25-len(title.split()); pattern=re.compile(CUES[token],re.I)
    excerpt='';locator=None;level='none';manual=True
    for i,para in enumerate(parser.paragraphs):
        # Sentence boundary is a locator heuristic, never evidence of topic truth.
        sentences=list(re.finditer(r'[^.!?]+[.!?](?:["\u201d\u2019])?',para))
        for j,m in enumerate(sentences):
            sentence=m.group().strip()
            if pattern.search(sentence) and 4<=len(sentence.split())<=budget:
                start=m.start()+len(m.group())-len(m.group().lstrip());end=m.end()
                # Add preceding sentence only if it fits; otherwise retain exact complete sentence.
                if j and len(para[sentences[j-1].start():end].split())<=budget:
                    start=sentences[j-1].start()
                    while start<end and para[start].isspace():start+=1
                excerpt=para[start:end];locator={'kind':'normalized_html_paragraph','paragraph_index':i,'start':start,'end':end,
                    'paragraph_sha256':sem.sha(para.encode('utf-8'))}
                level='complete_sentence_context';manual=False;break
        if excerpt:break
    if not excerpt:
        for i,para in enumerate(parser.paragraphs):
            if 4<=len(para.split())<=budget:
                excerpt=para;locator={'kind':'normalized_html_paragraph','paragraph_index':i,'start':0,'end':len(para),'paragraph_sha256':sem.sha(para.encode('utf-8'))}
                level='bounded_paragraph_manual';break
    # Compact evidence can still be insufficient: no semantic match assigned here.
    return {'title':title,'title_available':bool(full_title),'title_omitted_for_quote_budget':bool(full_title and not title),
        'excerpt':excerpt,'locator':locator,'extractor_version':sem.VERSION,'context_level':level,'manual_context_required':manual}

def validate_extraction(blob,token,extraction,*,content_hash,charset='utf-8'):
    sem.require(sem.sha(blob)==content_hash,'source_content_mismatch')
    sem.require(extract_context(blob,token,charset)==extraction,'excerpt_source_mismatch')

def check_public(url):
    sem.require(sem.public_reference(url),'unsupported_reference')
    u=urlsplit(url)
    addresses=socket.getaddrinfo(u.hostname,u.port or (443 if u.scheme=='https' else 80),type=socket.SOCK_STREAM)
    resolved=frozenset(str(ipaddress.ip_address(a[4][0])) for a in addresses)
    sem.require(resolved and all(ipaddress.ip_address(a).is_global for a in resolved),'nonpublic_address')
    return resolved

def _peer_ip(response):
    """Return the actual connected peer address from urllib/http.client wrappers."""
    queue=[response];seen=set()
    while queue:
        obj=queue.pop(0)
        if obj is None or id(obj) in seen:continue
        seen.add(id(obj))
        getpeer=getattr(obj,'getpeername',None)
        if callable(getpeer):
            try:
                peer=getpeer()
                if peer:return str(ipaddress.ip_address(peer[0] if isinstance(peer,tuple) else peer))
            except (OSError,ValueError,TypeError):
                pass
        for attr in ('fp','raw','_sock','sock'):
            child=getattr(obj,attr,None)
            if child is not None:queue.append(child)
    return None

def verify_public_peer(response,approved_addresses):
    peer=_peer_ip(response)
    sem.require(peer is not None,'peer_address_unavailable')
    sem.require(ipaddress.ip_address(peer).is_global,'nonpublic_peer_address')
    sem.require(peer in approved_addresses,'peer_address_not_preapproved')
    return peer

class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self,limit):super().__init__();self.limit=limit;self.chain=[];self.approved={}
    def approve(self,url,addresses):self.approved[url]=frozenset(addresses)
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        source=self.approved.get(req.full_url)
        sem.require(source,'redirect_source_not_preapproved')
        verify_public_peer(fp,source)
        self.chain.append({'from':req.full_url,'status':code,'to':newurl})
        sem.require(len(self.chain)<=self.limit,'redirect_limit')
        self.approve(newurl,check_public(newurl))
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def identity_requires_review(original,final):
    a,b=urlsplit(original),urlsplit(final)
    return (a.hostname or '').removeprefix('www.')!=(b.hostname or '').removeprefix('www.') or a.path.rstrip('/')!=b.path.rstrip('/') or a.query!=b.query or b.path in ('','/')

def blocked_context(e):
    return bool(re.search(r'access denied|request blocked|verify you are human|just a moment|page not found|captcha|enable javascript',e['title']+' '+e['excerpt'],re.I))

def retrieve(case,p,*,opener_factory=None):
    cfg=p['retrieval'];started=time.monotonic();redirects=Redirects(cfg['max_redirects'])
    url=case['DocumentIdentifier']
    e={'schema_version':sem.VERSION,'case_id':case['case_id'],'original_url':url,'final_url':None,
        'retrieved_at':datetime.now(timezone.utc).isoformat(),'protocol_sha256':sem.digest(p),'http_status':None,
        'availability':'document_unavailable','failure_category':None,'failure_detail':None,'attempts':1,
        'redirects':redirects.chain,'download_bytes':0,'content_sha256':None,'source_hash_scope':None,
        'content_type':None,'charset':None,'identity_review_required':False,'archive_lookup':'not_attempted',
        'title':'','title_available':False,'title_omitted_for_quote_budget':False,'excerpt':'','locator':None,
        'extractor_version':sem.VERSION,'context_level':'none','manual_context_required':True}
    try:
        if opener_factory is None:redirects.approve(url,check_public(url))
        opener=opener_factory(redirects) if opener_factory else urllib.request.build_opener(redirects)
        req=urllib.request.Request(url,headers={'User-Agent':'Psychohistory-research/0.5 (bounded semantic audit)','Accept':'text/html,application/xhtml+xml','Accept-Encoding':'identity'})
        with opener.open(req,timeout=cfg['timeout_seconds']) as response:
            e['http_status']=response.status;e['final_url']=response.geturl()
            if opener_factory is None:
                approved=redirects.approved.get(e['final_url'])
                sem.require(approved,'final_url_not_preapproved')
                verify_public_peer(response,approved)
            e['content_type']=response.headers.get_content_type();e['charset']=response.headers.get_content_charset() or 'utf-8'
            e['identity_review_required']=identity_requires_review(url,e['final_url'])
            blob=response.read(cfg['max_bytes']+1)
            e['download_bytes']=len(blob);e['content_sha256']=sem.sha(blob) if blob else None
            e['source_hash_scope']='bounded_prefix' if len(blob)>cfg['max_bytes'] else 'complete_response_body'
            sem.require(response.status==200,'non_200_status')
            sem.require(len(blob)<=cfg['max_bytes'],'response_size_limit')
            sem.require(e['content_type'] in ('text/html','application/xhtml+xml'),'unsupported_content_type')
            result=extract_context(blob,case['token'],e['charset'])
            validate_extraction(blob,case['token'],result,content_hash=e['content_sha256'],charset=e['charset'])
            e.update(result)
            if blocked_context(e):
                e['availability']='insufficient_context';e['failure_category']='blocked_or_error_page'
            elif e['identity_review_required']:
                e['availability']='insufficient_context';e['failure_category']='article_identity_requires_review'
            elif e['manual_context_required']:
                e['availability']='insufficient_context';e['failure_category']='context_requires_manual_review'
            else:e['availability']='retrieved_context'
    except urllib.error.HTTPError as exc:
        e.update(http_status=exc.code,final_url=exc.geturl(),failure_category='http_error',failure_detail=str(exc.code))
        exc.close()
    except HTTPException as exc:
        e['failure_category']='http_protocol_error';e['failure_detail']=type(exc).__name__
        partial=getattr(exc,'partial',None)
        if isinstance(partial,bytes) and partial:
            e.update(download_bytes=len(partial),content_sha256=sem.sha(partial),source_hash_scope='incomplete_response')
    except UnicodeError:
        e.update(availability='insufficient_context',failure_category='decode_error')
    except (LookupError,sem.Invalid) as exc:
        e['failure_category']=str(exc) if isinstance(exc,sem.Invalid) else 'unsupported_charset'
    except (urllib.error.URLError,TimeoutError,socket.timeout,OSError) as exc:
        reason=getattr(exc,'reason',exc)
        e['failure_category']='timeout' if isinstance(reason,(TimeoutError,socket.timeout)) else 'network_error'
        e['failure_detail']=type(reason).__name__
    e['duration_seconds']=round(time.monotonic()-started,6)
    e['context_sha256']=sem.context_hash(e)
    return e

def main():
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--network-integration',action='store_true',required=True);parser.add_argument('--sample-commit',required=True);args=parser.parse_args()
    import subprocess
    def pinned(path):return json.loads(subprocess.check_output(['git','show',args.sample_commit+':studies/gkg-semantics-v1/'+path],cwd=ROOT))
    p=read(STUDY/'preregistration.json');sample=read(STUDY/'sample.json');trust=pinned('sample-trust.json')
    sem.require(sample==pinned('sample.json'),'frozen_sample_changed')
    sem.validate_sample(sample,p,protocol_hash=trust['protocol_sha256'],sample_hash=trust['sample_sha256'])
    output=ROOT/'artifacts/gkg-phase5/retrieval';output.mkdir(parents=True,exist_ok=False)
    # Failures are written immediately, one receipt per selected reference; never replaced.
    def task(c):
        e=retrieve(c,p);write(output/(c['case_id']+'.json'),e);return e
    with ThreadPoolExecutor(max_workers=p['retrieval']['concurrency']) as pool:
        records=list(pool.map(task,sample['cases']))
    roots={e['case_id']:sem.digest(e) for e in records}
    sem.validate_evidence(records,sample,trusted_hashes=roots,protocol_hash=trust['protocol_sha256'])
    write(STUDY/'retrieval.json',records)
    write(STUDY/'retrieval-trust.json',{'schema_version':sem.VERSION,'sample_commit':args.sample_commit,'sample_sha256':trust['sample_sha256'],
        'receipt_hashes':roots,'origin':'Roots captured by trusted bounded retrieval execution before article bytes discarded; independently pin this Git publication on import.',
        'verification_limit':'Receipts authenticate captured excerpts; source hash alone cannot reconstruct discarded article bytes or prove article unchanged since GKG acquisition.'})
    from collections import Counter
    print(json.dumps({'total':len(records),'availability':dict(Counter(e['availability'] for e in records)),'failures':dict(Counter(e['failure_category'] for e in records))}))

if __name__=='__main__':main()
