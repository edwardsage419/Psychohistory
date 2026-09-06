"""Offline Phase 5 assessment/export. Pin a reviewed Git evidence revision on import."""
import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path
import subprocess

import gkg_semantics as s
from study_gkg_semantics import ROOT,STUDY,read,write

INPUTS=('preregistration.json','sample.json','sample-trust.json','retrieval.json','retrieval-trust.json',
        'annotations.json','reviewers.json','taxonomy-evidence.json','annotation-protocol.json')

def load_trusted(revision):
    result={}
    for name in INPUTS:
        original=json.loads(subprocess.check_output(['git','show',revision+':studies/gkg-semantics-v1/'+name],cwd=ROOT))
        s.require(original==read(STUDY/name),'input_differs_from_trusted_git_'+name)
        result[name]=original
    return result

def verify_artifacts(root,manifest,*,trusted_manifest_hash):
    s.authenticate(manifest,trusted_manifest_hash,'assessment_manifest')
    expected=set(manifest['artifacts'])
    s.require(expected and all(Path(n).name==n and not Path(n).is_absolute() for n in expected),'artifact_names')
    for name,h in manifest['artifacts'].items():
        path=Path(root)/name
        s.require(path.is_file() and not path.is_symlink() and s.sha(path.read_bytes())==h,'artifact_binding')
    return True

def export(data,output,*,evidence_revision):
    output=Path(output);p=data['preregistration.json'];sample=data['sample.json'];es=data['retrieval.json'];annotations=data['annotations.json'];rs=data['reviewers.json'];taxonomy=data['taxonomy-evidence.json']
    trust={'protocol':data['sample-trust.json']['protocol_sha256'],'sample':data['sample-trust.json']['sample_sha256'],
        'receipts':data['retrieval-trust.json']['receipt_hashes'],'reviewers':s.digest(rs),'annotations':s.digest(annotations),'taxonomy':s.digest(taxonomy)}
    s.require(data['annotation-protocol.json']['preregistration_sha256']==trust['protocol'],'annotation_contract_protocol')
    s.require(data['retrieval-trust.json']['sample_sha256']==trust['sample'],'retrieval_sample_binding')
    result=s.assess(sample,p,es,annotations,rs,taxonomy,trust=trust)
    human_packet=s.packet(sample,es,p);s.validate_packet(human_packet,sample,es,p)
    def grouped(key):
        values=sorted({c[key] for c in sample['cases']})
        return {str(v):s.summary([c for c in sample['cases'] if c[key]==v],es,annotations) for v in values}
    availability={'schema_version':s.VERSION,'total':s.summary(sample['cases'],es,annotations),
        'by_token':grouped('token'),'by_year':grouped('year'),'by_outlet':grouped('source_name'),
        'http_status_counts':dict(sorted(Counter(str(e['http_status']) for e in es).items())),
        'failure_taxonomy':dict(sorted(Counter(e['failure_category'] or 'none' for e in es).items())),
        'archived_status':'not_attempted; direct publisher retrieval only','identity_review_required':sum(e['identity_review_required'] for e in es),
        'availability_interpretation':'Bounded current retrieval outcomes; network/HTTP failures do not prove permanent article loss. Candidate contexts are not human-validated articles.'}
    records={'assessment.json':result,'token-assessments.json':result['tokens'],'agreement.json':result['agreement'],
        'availability.json':availability,'human-review-packet.json':human_packet}
    # Evidence cache, keyed by source bytes and exact extraction context/configuration.
    cache={};hits=0
    for c,e in zip(sample['cases'],es):
        s.require(c['case_id']==e['case_id'],'retrieval_order')
        if e['content_sha256']:
            key=s.digest([e['content_sha256'],c['token'],e['extractor_version'],trust['protocol'],e['context_sha256']])
            entry={'content_sha256':e['content_sha256'],'context_sha256':e['context_sha256'],'title':e['title'],'excerpt':e['excerpt'],
                'locator':e['locator'],'token':c['token'],'protocol_sha256':trust['protocol'],'extractor_version':e['extractor_version']}
            if key in cache:hits+=1;s.require(cache[key]==entry,'context_cache_collision')
            else:cache[key]=entry
    records['context-cache.json']={'version':s.VERSION,'entries':cache}
    records['efficiency.json']={'version':s.VERSION,'documents_processed_deterministically':len(es),
        'human_semantic_reviews':sum(a['reviewer_type']=='human' and a['label'] in s.SEMANTIC for a in annotations),
        'article_llm_review_calls':0,'documents_sent_to_llm':0,'full_articles_sent_to_llm':0,'full_article_context_required':None,
        'full_context_reason':'Not determined without human assessment; no full articles sent to a model.',
        'documents_requiring_llm_review':0,'llm_review_necessary':'not_assumed; pending genuine human review',
        'semantic_cases_resolved_using_compact_excerpts':0,'candidate_compact_contexts':sum(e['availability']=='retrieved_context' for e in es),
        'cached_context_entries':len(cache),'cached_context_hits':hits,'cached_review_hits':0,'repeated_llm_calls_avoided_via_cache':0,
        'article_model_input_tokens':0,'article_model_output_tokens':0,'codex_engineering_token_usage':None,
        'codex_engineering_token_usage_reason':'Not available from task accounting; no extra calls made to estimate it.',
        'full_article_storage_bytes':0,'recurring_paid_dependencies':0}
    for name,value in records.items():write(output/name,value)
    stream=io.StringIO(newline='');columns=['case_id','source','year','token','concept','url','title','excerpt','availability','label','reviewer_id','blinded']
    writer=csv.DictWriter(stream,fieldnames=columns,extrasaction='ignore',lineterminator='\n');writer.writeheader();writer.writerows(human_packet)
    with (output/'human-review-packet.csv').open('xb') as f:f.write(stream.getvalue().encode('utf-8'))
    names=list(records)+['human-review-packet.csv']
    manifest={'schema_version':s.VERSION,'evidence_revision':evidence_revision,'input_hashes':{n:s.digest(v) for n,v in sorted(data.items())},
        'implementation_hashes':{n:s.sha((ROOT/'scripts'/n).read_bytes().replace(b'\r\n',b'\n').removeprefix(b'\xef\xbb\xbf')) for n in ('gkg_semantics.py','study_gkg_semantics.py','retrieve_gkg_semantics.py','assess_gkg_semantics.py')},
        'implementation_hash_encoding':'UTF-8 source, optional BOM removed and CRLF normalized to LF; separate from source data hashes',
        'artifacts':{n:s.sha((output/n).read_bytes()) for n in sorted(names)},
        'trust_boundary':'Caller supplies independently accepted full manifest SHA256; a candidate manifest is not its own authority.'}
    write(output/'assessment-manifest.json',manifest)
    verify_artifacts(output,manifest,trusted_manifest_hash=s.digest(manifest))
    return result,manifest

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--evidence-commit',required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    result,manifest=export(load_trusted(args.evidence_commit),args.output,evidence_revision=args.evidence_commit)
    print(json.dumps({'recommendation':result['recommendation'],'manifest_sha256':s.digest(manifest),
        'tokens':[{k:t[k] for k in ('token','decision','gates')} for t in result['tokens']]}))

if __name__=='__main__':main()
