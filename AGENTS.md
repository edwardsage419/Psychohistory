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

1. Read this file and the documents in `docs/` that are relevant to the task.
2. Inspect the current code and tests.
3. Classify the task using the L0 to L5 policy below.
4. State the intended change, assumptions, risks, and acceptance criteria in the pull request or issue when appropriate.
5. Prefer small, reviewable changes over broad rewrites without tests.
6. Add or update tests for transformation logic and failure behavior.
7. Never fabricate source mappings, field meanings, or validation results.
8. If a required fact is unknown, record it as an open question and stop that specific assumption from entering production logic.
9. Restrict inspection and edits to files relevant to the task. Expand scope only when a concrete dependency requires it.
10. Stop once the requested behavior and acceptance criteria are satisfied. Do not continue with unrelated refactoring or optional cleanup unless explicitly requested.

## Task risk classification and model guidance

This classification exists to balance task reliability, scientific risk, and model cost.

Codex must classify substantial tasks before implementation. Codex cannot change the model that runs the current task. The operator selects the actual model before execution. If the selected model appears below the recommended minimum for the task, Codex should state that clearly before making a high risk change.

### L0: mechanical task

Characteristics:

* Formatting
* Renaming
* Comments
* Simple documentation
* Other deterministic edits with negligible reasoning risk

Recommended model and reasoning:

* GPT 5.6 Luna Low

### L1: local implementation

Characteristics:

* Scope is clear
* Behavior is already specified
* Usually limited to one file or one small component
* Failure has low scientific impact

Examples:

* Small bug fix
* Straightforward unit test
* CLI parameter
* Simple implementation from an approved specification

Recommended model and reasoning:

* GPT 5.6 Terra Medium

### L2: cross file or moderately complex implementation

Characteristics:

* Multiple files or modules are involved
* Dependencies must be traced
* Some debugging or implementation judgment is required
* Core scientific semantics are not being redefined

Examples:

* Pipeline implementation
* Cross module feature
* Nontrivial bug
* Migration implementation under an already approved design

Recommended model and reasoning:

* GPT 5.6 Terra High

### L3: architecture or semantic design

Characteristics:

* Requires a new design decision
* Changes schema, interfaces, data model, or system boundaries
* Existing behavior cannot simply be followed mechanically

Examples:

* Schema design
* Interface design
* Data model changes
* Indicator framework design
* Architecture decisions with long lived compatibility consequences

Recommended model and reasoning:

* GPT 5.6 Sol Medium

### L4: scientific validity or historical reproducibility risk

Characteristics:

A mistake can invalidate forecasts, historical reconstruction, backtests, calibration, scoring, or the evidence chain.

Examples:

* Forecast semantics
* Outcome resolution
* Calibration
* Scoring
* Backtesting
* Timestamp semantics
* Historical reconstruction
* Look ahead leakage
* Indicator definition changes that affect historical values
* Probability calculation
* Evidence or version provenance that affects reproducibility

Recommended model and reasoning:

* GPT 5.6 Sol High

Treat a change as L4 whenever it can alter historical outputs or evaluation results unless there is clear evidence that the change is purely mechanical.

### L5: system level unresolved problem

Characteristics:

* Fundamental architecture or methodology is uncertain
* An L4 problem remains unresolved after serious analysis
* Multiple core assumptions conflict
* The task requires repository wide methodological judgment

Examples:

* Fundamental forecasting architecture redesign
* Repository wide scientific integrity audit
* Persistent system level bug with unclear root cause
* Reassessment of core methodology

Recommended model and reasoning:

* GPT 6 Astra High

Use Astra XHigh only when High remains insufficient. Max reasoning is outside the normal workflow and should be exceptional.

## Escalation policy

Start with the lowest model that is expected to complete the task reliably.

Normal escalation path:

Terra Medium → Terra High → Sol Medium → Sol High → Astra High → Astra XHigh

Escalation is justified when one or more of the following occur:

* Root cause cannot be explained.
* Two implementation attempts fail.
* The proposed fix begins modifying unrelated files.
* Architecture or semantics must be guessed.
* Tests pass while semantic correctness remains uncertain.
* Test results conflict with the reasoning or specification.
* An existing specification appears to require change.
* Historical compatibility is unclear.
* Look ahead leakage may exist.
* Probability, calibration, scoring, resolution, or forecast semantics are affected.

Do not repeatedly retry the same uncertain problem with a weaker model when the uncertainty is architectural, methodological, or scientific.

## Downgrade policy

After an architecture or methodology decision is resolved, reassess the remaining work.

A stronger model may design or review a change while a lower cost model performs deterministic implementation.

Preferred pattern for high risk work:

1. Sol High or Astra High analyzes the design or methodological question.
2. Record the approved plan or specification.
3. Terra High implements the approved design when implementation is deterministic.
4. Sol High reviews scientific integrity when the change affects protected semantics.

Do not keep using an expensive model merely because an earlier stage of the task required it.

## Protected scientific domains

Substantive changes in the following areas require explicit semantic review:

* Forecast records and forecast semantics
* Outcome resolution
* Calibration
* Scoring
* Backtesting
* Historical reconstruction
* Timestamp semantics and information availability
* Probability calculations
* Indicator definitions
* Evidence provenance
* Model provenance
* Version provenance

Any change that can alter historical results should normally be treated as L4.

## Scientific integrity checks

For every L4 or L5 task, answer all applicable questions before declaring completion:

1. Was every input available at the historical prediction timestamp?
2. Does historical reconstruction use information that became available later?
3. Can a published forecast be modified in place?
4. Did an indicator, forecast, resolution, calibration, or scoring definition change?
5. If a definition changed, is a new explicit version recorded?
6. Is outcome resolution independent from the forecast that predicted the outcome?
7. Can knowledge of the final outcome influence interpretation of the original forecast?
8. Does a backtest use only data that would actually have been available at the simulated historical time?
9. Are missing historical values filled using information from the future?
10. Is calibration calculated over the correct forecast cohort?
11. Can the result be reproduced from stored data, code, and version metadata?
12. Are important transformations traceable to source evidence?

A passing test suite is insufficient when one of these scientific invariants is violated or remains unresolved.

## Context and token discipline

Do not scan the entire repository by default.

For each task:

1. Read `AGENTS.md` first.
2. Read only the relevant documents in `docs/`.
3. Inspect only the code and tests related to the requested change.
4. Expand scope only because of a concrete dependency discovered during the task.
5. Avoid repository wide analysis unless the task explicitly requires it.
6. Do not perform unrelated refactoring, renaming, cleanup, or speculative feature work.

The goal is reliable engineering and scientific output per unit of compute, rather than maximum model capability on every task.

## Stop conditions

Stop when all applicable conditions are satisfied:

1. The requested change is implemented.
2. Acceptance criteria are satisfied.
3. Relevant tests pass.
4. No unresolved semantic conflict remains.
5. No unrelated changes are required.
6. For L4 or L5 tasks, the scientific integrity checks have been completed.

Record unrelated findings separately instead of expanding the current task.

## Current phase

The next phase is architecture reset and data foundation design. The immediate objective is to establish a durable data model and source evaluation process before expanding the dashboard or building production forecasting logic.
