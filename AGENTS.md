# Psychohistory Codex Operating Guide

## Mission

Psychohistory is a long horizon, falsifiable evidence system for prospective forecasting.

Its primary goal is to preserve what was known, what forecast method was used, what probability was issued, how the outcome was resolved, how the forecast performed, and what failure evidence accumulated through time.

The project should evolve into an independent evidence layer for machine forecasting and later support public research and institutional forecast auditing.

## Strategic position

The governing strategic decision is `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`.

Primary program sequence:

1. Forecast Trust Core
2. Prospective Forecast Ledger
3. Outcome Resolution and Evaluation
4. Forecast Failure Corpus
5. Model Neutral Trust and Audit Layer
6. Public and Institutional Interfaces

Measurement research remains a supporting track.

An unresolved source or indicator blocks only the claims and forecasts that depend on it. Do not treat one candidate lifecycle as a global project lock.

## Product scope

The mature system may support:

1. verifiable probabilistic forecasts
2. transparent baseline forecasting methods
3. model neutral comparison of forecasting systems
4. longitudinal calibration and error analysis
5. structured Forecast Failure Corpus research
6. independent forecast audit evidence
7. supporting macro observations, indicators, and state representations where scientifically justified
8. downstream evidence for investment research and long horizon decisions

Formal forecast records, scenario analysis, observations, indicators, outcome resolutions, evaluations, and decisions must remain semantically distinct.

## Cost constraint

Default to zero or near zero recurring infrastructure cost.

Prefer local execution, compact Git tracked artifacts, content addressed evidence, standard library or lightweight open source dependencies, static publication, and lightweight local analytical storage.

Paid APIs, models, databases, hosting, or always on services require demonstrated scientific, reliability, product, or revenue value.

## Development horizon

Optimize for ten to twenty years of continuity.

Do not optimize for rapid visual demos, question volume, real time breadth, or model novelty at the expense of provenance, reproducibility, forecast integrity, or sustainable maintenance.

## Current strategic decision

The project was reactivated on 2026-09-11 after a short strategic pause.

The earlier V0.2 application, seven topic dashboard taxonomy, and GDELT DOC 2.0 updater remain retired from the active development tree. Git history preserves them as provenance.

GDELT GKG remains a preserved measurement research candidate. Its current semantic and historical evidence limitations remain valid. GKG recovery no longer controls the global development queue.

The current active task is always defined by `CURRENT_STATE.md` and `docs/NEXT_ACCEPTED_TASK.md`.

## Priority order

Use this order when tradeoffs arise:

1. scientific and provenance integrity
2. prospective ledger readiness and continuity
3. point in time evidence validity
4. immutable issuance and reproducible resolution
5. complete evaluation denominators and transparent baselines
6. failure knowledge and diagnostic value
7. model neutral trust comparison
8. supporting measurement research required by concrete targets
9. low maintenance public research outputs
10. commercial interfaces after evidence and demand exist

Interface richness and infrastructure scale remain low priority until they serve demonstrated value.

## Architecture principles

1. Keep target definitions, resolution rules, evidence snapshots, forecast methods, run attempts, issued forecasts, corrections, outcomes, evaluations, and decision outputs distinguishable.
2. Every consequential derived number must be traceable to source evidence and transformation logic.
3. Preserve timestamps, source versions, target versions, method versions, model versions, prompt or configuration identities, and transformation versions where consequential.
4. Issued forecast substance is immutable. Corrections append history.
5. Evaluation rules should be fixed before confirmatory score inspection.
6. Unknown, ambiguous, unresolved, failed, and insufficient evidence states remain explicit.
7. Avoid circular trust roots. An object cannot validate altered upstream semantics by merely repeating a newly computed hash.
8. Historical replay must obey point in time information rules.
9. Observation channels such as media volume remain observations until stronger interpretation is independently validated.
10. Prefer independent evidence mechanisms over many correlated providers.
11. A complete world state model is optional upstream capability rather than a universal forecast prerequisite.
12. New infrastructure must justify cost and operational burden.

## Authoritative startup context

For substantial Psychohistory work, begin with:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`
4. `SCIENTIFIC_INVARIANTS.md`
5. `docs/DEVELOPMENT_GOVERNANCE.md`
6. `docs/NEXT_ACCEPTED_TASK.md`
7. only the reports, decisions, code, and tests required by the bounded task

Do not rely on chat memory as the primary source of project state when repository evidence is available.

If `CURRENT_STATE.md` conflicts with Git history or immutable evidence, Git evidence wins and the state file must be corrected.

## Governance relationship

`AGENTS.md` governs how Codex executes an already bounded task.

`CURRENT_STATE.md` records the current project state.

`SCIENTIFIC_INVARIANTS.md` records durable scientific constraints.

`docs/DEVELOPMENT_GOVERNANCE.md` governs what should be developed next, dependency scoped gates, task decomposition, human review boundaries, and model allocation.

`docs/NEXT_ACCEPTED_TASK.md` defines the only currently authorized bounded implementation task.

Missing evidence is an evidence problem. Stronger models do not create unavailable historical documents, unknown vintages, missing labels, or genuine human review.

## Working method for Codex

Before implementing a substantial change:

1. Read the authoritative startup context.
2. Inspect only code and tests relevant to the bounded task.
3. Classify the task using L0 through L5 below.
4. State intended change, assumptions, risks, and acceptance criteria when appropriate.
5. Prefer small reviewable changes.
6. Add tests for transformation logic, trust boundaries, and failure behavior.
7. Never fabricate source mappings, timestamp availability, field meaning, validation results, target semantics, or resolution evidence.
8. If a required fact is unknown, preserve the unknown state and stop the affected assumption from entering authoritative logic.
9. Expand scope only when a concrete dependency requires it.
10. Stop once the task and acceptance criteria are satisfied.
11. Do not advance the project to a later gate solely because implementation succeeded.

## Task risk classification and model guidance

### L0: mechanical task

Characteristics include formatting, renaming, comments, and deterministic documentation edits with negligible semantic risk.

Recommended model and reasoning: GPT 5.6 Luna Low.

### L1: local implementation

Characteristics include clear behavior, limited scope, and low scientific impact.

Examples include a small bug fix, straightforward unit test, CLI parameter, or simple implementation from an accepted specification.

Recommended model and reasoning: GPT 5.6 Terra Medium.

### L2: cross file or moderately complex implementation

Characteristics include multiple modules, dependency tracing, nontrivial validation, or migration implementation under an already accepted design without redefining core scientific semantics.

Recommended model and reasoning: GPT 5.6 Terra High.

### L3: architecture or semantic design

Characteristics include a new schema, interface, data model, dependency boundary, or long lived compatibility decision.

Recommended model and reasoning: GPT 5.6 Sol Medium or High according to consequence.

### L4: scientific validity or historical reproducibility risk

Use L4 when a mistake can invalidate forecasts, historical reconstruction, outcome resolution, evaluation, calibration, scoring, point in time admissibility, measurement semantics, probability meaning, or consequential evidence provenance.

Recommended model and reasoning: GPT 5.6 Sol High.

Treat a change as L4 whenever it can alter authoritative historical or prospective scientific meaning unless the change is clearly mechanical under an already accepted contract.

### L5: system level unresolved problem

Use L5 when fundamental architecture or methodology remains uncertain after serious lower level analysis, multiple core assumptions conflict, or a repository wide scientific judgment is required.

Recommended model and reasoning: GPT 6 Astra High.

Astra XHigh is exceptional. Max reasoning is outside the normal workflow.

## Astra authorization discipline

Astra is reserved for a specific unresolved L5 question.

Do not recommend Astra merely because a task is large, contains many files, requires many tests, has difficult CI, has difficult retrieval, has large context, or lacks evidence.

Appropriate Astra use may include unresolved repository wide methodology, fundamental forecast or resolution methodology, difficult leakage audits, or scientific disputes that remain materially uncertain after Sol High analysis.

Once the difficult decision is resolved, reassess and downgrade deterministic implementation to Terra when appropriate.

## Escalation policy

Start with the lowest model expected to complete the task reliably.

Normal escalation path:

Terra Medium → Terra High → Sol Medium → Sol High → Astra High → Astra XHigh

Escalate when one or more of these occurs:

1. root cause cannot be explained
2. repeated implementation attempts fail
3. a proposed fix begins modifying unrelated files
4. architecture or scientific semantics would need to be guessed
5. tests pass while semantic correctness remains uncertain
6. tests conflict with the specification
7. an accepted specification appears to require change
8. historical or prospective compatibility is unclear
9. look ahead leakage may exist
10. probability, calibration, scoring, resolution, or target semantics are affected beyond an accepted mechanical rule
11. trusted root or immutability semantics become ambiguous

Do not escalate because evidence is absent. Record the gap and stop or perform separately authorized bounded evidence recovery.

## Downgrade policy

After architecture or methodology is resolved, reassess the remaining implementation.

Preferred pattern for high risk work:

1. Sol High or Astra High resolves the design or methodology question.
2. Record the accepted specification.
3. Terra High performs deterministic implementation when appropriate.
4. Sol High reviews scientific integrity when protected semantics are affected.

Do not keep using an expensive model merely because an earlier stage required it.

## Protected scientific domains

Substantive changes require explicit semantic review in:

1. target definitions
2. forecast records and probability semantics
3. information cutoff and timestamp availability semantics
4. outcome resolution
5. calibration
6. scoring and cohort selection
7. historical replay and backtesting
8. indicator definitions
9. evidence provenance and trust roots
10. model, prompt, fitted state, and version provenance
11. correction and supersession semantics
12. failure classification when causal claims are involved

Changes that can alter authoritative historical or prospective results should normally be L4 unless implementation is purely mechanical under an accepted design.

## Scientific integrity checks

For every L4 or L5 task, check applicable rules in `SCIENTIFIC_INVARIANTS.md` before declaring completion.

At minimum ask:

1. Was every forecast input admissible at the information cutoff?
2. Does historical reconstruction use later information, later revisions, or a model with unavailable historical knowledge?
3. Can an issued forecast be modified in place?
4. Did a target, indicator, method, resolution, calibration, or scoring definition change?
5. If scientific meaning changed, was a new explicit version created?
6. Is outcome resolution sufficiently independent from the original forecast?
7. Can outcome knowledge influence interpretation of the original target or forecast?
8. Does a historical evaluation preserve the information set that actually existed?
9. Are missing historical values filled using future information?
10. Is calibration calculated over a defensible frozen cohort with complete denominator accounting?
11. Can the result be reproduced from retained evidence, code, configuration, and version metadata?
12. Are important transformations traceable?
13. Can an altered upstream object reseal itself and incorrectly pass verification?
14. Are unresolved and failed states preserved where the accepted protocol requires them?

Passing software tests is insufficient when a scientific invariant remains violated or unresolved.

## Context and token discipline

Do not scan the entire repository by default.

For each task:

1. read authoritative startup files first
2. read only relevant reports and decisions
3. inspect only related code and tests
4. expand scope only because of a concrete dependency
5. avoid unrelated refactoring or cleanup
6. avoid broad source or market research inside an implementation task unless explicitly authorized

The goal is reliable scientific output per unit of compute and maintenance.

## Stop conditions

Stop when:

1. the bounded change is implemented
2. acceptance criteria are satisfied
3. relevant tests pass
4. no unresolved semantic conflict remains
5. no unrelated changes are required
6. applicable scientific integrity checks are complete

Record unrelated findings separately.

## Current phase

Use `CURRENT_STATE.md` for current project state and `docs/NEXT_ACCEPTED_TASK.md` for active implementation scope.

Do not infer current state from old phase reports, the 2026-09-09 pause record, retired prototypes, historical GKG task prose, or prior assistant plans.
