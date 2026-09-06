# Phase 6A.1 — targeted evidence recovery

Baseline: `f7073ab51e4eb0195fa740a38e96c2a945453602`.
Branch: `codex/project-reset-architecture`.
Recommendation: **`ready_for_targeted_human_identity_review`**, not semantic promotion.

## Scope and result

The protocol fixed exactly the existing 19 probable identities and seven conflicts
before retrieval. All 26 were processed; the other 94 records were not retrieved,
including all 92 unavailable cases. No replacement or resampling.

| Identity state, full frozen sample | Before | After |
|---|---:|---:|
| Confirmed | 2 | 6 |
| Probable, manual identity review required | 19 | 15 |
| Conflicting identity | 7 | 7 |
| Unresolved/unavailable | 92 | 92 |

Four targeted cases gained objective identity confirmation: three FOOD_SECURITY
and one WB_2747_UNEMPLOYMENT. Confirmation required dated article metadata,
canonical URI checks and exact response-hash continuity with independently pinned
baseline evidence. Same title/domain or similar subject matter was insufficient.
Remaining conflicts were not subjectively adjudicated or silently relabeled.

Full-sample sufficiency: **E0 114; E1 0; E2 0; E3 6**.
E0/E1 cannot enter semantic-positive review; E2/E3 require confirmed identity and
usable context. The six E3 cases are publisher evidence, not inferred archival copies.
There were **zero human semantic reviews and zero LLM semantic reviews**.

## Retrieval bounds and remaining evidence gaps

37 requests: 26 original publisher URLs, 10 previously recorded same-publisher
canonical/final candidates, one Wayback availability probe. Each publisher case
had at most two fetch attempts. The Wayback probe timed out and its run-wide circuit
closed immediately; no repeated provider queries or exhaustive archive recovery.
Other failures: one URL encoding failure and one HTTP 202 response.

Existing public-IP, pinned-peer, DNS-rebinding, redirect, TLS and size protections
were reused unchanged. Socket timeout: six seconds; checked deadline: 12 seconds;
2 MiB body limit; at most five redirects per top-level fetch. No proxy or bypass.
Successful compact receipts are retained and cached within the run; cache hits: zero.
The command refuses to re-fetch an already captured run. Full article bodies were
transient; none were sent to an LLM or retained as a corpus.

No independent authorship/distinctive-text/source-attribution anchors were available
for syndication. Similar syndicated articles are rejected as evidence, not substituted.
No archive paths were guessed. Wayback access, 15 subjective identity questions and
seven URI conflicts remain unresolved; this task stops after its 26 cases.

## Artifacts and trust

Compact additions in `studies/gkg-semantics-v2/`: `phase6a1-protocol.json`,
`phase6a1-triage.json`, `phase6a1-attempts.json`, `phase6a1-availability.json` and
`phase6a1-preservation.json`. Triage is a 26-case delta over the accepted baseline;
original `evidence.json`, Phase 6A retrieval receipts and availability remain intact.
New failures and identity evidence are linked by receipt hashes, with old metadata
retained when no objective upgrade was established.

The existing 120-row human packet now exposes sufficiency, identity, excerpt,
provenance and evidence hash. Human labels and reviewer IDs remain blank.
The v1.0.1 review-import contract and independently trusted protocol version/hash
binding are unchanged. The new import wrapper additionally blocks E0/E1 and
unsupported syndicated evidence; stale evidence and protocol roots fail closed.

The assessment manifest binds current implementation, original artifacts, the updated
packet and the new delta/protocol. Its baseline root remains recorded separately;
updating it is not a claim of replaying original Phase 6A network acquisition.
Canonical current root:
`6c1de6ebcb0e5f0ea074c55b58debf92442ee36be6bdb09e32a7eff9a4a0e97b`.
Importers must obtain trust from an independently accepted revision, not candidate hashes.

## Verification and stop

Seven new high-value offline tests cover sufficiency/identity gates, similar syndication,
stale evidence/protocol hashes, provider-budget termination, unchanged target metadata
and coherent resealing against an external root. Existing protocol and manifest tests
remain in force. The complete offline suite ran once after implementation: **286 tests,
285 passed, one Windows symlink-permission skip, zero errors/failures** (19.144 s).
The exact final-SHA Ubuntu CI run is verified separately in the completion response.

101 protected files and all 96 raw ZIPs were checked unchanged. Frozen 120 IDs,
token/year/cohort assignments, original URLs, Phase 4/5 and production are unchanged.
No main merge, forecasts, composites, semantic promotion or Phase 6B work.
Next prerequisite: genuine targeted human **identity** review of the remaining 15+7
cases, with separately justified archival access if needed. Six contexts do not justify
launching the planned full independent semantic review.
