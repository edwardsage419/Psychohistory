# Phase 3 lossless contracts v1.0.0

These are new contracts; no Phase 2 schema or evidence is reinterpreted.
Parser gkg_lossless 1.0.0 implements the preregistered GKG_PHASE_3_PROTOCOL.md.
JSON Schemas under schemas/gkg-lossless-*.v1.schema.json cover row disposition,
quarantine, batch ingestion, replay, and promotion assessment. Semantic meaning
changes require a new version. contracts.py validates the documented subset;
gkg_lossless.validate_batch and replay_gkg_lossless.validate_replay enforce
cross-field accounting, hashes, failure codes and status consistency.

## Row and quarantine

row_id is SHA-256 of canonical JSON containing schema_version, parser_version,
source, member, line, start, end and raw_sha256. Sorted keys, compact separators,
UTF-8 and no NaN define canonical encoding. Line numbers are one-based; byte
ranges are zero-based half-open within the expanded member, including LF/CRLF.
The full raw archive hash and source URL are in every row. No content is repaired.

Accepted rows carry the SHA-256 of their decoded 27-field vector and byte locator.
No opaque field is interpreted as an indicator or XML schema. Quarantine carries
base64 of the whole original row and explicit rejection codes; encoding spans
have row-relative start/end, exact hex bytes and one-based field numbers. Adding
row.start yields expanded-member offsets. Prefix timestamp is optional and never
required for a quarantine ID. The validated member contains the raw accepted
fields; future loss of it cannot be reversed using a field hash.

All duplicate record IDs within a batch are quarantined; no first-wins rule.
Cross-batch archive/member duplicates block corpus promotion/admission. Repeated
article URLs or syndicated articles are not asserted to be duplicate observations.

## Batch

source.acquisition refers to prior recorded retrieval, not new network activity.
archive_state, state, accepted_rows, quarantined_rows, physical_rows and
quarantine_fraction are independent explicit fields. Only clean_parse and
parse_with_quarantine with a complete verified member and positive accepted count
are locally eligible; rejected batches expose errors and release zero accepted
rows. An all-quarantined batch still retains its complete row ledger. A batch
rejected before complete row accounting uses an empty ledger and zero accounted
rows; this does not assert the physical member contains zero rows. Its nonempty
errors and rejected state prevent admission. Every disposition is reproduced from
verified member bytes before publishing an eligible result.

semantic_sha256 hashes the entire batch except itself. It includes full row
ledgers, quarantine bytes, stable versions and all counters/errors. No runtime
clocks appear in batch semantics. Compact study.json retains that hash plus the
full row ledger fingerprint and quarantine records; verifying that full batch
hash requires the local full batch JSON, not just the compact publication.

## Replay and assessment

Two independently executed output roots are compared slot-by-slot. Each full
batch fingerprint and semantic contract is revalidated before comparison, and
both observed raw hashes must equal the acquisition hash. Failures always carry
codes. Replay hashes exclude only created_at and the hash itself; manifest,
Phase 2 report and code fingerprints remain included. Assessment binds to the
exact batch and replay hashes and checks all gates. Its regression gate must be
supplied from recorded completed offline tests; the CLI does not auto-promote a
registry or production source. Invalid or contradictory evidence fails closed.

## Running offline and preserving outputs

From the repository root, Python 3.12+ standard library only:

```sh
python -B scripts/replay_gkg_lossless.py --corpus artifacts/gkg-study-96-v1 --output artifacts/gkg-phase3-run1
python -B scripts/replay_gkg_lossless.py --corpus artifacts/gkg-study-96-v1 --output artifacts/gkg-phase3-run2
python -B -m unittest discover -s scripts -p 'test_*.py' -v
```

Output must be a new directory disjoint from source inputs. Existing files and
hard links cannot be overwritten (exclusive creation). Input snapshots use one
read descriptor; ZIP and rows use the resulting immutable bytes. Mutations before
or during that read fail the pinned hash; mutations afterward cannot affect the
parsed snapshot. New reads detect a different revision. This is not an OS-level
sandbox against a hostile process changing output-directory permissions mid-run.

Compare with replay_gkg_lossless.compare(manifest, first_root, second_root).
Full ledgers and run.json remain local. code_hashes pins parser, runner, dependency
and schema bytes, including Git line endings. Preserve exact source snapshots or
checkout the recorded revision with matching bytes when reproducing later.
Run exits 0 for a completed corpus without rejected batches (including explicit
quarantine), 2 for rejected batches, 3 for study-level failures. It does not perform
network requests. Missing output files identify incomplete runs; they cannot be
certified or resumed by silently substituting new evidence.

Provenance receipts and storage profiles are descriptive v1 study artifacts.
Receipts bind source URL/hash/size, acquisition clocks and HTTP metadata to the
Phase 2 report SHA-256. Storage measures canonical JSONL payload bytes, separates
raw/quarantine/accepted-ledger/provenance categories and labels extrapolations.
See GKG_RETENTION_POLICY.md for permanent evidence and future raw policy limits.
