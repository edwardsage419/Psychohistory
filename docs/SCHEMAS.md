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
