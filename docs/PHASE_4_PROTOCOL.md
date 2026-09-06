# Phase 4 preregistered measurement protocol

Start: 09586cd, codex/project-reset-architecture, clean tree. Complete context
reads include AGENTS.md, every docs file and observation/source/ingestion schemas.
Baseline: 116 offline tests, 115 pass and one Windows symlink-permission skip.
Phase 3 is accepted; no ingestion contract redesign is authorized or needed.

## Four layers and study scope

Raw GKG bytes and Phase 3 dispositions are source data. A normalized observation
is a versioned scalar fact about source content. A source metric can exist for
every literal token without being an indicator. Only explicitly registered
experimental definitions create indicator values. Interpretation is a separate,
qualified claim. No event counts, real-world severity/risk, public opinion,
forecast, composite index, final ontology, country indicator or production value.

Use all 96 original batches, including years 2015/2016/2020/2023/2025/2026.
No new batch acquisition is initially justified: this phase measures semantics
and engineering behavior on the bounded corpus, not calendar representativeness.
Keep all fields/raw archives intact. Additional provider documentation downloads
are bounded research, never part of normal offline CI. External outcome comparison
is deferred unless a genuinely comparable series can be bounded without inferring
geography, events or contemporaneous complete daily coverage.

## Selection criteria established before choosing tokens

Target 5-15 small experimental token-prevalence definitions. Prefer explicit
provider examples with a documented topical explanation, followed by official
taxonomy labels with qualified semantics. Token spelling alone is not evidence.
Unknown tokens remain unresolved inventory entries. Require >=12 sampled batches
and >=3 sampled years for initial experimental inclusion, so a one-window spike
cannot dominate selection. These are exploratory usability screens, not scientific
validation thresholds. Prefer semantic diversity over correlated near-duplicates;
no old dashboard category is used as an ontology or selection input.

For every considered candidate record documentation quality, semantic clarity,
frequency/coverage/sparsity, temporal availability, unresolved extraction-definition
stability, denominator sensitivity, repeated-reporting risk, geographic ambiguity,
selection bias, interpretability and potential multi-source comparison. Naming
families are lexical inventory metadata only. Official examples establish a limited
label/use, not classifier precision or stable meaning across all historical years.
All selected definitions stay experimental. No silent aliasing or token expansion.

## Denominators, aggregation and quality

Primary metric: rows containing an exact V1THEMES token / all accepted rows.
Deduplicate a token within a row. Quarantine is excluded from both counts. Empty
theme fields stay in the primary denominator; their absence is also separately
reported. Compare the nonempty-theme denominator as a diagnostic of conditional
prevalence, never as a way to smooth the output. Zero denominator produces null,
not zero or NaN. Document-row prevalence measures sampled media tagging, not
actual events or all world news. Exact repeated document identifiers are a
separate diagnostic; do not modify primary counts or infer event deduplication.

Use configurable UTC windows that are integer multiples of 15 minutes and divide
a day. Evaluate hourly as primary and daily as a coverage stress test. Aggregate
by ratio of sums, never mean of batch percentages. Window start is inclusive,
end exclusive. Each window declares expected slots independently of which batches
arrived. A missing batch yields an incomplete-window flag and a null indicator
value; sampled numerator/denominator remain visible. No interpolation. Fully
covered windows with quarantine/empty themes/repeated IDs remain marked suspect.
Exact zero for an absent token is an observed literal absence, not proof the
provider was able to detect that concept in that historical year.

## Contracts, provenance and versioning

Keep observation v1 intact, with separate quality/provenance records keyed by
observation ID. Source metrics and indicator values are distinct new contracts.
Definitions include all requested source, transformation, scope, denominator,
aggregation, missingness, duplicate, smoothing, lag, bias and provenance fields.
Pin complete definition fingerprints and versions. Reject changing semantics under
an existing ID/version; retain append-only definition history. Historical outputs
state that the current experimental measurement rule was applied retrospectively,
not that its meaning was validated or deployed in those years.

Read pinned source bytes and verify each accepted row against Phase 3 hash/locator
before extracting fields. Exclude all quarantine. Bind batch/source/member/ledger,
parser, transformation and definition hashes to derived records. Execution clocks
are metadata outside semantic identity; prior acquisition timestamps stay in
provenance. Two independent runs must agree on stable outputs, regardless of input
ordering. Duplicate batches or source contradictions fail closed.

## Evidence, costs and decision

Produce full observed-token inventory, per-batch counts/prevalence distributions,
cohort/year coverage, deterministic selected-token co-occurrence diagnostics,
normalized observations, indicator values and separate quality/provenance JSONL.
Full inventory can be compressed for Git if measured size warrants it; lossless
compression changes no fields. Source metrics need not all become normalized
indicator observations. Measure the sizes of each derived class and compare with
raw ZIPs; extrapolations use actual sample means and explicit full-period counts.
No storage engine or paid dependency is selected in advance.

The architectural history recommendation requires deterministic, version-safe,
quality/provenance-complete outputs plus interpretable documented experimental
measurements. If historical meaning/stability remains inadequately supported for
cross-period analytical use, choose continue_semantic_validation; if the model
cannot express correct boundaries, redesign_indicator_foundation. Promotion never
means forecasts or validated societal severity. Do not weaken a gate to promote.

Dedicated adversarial self-review after implementation must challenge denominators,
coverage, duplicates, quarantine exclusion, hashes, definition versioning, ordering,
UTC boundaries, quality, source binding and retrospective semantics. Add regression
tests for each confirmed defect and rerun the full offline suite. Preserve all
prior evidence and protected production files; no main merge.
