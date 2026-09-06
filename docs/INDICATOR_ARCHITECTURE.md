# Indicator foundation contracts and local operation

Source data, normalized observations, registered indicators and interpretations
are separate concepts. All observed GKG token metrics can be inventoried; only
explicit IndicatorDefinition entries generate experimental indicator values.
Definitions express dataset, field, transformation and parameters, units, time,
spatial/entity scope, denominator, aggregation, missingness, duplication,
smoothing, lag, quality requirements, biases, limitations and provenance.
The schema is source-independent; computation adapters must reject unsupported
methods/policies rather than guess. No source family beyond GKG is integrated.

## Current implementation

* `gkg_indicator_metrics.py`: verifies raw ZIP/source/member and published Phase 3
  ledger pins, validates every row disposition against raw bytes, then extracts
  exact column-8 tokens. No case folding, whitespace trimming or synonym mapping.
* `indicator_definitions.py`: definition schema, content/version history,
  duplicate-definition checks and the supported experimental GKG adapter policy.
* `indicator_engine.py`: normalized source-count observations, configurable UTC
  aggregation, separate indicator values, quality and provenance; contract and
  cross-record reconciliation on export/import through `validate_bundle`.
* `study_gkg_indicators.py`: explicitly bounded offline 96-batch study, inventory,
  candidate/denominator/history diagnostics, storage measurement and replay check.
* `test_indicators.py`: synthetic offline fixtures, adversarial regressions and
  bounded end-to-end studies. Normal CI requires neither archives nor network.

Schemas live in `schemas/indicator-*.v1.schema.json` and
`schemas/gkg-source-metric.v1.schema.json`; observation v1 is unchanged. Definitions
and their initial release history live in `studies/gkg-indicators-v1/`.
The history is an append-only review contract: preserve previous key/fingerprint
pairs, add a version for a semantic change, and pass prior history to registry
validation when importing a successor. CI pins the initial release identities.
This does not defend against simultaneous rewriting of all code/trust anchors.

## Values and quality

Primary ratio: exact token row presence / all accepted rows. Include empty-theme
rows in the denominator; exclude all quarantines. Within-row duplicate token
mentions count once. Exact repeated document identifiers remain in primary counts,
with union-over-identifier statistics separately labeled diagnostic. No event or
syndication clustering. Nonempty-theme prevalence is a conditional diagnostic.

UTC window durations are integer multiples of 15 minutes dividing a day. Hourly
is the present research choice; daily is a coverage test. Expected slots come
from window boundaries independently of observed arrivals. Entirely missing
windows can be explicitly requested. Missing slots or zero denominator yield null;
partial sampled diagnostics remain visible. No imputation. All present indicator
values are suspect because definitions/historical interpretation are experimental.

Geography/entity are null: source outlet, mentioned place, event location and
subject geography cannot be substituted for one another. Observation time means
source batch/window time. It does not mean event or article publication time.
Same-version exact-token retrospective calculations do not establish that the
provider used the same semantic extractor historically.

## Provenance and retention

672 selected-token source observations in this study point to 96 compact receipts.
Receipts include acquisition metadata, source ZIP/hash/bytes, member and ledger
hashes, parser/schema versions, accepted/quarantine/empty counts and implementation
hashes. Indicator provenance points to those receipt hashes, contributing source
observation IDs, complete definition hash/version and expected window slots.
For an aggregate, `source_snapshot_sha256` hashes the ordered receipt-hash list;
it is not a claim that multiple ZIPs are one raw archive. The referenced receipt
manifest is retained with the value. `retrieved_at` is original acquisition
metadata or the study acquisition cutoff, not the execution clock; observation
identity excludes it by the unchanged v1 contract.

Retain compact irreplaceable quarantine bytes, definition histories, receipts and
study decisions. Normally retain derived observations and sidecars. Original
96-batch corpus and ledgers stay intact; ordinary future public raw artifacts may
only follow a separate configurable retention policy. No deletion is implemented.
Hashes verify recovered revisions but cannot reconstruct lost source bytes.
Local full metrics retain exact-document-identifier hashes and per-row token sets
for diagnostic replay; their 16 MB gzip footprint is measured separately from
compact published evidence. No storage engine is introduced.

## Reproduce locally

Use Python 3.12 and restore the existing pinned corpus/ledgers to their documented
local paths (see PHASE_3_REPORT.md). Commands below are offline; each output root
must be new, disjoint from input directories, and kept for review:

```text
python -B scripts/study_gkg_indicators.py --output artifacts/phase4-replay-a
python -B scripts/study_gkg_indicators.py --output artifacts/phase4-replay-b --ledgers artifacts/gkg-phase3-run4 --reverse
python -B -m unittest discover -s scripts -p "test_*.py"
```

To compare, import `study_gkg_indicators.compare_runs(first, second)` with scripts
on Python's module path. It verifies actual stable output bytes and input/code
pins, requires distinct evidence directories, and excludes only execution clocks.
Published `results/` contains additional review/CI artifacts; compare the original
run directories, not a publication directory with extra files.

The CLI reports every per-batch expected error in `batch-outcomes.json`, continues
to inspect all scheduled inputs, and produces `failure.json` with no success
manifest if any batch fails. Configuration/late-stage errors are machine-readable
JSON on stdout with exit 2. They cannot produce a passed execution receipt.
Exact source/registry bytes are retained in `artifacts/gkg-phase4/source-snapshot`; code pins include checkout line endings, so restore those bytes or declare a different implementation hash for cross-platform replay. Code/schema changes during a run prevent certification. Replays pin versions but
do not claim equality under future Python/gzip releases without verification.

Official documentation research is separate from execution and offline CI.
Snapshots are under `artifacts/gkg-phase4/source-documents` and the earlier codebook
path; hashes, URLs and all failed attempts are committed. No paid APIs or hosted
analytics are used. Detailed findings, sizes and unresolved questions are in
PHASE_4_REPORT.md; these modules never write dashboard or production files.
