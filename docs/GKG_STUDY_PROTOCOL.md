# Phase 2 GKG study protocol (preregistered)

Baseline: 5544bb9; branch codex/project-reset-architecture. This phase follows the
user's continuity-study scope; ROADMAP's old Phase 2 indicator work is deferred.
AGENTS.md, all docs (including retained evidence), and Issue 2/self-review report
were read before study changes. Baseline: 45 offline tests pass.

## Exact sample: 96 distinct scheduled batch addresses

* recent: 72 consecutive 15-minute slots, 2026-09-04 00:00 through 17:45 UTC.
* historical_2015: 2015-03-02 00:00, 00:15, 00:30, 00:45 UTC.
* historical_2016: 2016-09-05 06:00, 06:15, 06:30, 06:45 UTC.
* historical_2020: 2020-09-05 12:00, 12:15, 12:30, 12:45 UTC.
* historical_2023: 2023-09-05 18:00, 18:15, 18:30, 18:45 UTC.
* historical_2025: 2025-09-05 00:00, 00:15, 00:30, 00:45 UTC.
* historical_2026: 2026-08-05 12:00, 12:15, 12:30, 12:45 UTC.

The explicit machine-readable manifest is authoritative. Sample fixed before
acquisition; no availability-based substitutions. URLs are candidate addresses
`https://data.gdeltproject.org/gdeltv2/YYYYMMDDHHMMSS.gkg.csv.zip`.
Existence of each address is an empirical question. Older sparse windows do not
establish availability between them. The recent window covers 18 hours, not a
full day; extrapolations must expose time-of-day/weekday/season biases.

## Method and bounds

One sequential HTTPS GET per slot, no automatic retry or HTTP downgrade. Timeout
and limits are recorded. All HTTP codes, missing slots, TLS/network, size, ZIP,
parsing, persistence and replay failures remain in results. A rerun resumes
completed attempt records; retry requires a new run directory and cannot replace
original evidence. The runner does not fetch linked publisher articles.

Retain all complete response bodies (even malformed archives) locally under
ignored artifacts/gkg-study-96-v1/raw/ using content SHA-256 filenames. Partial
responses are not claimed as archives. Maximum 64 MiB response and 512 MiB expanded
member; study budget at most 96 * 64 MiB raw plus reports. Raw data is unsuitable
for Git history; commit the manifest, compact per-batch results, stable semantic
hashes and aggregate literal token frequencies. Document local backup/replay
strategy. No implicit cleanup of raw data.

Read each stored archive independently twice through the existing validator.
Compare entire deterministic validation output (all frequency counts, errors,
member metadata, source hash/size) plus batch consistency metrics. Exclude
acquisition/run clocks and measured durations; store both semantic hashes and
explicit comparison flags. Rehash stored raw bytes against acquisition SHA-256.
Check member filename and row-date distribution against expected timestamp;
unknown dates and mismatches remain explicit. A passing replay of invalid data
means repeatable rejection, not valid data. Detect identical archive hashes
across distinct scheduled slots without dropping them from denominators.

Report acquisition / complete scans / valid parsing / replay separately. Aggregate
only complete scans for distribution and theme summaries; retain partial counts
per batch for diagnosis. Storage estimates use measured response sizes only,
separately for recent and historical cohorts, with 96 batches/day, 30-day months
and 365-day years explicitly labeled extrapolations. No estimates from failed
or partial transfers; report sample counts, min/max and means.

## Decision gates

Promotion means permission to design a durable ingestion candidate, not production
launch. Consider promotion only if >=95% (at least 92/96) complete acquisitions,
all acquired archives pass integrity/structure/replay, timestamps have no unexplained
mismatch, no unexplained duplicate batches, and every historical window has a
successful retrieval. Also require measured feasible storage and verified provider
usage terms. Unresolved material issues imply continue_validation. Reject as
primary source only if evidence shows a fundamental unworkable access/rights or
quality limitation; local transient network failure alone is not such evidence.
Thresholds are engineering gates for this bounded study, not an SLA or statistical
proof of long-term reliability. No automatic promotion logic writes production.

## Acceptance and risks

Every one of 96 manifest slots is represented exactly once, all attempts and
missingness visible, raw source references and hashes preserved, deterministic
replay validated, offline tests cover normal and failed paths, and final report
contains historical/HTTPS/usage evidence, storage estimates and next issue.
The original dashboard, data JSON, DOC updater and production workflow remain
byte-identical. No mappings, indicators, models, paid services or main merge.
Risks: archived files may be unavailable, size guards may reject real batches,
local HTTP behavior may differ from Actions, and convenience sampling limits
inference. Record unknown facts; do not invent missing files or field meanings.
