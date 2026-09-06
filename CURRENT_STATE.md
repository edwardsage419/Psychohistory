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

This file is intentionally compact. It is not a substitute for phase reports, manifests, or Git history.

## Project objective

Psychohistory is a long-running falsifiable research and product project intended to:

* observe broad social and macro conditions
* detect emerging important trends
* produce probabilistic forecasts of major future developments
* support investment and long-horizon personal decisions with structured evidence
* preserve forecasts and evaluate them through resolution, scoring, calibration, and backtesting

Core pipeline:

public data/news -> normalized observations -> indicators -> state/trends -> probabilistic forecasts -> outcome resolution -> backtesting/calibration -> decision support

## Accepted baseline

Authoritative production baseline: `main`.

Accepted work on `main`: Phase 1 through Phase 4 foundation.

The accepted foundation includes source/data work, lossless and provenance-oriented processing, and experimental GKG media-prevalence measurement. Accepted numerical media-prevalence outputs must not be interpreted as direct real-world severity or risk.

## Unaccepted development work

Active research/development branch: `codex/project-reset-architecture`.

The branch contains later semantic-audit and historical-evidence-recovery work, including Phase 5, Phase 6A, and Phase 6A.1 work. This work is research evidence and candidate implementation until independently reviewed and accepted into the authoritative baseline.

Do not infer that a completed report on the development branch has been promoted to `main`.

## Current gate

Primary current gate: semantic and historical stability, with independent evidence validation still incomplete.

The current bottleneck is evidence quality, historical document identity, and genuine human validation. It is not production forecast implementation.

## Current evidence state

Phase 5 established an auditable cross-year semantic-audit method but did not establish historical semantic stability. Human semantic validation remains incomplete and recall is not estimated.

Phase 6A established bounded historical evidence recovery and identity/import contracts but recovered insufficient confirmed review context.

Phase 6A.1 targeted the 26 previously probable/conflicting identity cases. The frozen 120-case sample currently has:

* 6 confirmed E3 contexts
* 15 probable identities requiring genuine human identity review
* 7 conflicting identities requiring genuine human identity review or stronger independent evidence
* 92 unresolved/unavailable cases
* 0 genuine human semantic reviews
* 0 LLM semantic reviews counted as human evidence

The exact accepted numbers must be rechecked against the relevant branch reports before a consequential promotion decision.

## Human dependencies

Current genuine-human dependencies include:

* targeted identity review for the remaining probable/conflicting cases where the protocol requires human judgment
* later independent genuine human semantic review when sufficient context exists
* owner approval for consequential promotion into the authoritative baseline

LLMs must not be used to satisfy a protocol requirement for genuine human review.

## Blocked work

Until the applicable evidence gates are satisfied, do not begin or promote:

* production forecasting
* production composite-state construction
* semantic promotion of the experimental GKG tokens into authoritative historical indicators
* calibration claims based on an unvalidated measurement foundation
* historical backtests that treat unresolved measurement semantics as ground truth

Engineering experiments may be performed only when explicitly bounded and clearly marked non-authoritative.

## Next recommended actions

1. Perform an L4 acceptance review of Phase 5 through Phase 6A.1 before merging any of that work into `main`.
2. Keep acceptance review separate from new feature development.
3. Resolve genuine-human identity-review dependencies for the remaining targeted cases.
4. Improve bounded historical archive/evidence recovery only where it can add independent evidence without weakening provenance, identity, TLS, peer, or replay requirements.
5. After sufficient reviewable context exists, obtain genuine independent semantic review under the preregistered protocol.
6. Reassess cross-year semantic stability only after the evidence and reviewer gates are actually satisfied.

## Model routing for immediate work

* Phase 5-6A.1 acceptance review: L4, GPT-5.6 Sol High
* bounded archive/retrieval engineering under an approved protocol: L2, GPT-5.6 Terra High
* deterministic review-packet/import implementation: L1-L2, Terra Medium/High
* semantic or historical validity judgment: L4, Sol High
* unresolved system-level methodology after serious Sol analysis: L5, GPT-6 Astra High

Do not use Astra to compensate for missing historical evidence or missing human review.

## Startup procedure

A new GPT or Codex session continuing Psychohistory should begin with:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `SCIENTIFIC_INVARIANTS.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. only the phase reports, decisions, code, and tests relevant to the requested task

Do not scan the whole repository unless the task genuinely requires repository-wide review.

## Update rule

Update this file only when project state materially changes, such as:

* a phase or research result is accepted into `main`
* the active development branch changes
* the current gate changes
* a major evidence blocker is resolved or newly discovered
* a human dependency changes
* the next authoritative development priority changes

Routine commits and implementation details do not require an update.
