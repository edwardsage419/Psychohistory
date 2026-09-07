# Data Model Baseline

## Purpose

This document establishes conceptual entities that should remain stable even if the physical storage technology changes.

## Source

Represents a provider and dataset or endpoint.

Suggested fields:

* `source_id`
* `provider`
* `dataset_name`
* `access_method`
* `documentation_url`
* `license_note`
* `update_frequency`
* `coverage_note`
* `cost_tier`
* `production_status`
* `schema_version`

## Ingestion run

Represents one acquisition attempt.

Suggested fields:

* `run_id`
* `source_id`
* `started_at`
* `finished_at`
* `status`
* `records_seen`
* `records_written`
* `records_rejected`
* `error_class`
* `error_message`
* `source_snapshot_reference`
* `code_version`

## Observation

Represents a normalized measurable fact from a source.

Suggested fields:

* `observation_id`
* `source_id`
* `metric_id`
* `observed_at`
* `retrieved_at`
* `value`
* `unit`
* `geography`
* `entity`
* `quality_status`
* `source_record_reference`
* `schema_version`

The accepted `observation.v1` contract remains valid for current bounded GKG research. Its `observed_at` and `retrieved_at` fields must not be silently reinterpreted as a complete point-in-time availability/vintage model for future revised statistical sources.

When a source can be released after its reference period, revised after first publication, or queried historically through a current-state API, a versioned successor observation contract should distinguish the relevant point-in-time semantics. Depending on source type these may include:

* reference period start/end
* provider publication time
* earliest defensible availability time
* Psychohistory retrieval time
* revision/vintage identity
* revision publication time
* provider/source version
* immutable source snapshot or trusted reference

Do not overload old fields to avoid a schema version change.

## Indicator definition

Represents the meaning and transformation logic of a derived metric.

Suggested fields:

* `indicator_id`
* `version`
* `name`
* `description`
* `input_metrics`
* `formula_reference`
* `unit`
* `directionality`
* `normalization_method`
* `minimum_history`
* `missing_data_policy`
* `limitations`

For future point-in-time forecasting, fitted transformations also require a reproducible fit-information cutoff and fitted-state reference when their parameters depend on historical data.

## Indicator value

Represents a computed indicator at a point or period in time.

Suggested fields:

* `indicator_id`
* `indicator_version`
* `period`
* `geography`
* `value`
* `quality_status`
* `input_snapshot_reference`
* `computed_at`
* `code_version`

A historical forecast feature must remain bound to the exact admissible input/vintage snapshot used to compute it. A later recomputation from revised data is a different historical reconstruction unless identical inputs are proven.

## Event definition

Represents a resolvable real world event type used for concrete forecasts.

Suggested fields:

* `event_definition_id`
* `version`
* `name`
* `criteria`
* `geography_rule`
* `resolution_source`
* `resolution_method`
* `ambiguity_policy`

## Forecast

Represents an issued probabilistic statement.

Suggested fields:

* `forecast_id`
* `created_at`
* `forecast_type`
* `target_id`
* `question_text`
* `geography`
* `horizon_start`
* `horizon_end`
* `probability`
* `distribution_reference`
* `method_id`
* `model_version`
* `feature_snapshot_reference`
* `evidence_snapshot_reference`
* `resolution_rule_version`
* `status`

Before a production forecast schema is designed, also require explicit `information_cutoff` semantics and immutable bindings to the target definition, resolution rule, feature/evidence snapshots, model/method configuration, code version and substantive content hash as specified in `docs/FUTURE_EVALUATION_SAFEGUARDS.md`.

Substantive forecast fields become immutable after issuance.

## Forecast resolution

Represents the observed outcome of a forecast.

Suggested fields:

* `forecast_id`
* `resolved_at`
* `outcome`
* `resolution_source_reference`
* `resolution_rule_version`
* `resolver`
* `notes`

Resolution ambiguity must remain representable. A future schema must not require a binary outcome where the applicable rule supports `unresolved` or `ambiguous`.

## Evaluation record

Represents one scoring result.

Suggested fields:

* `forecast_id`
* `evaluation_method`
* `score`
* `baseline_score`
* `evaluated_at`
* `evaluation_code_version`

Future evaluation records should also preserve enough cohort and rule-version identity to reproduce which forecasts were eligible, resolved, excluded, unresolved or failed. Calibration and baseline claims must not depend on an unrecorded post-hoc cohort.

## Evidence record

Represents evidence used by a forecast or analysis.

Suggested fields:

* `evidence_id`
* `source_id`
* `captured_at`
* `source_reference`
* `content_hash`
* `summary`
* `quality_status`

For point-in-time use, evidence requires a defensible availability boundary in addition to capture time when the two differ.

## Decision support output

Represents a user facing synthesis for investment research or personal planning.

Suggested fields:

* `output_id`
* `created_at`
* `use_case`
* `question`
* `evidence_snapshot_reference`
* `forecast_snapshot_reference`
* `assumptions`
* `uncertainty_note`
* `model_version`

Decision support outputs should remain distinguishable from forecasts and from observations.

## Historical simulation class

Future evaluation should distinguish at least:

* genuine contemporaneous forecasts actually issued at the recorded time
* faithful historical replays using a defensible point-in-time information set and historically available method
* retrospective experiments applying a later method/model to historical inputs

These classes must not be merged silently. In particular, a current LLM applied to an old date is normally a retrospective experiment because its trained parameters may encode later information.

## Versioning rule

Any change that alters the semantic meaning of historical values requires a new schema, indicator, event definition, model, resolution, scoring or evaluation version as applicable. Historical records should not be silently reinterpreted under a changed definition.

## Point-in-time rule

Reference date is not equivalent to information availability.

Any future backtest or simulated forecast must prove that every input, transformation state, model/tool context and retrieved evidence was admissible under the simulated information cutoff. Current revised values, current search results, later corrections and later model knowledge cannot be substituted for missing historical states.
