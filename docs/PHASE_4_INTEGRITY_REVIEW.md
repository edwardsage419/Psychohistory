# Targeted post-Phase-4 integrity review

Starting commit: b3627a059ecf4332291f58cd744941978bb45838, clean working tree.
No next phase is authorized. Existing Phase 2/3 evidence, all 96 raw archives,
protected production behavior and the Phase 4 recommendation remain preserved.

## Reproduced attack and acceptance criteria

At the starting commit, an authenticated PROTEST count of 1 was replaced with 0,
the observation identity, downstream numerator/value and provenance identities
were updated, and the original receipt/source_metric_sha256 stayed unchanged.
Full bundle validation accepted the forged count and changed prevalence .5 to 0.
This is a confirmed source-to-observation provenance integrity defect.

The fix must compare every normalized count with the exact authenticated source
metric's theme_counts entry (including absent-token zero), not just row bounds or
a new derived hash. Tests must also cover coherent downstream alterations,
wrong/absent tokens, replaced evidence, hash mismatches, orphan/duplicate evidence,
definition policy/version binding, quality claims and manifest trust boundaries.
Acceptance requires all offline tests and final-HEAD CI passing, plus exact
96-batch replay showing whether legitimate published numerical outputs change.

## Design decision recorded before repair

Use complete existing source metrics through an explicit external validation
input, authenticated against an independently supplied batch-to-metric SHA-256
map. Do not infer trusted pins from bundle receipts or evidence supplied with the
bundle. Importers obtain pins from a separately verified published run/Git revision
or fresh raw-byte/Phase 3 ledger verification. Definition history, implementation
identity and replay manifest roots likewise come from the caller's trusted context.

This reuses the existing flat SHA-256 source contract and 16,060,713-byte compressed
96-batch metric cache. A Merkle proof would require changing source commitments
and cannot prove a subset against the existing flat metric hash. A new token-count
projection hash alone would add a second assertion without proving its relationship
to that hash. Full evidence resolution adds no duplicate data to compact bundles
and no service or storage engine. Fail closed if evidence is unavailable; raw
archives can regenerate metrics and their pinned hashes can verify recovery.
Do not promise verification from compact receipts alone or permanent upstream raw
availability. Existing local research metrics are retained; ordinary future
retention policy is not redesigned in this targeted review.

## Exact repair and trust boundary

`authenticated_metrics` checks structure, uniqueness, source family and the full
canonical semantic SHA-256 of every resolved metric against the independently
provided exact batch/hash set. `validate_bundle` reconstructs the entire expected
receipt from that authenticated metric and the trusted implementation fingerprint.
It requires exact receipt-set equality and exact source-observation coverage for
the selected tokens. For every normalized observation, it enforces:

```text
independent accepted-run pin == SHA256(canonical source metric)
receipt == receipt(authenticated metric, trusted implementation)
normalized value == authenticated metric.theme_counts.get(exact token, 0)
indicator numerator == sum(bound normalized input values)
```

The complete metric is supplied separately as `source_metrics`; it is not copied
into each compact bundle. `trusted_metric_hashes`, definition `history` and
`implementation_sha256` are mandatory keyword arguments. Missing evidence/context
fails closed. The study obtains pins only after successful raw ZIP, original
source hash, CRC/member and Phase 3 row-ledger authentication. Importers must use
separately trusted published/Git pins or fresh verified ingestion, never make a
candidate receipt or newly resealed source metric its own trust anchor.

For the retained original publication, [baseline-trust.json](../studies/gkg-indicators-v1/integrity-review/baseline-trust.json)
records pins read from immutable b3627a0 Git objects. All original source metrics
match those pins on fresh replay. No source-metric schema, token interpretation,
indicator definition/version, numerical transformation or Phase 3 code changed.
This deliberately avoids a second unauthenticated count hash and avoids inventing
a new Merkle/projection contract for a flat-hashed retained corpus.

## Adjacent defects and fixes

* Receipt/source evidence: self-consistent orphan receipts and unavailable,
  duplicate or replaced metric evidence were not resolved/checked on import.
  Authenticate and require exact source/receipt sets, full receipt contents and
  the trusted implementation fingerprint.
* Definition/transformation: the import path did not rerun registry history and
  supported-policy validation, and duplicate definitions could collapse in a map.
  Validate both before interpreting any value; reconcile provenance definition IDs.
* Source quality/identity: some altered source identity fields and source warning
  claims could survive resealing. Bind source, version, geography/entity, original
  acquisition timestamp and all source quality flags to authenticated evidence.
* Repetition diagnostics: sidecar repetition counts were shape-checked and used
  for flags but not recomputed from upstream rows. Recompute every window/token
  diagnostic from authenticated metric documents and compare the full result.
* Coverage: an available source batch could be omitted from a window and labeled
  missing while the remaining bundle stayed consistent. Reconcile observed slots
  with authenticated batch availability for that window, not just partition lists.
* Manifest boundary: two coherently rewritten manifests/artifact sets could pass
  equality and self-hash checks, including empty sets. `compare_runs` now requires
  two independently trusted full-manifest roots before checking contained bytes.
  This comparison proves pinned content equality; source-claim truth is established
  separately by authenticated bundle validation, not by hash consistency alone.
* Prior index cardinality: the study could collapse duplicate prior acquisition/
  ledger index entries before checking set size. It now checks list cardinality
  as well as the distinct batch set, with an offline regression.

The coherent primary attack and additional baseline reproductions are recorded in
[reproduction.json](../studies/gkg-indicators-v1/integrity-review/reproduction.json) and
[adjacent-reproductions.json](../studies/gkg-indicators-v1/integrity-review/adjacent-reproductions.json).
These findings concern importer/evidence verification. They do not imply that the
trusted original generator produced forged values. The exact original published
bundle passes the repaired validator against freshly regenerated source metrics.

## Regression and test evidence

There are **28 additional offline regression tests**, taking the complete suite
from 163 to **191**. The initial 15 adversarial tests produced 13 failed rejection
assertions on the old implementation; repaired tests reject those attacks. Required
coverage includes altered source counts with fresh IDs, fully propagated numerical
forgeries, wrong-token counts/labels, plausible positive counts for absent tokens,
source hash mismatch, internally valid replaced metrics with self-consistent
replacements downstream, missing/orphan/duplicate source evidence and orphan
receipts. Adjacent cases cover definition policy/history/duplicates, numerical and
source quality, implementation and provenance identity, omission of available
batches, coherent manifest rewriting and removed artifacts, and duplicate prior
indices. Valid bundles and evidence-order independence still pass.

Baseline local suite: 163 tests, 162 passed, one Windows symlink privilege skip,
zero failures/errors. Repaired full local suite: **191 tests, 190 passed, one
Windows symlink privilege skip, zero failures/errors**. All normal tests are offline;
no research archive is required by CI. Synthetic temporary corruption/deletion is
confined to test fixtures. The final committed HEAD is tested again before push;
the final response cites its exact GitHub run and SHA rather than relabeling an
ancestor's result.

The previously committed CI evidence referred to **033fd34**, 163/163 in 1.777 s.
An independent check confirms **b3627a0 itself also passed 163/163**, no skips,
in 2.304 s: [run 34001514230](https://github.com/edwardsage419/Psychohistory/actions/runs/34001514230).
These are distinct from final repaired-HEAD CI. Details are preserved in
[baseline-ci.json](../studies/gkg-indicators-v1/integrity-review/baseline-ci.json).

## Exact retained-corpus replay and numerical comparison

Two new offline runs authenticated all **96 original ZIPs**, totaling
**494,483,985 bytes**, and all original Phase 3 row dispositions. The ascending
run uses Phase 3 run3 ledgers; the descending run uses independent run4 ledgers.
Durations: **95.065 s / 93.539 s**. No acquisition, field reduction, raw rewrite,
quarantine repair or next-phase sampling occurred.

All 14 stable artifacts match across the two new runs. Full manifest root:
`a6c8c9c8fd2615101bdafc0492e0f131d380f3226bb94e8727e1c02f3bc2fd01`.
Artifact-set semantic hash:
`4dbb54d0acb8631667b91cf474810a1dd3c08f33c0c2030cae96aeb9a034ce13`.
Runtime clocks are excluded from semantic equality.

Against immutable b3627a0 Git artifacts:

* 96/96 authenticated source-metric hashes are unchanged.
* **672/672 normalized observations** retain exact numerical, unit, source,
  acquisition, scope and quality fields.
* **217/217 indicator records** retain exact counts, denominators, diagnostic
  prevalences, fractions/nulls, windows, definition versions and quality: 168
  non-null hourly records and 49 null partial-day records.
* **889/889 quality sidecars** retain every non-identity field, including complete
  repetition diagnostics and missingness/coverage.
* Nine artifacts are byte-identical: assessment, batch metrics/outcomes, candidate
  evaluation, co-occurrence, deferred candidates, historical assessment, complete
  inventory and storage measurements.

Only implementation fingerprints and dependent receipt/provenance/observation IDs
change in the newly generated bundles. Numerical comparison removes exactly those
identity/reference fields; it retains all numerical, definition, acquisition,
source and quality fields. The original publication is not overwritten. Both the
old bundle (using its original implementation pin) and new bundle pass the repaired
validator against independent original source pins.

[replay-comparison.json](../studies/gkg-indicators-v1/integrity-review/replay-comparison.json)
contains counts, hashes, preservation evidence and timings. The reproducible
comparison script is [verify.py](../studies/gkg-indicators-v1/integrity-review/verify.py).
Original run directories remain under `artifacts/gkg-phase4-integrity/replay-a`
and `replay-b`; the committed comparison/root evidence refers to those runs.

## Cost, preservation and conclusion

The full compressed source evidence remains **16,060,713 bytes** for 96 batches,
already retained before this review. No extra source evidence payload is added to
bundles, so measured storage representation is unchanged. Full evidence resolution
costs additional local validation CPU; it requires neither paid infrastructure nor
a new service/database. The prior hypothetical cache-volume estimate (~5.86 GB/year
at the mixed sample mean) remains an extrapolation, not a storage commitment. The
research caches remain intact. If both cached metrics and recoverable raw data are
lost, hashes alone cannot substantiate counts; validation must fail. This review
does not implement or decide a future raw-deletion policy.

Original raw archive hashes, Phase 2/3 evidence and protected dashboard/data/updater/
production-workflow content are unchanged. Existing Windows CRLF checkout behavior
is explicitly distinguished from Git blob bytes. No main merge. No next phase.
The recommendation remains **continue_semantic_validation**; this engineering
repair does not establish theme semantics or warrant promotion.

Implementation commit: `5096147`. The final evidence/documentation commit adds
this report, the final prior-index regression and the comparison verifier/evidence;
its exact SHA and its own CI outcome are reported in the final response. Review
and regression tests demonstrate these specific repairs, not absence of all bugs.
