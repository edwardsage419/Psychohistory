# GKG experimental indicator study v1

Decision: **continue_semantic_validation**. Definitions are experimental literal
media-tag prevalence, not social severity, risk, event counts or a final ontology.
See ../../docs/PHASE_4_REPORT.md and ../../docs/INDICATOR_ARCHITECTURE.md.

* definitions.json: seven explicit IndicatorDefinition records, version 0.1.0.
* definition-history.json: append-only definition ID/version fingerprints.
* candidate-sources.json and source-documents.json: official examples and retained
  documentation snapshot metadata, including failed acquisition attempts.
* results/inventory.json.gz: complete 9,927-token inventory; UTF-8 JSON compressed
  losslessly with gzip mtime=0. About 2.42 MB replaces 21.75 MB expanded JSON.
* results/*.jsonl: separate normalized observations, indicator values, quality,
  provenance and batch receipts. No dashboard data format is used.
* results/semantic-manifest.json: stable output and implementation/input hashes.
* results/replay.json: two distinct, independently ordered full-corpus runs.
* results/tests.json and protected-files.json: local verification evidence.

Use Python's gzip.open(path, 'rt', encoding='utf-8') and json.load to inspect the
full inventory. Counts and per-batch fractions are aligned to its batch_order.
Missing tokens are literal absence only; co-occurrence covers the declared panel.
The full per-row diagnostic cache, original ZIPs, Phase 3 ledgers, documentation
snapshots and exact implementation snapshot remain local under artifacts/ and are
not committed. Their paths/hashes and retention limitations are documented.

Original run directories contain exactly the semantic file set plus execution
metadata. This publication directory adds review evidence and should not be passed
to the strict original-run compare function. Reproduce into two new local output
roots; never overwrite or delete the research corpus. Normal CI stays offline.
