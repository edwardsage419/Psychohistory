# Psychohistory Scientific Risk Register

Date: 2026-09-07
Status: cross-project scientific governance artifact. This register does not advance the current Gate 3 work and does not authorize forecasting, backtesting, calibration, composite-state construction, or new source integration.

## Purpose

Record failure modes that can make a technically reproducible Psychohistory result scientifically invalid.

The register complements `SCIENTIFIC_INVARIANTS.md`. The invariants remain authoritative. Risk IDs below are operational interpretations used to design future schemas, tests, reviews, and stop conditions.

Existing GKG work already has strong controls for source hashing, replay, quarantine, evidence identity, frozen samples, semantic provenance, and human/machine separation. The largest remaining design risks concern future point-in-time data, source revisions, forecast issuance, AI historical evaluation, outcome resolution, and evaluation methodology.

## Severity

* `CRITICAL`: can invalidate a historical forecast, backtest, calibration result, or major scientific claim.
* `HIGH`: can materially bias state estimates, comparisons, or evaluation.
* `MEDIUM`: can distort interpretation or reduce reproducibility but is normally detectable before a final claim.

A CRITICAL unresolved risk blocks the applicable future gate.

## Risk register

### SR-01. Information-availability leakage

Severity: CRITICAL

Applicable invariants: I1, I4, I10.

Failure: a historical simulation uses a value because its reference period is in the past even though the value was published or became available after the simulated forecast timestamp.

Example: a 2025 GDP estimate published in 2026 is used in a 2025 forecast simulation.

Required control:

* preserve reference period separately from publication/availability time
* require `available_at <= forecast_issued_at` for every historical feature
* fail closed when exact availability is required but cannot be established

Current status: not yet implemented as a generic point-in-time contract. Current `observation.v1` has `observed_at` and `retrieved_at`, which is sufficient for the bounded GKG path but is not sufficient for all future revised statistical sources.

### SR-02. Revision and vintage leakage

Severity: CRITICAL

Applicable invariants: I1, I4, I9, I10.

Failure: a current revised historical series is substituted for the value that was actually knowable at the historical decision time.

Required control:

* preserve provider vintage/version or immutable release snapshot
* treat later revisions as new records, not in-place replacement
* historical simulation resolves the latest admissible vintage as of its cutoff

Current status: required prospectively by `docs/GATE6A_SOURCE_ADMISSION.md`; no generic vintage store exists yet.

### SR-03. Retrospective model-estimate leakage

Severity: CRITICAL

Applicable invariants: I1, I7, I10.

Failure: a provider's current modelled historical estimate incorporates later observations or later model versions and is used as though it were available historically.

Required control:

* distinguish measured/reported values from modelled estimates
* preserve model/version and estimate vintage
* prohibit retrospective current estimates from point-in-time forecast inputs unless historical vintage is established

### SR-04. Future-dependent transformation leakage

Severity: CRITICAL

Applicable invariants: I1, I3, I10.

Failure: normalization, standardization, detrending, smoothing, imputation, feature selection, or threshold selection uses observations after the simulated cutoff.

Examples:

* z-score parameters estimated over the full future dataset
* centered moving averages
* PCA fitted on the full history including future periods
* min/max scaling using later extremes

Required control:

* every transformation declares its fit window and as-of cutoff
* historical transformations are fitted only on admissible past data
* fitted transformation state is versioned and reproducibly referenced

### SR-05. Missing-value look-ahead leakage

Severity: CRITICAL

Applicable invariants: I1, I8, I10.

Failure: a missing historical value is filled with a later release, interpolation using future observations, or a revised current series.

Required control:

* missing stays missing unless a historically available imputation method is preregistered
* causal/one-sided imputation only for historical simulations unless the experiment explicitly studies another method
* imputation state and inputs are replayable

### SR-06. Target or outcome leakage into features

Severity: CRITICAL

Applicable invariants: I1, I5, I10.

Failure: feature engineering, labels, semantic interpretation, source selection, or case construction directly or indirectly uses the outcome being predicted.

Required control:

* target definition is versioned before evaluation
* outcome/resolution artifacts are inaccessible to forecast feature construction
* feature lineage is auditable to the historical information set

### SR-07. Current-LLM historical knowledge contamination

Severity: CRITICAL

Applicable invariants: I1, I10, I12.

Failure: a modern LLM is prompted to make a forecast for an old date and the result is treated as a genuine historical forecast, even though model parameters may encode events that happened after that date.

Required control:

* a model can count as historically available only if the exact model snapshot existed at the simulated time and its information boundary is defensible
* current models used on historical dates must be labelled `retrospective_model_experiment`, not historical forecasts
* closed-book prompting can reduce explicit leakage but cannot prove that model parameters contain no future knowledge
* stronger prompting or reasoning cannot convert an unknown training-information boundary into valid historical evidence

Current status: future AI backtests are blocked. This risk must be explicitly handled before Gate 9 or Gate 10 historical AI claims.

### SR-08. Retrieval/search leakage in historical AI experiments

Severity: CRITICAL

Applicable invariants: I1, I10.

Failure: a historical simulation allows web search, retrieval, tools, memory, connected sources, or knowledge bases to expose post-cutoff material.

Required control:

* historical retrieval corpus has a hard point-in-time cutoff
* every retrieved item has admissible availability metadata
* live web search is prohibited in historical forecast simulation unless a historically frozen search corpus/index is used
* tool calls and retrieved evidence are logged into the forecast evidence snapshot

### SR-09. Forecast backfill or mutation

Severity: CRITICAL

Applicable invariants: I2, I9, I10.

Failure: a forecast is created after the fact, timestamped retrospectively, or substantively modified after issuance.

Required control:

* immutable forecast content hash
* append-only issuance record
* trusted issue timestamp
* corrections create new auditable records linked to the original
* no delete-and-reissue path that erases a failed forecast

### SR-10. Non-atomic forecast snapshot

Severity: CRITICAL

Applicable invariants: I1, I2, I4.

Failure: `issued_at`, evidence, features, model configuration, or probability are captured at different times so the exact information set at issuance cannot be reconstructed.

Required control:

* feature/evidence snapshot closes before or at issuance
* every input has `available_at <= snapshot_cutoff <= issued_at`
* forecast record binds immutable hashes of feature snapshot, evidence snapshot, target definition, resolution rule, model/method configuration, and code version

### SR-11. Hindsight-driven outcome resolution

Severity: CRITICAL

Applicable invariants: I3, I5, I10.

Failure: event criteria, ambiguity policy, resolution source, or deadline are reinterpreted after seeing the outcome to improve scoring.

Required control:

* versioned resolution rule before forecast issuance whenever practical
* resolver records source evidence and rule version
* ambiguous/unresolved outcomes remain explicit
* rule changes create a new experiment/version rather than rewriting old outcomes

### SR-12. Evaluation cohort selection bias

Severity: CRITICAL

Applicable invariants: I8, I10.

Failure: inconvenient forecasts, unresolved cases, low-confidence periods, failed model runs, or difficult event classes are removed after results are visible.

Required control:

* define cohort inclusion/exclusion before scoring
* maintain a complete forecast registry
* report counts of issued, resolved, unresolved, excluded, and failed forecasts
* exclusions require reason codes and versioned policy

### SR-13. Repeated tuning and multiple-comparison bias

Severity: HIGH

Applicable invariants: I3, I10.

Failure: indicators, thresholds, prompts, models, event classes, or scoring choices are repeatedly optimized on the same evaluation history and the best result is reported as confirmatory evidence.

Required control:

* separate development/tuning and held-out evaluation periods or cohorts
* record model-selection attempts when consequential
* treat post-hoc optimized results as exploratory
* require a new untouched evaluation cohort for confirmatory claims after material tuning

### SR-14. Baseline information asymmetry

Severity: HIGH

Applicable invariants: I10.

Failure: the AI/model receives richer or later information than the baseline, or the baseline is intentionally under-specified, making relative performance uninterpretable.

Required control:

* all methods share the same admissible information cutoff
* document features available to each baseline
* distinguish feature advantage from model advantage
* include simple competent baselines appropriate to the target

### SR-15. Calibration cohort incompatibility

Severity: HIGH

Applicable invariants: I3, I10.

Failure: probabilities from materially different targets, horizons, rule versions, or model regimes are pooled into one calibration statistic without justification.

Required control:

* calibration cohort keys include target/rule version, horizon class, method/model version where relevant
* pooled results disclose heterogeneity
* low sample size and dependence limit claims

### SR-16. Correlated-outcome pseudo-sample size

Severity: HIGH

Applicable invariants: I8, I10.

Failure: many strongly related forecasts are counted as independent observations, creating overconfident performance estimates.

Examples: multiple horizons for one event, repeated daily forecasts for the same unresolved event, geographically nested targets.

Required control:

* preserve dependency/group identifiers
* report cluster-aware or event-level summaries where appropriate
* do not infer statistical certainty from nominal forecast count alone

### SR-17. Source dependence and double counting

Severity: HIGH

Applicable invariants: I6, I7, I8.

Failure: multiple providers or indicators reuse the same upstream evidence and are treated as independent confirmation or separately weighted evidence.

Required control:

* upstream lineage graph
* conservative independence labels from `docs/GATE6A_SOURCE_ADMISSION.md`
* composite/state models must expose shared lineage and avoid silent duplicate weighting

### SR-18. Semantic drift and version mixing

Severity: HIGH

Applicable invariants: I3, I7, I9.

Failure: the same indicator ID, source code, category, event definition, or transformation is assumed to mean the same thing across time after provider or project semantics changed.

Required control:

* explicit semantic versions
* validity intervals and break markers
* historical values remain attached to the definition under which they were produced

### SR-19. Geography/entity-definition drift

Severity: HIGH

Applicable invariants: I3, I7, I9.

Failure: changing borders, country codes, sector definitions, population bases, company universes, or market constituents create false historical changes.

Required control:

* geography/entity scheme version
* mapping provenance
* break handling rather than silent remapping when semantics change

### SR-20. Market-time and timezone leakage

Severity: CRITICAL for market-linked forecasts, otherwise HIGH.

Applicable invariants: I1, I10.

Failure: a daily value is treated as known before its actual fixing/close/release time, or timestamps from different timezones are aligned incorrectly.

Required control:

* UTC canonical timestamps plus source timezone
* market/fixing/release calendar semantics
* holiday and daylight-saving handling
* explicit rule for daily bars and partial sessions

### SR-21. Informative missingness and outage bias

Severity: HIGH

Applicable invariants: I7, I8, I10.

Failure: source outages, censorship, publication delays, market closures, or disaster-related reporting failures are treated as random missing data even when missingness is related to the state being measured.

Required control:

* preserve source availability/failure observations separately
* avoid silent zero filling
* evaluate whether missingness itself changes around target events

### SR-22. Historical source survivorship

Severity: HIGH

Applicable invariants: I4, I8, I10.

Failure: backtests use only sources, entities, securities, countries, or feeds that survive into the present, excluding discontinued or failed members that existed historically.

Required control:

* point-in-time universe membership
* explicit delisting/discontinuation handling
* no present-day universe reconstruction for historical samples unless justified

### SR-23. Evaluation metric or threshold gaming

Severity: HIGH

Applicable invariants: I3, I10.

Failure: scoring metric, probability threshold, event window, or success criterion is selected after inspecting performance.

Required control:

* versioned scoring protocol
* primary metric selected before confirmatory evaluation
* post-hoc metrics remain exploratory

### SR-24. Decision-feedback contamination

Severity: MEDIUM initially, potentially HIGH after product use.

Applicable invariants: I6, I8, I10.

Failure: user or system actions influenced by Psychohistory alter later observations/outcomes, but evaluation treats forecasts as passive and independent.

Required control:

* decision-support outputs and user actions remain separate logged artifacts where evaluation requires them
* distinguish observational forecast evaluation from policy/intervention evaluation

## Current protection map

Current repository protections already strong:

* source hashes and external trust roots
* deterministic replay
* lossless quarantine
* immutable/frozen study membership
* indicator definition pinning
* adversarial chain-integrity tests
* separate human and machine evidence layers
* explicit unknown/unavailable states

For example, `scripts/test_indicator_integrity.py` rejects internally resealed but externally unauthenticated evidence chains, duplicate or missing source evidence, changed definitions, and manipulated missingness claims. These controls protect evidence integrity but do not by themselves prove point-in-time forecast validity.

## Highest-priority future blockers

Before Gate 7 forecast implementation:

1. SR-01 availability-time contract
2. SR-02 vintage contract
3. SR-09 forecast immutability
4. SR-10 atomic forecast snapshot
5. SR-11 preregistered resolution contract

Before Gate 9 historical evaluation:

1. SR-01 through SR-06 point-in-time data/feature controls
2. SR-11 through SR-16 evaluation controls
3. SR-20 timezone/market-time control where applicable
4. SR-22 point-in-time universe control where applicable

Before any historical AI performance claim:

1. SR-07 current-LLM knowledge contamination
2. SR-08 retrieval/search leakage
3. SR-13 repeated tuning
4. SR-14 baseline parity

## Stop rule

If a future task encounters a CRITICAL risk without an accepted control, stop advancement at that gate. Do not solve the problem by weakening timestamps, replacing unavailable vintages with current data, relabeling a retrospective LLM run as a historical forecast, or excluding inconvenient cases.

## Maintenance

Add a risk when a new failure mode can change scientific interpretation or evaluation. Close or downgrade a risk only when a versioned contract plus executable tests or equivalent evidence control exists.

Do not delete retired risks merely because implementation improves. Preserve their history and mark the control/version that addressed them.
