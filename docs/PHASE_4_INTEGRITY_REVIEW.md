# Targeted post-Phase-4 integrity review

Starting commit: b3627a059ecf4332291f58cd744941978bb45838, clean working tree.
No next phase is authorized. Existing Phase 2/3 evidence, all 96 raw archives,
protected production behavior and the Phase 4 recommendation remain preserved.

## Reproduced attack and acceptance criteria

At the starting commit, an authenticated PROTEST count of 1 was replaced with 0,
the observation identity, downstream numerator/value and provenance identities
were updated, and the original receipt/source_metric_sha256 stayed unchanged.
Full bundle validation accepted the forged count and changed prevalence .5 to 0.
This is a confirmed source-to-observation provenance integrity defect.

The fix must compare every normalized count with the exact authenticated source
metric's theme_counts entry (including absent-token zero), not just row bounds or
a new derived hash. Tests must also cover coherent downstream alterations,
wrong/absent tokens, replaced evidence, hash mismatches, orphan/duplicate evidence,
definition policy/version binding, quality claims and manifest trust boundaries.
Acceptance requires all offline tests and final-HEAD CI passing, plus exact
96-batch replay showing whether legitimate published numerical outputs change.

## Design decision recorded before repair

Use complete existing source metrics through an explicit external validation
input, authenticated against an independently supplied batch-to-metric SHA-256
map. Do not infer trusted pins from bundle receipts or evidence supplied with the
bundle. Importers obtain pins from a separately verified published run/Git revision
or fresh raw-byte/Phase 3 ledger verification. Definition history, implementation
identity and replay manifest roots likewise come from the caller's trusted context.

This reuses the existing flat SHA-256 source contract and 16,060,713-byte compressed
96-batch metric cache. A Merkle proof would require changing source commitments
and cannot prove a subset against the existing flat metric hash. A new token-count
projection hash alone would add a second assertion without proving its relationship
to that hash. Full evidence resolution adds no duplicate data to compact bundles
and no service or storage engine. Fail closed if evidence is unavailable; raw
archives can regenerate metrics and their pinned hashes can verify recovery.
Do not promise verification from compact receipts alone or permanent upstream raw
availability. Existing local research metrics are retained; ordinary future
retention policy is not redesigned in this targeted review.

Results and final verification will be appended after the repaired replay.
