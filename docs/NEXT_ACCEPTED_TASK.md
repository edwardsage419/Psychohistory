# Next Accepted Task

Last updated: 2026-09-07

## Goal

Generate a deterministic recovery-target manifest over the complete frozen 120-case `gkg-semantics-v2` sample, then prepare the next bounded evidence-recovery batch without changing the frozen Phase 6A identity contract, sample membership, or semantic conclusions.

## Classification

Risk: L2 for deterministic target selection and bounded recovery preparation under an already accepted protocol.

Recommended execution model if Codex is used: GPT-5.6 Terra High.

Escalate to Sol High only if execution exposes a protocol ambiguity that would change scientific semantics, trust boundaries, sample membership, evidence identity, or readiness criteria.

Astra is not authorized for routine execution.

## Authoritative inputs

Read only what is needed, in this order:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `SCIENTIFIC_INVARIANTS.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. `studies/gkg-semantics-v2/frozen-sample-reference.json`
6. `studies/gkg-semantics-v1/sample.json`
7. `studies/gkg-semantics-v2/phase6a-protocol.json`
8. `studies/gkg-semantics-v2/assessment-manifest.json`
9. `studies/gkg-semantics-v2/evidence.json`
10. `studies/gkg-semantics-v2/phase6a1-protocol.json`
11. `studies/gkg-semantics-v2/phase6a1-triage.json`
12. `studies/gkg-semantics-v2/phase6a1-availability.json`
13. `studies/gkg-semantics-v2/human-identity-review-results.csv`
14. `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`
15. `scripts/gkg_recovery.py`
16. `scripts/phase6a1_recovery.py`

Implementation may inspect `scripts/gkg_semantics.py` only for the existing canonical serialization, digest, authentication, and validation helpers needed by the bounded task.

Do not scan unrelated repository history or production code unless a preservation check exposes a concrete dependency.

## Execution preflight aids

After independently reading and validating the authoritative inputs above, read:

* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline.json`
* `docs/CODEX_EXECUTION_READINESS_AUDIT.md`

These files are accepted execution aids and regression oracles. They are not evidence authorities and must never be used as their own trust roots.

The implementation must first recompute the frozen state, coverage, tiers and bounded-batch membership from the authoritative inputs. Only then compare the derived results against the expected-output baseline.

If the authoritative inputs disagree with the preflight baseline, do not force the implementation to match the baseline. Stop, preserve the discrepancy, and determine whether the accepted evidence state changed or the preflight artifact is stale.

## Trust-root and overlay sequence

The manifest must not authenticate an input using a digest calculated only from that same loaded candidate input.

Use this sequence:

1. Authenticate `studies/gkg-semantics-v1/sample.json` against the frozen SHA-256 in `frozen-sample-reference.json`, then verify exactly 120 unique cases, `replacement=false`, `resampling=false`, and the accepted case-ID set hash.
2. Treat the accepted `assessment-manifest.json` on authoritative `main` as the external content-root map for the accepted Phase 6A/6A.1 machine artifacts. Verify at minimum the accepted roots for `evidence.json`, `phase6a1-triage.json`, `phase6a1-protocol.json`, and `phase6a1-availability.json` before using them.
3. Call or reuse `phase6a1_recovery.resolve()` with `base_root=assessment_manifest["artifacts"]["evidence.json"]` and `delta_root=assessment_manifest["artifacts"]["phase6a1-triage.json"]`. Do not pass freshly computed self-digests as the sole authentication roots.
4. Verify the current accepted human-review and coverage-audit artifacts are unchanged from their accepted Git objects before joining them to the resolved machine view.
5. Keep machine evidence, human review, and generated manifest artifacts physically and semantically separate.

Expected accepted Git objects for the two post-assessment human/audit inputs are:

* `human-identity-review-results.csv`: `6ea6884e73918f7f3d3a52c076885dc409f5aca7`
* `PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`: `61cf2d3f51a30278e5a04ae032a268ec23f0e58f`

## Frozen facts

The 120-case sample remains immutable.

Current objective E3 coverage is:

* `PROTEST`: 0 / 24 required
* `FOOD_SECURITY`: 5 / 24 required
* `WB_2747_UNEMPLOYMENT`: 1 / 24 required
* total: 6 / 72 required

The current lower-bound deficit is 66 additional E3 contexts, with additional allocated-year distribution constraints.

The completed model-assisted human identity layer contains:

* 13 `SAME_ARTICLE`
* 2 `DIFFERENT_ARTICLE`
* 7 `INSUFFICIENT_EVIDENCE`

Human `SAME_ARTICLE` is a recovery-priority signal only. It does not automatically create E3.

## Deterministic interpretation

Recovery priority and current promotion eligibility are separate dimensions.

`recovery_priority_tier` describes whether and how urgently the original frozen case is worth further bounded objective recovery.

`promotion_target_excluded` describes whether the current machine/human evidence state excludes the case from promotion targeting now.

A case may therefore be Tier A and simultaneously promotion-excluded. Under the current accepted inputs this applies to HIR-11 and HIR-15 because they have human `SAME_ARTICLE` judgments in deficient year cells while their current machine state remains `identity_mismatch`.

Human review never mutates machine identity and never creates E3. Only new objective evidence satisfying the frozen identity contract can change the machine state.

## Exact tier precedence

Assign tiers only after resolving the current machine view and joining the human identity layer.

Use this precedence exactly for every row:

1. If `current_e3 == true`, assign no recovery tier and no recovery rank.
2. If human decision is `SAME_ARTICLE` and the allocated year cell has `year_cell_deficit > 0`, assign Tier A. This rule has precedence over current machine mismatch, which is why HIR-11 and HIR-15 are Tier A while still promotion-excluded.
3. Otherwise, if human decision is `INSUFFICIENT_EVIDENCE` or `DIFFERENT_ARTICLE`, assign Tier D.
4. Otherwise, if current machine identity is `identity_mismatch`, assign Tier D.
5. Otherwise, if the allocated year cell has no remaining deficit, assign Tier D.
6. Otherwise, assign Tier B when the current machine identity is `identity_probable_manual_review_required`.
7. Otherwise, an `identity_unresolved` case may also receive Tier B only when the resolved accepted evidence contains an explicit same-document locator candidate: `recovered_url` or at least one `canonical_urls` entry is URI-equivalent to `original_url` under the already accepted `gkg_recovery.uri()` comparison.
8. Otherwise, a deficient-cell `identity_unresolved` case receives Tier C.
9. Any residual non-E3 case receives Tier D.

Do not use title similarity, publication date, publisher reputation, article desirability, semantic relevance, current-page accessibility, or later forecasting usefulness to change Tier membership.

This precedence means human `INSUFFICIENT_EVIDENCE` is Tier D even when its machine state is probable. Human `SAME_ARTICLE` is the only human decision that can create the Tier A precedence exception.

## Promotion exclusion

Set `promotion_target_excluded = true` independently when either condition applies:

* current machine identity is `identity_mismatch`
* human decision is `DIFFERENT_ARTICLE`

Tier assignment must never silently alter this exclusion flag.

## Deterministic objective recoverability order

Do not invent weighted scores.

For non-E3 cases, compute the global recovery ordering lexicographically as:

1. tier rank: A, B, C, D
2. `year_cell_deficit` descending
3. current machine state rank:
   * `identity_probable_manual_review_required`
   * `identity_mismatch`
   * `identity_unresolved`
4. retained objective body/hash signal: non-empty `content_sha256` before absent
5. accepted Phase 6A `retrieval_method` rank from `phase6a-protocol.json` hierarchy
6. `frozen_order`

If a non-E3 row requires a retrieval-method ordering that cannot be mapped to the accepted Phase 6A hierarchy, stop rather than inventing a new rank.

The mismatch state can participate in recovery ordering while `promotion_target_excluded` remains true.

## Output structure and determinism

Use the fixed implementation footprint unless a concrete repository constraint makes one path impossible:

* `scripts/phase6a_recovery_manifest.py`
* `scripts/test_phase6a_recovery_manifest.py`
* `studies/gkg-semantics-v2/recovery-target-manifest.json`
* `docs/PHASE6A_RECOVERY_TARGET_MANIFEST.md`

The canonical machine-readable manifest must contain exactly 120 case records in immutable frozen-sample order. Give each non-E3 row a deterministic `recovery_rank`; E3 rows use no recovery rank. A separate ordered recovery queue may be emitted from those ranks, but it must not replace or reorder the authoritative 120-row case array.

Use the repository's existing canonical JSON serialization helper. Do not place wall-clock generation timestamps, random IDs, environment-specific paths, or other execution noise inside the canonical manifest. If execution metadata is useful, keep it outside the canonical scientific output.

The human-readable summary must be derived mechanically from the canonical manifest and must not contain model-generated scientific judgments.

## Required work

1. Resolve the accepted Phase 6A baseline plus the Phase 6A.1 26-case delta into one read-only current identity-status view for all 120 frozen cases.
2. Compute E3 coverage by token and allocated year.
3. Join the human identity layer by `case_id` and fail closed on duplicate review rows, unknown case IDs, or disagreement in frozen `token`, `year`, or `source` metadata.
4. Assign every non-E3 case a tier using the exact precedence above without changing machine identity status.
5. Set promotion exclusion independently using the rule above.
6. Compute deterministic recovery ranks using the exact lexicographic key above.
7. Emit the canonical 120-row manifest containing at minimum:
   * `frozen_order`
   * `case_id`
   * `token`
   * `year`
   * `cohort`
   * `source`
   * `original_url`
   * `machine_identity_status`
   * `evidence_sufficiency`
   * `current_e3`
   * `human_review_id` if present
   * `human_identity_decision` if present
   * `human_identity_confidence` if present
   * `year_cell_e3_count`
   * `year_cell_minimum`
   * `year_cell_deficit`
   * `token_e3_count`
   * `token_minimum`
   * `token_deficit`
   * `recovery_priority_tier`
   * `recovery_rank`
   * `promotion_target_excluded`
   * `promotion_exclusion_reason`
   * structured `objective_recoverability_signals`
   * structured `recovery_rationale_codes`
   * `allowed_next_recovery_methods`
   * immutable source/evidence locator or hash references sufficient for replay
8. At minimum, provenance for each row must preserve the frozen source-row identity available from `sample.json`, the accepted baseline evidence-row digest, the Phase 6A.1 delta-row digest when that case was overlaid, the resolved evidence-row digest, and the human `review_id` when present. Top-level input bindings must identify the frozen sample and accepted machine/human artifacts used.
9. `allowed_next_recovery_methods` must stay inside the frozen Phase 6A protocol. For a non-E3 case the only method families that may appear are `original_publisher`, `same_path_https_candidate` when an exact HTTPS equivalent is applicable, `wayback_availability_discovery`, and `dated_wayback_capture` conditional on an exact discovered locator satisfying the protocol. `unavailable` is a state, not a recovery method. Do not add broad search, syndicated substitution, or guessed publisher/archive paths.
10. Emit a compact human-readable summary showing the first bounded recovery batch.
11. Define the first bounded recovery batch mechanically as Tier A cases in zero-E3 year cells that are not currently promotion-excluded. Under unchanged accepted inputs, independently derived membership must match the nine-case set in the expected-output baseline. Do not hard-code those nine IDs as the selection algorithm.
12. Validate mechanically that:
   * all manifest case IDs belong to the frozen 120
   * there are exactly 120 rows and no duplicate case IDs
   * the frozen case-ID set hash matches the accepted reference
   * no replacement/sample substitution occurred
   * the six currently accepted E3 cases remain E3 and are not targeted for recovery
   * all 13 human `SAME_ARTICLE` cases remain separate human provenance and receive Tier A while their cells remain deficient
   * HIR-11 and HIR-15 are Tier A while still promotion-excluded under current machine mismatch
   * the two human `DIFFERENT_ARTICLE` cases are Tier D and not promotion targets
   * all current machine `identity_mismatch` cases are promotion-excluded; those without the Tier A SAME_ARTICLE exception are Tier D
   * all human `INSUFFICIENT_EVIDENCE` cases are Tier D
   * machine evidence artifacts and human-review artifacts are not overwritten
   * identical inputs produce byte-identical canonical manifest output
13. Add mutation/regression tests for duplicate case injection, frozen metadata mutation, automatic human-to-E3 promotion, stale/mismatched trust roots, incorrect tier precedence, promotion-exclusion removal, and first-batch membership drift.
14. Stop after manifest generation and bounded-batch definition. Network recovery is not authorized by this task.

## Scientific invariants to enforce

Applicable invariants include I3, I4, I6, I8, I9, I11 and I12.

In particular:

* no human judgment may silently rewrite machine evidence
* no failed or unresolved case may be replaced by a more convenient article
* no missing historical evidence may be inferred into existence
* no target-selection rule may use semantic label desirability or later forecasting utility
* no current-page similarity alone may be treated as historical identity confirmation

## Acceptance criteria

* Exact 120-case membership and frozen order preserved.
* Current E3 count remains exactly 6 before new recovery.
* The exact six E3 case IDs reproduce the expected-output baseline.
* Coverage counts reproduce `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`.
* Priority rules and `recovery_rank` are deterministic and reproducible.
* All 13 human `SAME_ARTICLE` judgments remain separate provenance fields, not E3 promotions.
* Tier A membership reproduces the expected 13-case set under unchanged inputs.
* All seven human `INSUFFICIENT_EVIDENCE` cases are Tier D.
* HIR-11 and HIR-15 remain Tier A while current promotion eligibility is false.
* Both human `DIFFERENT_ARTICLE` cases remain negative evidence, are Tier D, and are excluded from promotion targeting.
* All seven current machine mismatches are excluded from promotion targeting; only HIR-11 and HIR-15 may remain Tier A because of the explicit SAME_ARTICLE precedence rule.
* First bounded-batch membership reproduces the expected nine-case set under unchanged inputs.
* Manifest exposes enough provenance to replay why every case received its priority.
* The generated canonical machine-readable output is byte-deterministic for identical inputs.
* The four fixed output files exist and the offline test suite passes.
* No semantic review, semantic promotion, composite construction, forecast implementation, calibration or backtesting begins.

## Stop conditions

Stop and escalate to Sol High if:

* the accepted Phase 6A baseline and Phase 6A.1 delta cannot be resolved without changing evidence semantics
* the frozen sample membership does not reconcile to exactly 120 unique cases
* the frozen sample content or case-ID set does not authenticate against the accepted reference
* current E3 coverage does not reconcile to exactly six
* the exact six E3 case IDs differ from the independently accepted baseline
* human identity counts do not reconcile to 13 / 2 / 7
* coverage does not reconcile to the accepted audit
* the authoritative inputs disagree with the preflight oracle and the difference cannot be explained as a stale preparation artifact
* a required trust root would be circular or self-authenticating
* a proposed recovery method would violate the accepted identity hierarchy, archive-distance rule, network trust policy, provenance rules, or no-substitution rule
* deterministic target ranking requires inventing a new scientific criterion not already specified here or in the frozen protocol
* a non-E3 retrieval method cannot be mapped to the frozen hierarchy without inventing a new ranking rule

Otherwise complete with Terra High or equivalent deterministic tooling.

## After this task

Run bounded evidence recovery against the accepted target manifest only after explicit authorization, recompute E3 coverage mechanically, and repeat only while preserving the frozen sample and protocol. Independent semantic review remains blocked until every token has at least 24 E3 contexts and every allocated year has at least four.
