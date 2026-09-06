# Phase 3 self-review fixes

Starting commit: d16acc4 on codex/project-reset-architecture, clean working tree.
The original Phase 2/3 evidence, source snapshots and raw corpus remain immutable.

## Confirmed defects

1. compare accepted the same directory twice, including path aliases, and did not
   reject hard-linked per-batch ledgers. It now rejects these with
   replay_not_independent. Distinct files alone cannot prove independent execution
   against malicious fabricated logs; this check prevents accidental self-comparison.
2. validate_batch accepted a supplied member payload without recomputing its whole
   hash/length against the recorded member identity. It now rejects any mismatch
   before validating rows, even if a caller recomputes the outer semantic hash.
3. Standalone quarantine validation checked base64 bytes and row hash but not the
   corresponding disposition, invalid spans or failure details. These are now
   recomputed from the embedded bytes. Duplicate-ID membership still requires the
   complete member; a single quarantined row cannot prove that another row exists.
4. assess caught a malformed replay contract and then dereferenced missing fields,
   raising KeyError instead of issuing a failed assessment. Input shapes are now
   checked first, and invalid shapes produce continue_validation, false gates and
   a machine-readable error. The invalid replay fingerprint identifies rejected
   input; it is not represented as a verified replay.

Five new regression tests reproduced six failing assertions and one uncaught
exception before the fixes. After the fixes the complete local suite runs 116
tests: 115 passed, zero failures/errors and one Windows symlink-permission skip.
The Linux CI result is checked after pushing; no local skip is labeled passed.

## Compatibility and preservation

These changes enforce existing documented evidence relationships; they do not
change row acceptance policy or serialized schema meaning. Valid v1 evidence
remains valid. Code-byte fingerprints change and intentionally prevent the current
runner from masquerading as the original evaluator. Original run3/run4 comparison
must use the exact scripts/schemas under
artifacts/gkg-phase3-final/source-snapshot (put its scripts directory first on
Python's import path), or matching original checkout bytes. Do not edit old
run.json identities to bypass that protection.

No paid infrastructure, data deletion, sampling/field reduction, production
migration, or merge to main is part of this repair.

## Original corpus verification

All 96 original archives were parsed again with the corrected evaluator and
compared to the complete stored Phase 3 ledgers. All 96 results are exactly equal,
including row IDs, raw hashes, quarantine details and semantic hashes. The stricter
checks also accept the original replay evidence; recommendation remains
promote_to_ingestion_candidate in its original limited scope. See the separate
[machine-readable review evidence](evidence/gkg-phase3-self-review.json).
Original publications were not overwritten or relabeled as new runs.
