# Psychohistory

**Project status: `ACTIVE_STRATEGIC_REALIGNMENT`**

Psychohistory was explicitly reactivated by owner decision on 2026-09-11. The governing strategic decision is `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`.

The project is being developed as an independent evidence layer for machine forecasting.

Its primary long term chain is:

Forecast Trust Core
→ Prospective Forecast Ledger
→ Outcome Resolution and Evaluation
→ Forecast Failure Corpus
→ Model Neutral Trust and Audit Layer
→ Public and Institutional Interfaces

The project is designed to gain value as genuine prospective history accumulates. Immutable point in time records, reproducibility, explicit failures, calibration history, and model neutral comparison are the intended durable assets.

## Start here

For substantial inspection or continuation, read in this order:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`
4. `SCIENTIFIC_INVARIANTS.md`
5. `docs/DEVELOPMENT_GOVERNANCE.md`
6. `docs/NEXT_ACCEPTED_TASK.md`
7. only files directly required for the bounded task

Git history and immutable evidence artifacts remain the system of record for historical scientific evidence.

## Current active task

The current primary track is Forecast Trust Core.

`docs/NEXT_ACCEPTED_TASK.md` defines the bounded implementation of Forecast Trust Core v0.1 contracts and a deterministic verifier.

That task creates machine readable contracts for target definitions, resolution rules, point in time evidence snapshots, forecast methods, run attempts, issued forecasts, and append only corrections.

It creates no genuine forecast and requires no network service.

After acceptance, the next governance work is an adversarial Trust Core review followed by a separate Forecast Ledger Genesis protocol.

## Strategic position

The core product question is:

Which forecasts deserve trust, based on what was actually known, issued, resolved, and measured at the time?

Psychohistory should remain model neutral. Statistical baselines, econometric methods, language models, agentic systems, experts, public consensus estimates, and market implied probabilities may eventually be evaluated under common evidence rules when appropriate.

The project should avoid direct competition on model training scale, community size, prediction market liquidity, real time feed breadth, high frequency prediction, and frontend feature volume.

## Long term moat

The project should accumulate:

1. prospective records created before outcomes are known
2. immutable and replayable evidence lineage
3. long lived versioned target, method, and resolution contracts
4. explicit failed, ambiguous, unresolved, and corrected records
5. calibration and baseline comparison history
6. a structured Forecast Failure Corpus
7. cross model trust profiles under common rules
8. multi year operational continuity at near zero recurring cost

A future competitor can reproduce software more easily than it can recreate years of genuine prospective evidence.

## Supporting measurement research

Psychohistory retains a measurement research track for source validation, observations, indicators, semantic stability, and optional multi source state representations.

GKG remains one preserved experimental media attention candidate. Its frozen sample, accepted evidence, machine identity states, evidence sufficiency correction, human review provenance, failures, and unresolved cases remain unchanged.

GKG recovery no longer controls the global project queue. A future GKG recovery batch requires a separately accepted bounded task.

An unresolved measurement candidate blocks only claims and forecasts that depend on that measurement.

## Scientific boundaries

The project preserves these distinctions:

1. observation is distinct from underlying reality
2. media attention does not establish event severity or prevalence
3. machine retrieval does not count as genuine human review
4. model assisted identity review does not count as independent blinded semantic review
5. missing evidence cannot be inferred into existence
6. reviewable evidence does not establish representativeness
7. formal forecast issuance is distinct from a model run or narrative scenario
8. issued forecast substance cannot be silently rewritten
9. outcome ambiguity and insufficient evidence remain explicit
10. historical experiments must declare their actual information and model availability class

The full invariant set is in `SCIENTIFIC_INVARIANTS.md`.

## Repository map

1. `schemas/`: versioned machine readable contracts
2. `registry/`: source registry material
3. `scripts/`: deterministic tooling, validators, studies, and offline tests
4. `studies/`: immutable or append only research artifacts and evidence
5. `docs/`: architecture, protocols, reports, decisions, governance, and audits
6. `.github/workflows/`: bounded CI

The repository currently has no active product frontend.

## Local verification

Python 3.12 or later, with the current research code primarily using the standard library:

```sh
python -B -m unittest discover -s scripts -p 'test_*.py' -v
```

Live GKG validation remains explicitly integration scoped and is unrelated to the current active Forecast Trust Core task:

```sh
python -B scripts/validate_gkg.py --integration
```

Normal offline tests do not require network access.

## Cost posture

Default to zero or near zero recurring cost.

Prefer local execution, compact Git tracked scientific artifacts, static publication, content hashes, and lightweight analytical storage.

Paid infrastructure should appear only after demonstrated scientific, reliability, product, or revenue need.

## Roadmap

See `docs/ROADMAP.md` for the active program sequence and `docs/ARCHITECTURE.md` for the dependency scoped system design.

The historical project pause is preserved in `docs/PROJECT_PAUSE.md`. The 2026-09-11 reactivation decision supersedes its execution guard for current development.
