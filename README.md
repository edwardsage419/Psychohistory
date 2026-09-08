# Psychohistory

Psychohistory is a long-running, falsifiable evidence and forecasting research project. Its intended chain is:

public observations -> normalized observations -> indicators -> state/trends -> probabilistic forecasts -> outcome resolution -> evaluation/calibration -> decision support

The project is currently still in the measurement and historical-evidence stage. Production forecasting, production composite state, calibration claims and semantic promotion are blocked until the applicable scientific gates are satisfied.

GKG is one experimental media-attention candidate, not the project objective. Failure, restriction or pause of that candidate does not constitute failure of Psychohistory. The long-term objective requires heterogeneous evidence families and falsifiable forecast evaluation.

## Start here

For substantial work, read in this order:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `SCIENTIFIC_INVARIANTS.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. `docs/NEXT_ACCEPTED_TASK.md`
6. Only the files required for the bounded task

Git history and immutable evidence artifacts are the system of record. Chat summaries are secondary context.

## Current accepted baseline

Authoritative branch: `main`.

Accepted research currently includes:

* Phase 1-4 data and measurement foundation
* Phase 5 preregistered semantic audit and frozen 120-reference sample
* Phase 6A bounded historical evidence recovery
* Phase 6A.1 targeted 26-case identity recovery
* completed model-assisted human identity review with final human adjudication for the 22 cases requiring identity review
* evidence-sufficiency correction version `1.0.1`
* current Gate 3 recovery-selection and pivot safeguard

This work remains non-production research.

Current readiness uses review-ready E2/E3 context, with at least 24 review-ready contexts per token and at least 4 per allocated year before independent semantic review begins. Exact current counts are intentionally centralized in `CURRENT_STATE.md` and the machine-readable correction contract rather than duplicated here.

Readiness is a minimum evidence-volume condition. It is not proof that the review-ready subset is representative. Before any GKG semantic promotion, selection/missingness risk must be addressed under `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`.

Current correction artifacts:

* `studies/gkg-semantics-v2/context-sufficiency-correction.json`
* `docs/PHASE6A1_CONTEXT_SUFFICIENCY_CORRECTION.md`

The older confirmed-context coverage audit and original manifest preflight/oracle remain historical provenance for the pre-correction state and are superseded for current planning.

## Current task

The current accepted next task is to generate a deterministic recovery-target manifest over the complete frozen 120-reference sample and prepare the next bounded recovery batch. The frozen sample, document-identity contract and human/machine provenance separation must remain unchanged.

Current execution uses the V2 preparation artifacts and exact task contract in `docs/NEXT_ACCEPTED_TASK.md`. Network recovery is not authorized by the manifest-generation task.

After any later explicitly authorized bounded recovery batch, governance must reassess whether another batch can materially change the scientific decision. Recovery is not an open-ended requirement to rescue GKG.

## Active development model

The active development workflow is GPT-led project governance and design with bounded Codex execution under `AGENTS.md`.

The earlier V0.2 application and its GDELT DOC 2.0 updater have been retired from the active tree. Earlier assistant-specific product plans, including the abandoned Claude-era development direction, are not architectural authority. Git history preserves the retired implementation for provenance and historical inspection.

Do not restore the V0.2 dashboard, seven-topic taxonomy, DOC updater or scheduled direct writes to `main` unless a separately approved historical investigation requires them.

## Scientific boundaries

The project must preserve these distinctions:

* observation is not reality
* media attention is not real-world severity or event count
* machine retrieval is not genuine human review
* model-assisted identity review is not independent/blinded semantic review
* human `SAME_ARTICLE` judgment does not create E2/E3 machine evidence
* missing evidence cannot be reasoned into existence
* reviewable evidence is not automatically representative evidence
* historical outputs and issued forecasts must not be silently rewritten

The full invariant set is in `SCIENTIFIC_INVARIANTS.md`.

## Repository map

* `schemas/`: versioned machine-readable contracts
* `registry/`: source registry material
* `scripts/`: ingestion, validation, replay, indicator and recovery code plus offline tests
* `studies/`: immutable or append-only study artifacts and evidence
* `docs/`: architecture, protocols, reports, decisions, governance and audits
* `.github/workflows/`: offline CI for pull requests and pushes to `main`

The current repository no longer contains an active product frontend. Presentation work is deferred until the research foundation justifies it.

## Local verification

Python 3.12+, standard library only for the current research code:

```sh
python -B -m unittest discover -s scripts -p 'test_*.py' -v
```

Live GKG validation is explicitly integration-scoped:

```sh
python -B scripts/validate_gkg.py --integration
```

Normal offline tests do not require network access.

## Roadmap

Development advances by evidence gates and candidate lifecycles rather than old phase numbering. See `docs/ROADMAP.md`, `docs/DEVELOPMENT_GOVERNANCE.md`, and `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`.

The present bounded bottleneck is Gate 3A historical document identity and review-ready evidence sufficiency for the GKG candidate. The project does not need to force that candidate to succeed in order to preserve progress toward the wider multi-source forecasting objective.
