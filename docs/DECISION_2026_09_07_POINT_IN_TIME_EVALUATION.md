# Owner Decision: Point-in-Time Evaluation Integrity

Date: 2026-09-07
Status: accepted methodological direction for future forecasting/evaluation work. This decision does not activate Gate 7, Gate 8, Gate 9, or Gate 10.

## Decision

Future Psychohistory forecast evaluation must preserve the information set that was actually knowable at the relevant time.

Reference period, publication availability, retrieval time and data revision/vintage are separate concepts. Future schemas and pipelines must represent them explicitly when the source requires them.

Current revised historical API values may not substitute for missing historical vintages in a point-in-time backtest.

## Historical AI decision

A current LLM run against an old date is normally a retrospective model experiment because the model parameters may encode facts learned after the simulated date.

Such output may be useful for research, but it cannot be labelled as a genuine historical forecast or as evidence of what that model would have predicted at the old date unless the exact historical model snapshot and its admissible information boundary are independently established.

Closed-book prompting does not by itself eliminate parameter-level future knowledge.

Live current web search, current connected sources and current retrieval indexes are prohibited in strict historical forecast simulation unless they are replaced by a defensible frozen point-in-time corpus/index.

## Forecast integrity decision

Future formal forecasts must be append-only and bind an immutable information/evidence snapshot, target definition, resolution rule, method/model configuration and substantive content hash.

Corrections must preserve the original forecast.

## Evaluation decision

Confirmatory evaluation must use a predefined cohort and scoring protocol. Forecasts, unresolved outcomes and failed runs cannot be silently removed after results are visible.

Repeated tuning on an evaluation cohort converts that cohort into development data for stronger confirmatory claims.

Baselines and compared methods must use compatible admissible information sets unless the experiment explicitly measures the value of additional information.

## Implementation consequence

Before future Gate 7-10 implementation, use:

* `docs/SCIENTIFIC_RISK_REGISTER.md`
* `docs/FUTURE_EVALUATION_SAFEGUARDS.md`
* `docs/GATE6A_SOURCE_ADMISSION.md` for source time/vintage requirements

The existing `observation.v1` schema remains unchanged for accepted GKG research. Revised statistical-source integration should design a versioned successor point-in-time observation contract when required instead of overloading existing fields.

## Current gate preservation

This decision changes no current Phase 5/6A evidence, no frozen sample membership, no E3 status, and no semantic conclusion.

The current accepted advancement task remains `docs/NEXT_ACCEPTED_TASK.md`.
