# Phase 2 final report: GKG continuity and historical acquisition

Recommendation: **continue_validation**. All 96 addresses were acquired over
HTTPS and all archives passed integrity and replay, but four intact archives fail
strict UTF-8 parsing. This is an encoding/ingestion-policy blocker, not a reason
to reject the entire source. No source was promoted and no production data changed.

Baseline: `5544bb9`, branch `codex/project-reset-architecture`. The user's Phase 2
means this acquisition study; indicator research from the original roadmap remains
deferred. Protocol and manifest were committed in `9d21bc3` before downloads;
runner implementation and 68 passing offline tests in `8b9d658` preceded the study.

Data source: [The GDELT Project](https://www.gdeltproject.org/).

## Exact 96-batch sample

Authoritative [manifest](../studies/gkg-continuity-v1/manifest.json), canonical
SHA-256 `443f60269a89251655b0636799988e15034b55a8ceb58ffea57c8d236bf2ef15`.
All intervals below are inclusive UTC quarter-hour timestamps.

| Cohort | Sample window | Distinct batches | Acquired | Strict parsing passed |
| --- | --- | ---: | ---: | ---: |
| recent | 2026-09-04 00:00–17:45, every 15 minutes | 72 | 72 | 69 |
| historical_2015 | 2015-03-02 00:00–00:45 | 4 | 4 | 4 |
| historical_2016 | 2016-09-05 06:00–06:45 | 4 | 4 | 4 |
| historical_2020 | 2020-09-05 12:00–12:45 | 4 | 4 | 4 |
| historical_2023 | 2023-09-05 18:00–18:45 | 4 | 4 | 3 |
| historical_2025 | 2025-09-05 00:00–00:45 | 4 | 4 | 4 |
| historical_2026 | 2026-08-05 12:00–12:45 | 4 | 4 | 4 |
| Total | 72 recent + 24 older | **96** | **96** | **92** |

This is one 18-hour continuity window and six one-hour historical windows, not
96 consecutive recent batches or a multiyear continuity census. No failed address
was replaced. No additional GKG batches were downloaded outside this manifest.
Three bounded documentation/index requests are separately recorded and excluded
from acquisition denominators.

## Execution and results

Run: `2026-09-05T22:39:58Z` to `2026-09-05T22:42:38Z` (September 6 local time),
Python 3.12.14 on Windows. One sequential GET per slot, no retry, credentials,
HTTP fallback or paid service. Effective URLs remained HTTPS for **96/96**; no
redirects. HTTP **200** for every archive. Content-Length agreed with downloaded
bytes. Total wall-clock approximately 160 seconds; measured summed download time
95.944 seconds, summed processing/persistence/two-pass validation 52.249 seconds.
Median/max download duration: 0.885/2.007 seconds; processing: 0.521/1.107 seconds.
These are local processing measurements, not provider publication-lag metrics.

| Metric | Result |
| --- | --- |
| Acquisition success | **96/96 = 100%**, 0 failed, 0 unattempted/interrupted |
| Missing/unavailable (HTTP 404/410) | **0** among sampled addresses |
| Archive integrity | **96/96** passed full expanded-byte CRC checks |
| Strict parsing success | **92/96 = 95.83%**; **4/96 = 4.17%** encoding failures |
| Complete strict scans | **92** |
| Valid rows in complete scans | **112,707** |
| Row-level field/date/ID rejections in those scans | **0** |
| Field-count stability | **112,707/112,707** complete-scan rows have 27 fields |
| Unknown dates | **0** in checked validator rows |
| Timestamp/member-name mismatches | **0 detected**; date comparison covers valid rows actually read |
| Duplicate ZIP hashes | **0** across 96 scheduled slots |
| Duplicate expanded-member hashes | **0** |
| Two-pass stored-input replay | **96/96 equal raw hashes and full semantic outputs** |
| Separate subsequent offline replay | **96/96 matched original analysis** |

A deterministic rejection passes replay without passing parsing. The four failed
strict scans have partial counters (1,155 decoded rows in total); those counters
are retained per batch but excluded from complete-scan distribution summaries.
Dates in the unread remainder are not certified. No full-batch success is inferred
from partial rows.

## Failure taxonomy and byte-level diagnosis

Observed failure category: **invalid_encoding**, 4 batches. Other exercised
categories (HTTP unavailable, rate/server errors, TLS/network, size/truncated
response, ZIP corruption, local persistence, interrupted attempts and replay
mismatch) had **0 occurrences in this run**; offline tests cover them. Categories
may overlap and are counted once per batch, separately from acquisition success.

[Diagnostic evidence](../studies/gkg-continuity-v1/results/encoding-diagnostics.json)
rehashes original archives and scans raw lines without replacement decoding:

| Batch | Total physical lines | UTF-8-rejected lines | First invalid bytes | Field |
| --- | ---: | ---: | --- | ---: |
| 20260904063000 | 925 | 1 | f1 | 27 |
| 20260904113000 | 1,025 | 1 | f1 | 27 |
| 20260904141500 | 1,402 | 1 | e4 | 27 |
| 20230905180000 | 2,361 | 2 | a0, a0 | 27 |

All 5,713 physical lines in these four archives have 27 tab-separated fields at
byte level. Combined with complete strict scans, **118,420 physical rows** were
counted, with **five UTF-8-invalid lines**. That does not certify the unvalidated
fields of those records. The remaining 5,708 lines in rejected batches are not
silently added to validated aggregates. Hex evidence, exact byte offsets and line
numbers are retained; the bytes were not repaired, mapped to an assumed codec,
or discarded. ZIP integrity passing rules out ZIP transport corruption detected
by CRC, but does not establish why the publisher emitted these bytes.

## Theme availability and schema findings

In 92 complete scans: **12,106/112,707 = 10.7411%** have empty V1THEMES;
100,601 rows have at least one token. Across these scans there are **9,836 distinct
literal tokens**. Per-complete-batch distinct counts range from **1,639 to 2,886**.
Counts are document-row presence (deduplicated within a row), not mentions/events,
and do not imply each row describes a distinct real-world occurrence.

| Cohort | Valid complete-scan rows | Empty-theme rows | Per-batch distinct token range |
| --- | ---: | ---: | --- |
| recent | 75,824 | 8,462 | 1,639–2,552 |
| historical_2015 | 6,662 | 753 | 1,796–1,926 |
| historical_2016 | 7,748 | 822 | 2,536–2,752 |
| historical_2020 | 3,494 | 331 | 1,813–2,092 |
| historical_2023 | 7,560 | 743 | 2,803–2,886 |
| historical_2025 | 6,084 | 557 | 2,144–2,417 |
| historical_2026 | 5,335 | 438 | 2,409–2,618 |

All aggregate literal frequencies are machine-readable in study.json. For example,
TAX_FNCACT occurs in 88,198 validated rows and EPU_POLICY in 39,433. These are
observations of strings, not semantic endorsements or Psychohistory mappings.
27-column stability does not establish stable extraction models, token meaning,
coverage or valid measurements of societal conditions. No final ontology is made.

## Historical acquisition and HTTPS evidence

The provider's [2015 launch/access announcement](https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/)
links separate English and Translingual master lists and describes 15-minute
updates. This study uses the **English master-list filename family**:
`https://data.gdeltproject.org/gdeltv2/YYYYMMDDHHMMSS.gkg.csv.zip`.
The Translingual feed and other GKG families are untested; results and volumes
must not be presented as all multilingual GKG coverage.

A bounded **65,536-byte** HTTPS Range read of
[masterfilelist.txt](https://data.gdeltproject.org/gdeltv2/masterfilelist.txt)
returned HTTP 206, range `0-65535/127354357`. Saved prefix hash and sample lines
are in [source-access evidence](../studies/gkg-continuity-v1/results/source-documents.json).
It contains size/MD5/URL entries such as `20150218230000.gkg.csv.zip`.
The prefix confirms the addressing convention; it is not a full-index census or
proof that every indexed address still exists. No index hash is claimed for the
entire 127,354,357-byte file.

All 24 selected older addresses were fetched successfully, earliest verified
**2015-03-02 00:00 UTC** and latest historical cohort **2026-08-05 12:45 UTC**.
No observed missing slot exists within the seven sampled windows. Availability
between windows, pre-2015 GKG 2.1 availability, full retention horizon, deletion
policy, revisions and future immutability remain **unknown**. The 2015 announcement
contains historical plans; they are not treated as proof those plans were fulfilled.
The index prefix advertises February 18 timestamps while the launch text discusses
February 19 availability; this study does not resolve the earliest production boundary.

## Usage terms and storage

The provider's [Terms of Use](https://www.gdeltproject.org/about.html#termsofuse),
retrieved for this study, permit use without fees and redistribution/rehosting
with attribution and a link to GDELT. This supports retaining the GDELT dataset
for this study. It does not transfer rights to publisher articles linked by the
metadata; this study downloaded no such articles. No specific standard license
identifier, SLA or guaranteed retention policy was verified. Saved HTML hashes
identify the terms inspected; re-check terms before a future redistribution product.

Measured across 96 archives: **494,483,985 compressed bytes** (494.484 MB decimal),
**1,535,272,154 expanded bytes** (1.535 GB); compressed files range from 2,887,763
to 10,518,491 bytes. All 96 raw ZIPs are preserved locally, including four rejected
inputs. Full attempts, exact source-code snapshots and source documents accompany
them at `artifacts/gkg-study-96-v1/`; only compact JSON is committed to avoid Git
binary-history growth. See [retention and replay instructions](GKG_STUDY_SCHEMA.md).
No external backup exists or is claimed.

Extrapolations below use measured mean ZIP bytes * 96 batches/day * 30 or 365 days.
Units are decimal GB. These are **scenario estimates**, not measured daily/monthly/
yearly volume or statistical confidence bounds. They exclude translated/other feeds,
indexes, normalized tables, retries, metadata, replicas and backups.

| Size basis | Samples | Measured sample GB | Estimated GB/day | GB/30 days | GB/365 days |
| --- | ---: | ---: | ---: | ---: | ---: |
| recent | 72 | 0.3370 | **0.4493** | **13.4794** | **163.9993** |
| historical_2015 | 4 | 0.0237 | 0.5690 | 17.0685 | 207.6671 |
| historical_2016 | 4 | 0.0311 | 0.7474 | 22.4233 | 272.8171 |
| historical_2020 | 4 | 0.0146 | 0.3511 | 10.5320 | 128.1395 |
| historical_2023 | 4 | 0.0402 | 0.9647 | 28.9414 | 352.1199 |
| historical_2025 | 4 | 0.0250 | 0.6005 | 18.0144 | 219.1755 |
| historical_2026 | 4 | 0.0228 | 0.5473 | 16.4197 | 199.7731 |

The recent window omits six hours and samples one weekday; historical windows
are only one hour each. Time-of-day, weekday, season and provider changes could
materially shift volumes. Approximately 164 GB/year for this sampled feed already
argues against raw archives in Git. The measured study fits local storage; no
long-term storage service or spending decision has been made.

## Reproducibility and machine-readable deliverables

* [study.json](../studies/gkg-continuity-v1/results/study.json): all 96 slot results,
  hashes, sizes, durations, failure codes, stable metrics and aggregate frequencies.
* [replay.json](../studies/gkg-continuity-v1/results/replay.json): 96 independently
  re-read raw/semantic comparisons matching original analyses.
* [encoding diagnostics](../studies/gkg-continuity-v1/results/encoding-diagnostics.json):
  five invalid lines with byte-level provenance.
* [assessment.json](../studies/gkg-continuity-v1/results/assessment.json): human-reviewed
  recommendation and measured gates; no automated production status change.
* [source-documents.json](../studies/gkg-continuity-v1/results/source-documents.json):
  access/terms/index capture metadata and partial-index scope.

Runtime timestamps and durations are outside semantic hashes. Full per-batch
frequency maps are local; their fingerprints and distinct counts are published.
Exact ZIP and expanded hashes detect identical payloads; this is not cross-batch
article/syndication deduplication. Local replay does not test remote mutation over
weeks or months. Code-byte hashes protect the original evaluator; source snapshots
preserve portability across differing Git newline settings.

## Tests and review

* Baseline: **45** offline tests passed.
* Runner group: **68** offline tests passed before the live study.
* Contracts/diagnostics group: **73** offline tests passed (recorded final group
  run: 1.266 seconds, exit 0).
* Explicit integration acquisition completed every slot and returned nonzero as
  intended for four recorded encoding failures (CLI policy exit 2; PowerShell
  command wrapper reported exit 1). No errors were hidden to obtain a green run.
* Separate `--replay` invocation: **96 passed**, native exit 0, no network.
* Actual study/replay/diagnostic JSON passed schema and semantic accounting checks.
* `git diff --check`: passed.
* All six protected frontend/data/updater/workflow files remain byte-identical to
  `5544bb9`. CI continues using offline unittest discovery; no scheduled study
  or production workflow changes were made. No merge to main.

## Recommendation and next issue

**continue_validation** follows the preregistered gate: acquisition, integrity,
historical windows, duplicate detection and replay passed, but not every acquired
archive passed strict structure/encoding validation. Five invalid lines are few,
but silently repairing them or certifying their whole batches would violate the
provenance rule. There is no evidence here to reject GKG as fundamentally unusable.
It is not yet justified to promote it to the first long-term ingestion candidate.

Next issue: **Lossless GKG encoding and row-quarantine policy**. Use this retained
96-batch corpus, investigate field-27 byte encoding against provider documentation,
design explicit per-row quarantine and lossless raw-byte provenance, and test full
batch accounting without replacement decoding. Compare usable-row coverage and
replay with the present strict baseline, document whether the English-only feed
meets the initial source scope, then revisit promotion. Do not introduce theme
mappings, indicators or production ingestion as part of that policy study.

Remaining risks: sparse retrospective convenience sample; no sustained availability
or Actions SLA; unexplained encoding anomalies; untested Translingual coverage;
unknown cross-batch document duplication; no verified complete historical index,
immutability or guaranteed retention; storage/backup plan not selected. These
unknowns are recorded rather than filled with fabricated assumptions.

## Post-study bug review (2026-09-06)

Three implementation defects were corrected after publication: offline replay now
records a replay_mismatch failure code when raw hashes disagree even if parsed
semantics agree; publication validation rejects inconsistent semantic hashes
marked as passed; encoding diagnostics parse the same in-memory bytes whose hash
was verified instead of reopening a potentially changed file. Regression coverage
includes all three cases. All 75 offline tests pass. Published study and replay
contracts pass the stricter checks, and re-diagnosis of all four retained encoding
failures exactly matches published results. The recommendation remains
continue_validation. Production files and original study evidence are unchanged.

The runner's code-byte hash changed, so original-run replay must use the retained
source-code snapshot (README commands updated). Do not rewrite run.json identity
to bypass the evaluator check. The patched runner is for new study directories.
