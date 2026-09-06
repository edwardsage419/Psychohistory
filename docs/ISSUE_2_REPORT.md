# Issue 2 final engineering report

Work branch: `codex/project-reset-architecture`.
Baseline: `cb2058ce20026e7617b6f5ac733cebdff90d9b20`.
Local checkout: `D:/GPT/Psychohistory-issue2` (the original workspace was an
unversioned snapshot, preserved unchanged). No merge to main was performed.

## Files changed and why

* `docs/REPOSITORY_AUDIT.md`: all 19 baseline files classified before code edits;
  validator defects, architecture conflicts, risks and unknowns recorded.
* `.gitignore`: exclude bytecode, caches, environments and transient reports.
* Delete both tracked `scripts/*.cpython-313.pyc` files and inactive root
  `update-gdelt.yml`; production workflow remains untouched.
* `scripts/validate_gkg.py`: bounded strict ZIP/UTF-8/27-column/date validation,
  record ID duplicate detection, missingness and literal theme presence counts,
  source/hash provenance, explicit integration opt-in and atomic failure reports.
* `scripts/test_validate_gkg.py`: replace single assertion fixture with 30
  deterministic unittest cases covering parsing, transport and reporting.
* `.github/workflows/validate-gkg.yml`: run offline suite, mark live acquisition
  explicitly integration scoped, upload artifacts with `always()`.
* `.github/workflows/test.yml`: read-only offline development branch/PR CI.
* `schemas/validation-report.v1.schema.json`, `schemas/source-registry.v1.schema.json`,
  `schemas/observation.v1.schema.json`: versioned machine-readable contracts.
* `scripts/contracts.py`: standard-library validation of supported schema subset
  and semantic invariants; deterministic observation identity.
* `scripts/test_contracts.py`: 11 tests for reports, registry and observations.
* `registry/sources.v1.json`: GKG candidate with explicit limitations and unknowns.
* `docs/SCHEMAS.md`: field semantics, failure codes, limits, replay, versioning and
  migration documentation for every new schema.
* `docs/GKG_EVALUATION.md` and `docs/evidence/gkg-20260905221500.report.json`:
  documented structure, measured source frequencies and promotion gates.
* `docs/DECISIONS.md`, `README.md`, this report: current decisions, commands,
  final outcomes and tightly scoped follow-up; remove misleading old next steps.

## Tests and exact outcomes

Environment: Python **3.12.14**, Windows. No dependency installation needed for
Python code. Portable Git was installed outside the checkout because the bundled
Git lacked its HTTPS helper.

| Stage / command | Outcome |
| --- | --- |
| Cleanup baseline: `python -B scripts/test_validate_gkg.py` | `test_validate_gkg: PASS`, exit 0 (original single fixture) |
| Validator group: `python -B -m unittest discover -s scripts -p 'test_*.py' -v` | 26 tests, OK, exit 0 |
| Report contract group: same discovery command | 30 tests, OK, exit 0 |
| Registry/observation group: same discovery command | 37 tests, OK, exit 0 |
| Final suite after additional archive/partial-scan checks | **41 tests, OK, exit 0**, 0.096 seconds in recorded run |
| `python -B scripts/validate_gkg.py --integration --output artifacts/live-report.json` with approved network access | **exit 0**, passed; 479 valid rows, 0 rejected, complete CRC-checked scan |
| Retained empirical JSON loaded with `validate_contract('validation-report', report)` | passed, no exception |
| `node --check app.js` | exit 0 |
| `git diff --check` | exit 0; no whitespace errors |
| `git ls-files '*.pyc' '*.pyo'` | empty output; no tracked bytecode |
| `git diff --exit-code BASELINE -- app.js index.html style.css data/gdelt.json scripts/update_gdelt.py .github/workflows/update-gdelt.yml` | exit 0; all six preserved production files identical |

Offline tests do not acquire source data. Network exceptions are mocked. Fixtures
use fixed ZIP timestamps and fictional theme tokens; they are never represented
as empirical data. JSON replay tests compare byte-identical output given fixed
bytes/reference/time. CLI tests verify failure reports replace prior successes.
The live test is separate and explicitly integration scoped. GitHub-hosted CI was
not executed in this local validation record; workflow YAML was inspected.

## Audit result

10 keep, 4 replace, 5 retire classifications across 19 baseline files. Retire means
architectural disposition: the DOC updater and active production writer remain
unchanged pending separate retirement approval. Unknowns are explicitly recorded
for deployment settings, source reliability/rights/coverage and historical data.
The stricter validator replaces the eight-column minimum that accepted truncated
fixtures, missing date checks, lossy decoding and success-only reports.

## GKG recommendation

**continue_validation**. The live 20260905221500 batch was 2,102,833 ZIP bytes,
with 479 27-field rows and no rejected records. Empty themes occurred in 76 rows
(15.87%). There were 1,459 distinct literal theme tokens. Full frequencies, exact
source reference, SHA-256 and verified metadata checksum are retained in the
[empirical report](evidence/gkg-20260905221500.report.json).

This supports technical feasibility, not production promotion. One sample cannot
establish sustained acquisition, historical continuity, representative coverage
or theme validity. No production mapping, ontology, indicator or forecast was
created. See [evaluation](GKG_EVALUATION.md) for primary documentation references.

## Limitations and unresolved facts

Only one live batch was sampled locally. Earlier successful Actions acquisition
is reported by the baseline decision log but its artifact was not inspected.
The raw ZIP is source-referenced and hashed, not retained in Git. Source retention,
HTTPS behavior, backfill completeness, usage rights, distribution shifts and
cross-batch duplicate handling remain to be evaluated. Resource limits are initial
guardrails. Validated structure does not certify all 27 fields' semantics.

The observation contract is numeric and source-independent; it does not implement
storage, ingestion transactions, registry foreign-key enforcement or metric
semantics. Unknown dates/scopes remain null. Killed jobs or an unwritable disk
cannot guarantee an artifact; exit/job failure remains visible. The existing
prototype still has its documented legacy limitations; this issue preserves it.

## Recommended next issue

**GKG bounded continuity and reproducibility study:** account for 96 consecutive
15-minute batches plus a small historical sample, retain attempt/checksum/quality
manifests, compare replays, measure coverage/resource needs, investigate HTTPS
and usage terms, and propose storage/retention with a revised promotion decision.
No dashboard migration or theme mapping belongs in that issue.

## Post-implementation self-review (2026-09-06)

Four reproducible defects were found and fixed in validator 1.0.1. The report
schema stays at 1.0.0; retained live evidence still records its original 1.0.0
validator and has not been rewritten.

| Severity | Reproduction / impact | Fix |
| --- | --- | --- |
| High | --input and --output target the same file: a valid source ZIP is replaced with JSON | Reject identical/resolved paths and hard-link aliases; preserve source; JSON report_write_error on stderr, exit 4 |
| Medium | Discovery size contains 5,000 digits: Python int conversion raises uncaught ValueError instead of producing a failure report | Bound the numeric metadata token before conversion; return metadata_invalid |
| Medium | Retrieved timestamp ends in +00:99: datetime.fromisoformat normalizes the invalid offset and the contract accepts it | Validate explicit offset hour/minute ranges |
| Medium | Local ZIP exceeds read limit: the prefix checksum and prefix length are presented as the entire archive's provenance | Leave archive checksum/size null until the input is known to fit the limit |

All four new regression cases failed before the fixes (three assertions and one
uncaught exception). After fixes: `python -B -m unittest discover -s scripts -p
 'test_*.py' -v` ran **45 tests, OK, exit 0** (0.116 seconds in the recorded run).
The original 41 tests still pass. Tests are offline; a new live run was not needed
for these local failure and contract fixes. The GKG recommendation remains
continue_validation. Production frontend/data/updater/workflow remain unchanged.
