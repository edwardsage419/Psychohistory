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

## Evaluation record

Represents one scoring result.

Suggested fields:

* `forecast_id`
* `evaluation_method`
* `score`
* `baseline_score`
* `evaluated_at`
* `evaluation_code_version`

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

## Versioning rule

Any change that alters the semantic meaning of historical values requires a new schema, indicator, event definition, or model version. Historical records should not be silently reinterpreted under a changed definition.
