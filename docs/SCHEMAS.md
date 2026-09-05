# Versioned data contracts

## Validation report v1.0.0

`schemas/validation-report.v1.schema.json` is the machine-readable JSON Schema
2020-12 contract. `scripts/contracts.py` enforces its small documented subset
using the standard library, plus count/status invariants. Unknown keywords and
unknown object fields fail closed. It is not a general JSON Schema engine.
ContractError exposes `path` and `code`. Schema changes affecting meaning need a
new version; consumers must reject unknown versions.

The report records validator version, UTC validation time, source reference,
ZIP SHA-256 and size, member metadata, raw discovery line/metadata SHA-256,
provider size/MD5, status, statistics and structured errors (code/stage/message).
SHA-256 identifies exact acquired bytes; provider MD5 is an integrity comparison,
not an authenticity guarantee. Source references are retained as discovered.
`--url` bypasses discovery, so discovery metadata is null rather than fabricated.

`statistics.complete` means the entire member was read successfully, including
CRC verification. A complete scan can still fail row validation. On incomplete
scans counts are partial diagnostics and must not enter indicators. `rows` counts
decoded physical lines; `valid_rows + bad_rows = rows`. Undecodable/unread bytes
are not counted. Blank lines fail field count. Exactly 27 tab-separated columns
are required; final empty columns are preserved and quotes are literal characters.
Only structure, dates, record ID presence/uniqueness and theme frequencies are
checked; passing does not certify every field's semantics.

Date `0` is a documented unknown sentinel and counted separately. Other dates
must be 14 ASCII digits and valid calendar times. Empty theme fields are valid.
Theme counts are **valid rows containing each literal V1THEMES token**, deduplicated
within a row; empty tokens are ignored and whitespace/case are preserved. Counts
are not event counts or percentages of all world news. All codes and dates are
retained, not a top-N subset. No theme meaning or production mapping is assigned.

Errors enumerate metadata, transport, local I/O, ZIP, encoding, resource, row,
argument and report-write failures. Row rejection reasons appear as counts;
a row can have multiple reasons. Exit 0 = structurally passed, 2 = acquisition or
configuration failure, 3 = validation failure, 4 = report write failure (JSON on
stderr). Invalid CLI syntax uses argparse's standard exit 2 before an acquisition
attempt. Atomic report replacement prevents a prior success artifact from being
mistaken for a completed failed attempt. A killed process or full/unwritable disk
cannot guarantee an artifact; workflow failure remains the signal in that case.

Limits: 64 MiB ZIP, 512 MiB expanded member, 8 MiB physical line, 1 MiB discovery,
60-second socket timeout. These are initial validator guardrails, not measured
provider maxima. Counters and duplicate IDs use memory bounded by accepted input.
No archive is extracted. Empty/multiple data members, encryption, unexpected
member suffix, corruption and invalid UTF-8 fail closed.

`validate_zip` is deterministic for identical bytes. `run_validation` is deterministic
for identical bytes, references and supplied `run_at`; real acquisition timestamps
naturally differ. Canonical sorted JSON uses UTF-8, LF, no NaN, and a final newline.

Offline: `python -B -m unittest discover -s scripts -p 'test_*.py' -v`.
Replay: `python -B scripts/validate_gkg.py --input batch.zip --output report.json`.
Live: `python -B scripts/validate_gkg.py --integration [--url GKG_URL]`.
The misleading old `--date` and display-only `--top-themes` options are removed.
The report replaces V0.2.1-A's unversioned shape; only validation artifact consumers
need migration. The dashboard reads no validation reports and is unchanged.

## Source registry v1.0.0

`schemas/source-registry.v1.schema.json` describes a registry envelope containing
unique source IDs and `registry/sources.v1.json` is its initial candidate entry.
Required notes cover access, documentation, usage rights, cadence, geographic and
historical coverage, reliability, biases and cost. Unknown facts are explicitly
marked `unknown` in notes; unknown source version is null. Production status is
candidate, production, rejected or retired. Status changes require evidence;
passing a contract does not authorize promotion. This is a research registry,
not an ingestion adapter, and it does not alter the legacy dashboard sources.

## Normalized numeric observation v1.0.0

`schemas/observation.v1.schema.json` is an initial scalar numeric observation
contract. It is source-independent and has no seven-topic enum. Each observation
requires source ID/version, metric ID, observation and retrieval time, finite
numeric value (or null), explicit unit, geography/entity scope, quality status
and note, exact source record reference, snapshot SHA-256 and transformation
version. A scope is a `scheme`/`code` pair so FIPS, ISO or another explicitly named
scheme cannot be silently conflated. Unknown geography/entity/time/version is
null; unknown geography is never silently converted to worldwide coverage.
`observed_at` reflects the metric's documented time semantics, not automatically
an event time. Retrieval time must have a timezone. No production metric is
introduced by this contract; adapters must document metric semantics separately.

`missing` requires null value and nonmissing values require valid/suspect quality.
Zero is a real value. NaN, infinity, booleans-as-numbers, missing provenance,
unknown fields and unknown schema versions are rejected. Missing source/time or
scope knowledge must be explained in quality_note; quality remains an explicit
adapter judgment, not inferred from numerical magnitude. Registry referential
integrity must be checked by the eventual ingestion transaction.

`observation_id` is SHA-256 of sorted compact UTF-8 JSON of all fields except
observation_id and retrieved_at. `observation_id()` computes it and validation
checks it. Re-fetching identical facts preserves identity; value/provenance/
transformation/quality changes produce a distinct revision. This is content
identity, not an upsert/database implementation. Integer 1 and float 1.0 have
different serialized identities; adapters must choose a stable numeric form.
Preserve all retrieval attempts in run metadata when persistence is implemented.
No observations or theme mappings are written to production in this phase.

### Validator 1.0.1 self-review corrections

The report schema remains v1.0.0. Oversized local inputs leave zip_bytes/sha256
null because only a bounded prefix was read. Discovery size tokens longer than
20 digits are rejected as metadata_invalid before numeric conversion. Report
output must not resolve to the input archive (including hard-link aliases);
rejected writes return exit 4 with JSON on stderr and leave source bytes intact.
Timezone offsets require hours 00–23 and minutes 00–59; Python's normalization of
out-of-range offset minutes is not accepted as input validation.

## Continuity study contracts

The separate v1 study manifest, results, replay and byte-diagnostic contracts are
documented in [GKG_STUDY_SCHEMA.md](GKG_STUDY_SCHEMA.md). They do not change the
observation or dashboard contracts. Phase 2 keeps source production status candidate.
