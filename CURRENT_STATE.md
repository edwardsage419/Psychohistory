# Psychohistory Current State

Last updated: 2026-09-07

## Authority

This file is the compact operational state for continuing Psychohistory across devices, ChatGPT conversations, Codex sessions, and model changes.

For project status, prefer evidence in this order:

1. Git history and immutable evidence artifacts
2. This `CURRENT_STATE.md`
3. Accepted phase reports and decision records
4. `SCIENTIFIC_INVARIANTS.md`, `AGENTS.md`, and `docs/DEVELOPMENT_GOVERNANCE.md`
5. ChatGPT memory or conversation context

If this file conflicts with Git evidence, Git evidence wins and this file must be corrected.

Owner development decision as of 2026-09-07: active project governance and design are GPT-led and bounded implementation is performed with Codex. The earlier Claude-era product direction is retired and is not an architectural authority unless a specific decision has independently entered the accepted repository evidence/governance chain.

## Project objective

Psychohistory is a long-running falsifiable research and product project intended to observe broad social conditions, detect important trends, produce probabilistic forecasts, preserve outcomes and calibration history, and support evidence-based decisions.

Core pipeline:

public data/news -> normalized observations -> indicators -> state/trends -> probabilistic forecasts -> outcome resolution -> backtesting/calibration -> decision support

## Accepted baseline

Authoritative baseline: `main`.

Accepted on `main`:

* Phase 1-4 data/measurement foundation
* Phase 5 preregistered semantic-audit method and frozen 120-reference sample
* Phase 6A bounded historical evidence-recovery infrastructure and evidence
* Phase 6A.1 targeted 26-case identity-recovery delta
* completed model-assisted human identity review with final human adjudication for the 22 cases requiring identity review
* historical confirmed-context coverage audit
* evidence-sufficiency correction version `1.0.1`, which fixes the E1 versus E2/E3 boundary without changing frozen membership or machine identity

Phase 5-6A.1 remain non-production research/evidence-recovery work only. Their acceptance does not promote GKG media-prevalence tokens into validated historical social indicators.

Acceptance merge: `81ea41989fd884633c535e1063bd78e1231d2c5c`.
Acceptance review: `docs/PHASE_5_6A1_ACCEPTANCE_REVIEW.md`.
Human identity results: `studies/gkg-semantics-v2/human-identity-review-results.csv`.
Historical pre-correction coverage audit: `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`.
Current correction contract: `studies/gkg-semantics-v2/context-sufficiency-correction.json`.
Current correction report: `docs/PHASE6A1_CONTEXT_SUFFICIENCY_CORRECTION.md`.

## Operational cleanup on 2026-09-07

The retired V0.2 frontend, static dashboard data, GDELT DOC updater script and scheduled workflow were removed from the active tree. Git history preserves them for provenance.

The intended automation posture is:

* offline tests on pull requests and pushes to `main`
* read-only live GKG integration validation at low frequency plus manual dispatch
* no scheduled workflow that commits transient monitoring data directly to authoritative `main`

The live GKG validator has also been tightened to an HTTPS-only GDELT acquisition boundary with provider-preserving redirects. This changes transport safety only and does not rewrite accepted historical evidence.

## Current gate

Primary current gate: Gate 3A, historical document identity and evidence sufficiency.

The immediate bottleneck is objective historical document identity and review-ready context coverage across the frozen 120-case sample. The 22-case identity review is complete, but human `SAME_ARTICLE` judgments remain separate provenance and do not satisfy machine evidence-sufficiency requirements by themselves.

Production forecast implementation is not the current bottleneck.

## Current machine identity state

The frozen 120-case sample remains immutable.

Current resolved machine identity counts remain:

* `identity_confirmed`: 6
* `identity_probable_manual_review_required`: 15
* `identity_mismatch`: 7
* `identity_unresolved`: 92

The evidence-sufficiency correction did not change any of these machine identity states.

## Current evidence-sufficiency state

Evidence-sufficiency version: `1.0.1`.

Current counts are:

* E0: 114
* E1: 3
* E2: 0
* E3: 3

E1 means document identity is confirmed but the retained compact context is insufficient for semantic review. The earlier version `1.0.0` incorrectly allowed a non-empty manual fallback paragraph to satisfy the E1 versus E2/E3 boundary. Three previously counted E3 cases are therefore correctly classified as E1 under version `1.0.1`.

Review-ready context means E2 or E3. E2 remains valid for an identity-confirmed archive/equivalent context under the accepted protocol; E3 remains valid for an identity-confirmed original/same-publisher context. Current review-ready total is 3.

Current review-ready token coverage:

* `PROTEST`: 0 / required 24
* `FOOD_SECURITY`: 2 / required 24
* `WB_2747_UNEMPLOYMENT`: 1 / required 24

The lower-bound token deficit is therefore 69 additional review-ready contexts, subject also to the frozen requirement of at least 4 review-ready contexts per allocated year.

Historical semantic stability remains unproven. Recall remains unestimated. Independent semantic review is not yet authorized.

## Human identity layer

The completed model-assisted human identity review with final human adjudication contains:

* 13 `SAME_ARTICLE`
* 2 `DIFFERENT_ARTICLE`
* 7 `INSUFFICIENT_EVIDENCE`

This identity-review layer is not independent or blinded semantic review. It remains physically and semantically separate from machine evidence.

Human `SAME_ARTICLE` may affect deterministic recovery priority under the accepted manifest rules. It never creates E2 or E3 and never mutates machine identity status.

There are still:

* 0 independent human semantic reviews counted toward the later semantic-validation gate
* 0 LLM semantic reviews counted as human evidence

## Current recovery-manifest task

The current accepted task is `docs/NEXT_ACCEPTED_TASK.md`.

Execution must use evidence-sufficiency `1.0.1`, review-ready E2/E3 coverage, and the V2 preparation artifacts:

* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT_V2.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline-v2.json`

The earlier preflight, original recovery-manifest oracle, historical confirmed-context coverage audit, and `docs/CODEX_EXECUTION_READINESS_AUDIT.md` preserve the pre-correction state and are superseded for current execution.

Under unchanged current inputs, the first bounded recovery batch is defined mechanically as:

`Tier A AND year_cell_review_ready_count == 0 AND promotion_target_excluded == false`

The corrected V2 oracle pins membership at 10 cases. The implementation must derive that membership from authoritative inputs rather than hard-code it.

Network recovery is not authorized by the manifest-generation task.

## Human dependencies

Remaining human dependencies include:

* later independent genuine human semantic review after sufficient objective review-ready context exists
* owner approval for consequential semantic or production promotion

LLMs must not satisfy a protocol requirement for genuine human review.

## Blocked work

Until the applicable evidence gates are satisfied, do not begin or promote:

* production forecasting
* production composite-state construction
* semantic promotion of the experimental GKG tokens into authoritative historical indicators
* calibration claims based on the unresolved measurement foundation
* historical backtests that treat unresolved measurement semantics as ground truth
* independent semantic review before the frozen review-ready coverage threshold is met

## Next recommended actions

1. Generate the deterministic recovery-target manifest over the complete frozen 120-case sample using the corrected E2/E3 review-ready definition.
2. Preserve all historical evidence artifacts and human identity judgments; do not rewrite the frozen sample or machine identity states.
3. Prioritize recovery targets according to `docs/NEXT_ACCEPTED_TASK.md`, including the 13 human `SAME_ARTICLE` cases where their deficient cells justify Tier A.
4. Preserve `DIFFERENT_ARTICLE`, failed attempts, unresolved evidence and machine mismatches as visible provenance; do not replace frozen cases with substitute articles.
5. After explicit authorization for bounded network recovery, recompute review-ready coverage mechanically after each accepted batch.
6. Begin independent semantic review only after every token reaches at least 24 review-ready E2/E3 contexts and every allocated year reaches at least 4.
7. Reassess cross-year semantic stability only after evidence and reviewer gates are satisfied.

## Model routing for immediate work

* deterministic coverage/target-manifest generation: L1-L2, Terra Medium/High
* bounded archive/retrieval engineering under the frozen protocol: L2, Terra High
* semantic or historical validity judgment after evidence exists: L4, Sol High
* unresolved system-level methodology after serious Sol analysis: L5, Astra High

Do not use stronger models to compensate for missing historical evidence or missing human review.

## Startup procedure

A new GPT or Codex session continuing Psychohistory should begin with:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `SCIENTIFIC_INVARIANTS.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. `docs/NEXT_ACCEPTED_TASK.md`
6. only the phase reports, decisions, code and tests relevant to the bounded task

Do not scan the whole repository unless the task genuinely requires repository-wide review.

## Update rule

Update this file only when project state materially changes: accepted research enters `main`, a gate changes, a major evidence blocker is resolved/discovered, a human dependency changes, the next authoritative priority changes, or an operational change materially affects how future sessions interpret or execute the project.