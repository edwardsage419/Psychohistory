# Psychohistory Development Governance

Last updated: 2026-09-11

## Purpose

This document governs what Psychohistory develops next, how work is decomposed, and which decisions belong to GPT, Codex, or a human operator.

`AGENTS.md` governs Codex execution behavior. This document governs project direction and task routing.

The objective is durable scientific and commercial option value per unit of maintenance and compute while preserving evidence quality, reproducibility, historical validity, and the near zero recurring cost constraint.

## Active development authority

Owner decision, 2026-09-11: Psychohistory is reactivated under `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`.

The strategic north star is an independent evidence layer for machine forecasting.

GPT remains the project governance and design layer. Bounded implementation should be routed to the lowest model class that can execute the accepted contract reliably.

Historical plans remain provenance. They do not retain active authority when superseded by accepted current decisions.

## Strategic priority rule

The primary sequence is:

1. Forecast Trust Core
2. Prospective Forecast Ledger
3. Outcome and Evaluation Ledger
4. Forecast Failure Corpus
5. Model Neutral Trust and Audit Layer
6. Public and Institutional Interfaces

Measurement research is a supporting track.

A proposed core task should materially improve provenance integrity, prospective longitudinal history, failure knowledge, trust or comparison value, or low cost durability. Work that improves none of these requires explicit justification.

## Dependency scoped advancement

Scientific dependencies are evaluated at the level of the forecast, method, target, source, or measurement candidate they actually affect.

An unresolved GKG semantic question blocks a forecast that relies on that GKG interpretation. It does not globally block target definitions, ledger infrastructure, or forecasts based on independently defensible evidence.

A formal prospective forecast is authorized only when its own target semantics, resolution rule, information cutoff, evidence provenance, method identity, and issuance integrity satisfy the accepted contracts.

This dependency model replaces the earlier global sequencing assumption that all forecasting work must wait for a complete multi source state representation.

## Responsibility model

### GPT: governance and task planning

When the owner asks to continue Psychohistory, GPT should:

1. read the current accepted state and strategic decision
2. identify the active program track and actual bottleneck
3. distinguish engineering, methodology, evidence, and human dependencies
4. preserve historical evidence and accepted scientific semantics
5. refuse to substitute stronger reasoning for missing evidence or genuine human review
6. decompose work into bounded independently reviewable tasks
7. classify each task L0 through L5 using `AGENTS.md`
8. choose the lowest model and reasoning level expected to complete it reliably
9. define scope, acceptance criteria, stop conditions, and escalation conditions
10. verify that the task strengthens at least one strategic asset
11. produce a bounded Codex prompt only after the design is sufficiently specified

GPT should not advance later scientific claims merely because an engineering task succeeds.

### Codex: bounded execution

Codex should:

1. execute only the accepted bounded task
2. preserve specifications, evidence, provenance, and historical semantics
3. add deterministic validation and adversarial tests where required
4. fail closed on unrecognized scientific semantics
5. stop at the acceptance boundary
6. report unresolved ambiguity rather than silently expanding scope

Codex does not independently authorize a real forecast, scientific promotion, evaluation claim, or commercial deployment.

### Human operator: consequential authority and genuine human evidence

The human operator remains responsible for:

1. approval of major project direction changes
2. final acceptance of consequential work into the authoritative baseline
3. genuine human identity or semantic review when required by protocol
4. consequential target, resolution, measurement, or promotion decisions where governance requires owner approval
5. commercial commitments that create material recurring cost or obligations

An LLM cannot satisfy a protocol requirement for genuine independent human judgment.

## Program gates

### Gate A1: minimum Forecast Trust Core

Question: Can the system represent and verify targets, resolution rules, point in time evidence snapshots, forecast methods, run attempts, issuance, and corrections without circular trust or silent mutation?

Current status: active implementation target.

No real forecast issuance occurs inside this gate.

### Gate A2: adversarial ledger verification

Question: Does the verifier fail on future information, backdated issuance, altered target or method semantics, changed evidence membership, self sealed altered trust roots, invalid probabilities, broken references, and disguised substantive corrections?

Passing ordinary schema validation alone is insufficient.

### Gate B1: Genesis protocol

Question: Has a small prospective forecast program fixed target semantics, resolution rules, evidence cutoff policy, method set, retry policy, correction policy, cadence, and evaluation plan before issuance?

No retrospective record may be represented as prospective Genesis history.

### Gate B2: Forecast Ledger Genesis

Question: Can the first formal forecast be issued as an immutable prospective record under accepted contracts and independently verified afterward?

Genesis should favor low ambiguity targets, low cost public evidence, and transparent baseline methods.

### Gate C: prospective continuity

Question: Can the operator sustain issuance quality over time without increasing question volume or infrastructure faster than audit capacity?

Continuity takes priority over breadth.

### Gate D1: outcome resolution

Question: Can outcomes be resolved under the versions fixed at issuance while preserving ambiguity, insufficient evidence, source conflict, and expired unresolved states where required?

### Gate D2: confirmatory evaluation

Question: Can a frozen cohort account for every forecast in scope before confirmatory score inspection and preserve baseline information parity, dependency structure, and complete denominators?

Look ahead leakage is a blocking failure.

### Gate E: Forecast Failure Corpus

Question: Can forecast errors be classified with explicit evidence and uncertainty without inventing causal explanations?

Unknown failure attribution is an acceptable state.

### Gate F: model neutral trust evaluation

Question: Is there enough prospective evidence to compare method families under common target, information, resolution, and scoring rules?

Leaderboards remain secondary to reproducible evidence and failure diagnostics.

### Gate G: public research interface

Question: Can authoritative prepared outputs be exposed with low maintenance burden and no hidden browser side scientific transformations?

### Gate H: institutional commercialization

Question: Does accumulated evidence support a product an institution will pay for, and can delivery preserve scientific independence and low maintenance operation?

Paid infrastructure requires demonstrated revenue or a clearly evidenced reliability need.

## Supporting measurement gates

Each source or indicator candidate independently uses these gates:

### M1: source and evidence integrity

Can the source be acquired, preserved or referenced reproducibly, parsed safely, and traced through provenance?

### M2: measurement validity

Is the transformation explicit, versioned, reproducible, and empirically understood?

### M3: semantic and historical stability

Is there sufficient evidence that comparisons are interpretable across the intended period?

### M4: independent validation

Where genuine human or independent source validation is required, has it actually occurred?

### M5: experimental indicator promotion

Is the measurement sufficiently supported for explicitly experimental use under a recorded definition and limitation set?

Candidate failure, restriction, or pause is a valid outcome.

## Current GKG interpretation

GKG remains a preserved experimental media attention candidate within Track M.

Its accepted frozen sample, machine identity states, evidence sufficiency correction, human identity review, missingness safeguards, and historical evidence remain unchanged.

The pre reactivation deterministic GKG recovery target manifest remains preserved in Git history. Further recovery requires a new bounded information gain decision and no longer controls the project wide queue.

GKG does not need to succeed before Forecast Trust Core implementation or Forecast Ledger Genesis unless the selected Genesis target explicitly depends on GKG semantics.

## Evidence versus reasoning rule

Always distinguish insufficient reasoning from insufficient evidence.

Examples of evidence limitations include unavailable historical documents, unresolved document identity, unknown vintage data, absent independent labels, unknown model versions, and missing source documentation.

When evidence is insufficient:

1. record the gap
2. determine whether bounded recovery is justified
3. obtain genuine human review when required
4. preserve unknown or ambiguous states
5. stop the affected scientific claim when its dependency remains unmet

Stronger model reasoning does not create missing evidence.

## Task decomposition rule

Decompose broad work into separate units where applicable:

1. methodological or architectural decision
2. deterministic contract implementation
3. tests and adversarial regression protection
4. evidence acquisition
5. analysis of collected evidence
6. final scientific judgment

Classify each component separately.

Typical routing:

1. mechanical documentation or formatting: L0, Luna Low
2. local deterministic implementation: L1, Terra Medium
3. cross file engineering, validators, bounded retrieval: L2, Terra High
4. architecture, schema, or semantic design: L3, Sol Medium or High
5. scientific validity decisions: L4, Sol High
6. unresolved system level methodology: L5, Astra High

Astra is exceptional and task specific.

## Astra authorization policy

Astra may be appropriate for consequential unresolved questions such as repository wide methodological integrity, difficult point in time leakage analysis, fundamental resolution methodology, calibration methodology with conflicting assumptions, or core scientific design that remains materially uncertain after Sol High review.

Large file count, routine implementation, CI failure, retrieval difficulty, or unavailable evidence do not by themselves justify Astra.

After a design question is resolved, deterministic implementation should return to Terra when appropriate.

## Cost discipline

The project should optimize for reliable completed work per unit of compute and maintenance.

Default to zero or near zero recurring infrastructure cost.

Avoid permanent services, broad scheduled collection, paid databases, distributed systems, and recurring model calls until a demonstrated scientific or commercial need exists.

Static artifacts, local execution, Git provenance, and lightweight storage are preferred during the trust and ledger foundation stages.

## Standard continuation procedure

When the owner says to continue Psychohistory, GPT should return a bounded next task with:

1. active program track and gate
2. current authoritative baseline
3. actual bottleneck
4. strategic asset strengthened
5. next bounded task
6. L0 through L5 classification
7. recommended model and reasoning level
8. human dependency
9. files and modules in scope
10. important exclusions
11. acceptance criteria
12. stop conditions
13. escalation conditions
14. ready to use Codex prompt

Before recommending work, check whether an evidence or human dependency blocks the specific claim being advanced.

Do not globally route back to GKG recovery unless a current accepted decision makes GKG the relevant dependency.

## Current governance interpretation

Project status is `ACTIVE_STRATEGIC_REALIGNMENT`.

Primary active track is Forecast Trust Core.

The accepted next task is `docs/NEXT_ACCEPTED_TASK.md`, which implements minimum forecast ledger contracts and deterministic verification without real issuance.

Existing future forecast architecture and safeguards are now active design constraints for this bounded implementation. They remain constraints rather than evidence that production forecasting is already scientifically validated.

No current task authorizes real forecast issuance, outcome scoring, GKG network recovery, a frontend, multi user architecture, or paid infrastructure.

## Updating this policy

Change this document when the governance model, active program structure, or dependency interpretation changes materially.

Mutable counts and active evidence state belong in `CURRENT_STATE.md`. Bounded implementation scope belongs in `docs/NEXT_ACCEPTED_TASK.md`.
