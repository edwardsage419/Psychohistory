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
5. `studies/gkg-semantics-v2/phase6a-protocol.json`
6. `studies/gkg-semantics-v2/evidence.json`
7. `studies/gkg-semantics-v2/phase6a1-triage.json`
8. `studies/gkg-semantics-v2/phase6a1-availability.json`
9. `studies/gkg-semantics-v2/human-identity-review-results.csv`
10. `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`

Do not scan unrelated repository history or production code unless a preservation check requires it.

## Execution preflight aids

After independently reading and validating the authoritative inputs above, read:

* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline.json`

These two files are accepted execution aids and regression oracles. They are not evidence authorities and must never be used as their own trust roots.

The implementation must first recompute the frozen state, coverage, tiers and bounded-batch membership from the authoritative inputs. Only then compare the derived results against the expected-output baseline.

If the authoritative inputs disagree with the preflight baseline, do not force the implementation to match the baseline. Stop, preserve the discrepancy, and determine whether the accepted evidence state changed or the preflight artifact is stale.

## Frozen facts

The 120-case sample remains immutable.

Current objective E3 coverage is:

* `PROTEST`: 0 / 24 required
* `FOOD_SECURITY`: 5 / 24 required
* `WB_2747_UNEMPLOYMENT`: 1 / 24 required
* total: 6 / 72 required

The current lower-bound deficit is 66 additional E3 contexts, with additional allocated-year distribution constraints.

The completed genuine-human identity layer contains:

* 13 `SAME_ARTICLE`
* 2 `DIFFERENT_ARTICLE`
* 7 `INSUFFICIENT_EVIDENCE`

Human `SAME_ARTICLE` is a recovery-priority signal only. It does not automatically create E3.

## Deterministic interpretation

Recovery priority and current promotion eligibility are separate dimensions.

`recovery_priority_tier` describes whether and how urgently the original frozen case is worth further bounded objective recovery.

`promotion_target_excluded` describes whether the current machine/human evidence state excludes the case from promotion targeting now.

A case may therefore be Tier A and simultaneously promotion-excluded. Under the current accepted inputs this applies to HIR-11 and HIR-15 because they have genuine human `SAME_ARTICLE` judgments in deficient year cells while their current machine state remains `identity_mismatch`.

Human review never mutates machine identity and never creates E3. Only new objective evidence satisfying the frozen identity contract can change the machine state.

Objective recoverability must use a deterministic lexicographic order derived only from accepted evidence semantics. Do not invent weighted scores or new scientific criteria. The detailed ordering contract is recorded in `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT.md`.

## Required work

1. Resolve the accepted Phase 6A baseline plus the Phase 6A.1 26-case delta into one read-only current identity-status view for all 120 frozen cases.
2. Compute E3 coverage by token and allocated year.
3. For every non-E3 frozen case, assign a deterministic recovery-priority tier without changing identity status:
   * Tier A: human `SAME_ARTICLE` and located in an E3-deficient year cell.
   * Tier B: non-mismatch case with an existing same-document publisher/canonical candidate or other objective identity signal, located in an E3-deficient year cell.
   * Tier C: unresolved case requiring bounded archive recovery, located in an E3-deficient year cell.
   * Tier D: human `INSUFFICIENT_EVIDENCE` or other weak/conflicting candidate that may become useful only if new objective evidence appears, unless a higher-priority rule already applies.
4. Independently set `promotion_target_excluded = true` for human `DIFFERENT_ARTICLE` or current objective `identity_mismatch`. Preserve these cases as visible evidence and never substitute another article.
5. Rank within a tier first by year-cell deficit, then by objective recoverability under the accepted evidence hierarchy. Use stable frozen-sample order as the final tie-breaker. Do not invent a numeric recoverability score.
6. Emit a machine-readable manifest containing at minimum:
   * case_id
   * token
   * year
   * source
   * original_url
   * current machine identity status
   * current E3 state
   * human identity decision if present
   * year-cell current E3 count
   * year-cell minimum deficit
   * token total E3 count
   * token total deficit
   * recovery priority tier
   * promotion target exclusion state and reason
   * recovery rationale
   * allowed next recovery method(s) under the frozen protocol
   * immutable source/evidence locator or hash reference needed for replay
7. Emit a compact human-readable summary showing the first bounded recovery batch.
8. Define the first bounded recovery batch mechanically as Tier A cases in zero-E3 year cells that are not currently promotion-excluded. Under unchanged accepted inputs, independently derived membership must match the nine-case set in the expected-output baseline. Do not hard-code those nine IDs as the selection algorithm.
9. Validate mechanically that:
   * all manifest case IDs belong to the frozen 120
   * there are no duplicate case IDs
   * no replacement/sample substitution occurred
   * the six currently accepted E3 cases remain E3 and are not targeted for recovery
   * all 13 human `SAME_ARTICLE` cases remain separate human provenance and receive Tier A while their cells remain deficient
   * HIR-11 and HIR-15 are Tier A while still promotion-excluded under current machine mismatch
   * the two human `DIFFERENT_ARTICLE` cases are not promotion targets
   * all current machine `identity_mismatch` cases are not promotion targets
   * machine evidence artifacts and human-review artifacts are not overwritten
10. Stop after manifest generation and bounded-batch definition unless the task explicitly authorizes network recovery.

## Scientific invariants to enforce

Applicable invariants include I3, I4, I6, I8, I9, I11 and I12.

In particular:

* no human judgment may silently rewrite machine evidence
* no failed or unresolved case may be replaced by a more convenient article
* no missing historical evidence may be inferred into existence
* no target-selection rule may use semantic label desirability or later forecasting utility
* no current-page similarity alone may be treated as historical identity confirmation

## Acceptance criteria

* Exact 120-case membership preserved.
* Current E3 count remains exactly 6 before new recovery.
* The exact six E3 case IDs reproduce the expected-output baseline.
* Coverage counts reproduce `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`.
* Priority rules are deterministic and reproducible.
* All 13 human `SAME_ARTICLE` judgments remain separate provenance fields, not E3 promotions.
* Tier A membership reproduces the expected 13-case set under unchanged inputs.
* HIR-11 and HIR-15 remain Tier A while current promotion eligibility is false.
* Both human `DIFFERENT_ARTICLE` cases remain negative evidence and are excluded from promotion targeting.
* All seven current machine mismatches are excluded from promotion targeting.
* First bounded-batch membership reproduces the expected nine-case set under unchanged inputs.
* Manifest exposes enough provenance to replay why every case received its priority.
* The generated canonical machine-readable output is deterministic for identical inputs.
* No semantic review, semantic promotion, composite construction, forecast implementation, calibration or backtesting begins.

## Stop conditions

Stop and escalate to Sol High if:

* the accepted Phase 6A baseline and Phase 6A.1 delta cannot be resolved without changing evidence semantics
* the frozen sample membership does not reconcile to exactly 120 unique cases
* current E3 coverage does not reconcile to exactly six
* the exact six E3 case IDs differ from the independently accepted baseline
* human identity counts do not reconcile to 13 / 2 / 7
* coverage does not reconcile to the accepted audit
* the authoritative inputs disagree with the preflight oracle and the difference cannot be explained as a stale preparation artifact
* a proposed recovery method would violate the accepted identity hierarchy, archive-distance rule, network trust policy, provenance rules, or no-substitution rule
* deterministic target ranking requires inventing a new scientific criterion not already implied by the frozen protocol, coverage audit and accepted preflight clarification

Otherwise complete with Terra High or equivalent deterministic tooling.

## After this task

Run bounded evidence recovery against the accepted target manifest only after explicit authorization, recompute E3 coverage mechanically, and repeat only while preserving the frozen sample and protocol. Independent semantic review remains blocked until every token has at least 24 E3 contexts and every allocated year has at least four.
