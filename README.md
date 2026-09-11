# Psychohistory

**Project status: `ARCHIVED_INACTIVE`**

Psychohistory is preserved as a historical research predecessor and methodological provenance repository. Active development was deliberately ended on 2026-09-11 so a clean successor project can start from a new repository and a new prospective Genesis.

No active implementation task exists in this repository.

Read first:

1. `CURRENT_STATE.md`
2. `docs/PROJECT_ARCHIVE_2026_09_11.md`
3. `docs/NEW_PROJECT_MIGRATION_PACKET.md` when preparing the successor project
4. `SCIENTIFIC_INVARIANTS.md` when inspecting historical scientific work

## Why the project was archived

Psychohistory began as a broad social measurement and forecasting research project. It accumulated substantial GKG source validation, lossless parsing, indicator, semantic audit, provenance, evidence recovery, and scientific governance work.

On 2026-09-11 the long term product direction was refined toward a narrower forecast trust system centered on prospective evidence, immutable issuance, independent time anchoring, outcome resolution, evaluation, failure analysis, and model neutral audit infrastructure.

That direction is sufficiently distinct that continued implementation in the historical Psychohistory repository would create unnecessary conceptual and repository baggage. The successor will therefore start clean while preserving Psychohistory as provenance.

## Preserved research

The archive preserves all accepted Psychohistory evidence and research state, including:

1. Phase 1 through Phase 6 research history
2. GKG acquisition and lossless parsing work
3. experimental indicator infrastructure
4. the frozen 120 reference semantic sample
5. evidence recovery and identity work
6. model assisted human identity review with final human adjudication
7. evidence sufficiency correction version `1.0.1`
8. selection and missingness safeguards
9. point in time forecasting and evaluation methodology
10. scientific invariants and decision history

Archiving changes no historical scientific conclusion.

## Successor design material

The reusable forecast trust design has been distilled into:

`docs/NEW_PROJECT_MIGRATION_PACKET.md`

That packet carries forward the design concepts required for a clean successor project, including:

1. scientific invariants
2. point in time and vintage rules
3. target and resolution contracts
4. evidence snapshot rules
5. forecast method and run attempt provenance
6. immutable forecast issuance
7. prospective external time anchoring
8. append only corrections
9. frozen evaluation cohorts
10. baseline parity
11. Forecast Failure Corpus principles
12. model neutral trust evaluation
13. near zero recurring cost discipline

Historical GKG data and project state remain here and do not automatically become native evidence of the successor project.

## Archive guard

While `CURRENT_STATE.md` reports `ARCHIVED_INACTIVE`, do not resume substantive development merely because a roadmap, historical task, design, issue, or prior conversation exists.

Do not implement Forecast Trust Core, Forecast Ledger Genesis, new GKG recovery, new source integration, production forecasting, scoring, frontend work, API work, or production workflows in this repository without a new explicit owner reactivation decision.

Inspection, audit, reproduction, citation, and migration review remain allowed.

## Historical project shape

Psychohistory historically explored the chain:

public observations → normalized observations → indicators → state and trends → probabilistic forecasts → outcome resolution → evaluation → decision support

The later forecast trust design is retained as predecessor methodology. New implementation belongs to the successor repository.

## Local historical verification

The archived research code can still be verified locally using the preserved offline test suite:

```sh
python -B -m unittest discover -s scripts -p 'test_*.py' -v
```

Running tests or reproducing historical results does not reactivate the project.

## Reactivation

Reactivation requires an explicit owner decision recorded in the repository. That decision must explain why the work belongs in Psychohistory rather than the successor project and define a new bounded task.
