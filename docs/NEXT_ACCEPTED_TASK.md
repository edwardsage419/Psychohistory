# Next Accepted Task

Last updated: 2026-09-07

## Goal

Generate a deterministic recovery-target manifest over the complete frozen 120-case `gkg-semantics-v2` sample, then prepare the next bounded evidence-recovery batch without changing frozen sample membership, the accepted document-identity contract, human identity judgments, or semantic conclusions.

This task uses corrected evidence-sufficiency version `1.0.1` and treats E2/E3 as review-ready context.

## Classification

Risk: L2 for deterministic target selection and bounded recovery preparation under accepted scientific semantics.

Recommended Codex model: GPT-5.6 Terra High.

Escalate to Sol High only if execution exposes a new ambiguity that would alter identity semantics, evidence-sufficiency meaning, trust boundaries, sample membership, readiness criteria, or deterministic ranking rules.

Astra is not authorized for routine execution.

## Authoritative inputs

Read only what is needed, in this order:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `SCIENTIFIC_INVARIANTS.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. `studies/gkg-semantics-v2/frozen-sample-reference.json`
6. `studies/gkg-semantics-v1/sample.json`
7. `studies/gkg-semantics-v1/preregistration.json`
8. `studies/gkg-semantics-v2/phase6a-protocol.json`
9. `studies/gkg-semantics-v2/assessment-manifest.json`
10. `studies/gkg-semantics-v2/evidence.json`
11. `studies/gkg-semantics-v2/phase6a1-protocol.json`
12. `studies/gkg-semantics-v2/phase6a1-triage.json`
13. `studies/gkg-semantics-v2/context-sufficiency-correction.json`
14. `studies/gkg-semantics-v2/human-identity-review-results.csv`
15. `docs/PHASE6A1_CONTEXT_SUFFICIENCY_CORRECTION.md`
16. `scripts/gkg_semantics.py`
17. `scripts/retrieve_gkg_semantics.py`
18. `scripts/gkg_recovery.py`
19. `scripts/phase6a1_recovery.py`

The correction contract explicitly pins the Phase 5 cue/extractor semantics and the current recovery implementations because evidence-sufficiency `1.0.1` depends on them. Do not substitute a later unpinned extractor or cue vocabulary while recomputing the current state.

The historical `phase6a1-availability.json`, `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`, `docs/PHASE_6A1_REPORT.md`, and `docs/PHASE_5_6A1_ACCEPTANCE_REVIEW.md` preserve pre-correction state. Their old E3 counts and next-step wording are historical provenance and do not override current correction artifacts or `CURRENT_STATE.md`.

Do not scan unrelated repository history or future-gate code unless a concrete preservation check requires it.

## Current execution aids

Only after independently authenticating and recomputing the authoritative current state, read:

* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT_V2.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline-v2.json`

These are regression aids, not evidence authorities.

The following files remain historical preparation records and are superseded for current execution:

* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline.json`
* `docs/CODEX_EXECUTION_READINESS_AUDIT.md`

Do not force current results to match those historical pre-correction counts.

## Trust-root and overlay sequence

Do not confuse raw-file SHA-256 with the canonical JSON object digest expected by `phase6a1_recovery.resolve()`.

Use this sequence exactly:

1. Authenticate `studies/gkg-semantics-v1/sample.json` against the frozen sample SHA-256 recorded in `frozen-sample-reference.json`; verify 120 unique cases, no replacement/resampling, and the accepted case-ID set hash.
2. Verify the current `preregistration.json`, Phase 6A protocol, Phase 6A.1 protocol, and four semantic/implementation dependencies against `context-sufficiency-correction.json` before recomputing evidence sufficiency.
3. Read raw bytes for `evidence.json` and `phase6a1-triage.json`.
4. Verify the byte SHA-256 of those files against the independently accepted artifact hashes in `assessment-manifest.json`.
5. Parse the authenticated bytes.
6. Compute canonical object digests with the pinned `gkg_semantics.digest()` helper.
7. Call/reuse `phase6a1_recovery.resolve()` with those canonical object digests as `base_root` and `delta_root`.
8. Recompute evidence sufficiency with current version `1.0.1` and verify the result against `context-sufficiency-correction.json`.
9. Verify the human identity CSV against accepted Git object `6ea6884e73918f7f3d3a52c076885dc409f5aca7` before joining by `case_id`.
10. Keep machine evidence, human identity review, and generated manifest artifacts separate.

A digest computed from an unauthenticated candidate file is not an external trust root. Once file bytes or Git objects have been independently authenticated, computing the canonical object digest required by `resolve()` is valid transformation of authenticated input.

## Frozen and corrected facts

Frozen sample remains exactly 120 cases.

Current machine identity counts remain:

* `identity_confirmed`: 6
* `identity_probable_manual_review_required`: 15
* `identity_mismatch`: 7
* `identity_unresolved`: 92

Corrected evidence sufficiency version `1.0.1` is:

* E0: 114
* E1: 3
* E2: 0
* E3: 3

Review-ready context means E2 or E3. Current review-ready count is 3.

Current review-ready token coverage:

* `PROTEST`: 0 / 24, deficit 24
* `FOOD_SECURITY`: 2 / 24, deficit 22
* `WB_2747_UNEMPLOYMENT`: 1 / 24, deficit 23

Current lower-bound token deficit is 69 additional review-ready contexts, subject also to allocated-year minima.

The model-assisted human identity review with final human adjudication contains:

* 13 `SAME_ARTICLE`
* 2 `DIFFERENT_ARTICLE`
* 7 `INSUFFICIENT_EVIDENCE`

This human layer is separate provenance. It is not independent/blinded semantic review and never creates E2 or E3.

## Review-ready versus recovery target

Rows in E2/E3 receive no recovery tier and no recovery rank.

E1 means identity is confirmed but retained compact context remains insufficient for semantic review. E1 rows remain recovery candidates for additional objective context recovery.

Recovery priority and promotion exclusion are independent dimensions.

## Exact tier precedence

Assign tiers after resolving the machine view, recomputing sufficiency, computing review-ready coverage, and joining human identity review.

Apply exactly:

1. If `review_ready == true` (E2 or E3), assign no recovery tier and no recovery rank.
2. If human decision is `SAME_ARTICLE` and the allocated year cell has `year_cell_deficit > 0`, assign Tier A. This takes precedence over current machine mismatch for HIR-11 and HIR-15.
3. Otherwise, if human decision is `INSUFFICIENT_EVIDENCE` or `DIFFERENT_ARTICLE`, assign Tier D.
4. Otherwise, if current machine identity is `identity_mismatch`, assign Tier D.
5. Otherwise, if the allocated year cell has no remaining review-ready deficit, assign Tier D.
6. Otherwise, if machine identity is `identity_confirmed` with E1, assign Tier B.
7. Otherwise, if machine identity is `identity_probable_manual_review_required`, assign Tier B.
8. Otherwise, an `identity_unresolved` case may receive Tier B only when accepted resolved evidence contains an explicit URI-equivalent `recovered_url` or canonical URL under the pinned `gkg_recovery.uri()` semantics.
9. Otherwise, a deficient-cell `identity_unresolved` case receives Tier C.
10. Any residual non-review-ready case receives Tier D.

Do not use title similarity, publication date, publisher reputation, semantic desirability, current accessibility, or later forecasting utility to alter tier membership.

## Promotion exclusion

Set `promotion_target_excluded = true` independently when either applies:

* current machine identity is `identity_mismatch`
* human decision is `DIFFERENT_ARTICLE`

Tier assignment never clears this flag.

Under unchanged current inputs the exclusion union contains seven cases. HIR-11 and HIR-15 remain Tier A plus promotion-excluded.

## Deterministic recovery ordering

Do not invent weighted scores.

For non-review-ready cases, rank lexicographically by:

1. tier A, B, C, D
2. year-cell review-ready deficit descending
3. machine state rank:
   * `identity_confirmed` E1
   * `identity_probable_manual_review_required`
   * `identity_mismatch`
   * `identity_unresolved`
4. non-empty accepted `content_sha256` before absent
5. accepted retrieval-method rank below
6. frozen sample order

Normalize the already accepted Phase 6A and Phase 6A.1 method vocabulary only for deterministic ordering:

* rank 0: `original_publisher`
* rank 1: `same_path_https_candidate` and `canonical_publisher`
* rank 2: `wayback_availability_discovery`
* rank 3: `dated_wayback_capture`
* rank 4: `unavailable` or no successful evidence method

`canonical_publisher` is an accepted Phase 6A.1 same-publisher locator method. It shares rank 1 with `same_path_https_candidate`; equal-rank cases fall through to frozen order. This normalization does not change evidence sufficiency, identity status, or promotion eligibility.

If a current non-review-ready method is outside the accepted Phase 6A plus Phase 6A.1 vocabulary above, stop and escalate rather than inventing a new rank.

## Fixed output footprint

Create exactly:

* `scripts/phase6a_recovery_manifest.py`
* `scripts/test_phase6a_recovery_manifest.py`
* `studies/gkg-semantics-v2/recovery-target-manifest.json`
* `docs/PHASE6A_RECOVERY_TARGET_MANIFEST.md`

Change a path only if a concrete repository constraint makes it impossible and report that constraint.

## Canonical output

The canonical manifest must contain all 120 cases in immutable frozen order.

Every non-review-ready row receives a deterministic `recovery_rank`. Review-ready rows receive none.

Minimum fields:

* `frozen_order`
* `case_id`, `token`, `year`, `cohort`, `source`, `original_url`
* `machine_identity_status`
* `evidence_sufficiency_version`
* `evidence_sufficiency`
* `review_ready`
* human `review_id`, decision, confidence when present
* year-cell review-ready count/minimum/deficit
* token review-ready count/minimum/deficit
* recovery tier and rank
* promotion exclusion and reason
* structured objective recoverability signals
* structured rationale codes
* allowed next recovery methods
* immutable source/evidence provenance sufficient for replay

Per-row provenance must preserve frozen source-row identity, accepted baseline evidence-row identity/digest, Phase 6A.1 delta identity/digest when overlaid, resolved evidence-row digest, and human review ID when present.

Top-level bindings must identify the frozen sample, authenticated machine inputs, sufficiency correction contract, pinned semantic dependencies/current implementation identity, and human review artifact.

Use repository canonical JSON serialization. Do not include wall-clock timestamps, random IDs, local paths, or environment-specific metadata in the canonical scientific output.

## Allowed recovery methods

The manifest may list only accepted method families:

* `original_publisher`
* `same_path_https_candidate` when an exact HTTPS equivalent is applicable
* `canonical_publisher` only when an exact same-publisher canonical/final locator is already present in accepted evidence/protocol provenance; never guess a canonical path
* `wayback_availability_discovery`
* `dated_wayback_capture` only after an exact valid locator is discovered

`unavailable` is a state, not a next recovery method.

The Phase 6A protocol's deferred `canonical_publisher_archive` remains out of scope. It is distinct from the accepted Phase 6A.1 `canonical_publisher` method and may not be inferred from publisher naming or guessed paths.

No broad search, syndicated substitution, guessed publisher/archive path, or unrelated-result substitution is allowed.

This task performs no network recovery.

## First bounded batch

Define mechanically:

`Tier A AND year_cell_review_ready_count == 0 AND promotion_target_excluded == false`

Under unchanged current inputs the independently derived membership must match the ten-case set in the V2 oracle.

Do not hard-code those IDs as the algorithm.

The current count is 10 because the `FOOD_SECURITY` 2025 cell now has zero review-ready context after the sufficiency correction, so HIR-12 joins the historical nine-case batch.

## Required validation

Mechanically verify:

* 120 rows and 120 unique frozen case IDs
* frozen case-ID set hash exact
* no replacement/resampling
* machine identity 6/15/7/92
* sufficiency E0=114/E1=3/E2=0/E3=3
* exact E1 and E3 sets from the V2 oracle
* review-ready count exactly 3
* human counts 13/2/7
* human judgments do not mutate machine identity or sufficiency
* corrected review-ready token/year coverage exact
* all 13 SAME cases are Tier A while their cells remain deficient
* HIR-11/HIR-15 are Tier A plus promotion-excluded
* all current mismatches and human DIFFERENT cases are promotion-excluded
* human INSUFFICIENT cases remain Tier D under current non-review-ready state
* three current E2/E3 review-ready cases have no recovery tier
* current E1 cases remain visible recovery candidates
* the E1 case whose current retrieval method is `canonical_publisher` maps deterministically without triggering a false stop
* first bounded batch membership is exact ten under unchanged inputs
* identical inputs produce byte-identical canonical output
* frozen evidence, delta, protocols, preregistration, sample, and human-review artifacts remain byte unchanged

Add mutation tests for duplicate cases, frozen metadata changes, trust-root mismatches, semantic-dependency drift, human-to-E2/E3 promotion, tier-precedence errors, exclusion removal, review-ready/E1 confusion, unsupported retrieval methods, and first-batch drift.

## Scientific invariants

Applicable invariants include I3, I4, I6, I8, I9, I11 and I12.

In particular:

* no human judgment rewrites machine evidence
* no missing context is inferred into existence
* identity-confirmed E1 is not treated as review-ready
* no frozen case is replaced by a convenient article
* no semantic desirability or forecast usefulness enters target ranking
* no current-page similarity alone confirms historical identity
* changing the pinned cue/extractor semantics requires a new explicit version; it cannot silently alter current sufficiency

## Acceptance criteria

The task is accepted only if the complete offline test suite passes and all current corrected counts above are independently reproduced before comparing against the V2 oracle.

No semantic review, semantic promotion, composite construction, forecasting, calibration, or backtesting begins.

## Stop conditions

Stop and escalate to Sol High if:

* frozen membership/authentication fails
* machine identity cannot reconcile to 6/15/7/92
* sufficiency cannot reconcile to 114/3/0/3 under version 1.0.1
* a pinned preregistration/protocol/extractor/recovery dependency differs from the correction contract without an accepted version change
* exact E1/E3 sets differ under unchanged authenticated inputs
* review-ready coverage differs from the corrected V2 baseline
* human counts do not reconcile to 13/2/7
* a required trust root would be circular
* current inputs and V2 oracle disagree without an explained stale-oracle cause
* ranking requires a new scientific criterion
* a recovery method outside the accepted Phase 6A/6A.1 vocabulary would need a new rank
* a recovery method would violate frozen identity, archive-distance, provenance, or no-substitution rules
* implementation would modify accepted evidence or human-review artifacts

Otherwise complete with Terra High.

## After this task

Only after explicit authorization, run bounded objective evidence/context recovery against the accepted manifest, recompute E2/E3 review-ready coverage mechanically, and repeat while preserving the frozen sample and accepted versioned protocols.

After each accepted bounded recovery batch, reassess recovery viability before authorizing another batch. Evidence recovery is not an open-ended requirement to rescue GKG at any cost. A later governance decision may continue recovery, restrict the validated period/use case, or reject this candidate while preserving the result as scientific evidence.

Independent semantic review remains blocked until each token has at least 24 review-ready E2/E3 contexts and every allocated year has at least four.
