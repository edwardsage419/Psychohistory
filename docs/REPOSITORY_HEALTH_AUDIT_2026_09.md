# Psychohistory Repository Health Audit — 2026-09

## Purpose

This audit records the repository-wide maintenance review performed after acceptance of Phase 5-6A.1 and completion of the targeted human identity review.

It supersedes `docs/REPOSITORY_AUDIT.md` only as a description of the current repository. The earlier audit remains an immutable historical snapshot and should not be rewritten.

This audit is operational and architectural. It does not change scientific evidence, frozen sample membership, semantic conclusions or readiness thresholds.

## Baseline reviewed

Authoritative branch: `main`.

Scientific state at audit time:

* frozen semantic sample: 120 references
* confirmed E3 contexts: 6
* `PROTEST`: 0
* `FOOD_SECURITY`: 5
* `WB_2747_UNEMPLOYMENT`: 1
* human identity decisions: 13 `SAME_ARTICLE`, 2 `DIFFERENT_ARTICLE`, 7 `INSUFFICIENT_EVIDENCE`
* genuine human semantic reviews: 0
* current bottleneck: historical document identity and objective evidence sufficiency

The accepted next scientific task remains the deterministic recovery-target manifest in `docs/NEXT_ACCEPTED_TASK.md`.

## Overall assessment

### Scientific boundaries: healthy

The repository consistently separates:

* source observations from real-world claims
* media attention from severity or event counts
* machine evidence from human evidence
* identity review from semantic review
* experimental indicators from production promotion
* evidence recovery from forecasting

`SCIENTIFIC_INVARIANTS.md`, the Phase 5/6A protocols, evidence artifacts and current state remain aligned on these boundaries.

### Evidence traceability and reproducibility: healthy

The repository contains versioned schemas, source metrics, provenance, replay artifacts, preservation manifests, trust material, bounded recovery artifacts and adversarial regression tests.

No repository-wide evidence-chain defect was found during this maintenance review that would justify reopening accepted Phase 1-6A.1 work.

The current problem remains evidence sufficiency, not a known failure of the accepted evidence architecture.

### Repository governance: required cleanup

Several operational and documentation artifacts still reflected the earlier architecture-reset/V0.2 period. These could misroute future GPT/Codex work even though the accepted scientific state had advanced.

The cleanup actions below were therefore treated as repository-governance maintenance rather than scientific reinterpretation.

## P0 findings and actions

### P0.1 Scheduled legacy updater wrote directly to authoritative `main`

Finding:

`.github/workflows/update-gdelt.yml` ran the retired GDELT DOC 2.0 updater daily with `contents: write`, committed `data/gdelt.json`, and pushed directly to `main`.

Observed consequence:

The authoritative branch advanced automatically to commit `9591953d5557db62892ca3497508411e3ac95c91` with `chore: update GDELT data (2026-09-06)`, even though the current scientific bottleneck is unrelated to that dashboard feed.

Risk:

* unnecessary movement of authoritative HEAD
* provenance noise between scientific commits and transient dashboard refreshes
* stale Codex base references
* continued operation of a retired ingestion path

Action:

The scheduled updater workflow was removed from the active tree. No scheduled workflow should directly commit transient monitoring data to authoritative `main`.

### P0.2 Retired V0.2 application remained active at repository root

Finding:

`index.html`, `app.js`, `style.css`, `data/gdelt.json` and `scripts/update_gdelt.py` remained present even though the research architecture had moved away from the original dashboard and DOC API path.

Risk:

* future sessions could mistake the prototype for the active product architecture
* old seven-topic assumptions could leak back into indicator or product design
* the repository front door implied a product maturity that the validated research core does not yet support

Action:

The V0.2 frontend, static dashboard data and DOC updater were retired from the active tree. Git history remains the recovery/provenance mechanism for those files.

Owner decision:

The earlier Claude-era development direction is abandoned. Active development is GPT-led governance/design plus bounded Codex execution. Historical assistant-specific plans have no authority unless independently accepted into current repository governance or scientific evidence.

## P1 findings and actions

### P1.1 Offline test workflow targeted an obsolete branch

Finding:

`.github/workflows/test.yml` triggered pushes only for `codex/project-reset-architecture` even though `main` is now authoritative.

Action:

The workflow should trigger on pull requests, pushes to `main`, and manual dispatch. This restores direct CI protection for the authoritative branch.

### P1.2 Live validation duplicated the complete unit suite every hour

Finding:

`.github/workflows/validate-gkg.yml` ran hourly and repeated the entire offline unit suite before a live integration check.

Risk:

* unnecessary Actions usage
* coupling offline regression protection to an external-source availability check
* operational emphasis on live GKG availability after the scientific bottleneck moved to historical evidence recovery

Action:

Separate responsibilities:

* `test.yml`: offline regression suite on pull request and `main` push
* `validate-gkg.yml`: low-frequency read-only live integration check plus manual dispatch

Recommended live cadence: daily.

### P1.3 Durable documentation lagged accepted research state

Affected material included:

* `README.md`
* `docs/ROADMAP.md`
* `docs/DEVELOPMENT_GOVERNANCE.md`
* parts of `AGENTS.md`
* `docs/ARCHITECTURE.md`

Typical stale assumptions:

* accepted `main` described as Phase 1-4 only
* Phase 5+ described as still living on an active development branch
* V0.2 frontend described as temporarily retained active code
* roadmap implied old phase numbering should drive implementation order

Action:

Synchronize the durable documents with the accepted Phase 6A.1 state and replace the old phase-driven roadmap with gate-driven development.

`CURRENT_STATE.md` remains the compact mutable operational summary. Scientific evidence remains authoritative over prose.

## P2 findings and deferred items

### P2.1 Old branches

Legacy branches may remain after their relevant work has already entered `main`.

They no longer define active development state. Removing them is repository hygiene only and must not be interpreted as deleting accepted history, which remains in Git commits.

Branch deletion is optional and has no scientific urgency.

### P2.2 Initial repository audit

`docs/REPOSITORY_AUDIT.md` describes a much earlier repository shape and should not be used as current health status.

Action:

Preserve it unchanged as historical evidence. Use this audit and later dated audits for current repository health.

### P2.3 Product frontend

There is intentionally no active frontend after V0.2 retirement.

A new interface should be designed only after validated research outputs justify it. No compatibility requirement with the retired frontend exists.

## Future architecture readiness

The repository already has strong foundations for later work:

* source registry contract
* normalized observation contract
* indicator definition/value/quality/provenance contracts
* replay and validation machinery
* historical evidence recovery contracts
* explicit scientific invariants

It intentionally does not yet contain production forecast, outcome-resolution or calibration systems.

This is appropriate. Those components should be introduced only when their gates are reached.

## Current scientific risks that remain open

Repository cleanup does not resolve:

1. insufficient E3 coverage across the frozen 120 references
2. zero confirmed E3 for `PROTEST`
3. cross-year semantic stability
4. independent genuine human semantic review
5. recall estimation
6. production indicator promotion criteria in practice
7. multi-source state validity
8. future forecast/outcome/calibration methodology

These remain future scientific work, not maintenance defects.

## Invariants checked during cleanup

The maintenance changes must preserve:

* exact frozen 120 membership
* current six E3 contexts
* separate human and machine evidence provenance
* two `DIFFERENT_ARTICLE` negative judgments
* no automatic E3 promotion from human `SAME_ARTICLE`
* no production forecasting
* no composite-state promotion
* no calibration or backtest claims
* no rewriting of Phase 1-6A.1 evidence artifacts

## Post-cleanup repository posture

The desired active tree is now a research repository rather than a mixed research-plus-obsolete-dashboard repository.

The primary operational path is:

GPT governance/design
↓
bounded Codex implementation
↓
offline tests and review
↓
accepted `main`

Scientific advancement remains:

evidence gate
↓
bounded task
↓
mechanical/scientific validation
↓
explicit acceptance
↓
next gate only when authorized

## Audit limitations

This audit is based on repository-wide static inspection of tracked files, workflows, schemas, study artifacts and governance documents plus observed Git history around the legacy updater.

It is not an independent re-execution of every historical study and does not substitute for the preregistered evidence or human-review gates.

Any CI status observed after the maintenance changes is operational verification only and cannot validate unresolved scientific semantics.