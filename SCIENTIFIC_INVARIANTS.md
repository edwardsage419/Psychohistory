# Psychohistory Scientific Invariants

These rules protect the falsifiability, reproducibility, and historical validity of Psychohistory. They apply across models, devices, sessions, branches, and implementation phases.

If implementation convenience conflicts with an invariant, the invariant wins unless the owner explicitly approves a versioned methodological change with documented consequences.

## I1. No future information

Historical reconstruction, backtesting, and simulated forecasts may use only information that would have been available at the simulated decision or prediction timestamp.

Do not use later corrections, later publications, future-filled missing values, hindsight labels, or outcome knowledge unless the experiment explicitly models their historical availability.

## I2. Forecast immutability

Once a forecast is issued, its substantive prediction content must not be silently changed.

Corrections must preserve the original record and create an auditable correction/version trail.

## I3. Versioned semantics

Any definition that can change historical interpretation or numerical output must be explicitly versioned.

This includes indicator definitions, normalization rules, forecast semantics, target definitions, resolution rules, scoring rules, calibration methods, and important model/prompt logic.

## I4. Historical reproducibility

A claimed historical result must be reproducible from retained or reproducibly referenced source evidence, transformation code, configuration, and relevant versions.

A current output that cannot be traced to its historical inputs and transformations is not an authoritative historical result.

## I5. Independent outcome resolution

Outcome resolution must be defined and performed independently enough that the original forecast cannot be reinterpreted after the outcome is known merely to improve scoring.

Ambiguity must remain explicit when the preregistered or versioned rules do not support a defensible resolution.

## I6. Evidence traceability

Important observations, indicators, forecasts, resolutions, and evaluation outputs must retain a defensible evidence chain.

Every derived number should be traceable to source data or source references and transformation logic at an appropriate level of detail.

## I7. Observation is not reality

Media volume, search volume, textual mentions, model classifications, and similar signals are observations or attention proxies unless independently validated as measures of the underlying real-world state.

Do not silently convert an observation channel into a claim about severity, prevalence, causality, or ground truth.

## I8. Explicit uncertainty

Unknown, unavailable, ambiguous, conflicting, and insufficient-evidence states must remain explicit.

Do not force a binary label, semantic judgment, identity match, forecast resolution, or scientific conclusion merely to complete a pipeline.

## I9. No silent historical rewrite

New data, bug fixes, definition changes, or improved extraction must not silently overwrite prior authoritative historical outputs.

When historical values legitimately change, preserve provenance and identify the reason, affected version, and compatibility implications.

## I10. Evaluation integrity

Scoring, calibration, and backtesting must evaluate the forecast system that actually existed under the information and rules available at the relevant time.

Do not select favorable cohorts, reviewers, denominators, thresholds, definitions, or outcome interpretations after seeing results without explicitly treating that change as a new version or experiment.

## I11. Genuine human evidence remains human

When a protocol requires genuine independent human review, machine preprocessing, LLM judgment, synthetic personas, or relabeled model output cannot satisfy that requirement.

Human identity, independence, and attestation must be established by the responsible operator under the applicable protocol.

## I12. Missing evidence cannot be reasoned into existence

A stronger model cannot convert absent historical evidence, unknown source versions, unavailable documents, or unresolved identity into valid evidence.

Record the gap, attempt bounded recovery when justified, obtain required human review, or stop advancement at the applicable gate.

## Completion rule

For every L4 or L5 task, explicitly check the applicable invariants before declaring the task scientifically complete.

Passing software tests is necessary but not sufficient when an invariant is violated or unresolved.
