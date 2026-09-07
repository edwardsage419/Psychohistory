# Psychohistory Full Project Integrity and Goal Audit — 2026-09-07

## Scope

This audit reviewed the current authoritative `main` repository across:

* project vision and goal alignment
* current Gate and roadmap logic
* current recovery-manifest task and preflight/oracle chain
* Phase 5/6A/6A.1 evidence semantics and trust boundaries
* human/machine provenance separation
* GKG retrieval, identity and network boundaries
* schema and indicator contracts
* future multi-source, point-in-time, forecast, outcome and evaluation architecture
* offline CI and GitHub workflow supply-chain references
* repository-level governance protections visible through the connected GitHub interface

The audit intentionally did not start network evidence recovery, semantic review, source-family integration, composite-state construction, forecasting, calibration or historical backtesting.

No audit can prove that all possible bugs are absent. The completion claim is limited to: no known blocking correctness or design defect remains in the inspected current scope after the corrections below, subject to the explicitly recorded platform-level repository-protection gap.

## Executive conclusion

Current project direction remains aligned with the accepted north star: heterogeneous public observations -> transparent indicators -> interpretable state/trends -> dated probabilistic forecasts -> independent outcome resolution -> empirical evaluation/calibration -> evidence-aware decision support.

The GKG program remains one candidate media-attention measurement family. It is not the project objective and is not allowed to become an open-ended sunk-cost requirement.

The current scientific Gate remains Gate 3A for the GKG candidate. The deterministic recovery-target manifest remains the correct next bounded implementation task after this audit.

This audit found and repaired several real implementation/governance defects. None of the repairs changes the frozen 120-case sample, accepted machine identity counts, human identity judgments, semantic labels, or production status.

## Current scientific state preserved

Frozen sample:

* 120 cases
* no replacement
* no resampling

Machine identity:

* `identity_confirmed`: 6
* `identity_probable_manual_review_required`: 15
* `identity_mismatch`: 7
* `identity_unresolved`: 92

Evidence sufficiency version `1.0.1`:

* E0: 114
* E1: 3
* E2: 0
* E3: 3
* review-ready E2/E3: 3

Review-ready token coverage:

* `PROTEST`: 0 / 24
* `FOOD_SECURITY`: 2 / 24
* `WB_2747_UNEMPLOYMENT`: 1 / 24

Current lower-bound token deficit: 69, subject also to at least four review-ready contexts per allocated year.

Human identity review remains separate provenance:

* 13 `SAME_ARTICLE`
* 2 `DIFFERENT_ARTICLE`
* 7 `INSUFFICIENT_EVIDENCE`

The current first bounded manifest batch remains mechanically defined as:

`Tier A AND year_cell_review_ready_count == 0 AND promotion_target_excluded == false`

Under unchanged authenticated inputs, the current V2 oracle pins membership at 10 cases.

## Finding 1: accepted Phase 6A.1 method could falsely stop manifest generation

### Defect

The current machine view contains a non-review-ready E1 case with `retrieval_method=canonical_publisher`, an accepted Phase 6A.1 same-publisher method.

Earlier current manifest instructions ranked only the older Phase 6A method vocabulary and required an unmapped non-review-ready method to trigger a stop. The accepted current input could therefore stop deterministic manifest generation even though no new scientific ambiguity existed.

### Repair

`docs/NEXT_ACCEPTED_TASK.md` and `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT_V2.md` now normalize accepted Phase 6A/6A.1 methods for ranking:

* rank 0: `original_publisher`
* rank 1: `same_path_https_candidate`, `canonical_publisher`
* rank 2: `wayback_availability_discovery`
* rank 3: `dated_wayback_capture`
* rank 4: `unavailable` or no successful evidence method

`canonical_publisher` is permitted only when an exact same-publisher canonical/final locator already exists in accepted evidence/protocol provenance. It is explicitly distinct from the deferred `canonical_publisher_archive` path, which remains unauthorized.

No evidence level, identity state, tier-A membership or first-batch membership changed.

## Finding 2: evidence-sufficiency correction trust closure was incomplete

### Defect

Evidence-sufficiency version `1.0.1` depends on the frozen Phase 5 cue/extractor semantics because `gkg_recovery.reviewable_context()` uses the Phase 5 token-cue vocabulary and recovery uses the Phase 5 extractor.

The initial correction contract pinned only the recovery scripts. A later cue/extractor code change could therefore have altered E1/E2/E3 interpretation without necessarily invalidating the correction contract.

### Repair

`studies/gkg-semantics-v2/context-sufficiency-correction.json` is now version `1.0.1` and explicitly binds:

* frozen Phase 5 preregistration
* Phase 6A protocol
* Phase 6A.1 protocol
* `scripts/gkg_semantics.py`
* `scripts/retrieve_gkg_semantics.py`
* `scripts/gkg_recovery.py`
* `scripts/phase6a1_recovery.py`

The V2 manifest oracle and current task/preflight reference these bindings. Offline integrity tests now fail closed on semantic dependency drift.

Historical assessment-manifest implementation pins remain historical provenance and are not rewritten to pretend the original run used later code.

## Finding 3: evidence URI identity ignored non-default ports

### Defect

`gkg_recovery.uri()` previously compared normalized host/path/query while omitting port identity. This could treat a custom-port endpoint as equivalent to the standard endpoint.

The frozen sample uses the accepted public HTTP(S) reference contract, so the defect did not change current 120-case results, but it was an identity-boundary weakness.

### Repair

URI identity now:

* retains accepted normal HTTP/HTTPS/default-port equivalence
* preserves non-default ports as part of URI identity
* rejects archive/evidence identity when a custom port differs from the frozen original

Regression tests cover both normal scheme upgrade and custom-port mismatch.

## Finding 4: new integrity test could fail spuriously on Windows line endings

### Defect

The new correction dependency test initially used `git hash-object <path>` directly against the worktree. Python files are not forced to LF by `.gitattributes`, so a Windows CRLF checkout could produce a false semantic-drift failure.

### Repair

The integrity test now normalizes CRLF to LF before applying the Git blob hash algorithm through `git hash-object --stdin`.

Actual code-content drift remains detectable while line-ending conversion does not create a platform-specific false failure.

## Finding 5: review-ready recovery subset could be mistaken for representative semantic evidence

### Defect

Phase 5 already documented strongly uneven historical article availability and explicitly warned that survivor-only semantic comparison would be biased. It also recorded that English cues and compact-context extraction affect which cases become reviewable.

The 24-per-token and 4-per-year readiness rule is a useful minimum evidence-volume threshold. By itself it does not establish that the recovered E2/E3 subset is representative of all frozen token-positive cases.

Without an explicit later guard, a future workflow could pass readiness and human semantic thresholds on a selected survivor subset and overstate historical validity.

### Repair

Created `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`.

Before any GKG token may enter Gate 5 experimental historical-indicator promotion, Gate 3B/4 work must explicitly address reviewability/recovery selection and missingness. At minimum it must keep full frozen selected denominators and actually reviewed denominators visible and assess reviewability by token/year and relevant source/recovery factors.

Unresolved and unreviewable cases remain in denominator accounting. Favorable semantic rates among surviving reviewed cases cannot erase them.

Recall remains `recall_not_estimated` until a separately defensible relevant-document frame exists.

## Finding 6: risk of project path dependence on GKG

### Defect

A strictly global reading of sequential gates could encourage indefinite effort to make the current GKG candidate succeed before any other source family could be researched. That would conflict with the project north star, which requires heterogeneous evidence families and treats candidate rejection as a valid scientific outcome.

### Repair

The current state, README and roadmap now explicitly state:

* GKG is one candidate media-attention family
* recovery is bounded
* after every separately authorized recovery batch, governance reassesses whether another batch can materially change the scientific decision
* valid outcomes include continued bounded recovery, restricted historical validity/use case, pause pending a genuinely new capability, or rejection of the candidate
* Gates 1-5 normally apply at the relevant source/measurement-candidate lifecycle
* another source family may begin a separately authorized Gate 1/2 lifecycle even if GKG remains limited or rejected
* this does not authorize Gate 6B multi-source state construction

No arbitrary recovery-yield threshold was invented because current evidence does not justify one.

## Finding 7: CI actions used movable major tags

### Defect

The repository uses successful CI as part of acceptance evidence, while GitHub workflows referenced movable major action tags.

### Repair

The current official major-tag targets were resolved and pinned to exact commits for:

* `actions/checkout`
* `actions/setup-python`
* `actions/upload-artifact`

The workflow behavior and Python version remain unchanged. The change reduces supply-chain movement in the CI trust boundary.

## Finding 8: repository-level main protection is not visibly enforced

### Observation

The GitHub rulesets endpoint currently returns no repository rulesets through the connected GitHub interface.

The branch-protection endpoint cannot be inspected through the current managed integration because that endpoint requires administration access and returns 403 to this connection.

Therefore this audit can establish that no repository ruleset is visible, but it cannot conclusively state whether another branch-protection mechanism is configured.

### Remaining platform action

The current connector exposes no repository-administration write action for rulesets/branch protection, so this item cannot be repaired from the current session.

The owner should manually verify repository settings for `main`. Recommended minimum protections are:

* block force pushes to `main`
* block branch deletion
* preserve required CI checks for merge workflows where used
* optionally require pull requests if the development workflow is changed to PR-only operation

Requiring PRs is a workflow choice, not a current scientific requirement. The existing GPT/Codex workflow currently performs bounded direct commits to `main`, so enabling PR-only protection should be an explicit owner decision rather than an implicit audit change.

## Goal-alignment audit

### Project vision

PASS.

The current repository continues to target a long-running falsifiable evidence and forecasting system. Current work is foundational evidence validation, not a replacement product objective.

### Observation versus reality

PASS.

GKG remains a media-attention candidate. Source registry and indicator architecture do not promote media volume into event severity, public opinion or real-world state without further validation.

### Multi-source objective

PASS.

Future source strategy prioritizes independent evidence-generation mechanisms, upstream lineage, point-in-time availability and revision behavior. Provider count is not treated as evidence independence.

### Forecast falsifiability

PASS at design level, future implementation still blocked.

Future architecture requires versioned targets/resolution rules, point-in-time snapshots, immutable issuance, failed-run retention, explicit unresolved outcomes, frozen evaluation cohorts and transparent baselines.

No production forecast engine or schema has been activated prematurely.

### Historical evaluation integrity

PASS at design level, future implementation still blocked.

Current safeguards cover availability-time leakage, revision/vintage leakage, future-fitted transformations, current-LLM historical contamination, retrieval leakage, forecast mutation, hindsight resolution, cohort selection and baseline parity.

### Product sequencing

PASS.

The retired frontend remains retired. Interface/product work is downstream of validated research outputs.

### Cost discipline

PASS.

The project still targets zero/near-zero recurring cost during validation while explicitly refusing to weaken provenance, retention or scientific thresholds merely to save cost.

## Current architecture consistency audit

The future B/C/D design artifacts are mutually compatible in the inspected scope:

* source admission distinguishes reference period, publication/availability time, retrieval time and revision/vintage
* data-model documentation refuses to overload `observation.v1` with future point-in-time semantics
* source independence is based on upstream lineage rather than provider names
* target and resolution semantics precede forecast issuance
* forecast inputs require `available_at <= information_cutoff <= issued_at`
* issued substantive forecasts are immutable
* failed attempts and unresolved outcomes remain visible
* confirmatory evaluation freezes cohort/rules before scoring
* current LLM historical runs are classified as retrospective experiments unless contemporaneous model availability is independently defensible

No reviewed future-design document activates Gate 6A, 6B, 7, 8, 9 or 10 by itself.

## Current task readiness after audit

The deterministic recovery-target manifest remains an L2 task suitable for GPT-5.6 Terra High.

The current task package now explicitly covers:

* frozen membership and trust roots
* Phase 5 cue/extractor dependency pins
* evidence-sufficiency `1.0.1`
* E2/E3 review-ready semantics
* human/machine provenance separation
* exact tier precedence
* promotion exclusion
* accepted Phase 6A/6A.1 method normalization, including `canonical_publisher`
* deterministic output and mutation tests
* 10-case first bounded batch regression oracle
* no network recovery during manifest generation

A new scientific criterion remains a Sol High stop condition rather than something Terra should invent.

## Scientific invariant check

No audit repair changes a frozen historical sample or silently rewrites an old evidence artifact.

Applicable protections remain consistent with:

* I1 no future information
* I2 forecast immutability
* I3 versioned semantics
* I4 historical reproducibility
* I5 independent outcome resolution
* I6 evidence traceability
* I7 observation is not reality
* I8 explicit uncertainty
* I9 no silent historical rewrite
* I10 evaluation integrity
* I11 genuine human evidence remains human
* I12 missing evidence cannot be reasoned into existence

## Final audit status

Subject to successful final offline CI on the audit completion HEAD:

* no known blocking code bug remains in the current Gate 3A/manifest-preparation path
* no known unresolved design defect requires changing the current next task
* project goal alignment is PASS
* GKG sunk-cost/path-dependence risk is explicitly controlled
* survivor/recovery selection risk is explicitly blocked from future semantic promotion
* future multi-source and forecasting designs remain downstream specifications, not authorization
* repository-level main protection remains the only identified platform hardening item that could not be conclusively inspected or changed through the current GitHub integration

The next development action after final CI is the deterministic recovery-target manifest defined in `docs/NEXT_ACCEPTED_TASK.md`.
