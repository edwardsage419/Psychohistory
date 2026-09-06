# Psychohistory Codex Operating Guide

## Mission

Psychohistory is a long term, production oriented system for observing social conditions, identifying emerging macro trends, assigning probabilities to future developments, preserving forecasts, and evaluating forecast quality against outcomes.

The product is intended to evolve from a personal research system into a formal product that may serve other users.

## Product scope confirmed by owner

The system should eventually support all of the following:

* Describe how the world is changing at the macro level.
* Detect important social trends before they become obvious.
* Estimate probabilities for major future events.
* Provide structured evidence that may inform investment research.
* Provide structured evidence that may inform long horizon personal decisions.
* Serve as a long running, falsifiable weak form psychohistory experiment.

The system should support both broad trend forecasts and concrete event forecasts.

## Cost constraint

During early development, prefer free or very low cost infrastructure and data. Paid APIs, models, databases, or hosting may be introduced after the system demonstrates clear value and reliability.

## Development horizon

This is a long term project. Do not optimize for rapid visual demos at the expense of data quality, reproducibility, validation, or forecast integrity.

## Current strategic decision

Treat the existing V0.2 application as a prototype and research artifact. Preserve useful experiments, especially the successful GDELT GKG validation work. Do not let the existing frontend, JSON schema, seven topic taxonomy, or DOC API implementation constrain the new architecture.

The GDELT DOC 2.0 API path is considered unsuitable as a production ingestion method in GitHub Actions because repeated real runs produced severe HTTP 429 failures. Do not spend further development effort on retry tuning unless new evidence changes this conclusion.

GDELT GKG remains a candidate source because the validation workflow has successfully downloaded and parsed current GKG files in GitHub Actions.

## Priority order

Use this order when tradeoffs arise:

1. Reliable source acquisition
2. Reproducible raw data preservation or reproducible source references
3. Clean normalized data
4. Transparent indicators
5. Historical backfill and continuity
6. Validation and quality checks
7. Forecast specification and immutable forecast records
8. Forecast evaluation and calibration
9. AI analysis
10. Dashboard and presentation

## Architecture principles

* Separate raw ingestion, normalization, indicators, forecasts, evaluation, and presentation.
* Every derived number must be traceable to source data and transformation code.
* Avoid a single monolithic JSON file as the long term database design.
* Avoid hard coding topic mappings until they are supported by source documentation and empirical frequency checks.
* Distinguish media attention from real world conditions. News volume is an observation channel, not the ground truth state of society.
* Prefer multiple independent data families over dependence on a single provider.
* Preserve timestamps, source versions, model versions, prompt versions, and transformation versions.
* Forecast records must become immutable once issued, except for explicit metadata corrections that preserve an audit trail.
* Evaluation rules must be defined before outcome scoring whenever practical.
* New infrastructure must justify its cost and operational burden.

## Working method for Codex

Before implementing a substantial change:

1. Read this file and the documents in `docs/`.
2. Inspect the current code and tests.
3. State the intended change, assumptions, risks, and acceptance criteria in the pull request or issue.
4. Prefer small, reviewable changes over broad rewrites without tests.
5. Add or update tests for transformation logic and failure behavior.
6. Never fabricate source mappings, field meanings, or validation results.
7. If a required fact is unknown, record it as an open question and stop that specific assumption from entering production logic.

## Current phase

The next phase is architecture reset and data foundation design. The immediate objective is to establish a durable data model and source evaluation process before expanding the dashboard or building production forecasting logic.
