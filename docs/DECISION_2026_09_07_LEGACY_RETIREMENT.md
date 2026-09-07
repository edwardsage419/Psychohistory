# Decision: Legacy V0.2 Retirement and Active Development Authority

Date: 2026-09-07

Status: accepted owner decision

## Decision

The earlier Claude-era product-development direction is retired. Psychohistory active development is now governed by GPT and implemented through bounded Codex tasks under `AGENTS.md`, `CURRENT_STATE.md`, `SCIENTIFIC_INVARIANTS.md`, and `docs/DEVELOPMENT_GOVERNANCE.md`.

The V0.2 frontend, seven-topic dashboard taxonomy, GDELT DOC 2.0 updater, static dashboard data and scheduled updater are retired from the active repository tree.

Git history preserves those artifacts as historical provenance. Their existence in history does not make them current architecture, current product requirements or current scientific evidence.

## Supersedes

This decision supersedes the temporary 2026-09-06 decision in `docs/DECISIONS.md` that allowed the existing V0.2 frontend to remain temporarily active.

It does not rewrite that historical decision. The earlier decision remains part of the chronological record and is interpreted as superseded from this date forward.

## Scientific impact

None.

This decision does not change:

* the frozen 120-reference sample
* Phase 5, Phase 6A or Phase 6A.1 protocols
* machine evidence or human-review artifacts
* the six current E3 contexts
* token/year readiness thresholds
* semantic conclusions
* blocked production work

## Operational implications

1. Do not restore the V0.2 dashboard or DOC updater as active components without a separately approved bounded reason.
2. Do not treat the old seven-topic dashboard taxonomy as an ontology or indicator requirement.
3. Do not allow transient monitoring jobs to commit directly to authoritative `main`.
4. Use `main` plus the startup governance files as the current development authority.
5. Old branches and old assistant plans are historical context only unless their work has been accepted into `main`.
6. A future frontend should be designed from validated research outputs rather than compatibility with V0.2.

## Rationale

The repository has evolved into a reproducible research system with versioned schemas, evidence preservation, replay, indicator foundations, semantic-audit protocols and historical recovery. Keeping the obsolete prototype active creates routing and maintenance risk without contributing to the current scientific bottleneck.

Retiring active legacy components reduces ambiguity while Git history preserves full recoverability and provenance.