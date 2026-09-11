# Successor Project Migration Packet

Date: 2026-09-11

Status: AUTHORITATIVE MIGRATION HANDOFF FROM PSYCHOHISTORY

## Purpose

This document extracts the reusable design knowledge required to start a clean successor project without carrying Psychohistory's historical research state into the new repository.

The successor project should have a new repository, a new project Genesis, and a new operational state. Its final public name is intentionally unresolved at migration time.

Psychohistory remains the historical source of these methodological ideas and evidence lessons.

## 1. Successor project thesis

Build an independent evidence layer for forecasting systems.

The core question is:

Which forecasts deserve trust, based on what was actually knowable, committed, resolved, and measured at the relevant time?

The long term strategic sequence is:

1. Forecast Trust Core
2. Prospective Forecast Ledger
3. Outcome and Evaluation Ledger
4. Forecast Failure Corpus
5. Model Neutral Trust and Audit Layer
6. Low maintenance public research outputs
7. Institutional audit, benchmark, data, and verification services after evidence and demand exist

The primary moat should come from elapsed prospective history, strong provenance, stable methodology, accumulated failures, and cross method comparability.

Software can be copied. A genuine prospective record that should have existed years earlier cannot be manufactured later without detectable evidence problems if the anchoring and registry design is sound.

## 2. Strategic constraints

The successor project is maintained by one operator and should remain viable under zero or near zero recurring cost for as long as possible.

Avoid competition based on:

1. compute scale
2. frontier model training
3. real time data breadth
4. high frequency prediction
5. prediction market liquidity
6. large forecasting communities
7. large question volume
8. feature rich consumer SaaS
9. expensive always on infrastructure

Prefer:

1. local deterministic execution
2. compact authoritative artifacts in Git
3. content addressed records
4. lightweight open source dependencies
5. static publication when possible
6. SQLite, DuckDB, or Parquet only when a demonstrated need appears
7. bounded scheduled work
8. a small number of high quality, objectively resolvable forecast targets
9. low maintenance institutional products after a defensible evidence record exists

## 3. Core scientific invariants to carry forward

The successor project should restate these as its own versioned scientific invariants before implementation.

### S1. No future information

A historical reconstruction, replay, or simulated forecast may use only information defensibly available at the relevant information cutoff.

### S2. Forecast immutability

Once formally issued, substantive forecast content is immutable. Corrections append new records and preserve the original.

### S3. Versioned semantics

Any definition that can alter historical interpretation, forecast meaning, resolution, scoring, calibration, or numerical output requires an explicit version.

### S4. Historical reproducibility

A claimed historical result must be reproducible from retained or reproducibly referenced evidence, code, configuration, and relevant versions.

### S5. Independent outcome resolution

Outcome rules must be fixed independently enough to prevent hindsight driven reinterpretation after the result is known.

### S6. Evidence traceability

Consequential observations, features, forecasts, resolutions, and evaluation results require a defensible evidence chain.

### S7. Observation is not reality

A measured signal remains an observation or proxy unless independently validated for the stronger real world construct being claimed.

### S8. Explicit uncertainty

Unknown, unavailable, ambiguous, conflicting, and insufficient evidence states remain explicit.

### S9. No silent historical rewrite

Bug fixes, revised data, definition changes, improved extraction, or model changes must not silently replace authoritative historical outputs.

### S10. Evaluation integrity

Scoring and calibration must account for the forecast system and cohort that actually existed under the accepted protocol. Forecasts cannot disappear because they are inconvenient or perform poorly.

### S11. Genuine human evidence remains human

A protocol requirement for genuine independent human judgment cannot be satisfied by an LLM, synthetic persona, or relabelled machine output.

### S12. Missing evidence cannot be reasoned into existence

Model strength cannot convert absent evidence or unknown historical state into valid evidence.

## 4. Point in time data semantics

The successor data model must distinguish these concepts when applicable:

1. reference period
2. publication time
3. defensible availability time
4. retrieval time
5. revision or vintage identity
6. revision publication time
7. provider or source version
8. source snapshot or trusted source reference
9. transformation version

Required rule:

All forecast inputs must satisfy `available_at <= information_cutoff` under the accepted source contract.

A current revised historical API value cannot silently replace a missing historical vintage in a point in time evaluation.

When availability cannot be established with enough precision for the intended use, the observation is ineligible for that point in time claim.

## 5. Causal transformation rule

Every transformation used for historical simulation or live issuance must declare whether it is stateless or fitted.

A fitted transform should bind:

1. fitting window
2. fit information cutoff
3. input snapshot root
4. fitted state or parameter identity
5. code and version identity

Future information must not enter through normalization, PCA, thresholds, imputation, embeddings, seasonal adjustment, detrending, ranking, or any other fitted preprocessing step.

## 6. Minimum Forecast Trust Core object model

The first implementation should define separate versioned contracts for the following objects.

### 6.1 Target definition

Minimum semantics:

1. target ID
2. target version
3. forecast class
4. formal question semantics
5. allowed outcome or category space
6. geography or entity rule when applicable
7. reference period and horizon rules
8. target measurement or source rule
9. revision or vintage policy when applicable
10. ambiguity policy
11. unresolved policy
12. resolution deadline rule
13. substantive content identity

### 6.2 Resolution rule

Minimum semantics:

1. rule ID and version
2. compatible target identity
3. source hierarchy
4. source conflict policy
5. evidence sufficiency rule
6. allowed resolution states
7. vintage selection rule
8. deadline
9. ambiguity and unresolved handling
10. substantive content identity

Resolution must permit explicit unresolved states.

### 6.3 Point in time evidence snapshot

Minimum semantics:

1. snapshot ID
2. information cutoff
3. snapshot creation or close time
4. deterministic member list
5. source identity for each member
6. applicable reference, publication, availability, retrieval, and vintage times
7. transformation or definition version where derived
8. content identity or source reference
9. trusted upstream root where required
10. deterministic snapshot root

Unknown required availability fails closed.

### 6.4 Forecast method

Minimum semantics:

1. method ID and version
2. method family
3. compatible forecast classes
4. required inputs
5. implementation identity
6. fitted state identity when applicable
7. model identity when applicable
8. prompt or configuration identity when applicable
9. retrieval and tool policy
10. randomness and seed policy when applicable
11. probability and post processing semantics
12. limitations
13. substantive content identity

### 6.5 Forecast run attempt

Minimum semantics:

1. attempt ID
2. method identity
3. start and end times
4. information cutoff
5. input snapshot references
6. run status
7. failure or abort reason when applicable
8. output reference if successful
9. configuration or seed when applicable
10. tool or evidence log reference when applicable

Minimum terminal states:

1. issued
2. failed_pre_issue
3. aborted_pre_issue
4. invalid_pre_issue

Retries require distinct attempt IDs.

### 6.6 Issued forecast

Minimum semantics:

1. forecast ID
2. claimed issuance time
3. information cutoff
4. forecast class
5. target identity and hash
6. horizon
7. entity or geography scope when applicable
8. probability or predictive distribution
9. method identity and hash
10. model or configuration identity when applicable
11. evidence and feature snapshot roots
12. resolution rule identity and hash
13. consequential code identity
14. run attempt reference
15. substantive content hash
16. lifecycle status

The local claimed issuance time is metadata. It does not alone establish genuine prospective status.

### 6.7 Prospective issuance anchor receipt

Minimum semantics:

1. anchor receipt ID
2. anchor scheme and version
3. forecast substantive hash or deterministic batch root
4. external reference or proof material
5. independently observed or derived anchor time semantics
6. verification method version
7. verification status
8. proof content identity
9. delay or finality semantics when applicable
10. receipt content identity

The anchor exists to make retrospective backdating materially detectable.

A local clock, file modification time, operator controlled Git timestamp, generated UUID time component, or digital signature without an independently trusted time source is insufficient as the sole prospective time proof.

The core schema should remain provider neutral. The Genesis protocol selects and tests the actual low cost anchor mechanism.

### 6.8 Forecast correction

Minimum semantics:

1. correction ID
2. original forecast ID
3. correction time
4. correction type
5. reason
6. affected fields
7. authority or reviewer reference when applicable
8. corrected metadata or replacement forecast reference when applicable
9. scoring consequence classification
10. content identity

Probability, target, or horizon changes cannot be disguised as ordinary metadata corrections.

## 7. Trust root rule

A scientific object cannot authenticate its own upstream semantics merely by repeating hashes inside itself.

Consequential target, method, resolution, evidence, and anchor bindings must be checked against independently supplied or independently authenticated trusted objects or roots.

Tests should include an attack in which an upstream object is altered and all downstream hashes are recomputed. Validation must still fail when the independent trusted root remains unchanged.

## 8. Canonicalization rule

Use one documented deterministic canonical representation for scientific JSON objects.

Minimum properties:

1. UTF 8
2. deterministic key ordering
3. deterministic separators
4. deterministic newline policy
5. no random identifiers generated during validation
6. no wall clock values injected by canonicalization
7. a content hash excludes its own hash field
8. hash coverage is explicit for each object type
9. identical input and trusted roots produce identical validation results

SHA 256 is an acceptable default unless the successor project records a different deliberate decision.

Do not invent a custom cryptographic protocol when established primitives are sufficient.

## 9. Forecast classification

Keep at least three historical experiment classes distinct.

### Genuine contemporaneous forecast

The forecast actually existed prospectively with a preserved admissible information set and qualifying independent time anchor.

### Faithful historical replay

The historical method and information environment are reconstructable closely enough to support the stated replay claim.

### Retrospective model experiment

A later method or model is applied to historical inputs after the outcome period.

A current LLM used on an old date normally belongs in the retrospective class because parameter level future information may exist even when the explicit evidence packet is historical.

A prompt instructing the model to pretend it is an earlier year does not control that leakage.

## 10. Retrieval rule for historical experiments

Strict historical retrieval requires:

1. frozen corpus membership
2. admissible availability time for every document
3. a cutoff safe index
4. ranking features that do not use later outcome, popularity, or citation information
5. retrieved document identities included in the evidence snapshot

Current live web search is unsuitable for strict historical replay unless it operates against a defensible preserved historical environment.

## 11. Outcome and evaluation layer

After prospective forecasts begin resolving, add separate objects for:

1. outcome resolution
2. evaluation cohort manifest
3. evaluation result
4. calibration analysis when useful

Outcome resolution should preserve target and rule versions, evidence, source vintage, resolver provenance, ambiguity, conflicts, and unresolved states.

Confirmatory evaluation should freeze its cohort and scoring policy before result inspection.

The result should account for all forecasts within scope through explicit counts such as issued, eligible, resolved, unresolved, excluded, failed where relevant, and final scoreable denominator.

## 12. Baseline parity

Forecast comparisons must distinguish modeling value from information advantage.

Compared methods should use compatible admissible information sets unless the experiment explicitly studies additional information value.

Transparent baselines should be first class forecast methods. Useful initial families include historical base rates, persistence, simple trend rules, and simple statistical models.

## 13. Forecast Failure Corpus

The Failure Corpus should be derived from real resolved history after enough outcomes exist.

A failure record should be able to bind:

1. forecast identity
2. method identity
3. information set identity
4. uncertainty
5. outcome and resolution provenance
6. score and baseline comparison
7. error or failure class when evidence supports one
8. known data, method, semantic, regime, retrieval, or resolution limitations
9. correction history
10. unknown causal classification when the evidence cannot support a stronger explanation

Do not turn failure analysis into retrospective storytelling. Preserve `unknown` when causal attribution is unsupported.

## 14. Model neutrality

The project should evaluate forecasting methods rather than depend on owning the strongest model.

Potential future method families include:

1. transparent statistical baselines
2. econometric models
3. language models
4. agentic forecasting systems
5. expert estimates
6. consensus forecasts
7. market implied probabilities where legally and methodologically appropriate

New model generations should increase the value of the evaluation layer by creating additional comparable methods.

Avoid collapsing trust into one opaque universal score. Prefer decomposable performance profiles by target family, horizon, regime, calibration, information set, and failure mode.

## 15. Genesis boundary

The successor repository should implement and adversarially review the Trust Core before issuing its first genuine forecast.

Forecast Ledger Genesis requires a separate accepted protocol that fixes at least:

1. initial target set
2. target versions
3. resolution rules
4. evidence cutoff policy
5. issuance cadence
6. forecast methods and transparent baselines
7. retry policy
8. correction policy
9. external prospective time anchor scheme
10. anchor failure policy
11. evaluation plan
12. publication and retention policy

No synthetic fixture, retrospective experiment, or imported Psychohistory artifact may be presented as part of the successor project's prospective Genesis history.

## 16. What may be reused from Psychohistory

Reuse as design input, with attribution to the predecessor repository:

1. `SCIENTIFIC_INVARIANTS.md`
2. `docs/DECISION_2026_09_07_POINT_IN_TIME_EVALUATION.md`
3. `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md`
4. `docs/GATE7_9_SCHEMA_REQUIREMENTS.md`
5. `docs/FUTURE_EVALUATION_SAFEGUARDS.md`
6. `docs/DECISION_2026_09_11_PROSPECTIVE_TIME_ANCHOR.md`
7. `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`
8. the relevant forecast trust sections of `docs/ARCHITECTURE.md`
9. the low cost and bounded task principles in `AGENTS.md` and `docs/DEVELOPMENT_GOVERNANCE.md`
10. the intended first Trust Core task design preserved in the 2026-09-11 version of `docs/NEXT_ACCEPTED_TASK.md`

Reuse concepts first. Copy implementation only after the successor project independently decides that the implementation is still appropriate.

## 17. What should remain in Psychohistory

Do not migrate these as native successor project state:

1. GKG datasets and evidence
2. the frozen 120 case semantic sample
3. GKG identity classifications
4. GKG evidence sufficiency classifications
5. model assisted human identity review results
6. Phase 1 through Phase 6 research reports
7. GKG acquisition, recovery, semantic, and indicator scripts
8. GKG specific schemas
9. historical Gate 3 recovery queues
10. retired V0.2 application artifacts
11. old project phase numbering
12. historical Psychohistory current state files

These remain available in Psychohistory for provenance, research reuse, and case study purposes.

## 18. Evidence migration rule

The successor project should explicitly record that its methodology was derived partly from Psychohistory.

That provenance statement does not make Psychohistory evidence native evidence of the successor project.

If a specific Psychohistory artifact is later reused in a successor experiment, import it through an explicit source and evidence admission process with its original provenance preserved.

## 19. Recommended clean repository bootstrap

A minimal initial repository can begin with:

1. `README.md`
2. `PROJECT_VISION.md`
3. `SCIENTIFIC_INVARIANTS.md`
4. `ARCHITECTURE.md`
5. `DEVELOPMENT_GOVERNANCE.md`
6. `CURRENT_STATE.md`
7. `DECISIONS.md`
8. `NEXT_ACCEPTED_TASK.md`
9. `docs/POINT_IN_TIME_RULES.md`
10. `docs/FORECAST_TRUST_CORE.md`
11. `docs/PROSPECTIVE_TIME_ANCHOR.md`
12. `schemas/`
13. `src/` or `scripts/`
14. `tests/`
15. one offline CI workflow

Do not create GKG, indicator, frontend, API, database, or live model modules at bootstrap unless a bounded task later justifies them.

## 20. Recommended first development sequence

### Step 0. Project identity

Choose a final project name and repository name. Record the predecessor relationship to Psychohistory.

### Step 1. Bootstrap governance

Create the minimal repository files above. Adapt the extracted invariants to the new project as version 1.0. Keep the current status pre Genesis.

### Step 2. Trust Core v0.1

Implement versioned contracts and deterministic validators for target, resolution rule, evidence snapshot, method, run attempt, issuance, prospective anchor receipt, and correction.

Use synthetic fixtures only.

### Step 3. Adversarial Trust Core review

Attack at least:

1. point in time leakage
2. circular trust roots
3. local timestamp backdating
4. altered upstream objects with resealed downstream hashes
5. forecast mutation
6. correction abuse
7. retry selection bias
8. unknown availability
9. synthetic fixture contamination
10. false prospective classification

### Step 4. Genesis protocol

Select a deliberately small set of objectively resolvable targets and transparent baselines. Select and test the external time anchor mechanism.

### Step 5. First genuine prospective issuance

Start the permanent ledger only after the Genesis protocol passes acceptance.

### Step 6. Long running operation

Favor stable repeated issuance, resolution, evaluation, and preservation over feature growth.

### Step 7. Failure Corpus and trust profiles

Build these only from accumulated resolved evidence.

### Step 8. Commercial interfaces

Add institutional audit, benchmark, data export, API, or hosted products only when evidence history and real demand justify the maintenance cost.

## 21. Initial implementation risk routing

Suggested model routing inherited from Psychohistory:

1. deterministic contract implementation and tests: L2, Terra High
2. new schema semantics or trust boundary decisions: L3 to L4, Sol High
3. unresolved system level methodology after serious Sol review: L5, strongest available research model
4. routine mechanical documentation: lowest reliable model

Model strength never substitutes for missing evidence.

## 22. Success metrics during the first years

Prioritize metrics that strengthen durable assets:

1. percentage of issued forecasts with valid independent time anchors
2. percentage with fully reproducible target, method, evidence, and resolution bindings
3. prospective history duration
4. number of resolved forecasts under stable protocols
5. calibration and baseline relative performance by compatible cohort
6. unresolved and failure accounting completeness
7. reproducibility pass rate
8. ledger integrity verification rate
9. maintenance cost per forecast cycle
10. number and quality of evidence supported failure patterns

Question volume and frontend feature count are secondary.

## 23. New chat bootstrap instruction

When starting the successor project in a new ChatGPT conversation, provide this migration packet and use the following instruction:

"Start a new project from zero using this migration packet as predecessor design input. Do not continue development inside the Psychohistory repository. First choose or confirm the new project name, create a clean project vision and scientific invariants, define the minimal repository structure, and produce the first bounded Trust Core implementation task. Treat Psychohistory as archived provenance. Do not import its GKG research state as native evidence. Preserve the prospective Genesis boundary: no genuine forecast is issued until Trust Core, adversarial review, Genesis protocol, and external time anchoring are accepted. Maintain a zero or near zero recurring cost architecture."

## 24. Final migration state

This packet contains the design knowledge considered necessary for the successor project's initial bootstrap.

The successor project should independently version and own all future schemas, decisions, code, forecasts, anchors, resolutions, evaluations, and failure records from its own Genesis forward.

Psychohistory remains the provenance source for the predecessor methodology and historical measurement research.
