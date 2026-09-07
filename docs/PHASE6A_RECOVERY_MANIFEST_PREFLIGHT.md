# Phase 6A Recovery Manifest Preflight

Date: 2026-09-07
Status: accepted preparation artifact only. No network recovery, evidence promotion, semantic review, or semantic promotion is performed here.

## Purpose

Prepare the deterministic recovery-target manifest task so the later Codex implementation can be mechanical, bounded, and fail closed.

This preflight does four things:

1. Binds the accepted frozen inputs and their independent trust references.
2. Reproduces the expected frozen counts and coverage matrix before any new recovery.
3. Records the already approved deterministic interpretation of recovery priority versus current promotion exclusion.
4. Defines a regression oracle that the implementation must reproduce without hard-coding its answers.

The machine-readable companion is:

`studies/gkg-semantics-v2/recovery-manifest-expected-baseline.json`

That file is a regression oracle only. It is not a source of evidence and must never become its own trust root.

## Preflight repository snapshot

The repository snapshot inspected before adding the preflight artifacts was:

`fbe7ef5c68fd82f4f3a1f7b012810ffecbecccfb`

The preflight and expected-output baseline are later documentation/research-preparation commits. They do not alter the accepted Phase 6A or Phase 6A.1 evidence inputs.

## Frozen input bindings

### Frozen sample

`studies/gkg-semantics-v2/frozen-sample-reference.json`

Git blob: `dfaabc6308ed71a2b36c418714afd2ea7055efcd`

Expected properties:

* cases: 120
* replacement: false
* resampling: false
* case ID set SHA-256: `50dace526474525e69f552cc833221c07e5ef91305f755fd8f4ac64c026c9895`
* frozen `sample.json` content SHA-256: `3a8710caabb8d571edbbd5f80276e00f25cec26c9622655d3b3db8d7045b9a46`
* frozen sample commit: `77fe85ae6904afa7b58590c5604f99a3c348ae64`

The actual frozen case metadata remains sourced from `studies/gkg-semantics-v1/sample.json` and authenticated against the frozen SHA-256 above. There is intentionally no separate `gkg-semantics-v2/sample.json`.

### Phase 6A protocol

`studies/gkg-semantics-v2/phase6a-protocol.json`

Git blob: `31392b97a3bc4881e2e550d956ca4fcfe4b15e9b`

The accepted hierarchy is:

1. `original_publisher`
2. `same_path_https_candidate`
3. `wayback_availability_discovery`
4. `dated_wayback_capture`
5. `unavailable`

Wayback discovery is locator discovery only. It is not article evidence. A capture must preserve original URI identity and satisfy the frozen seven-day distance rule.

No guessed publisher archive path, unrelated search result, or syndicated substitute is authorized.

### Accepted Phase 6A evidence

`studies/gkg-semantics-v2/evidence.json`

Content SHA-256 from the accepted assessment manifest:

`5e828feff976b47da5d9da67174b1b47c0a91a1003e3cbf1fff028ed5237b70d`

### Phase 6A.1 protocol

`studies/gkg-semantics-v2/phase6a1-protocol.json`

Git blob: `2b9f90f0f280842e3cb1ea6080fac9bb10a46064`

Content SHA-256 from the accepted assessment manifest:

`1f2a5b377b2b306fc9b460c40fa34bcbfd5863005c800fd2707aaf983def425c`

Expected targeted delta count: 26.

### Phase 6A.1 delta

`studies/gkg-semantics-v2/phase6a1-triage.json`

Content SHA-256 from the accepted assessment manifest:

`9d7f27660cfc9034cec8fe4b203c863e63c3f5c2aad7cb6a4a777abf80f10869`

The accepted data layout remains:

* `evidence.json` is the frozen Phase 6A baseline.
* `phase6a1-triage.json` is a 26-case delta.
* The current machine view is resolved by overlaying the delta onto the baseline.
* Neither artifact is overwritten by the manifest task.

### Phase 6A.1 availability summary

`studies/gkg-semantics-v2/phase6a1-availability.json`

Git blob: `c6aff8a99ab07dfa98e38e1afe0c94b6cbe283c2`

Content SHA-256:

`040ef06815f576d308689fa6de23d9cfbf0166a7c5a2cc4537dae2caf6f4b21a`

### Human identity layer

`studies/gkg-semantics-v2/human-identity-review-results.csv`

Git blob: `6ea6884e73918f7f3d3a52c076885dc409f5aca7`

The human layer must remain separate from machine identity evidence.

### Coverage audit

`docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`

Git blob: `61cf2d3f51a30278e5a04ae032a268ec23f0e58f`

### Overlay implementation

`scripts/phase6a1_recovery.py`

Git blob: `ff52b481d93832c4d0d4c2eba0bc58393915370c`

Accepted implementation SHA-256 from the assessment manifest:

`15fdef25a22ce0232420cd15801ddbce099adbb666a8757bdff42f94b1419a6c`

The manifest implementation should reuse the accepted `resolve()` and `level()` semantics where safe instead of creating a second identity-resolution implementation.

## Independently reproduced pre-recovery state

Expected current machine identity counts:

| State | Count |
|---|---:|
| `identity_confirmed` | 6 |
| `identity_probable_manual_review_required` | 15 |
| `identity_mismatch` | 7 |
| `identity_unresolved` | 92 |
| Total | 120 |

Expected evidence sufficiency:

| Level | Count |
|---|---:|
| E3 | 6 |
| E0 | 114 |

Expected human identity decisions:

| Decision | Count |
|---|---:|
| `SAME_ARTICLE` | 13 |
| `DIFFERENT_ARTICLE` | 2 |
| `INSUFFICIENT_EVIDENCE` | 7 |
| Total reviewed | 22 |

There are zero genuine human semantic reviews.

## Exact six E3 cases

The six accepted E3 cases must remain unchanged before new recovery:

1. `61c7c1dd513d1d62021d93228f909aef8a2d961f3e850dca97c21ac2b45a3642`
2. `9443d204438f5a3213b4c7b39aec856ba8ae66e5a2d383b5e89817bb4a6b1cc5`
3. `374a5d91e1d48f34c1c096ce025537660995161964315da7473ebfd68cf8d2ca`
4. `544d11e2fe2d02e978eb4f6c4e4910a4ca5acd309033e115b587195de2e5b7a1`
5. `a6140896cd33c01e2e14e4fd8f9a44331ddc16f739648a5ffc945d5daa4fb1dc`
6. `3971850d00836d8a487c96f2128ac0ebd040bd5cee818d70c42939f90c377d57`

All six must have no recovery priority tier and must not appear in a recovery batch.

## Coverage matrix

### PROTEST

| Year | E3 | Minimum | Deficit |
|---:|---:|---:|---:|
| 2015 | 0 | 4 | 4 |
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 0 | 4 | 4 |
| 2026 | 0 | 4 | 4 |

Token total: 0 / 24. Deficit: 24.

### FOOD_SECURITY

| Year | E3 | Minimum | Deficit |
|---:|---:|---:|---:|
| 2015 | 1 | 4 | 3 |
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 1 | 4 | 3 |
| 2026 | 3 | 4 | 1 |

Token total: 5 / 24. Deficit: 19.

### WB_2747_UNEMPLOYMENT

| Year | E3 | Minimum | Deficit |
|---:|---:|---:|---:|
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 1 | 4 | 3 |
| 2026 | 0 | 4 | 4 |

Token total: 1 / 24. Deficit: 23.

The overall token-level lower-bound deficit is 66 additional E3 contexts.

For unemployment, the allocated-year minima require 19 additional E3 cases, then four more E3 cases are still required in any allocated unemployment year or years to reach the token total of 24.

## Deterministic overlay contract

The accepted Phase 6A.1 `resolve()` function already enforces the critical overlay invariants:

* the delta case set must equal the expected 26-case target set
* baseline and delta are authenticated before overlay
* `case_id`, `token`, `year`, `cohort`, and `original_url` cannot change
* the original 120-case order is preserved
* evidence sufficiency is recomputed with the accepted `level()` semantics

The manifest implementation should call or reuse these semantics instead of reconstructing them from prose.

## Recovery priority and promotion eligibility are separate dimensions

The deterministic interpretation is:

`recovery_priority_tier` answers whether and how urgently a frozen case is worth further bounded objective recovery.

`promotion_target_excluded` answers whether the current evidence state permits that case to be treated as a promotion target now.

A case may therefore simultaneously be Tier A and promotion-excluded.

This is required for HIR-11 and HIR-15. Both have genuine human `SAME_ARTICLE` judgments in deficient zero-E3 cells, so objective recovery remains high-value. Both currently have machine `identity_mismatch`, so current promotion eligibility remains false until new objective evidence changes the machine state under the frozen contract.

Human review never mutates machine identity and never creates E3.

## Tier assignment contract

For every row after current machine-state resolution:

1. Current E3 cases receive no recovery tier.
2. Human `SAME_ARTICLE` in an E3-deficient allocated-year cell receives Tier A.
3. Among remaining non-E3 cases, a non-mismatch case with an accepted same-document publisher, canonical, or other objective identity signal in a deficient cell receives Tier B.
4. Among remaining non-E3 cases, an unresolved case requiring bounded archive recovery in a deficient cell receives Tier C.
5. Human `INSUFFICIENT_EVIDENCE`, weak/conflicting cases, cases outside a deficient cell, and other residual cases receive Tier D unless a higher rule above applies.

Independently set current promotion exclusion to true when either condition applies:

* machine identity is `identity_mismatch`
* human decision is `DIFFERENT_ARTICLE`

Under the current accepted data, the two human `DIFFERENT_ARTICLE` cases are already a subset of the seven machine mismatches, so the expected union contains seven cases.

## Exact Tier A expectation

All 13 current human `SAME_ARTICLE` cases are in still-deficient allocated-year cells. Therefore Tier A membership is exactly 13 cases under unchanged inputs.

Two of those Tier A cases are simultaneously promotion-excluded:

* HIR-11: `eb1ebf5f941b79628ac2d4238285747436e9d2f612f92e5bba43c89c9187815d`
* HIR-15: `745ce5ea9b3a0e51f50d97462aac8078fa91098c90b12e4e77414578a6310c67`

The companion expected-output baseline contains the full 13-case Tier A set.

## Objective recoverability ordering

Do not invent a numeric score.

Use a lexicographic ordering derived only from accepted evidence semantics:

1. recovery tier
2. year-cell deficit descending
3. current machine evidence state under accepted Phase 6A semantics
4. retained usable response-body or content-hash signal when present
5. accepted protocol method hierarchy
6. stable frozen-sample order

For non-E3 recovery ranking, the relevant current machine ordering is:

1. `identity_probable_manual_review_required`
2. `identity_mismatch`
3. `identity_unresolved`

The mismatch state can rank a recovery attempt while still having `promotion_target_excluded = true`.

Do not create weighted scores for canonical URL, title similarity, publication date, publisher reputation, modern-page accessibility, semantic desirability, or later forecasting usefulness.

If deterministic ranking would require a new scientific criterion outside accepted evidence fields and this preflight contract, stop and escalate to Sol High.

## First bounded recovery batch

The first batch selection rule is:

`Tier A AND year_cell_current_e3 == 0 AND promotion_target_excluded == false`

Under the accepted inputs this produces exactly nine cases:

* HIR-03: `fdf4e8e8fd4387f8734c40cffd6936c0ee5fb1897b6fe378d8225ba0880c4eaa`
* HIR-06: `194bde000746759edf4a787b6c7794c5153068695b5e7df3f74f308a69c1b654`
* HIR-07: `fe06652e1d34ae9808843795bc3d7cbdbb40e7684a82819e68d5a2db6d01d0e0`
* HIR-08: `da06132eebc199a31debb4dec3b1d7d8d219ead51f657ce36e67f791b357281a`
* HIR-09: `edbc803ec616278c7558e78af730e80e569da4259c446e53115641ec1aa59408`
* HIR-16: `c53b0be8810a53fd1c46c0fa9107188b6dbdfc63af09b9cf9c5adabe43e981ec`
* HIR-18: `5c4aa90d7b080ec8063905db4414e74c31c17c3bfee3bd6e9e04c0cdad3400cb`
* HIR-19: `2485b3733f5a41a3244eac8d6fa53fdb4bef5fc7cb95e6177809b76ff7481d46`
* HIR-21: `9f8db6b75f5c0051eed87eb830e6e60dcf761759471b017beb84c5829dce74d7`

Do not hard-code these nine case IDs as the implementation rule. The implementation must derive them from the rule and then compare the resulting membership against the expected-output baseline.

The expected-output baseline intentionally pins batch membership, not array order. Exact order must be recomputed from accepted objective recoverability signals and frozen order.

HIR-11 and HIR-15 remain Tier A conflict-recovery candidates but are excluded from the first promotion-eligible batch while their machine state is still mismatch.

HIR-12 and HIR-13 remain Tier A but have lower immediate year-cell leverage because their cells already contain E3 evidence.

## Expected manifest shape

The implementation should emit one record for every frozen case, including the six E3 cases, so membership preservation can be audited directly.

Minimum recommended fields:

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
* `human_identity_decision`
* `human_identity_confidence`
* `year_cell_e3_count`
* `year_cell_minimum`
* `year_cell_deficit`
* `token_e3_count`
* `token_minimum`
* `token_deficit`
* `recovery_priority_tier`
* `promotion_target_excluded`
* `promotion_exclusion_reason`
* `objective_recoverability_signals`
* `recovery_rationale_codes`
* `allowed_next_recovery_methods`
* immutable source/evidence hash or locator references sufficient for replay

Prefer structured rationale codes over free-form model prose.

Useful codes include:

* `HUMAN_SAME_ARTICLE`
* `ZERO_E3_YEAR_CELL`
* `YEAR_CELL_DEFICIT_4`
* `CURRENT_MACHINE_PROBABLE`
* `CURRENT_MACHINE_MISMATCH`
* `CURRENT_MACHINE_UNRESOLVED`
* `SAME_PUBLISHER_CANONICAL_PRESENT`
* `ARTICLE_METADATA_PRESENT`
* `CONTENT_HASH_PRESENT`
* `HUMAN_INSUFFICIENT_EVIDENCE`
* `HUMAN_DIFFERENT_ARTICLE`

Codes must describe accepted facts. They must not invent evidence.

## Expected regression checks

The later implementation must fail closed unless all applicable checks pass:

1. Exactly 120 manifest rows.
2. Exactly 120 unique frozen case IDs.
3. Frozen case ID set hash matches the accepted reference.
4. No replacement or resampling.
5. Current machine identity counts reproduce 6 / 15 / 7 / 92.
6. Current E3 count is exactly six.
7. The exact six E3 case IDs match the baseline.
8. Human review counts reproduce 13 / 2 / 7.
9. Human judgments do not mutate machine identity or evidence sufficiency.
10. Coverage by token and allocated year exactly reproduces the accepted audit.
11. All 13 human `SAME_ARTICLE` cases receive Tier A while their cells remain deficient.
12. HIR-11 and HIR-15 are Tier A and simultaneously promotion-excluded.
13. Both human `DIFFERENT_ARTICLE` cases are promotion-excluded.
14. All seven current machine mismatches are promotion-excluded.
15. The six E3 cases have no recovery tier and are not recovery targets.
16. The first bounded batch membership is exactly the expected nine-case set under unchanged inputs.
17. Re-running manifest generation on identical inputs produces byte-equivalent canonical machine-readable output, excluding only explicitly non-semantic execution metadata if such metadata is kept outside the canonical manifest.
18. Mutation of `case_id`, `token`, `year`, `cohort`, or `original_url` fails closed.
19. Duplicate case injection fails closed.
20. Automatic E3 promotion from human `SAME_ARTICLE` fails closed.
21. Accepted evidence, delta, protocol, human-review, and frozen-sample artifacts remain byte unchanged.

## What this baseline intentionally does not precompute

The expected-output baseline does not pin:

* Tier B membership or count
* Tier C membership or count
* complete Tier D membership or count
* exact objective-recoverability ordering
* the 120 manifest rows
* future recovery outcomes
* semantic labels
* semantic promotion

Those outputs must be derived from accepted machine evidence by the implementation. Precomputing them here would duplicate the actual task and risk turning the preparation artifact into a second implementation.

## Stop conditions

Stop and escalate rather than guess if any of the following occurs:

* current frozen membership is not exactly 120 unique cases
* the frozen case ID set hash changes
* current E3 is not exactly six
* the exact E3 set changes before authorized recovery
* human counts no longer reproduce 13 / 2 / 7
* coverage differs from the accepted audit
* baseline plus delta cannot be reconciled using accepted overlay semantics
* a proposed ranking requires a new scientific criterion
* any recovery method would require replacement sampling, unrelated search substitution, guessed archive identity, or syndicated substitution
* the task would need to modify accepted machine evidence or human-review artifacts

## Handoff

After this preflight, the remaining manifest work is an L2 deterministic implementation task suitable for GPT-5.6 Terra High.

Recommended implementation footprint:

* `scripts/phase6a_recovery_manifest.py`
* `scripts/test_phase6a_recovery_manifest.py`
* `studies/gkg-semantics-v2/recovery-target-manifest.json`
* `docs/PHASE6A_RECOVERY_TARGET_MANIFEST.md`

Names may be adjusted to existing repository conventions, but the scientific contracts above must remain unchanged.

The implementation should stop after manifest generation, validation, compact summary, and bounded-batch definition. Network evidence recovery remains a separate explicitly authorized task.
