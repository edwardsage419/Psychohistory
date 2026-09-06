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

Phase 5-6A.1 are accepted as **non-production research/evidence-recovery work only**. Their acceptance does not promote GKG media-prevalence tokens into validated historical social indicators.

Acceptance merge: `81ea41989fd884633c535e1063bd78e1231d2c5c`.
Acceptance review: `docs/PHASE_5_6A1_ACCEPTANCE_REVIEW.md`.

## Current gate

Primary current gate: semantic and historical stability with independent evidence validation incomplete.

The bottleneck is historical document identity, evidence availability and genuine human validation. Production forecast implementation is not the current bottleneck.

## Current evidence state

Phase 5 remains `continue_semantic_validation`.

Phase 6A remains `continue_evidence_recovery`.

Phase 6A.1 is `ready_for_targeted_human_identity_review`.

The frozen 120-case sample currently has:

* 6 confirmed E3 contexts
* 15 probable identities requiring genuine human identity review
* 7 conflicting identities requiring genuine human identity review or stronger independent evidence
* 92 unresolved/unavailable cases
* 0 genuine human semantic reviews
* 0 LLM semantic reviews counted as human evidence

Historical semantic stability is unproven. Recall is unestimated. Six E3 contexts are insufficient to launch the planned full independent semantic review.

## Human dependencies

Current genuine-human dependencies:

* targeted identity review of the remaining 15 probable and 7 conflicting cases where the protocol requires human judgment
* later independent genuine human semantic review once sufficient context exists
* owner approval for consequential semantic/production promotion

LLMs must not satisfy a protocol requirement for genuine human review.

## Blocked work

Until the applicable evidence gates are satisfied, do not begin or promote:

* production forecasting
* production composite-state construction
* semantic promotion of the experimental GKG tokens into authoritative historical indicators
* calibration claims based on the unresolved measurement foundation
* historical backtests that treat unresolved measurement semantics as ground truth

## Next recommended actions

1. Prepare the 15 probable and 7 conflicting cases for genuine targeted human identity review using the accepted evidence packet.
2. Perform genuine human identity review without allowing LLM output to count as the human judgment.
3. Separately improve bounded archive/evidence recovery where objective evidence can improve unresolved cases without weakening provenance, identity, TLS, peer or replay requirements.
4. After sufficient confirmed context exists, obtain genuine independent semantic review under the preregistered protocol.
5. Reassess cross-year semantic stability only after evidence and reviewer gates are satisfied.

## Model routing for immediate work

* human identity-review packet preparation/import tooling: L1-L2, Terra Medium/High
* bounded archive/retrieval engineering under an approved protocol: L2, Terra High
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
