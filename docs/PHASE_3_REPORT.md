# Phase 3 final report: lossless GKG parsing and quarantine

Recommendation: **promote_to_ingestion_candidate**, limited to raw acquisition,
archive verification, lossless row parsing, deterministic quarantine and
reproducible provenance. This does **not** validate GKG themes as Psychohistory
indicators, approve a final ontology, or authorize production dashboard migration.

## Starting state, commits and push status

Repository: edwardsage419/Psychohistory. Working branch:
`codex/project-reset-architecture`. Actual local checkout:
`D:/GPT/Psychohistory-issue2`. Start HEAD was exactly
`eabba6a416cead3b23fcf36b597d3060e21de1a1`, with a clean working tree and all 75
baseline offline tests passing. Its three self-review fixes were preserved;
no reset, rebase, recreation or main merge occurred. The previously unpushed
`eabba6a` was successfully pushed before Phase 3 implementation.

Reviewable commits created in this phase:

* `dcd07df`: preregister lossless policy and promotion gates before evaluation.
* `2085159`: parser, quarantine/replay contracts, tests and near-zero-cost design.
* `97798e2`: enforce the row resource bound before allocating a field list.
* Final publication commit containing this report: `docs: publish Phase 3 quarantine evidence and candidate assessment`.

The first three are confirmed on GitHub. The publication commit is pushed in the
completion step; its exact SHA is reported in the task completion message. No
source-registry production status is promoted automatically.

## Exact corpus and execution

The [original manifest](../studies/gkg-continuity-v1/manifest.json) is unchanged;
canonical SHA-256 is `443f60269a89251655b0636799988e15034b55a8ceb58ffea57c8d236bf2ef15`.
All listed windows are inclusive UTC quarter-hour slots:

| Cohort | Window | Batches |
| --- | --- | ---: |
| recent | 2026-09-04 00:00 through 17:45 | 72 |
| historical_2015 | 2015-03-02 00:00 through 00:45 | 4 |
| historical_2016 | 2016-09-05 06:00 through 06:45 | 4 |
| historical_2020 | 2020-09-05 12:00 through 12:45 | 4 |
| historical_2023 | 2023-09-05 18:00 through 18:45 | 4 |
| historical_2025 | 2025-09-05 00:00 through 00:45 | 4 |
| historical_2026 | 2026-08-05 12:00 through 12:45 | 4 |

This is the English-feed filename family, with 24 sparse historical batches,
not verified availability between those windows or a multilingual census. No
new source batches were downloaded or substituted. Acquisition state is inherited
from the Phase 2 receipts; Phase 3 independently verifies retained revisions.

Two full preliminary runs used `artifacts/gkg-phase3-run1` and `run2`. A subsequent
resource-allocation fix warranted two more independent full runs, `run3` and
`run4`, using final implementation `97798e2`. All four outputs remain intact.
The two final runs were separate offline processes and output directories; their
semantic results also match all 96 preliminary results. No failed sample was
removed. Python 3.12.14, standard library only; no live source calls in replay.

## Results

| Metric | Final result |
| --- | ---: |
| Scheduled batches | 96 |
| Prior acquisitions passed | 96 |
| Archive SHA-256/size matches acquisition | 96 |
| Complete archive/member integrity verified | 96 |
| Physical rows | 118,420 |
| Accepted rows | 118,415 |
| Quarantined rows | 5 |
| Quarantine percentage | 0.0042222598% |
| Quarantine category | 5 quarantined_encoding |
| Affected batches | 4 |
| Clean batches | 92 |
| Batches accepted with quarantine | 4 |
| Rejected batches | 0 |
| Independent final replay matches | 96/96 |
| Raw source hash consistency | 96/96 |
| Recomputed semantic hash consistency | 96/96 |
| Duplicate archives / expanded members | 0 / 0 |
| Unexpected exceptions | 0 |

All five known Phase 2 invalid spans matched exactly by batch, physical line,
expanded byte offset and hex bytes. Phase 3 accounts for 5,708 additional accepted
rows from the four previously rejected strict scans: 118,415 versus Phase 2's
112,707 complete-scan accepted rows. This is safe partial syntactic acceptance
under a new explicit policy, not a revision of the original Phase 2 result.

## Encoding evidence and documentation

[Detailed research](GKG_ENCODING_EVIDENCE.md) separates provider documentation,
observed bytes, engineering policy and unknowns. The
[GKG 2.1 codebook](https://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)
specifies tab-delimited records and the XML extension field. The
[2016 metadata announcement](https://blog.gdeltproject.org/new-gkg-2-0-article-metadata-fields/)
explains last-column extracted metadata and AMP URLs. No authoritative whole-file
encoding guarantee or explanation of these particular malformed rows was located.
A statement about escaped author names does not establish an AMP URL codec.
Other GDELT products' encoding policies are not imported into this feed.

Every invalid span below is in **field 27, inside PAGE_ALTURL_AMP**. This is a
byte-level observation; the cause and intended characters remain unknown.

| Archive batch | Member line | Raw row range [start,end) | Invalid member byte offset | Hex |
| --- | ---: | --- | ---: | --- |
| 20260904063000 | 96 | [1250200,1256794) | 1256654 | f1 |
| 20260904113000 | 427 | [5487096,5501095) | 5500933 | f1 |
| 20260904141500 | 560 | [7259891,7270535) | 7270358 | e4 |
| 20230905180000 | 76 | [1032130,1042017) | 1041911 | a0 |
| 20230905180000 | 173 | [2167618,2177500) | 2177394 | a0 |

Member names are the batch ID plus `.gkg.csv`. Complete archive hashes, row hashes,
row IDs, parser/schema versions, source URLs and exact base64 bytes are in
[quarantine.json](../studies/gkg-lossless-v1/results/quarantine.json).
The five raw rows total **51,006 bytes**. Nothing was replacement-decoded,
transcoded, stripped or silently repaired; no alternate codec was admitted.

## Architecture, states and partial acceptance

[Contracts](GKG_LOSSLESS_CONTRACTS.md) define accepted, quarantined_encoding,
quarantined_schema, quarantined_timestamp, quarantined_resource and
quarantined_other. Each physical row has a deterministic ID, archive/member
reference, contiguous byte locator, raw SHA-256 and explicit disposition.
Quarantine embeds the entire original row. Accepted rows have a decoded field-vector
hash and raw locator; all original fields remain in the retained source archives.
No normalized observation database or field semantics is created in this phase.

Archive bytes are captured once and pinned to the Phase 2 SHA-256 and size. ZIP
CRC verification, member hashing, parsing and quarantine derive from that same
immutable snapshot. Complete member verification precedes releasing any row.
Source replacement after reading cannot affect it; replacement/truncation before
a later read fails the expected hash. Hard-link mutation is tested locally and
symlink switching is tested on Linux CI. Output directories must be new and
disjoint from inputs; exclusive creation prevents overwriting existing evidence.

Structural, encoding, timestamp and bounded row-resource failures allow other
independently valid rows to remain eligible. All repeated record IDs in a batch
are quarantined, not just later duplicates. Wrong archive revision/member, CRC
failure, unsupported/encrypted ZIP, whole-batch resource failure and unexpected
exceptions reject the batch with zero accepted rows. Cross-batch duplicate archive
or member hashes block corpus admission pending resolution.

A batch with quarantine is explicitly parse_with_quarantine, never clean_parse.
Downstream consumers must retain batch quality, accepted/quarantined counts and
fraction and must not treat an incomplete batch as complete. An all-quarantined
batch is rejected. A pre-accounting archive failure has no certified row ledger;
zero accounted rows is not a claim that its source contains no physical rows.
No downstream indicator currently consumes these results.

## Promotion gates and reproducibility

The [preregistered protocol](GKG_PHASE_3_PROTOCOL.md) established the gates before
corpus evaluation. No quarantine percentage threshold was tuned to make five rows
pass. Gates require exact sample/acquisition identity; complete archive integrity;
no duplicate batches; complete disposition and cryptographic provenance; two
independent semantic replays; mutation/failure regression coverage; transparent
batch usability; zero unexpected corpus exceptions; and quarantine containment
of encoding ambiguity. All gates pass in
[assessment.json](../studies/gkg-lossless-v1/results/assessment.json).

Replay revalidates whole batch fingerprints and accounting instead of trusting
success flags. Contradictory hashes or missing failure codes fail the gate. Batch
semantic hashes include all row ledgers, quarantine bytes, reasons, counters and
versions. Only execution clocks are excluded from run/replay semantic comparison;
acquisition clocks are retained separately in provenance receipts. Manifest,
Phase 2 evidence and code/schema hashes remain bound to the result.

Final replay semantic SHA-256: `92936274e7ae98eb25c29905196c817e70e4403122baff795f9fd2318be76c51`.
Full ledgers and exact source snapshots remain local; compact publications alone
cannot recompute a full-ledger hash. The original 96 ZIPs remain unchanged.

## Offline tests and CI

Baseline: 75/75 passed. Final local suite: **111 run, 110 passed, 0 failed,
0 errors, 1 skipped** in 3.821 seconds. The skip is Windows inability to create a
symlink, recorded explicitly in [tests.json](../studies/gkg-lossless-v1/results/tests.json).
Hard-link mutation, replacement, truncation and all other local regressions pass.

GitHub Actions on Ubuntu for `97798e2`: **111/111 tests passed, no skips**, including
the symlink-switch test. Verified
[push run 33998854547](https://github.com/edwardsage419/Psychohistory/actions/runs/33998854547)
and [PR run 33998856519](https://github.com/edwardsage419/Psychohistory/actions/runs/33998856519)
are successful. [CI evidence](../studies/gkg-lossless-v1/results/ci.json) records
commit, job, URLs and test log excerpts. Normal CI remains entirely offline.

The 36 added tests cover malformed UTF-8 in several fields, row/schema/timestamp
failures, duplicate rows/batches, deterministic IDs, byte preservation, source
mutation, semantic contradictions, missing codes, symlinks/hard links, resource
limits, collisions, unexpected exceptions, replay, schema and storage measurements.
No network request is required by tests. Two bounded provider-document downloads
were research activities, not CI tests or new data acquisitions.

## Near-zero-cost impact and measured storage

The project-wide principle now reads:

> Default to zero or near-zero recurring infrastructure cost. Paid infrastructure should be introduced only when a free approach materially harms data integrity, reproducibility, reliability, analytical quality, or product capability, and the benefit is supported by evidence.

[Architecture](ARCHITECTURE.md), [decisions](DECISIONS.md) and
[retention design](GKG_RETENTION_POLICY.md) record it. No recurring service,
paid API/database/object store, destructive cleanup or sampling/field reduction
was introduced. The 96-batch research corpus is intact and exempt from any future
ordinary raw-expiration policy.

[storage.json](../studies/gkg-lossless-v1/results/storage.json) measures canonical
UTF-8 JSONL logical payloads, distinct from pretty-printed publication wrappers:

| Storage class | Measured 96-batch bytes | Recent-based bytes/day | Bytes/30 days | Bytes/365 days |
| --- | ---: | ---: | ---: | ---: |
| Raw ZIP archives | 494,483,985 | 449,313,185 | 13,479,395,560 | 163,999,312,647 |
| Permanent quarantine evidence | 72,355 | 59,024 | 1,770,720 | 21,543,760 |
| Derived accepted-row ledgers | 89,144,276 | 79,439,964 | 2,383,198,920 | 28,995,586,860 |
| Manifest/provenance records | 75,004 | 74,784 | 2,243,520 | 27,296,160 |
| Normalized field-value records | Not created | Unknown | Unknown | Unknown |

The recent basis is only 72 batches/18 hours. Daily/monthly/yearly columns are
**extrapolations**, not observed full periods, statistical bounds or guaranteed
capacity. Permanent quarantine plus receipts extrapolate to about **48.84 MB/year**
of logical record payload in this sample; raw ZIPs to about **164 GB/year** and
accepted-row ledgers to **29 GB/year**. Future quarantine rates may be different.
Code, schemas, report wrappers, normalized values, indexes, backups and Git history
are additional and are not silently included. No compression ratio is assumed.

One complete local batch-ledger run occupies 89,297,849 bytes; four retained runs
use 357,191,396 bytes, separate from the raw corpus and ancillary reports. The
committed quarantine JSON is about 74 KB and receipt JSON about 81 KB. Compact
permanent evidence fits Git review; large generated ledgers fit local storage.
SQLite/DuckDB/Parquet and free execution remain compatibility targets, not selected
infrastructure or promised unlimited capacity.

Future ordinary raw retention may be configurable only after a separate recovery
and analytical-quality study. A URL/hash is a verifiable reference, not a backup
or guarantee of re-download. Without raw bytes, full accepted-row replay may be
unavailable; field hashes cannot reconstruct values. Exact quarantined rows remain
independently inspectable because their bytes are embedded, although re-verifying
membership requires the original archive. Normally retained normalized values
will need a concrete measured layout in a later phase. No deletion is implemented.

## Protected scope and unresolved risks

All six protected files remain byte-identical to `eabba6a` (and Phase 2 baseline
`5544bb9`): app.js, index.html, style.css, data/gdelt.json,
scripts/update_gdelt.py and .github/workflows/update-gdelt.yml. Phase 2 outputs and
its 96 raw archives are unchanged. Git diff whitespace checks pass. No main merge,
production ingestion activation, theme mapping, prediction model or dashboard
migration occurred.

Unknowns remain: intended source encoding and cause of AMP anomalies; future
remote revision/retention behavior; unsampled historical gaps; sustained
operational availability and free-execution capacity; multilingual coverage;
article-level cross-batch duplication; and analytical meaning of accepted opaque
fields. The parser is bounded but materializes a whole member, so large-limit
memory behavior deserves measurement before sustained scheduling. Local backup
is not configured; near-zero service cost does not remove disk-failure risk.
Quarantine statistics from one convenience corpus are not a future quality SLA.

## Recommendation and next issue

**promote_to_ingestion_candidate** is justified for the limited foundation:
all archives and row dispositions are traceable, invalid rows stay lossless and
visible, valid rows are independently verifiable, and replay plus mutation tests
pass. GKG themes are **not** validated as Psychohistory indicators. The source
registry remains candidate, with no automatic production activation.

Next recommended issue: **Local durable ingestion candidate and retention/recovery
study**. Evaluate an idempotent lightweight full-field storage layout, transactions,
batch quality joins, restart/recovery and source revision handling; measure memory,
disk and free-execution costs; test retrieval of pinned revisions and design a
configurable retention policy without deleting this research corpus. Any proposed
sampling/field/coverage reduction requires separate evidence. Keep theme semantics,
indicators and production dashboard migration out of that issue.

## Evidence and local reproduction

Committed artifacts under studies/gkg-lossless-v1/results include study, replay,
quarantine, acquisition provenance, storage profile, assessment, tests, CI,
source-document hashes and execution metadata. Final local roots are
artifacts/gkg-phase3-run3, artifacts/gkg-phase3-run4 and
artifacts/gkg-phase3-final. Earlier runs and source-documents remain under their
original directories. See GKG_LOSSLESS_CONTRACTS.md for CLI instructions and
GKG_RETENTION_POLICY.md for preservation requirements. Choose a new output root
for any additional replay; never overwrite the original corpus or run identities.
