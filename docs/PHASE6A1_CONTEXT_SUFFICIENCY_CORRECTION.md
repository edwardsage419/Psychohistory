# Phase 6A.1 Context Sufficiency Correction

Date: 2026-09-07
Status: accepted scientific correction to current planning/evidence-sufficiency interpretation. Historical Phase 6A/6A.1 artifacts remain preserved as historical provenance.

## Finding

A project self-audit found a defect in evidence-sufficiency version `1.0.0`.

The frozen Phase 5 context extractor first searches for a bounded sentence containing the token-specific cue. When no cue-bearing sentence is found, it may return a short fallback paragraph with `manual_context_required=true` so a human can inspect the page manually.

The old Phase 6A.1 `level()` implementation used only `excerpt != ""` to distinguish E1 from E2/E3. Therefore an identity-confirmed article could receive E3 even when the retained excerpt was only the fallback paragraph and did not provide token-cue context.

This contradicted the Phase 6A.1 protocol meaning of E1: identity-confirmed but insufficient context.

## Correction

Evidence-sufficiency semantics are versioned to `1.0.1`.

An identity-confirmed record is review-ready only when its retained compact context is produced through the frozen Phase 5 token-cue path and remains bound to a locator.

Current levels are interpreted as:

* E0: document identity is not confirmed, or the method is outside the accepted equivalence contract.
* E1: document identity is confirmed, but retained compact context is insufficient for semantic review.
* E2: document identity is confirmed and review-ready context is recovered through an accepted dated archive/equivalent path.
* E3: document identity is confirmed and review-ready context is recovered through an accepted original/same-publisher path.

The review-ready set is therefore `{E2, E3}`.

Human `SAME_ARTICLE` remains only recovery guidance. It creates neither E2 nor E3.

## Current mechanical recomputation

The accepted Phase 6A baseline and Phase 6A.1 delta were authenticated against their historical assessment artifact hashes, overlaid with the accepted immutable metadata checks, and re-evaluated under evidence-sufficiency version `1.0.1`.

Machine identity is unchanged:

| Machine identity state | Count |
|---|---:|
| `identity_confirmed` | 6 |
| `identity_probable_manual_review_required` | 15 |
| `identity_mismatch` | 7 |
| `identity_unresolved` | 92 |
| Total | 120 |

Corrected evidence sufficiency:

| Level | Count |
|---|---:|
| E0 | 114 |
| E1 | 3 |
| E2 | 0 |
| E3 | 3 |
| Total | 120 |

Three previously counted E3 records are E1 under the corrected rule:

1. `61c7c1dd513d1d62021d93228f909aef8a2d961f3e850dca97c21ac2b45a3642` (`FOOD_SECURITY`, 2015)
2. `9443d204438f5a3213b4c7b39aec856ba8ae66e5a2d383b5e89817bb4a6b1cc5` (`FOOD_SECURITY`, 2025)
3. `a6140896cd33c01e2e14e4fd8f9a44331ddc16f739648a5ffc945d5daa4fb1dc` (`FOOD_SECURITY`, 2026)

The three current E3 records are:

1. `374a5d91e1d48f34c1c096ce025537660995161964315da7473ebfd68cf8d2ca` (`FOOD_SECURITY`, 2026)
2. `544d11e2fe2d02e978eb4f6c4e4910a4ca5acd309033e115b587195de2e5b7a1` (`FOOD_SECURITY`, 2026)
3. `3971850d00836d8a487c96f2128ac0ebd040bd5cee818d70c42939f90c377d57` (`WB_2747_UNEMPLOYMENT`, 2025)

No current E2 records exist.

## Corrected readiness coverage

The Phase 6A readiness requirement is applied to review-ready identity-confirmed context, meaning E2 or E3 under the versioned sufficiency contract.

Thresholds remain:

* at least 24 review-ready contexts per token
* at least 4 review-ready contexts per allocated year

Current token coverage:

| Token | Review-ready | Required | Deficit |
|---|---:|---:|---:|
| `PROTEST` | 0 | 24 | 24 |
| `FOOD_SECURITY` | 2 | 24 | 22 |
| `WB_2747_UNEMPLOYMENT` | 1 | 24 | 23 |

Current lower-bound token deficit is 69 additional review-ready contexts.

### PROTEST

| Year | Review-ready | Minimum | Deficit |
|---:|---:|---:|---:|
| 2015 | 0 | 4 | 4 |
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 0 | 4 | 4 |
| 2026 | 0 | 4 | 4 |

### FOOD_SECURITY

| Year | Review-ready | Minimum | Deficit |
|---:|---:|---:|---:|
| 2015 | 0 | 4 | 4 |
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 0 | 4 | 4 |
| 2026 | 2 | 4 | 2 |

### WB_2747_UNEMPLOYMENT

| Year | Review-ready | Minimum | Deficit |
|---:|---:|---:|---:|
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 1 | 4 | 3 |
| 2026 | 0 | 4 | 4 |

## Historical artifact preservation

The following remain historical records and are not rewritten to erase the original result:

* `studies/gkg-semantics-v2/evidence.json`
* `studies/gkg-semantics-v2/phase6a1-triage.json`
* `studies/gkg-semantics-v2/phase6a1-availability.json`
* `studies/gkg-semantics-v2/assessment-manifest.json`
* `docs/PHASE_6A_REPORT.md`
* `docs/PHASE_6A1_REPORT.md`
* `docs/PHASE6A1_CONFIRMED_COVERAGE_AUDIT.md`
* `studies/gkg-semantics-v2/recovery-manifest-expected-baseline.json`
* `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT.md`
* `docs/CODEX_EXECUTION_READINESS_AUDIT.md`

They describe the historical state at the time they were produced. For current planning, corrected evidence-sufficiency version `1.0.1`, this document, the V2 recovery preflight, and the V2 expected-output oracle take precedence.

## Implementation correction

Current corrected implementation:

* `scripts/gkg_recovery.py` requires reviewable token-cue context before semantic import and withholds fallback excerpts from newly confirmed evidence.
* `scripts/phase6a1_recovery.py` computes E1 when identity is confirmed but reviewable context is absent.
* the historical assessment implementation pins remain preserved; current corrected implementation is independently bound by `studies/gkg-semantics-v2/context-sufficiency-correction.json`.

Regression tests authenticate the historical evidence/triage file bytes before computing the canonical object digests used by the overlay resolver.

## Scientific non-changes

This correction changes no frozen sample membership, no original URL, no machine identity status, no human identity judgment, no semantic label, and no production promotion.

The current gate remains Gate 3A historical document identity/evidence sufficiency.

Independent semantic review remains blocked because review-ready coverage is far below the frozen threshold.
