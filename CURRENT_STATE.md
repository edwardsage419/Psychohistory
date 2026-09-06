# Psychohistory Current State

Last updated: 2026-09-06

## Authority

This file is the compact operational state for continuing Psychohistory across devices, ChatGPT conversations, Codex sessions, and model changes.

For project status, prefer evidence in this order:

1. Git history and immutable evidence artifacts
2. This `CURRENT_STATE.md`
3. Accepted phase reports and decision records
4. `SCIENTIFIC_INVARIANTS.md`, `AGENTS.md`, and `docs/DEVELOPMENT_GOVERNANCE.md`
5. ChatGPT memory or conversation context

If this file conflicts with Git evidence, Git evidence wins and this file must be corrected.

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
* Phase 6A.1 targeted 26-case identity-recovery delta and sufficiency assessment
* genuine-human identity adjudication results for the 22 Phase 6A.1 cases requiring human judgment
* mechanical confirmed-context coverage audit against the frozen Phase 6A readiness rule

Phase 5-6A.1 remain **non-production research/evidence-recovery work only**. Their acceptance does not promote GKG media-prevalence tokens into validated historical social indicators.

Acceptance merge: `81ea41989fd884633c535e1063bd78e1231d2c5c`.
Acceptance review: `docs/PHASE_5_6A1_ACCEPTANCE_REVIEW.md`.
Human identity results: `studies/gkg-semantics-v2/human-identity-review-results.csv`.
Coverage audit: `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`.

## Current gate

Primary current gate: semantic and historical stability with independent evidence validation incomplete.

The immediate bottleneck is objective historical document identity/evidence coverage across the frozen 120-case sample. The previously pending 22-case human identity review is complete, but human `SAME_ARTICLE` judgments do not satisfy the frozen E3 identity contract by themselves.

Production forecast implementation is not the current bottleneck.

## Current evidence state

Phase 5 remains `continue_semantic_validation`.

Phase 6A remains `continue_evidence_recovery`.

Phase 6A.1 targeted human identity review is complete. Its human layer contains:

* 13 `SAME_ARTICLE`
* 2 `DIFFERENT_ARTICLE`
* 7 `INSUFFICIENT_EVIDENCE`

These are genuine-human identity judgments stored separately from machine evidence. They do not silently rewrite `phase6a1-triage.json`, `evidence.json`, or E3 status.

The frozen 120-case sample still has only:

* 6 confirmed E3 contexts
* 114 non-E3 contexts
* 0 genuine human semantic reviews
* 0 LLM semantic reviews counted as human evidence

Current E3 distribution:

* `PROTEST`: 0 / required 24
* `FOOD_SECURITY`: 5 / required 24
* `WB_2747_UNEMPLOYMENT`: 1 / required 24

The frozen readiness rule requires at least 24 identity-confirmed contexts per token and at least 4 per allocated year. The current lower-bound deficit is 66 additional E3 contexts, subject also to year-distribution constraints.

Historical semantic stability remains unproven. Recall remains unestimated. Independent semantic review is not yet authorized by the frozen Phase 6A readiness rule.

## Human dependencies

Completed genuine-human dependency:

* targeted identity review of the 22 Phase 6A.1 probable/conflicting cases

Remaining genuine-human dependencies:

* later independent genuine human semantic review after sufficient objective E3 context exists
* owner approval for consequential semantic/production promotion

LLMs must not satisfy a protocol requirement for genuine human review.

## Blocked work

Until the applicable evidence gates are satisfied, do not begin or promote:

* production forecasting
* production composite-state construction
* semantic promotion of the experimental GKG tokens into authoritative historical indicators
* calibration claims based on the unresolved measurement foundation
* historical backtests that treat unresolved measurement semantics as ground truth
* full independent semantic review before the frozen Phase 6A confirmed-context readiness threshold is met

## Next recommended actions

1. Build a deterministic recovery-target manifest over the complete frozen 120-case sample, preserving original sample membership and ranking targets by allocated-year E3 deficit and objective recoverability.
2. Prioritize the 13 human `SAME_ARTICLE` cases for objective recovery where they can fill deficient year cells, without treating the human judgment itself as E3 evidence.
3. Continue bounded publisher/archive recovery for additional frozen cases, especially cells with zero E3 coverage.
4. Preserve `DIFFERENT_ARTICLE`, failed attempts, unresolved evidence and human judgments as visible provenance; do not replace frozen cases with substitute articles.
5. Recompute E3 coverage mechanically after each bounded recovery batch.
6. Start genuine independent semantic review only after every token reaches >=24 E3 contexts and every allocated year reaches >=4 E3 contexts under the frozen protocol.
7. Reassess cross-year semantic stability only after evidence and reviewer gates are satisfied.

## Model routing for immediate work

* deterministic coverage/target-manifest generation: L1-L2, Terra Medium/High
* bounded archive/retrieval engineering under the frozen protocol: L2, Terra High
* semantic or historical validity judgment after evidence exists: L4, Sol High
* unresolved system-level methodology after serious Sol analysis: L5, Astra High

Do not use Astra to compensate for missing historical evidence or missing human review.

## Startup procedure

A new GPT or Codex session continuing Psychohistory should begin with:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `SCIENTIFIC_INVARIANTS.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. only the phase reports, decisions, code and tests relevant to the bounded task

Do not scan the whole repository unless the task genuinely requires repository-wide review.

## Update rule

Update this file only when project state materially changes: accepted research enters `main`, a gate changes, a major evidence blocker is resolved/discovered, a human dependency changes, or the next authoritative priority changes.
