# Phase 5 semantic audit architecture

The audit is a local, standard-library research layer. It does not change the
frozen indicator engine, production ingestion, dashboard or seven definitions.

## Evidence flow and trust

1. `study_gkg_semantics.py` authenticates original ZIP bytes and Phase 3 row ledgers,
   regenerates source metrics against independently pinned Phase 4 hashes, then
   extracts exact DocumentIdentifiers and row locators. Selection uses the frozen
   protocol, seed, theme-richness edge rule and cohort allocations.
2. Commit the sample and its root before article inspection. `77fe85a` is this
   study's sample publication. No replacements or silent shortfall reallocation.
3. `retrieve_gkg_semantics.py --network-integration --sample-commit <trusted SHA>`
   performs one bounded public GET per reference, validates redirects, extracts
   complete sentence/paragraph context, checks extraction against response bytes,
   and retains compact receipts. Full publisher responses are transient. A cue
   locates text; it never assigns a topical label. Identical URL/path is only an
   identity screen, not proof that historical content survived unchanged.
4. `ea22f67` pins all 120 receipts, the registry, protocol and initial machine
   availability annotations. Human annotations require a genuine operator-attested
   human registry entry. LLM entries require model/prompt/settings/protocol metadata
   and cannot become human records by editing an annotation's reviewer type.
5. `assess_gkg_semantics.py --evidence-commit <trusted SHA> --output <new directory>`
   reads inputs from that independently selected Git revision and compares working
   files. It authenticates every input before calculating denominators, agreement
   and gates. Importers must not accept a candidate-provided revision/root as its
   own authority. `verify_artifacts` also requires an independently accepted full
   manifest root, including input and implementation hashes.

Raw/GKG and publisher-body hashes always cover exact bytes. Implementation hashes
alone normalize CRLF to LF and remove an optional UTF-8 BOM for portable code
identity. No source bytes are normalized for provenance. Original corpus hashes,
row offsets, line identities, metric hashes, source references and parser/contract
versions remain resolvable through pinned Phase 3/4 evidence.

A receipt proves what the trusted capture recorded. A source hash alone cannot
reconstruct discarded text, prove a new excerpt against missing bytes, or prove
that a publisher response equals its historical GDELT revision. Fail closed on
missing trust context; retain this limitation when interpreting semantic evidence.

## Review and numerical rules

The human packet has 120 rows, fixed label choices and blank human labels. It is
explicitly unblinded: year, source and concept are visible; aggregate prevalence
and expected conclusions are absent. The packet is reconstructed and validated
against authenticated inputs. Human reviewers must verify article identity and
context; machine-selected context is provisional. Additional retrieval/context
would require a versioned protocol and new receipts without removing old failures.

No optional model review is executed. Cache contracts bind content, excerpt,
protocol, model, prompt and settings. The committed compact context cache permits
reuse without sending full articles to a model. Changing any review configuration
invalidates cached judgments. Actual human attestation cannot be established by
schema validation alone; its trusted registry must come from a responsible operator.

Deduplicate exact references before selection. Complete response-body hashes alone
identify exact content duplicates; bounded prefixes do not. Within each reported
scope, choose a deterministic representative but resolve a review from any identical
reference for the same concept. Reject conflicting same-reviewer labels on identical
content. Agreement between independent reviewers remains visible, including by token
and year. Cross-token/year subgroup counts need not add to global unique-article N
when exact duplicate bodies exist; this sample has none. Different syndicated
revisions are not automatically collapsed.

Always show selected, unique candidate-context, unavailable, insufficient and
actually semantically reviewed denominators. Semantic rates remain null without
semantic labels. No recall from positive-only sampling. Required-year gates use
preregistered allocated strata, never just surviving cases. Every adequately paired
independent reviewer pair must meet the agreement threshold; a favorable pair
cannot hide an unfavorable pair. Statistics are descriptive convenience-sample
checks, not population classifier precision or proof of historical stability.

## Cost and storage

Default to zero or near-zero recurring infrastructure cost. Paid infrastructure
should be introduced only when a free approach materially harms data integrity,
reproducibility, reliability, analytical quality, or product capability, and the
benefit is supported by evidence.

Retain irreplaceable protocols, samples, receipts/minimal excerpts, reviewer
attestations, annotations and roots; normally retain derived packets/assessments.
The original 96 ZIPs and quarantine evidence remain intact. Future ordinary GKG
raw retention stays separately configurable; no deletion or cadence/field reduction
is implemented. No database, hosted compute, paid API or model dependency is added.
Git stores compact evidence/code, local files store original archives and replay
fixtures, and normal GitHub CI is fully offline. Exact category measurements and
conditional storage scenarios are in `studies/gkg-semantics-v1/storage.json`.

## Reproduce the accepted assessment

```text
python -B scripts/assess_gkg_semantics.py --evidence-commit ea22f67cc139c3e9203151ef5a5b7b84b46a8f2e --output artifacts/new-phase5-replay
python -B -m unittest discover -s scripts -p "test_*.py"
```

The accepted assessment manifest's canonical root is
`7776721638beeecb7eb235c3bded17f439abaa1e831dbd81d44371c652d532d4`.
Resolve it through a separately accepted Git publication before using it as trust.
Replaying captures is offline and does not claim live URLs reproduce old bytes.
The sample CLI is a write-once original-study command: full sample regeneration
requires the retained local corpus and a separate output workspace; do not rerun
network acquisition merely to regenerate statistics or overwrite frozen evidence.
