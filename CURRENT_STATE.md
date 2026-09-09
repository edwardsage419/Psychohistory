# Psychohistory Current State

Last updated: 2026-09-09

## Project status

Status: `PAUSED`.

Active Psychohistory development and research execution were paused by owner decision on 2026-09-09 as a strategic resource-allocation decision. This pause does not alter accepted scientific evidence, frozen samples, machine identity states, human adjudication, evidence-sufficiency classifications, protocols, invariants, or provenance.

While status remains `PAUSED`, no task described in this file, `docs/NEXT_ACCEPTED_TASK.md`, a roadmap, phase report, issue, or prior chat is authorized for execution solely because it is documented. Substantive work requires an explicit owner reactivation decision first.

The pause decision and reactivation procedure are recorded in `docs/PROJECT_PAUSE.md`.

## Authority

This file is the compact operational state for continuing Psychohistory across devices, ChatGPT conversations, Codex sessions, and model changes.

For project status, prefer evidence in this order:

1. Git history and immutable evidence artifacts
2. This `CURRENT_STATE.md`
3. Accepted phase reports and decision records
4. `SCIENTIFIC_INVARIANTS.md`, `AGENTS.md`, and `docs/DEVELOPMENT_GOVERNANCE.md`
5. ChatGPT memory or conversation context

If this file conflicts with Git evidence, Git evidence wins and this file must be corrected.

Owner development decision as of 2026-09-07: active project governance and design were GPT-led and bounded implementation was performed with Codex before the project pause. The earlier Claude-era product direction is retired and is not an architectural authority unless a specific decision has independently entered the accepted repository evidence/governance chain.

## Project objective

Psychohistory is a long-running falsifiable research and product project intended to observe broad social conditions, detect important trends, produce probabilistic forecasts, preserve outcomes and calibration history, and support evidence-based decisions.

Core pipeline:

public data/news -> normalized observations -> indicators -> state/trends -> probabilistic forecasts -> outcome resolution -> backtesting/calibration -> decision support

The north star remains heterogeneous public observations, transparent indicators, dated forecasts, independent outcome resolution, empirical evaluation, and evidence-aware decision support. GKG is one candidate media-attention family inside that program; recovering GKG is not itself the project objective.

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
* current Gate 3 selection-bias and recovery-pivot safeguard in `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`

Phase 5-6A.1 remain non-production research/evidence-recovery work only. Their acceptance does not promote GKG media-prevalence tokens into validated historical social indicators.

Acceptance merge: `81ea41989fd884633c535e1063bd78e1231d2c5c`.
Acceptance review: `docs/PHASE_5_6A1_ACCEPTANCE_REVIEW.md`.
Human identity results: `studies/gkg-semantics-v2/human-identity-review-results.csv`.
Historical pre-correction coverage audit: `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`.
Current correction contract: `studies/gkg-semantics-v2/context-sufficiency-correction.json`.
Current correction report: `docs/PHASE6A1_CONTEXT_SUFFICIENCY_CORRECTION.md`.
Current Gate 3 guard: `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`.

Historical Phase 6A.1 reports and the original Phase 5-6A.1 acceptance review retain the pre-correction six-E3 snapshot as historical provenance. Their old sufficiency counts and old next-step wording do not override this file or the current correction contract.

## Operational cleanup and hardening on 2026-09-07

The retired V0.2 frontend, static dashboard data, GDELT DOC updater script and scheduled workflow were removed from the active tree. Git history preserves them for provenance.

The intended automation posture is:

* offline tests on pull requests and pushes to `main`
* no standing live-source workflow is required by the current Gate 3A task
* no workflow commits transient monitoring data directly to authoritative `main`

The live `Validate GKG Source` workflow was retired on 2026-09-08 after an Actions audit. It validates only the latest upstream GKG batch and does not advance the frozen historical-evidence gate or the current deterministic manifest task. Its network dependence also created operational noise. `scripts/validate_gkg.py` remains preserved as historical and reusable integration tooling and may be run explicitly outside the standing Actions set if a future authorized source-admission or production-ingestion task requires current live validation.

The preserved GKG validator code is constrained to an HTTPS-only GDELT acquisition boundary with provider-preserving redirects. Evidence URI comparison also preserves non-default ports while retaining the already accepted normal HTTP-to-HTTPS/default-port equivalence. These transport and identity hardenings do not rewrite accepted historical evidence.

## Current gate at pause

Primary scientific gate at the pause point: Gate 3A, historical document identity and evidence sufficiency for the GKG candidate.

The immediate bottleneck at the pause point was objective historical document identity and review-ready context coverage across the frozen 120-case sample. The 22-case identity review is complete, but human `SAME_ARTICLE` judgments remain separate provenance and do not satisfy machine evidence-sufficiency requirements by themselves.

Production forecast implementation was not the current bottleneck.

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

## Selection and missingness limitation

The current 24-per-token and 4-per-allocated-year E2/E3 readiness rule is a minimum evidence-volume condition for later semantic review. It is not evidence that the review-ready subset is representative.

Phase 5 already showed strong historical availability differences and warned that survivor-only semantic comparison would be biased. Successful recovery may remain associated with year, outlet, document survival and the frozen cue/extractor path.

Before any GKG token can enter Gate 5 experimental historical-indicator promotion, the project must perform the selection/missingness analysis defined in `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`. Semantic rates must retain reviewed and full selected denominators, recall remains unestimated, and unresolved cases cannot be dropped merely because they are inconvenient.

Reaching the current readiness threshold may authorize a later independent semantic-review task. It does not by itself authorize indicator promotion.

## Frozen recovery-manifest task

At the pause point, the accepted next task was `docs/NEXT_ACCEPTED_TASK.md`.

Execution is suspended while project status is `PAUSED`. The task contract is preserved unchanged as a recovery point and must not be executed unless the owner explicitly reactivates Psychohistory and confirms that it remains the correct next task.

If reactivated without a superseding accepted decision, execution must use evidence-sufficiency `1.0.1`, review-ready E2/E3 coverage, and the current V2 preparation artifacts:

* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT_V2.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline-v2.json`

The correction contract now pins the Phase 5 preregistration/cue-extractor semantics, Phase 6A/6A.1 protocols, and current recovery implementations required to reproduce evidence sufficiency. Silent semantic dependency drift must fail closed.

The earlier preflight, original recovery-manifest oracle, historical confirmed-context coverage audit, and `docs/CODEX_EXECUTION_READINESS_AUDIT.md` preserve the pre-correction state and are superseded for current execution.

Under unchanged current inputs, the first bounded recovery batch is defined mechanically as:

`Tier A AND year_cell_review_ready_count == 0 AND promotion_target_excluded == false`

The corrected V2 oracle pins membership at 10 cases. The implementation must derive that membership from authoritative inputs rather than hard-code it.

The accepted Phase 6A.1 `canonical_publisher` method is now explicitly normalized in manifest ordering and allowed-method logic. It must not be confused with the deferred Phase 6A `canonical_publisher_archive` method.

Network recovery is not authorized by the manifest-generation task.

## Candidate lifecycle and pivot rule

Gates 1 through 5 are interpreted at the relevant source/measurement-candidate level unless a specification explicitly states a project-wide prerequisite.

Failure or restriction of GKG does not constitute failure of Psychohistory and does not permanently block research on other source families. A separately authorized future source may begin its own Gate 1/2 admission and measurement-validation path while GKG remains limited or rejected.

After the deterministic manifest and after each separately authorized bounded GKG network-recovery batch, governance must reassess whether another batch can materially change the scientific decision. Valid outcomes include continuing bounded recovery, restricting the valid period/use case, pausing pending a genuinely new capability, or rejecting the candidate while preserving all evidence.

No numeric recovery-yield threshold is invented at this stage. Missing evidence never justifies lowering identity, context, reviewer or semantic standards.

## Human dependencies

Remaining human dependencies include:

* later independent genuine human semantic review after sufficient objective review-ready context exists
* owner approval for consequential semantic or production promotion

LLMs must not satisfy a protocol requirement for genuine human review.

## Blocked work

Until the project is explicitly reactivated and the applicable evidence gates are satisfied, do not begin or promote:

* production forecasting
* production composite-state construction
* semantic promotion of the experimental GKG tokens into authoritative historical indicators
* calibration claims based on the unresolved measurement foundation
* historical backtests that treat unresolved measurement semantics as ground truth
* independent semantic review before the frozen review-ready coverage threshold is met

The project pause additionally blocks execution of the frozen recovery-manifest task and any new evidence-recovery batch until explicit reactivation.

## Reactivation path

There are no active development actions while project status is `PAUSED`.

Before substantive work resumes:

1. Record an explicit owner reactivation decision.
2. Review `docs/PROJECT_PAUSE.md` and reassess the project against material changes in AI, forecasting, measurement science, data availability, competition, and intended product value since 2026-09-09.
3. Revalidate this repository state and immutable evidence against Git history.
4. Decide explicitly whether `docs/NEXT_ACCEPTED_TASK.md` remains the correct next task.
5. If it remains correct, generate the deterministic recovery-target manifest over the complete frozen 120-case sample using the corrected E2/E3 review-ready definition and pinned semantic dependencies.
6. Preserve all historical evidence artifacts and human identity judgments; do not rewrite the frozen sample or machine identity states.
7. Continue only through separately authorized bounded tasks and the existing scientific gates.

## Model routing if reactivated

* deterministic coverage/target-manifest generation: L1-L2, Terra Medium/High
* bounded archive/retrieval engineering under the accepted protocol: L2, Terra High
* semantic, selection-bias or historical validity judgment after evidence exists: L4, Sol High
* unresolved system-level methodology after serious Sol analysis: L5, Astra High

Do not use stronger models to compensate for missing historical evidence or missing human review.

## Startup procedure

A new GPT or Codex session inspecting or considering continuation of Psychohistory should begin with:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `docs/PROJECT_PAUSE.md`
4. `SCIENTIFIC_INVARIANTS.md`
5. `docs/DEVELOPMENT_GOVERNANCE.md`
6. `docs/NEXT_ACCEPTED_TASK.md` only after explicit owner reactivation
7. only the phase reports, decisions, code and tests relevant to the bounded task

If project status is still `PAUSED`, stop before implementation or research execution unless the owner has explicitly requested reactivation. Inspection, summarization, comparison, and reuse analysis do not themselves constitute reactivation.

Do not scan the whole repository unless the task genuinely requires repository-wide review.

## Update rule

Update this file only when project state materially changes: accepted research enters `main`, a gate changes, a major evidence blocker is resolved/discovered, a human dependency changes, the next authoritative priority changes, the project is paused/reactivated, or an operational change materially affects how future sessions interpret or execute the project.
