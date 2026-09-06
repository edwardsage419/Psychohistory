# Targeted post-Phase-4 integrity evidence

Start: b3627a0. Recommendation remains continue_semantic_validation. No next phase.
See ../../../docs/PHASE_4_INTEGRITY_REVIEW.md for the reproduced attack, exact
external-source authentication contract, adjacent fixes, tests and preservation.

baseline-trust.json comes from the separately identified b3627a0 Git objects;
it is not a self-assertion copied from a candidate bundle. Original source metrics
resolve from retained local gzip caches or fresh authenticated raw/ledger replay.
Missing evidence fails closed. No source metric is embedded redundantly in bundles.

replay-comparison.json commits the independently captured roots of two completed
verified new runs and their full numerical comparison with original Git artifacts.
Local full replay directories remain under artifacts/gkg-phase4-integrity/replay-a
and replay-b. Source archives and old results have not been overwritten. verify.py
requires an independently trusted full-manifest root, never one derived from a
possibly modified candidate being audited. Example after restoring the pinned runs:

```text
python -B studies/gkg-indicators-v1/integrity-review/verify.py artifacts/gkg-phase4-integrity/replay-a artifacts/gkg-phase4-integrity/replay-b --trusted-manifest-sha256 a6c8c9c8fd2615101bdafc0492e0f131d380f3226bb94e8727e1c02f3bc2fd01 --output artifacts/new-integrity-comparison.json
```

Each output path must be new. Retain the trust root independently of candidate
artifacts; hashes do not authenticate their own origin. CI remains fully offline.
Baseline CI evidence is explicitly commit-specific; the final response identifies
the repaired HEAD's separate CI result and exact SHA.
