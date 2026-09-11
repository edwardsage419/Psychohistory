# Forecast Architecture Activation Amendment

Date: 2026-09-11

Status: ACCEPTED DESIGN AMENDMENT

## Purpose

Activate the previously future only forecast, outcome, point in time, and evaluation architecture for a bounded implementation of Forecast Trust Core v0.1 after the strategic reactivation decision.

This amendment changes authorization and dependency interpretation. It does not weaken or replace the scientific requirements in:

1. `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md`
2. `docs/GATE7_9_SCHEMA_REQUIREMENTS.md`
3. `docs/FUTURE_EVALUATION_SAFEGUARDS.md`
4. `docs/DECISION_2026_09_07_POINT_IN_TIME_EVALUATION.md`
5. `SCIENTIFIC_INVARIANTS.md`

## Superseded boundary statements

Where the older forecast architecture documents state that schema implementation must wait globally for Gate 3A GKG evidence sufficiency, that global dependency is superseded.

The new rule is dependency scoped:

1. Forecast Trust Core contracts and validators may be implemented now.
2. A future forecast may be issued only when the dependencies of that specific forecast satisfy accepted target, evidence, method, resolution, and issuance requirements.
3. An unresolved measurement candidate blocks forecasts that depend on that measurement.
4. An unresolved measurement candidate does not block unrelated target or ledger infrastructure work.
5. A complete multi source state representation is not a universal prerequisite for forecast issuance.

## Current authorization

The only forecast related implementation currently authorized is `docs/NEXT_ACCEPTED_TASK.md`.

That task may implement:

1. target definition contract
2. resolution rule contract
3. point in time evidence snapshot contract
4. forecast method contract
5. run attempt contract
6. issued forecast contract
7. append only correction contract
8. deterministic canonicalization, hashing, cross object verification, and adversarial tests

It may not create a genuine prospective forecast.

## Requirements retained without relaxation

The following older requirements remain fully active:

1. target semantics must be versioned and fixed before issuance
2. resolution semantics must be bound before issuance
3. every point in time input must be admissible at the information cutoff
4. current revised data cannot silently replace unavailable historical vintage data
5. consequential upstream roots cannot be self authenticated circularly
6. run attempts remain distinct from issued forecasts
7. failed attempts remain visible where selection bias policy requires them
8. issued forecast substance is immutable
9. corrections append history
10. unresolved and ambiguous resolution states remain explicit
11. confirmatory evaluation uses frozen cohort manifests
12. complete registry denominator accounting is required
13. calibration does not retroactively alter issued probabilities
14. current models used on historical dates require truthful historical experiment classification
15. repeated forecasts may require dependency grouping
16. transparent baselines are first class forecast methods

## Genesis boundary

Forecast Ledger Genesis requires a separate accepted protocol after Forecast Trust Core v0.1 passes implementation and adversarial review.

Genesis must fix its target set, target versions, resolution rules, evidence cutoff policy, issuance cadence, method set, retry policy, correction policy, and initial evaluation plan before the first genuine forecast is issued.

No synthetic test fixture or retrospective experiment may be presented as part of prospective Genesis history.

## GKG boundary

This amendment changes no GKG scientific conclusion or artifact.

GKG remains a supporting measurement research candidate. Further GKG evidence recovery requires separate authorization and remains subject to its accepted Gate 3 safeguards.
