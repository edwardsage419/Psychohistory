# Phase 6A.1 Confirmed Coverage Audit

Date: 2026-09-06
Status: mechanical coverage audit only; no evidence promotion and no semantic review authorization.

## Purpose

Measure the current `identity_confirmed` / E3 coverage of the frozen 120-case `gkg-semantics-v2` sample against the preregistered Phase 6A readiness rule.

This audit treats the accepted Phase 6A evidence set plus the Phase 6A.1 26-case delta as authoritative. Human identity adjudications are recorded separately and are **not** converted into E3 automatically.

## Frozen readiness rule

Phase 6A requires, for each token:

- at least **24 identity-confirmed contexts per token**; and
- at least **4 identity-confirmed contexts per allocated year**.

Failure of either condition means `continue_evidence_recovery`; it does not authorize semantic promotion.

## Current E3 total

The accepted Phase 6A.1 availability summary reports:

- frozen references: 120
- `identity_confirmed`: **6**
- `identity_probable_manual_review_required`: 15
- `identity_mismatch`: 7
- `identity_unresolved`: 92
- E3: **6**
- E0: 114

The six current E3 contexts are:

| Token | Year | Source | Case ID | Origin |
|---|---:|---|---|---|
| FOOD_SECURITY | 2015 | oilprice.com | `61c7c1dd513d1d62021d93228f909aef8a2d961f3e850dca97c21ac2b45a3642` | Phase 6A.1 upgrade |
| FOOD_SECURITY | 2025 | visayandailystar.com | `9443d204438f5a3213b4c7b39aec856ba8ae66e5a2d383b5e89817bb4a6b1cc5` | accepted Phase 6A baseline |
| FOOD_SECURITY | 2026 | latimes.com | `374a5d91e1d48f34c1c096ce025537660995161964315da7473ebfd68cf8d2ca` | accepted Phase 6A baseline |
| FOOD_SECURITY | 2026 | prospect.org | `544d11e2fe2d02e978eb4f6c4e4910a4ca5acd309033e115b587195de2e5b7a1` | Phase 6A.1 upgrade |
| FOOD_SECURITY | 2026 | thehindubusinessline.com | `a6140896cd33c01e2e14e4fd8f9a44331ddc16f739648a5ffc945d5daa4fb1dc` | Phase 6A.1 upgrade |
| WB_2747_UNEMPLOYMENT | 2025 | marketpulse.com | `3971850d00836d8a487c96f2128ac0ebd040bd5cee818d70c42939f90c377d57` | Phase 6A.1 upgrade |

`PROTEST` currently has no E3 contexts.

## Token-level gap

| Token | Current E3 | Required total | Total deficit |
|---|---:|---:|---:|
| PROTEST | 0 | 24 | **24** |
| FOOD_SECURITY | 5 | 24 | **19** |
| WB_2747_UNEMPLOYMENT | 1 | 24 | **23** |
| **Total** | **6** | **72** | **66** |

At least 66 additional frozen cases must become objectively `identity_confirmed` to satisfy the three token-level totals. This is a lower bound; year-distribution constraints must also be satisfied.

## Allocated-year coverage

The frozen evidence set shows the following allocated years.

### PROTEST

Allocated years: 2015, 2016, 2020, 2023, 2025, 2026.

| Year | Current E3 | Minimum | Minimum deficit |
|---:|---:|---:|---:|
| 2015 | 0 | 4 | 4 |
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 0 | 4 | 4 |
| 2026 | 0 | 4 | 4 |

The year minima alone equal the 24-token requirement. Therefore PROTEST must reach at least four E3 cases in every allocated year.

### FOOD_SECURITY

Allocated years: 2015, 2016, 2020, 2023, 2025, 2026.

| Year | Current E3 | Minimum | Minimum deficit |
|---:|---:|---:|---:|
| 2015 | 1 | 4 | 3 |
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 1 | 4 | 3 |
| 2026 | 3 | 4 | 1 |

The minimum year deficits sum to 19, exactly the token-level deficit. FOOD_SECURITY therefore also needs at least four E3 cases in every allocated year.

### WB_2747_UNEMPLOYMENT

Allocated years: 2016, 2020, 2023, 2025, 2026.

| Year | Current E3 | Minimum | Minimum deficit |
|---:|---:|---:|---:|
| 2016 | 0 | 4 | 4 |
| 2020 | 0 | 4 | 4 |
| 2023 | 0 | 4 | 4 |
| 2025 | 1 | 4 | 3 |
| 2026 | 0 | 4 | 4 |

The year minima require 19 additional E3 contexts, but the token total requires 23 additional E3 contexts. After every allocated year reaches four, at least four more frozen unemployment cases must also become E3 in any allocated year(s).

## Effect of the completed 22-case human identity adjudication

The human layer contains 13 `SAME_ARTICLE`, 2 `DIFFERENT_ARTICLE`, and 7 `INSUFFICIENT_EVIDENCE` judgments. These judgments remain separate from machine/protocol evidence.

The 13 `SAME_ARTICLE` cases are useful recovery priorities because a human reviewer found identity continuity plausible, but **none is E3 merely because of that judgment**. Each still has to satisfy the frozen objective identity contract.

Even in the hypothetical best case where all 13 human `SAME_ARTICLE` cases later satisfy the objective E3 contract, total E3 would rise only from 6 to 19, still far below the required 72. Therefore the next recovery phase must include unresolved cases outside the 22-case adjudication set.

## Recovery priority

Priority is determined by scientific leverage, not by ease alone.

### Priority A: human-SAME cases that fill empty or weak year cells

Attempt objective recovery for all 13 human `SAME_ARTICLE` cases, with highest immediate leverage for years currently at zero E3:

- PROTEST 2020: HIR-03
- PROTEST 2026: HIR-06, HIR-07, HIR-08
- FOOD_SECURITY 2020: HIR-09
- FOOD_SECURITY 2023: HIR-11
- WB_2747_UNEMPLOYMENT 2016: HIR-15, HIR-16
- WB_2747_UNEMPLOYMENT 2020: HIR-18
- WB_2747_UNEMPLOYMENT 2023: HIR-19
- WB_2747_UNEMPLOYMENT 2026: HIR-21

The remaining human-SAME cases are also useful:

- FOOD_SECURITY 2025: HIR-12
- FOOD_SECURITY 2026: HIR-13

### Priority B: frozen cases in years with zero E3 and no human-SAME coverage sufficient to reach four

The largest structural gaps are:

- all PROTEST years, especially 2015, 2016, 2023 and 2025 where the completed human-SAME set contributes no candidate;
- FOOD_SECURITY 2016, where current E3 is zero and the completed human-SAME set contributes no candidate;
- FOOD_SECURITY 2015, 2020, 2023 and 2025 after the obvious human-SAME candidates are exhausted;
- WB_2747_UNEMPLOYMENT 2016, 2020, 2023 and 2026 beyond the available human-SAME candidates.

Recovery must operate only on the original frozen references. No replacement cases, guessed alternate articles, or syndicated substitutes are allowed.

### Priority C: human `INSUFFICIENT_EVIDENCE`

These can be retried only with new objective evidence such as an authenticated publisher response satisfying the frozen contract or a verified near-date archive capture. The human uncertainty itself is not a blocker if stronger objective evidence is later recovered.

### Do not pursue as promotion targets

The two human `DIFFERENT_ARTICLE` cases should remain visible as negative identity evidence. Do not replace them with a different article merely to improve coverage.

## Decision

**Result: `continue_evidence_recovery`.**

Independent semantic review is not authorized under the current frozen Phase 6A readiness rule.

The next bounded task should be a recovery-target manifest over the complete frozen 120-case sample, ranked first by year-cell deficit and then by objective recoverability. It must preserve original case identity, evidence hashes, failed attempts, and all human judgments as separate provenance layers.
