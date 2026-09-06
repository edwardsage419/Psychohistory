# Next Accepted Task

Last updated: 2026-09-06

## Goal

Integrate the already-reviewed Phase 5 through Phase 6A.1 research/evidence-recovery work from `codex/project-reset-architecture` into the current `main` baseline without changing scientific conclusions or starting new development.

## Classification

Risk: L2 for repository integration, with L4 acceptance semantics already reviewed separately.

Recommended execution model if Codex is used: GPT-5.6 Terra High.

Astra: not authorized.

## Preconditions already satisfied

* Static L4 acceptance review completed and recorded in `docs/PHASE_5_6A1_ACCEPTANCE_REVIEW.md`.
* Reviewed development HEAD: `2adf167d283e4be47e63b8fe90c890676467d1fa`.
* Final reviewed development HEAD offline CI succeeded.
* No accepted Phase 4 indicator outputs or production behavior are modified by the 22 development commits.
* Scientific status remains bounded: Phase 5 `continue_semantic_validation`, Phase 6A `continue_evidence_recovery`, Phase 6A.1 `ready_for_targeted_human_identity_review`.

## Required work

1. Integrate the reviewed development history onto the current `main` without force-moving or replacing `main`.
2. Preserve all current governance files and their latest contents:
   * `AGENTS.md`
   * `CURRENT_STATE.md`
   * `SCIENTIFIC_INVARIANTS.md`
   * `docs/DEVELOPMENT_GOVERNANCE.md`
   * `docs/PHASE_5_6A1_ACCEPTANCE_REVIEW.md`
3. Preserve the reviewed Phase 5, Phase 6A and Phase 6A.1 code, tests, reports and compact evidence artifacts exactly unless a merge conflict requires a documented mechanical reconciliation.
4. Add durable decision-log entries for:
   * Phase 6A: `continue_evidence_recovery`
   * Phase 6A.1: `ready_for_targeted_human_identity_review`
   * neither authorizes semantic promotion, Phase 6B, composites, forecasting, calibration or historical backtesting
5. Update `CURRENT_STATE.md` so Phase 5 through Phase 6A.1 are described as accepted non-production research/evidence-recovery work on `main`, while the scientific blockers remain unchanged.
6. Run the complete offline suite on the exact integrated HEAD.
7. Verify that accepted Phase 4 outputs and protected files remain unchanged relative to their accepted hashes where the existing preservation checks cover them.
8. Stop. Do not perform archive recovery, human review, semantic promotion, new indicator work, forecasting or unrelated cleanup in this task.

## Acceptance criteria

* Integration is based on reviewed development HEAD `2adf167d...` or an explicitly documented mechanical descendant containing no new scientific development.
* Current governance files are preserved.
* Phase 5/6A/6A.1 scientific recommendations are unchanged.
* `CURRENT_STATE.md` accurately reflects the new accepted repository state.
* Decision log records Phase 6A and 6A.1 status.
* Complete offline tests pass on the exact integrated HEAD, apart from documented platform-specific skips already accepted by policy.
* No production indicator, composite, forecast, calibration or historical-backtest activation occurs.

## Stop conditions

Stop immediately and escalate to Sol High if:

* a merge conflict requires changing scientific semantics, protocol rules, trust roots, sample membership, evidence identity, or historical outputs
* reviewed evidence artifacts fail preservation checks
* the exact integrated test suite fails for a reason that cannot be explained as a mechanical integration issue
* integration would require discarding current governance/state files

Otherwise complete the bounded repository integration with Terra High or equivalent deterministic tooling.

## After this task

The next scientific dependency remains genuine targeted human identity review for the remaining 15 probable and seven conflicting cases, with separately bounded evidence recovery where objective evidence can improve identity without weakening trust requirements.
