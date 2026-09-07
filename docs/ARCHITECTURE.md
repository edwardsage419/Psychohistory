# Target Architecture

## Status

This document defines the intended architecture direction. It is not a claim that every component already exists or is authorized to be implemented.

The current implementation is mature through source validation, reproducible observations, experimental indicator infrastructure, provenance, semantic-audit tooling and historical evidence recovery. Composite-state, forecast, outcome-resolution, calibration and decision-support components remain future architecture until their scientific gates are satisfied.

Future Gate 7-9 design is specified in `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md`, `docs/GATE7_9_SCHEMA_REQUIREMENTS.md` and `docs/FUTURE_EVALUATION_SAFEGUARDS.md`. These are design constraints, not implementation authorization.

The retired V0.2 frontend, seven-topic taxonomy, GDELT DOC updater and `data/gdelt.json` pattern are preserved only in Git history. They are not active architecture.

## System shape

Psychohistory should evolve into a layered pipeline:

Source acquisition
↓
Raw or source-referenced evidence
↓
Normalization
↓
Quality checks
↓
Base indicators
↓
Interpretable multi-source state/trend representation
↓
Forecast features and evidence snapshots
↓
Forecast generation
↓
Immutable forecast registry
↓
Independent outcome resolution
↓
Evaluation and calibration
↓
API/export layer
↓
Presentation and decision support

Each transition is gate-controlled. The existence of a downstream schema or implementation idea does not authorize advancement when an upstream evidence gate remains open.

## Layer 1: source registry

Maintain a registry of every data source with at least:

* provider
* dataset or endpoint
* license and usage constraints
* access method
* update frequency
* geographic coverage
* historical coverage
* reliability history
* known biases
* cost
* source documentation reference
* current production status

No source should enter production simply because it is easy to query.

## Layer 2: acquisition and evidence

Each source should have an independent ingestion or evidence-acquisition adapter.

Acquisition code should:

* preserve retrieval timestamps
* record source identifiers and versions where available
* detect partial and complete failures
* preserve objective identity and provenance
* avoid silently replacing missing values or unavailable evidence
* be idempotent where repeated acquisition semantics permit it
* support backfill where the provider permits it
* produce machine-readable run metadata

For historical evidence recovery, failed attempts, mismatches and unresolved identity are first-class results. Replacement sampling or silent substitution is prohibited when a protocol freezes sample membership.

GitHub Actions may remain useful during the low-cost stage. Scheduled jobs must not mutate the authoritative scientific baseline merely to refresh transient monitoring data.

## Layer 3: raw and normalized storage

The former single-file V0.2 dashboard data pattern has been retired.

Early research may continue to use versioned repository files for compact evidence and local ignored storage for larger raw artifacts. A later move to SQLite, DuckDB, Parquet, Postgres, object storage or a similar system should remain possible without changing scientific semantics.

A normalized observation should generally include:

* observation time
* retrieval time
* source
* metric identifier
* value
* unit
* geographic scope
* entity scope if applicable
* source record reference
* quality status
* schema version

Storage technology must not become a hidden semantic dependency.

## Layer 4: quality and provenance

Quality checks should cover where relevant:

* schema validity
* missingness
* duplicate records
* staleness
* unexpected distribution shifts
* coverage changes
* source outages
* unexpected unit or scale changes
* source identity conflicts
* historical version uncertainty
* replayability and trust-root integrity

Quality failures should remain visible downstream rather than being silently repaired into plausible data.

## Layer 5: indicator registry

Every indicator requires documentation of:

* identifier and human name
* purpose and semantic interpretation
* source inputs
* formula/transformation
* unit or normalized range
* directionality where applicable
* update frequency
* geography/entity scope
* minimum history requirement
* missing-data behavior
* smoothing and lag rules
* known biases and limitations
* quality requirements
* provenance requirements
* version and promotion status

Indicator changes that alter historical meaning require a new version. A technically reproducible token count does not automatically become a validated social indicator.

## Layer 6: multi-source state and trend representation

Composite or latent state construction should begin only when multiple sufficiently independent validated indicators exist.

Weights, normalization, smoothing, lag structure and missing-data rules must be explicit. Composite values must be decomposable into contributing indicators and should preserve uncertainty.

Prefer independent evidence families over increasingly elaborate transformations of one news source. Do not publish an opaque single world-risk score.

## Layer 7: forecasting

Future forecasting follows `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md`.

Before an issued forecast can exist, the architecture must already have versioned target semantics, a compatible resolution rule, an admissible point-in-time information snapshot and a versioned forecast method.

Forecast objects should eventually contain at least:

* forecast ID
* issuance timestamp
* information cutoff
* forecast class
* target and target-definition version/hash
* geography or entity scope where applicable
* horizon
* probability or predictive distribution
* method identifier/version/hash
* model and prompt/configuration identity where applicable
* feature snapshot reference
* evidence snapshot reference
* resolution rule reference/version/hash
* run-attempt reference
* status
* immutable substantive content identity

Run attempts and issued forecasts are separate concepts. Failed pre-issue attempts remain auditable when scientifically consequential.

Once issued, substantive forecast fields are immutable. Corrections append records and preserve the original. Forecast architecture remains future work until the applicable measurement gates are satisfied.

## Layer 8: resolution and evaluation

Outcome resolution should be independent from forecast generation when possible and must remain bound to the target and resolution-rule versions fixed at issuance.

Resolution must preserve source references, target-data vintage, rule versions, ambiguity/unresolved states and resolver provenance. Missing or conflicting evidence cannot be converted into a convenient negative outcome merely to increase scoreable sample size.

Confirmatory evaluation operates on a frozen evaluation-cohort manifest. The cohort accounts for every issued forecast within scope as eligible, unresolved, excluded under a predefined rule, or otherwise reproducibly outside scope. Forecasts do not disappear because they perform poorly or are difficult to resolve.

Evaluation metrics may include Brier score, log score, calibration curves, discrimination measures, interval coverage, directional accuracy, baseline comparison and stability through time. Metric choice depends on forecast class and must be fixed before confirmatory result inspection.

Historical evaluation must use only data, vintages, transformation states, models/tools and rules admissible at the relevant historical information cutoff. Current-model historical experiments are separately classified from genuine contemporaneous forecasts.

Detailed future schema constraints are defined in `docs/GATE7_9_SCHEMA_REQUIREMENTS.md` and point-in-time/adversarial requirements in `docs/FUTURE_EVALUATION_SAFEGUARDS.md`.

## Layer 9: AI analysis

AI should consume structured observations, indicators, forecasts and source evidence. It should not become the sole source of historical facts or numerical indicators.

AI responsibilities may include:

* evidence synthesis
* scenario generation
* contradiction detection
* forecast-rationale drafting
* feature-hypothesis generation
* natural-language interface

Model and prompt versions used in consequential analysis should be recorded. AI forecast value must eventually be measured against transparent baselines.

For formal AI forecasts, preserve model/configuration, prompt/template, tool/retrieval policy, structured input/evidence snapshots, run-attempt provenance and any human override. Private chain-of-thought is not a required scientific artifact.

## Layer 10: presentation and decision support

The interface should read prepared outputs. Browser code should not perform critical source acquisition or hidden analytical transformations.

A future product should distinguish:

* current observations
* validated and experimental indicators
* trends and decomposable state estimates
* forecasts
* evidence
* historical forecast performance
* data quality and freshness
* uncertainty

Investment research and personal-planning outputs should remain downstream decision-support artifacts, distinguishable from observations and forecasts.

The next interface will be designed from validated research outputs. The retired V0.2 frontend imposes no compatibility requirement.

## Infrastructure cost principle

Default to zero or near-zero recurring infrastructure cost. Paid infrastructure should be introduced only when a free approach materially harms data integrity, reproducibility, reliability, analytical quality or product capability and the benefit is supported by evidence.

Local files, Git/GitHub for compact evidence, and lightweight local SQLite, DuckDB or Parquet storage remain compatibility targets rather than predetermined selections.

Do not weaken provenance, evidence retention, scientific thresholds or historical reproducibility to reduce infrastructure cost.

## Initial technology posture

For the current stage, prefer technology that GPT and Codex can maintain and audit reliably:

* Python for acquisition, normalization, indicators, replay, tests and evaluation
* GitHub Actions for bounded CI and low-frequency read-only integration checks
* versioned files for compact evidence and local analytical storage for larger artifacts
* no active frontend until product requirements are justified by validated outputs

Do not introduce distributed infrastructure, queues, microservices, paid databases or production forecasting machinery before they solve a demonstrated and currently authorized limitation.