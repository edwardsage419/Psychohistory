# Roadmap

## Phase 0: architecture reset

Goal: establish durable project rules before new production features.

Acceptance criteria:

* Codex operating guide exists.
* Product vision is explicit.
* Target architecture is documented.
* Conceptual data model is documented.
* Existing V0.2 components are classified as keep, replace, or retire.
* Open questions are recorded.

## Phase 1: data source foundation

Goal: build a reliable, testable source ingestion foundation.

Work:

* Create a source registry.
* Complete GDELT GKG technical validation and document observed field frequencies.
* Research additional candidate source families.
* Define ingestion run metadata and quality reporting.
* Establish normalized observation schema.
* Choose early storage format based on actual data volume.
* Add backfill strategy where feasible.

Acceptance criteria:

* At least one production candidate source can run automatically with reliable failure reporting.
* Repeated runs are idempotent.
* Source provenance is preserved.
* Schema tests and failure tests exist.
* Data can be backfilled or the absence of backfill is explicitly documented.

## Phase 2: indicator research and registry

Goal: replace the current seven topic prototype with defensible base indicators.

Work:

* Propose candidate indicators across economic, financial, conflict, political, energy, technology, public health, disaster, demographic, and sentiment domains where reliable data exists.
* Evaluate overlap, coverage, lag, revision behavior, and source bias.
* Define normalization and missing data rules.
* Create indicator registry and versioning.

Acceptance criteria:

* Every production indicator has documented semantics and tests.
* Media attention indicators are clearly labeled as attention measures.
* Indicator history can be reproduced from source data and code.

## Phase 3: composite state and trend system

Goal: derive interpretable higher level conditions from multiple indicators.

Work:

* Define candidate composite dimensions.
* Test weighting and normalization approaches.
* Compare simple transparent baselines before complex models.
* Add decomposition views showing component contributions.

Acceptance criteria:

* Composite values are reproducible and decomposable.
* Historical behavior is inspected for obvious artifacts.
* Version changes preserve prior histories.

## Phase 4: forecast registry and baseline forecasting

Goal: make falsifiable forecasting a first class system component.

Work:

* Define macro trend forecast schema.
* Define concrete event forecast schema.
* Build immutable forecast storage.
* Define resolution sources and rules.
* Establish simple baselines before AI or machine learning methods.

Acceptance criteria:

* Forecasts have unique IDs, timestamps, horizons, probabilities, evidence references, and resolution rules.
* Issued forecasts cannot be silently edited.
* At least one automated or reproducible baseline forecast method exists.

## Phase 5: evaluation and calibration

Goal: measure whether forecasting adds value.

Work:

* Implement scoring appropriate to each forecast class.
* Compare forecasts against naive baselines.
* Build calibration and error reports.
* Track performance by method, horizon, geography, and event class where sample size permits.

Acceptance criteria:

* Forecast performance can be reproduced from stored records.
* Model comparison uses predefined metrics.
* Weak performance remains visible rather than being hidden by selective examples.

## Phase 6: AI analysis

Goal: use language models where structured reasoning and synthesis add value.

Work:

* Add evidence synthesis from structured data.
* Add scenario generation and contradiction checks.
* Experiment with AI assisted forecast generation against baselines.
* Record model and prompt versions.

Acceptance criteria:

* AI outputs are traceable to evidence snapshots.
* AI forecast performance is scored against baselines.
* Hallucinated or unsupported facts are detectable through source references and validation.

## Phase 7: product interface

Goal: turn the validated system into a useful formal product.

Work:

* Redesign dashboard around state, trends, forecasts, evidence, quality, and track record.
* Add user oriented explanations of uncertainty.
* Add investment research and personal planning views as evidence synthesis surfaces.
* Evaluate whether accounts, backend services, and paid infrastructure are justified.

Acceptance criteria:

* The interface exposes data freshness and quality.
* Forecast history and accuracy are prominent.
* User facing conclusions can be traced to underlying evidence.

## Near term Codex tasks

Codex should begin with Phase 0 and Phase 1 only.

Immediate engineering sequence:

1. Audit existing repository files and workflows.
2. Remove accidental generated Python bytecode from source control and add appropriate ignore rules.
3. Produce a keep, replace, retire inventory for V0.2.
4. Formalize the GKG validation output into a stable machine readable report schema.
5. Add tests around GKG validation edge cases.
6. Design the source registry and normalized observation schema in code.
7. Research and propose the first production ingestion path before modifying the current dashboard data contract.

Do not begin production forecast logic until the data foundation has passed its acceptance criteria.

## Execution note: 2026-09-06

The owner requested a Phase 2 GKG continuity/reproducibility/historical study
before indicator research. That bounded acquisition phase is recorded in
PHASE_2_REPORT.md and does not authorize the indicator Phase 2 described above.
Its next recommended issue is lossless encoding and row-quarantine policy;
production ingestion, ontology and forecast work remain deferred.

## Execution note: Phase 4 measurement foundation

The owner's phase numbering supersedes the original planning sequence above.
Phase 3 ingestion is accepted at 09586cd. Phase 4 indicator foundation and GKG
semantic validation is recorded in PHASE_4_REPORT.md. Current recommendation:
continue_semantic_validation. The next recommended issue is a preregistered,
bounded semantic audit across historical cohorts and provider-version evidence;
not the original roadmap's forecasting phase. Experimental media prevalence must
not become a social-severity/risk series without additional validation. Production,
forecasting, final ontology and geographic attribution remain deferred.
