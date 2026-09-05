# Phase 3 protocol: lossless parsing and quarantine v1

Preregistered before the Phase 3 corpus evaluation. Start: eabba6a on
codex/project-reset-architecture, clean tree, 75 offline tests passed. eabba6a
was pushed successfully before this phase. Phase 2 results are immutable history.

## Scope and evidence

Use exactly studies/gkg-continuity-v1/manifest.json and its 96 retained ZIPs.
No download, sample replacement, theme interpretation, normalization deployment,
or production migration. Phase 3 is an offline candidate evaluation only.
Provider documentation informs facts; strict UTF-8 acceptance is an engineering
policy unless a global provider guarantee is located. Unknown encodings remain
unknown and their rows remain quarantined, even if another codec decodes them.

## Byte and row policy

Read a bounded archive once into immutable bytes and verify its SHA-256 against
Phase 2 evidence. ZIP parsing, CRC, member hash, rows and diagnostics all use
those bytes. Read and verify the entire bounded member before releasing any row.
One correctly named unencrypted member is required. Archive mismatch, CRC failure,
unsupported archive, empty member, whole-member resource exhaustion, source
identity conflict and unexpected exceptions reject the batch with explicit codes.
No provisional accepted rows may escape a subsequently rejected archive.

Physical rows are LF-delimited byte ranges, including their terminators. CRLF is
recognized without altering retained bytes; a nonempty unterminated final row is
quarantined_schema (possible truncation). Bounds: 64 MiB ZIP, 512 MiB expanded,
8 MiB row, 100,000 physical rows per batch. Row resource quarantine is possible
only after the entire archive is verified and the full row is locatable. Exceeding
the batch row bound rejects the batch, rather than publishing a partial ledger.

Each row carries source URL/ID, expected and observed archive hash, member,
line number, zero-based half-open byte range, row SHA-256, deterministic ID,
parser/contract versions, disposition, and deterministic reason details.
Quarantine includes exact base64 bytes. Accepted rows retain byte locators and
hashes plus a hash of the strictly decoded 27-field vector; no theme mapping.
All occurrences of duplicate nonempty record IDs are quarantined, avoiding
order-dependent first-wins acceptance. Timestamp 0, invalid dates or dates not
matching the scheduled batch are quarantined_timestamp. The row classifier uses
precedence resource, encoding, schema, timestamp, other (duplicate identity).
Encoding diagnostics enumerate all invalid byte spans, without codec guessing.

## Partial acceptance and batch states

Acquisition is inherited evidence, not a new network success. Archive verification
is independent. Batch states are clean_parse, parse_with_quarantine, rejected.
Only fully verified, completely accounted nonempty batches with accepted rows
are locally eligible. A quarantine does not repair a record or certify its other
fields. Valid row acceptance means syntactic/provenance safety only, not semantic
validity. Downstream use must join batch quality, counts, quarantine fraction and
corpus duplicate checks; a generic success Boolean is insufficient. A rejected
batch releases zero accepted rows. Cross-batch duplicate archive/member hashes
block corpus admission until resolved; never deduplicate away sample slots.

## Promotion gates fixed before evaluation

Every gate below must pass for promote_to_ingestion_candidate in this limited
scope. Otherwise continue_validation, unless independently established fundamental
source/rights limitations justify reject_as_primary_source. No percentage cutoff
is selected to fit five known anomalies. Quarantine percentage is always reported;
any batch with zero accepted rows fails usability. These are engineering checks,
not a reliability SLA or proof of representative coverage.

1. Exact sample and identity: 96 ordered distinct manifest slots, all Phase 2
   acquisition records successful, exact URL/hash/size references. Rationale: no
   substituted evidence or nominal transport success overriding changed bytes.
2. Archive integrity: all 96 complete CRC/member/hash checks pass; no duplicate
   archive or expanded-member hashes. Rationale: trustworthy independent units.
3. Complete row disposition: every physical byte belongs to exactly one row;
   accepted + quarantined = total; nonempty batches; zero unaccounted rows/bytes.
4. Provenance and quarantine: recomputed IDs, raw hashes, byte locators, base64
   quarantine round trips and accepted field hashes validate for every row.
5. Reproducibility: two independent full offline runs agree on source hashes and
   recomputed semantic hashes for every batch and ledger. Contradictory flags,
   absent failure codes or inconsistent success records fail, never override facts.
6. Mutation protection: offline replacement, truncation, hard-link/symlink where
   supported, input/output collision and revision mismatch regressions pass.
7. Exception and quality transparency: zero unexpected exceptions in the corpus;
   all failure categories recorded; batch states/counts are internally consistent;
   no rejected batch or zero-accepted batch is eligible for promotion.
8. Encoding ambiguity containment: no guessed/replacement decoding; all undecodable
   rows quarantined with exact bytes. Unknown provider encoding is not resolved by
   a successful alternative codec. Ambiguity in accepted data blocks promotion;
   quarantined-only ambiguity remains a documented limitation of the candidate.

## Deliverables and acceptance

Versioned row, quarantine, batch, replay and assessment contracts; substantial
offline regression coverage; local full row ledgers for both runs; committed
compact batch evidence and all quarantine records; source-code hashes; final
report with unchanged-production checks, push/CI status and unresolved questions.
Original 96 raw archives and Phase 2 outputs must not be overwritten. Use a new,
exclusive output directory outside the input corpus; a second run uses another
new directory. Local reports/ledgers need the same backup policy as raw evidence.
