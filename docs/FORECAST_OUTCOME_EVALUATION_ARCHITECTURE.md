# Forecast, Outcome and Evaluation Architecture

Date: 2026-09-07
Status: accepted future architecture specification. This document does not activate Gate 7, Gate 8, Gate 9 or Gate 10 and does not authorize production forecasting, historical backtesting or calibration.

## Purpose

Define the conceptual contracts for future Psychohistory forecasts, targets, issuance, outcome resolution, baselines and evaluation before implementation begins.

This specification sits downstream of the current measurement gates and must be read with:

* `SCIENTIFIC_INVARIANTS.md`
* `docs/SCIENTIFIC_RISK_REGISTER.md`
* `docs/FUTURE_EVALUATION_SAFEGUARDS.md`
* `docs/DECISION_2026_09_07_POINT_IN_TIME_EVALUATION.md`

The goal is to make future predictive claims falsifiable, point-in-time valid, immutable and comparable with transparent baselines.

## 1. Separation of concepts

Future implementation must keep these entities separate:

1. target definition
2. forecast method
3. forecast run attempt
4. issued forecast
5. forecast correction
6. resolution rule
7. outcome resolution
8. baseline forecast
9. evaluation cohort
10. evaluation result
11. calibration analysis
12. decision-support output

A convenient implementation may store some entities together physically, but their semantics and provenance must remain independently identifiable.

A forecast is a probabilistic claim issued under a fixed information set. It is not an indicator value, a narrative scenario, a post-hoc explanation, a model run that failed before issuance, or a user decision.

## 2. Forecast classes

The first future implementation should support only forecast classes with explicit resolution and scoring semantics.

### 2.1 Binary event forecast

Question form: whether a versioned event condition will occur within a defined horizon.

Required forecast output:

* probability in `[0,1]`
* target definition version
* horizon start/end
* geography/entity scope where applicable
* resolution rule version

Typical scoring candidates:

* Brier score
* log score

A binary target must still allow the resolution state to remain unresolved or ambiguous when evidence does not satisfy the rule.

### 2.2 Directional or categorical trend forecast

Question form: whether a versioned quantity or state will increase, decrease, remain stable, or enter another preregistered category over a defined horizon.

Required forecast output:

* probability distribution over mutually exclusive predefined categories
* exact trend/category definition
* reference baseline period
* horizon
* resolution rule version

The category boundaries must be defined before issuance. They cannot be chosen after observing the outcome.

### 2.3 Continuous forecast

Future optional class for a numerical target with a predictive distribution or interval.

Do not add this class until the target's point-in-time measurement, revision policy, evaluation metric and interval/distribution semantics are explicit.

A single point estimate without uncertainty is not the preferred formal Psychohistory forecast object.

### 2.4 Scenario analysis

Scenario generation remains an analytical artifact, not a formal probabilistic forecast unless each scenario has a defined probability semantics, target, horizon and resolution contract.

This distinction prevents narrative scenario quality from being confused with forecast accuracy.

## 3. Target definition contract

Every formal forecast points to an immutable versioned target definition.

A target definition should contain or bind at minimum:

* `target_id`
* `target_version`
* human-readable name
* formal question semantics
* forecast class
* unit/category space
* geography/entity rule
* reference-period rule
* horizon rule
* positive/negative or category criteria
* measurement source hierarchy
* revision/vintage policy for the target observation
* ambiguity policy
* unresolved policy
* resolution deadline rule
* target-definition content hash

Target definitions should be reusable across many forecasts when semantics are genuinely identical.

Any change that can alter which outcome is considered correct requires a new target version.

Examples requiring a new version include:

* changing an event threshold
* changing geographic scope
* changing the measurement series
* changing a trend category boundary
* changing the reference period
* changing the treatment of revised outcome data

## 4. Resolution rule contract

A target definition may bind a separate resolution rule object when the resolution logic is complex or reusable.

A resolution rule should define:

* `resolution_rule_id`
* version
* allowed outcome state space
* source hierarchy
* source conflict policy
* observation/vintage rule
* resolution deadline
* evidence sufficiency threshold
* ambiguity handling
* unresolved handling
* content hash

The rule must exist before or at forecast issuance for confirmatory forecasting.

A later improved rule can be created as a new version, but old forecasts remain bound to the rule under which they were issued unless an explicitly versioned methodological study compares alternative rules.

## 5. Information snapshot contract

Every issued forecast binds the exact admissible information set used to produce it.

The information boundary includes:

* `information_cutoff`
* feature snapshot root
* evidence snapshot root
* source/vintage identities
* transformation-state references
* model/method configuration
* retrieval/tool policy

Every forecast input must satisfy the applicable point-in-time rules in `docs/FUTURE_EVALUATION_SAFEGUARDS.md`.

A feature snapshot and evidence snapshot must be immutable or externally authenticated. Internal hashes alone cannot serve as their own trust root.

## 6. Forecast method contract

A forecast method is the reproducible procedure that converts an admissible information snapshot into a predictive output.

A method definition should preserve:

* `method_id`
* version
* method family
* implementation/code identity
* required input contract
* output semantics
* fitted-state requirements
* randomness policy
* seed policy where relevant
* model/provider identity where relevant
* prompt/configuration identity for AI methods
* tool/retrieval policy
* known limitations
* content hash

Material changes require a new method version.

Changing only a deployment timestamp or run identifier does not necessarily create a new method version. Changing prompt instructions, model version, feature construction, training/fitting logic, probability mapping, retrieval permissions or post-processing does.

## 7. Forecast run attempts

Future implementation must distinguish a model/method run attempt from an issued forecast.

A run attempt may end as:

* `issued`
* `failed_pre_issue`
* `aborted_pre_issue`
* `invalid_pre_issue`

Failed attempts are retained for operational and selection-bias audit when consequential.

A failed run must never be silently rerun until a favorable answer appears and then represented as though only one run occurred.

If retries are allowed, the retry policy must be documented, and the issued forecast must identify the accepted attempt.

## 8. Forecast issuance contract

Issuance is the event that converts a prepared predictive result into an immutable scientific record.

An issued forecast should bind at minimum:

* `forecast_id`
* `issued_at`
* `information_cutoff`
* forecast class
* target ID/version/hash
* horizon start/end
* geography/entity scope where applicable
* probability or predictive distribution
* method ID/version/hash
* model identity/version where applicable
* prompt/configuration hash where applicable
* feature snapshot root
* evidence snapshot root
* resolution rule ID/version/hash
* code version
* run-attempt reference
* substantive content hash
* issuance status

Required ordering:

`all admissible input available_at <= information_cutoff <= issued_at`

An issued forecast cannot be backdated.

Issuance should be atomic at the scientific-record level: the probability, target, method and snapshot references must all refer to one coherent issuance state.

## 9. Forecast lifecycle

Recommended lifecycle states:

* `prepared`
* `issued`
* `corrected`
* `superseded_for_future_use`
* `resolved`
* `unresolved_closed`

`prepared` is not part of the formal forecast registry until issuance.

`corrected` does not mutate the original. It indicates that a linked correction record exists.

`superseded_for_future_use` means a forecast or method should no longer guide future operation, but the historical prediction remains scoreable under its original contract if its target later resolves.

Do not use a lifecycle state to erase a poor forecast from evaluation.

## 10. Correction contract

Corrections are append-only.

A correction should record:

* correction ID
* original forecast ID
* correction timestamp
* correction type
* reason
* fields affected
* corrected representation where applicable
* whether scientific scoring remains based on the original forecast
* reviewer/authority

A correction to non-substantive metadata may preserve the original scoring object.

A change to probability, horizon, target semantics or other substantive prediction content creates a new forecast or methodological version. It cannot retroactively replace the original prediction.

## 11. Outcome resolution states

Resolution must support more than binary resolved/unresolved bookkeeping.

Recommended generic states:

* `pending`
* `resolved`
* `ambiguous`
* `insufficient_evidence`
* `source_conflict`
* `resolution_window_expired_unresolved`

The resolved outcome itself is target-specific and stored separately from the resolution status.

For a binary target, a `resolved` record may carry `true` or `false`.

For a categorical target, it may carry one of the predefined categories.

The system must not convert ambiguity, source conflict or missing evidence into a convenient negative outcome.

## 12. Outcome resolution record

A resolution record should bind:

* `resolution_id`
* forecast ID
* target ID/version/hash
* resolution rule ID/version/hash
* resolution status
* resolved outcome when applicable
* resolved-at timestamp
* evidence references/hashes
* target-data vintage/reference used
* resolver identity/type
* notes/reason codes
* resolution content hash

Resolution records are append-only.

If a factual error is later discovered, create a correction or superseding resolution record with provenance. Do not silently rewrite the original resolution.

## 13. Resolver independence

Forecast generation and resolution should be separated as much as practical.

Minimum safeguards:

* the resolver receives the target and rule, not a request to maximize forecast score
* resolution evidence is independent of the forecast rationale when possible
* outcome criteria are fixed before the outcome is inspected for confirmatory evaluation
* unresolved remains an allowed result

Machine resolution may be used for deterministic cases if the source and rule permit it. Human resolution should be used where interpretation is genuinely required, with provenance and uncertainty preserved.

## 14. Baseline architecture

Baselines are first-class forecast methods, not ad-hoc numbers calculated only after AI results are known.

Each baseline should have:

* method ID/version
* target compatibility
* admissible information set
* fitting policy
* output probability semantics
* code/version
* evaluation eligibility

Initial baseline families should remain simple and transparent:

* historical base rate
* persistence
* recent-trend rule
* simple regression/classification method
* market-implied probability where valid and point-in-time available

A sophisticated method may only claim modeling advantage when compared with competent baselines under compatible information sets.

## 15. Evaluation cohort manifest

Every confirmatory evaluation should operate on a frozen cohort manifest.

A cohort manifest should bind:

* `evaluation_cohort_id`
* version
* creation/freeze timestamp
* forecast registry snapshot root
* cohort date range
* eligible forecast classes
* target IDs/versions
* method versions
* horizon classes
* inclusion rules
* exclusion rules
* unresolved treatment
* failed-run treatment
* duplicate/dependency grouping policy
* primary metrics
* secondary metrics
* baseline methods
* minimum sample or claim restrictions
* content hash

The manifest must be frozen before confirmatory result inspection.

Changing cohort rules after results are visible creates a new exploratory or separately versioned evaluation.

## 16. Evaluation result contract

An evaluation result should preserve:

* evaluation ID
* cohort manifest ID/version/hash
* scorer/evaluation-method version
* evaluated-at timestamp
* forecast-registry snapshot root
* resolution snapshot root
* counts for issued/eligible/resolved/unresolved/excluded/failed
* exclusion reason counts
* primary metric results
* baseline results
* uncertainty intervals where justified
* dependency/effective-sample caveats
* content hash

No score should be reported without enough information to reconstruct its denominator.

## 17. Scoring by forecast class

### Binary forecasts

Preferred primary candidates:

* Brier score
* log score

Optional diagnostics:

* calibration/reliability plots
* discrimination/AUC when scientifically appropriate
* calibration slope/intercept when sample size supports it

### Categorical forecasts

Use a proper scoring rule compatible with the full probability distribution.

Do not reduce probabilistic category forecasts to accuracy alone.

### Continuous forecasts

Metric choice must match the issued distribution/interval semantics and be defined before confirmatory evaluation.

Do not introduce continuous scoring until the forecast object actually preserves enough distribution information.

## 18. Calibration architecture

Calibration is an evaluation view over immutable forecasts and resolved outcomes. It is not a process that retroactively adjusts historical probabilities.

Future calibration analyses should record:

* target and horizon grouping
* forecast method/model versions
* cohort manifest
* binning or calibration-estimator rule
* nominal sample size
* dependency concerns
* uncertainty method

If a calibration model is later used to transform future forecast probabilities, that transformation becomes part of a new forecast method version and must itself be fit only on past admissible data.

## 19. Forecast registry completeness

The registry must support reconstruction of every formal forecast that was issued.

It should never contain only currently active or successfully resolved forecasts.

Required completeness concepts:

* all issued forecasts
* linked corrections
* lifecycle state
* resolution status
* method/version
* target/version
* issuance timestamp

Failed pre-issue attempts may live in a separate run-attempt registry but must remain available when they are relevant to retry/selection-bias analysis.

## 20. AI forecast provenance

For an AI-based forecast, preserve enough configuration to understand what system produced the result.

Required or strongly preferred fields include:

* provider/system family
* exact model identifier/version where exposed
* reasoning/configuration level where consequential and recordable
* system/project instruction version or hash
* task prompt/template version or hash
* structured input/evidence snapshot root
* tool permissions
* tool-call/evidence log reference
* retrieval corpus/index reference where used
* temperature/randomness settings where exposed and consequential
* run-attempt identity
* any human override or probability editing

Do not store private chain-of-thought as a scientific requirement. Preserve reproducible inputs, outputs, evidence, configurations and concise rationale/provenance instead.

## 21. Human override contract

If a human changes a machine-generated probability before formal issuance, the issued forecast must identify that fact.

Recommended fields:

* `human_override_applied`
* pre-override model probability/distribution reference
* issued probability/distribution
* override reason category
* operator identity/reference

This allows later evaluation of model-only, human-only and combined performance without rewriting history.

## 22. Forecast rationale

A concise rationale may be preserved for transparency, but it is secondary to the formal probability and evidence snapshot.

The rationale must not become an unversioned source of target semantics or resolution criteria.

Later explanations may be appended, but they cannot change what the original forecast meant.

## 23. Dependency and repeated-forecast handling

Multiple forecasts can concern the same underlying future event or overlapping horizons.

The registry should preserve a dependency/grouping key when known, such as:

* event family
* target episode
* rolling horizon series
* shared outcome instance

Evaluation must not automatically treat repeated forecasts on one event as independent samples.

## 24. Failed and unavailable outcomes

Forecasts with unavailable or unresolved outcomes remain in the registry.

Evaluation policy may exclude them from a particular proper score when the target cannot be resolved, but must report them in cohort accounting.

A high unresolved rate is itself a target/resolution quality signal and should remain visible.

## 25. Decision support separation

Investment or personal decision-support outputs may consume forecasts, but they are separate records.

A decision-support record should preserve:

* referenced forecasts
* evidence snapshot
* assumptions
* user constraints where applicable
* decision/recommendation produced
* uncertainty
* model/method version

Future utility evaluation may ask whether decisions were useful, but decision outcomes must not be substituted for forecast-resolution outcomes.

## 26. Minimum future object families

Before Gate 7-9 can be considered implemented, expect versioned contracts for at least:

1. target definition
2. resolution rule
3. forecast method
4. forecast run attempt
5. issued forecast
6. forecast correction
7. outcome resolution
8. evaluation cohort manifest
9. evaluation result

Point-in-time observation/vintage and feature/evidence snapshot contracts are prerequisites rather than optional extras.

Exact file names and storage format remain implementation decisions.

## 27. Implementation sequence

When upstream scientific gates eventually permit this work, use this order:

### Gate 7A: target and resolution semantics

Design target-definition and resolution-rule schemas first.

Reason: a probability is meaningless until the event/trend being predicted is fixed and resolvable.

### Gate 7B: point-in-time snapshot and method contracts

Implement admissible input, feature/evidence snapshot and method/version contracts.

### Gate 7C: forecast issuance registry

Implement append-only issuance, correction, lifecycle and run-attempt records.

### Gate 8: outcome resolution

Implement resolution under the already-bound target/rule versions.

### Gate 9A: frozen cohort evaluation

Implement evaluation cohort manifests and proper scoring.

### Gate 9B: calibration and baseline comparison

Add calibration diagnostics, dependence handling and fair baseline comparisons only after registry completeness and resolution integrity are demonstrated.

### Gate 10: AI forecasting evaluation

Evaluate AI methods only after the same registry and evaluation machinery can falsify them against transparent baselines.

## 28. Acceptance conditions for a future implementation

A future Gate 7-9 implementation is not scientifically complete unless it can demonstrate at minimum:

* no post-cutoff input enters an issued historical simulation
* an issued forecast cannot be mutated without detection
* target and resolution versions are immutable and bound at issuance
* unresolved outcomes remain representable
* every issued forecast remains discoverable
* correction records preserve originals
* evaluation cohort membership is replayable
* excluded forecasts have explicit reasons
* baseline information parity is checked
* score denominators are reconstructable
* AI provenance is sufficient to identify the evaluated method
* applicable adversarial tests from `docs/FUTURE_EVALUATION_SAFEGUARDS.md` pass

## 29. Current project boundary

None of the object families above are authorized for production implementation today.

The current accepted project bottleneck remains Gate 3A historical evidence recovery over the frozen GKG semantic sample.

This architecture exists to prevent future implementation from inventing forecast semantics after predictive results become available.
