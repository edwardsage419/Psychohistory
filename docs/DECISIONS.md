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

## 2026 09 06: Phase 2 bounded GKG continuity study

The user's Phase 2 acquisition study takes precedence over the roadmap's original
Phase 2 indicator research heading. The 96-address manifest was fixed before
acquisition: 72 consecutive recent slots plus six four-slot historical windows.

Evidence: 96/96 HTTPS GETs and independent ZIP CRC checks passed, including all 24
historical samples; 92/96 strict UTF-8 parses passed. Four intact ZIPs contain five
invalid UTF-8 lines, all in field 27. All 96 stored archives reproduced their
original deterministic semantic outputs in an independent offline replay.

Decision: continue_validation, not promote_to_ingestion_candidate. No silent
codec fallback or field deletion is permitted to turn these failures into success.
Next: evidence-backed lossless encoding/row-quarantine policy against this corpus.

Provider terms permit dataset use and redistribution with attribution/link; this
is distinct from linked publisher article rights. English master-list feed only
was sampled; translated feeds, unsampled historical continuity and retention
promises remain unknown. Measured raw ZIP volume is 494,483,985 bytes; recent mean
extrapolates to about 164 GB/year for that feed alone. Raw data remains local,
content-addressed and outside Git; compact evidence is committed. Long-term
backup/storage is not selected. See PHASE_2_REPORT.md and GKG_STUDY_SCHEMA.md.

## 2026 09 06: project-wide infrastructure cost constraint

Default to zero or near-zero recurring infrastructure cost. Paid infrastructure should be introduced only when a free approach materially harms data integrity, reproducibility, reliability, analytical quality, or product capability, and the benefit is supported by evidence.

This constraint does not weaken provenance, validation, quarantine, or the
preregistered Phase 3 promotion gates. Keep all 96 research archives intact.
Do not implement deletion or reduce acquisition/fields/coverage for cost.
Retain exact quarantined bytes and compact acquisition/provenance evidence
permanently; future ordinary raw retention requires a separately reviewed,
configurable policy. Hashes verify a recovered revision but cannot recreate it.
No paid service or new recurring dependency is introduced.

## 2026 09 06: Phase 3 limited ingestion candidate recommendation

The preregistered gates pass for 96 verified archives: 118,415 accepted rows, five
exact-byte quarantines, 92 clean batches and four with quarantine. Two independent
final replays agree on all hashes/semantics; 111 offline tests pass on Ubuntu CI.
Recommend promote_to_ingestion_candidate for raw acquisition, archive verification,
lossless parsing, quarantine and provenance only. This validates no theme semantics
or indicators and does not activate production ingestion. See PHASE_3_REPORT.md.
Near-zero-cost retention separates permanent quarantine/receipts from future
configurable ordinary raw retention. No research archive is deleted.
