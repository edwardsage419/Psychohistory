# Phase 6A: historical evidence recovery foundation

**Recommendation: `continue_evidence_recovery`.** No semantic promotion or Phase 6B review.

## Baseline and scope

Baseline: `b3eb34bdc789bef6a48615639948707e71353ba0`, branch
`codex/project-reset-architecture`, clean after fast-forwarding the existing checkout.
The Phase 5 peer/manifest repairs were retained. Baseline tests: 263, one Windows skip.
Read only AGENTS and relevant Phase 5 recovery, contract, repair and report dependencies.

Commits: `0eba083` freezes the protocol/input reference; `66180cf` implements transport,
identity/import contracts and tests; `0826c60` publishes recovery receipts and the packet.
The final report/replay commit is identified in Git and the completion response.
No forecasting, production activation, composites, ontology or AI semantic review.

## Frozen sample and protocol

All **120 original references**, case IDs, token assignments, years/cohorts and
DocumentIdentifiers match the accepted Phase 5 sample commit `77fe85a` and baseline.
There remain 40 cases each for PROTEST, FOOD_SECURITY and WB_2747_UNEMPLOYMENT.
No resampling or replacement. Canonical sample root:
`3a8710caabb8d571edbbd5f80276e00f25cec26c9622655d3b3db8d7045b9a46`.
[Input reference](../studies/gkg-semantics-v2/frozen-sample-reference.json)
contains hashes rather than duplicated Phase 5 files.

[Protocol v1.0.0](../studies/gkg-semantics-v2/phase6a-protocol.json): original publisher,
then same-path HTTPS candidate when applicable, then a Wayback availability query
nearest the original batch date, then a verified capture within seven days if found.
The [official API documentation](https://archive.org/help/wayback_api.php) supports
URL/timestamp lookup; discovery results alone are never article evidence.
No guessed publisher archives, unrelated search results or syndicated substitutions.
These alternatives remain unresolved without a cheap independent identity locator.

At most four top-level fetch attempts per case, each with at most five redirects;
the top-level budget excludes redirect hops. Responses are capped at 2 MiB, socket
operations at 12 seconds, with a checked 30-second request deadline. OS DNS resolution
is separate from socket timing. Public DNS addresses are pinned to a numeric address;
the actual peer is checked **before HTTP is sent**, TLS verifies the original hostname,
and every redirect is revalidated. No proxies, credentials or certificate bypass.
One preapproved address is attempted per connection; remaining-address fallback is
not implemented. Failures do not prove universal or permanent source unavailability.

## Recovery and identity counts

| Result | Cases |
|---|---:|
| Original references | 120 |
| Obtained publisher response body | 28 |
| `identity_confirmed` with compact context | 2 |
| `identity_probable_manual_review_required` | 19 |
| `identity_mismatch` / conflicting URI | 7 |
| `identity_unresolved`, no usable body | 92 |
| Completed human semantic reviews | **0** |

There were **272 top-level attempts**: 120 original publisher, 34 same-path HTTPS,
118 Wayback availability queries. **All 118 Wayback queries timed out**; zero archived
captures were retrieved. This is a client/method outcome, not evidence of no archive.
The two confirmed cases are FOOD_SECURITY, one each in 2025 and 2026. No other token
has confirmed review context. [Availability](../studies/gkg-semantics-v2/availability.json)
contains year strata and every failure category; none was silently dropped.

Identity confirmation requires matching canonical URI, article metadata and plausible
publication date, plus an independently pinned unchanged Phase 5 response hash or a
verified near-date archive locator. Same title alone is insufficient. Changed publisher
bytes require manual identity review; conflicting article/archive locators are rejected.
The two confirmed cases satisfy the prior-response-hash path. These conditions establish
bounded document identity, not certainty about the exact historical GDELT classifier input.

Only confirmed material exposes a compact excerpt. Phase 5 complete-sentence extraction
is reused under a 25-word title/excerpt budget; longer titles may be omitted. Keyword
cues locate context only: **no semantic labels were assigned**. Full publisher bodies
were processed transiently and not retained. Hashes cannot reconstruct discarded text.

## Packet, import and trust

The [JSON packet](../studies/gkg-semantics-v2/human-review-packet.json) and
[CSV packet](../studies/gkg-semantics-v2/human-review-packet.csv) contain all frozen cases,
identity states, URLs, source/year/token, compact evidence/hash and blank human label
and reviewer ID. No conclusions, aggregate success rates or other reviewer answers.
CSV formula-like text is escaped; canonical evidence remains in JSON.

The [future import contract](../studies/gkg-semantics-v2/review-import-contract.json)
requires known cases, unchanged metadata, fresh evidence hashes, valid labels and an
independently trusted genuine-human registry with attestation. Duplicate annotations,
person IDs or independence groups fail; machines/LLMs cannot become human by relabeling.
Actual human identity/attestation must be supplied by a responsible operator; a schema
cannot establish it. No actual human registry or annotations were invented.

Receipts and evidence are anchored by an independently selected accepted Git revision.
Never adopt a candidate manifest/root as its own authority. Offline replay against
`0826c60` reproduced all six artifacts and the manifest exactly, with zero network calls.
Root: `f0d1a54ebc1d428393aca31e853db269a1f7cc3d347e0d9239cd013b6ffe95de`.
Replay rebuilds packaging/statistics from authenticated captures; it does not claim
re-extraction from discarded bodies. [Replay record](../studies/gkg-semantics-v2/replay.json).

## Tests, CI and preservation

**277 offline tests:** 276 passed, one Windows symlink-permission skip, no errors/failures.
The 14 new high-value tests cover frozen cases, private/DNS-peer/redirect boundaries,
size/time failures, identity/capture mismatches, changed content, stale/altered evidence,
human attestation/duplicates and externally pinned manifest rejection. Normal CI is offline.
Implementation `66180cf` passed **277/277** on Ubuntu, zero skips, in 4.289 seconds:
[CI run 34008554982](https://github.com/edwardsage419/Psychohistory/actions/runs/34008554982).
The exact final documentation HEAD is separately tested and its own CI run reported
in the completion response; this implementation run is not relabeled as final-HEAD CI.

[Preservation](../studies/gkg-semantics-v2/preservation.json) verifies **128 original files**
and **96 ZIPs / 494,483,985 bytes** unchanged, including Phase 2/3/4/5 evidence and
production files/workflows. New compact artifacts total approximately 0.5 MB.
No paid infrastructure, raw deletion, production change or merge to main.

## Phase 6B prerequisites and unresolved work

Only 2/120 cases currently provide confirmed compact context; readiness thresholds
(24 per token, four per allocated year) are unmet. Obtain safe archival connectivity
or independently dated identity locators without weakening peer/TLS/provenance rules;
resolve the 19 manual-identity cases and seven URI conflicts; recover early-year context.
Then register genuine independent human reviewers and import their actual annotations.
No Phase 6B semantic review has begun. Phase 5 remains `continue_semantic_validation`.
