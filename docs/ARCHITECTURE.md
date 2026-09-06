# Target Architecture

## Status

This document defines the intended architecture direction. It is a design baseline, not a claim that every component already exists.

## System shape

Psychohistory should evolve into a layered pipeline:

Source acquisition
↓
Raw or source referenced records
↓
Normalization
↓
Quality checks
↓
Base indicators
↓
Composite state and trend indicators
↓
Forecast features
↓
Forecast generation
↓
Immutable forecast registry
↓
Outcome resolution
↓
Evaluation and calibration
↓
API or export layer
↓
Dashboard and decision support

## Layer 1: source registry

Maintain a registry of every data source with at least:

* Provider
* Dataset or endpoint
* License and usage constraints
* Access method
* Update frequency
* Geographic coverage
* Historical coverage
* Reliability history
* Known biases
* Cost
* Source documentation reference
* Current production status

No source should enter production simply because it is easy to query.

## Layer 2: acquisition

Each source should have an independent ingestion adapter.

Acquisition code should:

* Preserve retrieval timestamps.
* Record source identifiers and versions where available.
* Detect partial and complete failures.
* Avoid silently replacing missing values with plausible values.
* Be idempotent for repeated runs.
* Support backfill when the provider permits it.
* Produce machine readable run metadata.

GitHub Actions may remain useful during the low cost stage. The architecture must permit migration to scheduled cloud jobs later.

## Layer 3: raw and normalized storage

The current single `data/gdelt.json` pattern should be considered transitional.

The initial replacement may still use repository files if data volume remains small, but schemas must be separated by purpose. A later move to SQLite, DuckDB, Postgres, object storage, or a similar system should remain possible without changing indicator semantics.

A normalized observation should generally include:

* Observation time
* Retrieval time
* Source
* Metric identifier
* Value
* Unit
* Geographic scope
* Entity scope if applicable
* Source record reference
* Quality status
* Schema version

## Layer 4: quality system

Quality checks should cover where relevant:

* Schema validity
* Missingness
* Duplicate records
* Staleness
* Abrupt unexplained distribution shifts
* Coverage changes
* Source outages
* Unexpected unit or scale changes

Quality failures should be visible downstream.

## Layer 5: indicator registry

Every indicator requires documentation of:

* Identifier and human name
* Purpose
* Source inputs
* Formula
* Unit or normalized range
* Directionality
* Update frequency
* Geography
* Minimum history requirement
* Missing data behavior
* Known limitations
* Version

Indicator changes that alter historical meaning require a new version.

## Layer 6: composite indices

Composite indices should combine multiple base indicators only when the combination has a defensible rationale.

Weights, normalization, smoothing, lag structure, and missing data rules must be explicit. Composite indices must be decomposable into their inputs.

The current seven topic taxonomy is not an architectural requirement. It should be replaced or retained only after empirical evaluation.

## Layer 7: forecasting

Forecast objects should contain at least:

* Forecast ID
* Creation timestamp
* Forecast type
* Question or target
* Event definition or trend definition
* Geography
* Horizon
* Probability or predictive distribution
* Method identifier
* Model version
* Feature snapshot reference
* Evidence snapshot reference
* Resolution source
* Resolution rule
* Resolution deadline
* Status

Once issued, substantive forecast fields should be immutable.

## Layer 8: resolution and evaluation

Outcome resolution should be independent from forecast generation when possible.

Evaluation metrics may include Brier score, log score, calibration curves, discrimination measures, interval coverage, directional accuracy, baseline comparison, and stability through time. Metric choice depends on forecast type.

## Layer 9: AI analysis

AI should consume structured observations, indicators, forecasts, and source evidence. It should not become the sole source of historical facts or numerical indicators.

AI responsibilities may include:

* Evidence synthesis
* Scenario generation
* Contradiction detection
* Forecast rationale drafting
* Feature hypothesis generation
* Natural language interface

Model prompts and versions used in production analysis should be recorded.

## Layer 10: presentation

The dashboard should read prepared outputs. Browser code should not perform critical source acquisition or hidden analytical transformations.

The interface should eventually distinguish:

* Current observations
* Trends
* Composite state estimates
* Forecasts
* Evidence
* Historical forecast performance
* Data quality and freshness

## Infrastructure cost principle

Default to zero or near-zero recurring infrastructure cost. Paid infrastructure should be introduced only when a free approach materially harms data integrity, reproducibility, reliability, analytical quality, or product capability, and the benefit is supported by evidence.

Local files, Git/GitHub for compact evidence, and lightweight local SQLite,
DuckDB or Parquet storage are compatibility targets, not selections. Free
execution capacity must be measured rather than assumed unlimited. The
[retention design](GKG_RETENTION_POLICY.md) separates permanent evidence from
raw retention; no Phase 3 deletion or reduced sampling is authorized.

## Initial technology posture

For the next stage, prefer simple technology that Codex can maintain reliably:

* Python for ingestion, normalization, indicators, tests, and evaluation.
* GitHub Actions for scheduled jobs while volume and runtime remain reasonable.
* Versioned files or a lightweight analytical database during early validation.
* Static frontend or a thin application layer until product requirements justify a backend service.

Do not introduce distributed infrastructure, queues, microservices, or paid databases before they solve a demonstrated limitation.
