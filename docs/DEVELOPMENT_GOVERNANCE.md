# Psychohistory Development Governance

## Purpose

This document governs what Psychohistory should develop next, how work should be decomposed, and which decisions belong to GPT, Codex, or a human operator.

`AGENTS.md` governs Codex execution behavior. This document governs project direction and task routing.

The objective is reliable scientific progress per unit of compute while preserving evidence quality, reproducibility, historical validity, and the project's near-zero-cost development constraint.

## Active development authority

Owner decision, 2026-09-07: active Psychohistory development is governed by GPT and executed through bounded Codex work. The earlier Claude-era product direction and V0.2 application plan are retired.

Historical code and documents remain valid as provenance where Git history, phase evidence or accepted decisions depend on them. They do not remain architectural authority merely because they existed earlier.

When an old plan conflicts with accepted `main`, current governance, scientific invariants or immutable evidence, the accepted current repository state wins.

## Responsibility model

### GPT: governance and task planning

When the owner asks to continue Psychohistory, GPT should act as the project governance layer before producing a Codex task.

GPT should:

1. Read the current accepted repository state and relevant active development reports.
2. Identify the current scientific or engineering gate.
3. Identify the actual bottleneck rather than assuming the next numbered phase should begin.
4. Determine whether the bottleneck is engineering, methodological, evidentiary, or human-dependent.
5. Refuse to substitute stronger model reasoning for missing evidence or required human judgment.
6. Decompose broad phases into independently reviewable tasks.
7. Classify each task L0-L5 using `AGENTS.md`.
8. Recommend the lowest model and reasoning level expected to complete each task reliably.
9. Define scope, acceptance criteria, stop conditions, and escalation conditions.
10. Produce a bounded Codex prompt only after those decisions are made.

GPT should not automatically translate requests such as "continue Phase N" into one large Codex task.

### Codex: bounded execution

Codex should:

1. Execute the bounded task under `AGENTS.md`.
2. Classify the task and warn when the selected model appears below the recommended minimum.
3. Preserve specifications, evidence, provenance, tests, and historical semantics.
4. Stop at the defined acceptance criteria.
5. Report unresolved uncertainty rather than silently expanding scope.

Codex should not independently advance the project to a later scientific gate merely because implementation of the current task succeeds.

### Human operator: authority and genuine human evidence

The human operator remains responsible for:

* genuine human identity judgments when required by protocol
* genuine human semantic review when required by protocol
* approval of consequential promotion decisions
* approval of major changes to scientific definitions or project direction
* final acceptance of consequential work into the authoritative baseline

An LLM must never be relabeled as a human reviewer or used to satisfy a protocol requirement for independent genuine human judgment.

## Development gates

Psychohistory should advance by evidence gates rather than by phase numbering alone.

### Gate 1: source and evidence integrity

Question: Can the source be acquired, preserved or referenced reproducibly, parsed safely, and traced through provenance?

Do not advance a source when acquisition or provenance is unreliable.

### Gate 2: measurement validity

Question: Is the transformation from source data to an observation or indicator explicit, versioned, reproducible, and empirically understood?

A technically reproducible metric is not automatically a valid measure of a real-world condition.

### Gate 3: semantic and historical stability

Question: Is there sufficient evidence that the measurement has an interpretable meaning and that historical comparisons are defensible across the intended time range?

Missing historical evidence is a data problem, not a reason to increase model strength.

### Gate 4: independent validation

Question: Where the protocol requires human or independent-source validation, has that validation actually occurred with sufficient evidence and independence?

Do not infer completion from machine preprocessing, LLM review, or unavailable cases.

### Gate 5: experimental historical indicator promotion

Question: Is the measurement sufficiently supported to enter an explicitly experimental historical indicator registry?

Promotion must record definition version, evidence basis, known limitations, applicable time range, and unresolved uncertainty.

### Gate 6: multi-source state construction

Question: Can multiple independent data families support a defensible representation of a broader real-world state?

Prefer independent evidence families over a more elaborate transformation of one news source.

### Gate 7: forecast registry

Question: Are targets, horizons, timestamps, evidence snapshots, probability semantics, versions, and immutable forecast records sufficiently specified?

Do not begin production forecasting before the measurement foundation is adequate for the intended target.

### Gate 8: outcome resolution

Question: Are outcome definitions and resolution rules specified independently enough to prevent hindsight-driven scoring?

### Gate 9: scoring, calibration and backtesting

Question: Can forecasts be evaluated using only information and rules that would have been available at the relevant historical time?

Look-ahead leakage and retrospective reinterpretation are blocking failures.

### Gate 10: AI forecasting and decision support

Question: Does AI add measurable forecasting or decision value over transparent baselines under the established evaluation framework?

AI sophistication should come after the evaluation system can falsify its performance.

## Task decomposition rule

Never assign one risk level merely because work belongs to the same Phase.

Decompose work into, when applicable:

1. methodological or architectural decision
2. deterministic implementation
3. tests and regression protection
4. evidence acquisition or recovery
5. analysis of collected evidence
6. final scientific judgment

Classify each component separately.

Typical routing:

* mechanical documentation or formatting: L0, Luna Low
* local deterministic implementation: L1, Terra Medium
* cross-file engineering and bounded retrieval: L2, Terra High
* architecture, schema, or semantic design: L3, Sol Medium
* scientific-validity decisions: L4, Sol High
* unresolved system-level methodological judgment: L5, Astra High

Astra XHigh is exceptional. Max is outside the normal workflow.

## Astra authorization policy

Astra should be rare and task-specific.

Astra is appropriate for consequential unresolved questions such as:

* repository-wide methodological integrity review
* unresolved cross-year measurement validity
* fundamental forecast or resolution methodology
* calibration methodology with conflicting assumptions
* difficult look-ahead leakage audit
* core methodology that remains materially uncertain after Sol High analysis

Astra is normally not justified merely because:

* a task is large
* many files are involved
* many tests must be written
* a Phase is important
* retrieval is difficult
* CI is failing
* context is large
* evidence is unavailable
* routine implementation follows an approved design

After Astra or Sol resolves a design question, downgrade deterministic implementation to Terra when appropriate.

## Evidence versus reasoning rule

Always distinguish insufficient reasoning from insufficient evidence.

Examples of evidence limitations include unavailable historical articles, unresolved document identity, missing independent labels, unknown historical classifier versions, and absent source documentation.

Increasing reasoning strength cannot turn absent evidence into valid evidence.

When evidence is insufficient:

1. record the gap
2. determine whether bounded recovery is possible
3. obtain genuine human review when required
4. preserve unknown or ambiguous states
5. stop promotion if the gate remains unmet

## Cost discipline

Default target for ordinary future Codex task volume:

* Luna: about 5%
* Terra Medium: about 30%
* Terra High: about 40%
* Sol Medium: about 10%
* Sol High: about 12%
* Astra High: about 3%
* Astra XHigh: near zero

These are planning targets, not quotas. Scientific risk overrides the percentages.

The intended operating pattern is roughly 75% Terra, 22% Sol, and 3% Astra by task count.

Optimize for reliable completed work per unit of compute, not minimum tokens and not maximum model capability.

## Standard GPT continuation procedure

When the owner says "continue Psychohistory" or equivalent, GPT should produce a next-task decision with these fields:

* Current gate
* Current repository/baseline state
* Actual bottleneck
* Next bounded task
* L0-L5 classification
* Recommended model
* Recommended reasoning level
* Why that model is sufficient
* Whether Astra is authorized
* Human dependency
* Files/modules in scope
* Files/modules explicitly out of scope when useful
* Acceptance criteria
* Stop conditions
* Escalation conditions
* Ready-to-use Codex prompt

Before recommending a new development task, GPT should check whether unresolved evidence or human-review requirements block advancement.

## Current governance interpretation

The authoritative `main` baseline contains accepted Phase 1-4 data/measurement foundation work, Phase 5 preregistered semantic-audit work, Phase 6A bounded historical evidence recovery, Phase 6A.1 targeted identity recovery, the completed model-assisted human identity review, and the confirmed-context coverage audit.

Phase 5-6A.1 remain non-production research and evidence-recovery work. Acceptance into `main` does not semantically promote the three audited GKG tokens.

The current gate is semantic and historical stability with independent evidence validation incomplete. The immediate bottleneck is objective document identity and E3 evidence sufficiency across the immutable frozen 120-reference sample.

The current frozen evidence state remains exactly six E3 contexts: `PROTEST` 0, `FOOD_SECURITY` 5, `WB_2747_UNEMPLOYMENT` 1. The readiness threshold remains at least 24 E3 per token and at least 4 E3 per allocated year before independent semantic review.

The current accepted next task is the deterministic recovery-target manifest defined in `docs/NEXT_ACCEPTED_TASK.md`. It must preserve frozen membership, keep human and machine provenance separate, exclude known mismatches from promotion targets, and stop after manifest plus bounded batch preparation unless network recovery is explicitly authorized.

Do not begin production forecasting, composite-state construction, semantic promotion, calibration claims, or historical backtests that treat unresolved measurement semantics as ground truth.

## Updating this policy

Change this document when the governance model itself changes or when a stale current-governance paragraph would materially misroute future work.

Routine mutable project status belongs in `CURRENT_STATE.md` and accepted task scope belongs in `docs/NEXT_ACCEPTED_TASK.md`.