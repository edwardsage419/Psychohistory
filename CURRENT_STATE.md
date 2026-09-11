# Psychohistory Current State

Last updated: 2026-09-11

## Project status

Status: `ACTIVE_STRATEGIC_REALIGNMENT`.

The owner explicitly reactivated Psychohistory on 2026-09-11 and accepted a revised long horizon strategy. The governing decision is `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`.

The project is now centered on an independent evidence layer for machine forecasting. The primary compounding asset is prospective, immutable, point in time forecast history with reproducible target, evidence, method, resolution, evaluation, and failure records.

The 2026-09-09 pause remains a valid historical decision record. It no longer blocks development after the 2026-09-11 reactivation decision.

## Authority

This file is the compact operational state for continuing Psychohistory across devices, conversations, Codex sessions, and model changes.

Use evidence in this order when project state conflicts:

1. Git history and immutable evidence artifacts
2. this `CURRENT_STATE.md`
3. accepted decision records and task contracts
4. `SCIENTIFIC_INVARIANTS.md`, `AGENTS.md`, and `docs/DEVELOPMENT_GOVERNANCE.md`
5. chat context

Historical scientific evidence remains governed by the exact protocols and artifacts under which it was created.

## Strategic objective

Working position:

Psychohistory is an independent evidence layer for machine forecasting.

The core product question is:

Which forecasts deserve trust, based on what was actually known, issued, resolved, and measured at the time?

The strategic progression is:

Forecast Trust Core
→ Prospective Forecast Ledger
→ Outcome and Evaluation Ledger
→ Forecast Failure Corpus
→ Model Neutral Trust and Audit Layer
→ Public and Institutional Interfaces

The project should gain value as elapsed prospective history accumulates.

## Primary moat

Core durable assets are:

1. prospective records that existed before outcomes were known
2. immutable and replayable provenance
3. long lived method and schema continuity
4. explicit failed, ambiguous, and unresolved records
5. accumulated calibration and error history
6. structured forecast failure evidence
7. cross method comparability under stable rules
8. independence from any one model provider or source family
9. near zero cost durability that permits multi year operation

Software alone is replaceable. Prospective history cannot be recreated after the fact.

## Active program tracks

### Track A: Forecast Trust Core

Status: `PRIMARY_ACTIVE_TRACK`.

Build the minimum contracts and deterministic verifier for target definitions, resolution rules, point in time evidence snapshots, forecast methods, run attempts, issued forecasts, and append only corrections.

The first implementation task must create no real forecasts and require no network service.

### Track B: Prospective Forecast Ledger

Status: `BLOCKED_BY_TRACK_A_MINIMUM_CORE`.

After the minimum Trust Core passes acceptance, define a small curated Genesis forecast protocol and begin genuine prospective issuance. Quality of provenance takes priority over question volume.

### Track C: Forecast Failure Corpus

Status: `FUTURE_AFTER_RESOLUTIONS`.

Accumulate structured error and failure evidence from resolved forecasts, including method, information set, uncertainty, baseline comparison, failure class, and known limitations.

### Track D: Trust and Audit Layer

Status: `FUTURE_AFTER_SUFFICIENT_LEDGER_HISTORY`.

Compare internal and external forecasting methods under common contracts. Potential method families include transparent statistical baselines, econometric methods, language models, agentic systems, expert estimates, public consensus, and market implied probabilities where appropriate.

### Track E: Public and Commercial Interfaces

Status: `FUTURE`.

Preferred sequence is static public views and exports, then machine readable verification, professional research outputs, private institutional audits and custom benchmarks, and finally paid hosted services or APIs when demand justifies recurring cost.

### Track M: Measurement Research

Status: `SECONDARY_BOUNDED_RESEARCH`.

Existing indicator and source validation work remains valid and preserved. GKG remains one experimental media attention candidate. Its recovery path no longer controls the global project queue.

Additional GKG recovery requires a separately accepted bounded task showing useful expected scientific information gain. New source family work should support a concrete forecast target, trust evaluation, or defined measurement question.

## Dependency rule

Forecast authorization is dependency scoped.

A formal experimental prospective forecast may proceed only when its own target semantics, information cutoff, evidence provenance, method identity, resolution rule, and issuance integrity are defensible.

A forecast that depends on an unresolved or unvalidated measurement remains blocked or must be explicitly classified under an accepted experimental protocol.

An unrelated unresolved measurement candidate does not block a forecast whose evidence foundation is independently valid.

This replaces the earlier global sequencing assumption that broad multi source state construction must precede all forecast ledger work.

## Preserved GKG scientific state

The accepted GKG research baseline remains unchanged by strategic reactivation.

The frozen 120 case sample remains immutable.

Current machine identity counts remain:

1. `identity_confirmed`: 6
2. `identity_probable_manual_review_required`: 15
3. `identity_mismatch`: 7
4. `identity_unresolved`: 92

Evidence sufficiency version remains `1.0.1`:

1. E0: 114
2. E1: 3
3. E2: 0
4. E3: 3

Review ready context remains E2 or E3, with current review ready total 3.

The completed model assisted human identity review remains separate provenance with 13 `SAME_ARTICLE`, 2 `DIFFERENT_ARTICLE`, and 7 `INSUFFICIENT_EVIDENCE` outcomes.

Historical semantic stability remains unproven. Recall remains unestimated. Independent semantic review remains unauthorized until its accepted prerequisites are satisfied.

The old deterministic recovery target manifest task in `docs/NEXT_ACCEPTED_TASK.md` as it existed before reactivation is preserved by Git history. It is superseded as the active global next task.

## Current primary gate

Current primary engineering gate: Forecast Trust Core v0.1.

The project already has accepted forecast, outcome, point in time, and evaluation design constraints in:

1. `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md`
2. `docs/GATE7_9_SCHEMA_REQUIREMENTS.md`
3. `docs/FUTURE_EVALUATION_SAFEGUARDS.md`
4. `docs/DECISION_2026_09_07_POINT_IN_TIME_EVALUATION.md`

The active task is defined in `docs/NEXT_ACCEPTED_TASK.md`.

The task should implement minimum machine readable contracts and deterministic validation only. It must not issue a real forecast, start a network service, create a production database, or rewrite historical GKG evidence.

## Immediate sequence

1. Complete and accept Forecast Trust Core v0.1 contracts and verifier.
2. Conduct an adversarial review of issuance integrity, point in time admissibility, external trust roots, and correction semantics.
3. Define a Forecast Ledger Genesis protocol with a deliberately small set of low cost, objectively resolvable targets and transparent baselines.
4. Begin prospective issuance only after the Genesis protocol is accepted.
5. Preserve every issued, failed where policy requires, corrected, unresolved, and resolved record.
6. Add outcome resolution and frozen cohort evaluation as observations mature.
7. Build the Failure Corpus from actual resolved history.
8. Add model comparison and institutional audit capabilities only after sufficient evidence exists.

## Non goals for the current stage

Do not prioritize:

1. a large forecasting community
2. prediction market operation
3. frontier model training
4. high frequency or real time market prediction
5. broad real time news coverage
6. a single opaque global risk score
7. a feature rich frontend
8. multi user authentication
9. paid databases or distributed infrastructure
10. large question volume

## Cost posture

The zero or near zero recurring cost constraint remains active.

Prefer local deterministic execution, Git for compact authoritative artifacts, content hashes, standard library or lightweight open source dependencies, and SQLite, DuckDB, or Parquet only when a demonstrated need appears.

Paid infrastructure requires evidence that it materially improves reliability, reproducibility, product value, or revenue capacity.

## Development routing

Current expected routing:

1. forecast contract implementation and deterministic validators: L2, Terra High
2. new schema semantics or unresolved trust boundary decisions: L3 to L4, Sol High
3. consequential unresolved methodology after serious Sol review: L5, Astra High
4. routine documentation and deterministic tests: lowest reliable model

Model strength never substitutes for missing evidence or required genuine human review.

## Startup procedure

A new GPT or Codex session should begin with:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`
4. `SCIENTIFIC_INVARIANTS.md`
5. `docs/DEVELOPMENT_GOVERNANCE.md`
6. `docs/NEXT_ACCEPTED_TASK.md`
7. only files directly required by the bounded task

Do not default back to the frozen GKG recovery task from pre reactivation history.

## Update rule

Update this file only when project status, primary track, accepted evidence, active task, gate state, major blocker, or operating policy materially changes.
