# Next Accepted Task

Last updated: 2026-09-06

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

## Required work

1. Resolve the accepted Phase 6A baseline plus the Phase 6A.1 26-case delta into one read-only current identity-status view for all 120 frozen cases.
2. Compute E3 coverage by token and allocated year.
3. For every non-E3 frozen case, assign a deterministic recovery-priority tier without changing identity status:
   * Tier A: human `SAME_ARTICLE` and located in an E3-deficient year cell.
   * Tier B: non-mismatch case with an existing same-document publisher/canonical candidate or other objective identity signal, located in an E3-deficient year cell.
   * Tier C: unresolved case requiring bounded archive recovery, located in an E3-deficient year cell.
   * Tier D: human `INSUFFICIENT_EVIDENCE` or other weak/conflicting candidate that may become useful only if new objective evidence appears.
   * Excluded-from-promotion-target: human `DIFFERENT_ARTICLE` or objective `identity_mismatch`; preserve as negative evidence and do not substitute another article.
4. Rank within a tier first by year-cell deficit, then by objective recoverability. Use stable frozen-sample order as the final tie-breaker.
5. Emit a machine-readable manifest containing at minimum:
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
   * recovery rationale
   * allowed next recovery method(s) under the frozen protocol
   * immutable source/evidence locator or hash reference needed for replay
6. Emit a compact human-readable summary showing the first bounded recovery batch.
7. Keep the first recovery batch small enough to review independently. Prefer targets that can close or materially reduce zero-E3 year cells; do not simply select the easiest modern pages.
8. Validate mechanically that:
   * all manifest case IDs belong to the frozen 120
   * there are no duplicate case IDs
   * no replacement/sample substitution occurred
   * the six currently accepted E3 cases remain E3 and are not targeted for recovery
   * the two human `DIFFERENT_ARTICLE` cases are not promotion targets
   * machine evidence artifacts and human-review artifacts are not overwritten
9. Stop after manifest generation and bounded-batch definition unless the task explicitly authorizes network recovery.

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
* Coverage counts reproduce `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`.
* Priority rules are deterministic and reproducible.
* All 13 human `SAME_ARTICLE` judgments remain separate provenance fields, not E3 promotions.
* Both human `DIFFERENT_ARTICLE` cases remain negative evidence and are excluded from promotion targeting.
* Manifest exposes enough provenance to replay why every case received its priority.
* No semantic review, semantic promotion, composite construction, forecast implementation, calibration or backtesting begins.

## Stop conditions

Stop and escalate to Sol High if:

* the accepted Phase 6A baseline and Phase 6A.1 delta cannot be resolved without changing evidence semantics
* the frozen sample membership does not reconcile to exactly 120 unique cases
* current E3 coverage does not reconcile to exactly six
* a proposed recovery method would violate the accepted identity hierarchy, archive-distance rule, network trust policy, provenance rules, or no-substitution rule
* deterministic target ranking requires inventing a new scientific criterion not already implied by the frozen protocol and coverage audit

Otherwise complete with Terra High or equivalent deterministic tooling.

## After this task

Run bounded evidence recovery against the accepted target manifest, recompute E3 coverage mechanically, and repeat only while preserving the frozen sample and protocol. Independent semantic review remains blocked until every token has at least 24 E3 contexts and every allocated year has at least four.
