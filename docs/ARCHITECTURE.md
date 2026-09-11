# Target Architecture

Last updated: 2026-09-11

## Status

This document defines the intended architecture after the 2026-09-11 strategic reactivation.

The primary system is a forecast evidence, ledger, resolution, evaluation, failure, and trust architecture. Measurement and indicator research remains a supporting subsystem that can feed forecast evidence when its individual scientific gates are satisfied.

Existing accepted GKG research and historical evidence are unchanged.

## System shape

The target architecture has two cooperating paths.

### Forecast Trust path

Target definition and resolution rule
↓
Point in time evidence and feature snapshot
↓
Forecast method and run attempt
↓
Immutable forecast issuance
↓
Append only correction history
↓
Independent outcome resolution
↓
Frozen evaluation cohort
↓
Scoring and calibration
↓
Forecast Failure Corpus
↓
Method trust profiles and audit outputs
↓
Public exports and institutional interfaces

### Measurement research path

Source registry
↓
Acquisition or source referenced evidence
↓
Normalization
↓
Quality and provenance
↓
Candidate indicators
↓
Semantic and historical validation
↓
Optional validated indicators and state representations
↓
Forecast evidence snapshots when applicable

The measurement path is one producer of forecast inputs. Direct official data, transparent external estimates, and other admissible evidence may also feed a forecast snapshot under an accepted target and method contract.

## Dependency principle

Dependencies are evaluated per forecast and per measurement candidate.

A forecast may enter an experimental prospective ledger when its own target, resolution, point in time evidence, method, and issuance requirements are satisfied.

An unresolved GKG measurement blocks forecasts that depend on that GKG interpretation. It does not block unrelated targets that use independently defensible evidence.

A complete multi source world state model is optional future upstream capability.

## Layer 1: target registry

Every formal forecast requires an immutable versioned target definition.

A target should bind at minimum:

1. target ID and version
2. forecast class
3. formal semantics
4. outcome or category space
5. entity or geography rule where applicable
6. reference period and horizon rule
7. target measurement source rule
8. vintage or revision policy where applicable
9. ambiguity and unresolved policies
10. resolution deadline rule
11. substantive content hash

Changes that can alter scoring meaning require a new version.

## Layer 2: resolution rule registry

Resolution semantics must exist before or at issuance.

A rule should bind:

1. rule ID and version
2. compatible target versions
3. source hierarchy
4. source conflict policy
5. evidence sufficiency requirements
6. vintage selection policy
7. allowed outcome and unresolved states
8. resolution deadline
9. substantive content hash

A later improved rule does not silently replace the version attached to an old forecast.

## Layer 3: point in time evidence and feature snapshots

Each issued forecast binds the admissible information set actually used.

A snapshot must preserve or bind:

1. information cutoff
2. evidence members
3. feature members where applicable
4. source and vintage identities
5. availability timestamps where required
6. transformation state
7. code or definition versions for derived values
8. trusted upstream roots
9. deterministic membership identity

Every member must have been admissible at the forecast information cutoff.

Current revised history cannot silently substitute for unavailable historical vintage data.

Internal hashes alone cannot authenticate altered upstream history when the trust relationship would be circular.

## Layer 4: forecast method registry

Methods are versioned procedures that convert admissible inputs into probabilities or predictive distributions.

A method should bind:

1. method ID and version
2. method family
3. compatible forecast classes
4. required input contract
5. implementation identity
6. fitted state where applicable
7. model identity where applicable
8. prompt and configuration identity where applicable
9. retrieval and tool policy
10. randomness and retry policy
11. probability and post processing semantics
12. known limitations
13. substantive content hash

Transparent baselines use the same method contract where practical.

The architecture remains model neutral.

## Layer 5: run attempt ledger

A run attempt is distinct from an issued forecast.

Allowed terminal states should include:

1. `issued`
2. `failed_pre_issue`
3. `aborted_pre_issue`
4. `invalid_pre_issue`

Retries create new attempt identities when selection among attempts could matter scientifically.

Consequential failed attempts remain auditable under the accepted protocol.

## Layer 6: forecast issuance ledger

Issuance converts a prepared forecast into an immutable scientific record.

Every issuance should bind:

1. forecast ID
2. issued timestamp
3. information cutoff
4. target ID, version, and hash
5. forecast class and horizon
6. probability or predictive distribution
7. method ID, version, and hash
8. evidence and feature snapshot roots
9. resolution rule ID, version, and hash
10. run attempt reference
11. code identity where consequential
12. substantive content hash
13. lifecycle status

Backdated formal issuance is prohibited.

Substantive mutation after issuance must fail verification.

## Layer 7: correction ledger

Corrections append records and preserve the original issuance.

Metadata corrections, invalidation, and replacement forecasts require explicit semantics.

Probability, target, or horizon changes cannot be disguised as metadata corrections.

## Layer 8: outcome resolution ledger

Outcome resolution should be operationally separate from forecast generation where practical.

Each record binds the target and resolution rule versions fixed at issuance, together with evidence references, target data vintage, resolver provenance, resolution timestamp, and resolution state.

Supported states must include defensible unresolved conditions such as ambiguity, insufficient evidence, source conflict, and expired unresolved windows.

A missing resolution does not become a negative outcome merely to increase the scoreable sample.

## Layer 9: evaluation and calibration

Confirmatory evaluation operates on frozen cohort manifests.

A cohort records inclusion and exclusion rules, unresolved treatment, failed run treatment, target and method versions, horizon grouping, dependency grouping, metrics, baselines, and registry snapshot identity before confirmatory score inspection.

Evaluation outputs preserve complete denominator accounting.

Potential metrics include Brier score, log score, calibration measures, discrimination, interval or distribution scoring, and baseline relative performance according to forecast class.

Calibration analyses never rewrite issued forecasts. A learned calibration transform used prospectively becomes a new method component with fitting provenance.

## Layer 10: Forecast Failure Corpus

The Failure Corpus is a first class derived scientific asset.

It should preserve, where evidence supports the classification:

1. forecast identity
2. method identity
3. information set identity
4. issued uncertainty
5. outcome and resolution provenance
6. score and baseline comparison
7. error magnitude or category
8. failure class
9. supporting evidence for the failure classification
10. uncertainty or unknown attribution
11. correction and supersession history

Failure classes may include data quality, missing information, method specification, fitting or calibration, regime change, semantic mismatch, resolution design, retrieval or tool failure, and unknown.

The system must avoid causal overclaiming when an error source cannot be established.

## Layer 11: trust profiles and audit outputs

After sufficient prospective history exists, evaluation may produce method trust profiles by target class, horizon, regime, evidence quality, or other preregistered groupings.

Potential comparison subjects include internal baselines, statistical models, econometric models, language models, agentic systems, expert estimates, public consensus, and market implied probabilities where appropriate.

A leaderboard may summarize results. The underlying verifiable lineage and diagnostic evidence remain the primary asset.

## Layer 12: public and commercial interfaces

Presentation should read prepared authoritative outputs.

Preferred progression:

1. static ledger and methodology views
2. machine readable exports
3. deterministic verifier interfaces
4. historical trust and failure reports
5. private institutional audit packages
6. API or hosted service only when demonstrated demand justifies operating cost

Browser code should never perform hidden scientific transformations that cannot be replayed independently.

## Supporting measurement subsystem

### Source registry

Maintain provider, dataset, terms, access method, update frequency, historical coverage, revision behavior, known biases, cost, documentation, and production status.

### Acquisition and evidence

Adapters should preserve retrieval time, source identifiers, integrity information, explicit failure states, source identity, and machine readable run metadata.

Historical recovery must preserve failed, mismatched, unavailable, and unresolved states.

### Normalized observations

A normalized observation should generally contain observation time, retrieval or availability time, source, metric identity, value, unit, scope, source reference, quality state, and schema version.

Storage technology must remain separable from semantics.

### Quality and provenance

Checks may include schema validity, missingness, duplicates, staleness, distribution shifts, coverage changes, source outage, unit changes, identity conflicts, vintage uncertainty, replayability, and trust root integrity.

### Indicator registry

Every promoted indicator requires explicit definition, source lineage, transformation, units, update frequency, scope, missingness behavior, smoothing or lag policy, known limitations, provenance requirements, version, and promotion status.

Observation channels such as media attention remain observations until validated for stronger interpretations.

### Optional state and trend representation

Composite or latent state construction begins only when enough suitable independent indicators exist for the intended construct.

Weights, normalization, uncertainty, missingness, and component decomposition must remain explicit.

Do not publish a single opaque global risk score.

## AI architecture

AI may serve as one forecast method family and may also assist evidence synthesis, contradiction detection, scenario generation, or operator interfaces.

Formal AI methods must preserve provider or system family, exposed model version, prompt and configuration identity, structured inputs, retrieval and tool policy, run attempt provenance, pre override output where relevant, and issued output.

Private chain of thought is not a required scientific artifact.

A current model applied to historical evidence is classified according to the accepted historical experiment rules. Restricting explicit evidence to an old date does not establish that the model itself lacked later learned knowledge.

## Storage posture

Scientific semantics should be storage independent.

For the current stage prefer:

1. Git tracked JSON or JSONL for compact authoritative contracts and records
2. local ignored storage for large raw evidence
3. SQLite, DuckDB, or Parquet when query volume or artifact size justifies them
4. content hashes and independently trusted roots where appropriate

A production database, object store, or hosted API should appear only when a demonstrated requirement exists.

## Infrastructure cost principle

Default to zero or near zero recurring infrastructure cost.

Paid infrastructure is justified only when a free approach materially harms evidence integrity, reproducibility, reliability, analytical quality, user value, or viable revenue delivery.

Avoid queues, microservices, always on servers, broad scheduled ingestion, and recurring model calls at the current stage.

## Current implementation boundary

The currently authorized implementation boundary is Forecast Trust Core v0.1 as defined in `docs/NEXT_ACCEPTED_TASK.md`.

That task may create the minimum contracts and deterministic verifier needed for future issuance.

It may not issue real forecasts, resolve outcomes, perform confirmatory evaluation, resume GKG network recovery, build a frontend, or introduce production infrastructure.
