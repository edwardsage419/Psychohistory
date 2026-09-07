# Gate 6A Source Admission Standard

Date: 2026-09-07
Status: future governance specification. Gate 6A is not currently active and this document does not admit any new source.

## Purpose

Define the minimum evidence required before a new external source family can become an accepted Psychohistory research input.

The standard is designed to prevent a future expansion phase from repeating early-project mistakes such as choosing a source because it is easy to query, treating an API response as ground truth, overlooking historical revisions, confusing provider diversity with evidence independence, or allowing product convenience to weaken scientific provenance.

## Admission principle

A source is admitted because its acquisition, semantics, historical behavior, lineage and legal use are sufficiently understood for a bounded purpose.

Admission does not validate an indicator and does not authorize production use.

Every candidate may end as:

* admitted for bounded research
* admitted with restrictions
* deferred pending evidence
* rejected

Rejection is a valid outcome.

## Required admission stages

### A0. Research candidate definition

Before coding an adapter, record:

* provider and dataset
* intended source family
* intended construct or factual observation
* reason it adds information beyond existing sources
* expected update cadence
* expected geographic/entity scope
* known access requirements
* known license/product constraints

Do not start with an indicator formula. Start with the source and the measurable fact it actually exposes.

### A1. Access and legal compatibility

Required evidence:

* official access documentation
* current API/download mechanism
* authentication requirements
* rate limits where known
* provider terms/license
* redistribution conditions
* commercial-use conditions
* attribution requirements
* third-party data exceptions

Fail or restrict admission when the intended use violates provider terms or when important rights remain unknown.

A source can be scientifically valuable but unsuitable for a future commercial product. Record this explicitly rather than ignoring the conflict.

Credentials must never be committed to Git. If a provider requires keys or tokens, the future implementation must use repository/environment secrets or local configuration with tests that do not require the secret.

### A2. Acquisition and provenance integrity

A bounded empirical acquisition study must demonstrate:

* deterministic request construction or recorded source references
* successful retrieval from representative current and historical cases where applicable
* exact response hashing
* response size and format validation
* safe bounded parsing
* explicit partial/failure states
* retrieval timestamps with timezone
* source/provider version when available
* metadata needed to reproduce the query
* no silent imputation or fallback provider

Where raw source bytes are not retained permanently, document exactly what evidence is preserved and what cannot later be reconstructed.

### A3. Time semantics and publication availability

For every proposed observation type, distinguish at minimum:

* reference/observation period
* provider publication or release time
* Psychohistory retrieval time
* revision/update time where available

The system must know when a value became knowable, not only the period it describes.

A GDP value labelled 2025 but published in 2026 is unavailable to a forecast issued in 2025. A revised 2025 value retrieved in 2027 cannot be substituted into a 2026 backtest unless the relevant historical vintage is established.

If exact release time is unavailable, preserve that uncertainty and restrict uses that require point-in-time availability.

### A4. Revision and vintage contract

Classify each series/dataset as one or more of:

* immutable release
* version-addressable release
* revised current history
* rolling/candidate data
* modelled estimate
* unknown revision behavior

For mutable sources, one of the following must exist before forecast/backtest use:

1. provider-native vintage/version retrieval
2. provider release archives that establish historical states
3. Psychohistory point-in-time snapshots captured during live operation

A current revised API response alone cannot establish a historical information set.

The adapter must never silently overwrite a prior retrieved value. Revised observations are new revisions linked to the same underlying metric/reference period with separate retrieval/provenance information.

### A5. Semantic and unit contract

Before normalizing values, document:

* source field/series definition
* unit
* seasonal adjustment state where applicable
* nominal/real status where applicable
* currency/base-year semantics where applicable
* geography/entity definition
* population/sample definition where applicable
* measurement versus estimate/model status
* missing-value codes
* confidentiality/suppression flags
* quality/status flags

Unknown meanings remain unknown.

Do not infer a real-world construct from a convenient series name. The exact provider definition is authoritative for what was measured.

### A6. Historical continuity study

Sample enough historical periods to test the intended use horizon.

At minimum inspect:

* schema changes
* field/code changes
* unit/base changes
* classification changes
* geographic changes
* coverage changes
* methodological changes
* breaks in series
* missingness patterns
* revision behavior
* provider version history where available

Historical continuity is series-specific. Passing one dataset-level API test does not prove every indicator inside the dataset is historically comparable.

If continuity only holds after a date, encode a restricted validity period rather than forcing full-history continuity.

### A7. Upstream lineage and independence review

Every proposed source/series needs enough lineage metadata to identify shared upstream evidence with existing sources.

Record, when knowable:

* original data-generating institution
* intermediate compiler/harmonizer
* modelling/imputation layer
* documentary sources for coded-event data
* whether another Psychohistory source reuses the same upstream series

Independence labels should be conservative:

* `independent_mechanism`: materially separate underlying measurement/reporting process
* `partially_shared_lineage`: some shared upstream evidence or reporting institutions
* `duplicate_upstream`: same underlying series/facts redistributed through another provider
* `unknown_lineage`: insufficient evidence to claim independence

Only `independent_mechanism` can support a strong claim of independent cross-source confirmation without further qualification.

Provider names are never a sufficient basis for independence.

### A8. Bounded measurement study

After the source passes A1-A7, define a small experimental measurement.

Required:

* versioned IndicatorDefinition or source-metric definition
* deterministic transformation
* denominator/aggregation rules
* missingness policy
* revision handling
* quality requirements
* known biases
* limitations
* provenance chain
* replay test

The study should prefer a simple transparent metric over a composite or ML-derived measure.

### A9. Admission decision

The admission review records:

* exact dataset/provider version or reference
* evidence artifacts
* passed/failed stages
* allowed use cases
* forbidden use cases
* historical validity range
* license/product restrictions
* lineage/independence classification
* remaining uncertainties
* source registry status recommendation

Admission for bounded research does not imply production use.

## Minimum source admission artifact set

A future source study should normally produce:

* protocol/preregistration or bounded study plan
* source-document snapshots or immutable references
* acquisition manifest
* response hashes/receipts
* parser/schema tests
* historical continuity results
* revision/vintage assessment
* lineage map
* legal/access note
* final source admission report

Exact file names may follow repository conventions at implementation time.

## Source registry policy

The current registry uses provider-level statuses such as candidate, production, rejected and retired.

Do not add a source to `registry/sources.v1.json` merely because it appears in `SOURCE_FAMILY_RESEARCH_2026_09.md`.

A new candidate registry entry should be created only when a bounded source study is actually accepted. The entry must describe observed behavior rather than anticipated behavior.

If future source-lineage requirements cannot fit the current schema without ambiguity, design a versioned successor schema. Do not silently overload existing free-text fields with semantics that downstream code cannot validate.

## Admission restrictions by data type

### Official statistical series

Special attention:

* revision vintages
* publication lags
* rebasing
* seasonal-adjustment revisions
* national-to-international harmonization
* modelled versus reported observations

### Financial/rate series

Special attention:

* business-day/timezone semantics
* fixing/close time
* market holidays
* revised versus final values
* source licensing
* derived versus directly reported rates

### Physical sensor/hazard data

Special attention:

* event version updates
* sensor/network coverage changes
* magnitude/classification revisions
* detection thresholds
* deleted/merged events

### Human-coded event datasets

Special attention:

* coding rules
* source-document lineage
* event inclusion threshold
* candidate versus final datasets
* later recoding
* source availability bias
* coder disagreement/uncertainty where documented

### Modelled estimates

Special attention:

* model/version
* upstream inputs
* forecast versus estimate distinction
* historical revisions
* uncertainty intervals
* use of later data in retrospective model runs

A retrospectively improved estimate can be useful for historical description while still being invalid as a historical forecast input.

## Cost gate

Near-zero cost remains the default during source validation.

Paid access can be proposed only when:

* the source fills a materially important evidence gap
* no sufficiently reliable free alternative exists
* terms permit the intended research/product use
* expected scientific/product benefit is documented
* recurring cost is bounded and owner-approved

Do not reduce sampling quality, provenance, historical validity or evidence retention merely to keep an unsuitable free source.

## Product-license gate

Because Psychohistory may become a public or commercial product, every source receives two separate legal-fit judgments:

* `research_use_fit`
* `future_product_fit`

A source can pass research use while failing or remaining unresolved for product use.

This distinction is especially relevant to candidates such as UN Comtrade, EM-DAT, BIS statistics and some FAO/third-party datasets.

No assumption of future commercial rights may be inferred from free web/API access.

## Independence gate for multi-source state construction

Even after several sources are individually admitted, Gate 6B remains blocked until there are enough validated indicators with sufficiently different upstream evidence.

Before a composite/state model is designed, produce a source-lineage graph and identify correlated/duplicate evidence paths.

At minimum the first multi-source state experiment should contain observations from three materially different evidence mechanisms in addition to or including GKG. The current preferred path is:

* GKG: media/document extraction
* BIS: financial/central-bank reporting
* EIA: physical/administrative energy statistics
* ILOSTAT: labor surveys/administrative/modelled statistics with explicit subtype separation

This composition is a research target, not a claim that these families are already validated or fully independent.

## Fail-closed conditions

Reject, defer or restrict a source when any of these apply:

* intended field meaning is guessed
* provider identity/version cannot be established
* historical values are mutable but no vintage strategy exists for intended backtesting use
* access requires prohibited credential handling
* license forbids intended use
* source silently substitutes another provider on failure
* historical continuity cannot support the proposed period
* reference time and publication time cannot be distinguished where the use case requires it
* duplicate upstream evidence is presented as independent confirmation
* modelled forecasts are mixed with observed data
* missing/suppressed values are converted to zero without source semantics
* source quality is inferred only from provider reputation

## Current application of this standard

No new source is admitted as of 2026-09-07.

The existing GDELT GKG candidate predates this Gate 6A standard but already has extensive source integrity, replay, measurement and semantic-evidence work. Its unresolved historical semantic gate remains governed by the current Phase 5/6A research path.

Future Gate 6A studies should use this standard prospectively.

## Relationship to current project gate

The current accepted project task remains the Phase 6A recovery-target manifest and subsequent bounded evidence recovery only when explicitly authorized.

This source-admission standard is preparation for a later gate. It must not be used to justify starting BIS, EIA, ILOSTAT or any other integration while Gate 3 remains the accepted advancement bottleneck.
