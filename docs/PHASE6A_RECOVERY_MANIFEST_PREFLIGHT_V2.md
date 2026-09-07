# Phase 6A Recovery Manifest Preflight V2

Date: 2026-09-07
Status: accepted corrected preparation artifact. No network recovery, evidence promotion, semantic review, or semantic promotion occurs here.

## Why V2 exists

The project self-audit identified an evidence-sufficiency bug in version `1.0.0`: identity-confirmed fallback paragraphs without token-cue context could be counted as E3.

`docs/PHASE6A1_CONTEXT_SUFFICIENCY_CORRECTION.md` and evidence-sufficiency version `1.0.1` supersede the old E3-only planning counts.

The historical file `docs/PHASE6A_RECOVERY_MANIFEST_PREFLIGHT.md` remains provenance for the earlier planning state. It must not be used as the current regression specification.

Current machine-readable oracle:

`studies/gkg-semantics-v2/recovery-manifest-expected-baseline-v2.json`

The oracle is a regression aid only. It never authenticates evidence.

## Authoritative state to reproduce

Frozen sample:

* 120 unique cases
* no replacement
* no resampling
* sample SHA-256 `3a8710caabb8d571edbbd5f80276e00f25cec26c9622655d3b3db8d7045b9a46`
* case-ID set SHA-256 `50dace526474525e69f552cc833221c07e5ef91305f755fd8f4ac64c026c9895`

Machine identity:

* confirmed 6
* probable 15
* mismatch 7
* unresolved 92

Corrected evidence sufficiency version `1.0.1`:

* E0 114
* E1 3
* E2 0
* E3 3
* review-ready `{E2,E3}` total 3

Human identity layer:

* SAME_ARTICLE 13
* DIFFERENT_ARTICLE 2
* INSUFFICIENT_EVIDENCE 7

The human identity layer is model-assisted with final human adjudication/attestation. It is separate from machine identity and is not independent semantic review.

## Review-ready coverage

Readiness counts E2 and E3, because both satisfy the accepted semantic-import sufficiency contract.

Token coverage:

* `PROTEST`: 0 / 24, deficit 24
* `FOOD_SECURITY`: 2 / 24, deficit 22
* `WB_2747_UNEMPLOYMENT`: 1 / 24, deficit 23

Total lower-bound token deficit: 69.

Allocated-year coverage:

### PROTEST

* 2015: 0 / 4
* 2016: 0 / 4
* 2020: 0 / 4
* 2023: 0 / 4
* 2025: 0 / 4
* 2026: 0 / 4

### FOOD_SECURITY

* 2015: 0 / 4
* 2016: 0 / 4
* 2020: 0 / 4
* 2023: 0 / 4
* 2025: 0 / 4
* 2026: 2 / 4

### WB_2747_UNEMPLOYMENT

* 2016: 0 / 4
* 2020: 0 / 4
* 2023: 0 / 4
* 2025: 1 / 4
* 2026: 0 / 4

## Trust sequence

Do not confuse file-byte hashes with canonical JSON object digests, and do not let mutable current code redefine the frozen context contract silently.

Use this sequence:

1. Authenticate `studies/gkg-semantics-v1/sample.json` against the frozen sample SHA from `frozen-sample-reference.json`.
2. Verify `studies/gkg-semantics-v1/preregistration.json`, Phase 6A protocol, Phase 6A.1 protocol, `gkg_semantics.py`, `retrieve_gkg_semantics.py`, `gkg_recovery.py`, and `phase6a1_recovery.py` against the current `context-sufficiency-correction.json` bindings.
3. Read the raw bytes of `evidence.json` and `phase6a1-triage.json`.
4. Verify their byte SHA-256 values against the independently accepted `assessment-manifest.json` artifact entries.
5. Parse the authenticated bytes.
6. Compute canonical object digests with the pinned `gkg_semantics.digest()` helper.
7. Pass those canonical digests to `phase6a1_recovery.resolve()` as `base_root` and `delta_root`.
8. Recompute evidence sufficiency using version `1.0.1`.
9. Verify the resulting identity and sufficiency counts against the independently accepted correction contract.
10. Join the human identity layer only after verifying its accepted Git object and frozen metadata.
11. Derive tiers, ranks, coverage, and first-batch membership from the authenticated current view.
12. Only after derivation compare with the V2 oracle.

A freshly computed digest of an unauthenticated candidate file is not an external trust root.

## Review-ready versus recovery target

Rows in E2 or E3 are already review-ready and receive no recovery tier or recovery rank.

E1 rows remain identity-confirmed but context-insufficient. They remain recovery candidates because additional objective recovery may provide a review-ready token-cue context without changing document identity.

Recovery priority and promotion exclusion remain orthogonal.

## Tier precedence

Apply exactly:

1. E2 or E3: no tier and no recovery rank.
2. Human `SAME_ARTICLE` in a deficient allocated-year cell: Tier A.
3. Otherwise human `INSUFFICIENT_EVIDENCE` or `DIFFERENT_ARTICLE`: Tier D.
4. Otherwise machine `identity_mismatch`: Tier D.
5. Otherwise a cell with no remaining review-ready deficit: Tier D.
6. Otherwise machine `identity_confirmed` with E1: Tier B.
7. Otherwise machine `identity_probable_manual_review_required`: Tier B.
8. Otherwise unresolved with an explicit URI-equivalent recovered/canonical locator under the pinned `gkg_recovery.uri()` semantics: Tier B.
9. Otherwise deficient-cell unresolved: Tier C.
10. Residual non-review-ready case: Tier D.

Human `SAME_ARTICLE` takes Tier A precedence even for HIR-11 and HIR-15, while their machine mismatch still sets promotion exclusion.

## Promotion exclusion

Set `promotion_target_excluded=true` when either applies:

* current machine identity is `identity_mismatch`
* human identity decision is `DIFFERENT_ARTICLE`

The current expected union remains seven cases.

No human decision changes machine identity or creates E2/E3.

## Deterministic recovery ordering

For non-review-ready rows:

1. tier A/B/C/D
2. year-cell review-ready deficit descending
3. machine-state rank:
   * confirmed E1
   * probable
   * mismatch
   * unresolved
4. retained non-empty `content_sha256` before absent
5. accepted retrieval-method rank
6. frozen order

No weighted score is allowed.

Normalize the accepted Phase 6A and Phase 6A.1 method vocabulary as follows:

* rank 0: `original_publisher`
* rank 1: `same_path_https_candidate`, `canonical_publisher`
* rank 2: `wayback_availability_discovery`
* rank 3: `dated_wayback_capture`
* rank 4: `unavailable` or no successful evidence method

`canonical_publisher` was introduced by the accepted Phase 6A.1 canonical-policy path and is already treated as same-publisher E3-capable evidence when reviewable. Ranking it with `same_path_https_candidate` is a deterministic method-family normalization only. It does not change identity or evidence sufficiency.

This clarification is necessary because current E1 case `61c7c1dd513d1d62021d93228f909aef8a2d961f3e850dca97c21ac2b45a3642` carries `retrieval_method=canonical_publisher`; the manifest must not falsely stop on an already accepted method.

If a method lies outside the accepted Phase 6A/6A.1 vocabulary above, stop and escalate rather than inventing a new scientific rule.

## Current exact review-ready set

E3:

* `374a5d91e1d48f34c1c096ce025537660995161964315da7473ebfd68cf8d2ca`
* `544d11e2fe2d02e978eb4f6c4e4910a4ca5acd309033e115b587195de2e5b7a1`
* `3971850d00836d8a487c96f2128ac0ebd040bd5cee818d70c42939f90c377d57`

E2: none.

These three receive no recovery tier.

Current E1 cases requiring further context recovery are:

* `61c7c1dd513d1d62021d93228f909aef8a2d961f3e850dca97c21ac2b45a3642`
* `9443d204438f5a3213b4c7b39aec856ba8ae66e5a2d383b5e89817bb4a6b1cc5`
* `a6140896cd33c01e2e14e4fd8f9a44331ddc16f739648a5ffc945d5daa4fb1dc`

## Tier A expectation

All 13 current human `SAME_ARTICLE` cases remain in deficient review-ready cells, so Tier A remains exactly 13 cases under unchanged inputs.

HIR-11 and HIR-15 remain Tier A plus promotion-excluded.

## First bounded batch

Selection rule:

`Tier A AND year_cell_review_ready_count == 0 AND promotion_target_excluded == false`

Under unchanged inputs this produces ten cases. The V2 oracle pins membership, not ordering.

The additional member relative to the historical nine-case oracle is HIR-12 because the `FOOD_SECURITY` 2025 context previously counted as E3 is now E1; the 2025 cell therefore has zero review-ready context.

Do not hard-code the ten IDs as the algorithm.

## Canonical manifest requirements

The canonical machine output keeps all 120 rows in frozen order.

Recommended row fields include:

* frozen order and frozen source-row identity
* case/token/year/cohort/source/original URL
* machine identity status
* evidence sufficiency version and level
* `review_ready`
* human review ID/decision/confidence where present
* year-cell review-ready count/minimum/deficit
* token review-ready count/minimum/deficit
* recovery tier and recovery rank
* promotion exclusion and reason
* objective recoverability signals
* structured rationale codes
* allowed next recovery methods
* immutable replay/provenance references

The canonical output must exclude wall-clock generation timestamps, random IDs, local paths, and environment-specific noise.

## Recovery method vocabulary

The manifest may describe only accepted method families:

* `original_publisher`
* `same_path_https_candidate` when exact applicability exists
* `canonical_publisher` only when an exact same-publisher canonical/final locator already exists in accepted evidence/protocol provenance; never guess the path
* `wayback_availability_discovery`
* `dated_wayback_capture` after exact valid locator discovery

`unavailable` is a state.

The deferred Phase 6A `canonical_publisher_archive` method remains out of scope and must not be confused with Phase 6A.1 `canonical_publisher`.

No broad search, guessed publisher/archive identity, unrelated result substitution, or syndicated replacement is allowed.

This manifest task performs no network recovery.

## Regression checks

Fail closed unless:

* exactly 120 frozen rows and 120 unique IDs
* sample/hash/reference bindings match
* pinned preregistration/protocol/extractor/recovery dependencies match the correction contract
* identity counts are 6/15/7/92
* sufficiency is E0=114, E1=3, E2=0, E3=3
* exact E1/E3 sets match the V2 oracle
* review-ready count is 3
* human counts are 13/2/7
* coverage matches the corrected matrix
* 13 SAME cases are Tier A while their cells remain deficient
* HIR-11/HIR-15 remain Tier A plus excluded
* all mismatches and human DIFFERENT cases are promotion-excluded
* human INSUFFICIENT cases are Tier D unless no tier is possible because a future independently obtained E2/E3 supersedes current state
* the current E1 `canonical_publisher` method maps to rank 1 without a false stop
* first batch membership matches the derived ten-case set under unchanged inputs
* human SAME never creates E2/E3
* frozen machine/human artifacts remain byte unchanged
* repeated generation on identical inputs is byte-identical

## Stop conditions

Stop if frozen membership, authenticated machine inputs, pinned semantic dependencies, corrected sufficiency counts, human counts, coverage, or V2 oracle comparison cannot be reconciled without changing accepted scientific semantics.

Stop if deterministic ranking requires a new scientific criterion or encounters a method outside the accepted Phase 6A/6A.1 vocabulary.

Stop if implementation would modify frozen evidence or human-review artifacts.

Otherwise this remains an L2 deterministic implementation suitable for GPT-5.6 Terra High.
