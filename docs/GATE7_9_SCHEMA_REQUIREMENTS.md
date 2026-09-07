# Gate 7-9 Schema Requirements

Date: 2026-09-07
Status: future implementation requirements. No production schema is created by this document.

## Purpose

Translate `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md` into a fail-closed checklist for future schema design and implementation.

These requirements deliberately avoid choosing exact JSON Schema file names, storage technology or database layout. The contracts should be designed only when upstream gates authorize implementation.

## Global rules

All future Gate 7-9 contracts must:

* use explicit schema versions
* reject unknown required semantics rather than guessing them
* preserve immutable content identities for substantive records
* preserve external or independently trusted roots where self-authentication would be circular
* distinguish timestamps with different meanings
* keep missing, ambiguous, unresolved and failed states explicit
* avoid silently changing old records when rules or data improve
* bind consequential derived records to the exact upstream versions used

## R1. Target definition schema

Must represent:

* target ID
* target version
* forecast class
* formal target semantics
* outcome/category space
* geography/entity rule
* reference-period rule
* horizon rule
* target measurement/source rule
* target vintage/revision rule where applicable
* ambiguity policy
* unresolved policy
* resolution deadline rule
* content hash
* status such as experimental/active/retired where useful

Validation requirements:

* version required
* category states unique and explicit
* binary targets cannot silently imply unresolved = false
* target semantics cannot be changed in place
* content hash must cover all fields that affect resolution/scoring meaning

## R2. Resolution rule schema

Must represent:

* rule ID/version
* compatible target IDs/versions or compatibility contract
* source hierarchy
* source conflict policy
* allowed resolution statuses
* evidence sufficiency rule
* resolution deadline
* revision/vintage selection rule
* ambiguity/unresolved handling
* content hash

Validation requirements:

* no forced binary fallback unless target contract explicitly requires and justifies it
* source hierarchy cannot be omitted for a rule that depends on external evidence
* later rule versions cannot transparently replace the version bound by an old forecast

## R3. Forecast method schema

Must represent:

* method ID/version
* method family
* compatible forecast classes
* required inputs
* code/implementation identity
* model identity where applicable
* prompt/configuration identity where applicable
* fitting/training-state reference where applicable
* randomness/seed policy where applicable
* retrieval/tool policy
* probability/post-processing semantics
* limitations
* content hash

Validation requirements:

* material model/prompt/feature/probability changes require a new version
* a method requiring fitted state must bind that state or reject issuance
* a method using tools/retrieval must declare permitted tool context

## R4. Forecast run-attempt schema

Must represent:

* attempt ID
* method ID/version
* start/end timestamp
* information cutoff
* input snapshot references
* run status
* failure/abort reason where applicable
* output reference if successful
* random seed/configuration where applicable
* tool/evidence log reference where applicable

Allowed terminal states should include at least:

* issued
* failed_pre_issue
* aborted_pre_issue
* invalid_pre_issue

Validation requirements:

* retries create new attempt IDs
* attempt history cannot be collapsed into only the successful retry when retry selection may matter scientifically

## R5. Issued forecast schema

Must represent:

* forecast ID
* issued-at timestamp
* information cutoff
* forecast class
* target ID/version/hash
* horizon start/end
* geography/entity scope if applicable
* probability or full predictive distribution
* method ID/version/hash
* model identity/version where applicable
* prompt/configuration hash where applicable
* feature snapshot root
* evidence snapshot root
* resolution rule ID/version/hash
* code version
* run-attempt reference
* substantive content hash
* issuance/lifecycle status

Validation requirements:

* all probability values valid for forecast class
* categorical probability distribution is complete and normalized within declared tolerance
* horizon is valid and target-compatible
* `information_cutoff <= issued_at`
* all bound point-in-time inputs pass admissibility validation
* target and resolution hashes match independently supplied trusted definitions
* forecast cannot authenticate its own target/method/evidence roots merely by repeating their hashes
* substantive mutation after issuance fails validation
* backdated issuance is prohibited

## R6. Forecast correction schema

Must represent:

* correction ID
* original forecast ID
* correction timestamp
* correction type
* reason
* affected fields
* authority/reviewer reference
* corrected metadata or linked replacement forecast where applicable
* scoring consequence
* content hash

Validation requirements:

* original forecast remains present and unchanged
* probability/horizon/target changes cannot be disguised as metadata correction
* correction timestamp must be after original issuance

## R7. Point-in-time feature/evidence snapshot contract

Must represent or bind:

* snapshot ID/root
* creation/close timestamp
* information cutoff
* member observations/features/evidence
* each member's admissible availability/vintage identity
* transformation-state references
* source trust roots
* code/version where derived

Validation requirements:

* every member satisfies `available_at <= information_cutoff`
* future-fitted transform state is rejected
* current revised substitute for missing old vintage is rejected
* snapshot membership cannot change after forecast issuance
* self-contained resealing without external trust roots must not validate an altered upstream history

## R8. Outcome resolution schema

Must represent:

* resolution ID
* forecast ID
* target ID/version/hash
* resolution rule ID/version/hash
* resolution status
* outcome if resolved
* resolved-at timestamp
* evidence references/hashes
* target data vintage/reference
* resolver identity/type
* reason/notes
* content hash
* correction/supersession link where applicable

Resolution statuses must support at least:

* pending
* resolved
* ambiguous
* insufficient_evidence
* source_conflict
* resolution_window_expired_unresolved

Validation requirements:

* resolved outcome is valid under target state space
* unresolved statuses do not require a fabricated outcome
* rule and target versions match the forecast binding
* a correction appends; it does not overwrite prior resolution

## R9. Evaluation cohort manifest schema

Must represent:

* cohort ID/version
* freeze timestamp
* forecast-registry snapshot root
* date range
* eligible forecast classes
* target IDs/versions
* method versions
* horizon grouping
* inclusion rules
* exclusion rules
* unresolved treatment
* failed-run treatment
* dependency/grouping policy
* primary metrics
* secondary metrics
* baseline methods
* claim/sample restrictions
* content hash

Validation requirements:

* cohort manifest cannot depend on outcome scores already calculated in the same confirmatory experiment
* every exclusion maps to a predefined reason/policy
* all issued forecasts in the registry snapshot are either eligible, explicitly excluded, or outside scope with reproducible logic

## R10. Evaluation result schema

Must represent:

* evaluation ID
* cohort manifest ID/version/hash
* scorer/method version
* evaluation timestamp
* forecast-registry snapshot root
* resolution snapshot root
* issued count
* eligible count
* resolved count
* unresolved count
* excluded count
* failed-run count where relevant
* exclusion reason counts
* scoreable denominator
* primary metric values
* baseline results
* uncertainty/dependency metadata
* content hash

Validation requirements:

* denominator reconstructable from the frozen cohort and resolution snapshot
* metric implementation/version explicit
* incompatible target or resolution versions cannot be pooled silently
* baseline comparison must carry information-parity metadata

## R11. Calibration analysis schema

If calibration is represented separately, it must bind:

* evaluation/cohort reference
* forecast classes
* target/horizon groupings
* method/model versions
* binning or calibration estimator
* nominal sample size
* dependency/effective-sample notes
* uncertainty method
* result values
* code/method version

Validation requirements:

* calibration analysis cannot mutate issued forecasts
* any learned calibration transform used prospectively becomes a new forecast-method component with causal fitting provenance

## R12. Baseline method requirements

Baselines should use the same forecast-method contract where practical.

Every baseline must identify:

* allowed point-in-time inputs
* fitting state/window
* probability semantics
* compatible targets
* implementation version

Validation requirements:

* no current revised history in a historical baseline unless admissible vintage is established
* no weaker information set passed off as a fair model comparison without explicit classification

## R13. AI provenance requirements

For AI forecast methods, future contracts must support:

* provider/system family
* exact model identifier/version when exposed
* prompt/template hash
* project/system instruction hash where consequential
* structured input snapshot
* retrieval/tool policy
* tool/evidence log reference
* output before human override
* issued output after override
* override flag and reason
* run-attempt identity

Do not require private chain-of-thought storage.

A concise rationale can be stored separately from the formal forecast object.

## R14. Historical experiment classification

Any future evaluation/backtest record must identify the historical experiment class:

* genuine_contemporaneous_forecast
* faithful_historical_replay
* retrospective_model_experiment

Validation requirements:

* a current LLM cannot be marked genuine contemporaneous merely because the prompt limits explicit evidence to an old date
* live current retrieval prevents strict historical replay unless a defensible frozen historical retrieval environment exists

## R15. Dependency grouping

Future forecast/evaluation contracts need a way to represent repeated or dependent forecasts.

Possible fields/concepts:

* target episode ID
* event family ID
* rolling-series ID
* shared outcome ID
* dependency group ID

Evaluation code must not infer independence solely from unique forecast IDs.

## R16. Registry completeness checks

Before scoring, validation must prove:

* every issued forecast in registry scope is accounted for
* corrections do not replace originals
* unresolved forecasts remain present
* superseded forecasts remain historical records
* evaluation exclusions are explicit
* failed pre-issue attempts are retained where the accepted policy requires them for selection-bias audit

## R17. Cross-object referential integrity

Future validators should fail closed on:

* unknown target version
* unknown resolution rule version
* unknown method version
* mismatched content hash
* missing snapshot root
* duplicate forecast ID
* duplicate correction ID
* duplicate resolution ID
* resolution attached to incompatible target/rule
* evaluation referring to mutable/unfrozen cohort
* missing trusted upstream definition when self-authentication would be circular

## R18. No silent migration rule

If a future schema successor changes scientific meaning:

* preserve old records
* write an explicit migration/compatibility policy
* distinguish lossless mechanical migration from semantic reinterpretation
* do not rewrite old forecast, target, resolution or evaluation objects in place solely to satisfy a new schema

## R19. Suggested adversarial-test mapping

When implementation begins, minimum mappings should include:

* target/resolution: `FCT-003`, `RES-001`, `RES-002`
* point-in-time snapshot: `PTI-001` through `PTI-006`
* forecast issuance: `FCT-001`, `FCT-002`
* evaluation: `EVAL-001` through `EVAL-005`
* AI provenance: `AI-001` through `AI-003`
* source independence: `SRC-001`
* semantic continuity: `SEM-001`

The test definitions live in `docs/FUTURE_EVALUATION_SAFEGUARDS.md`.

## R20. Recommended implementation order

Do not begin with a forecast JSON schema in isolation.

Recommended sequence:

1. point-in-time observation/vintage successor contract where required
2. target definition
3. resolution rule
4. feature/evidence snapshot
5. forecast method
6. run attempt
7. issued forecast
8. correction
9. outcome resolution
10. evaluation cohort manifest
11. evaluation result
12. calibration analysis

Each step should receive deterministic validators and adversarial tests before downstream use.

## Current boundary

These are future requirements only.

No current `schemas/*.json` file should be added merely to mirror this document while Gate 3A remains unresolved. A schema becomes useful only when its bounded implementation task is scientifically authorized and testable.
