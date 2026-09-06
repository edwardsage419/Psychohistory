# Psychohistory

An evidence system for observing social conditions and eventually evaluating
probabilistic forecasts. The existing V0.2 dashboard is a preserved prototype.

## Current work: architecture reset and data foundation

Read [AGENTS.md](AGENTS.md) and [docs/ROADMAP.md](docs/ROADMAP.md) first.
Architecture documents supersede the old seven-topic migration plan. GDELT DOC
API ingestion is a legacy path with recorded HTTP 429 failures; no further retry
tuning is planned. GKG is a candidate, **not a production source**.

Issue 2 deliverables:

* [Complete baseline repository audit](docs/REPOSITORY_AUDIT.md).
* [Versioned report, source registry and observation contracts](docs/SCHEMAS.md).
* [Empirical GKG evaluation and next phase](docs/GKG_EVALUATION.md).
* [Final implementation and validation report](docs/ISSUE_2_REPORT.md).

Python 3.12+, standard library only:

```sh
python -B -m unittest discover -s scripts -p 'test_*.py' -v
python -B scripts/validate_gkg.py --input path/to/batch.zip --output report.json
```

Network acquisition is explicitly integration scoped:

```sh
python -B scripts/validate_gkg.py --integration
python -B scripts/validate_gkg.py --integration --url https://data.gdeltproject.org/gdeltv2/20260905221500.gkg.csv.zip
```

Reports default to `scripts/gkg_validation_report.json`, an ignored run artifact.
The read-only validation workflow uploads reports even on failure. Offline PR CI
makes no source requests. The old `--date` option never selected historical data
and has been removed. No GKG theme mappings are production-approved.

## Preserved prototype

`index.html`, `style.css` and `app.js` display `data/gdelt.json`. Monitoring Topics
contains legacy DOC API data; trends, forecasts, history and model scores are
explicitly mock data. Coverage percentages describe media attention, not actual
societal risk or severity. Failed topic states preserve the last available value.

The legacy updater and its scheduled workflow are retained unchanged until a
separate production retirement review. Its baseline stores failed run metadata
and exits 0 even when all topics fail; it must not be reused as the new ingestion
foundation. The historical implementation narrative remains in Git history at
`cb2058ce20026e7617b6f5ac733cebdff90d9b20`.

No dashboard data-contract migration, forecasting, redesign or paid infrastructure
is included in Issue 2. Changes remain on `codex/project-reset-architecture` for
review and must not be merged to main without separate approval.

## Phase 2: GKG continuity study

The bounded 96-batch study is complete: 96 HTTPS acquisitions and integrity checks
passed, 92 strict parses passed, and all 96 stored inputs reproduced exactly.
Four batches contain invalid UTF-8; recommendation remains **continue_validation**.
See [Phase 2 report](docs/PHASE_2_REPORT.md), [preregistered protocol](docs/GKG_STUDY_PROTOCOL.md)
and [machine-readable results](studies/gkg-continuity-v1/results/study.json).

```sh
python -B scripts/study_gkg.py --integration --root artifacts/gkg-study-96-v1
python -B artifacts/gkg-study-96-v1/source-code/study_gkg.py --manifest studies/gkg-continuity-v1/manifest.json --replay --root artifacts/gkg-study-96-v1
```

Raw inputs are preserved locally under the ignored study directory. A fresh clone
includes compact evidence, not 494 MB of raw ZIPs; follow the [retention/replay
instructions](docs/GKG_STUDY_SCHEMA.md) to use the retained dataset. No production
migration or theme mapping is authorized by these results.

## Phase 3: lossless parsing and quarantine

The exact 96-batch corpus now has 118,415 accepted rows and five losslessly
quarantined rows. Both independent final replays match all 96 batches; 111 tests
pass on Ubuntu CI. Recommendation: **promote_to_ingestion_candidate**, limited
to raw acquisition/parsing/provenance. This does not validate theme indicators
or activate production ingestion. See [Phase 3 report](docs/PHASE_3_REPORT.md),
[contracts](docs/GKG_LOSSLESS_CONTRACTS.md), and [near-zero-cost retention design](docs/GKG_RETENTION_POLICY.md).

Keep the original 96 archives intact. Permanent quarantine embeds exact raw bytes;
future raw retention policy cannot assume that a hash or URL reconstructs data.
No paid infrastructure or destructive retention job has been introduced.
