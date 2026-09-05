# Decision Log

## 2026 09 06: Product ambition

Decision: Psychohistory is intended to become a formal product rather than remain only a personal prototype.

Implication: architecture should preserve a path toward multiple users and more robust infrastructure without paying that complexity cost during the early proof stage.

## 2026 09 06: Forecast scope

Decision: support both macro trend forecasts and concrete event forecasts.

Implication: the system needs separate forecast schemas and evaluation methods where necessary.

## 2026 09 06: Decision support scope

Decision: the long term system should support world state awareness, early trend detection, event probabilities, investment research, personal long horizon planning, and a falsifiable psychohistory experiment.

Implication: these use cases share one evidence and forecast core. Investment and personal planning should be downstream decision support views rather than separate data pipelines.

## 2026 09 06: Cost policy

Decision: prefer free or low cost infrastructure during early validation. Paid services are acceptable after demonstrated value.

Implication: GitHub Actions, public datasets, lightweight storage, and simple deployment remain preferred until they create measurable limitations.

## 2026 09 06: Development horizon

Decision: prioritize durable foundations over rapid feature delivery.

Implication: months of data and validation work are acceptable before the interface becomes substantially more sophisticated.

## 2026 09 06: Existing V0.2 status

Decision: retain the repository and useful experiments, while treating the current application architecture as a prototype rather than a constraint.

Implication: existing frontend code may be retained temporarily. Existing data contracts and topic taxonomy may be replaced.

## 2026 09 06: GDELT DOC 2.0 API

Decision: stop treating GDELT DOC 2.0 API as the production ingestion route in GitHub Actions.

Evidence: repeated real workflow runs produced widespread HTTP 429 failures despite reduced request volume and backoff logic. Current production data contains extensive failed topic states.

Implication: further retry tuning is not a near term engineering priority.

## 2026 09 06: GDELT GKG

Decision: keep GDELT GKG as a production candidate, subject to further semantic and frequency validation.

Evidence: the repository contains a validation script, offline tests, and a scheduled validation workflow. Recent GitHub Actions validation completed successfully and produced an artifact.

Implication: Codex may extend GKG validation, but must not invent theme mappings or treat successful file parsing as proof that any proposed social indicator is valid.

## 2026 09 06: Seven topic taxonomy

Decision: Economic, Geopolitics, Technology, Energy, War and Conflict, Inflation, and AI are prototype dashboard categories only.

Implication: future indicator design should start from measurable constructs and available evidence. It may produce more, fewer, or differently organized indicators.

## 2026 09 06: Data priority

Decision: development priority is data, indicators, validation, forecasts, evaluation, AI, then interface.

Implication: dashboard expansion should not lead the roadmap.

## 2026 09 06: Forecast integrity

Decision: forecasts must be timestamped, versioned, resolvable, and substantively immutable after issuance.

Implication: the data model must preserve evidence snapshots, model versions, horizon, probability, and resolution rules.

## 2026 09 06: Multi source strategy

Decision: the mature system should use multiple independent data families.

Implication: GDELT must not become the ontology for the whole project. Source adapters and indicators should be designed so other providers can be added independently.

## Open decisions

The following remain unresolved and require evidence before implementation:

* Final physical storage technology.
* First production set of indicators.
* Exact GKG theme mappings, if GKG themes are used.
* Additional production data providers.
* Geographic resolution strategy.
* Forecast cadence and initial event classes.
* AI provider and model strategy.
* Criteria that justify moving from free infrastructure to paid services.
* Multi user product architecture and authentication timing.

## 2026 09 06: Issue 2 foundation implementation

Decision: retain GKG as `continue_validation`; do not promote it to production.
The strict local integration run parsed 479 complete 27-field records, rejected
none, and observed 76 empty theme rows and 1,459 literal theme codes. Full source
reference, checksums and frequency evidence are in GKG_EVALUATION.md and its
retained report. One batch cannot establish continuity or indicator validity.

Decision: require explicit network integration opt-in, strict UTF-8, bounded ZIP
processing, complete/partial statistics and machine-readable failure reports.
Adopt v1.0.0 contracts for reports, a source registry and numeric observations.
Use standard-library contract validation and tests; no runtime dependency added.
Observation content identity excludes retrieval timestamps, preserving replay
identity while allowing distinct content revisions. Persistence remains future work.

Migration impact: validation report consumers must adopt the new versioned shape;
old --date/--top-themes CLI flags are removed. Prototype frontend, DOC updater,
production workflow and data/gdelt.json are unchanged. Bytecode and the inactive
root workflow copy are retired on the development branch only. No theme mapping,
final ontology, indicator, forecast or storage-engine decision was made.
