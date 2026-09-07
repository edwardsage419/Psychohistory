# Psychohistory Self-Audit — 2026-09-07

## Scope

This audit reviewed the current Gate 3A research path, evidence-sufficiency semantics, trust-root usage, live GKG validation transport boundaries, startup/governance documents, and the deterministic recovery-manifest preparation chain.

The audit intentionally did not start semantic review, network recovery, composite-state construction, forecasting, calibration, or backtesting.

## Baseline at audit start

The audit began from the accepted `main` state in which Phase 6A.1 machine identity counts were 6 confirmed, 15 probable/manual-review-required, 7 mismatch, and 92 unresolved, with the frozen sample fixed at 120 cases.

Historical Phase 6A.1 artifacts had classified six identity-confirmed non-empty excerpts as E3. Later manifest-preparation documents also treated readiness as E3-only.

## Bug 1: non-empty fallback excerpts could be promoted to E3

### Finding

Evidence-sufficiency version `1.0.0` used a non-empty excerpt as the practical boundary between E1 and E2/E3 once machine identity was confirmed.

The frozen Phase 5 extractor can emit a bounded manual fallback paragraph when no token-cue context is available. Such a fallback is useful for manual inspection but is not automatically sufficient semantic-review context.

This allowed three identity-confirmed fallback paragraphs to be classified as E3 even though they did not satisfy the intended review-context boundary.

### Fix

Evidence-sufficiency version `1.0.1` now requires the accepted token-cue context/locator path for E2/E3 review readiness. Identity-confirmed fallback context remains E1.

Historical evidence files were not rewritten. The correction is represented separately in:

* `studies/gkg-semantics-v2/context-sufficiency-correction.json`
* `docs/PHASE6A1_CONTEXT_SUFFICIENCY_CORRECTION.md`

### Corrected current state

Machine identity remains unchanged:

* confirmed: 6
* probable/manual-review-required: 15
* mismatch: 7
* unresolved: 92

Evidence sufficiency becomes:

* E0: 114
* E1: 3
* E2: 0
* E3: 3

Review-ready context is E2 or E3, so current review-ready total is 3.

Current review-ready token coverage is:

* `PROTEST`: 0 / 24
* `FOOD_SECURITY`: 2 / 24
* `WB_2747_UNEMPLOYMENT`: 1 / 24

The lower-bound token deficit is 69, subject also to the four-per-allocated-year rule.

## Bug 2: readiness was narrowed to E3-only after Phase 6A

### Finding

The accepted recovery protocol distinguishes E2 archive/equivalent context from E3 original/same-publisher context, and semantic import accepts both E2 and E3.

Later coverage/planning documents simplified readiness to E3-only. This had no numerical effect while E2 count was zero, but it would incorrectly reject a future valid dated Wayback context.

### Fix

Current planning now defines review-ready context as E2 or E3.

The current deterministic manifest contract is in `docs/NEXT_ACCEPTED_TASK.md` and the corrected regression oracle is:

`studies/gkg-semantics-v2/recovery-manifest-expected-baseline-v2.json`

The old confirmed-context coverage audit, original manifest preflight/oracle, and `docs/CODEX_EXECUTION_READINESS_AUDIT.md` remain historical provenance for the pre-correction state and are superseded for current execution.

## Bug 3: raw file SHA and canonical object digest were conflated

### Finding

An earlier manifest-readiness instruction attempted to pass `assessment-manifest.json` artifact hashes directly into `phase6a1_recovery.resolve()`.

Those accepted artifact roots authenticate raw file bytes, while `resolve()` authenticates canonical parsed JSON objects. Treating the two digest types as interchangeable caused fail-closed regression failure.

### Fix

The required sequence is now:

1. authenticate raw file bytes against accepted external file hashes
2. parse the authenticated bytes
3. compute the accepted canonical object digest
4. pass that canonical digest into `resolve()`

This preserves an external trust root while using the digest representation expected by the existing resolver.

Historical assessment implementation pins remain historical provenance. Corrected implementation pins are stored separately in the context-sufficiency correction contract.

## Bug 4: live GKG validator transport boundary was weaker than study acquisition

### Finding

The live validator accepted HTTP/HTTPS batch URLs and used default redirect behavior, while the accepted study acquisition path already enforced GDELT HTTPS and provider-preserving redirects.

### Fix

The live validator now:

* accepts explicit GDELT HTTPS batch URLs only
* upgrades legacy HTTP metadata locators to the equivalent GDELT HTTPS acquisition URL before retrieval
* rejects redirects that leave the GDELT HTTPS batch endpoint or downgrade TLS

This transport correction does not rewrite historical study evidence.

## Bug 5: current-state documentation duplicated stale counts

### Finding

README, `CURRENT_STATE.md`, development governance, and ROADMAP duplicated mutable E3 counts. After the evidence-sufficiency correction, several startup documents still reported six E3 contexts and the old 66-context deficit.

`CURRENT_STATE.md` also used wording that could overstate the independence of the 22-case identity review.

### Fix

* `CURRENT_STATE.md` now records the corrected machine/evidence/readiness state and labels the identity layer as model-assisted with final human adjudication, not independent/blinded semantic review.
* README, governance and ROADMAP no longer duplicate mutable exact counts except where the current-state document is explicitly responsible for them.
* Current execution documents refer to the V2 preflight/oracle and evidence-sufficiency `1.0.1`.

## Recovery-manifest consequence

The corrected first bounded batch rule is:

`Tier A AND year_cell_review_ready_count == 0 AND promotion_target_excluded == false`

Under unchanged current inputs, the V2 oracle pins membership at 10 cases. The implementation must derive membership mechanically and must not hard-code the case list as its selection algorithm.

## Preserved scientific boundaries

This audit did not change:

* frozen 120-case membership
* frozen original URLs
* machine document-identity states
* the 13 / 2 / 7 human identity decisions
* historical evidence files
* semantic labels
* semantic promotion status
* production forecasting status

Applicable invariants preserved include I3, I4, I6, I8, I9, I11 and I12.

## Current gate after audit

Gate 3A remains open.

The next accepted task remains deterministic recovery-target manifest generation under `docs/NEXT_ACCEPTED_TASK.md`.

Network recovery remains separately authorized work. Independent semantic review remains blocked until every token has at least 24 review-ready E2/E3 contexts and every allocated year has at least four.