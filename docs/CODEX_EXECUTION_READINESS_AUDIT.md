# Codex Execution Readiness Audit

Date: 2026-09-07
Status: accepted execution-readiness artifact for the current deterministic Phase 6A recovery-manifest task. This audit does not perform network recovery, change evidence, alter the frozen sample, or advance the scientific gate.

## Verdict

READY for bounded GPT-5.6 Terra High Codex execution after the documentation clarifications committed in the same readiness pass.

No unresolved scientific criterion remains that requires Sol High before implementation.

The task remains L2 because the scientific identity contract, sample membership, coverage gate, tier intent, promotion exclusion and first-batch rule are already accepted. The remaining work is deterministic cross-file implementation plus regression protection.

If execution encounters one of the stop conditions in `docs/NEXT_ACCEPTED_TASK.md`, the task must stop rather than using model strength to fill an evidence or protocol gap.

## Repository snapshot inspected

Pre-audit `main` HEAD:

`8b7be78b215151a9ef347f0b79a2e12eebe33f22`

The readiness pass then updated only the accepted task specification and added this audit. No scientific evidence input was modified.

## Scope inspected

Primary execution package:

* `AGENTS.md`
* `docs/NEXT_ACCEPTED_TASK.md`
* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline.json`

Required frozen/evidence dependencies:

* `studies/gkg-semantics-v2/frozen-sample-reference.json`
* `studies/gkg-semantics-v1/sample.json`
* `studies/gkg-semantics-v2/phase6a-protocol.json`
* `studies/gkg-semantics-v2/assessment-manifest.json`
* `studies/gkg-semantics-v2/evidence.json`
* `studies/gkg-semantics-v2/phase6a1-protocol.json`
* `studies/gkg-semantics-v2/phase6a1-triage.json`
* `studies/gkg-semantics-v2/phase6a1-availability.json`
* `studies/gkg-semantics-v2/human-identity-review-results.csv`
* `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`

Relevant accepted implementation semantics:

* `scripts/gkg_recovery.py`
* `scripts/phase6a1_recovery.py`

## Readiness findings

### R1. Authoritative-input closure was incomplete

Severity for execution: HIGH

Finding:

The earlier `NEXT_ACCEPTED_TASK.md` listed the Phase 6A protocol/evidence/delta/human/audit inputs but omitted several files that the implementation necessarily needs to authenticate and resolve the frozen view:

* `frozen-sample-reference.json`
* the actual frozen `gkg-semantics-v1/sample.json`
* `assessment-manifest.json`
* `phase6a1-protocol.json`
* `gkg_recovery.py`
* `phase6a1_recovery.py`

Risk:

Codex could have treated the preflight oracle as authority, scanned unrelated files to rediscover dependencies, or reimplemented overlay semantics from prose.

Disposition:

CLOSED. `docs/NEXT_ACCEPTED_TASK.md` now contains the complete bounded dependency set and separates authoritative inputs from execution aids.

### R2. Tier precedence could be interpreted inconsistently

Severity for execution: HIGH

Finding:

The prior prose allowed a possible reading in which Tier B/C could override human `INSUFFICIENT_EVIDENCE`. The accepted project clarification is stricter:

* E3: no tier
* human SAME in a deficient cell: Tier A, including HIR-11/HIR-15
* otherwise human INSUFFICIENT or DIFFERENT: Tier D
* otherwise machine mismatch: Tier D
* otherwise no cell deficit: Tier D
* then Tier B/C logic

Risk:

A probable machine case with human `INSUFFICIENT_EVIDENCE` could otherwise be classified B instead of D, changing the deterministic queue.

Disposition:

CLOSED. The exact precedence is now normative in `docs/NEXT_ACCEPTED_TASK.md`.

### R3. Tier B versus Tier C needed a machine-computable predicate

Severity for execution: MEDIUM

Finding:

The phrase "other objective identity signal" was scientifically bounded but implementation-ambiguous.

Disposition:

CLOSED conservatively without introducing title/date/similarity scoring.

Tier B now uses only accepted machine semantics:

1. current machine state is `identity_probable_manual_review_required`; or
2. an unresolved case has an explicit URI-equivalent `recovered_url` or canonical URL under the already accepted `gkg_recovery.uri()` comparison.

Remaining deficient-cell unresolved cases are Tier C after the Tier A/D precedence rules.

Title similarity, publication date, publisher reputation, semantic desirability and current-page accessibility do not affect Tier membership.

### R4. `resolve()` trust-root invocation required explicit external roots

Severity for execution: HIGH

Finding:

`phase6a1_recovery.resolve()` accepts `base_root` and `delta_root`. Passing `digest(base)` and `digest(delta)` immediately after loading the same candidate files would satisfy the function mechanically while providing circular authentication.

The accepted `assessment-manifest.json` already contains independently accepted artifact roots:

* `evidence.json`: `5e828feff976b47da5d9da67174b1b47c0a91a1003e3cbf1fff028ed5237b70d`
* `phase6a1-triage.json`: `9d7f27660cfc9034cec8fe4b203c863e63c3f5c2aad7cb6a4a777abf80f10869`

Disposition:

CLOSED. The accepted task now requires using the assessment-manifest roots when calling/reusing `resolve()` and explicitly forbids self-digest-only authentication.

### R5. Deterministic ordering needed a fully mechanical key

Severity for execution: MEDIUM

Finding:

The preflight defined the dimensions but Codex could still vary implementation details.

Disposition:

CLOSED. Global non-E3 recovery ordering is now lexicographic:

1. A/B/C/D tier rank
2. year-cell deficit descending
3. machine state: probable, mismatch, unresolved
4. non-empty accepted `content_sha256` before absent
5. frozen Phase 6A retrieval-method hierarchy
6. frozen sample order

No weighted recoverability score is allowed.

A retrieval method that cannot be mapped to the frozen hierarchy is a stop condition, not an invitation to invent a rank.

### R6. Manifest membership order and recovery priority order were conflated

Severity for execution: MEDIUM

Finding:

A priority-sorted 120-row array would make frozen-order preservation less transparent, while a frozen-order array alone would not visibly encode the required recovery ranking.

Disposition:

CLOSED.

The canonical `cases` array remains in immutable frozen order. Each non-E3 row receives a deterministic `recovery_rank`; E3 rows receive none. Any derived queue is produced from those ranks.

This keeps membership/provenance replay simple while preserving an explicit deterministic priority order.

### R7. Canonical output could have been contaminated by execution noise

Severity for execution: MEDIUM

Finding:

A wall-clock `generated_at`, local path, random ID, or environment-specific metadata would violate byte-equivalent rerun expectations even when scientific inputs were unchanged.

Disposition:

CLOSED. The canonical manifest must use the existing repository canonical JSON helper and exclude nondeterministic execution metadata. Execution metadata, if useful, belongs outside the canonical scientific output.

### R8. Allowed recovery methods needed a closed vocabulary

Severity for execution: MEDIUM

Finding:

A free-form `allowed_next_recovery_methods` field could accidentally reintroduce broad search, syndicated substitution or guessed archive/publisher paths.

Disposition:

CLOSED. The only allowed method families are the frozen Phase 6A methods:

* `original_publisher`
* `same_path_https_candidate` when applicable
* `wayback_availability_discovery`
* `dated_wayback_capture` only after an exact valid locator is discovered

`unavailable` is a state. It is not a recovery method.

This task performs none of those network operations; it only records which method families remain protocol-permitted.

### R9. Output footprint was optional

Severity for execution: LOW

Finding:

The preflight recommended filenames but allowed adjustment. That freedom provides little value for this task and creates unnecessary review variance.

Disposition:

CLOSED. The current task fixes the expected footprint:

* `scripts/phase6a_recovery_manifest.py`
* `scripts/test_phase6a_recovery_manifest.py`
* `studies/gkg-semantics-v2/recovery-target-manifest.json`
* `docs/PHASE6A_RECOVERY_TARGET_MANIFEST.md`

Change a path only if a concrete repository constraint makes it impossible, and report that constraint.

## Frozen regression expectations that remain unchanged

This readiness audit does not replace the independent oracle. Under unchanged accepted inputs the implementation must still independently reproduce:

* 120 unique frozen cases
* machine states 6 confirmed / 15 probable / 7 mismatch / 92 unresolved
* E3 = 6
* human decisions 13 SAME / 2 DIFFERENT / 7 INSUFFICIENT
* token E3 counts 0 / 5 / 1
* exact six E3 case IDs
* exact 13-case Tier A set
* exact seven-case promotion-excluded set
* HIR-11 and HIR-15 = Tier A plus promotion-excluded
* exact nine-case first bounded batch membership

Tier B, Tier C, full Tier D membership and the final 120-row manifest remain implementation-derived outputs and are intentionally not precomputed by the oracle.

## Required provenance closure

Each generated case row should make its classification replayable without treating the generated manifest as its own authority.

Minimum row-level provenance:

* frozen sample order and source-row identifiers/hashes already present in `sample.json`
* baseline Phase 6A evidence-row digest
* Phase 6A.1 delta-row digest if the case is in the 26-case overlay
* resolved evidence-row digest
* human `review_id` when present

Minimum top-level bindings:

* frozen sample reference/content root
* accepted assessment-manifest/root identity
* accepted machine artifact roots
* accepted human-review artifact identity
* accepted protocol identity

Derived row digests help replay the calculation but do not replace the external accepted roots above.

## Test sufficiency checklist

The bounded Codex implementation is expected to include tests that fail on at least:

* frozen sample cardinality or case-set mutation
* duplicate case injection
* frozen `case_id`, `token`, `year`, `cohort`, or `original_url` mutation
* stale or incorrect machine trust roots
* machine/human provenance overwrite
* automatic E3 creation from human SAME
* human INSUFFICIENT receiving B/C instead of D
* non-SAME mismatch receiving A/B/C instead of D
* HIR-11 or HIR-15 losing Tier A or losing promotion exclusion
* DIFFERENT_ARTICLE becoming promotion eligible
* E3 receiving a recovery tier/rank
* first bounded batch membership drift
* nondeterministic canonical output on identical inputs

The existing offline workflow already discovers `scripts/test_*.py`, so no CI workflow modification is needed for the expected test filename.

## Expected execution sequence

A low-rework Codex run should follow this order:

1. Read startup governance and the bounded task.
2. Authenticate the frozen sample and accepted input roots.
3. Resolve baseline plus 26-case delta using accepted code semantics and external roots.
4. Verify the 120-case/6-E3/coverage baseline before any tier calculation.
5. Strictly join the 22 human identity rows.
6. Compute coverage cells.
7. Assign tiers with the exact precedence.
8. Compute promotion exclusion independently.
9. Compute objective recoverability key and recovery ranks.
10. Build the 120 frozen-order canonical manifest.
11. Derive the first bounded batch and compare membership to the oracle.
12. Generate the deterministic human-readable summary.
13. Run focused tests, then the full offline suite.
14. Report hashes/counts and stop.

No network call belongs anywhere in this sequence.

## Model routing conclusion

Recommended: GPT-5.6 Terra High.

Why Terra High is sufficient:

* no new scientific semantics need to be invented
* overlay and E3 semantics already exist in accepted code
* tier and ordering ambiguity has been removed
* expected high-value regression outputs are independently pinned
* implementation spans several artifacts and tests, so Terra Medium is unnecessarily risky

Sol High is reserved only for a stop-condition ambiguity that changes scientific meaning or trust boundaries.

Astra remains unauthorized.

## Invariant check

This readiness work was checked against the applicable invariants:

* I3 Versioned semantics: no accepted identity or evidence semantics changed.
* I4 Historical reproducibility: trust-root and provenance requirements were strengthened.
* I6 Evidence traceability: row-level replay bindings were made explicit.
* I8 Explicit uncertainty: mismatch, unresolved and insufficient evidence remain explicit.
* I9 No silent historical rewrite: no accepted evidence artifact is modified.
* I11 Genuine human evidence remains human: human identity review remains a separate provenance layer and does not create E3.
* I12 Missing evidence cannot be reasoned into existence: no recovery result or semantic judgment is fabricated.

## Current scientific state preservation

This audit does not change:

* the frozen 120-case sample
* the six current E3 cases
* machine identity counts
* human review outcomes
* semantic conclusions
* the readiness threshold for independent semantic review
* the current Gate 3A bottleneck

The next scientific advancement remains the deterministic recovery-target manifest, followed only by separately authorized bounded objective recovery.
