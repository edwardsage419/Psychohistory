# GKG study machine-readable contracts

All schemas use JSON Schema 2020-12 and the repository's standard-library subset
validator. Schema version 1.0.0 is independent of study and validator code versions.
`study_contracts.check_publication` adds exact sample identity, manifest hash,
acquisition denominator and replay consistency checks. Tests are always offline.

## Manifest: gkg-study-manifest.v1.schema.json

`studies/gkg-continuity-v1/manifest.json` records study_id and exactly 96 entries,
each with a unique quarter-hour batch_id, cohort and matching HTTPS source URL.
The runner also enforces calendar validity, exact 96-entry count and no duplicates.
The SHA-256 of sorted compact UTF-8 manifest JSON identifies this exact sample,
not the formatting of the manifest file. Wrong shape/version/URL is rejected.
Availability is not inferred from the manifest; each entry is a scheduled probe.

## Study: gkg-study.v1.schema.json

`study.json` has manifest identity, run metadata, one ordered entry per scheduled
slot, summary and finish/checkpoint time. Run metadata includes Python/platform,
policy, timeout, size bound, study/validator versions and exact source-code byte
hashes. `finished_at` is a checkpoint timestamp until no pending slots remain.

Entries include batch_id/cohort/url, state, acquisition status, retrieval times,
download and processing durations, HTTP status/effective URL/headers, relative raw
path, archive SHA-256/byte length, analysis, replay and errors. A successful GET
is distinct from valid content. Acquisition may pass while parsing or persistence
fails. Download duration includes failed requests; processing duration includes
raw persistence plus both validation/integrity passes. Neither measures provider
publication latency. Stored response headers are observations, not availability
promises. HTTP redirects outside GDELT HTTPS batch addresses fail closed.

`analysis.validation` derives from the Issue 2 deterministic ZIP report, with full
statistics retained locally. Published compact records replace each theme_counts
map with distinct_theme_tokens and its canonical JSON SHA-256. The study summary
retains aggregate literal theme counts for complete scans. Full per-batch maps
remain in local attempts/*.json and can be reproduced from raw ZIPs. Partial scans
remain visible in per-batch counts but are excluded from aggregate distributions.

`analysis.integrity` independently streams the archive, checks CRC and hashes the
expanded member. This distinguishes invalid UTF-8 inside an intact ZIP from ZIP
corruption. Status is passed, failed or not_checked; content_sha256 is null unless
all expanded bytes were checked within limits. Both ZIP and expanded-member hash
groups detect duplicate payloads across scheduled slots; slots are never dropped.

Timestamp consistency compares member basename and valid-row date distribution
to batch_id. Unknown date sentinel rows are counted explicitly. Comparisons on a
partial scan are incomplete; no claim about unread rows or document publication
accuracy is made. Record-ID timestamp prefixes are not separately checked.

Replay contains two raw hashes, two semantic hashes, flags for agreement and
matching acquisition, and status. Semantic input is the complete deterministic
analysis (validator version, archive bytes/hash, member metadata, all counters,
validation errors, independent integrity and timestamp metrics). Run clocks,
references external to batch identity and durations are outside that comparison.
Stable hashes use compact sorted UTF-8 JSON; reports use readable sorted JSON.

Summary counts keep acquisition, parsing, integrity, complete scans and replay
separate. acquisition_success_rate = acquired / all 96 scheduled slots, including
pending/unavailable slots in the denominator. acquisition_failed counts completed
failed acquisitions; interruptions/pending are separate, not silently failures or
successes. failure_batches_by_code counts each code once per batch (categories may
overlap). Raw/unavailable/duplicate ID lists are explicit. Empty-theme fraction
uses valid rows in complete scans. Row rejections on partial scans must be read
from per-batch evidence and are not silently folded into complete-scan statistics.

Storage_by_cohort contains measured total/min/max/mean compressed bytes of complete
responses, including acquired archives later rejected by the parser. Missing
acquisitions are excluded and the sample denominator is recorded. Per-day,
30-day and 365-day values are extrapolations: mean * 96 * days. They are not
measurements of those periods or confidence intervals. Empty cohorts yield null
estimates. Partial response bodies never enter size estimates as full archives.

## Replay: gkg-study-replay.v1.schema.json

`replay.json` is a new offline read of all stored archives after acquisition.
Each scheduled slot gets passed, failed or not_available. Passing requires two
matching raw hashes, two matching semantic hashes and equality with the original
stored analysis. Repeatable invalid input can pass replay while failing parsing.
Absent/corrupt raw data and changed analysis are explicit failures. This establishes
local deterministic validation, not that future remote downloads are immutable.

## Diagnostics: gkg-encoding-diagnostics.v1.schema.json

`encoding-diagnostics.json` examines only encoding-failed study batches, with their
original raw hash checked first. It counts physical lines and tab-delimited fields
without repairing text; strict UTF-8 failures record up to 100 samples of line
number, uncompressed byte offset, field number, invalid byte hex and decoder reason.
The count is affected lines, not invalid byte occurrences. samples_truncated signals
capped evidence. Failed diagnostics have a coded error instead of invented counts.
This evidence is not an alternate production parser or normalized dataset.

## Failure taxonomy and execution

* HTTP 404/410: unavailable; other HTTP failures: http_error with status code.
* TLS, socket/HTTP protocol failures: tls_error or network_error.
* Redirect downgrade/provider change: unsafe_redirect.
* Invalid/truncated/oversized responses: invalid_content_length,
  truncated_response, resource_limit; other unexpected status is explicit.
* Persistence failure/corruption: io_error or raw_cache_corrupt.
* Validator errors retain Issue 2 codes, including invalid_encoding, invalid_zip,
  invalid_rows and resource_limit; independent integrity failure adds a code.
* Timestamp mismatch and replay mismatch remain separate from transport success.
* Interrupted attempts are persisted as interrupted; resume never silently retries.
* Invalid manifest, resume mismatch and report I/O errors produce JSON on stderr.

CLI acquisition exits 0 only if all scheduled entries complete without errors;
2 means recorded batch failures; 3 means a study-level failure. Replay exits 0
only when all 96 pass, 2 for nonpassing/missing results. PowerShell may map a
native nonzero code to shell exit 1; use LASTEXITCODE to inspect native exit codes.
A killed process or a disk unable to store a report cannot guarantee a final
artifact. Started attempt records support identifying interrupted work on resume.
No retry is automatic; a new acquisition directory defines a separate new attempt
set and must not replace the original study evidence.

```sh
python -B scripts/study_gkg.py --integration --root artifacts/gkg-study-96-v1
python -B artifacts/gkg-study-96-v1/source-code/study_gkg.py --manifest studies/gkg-continuity-v1/manifest.json --replay --root artifacts/gkg-study-96-v1
python -B scripts/diagnose_gkg_encoding.py --root artifacts/gkg-study-96-v1
python -B -m unittest discover -s scripts -p 'test_*.py' -v
```

Source-document probe evidence is a JSON array with requested/effective URL,
retrieval time, HTTP status/length/range, saved-prefix size/hash, truncation flag
and any errors. It records bounded research requests, outside the 96-batch
acquisition denominator. The master index capture is only a 65,536-byte range,
not a full index hash, even when truncated_to_limit is false (the server honored
the Range request). HTML/index snapshots remain local under source-documents/.

## Raw retention and portable replay

All 96 response bodies, including failed parsing inputs, are retained under
`artifacts/gkg-study-96-v1/raw/<sha256>.zip` (ignored by Git). Full attempts,
run metadata, source-document snapshots and exact source-code copies accompany
them. No archives are discarded. Measured compressed total is about 494 MB;
committing binary raw inputs would bloat permanent Git history. Commit compact
study/replay/diagnostic JSON and keep this local evidence directory intact.

Back up or copy the entire directory to another local disk before cleanup; no
external storage/account is configured and no remote backup is claimed. The
user retains responsibility for long-term backup until a storage policy is approved.
To replay elsewhere, copy this directory and the committed manifest, preserve
source-code/study_gkg.py and source-code/validate_gkg.py byte-for-byte, and run:

```sh
python -B source-code/study_gkg.py --manifest /path/to/manifest.json --replay --root /path/to/evidence-directory
```

Explicit manifest is necessary when using the source snapshot. Code hashes include
line endings; using exact snapshots avoids platform Git newline conversions.
Raw payload hashes and stable semantic comparisons exclude filesystem paths and
runtime clocks. Re-downloading a source URL without saved bytes is weaker evidence;
verify the expected SHA-256 and keep any changed remote payload as a new revision.

Data source: [The GDELT Project](https://www.gdeltproject.org/). Attribution and link
must accompany use or redistribution under its published terms. Source article
rights are not automatically conveyed by metadata access.

## Assessment v1

`results/assessment.json` is a human-reviewed decision record with schema_version,
study/manifest identity, one of the three permitted recommendations, measured
counts, Boolean preregistered gate outcomes, blocking reason, scope limitations
and the next issue. It is not generated by an automatic promotion rule and does
not mutate the source registry's production status. Fields describe this study;
changing a decision requires new evidence and an explicit review record.
