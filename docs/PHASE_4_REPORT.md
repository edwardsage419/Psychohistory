# Phase 4 report: indicator foundation and GKG semantic validation

**Decision: `continue_semantic_validation`.** The measurement foundation is implemented and reproducible for literal media-tag prevalence. It is not yet sufficiently validated to begin cross-year historical indicator series interpreted as social conditions. Phase 3 remains accepted as `promote_to_ingestion_candidate` for acquisition, parsing, quarantine and provenance only. No forecast or production indicator is authorized.

## Baseline, work and verification

- Repository: `edwardsage419/Psychohistory`; branch `codex/project-reset-architecture`. Local checkout: `D:/GPT/Psychohistory-issue2`.
- Starting HEAD: `09586cdeed612ed878c9b340e7cd23622ec4eddb`, clean. AGENTS, all docs, previous reports and source/observation/ingestion contracts were read before implementation. Full-read file hashes are retained locally in `artifacts/gkg-phase4/context-read.json`.
- `19e882d`: preregistered measurement and candidate selection protocol.
- `e0710fa`: definitions, schemas, source metrics, aggregation, study and initial tests.
- `210c0db`: adversarial review fixes and replay checks.
- `43cf624`: complete inventory, normalized/indicator outputs, replay evidence, architecture, decisions and report.
- `033fd34`: scoped LF checkout rules preserve published evidence hashes.
- The final documentation-only verification commit records CI evidence; its own identifier is available from Git history, avoiding a self-referential hash.

Baseline command: `python -B -m unittest discover -s scripts -p "test_*.py"`. Baseline: 116 tests, 115 passed, one Windows symlink-permission skip, no failures/errors. Initial implementation: 36 new tests passed; full suite 152 tests, 151 passed, one skip. Dedicated adversarial regressions then produced **7 confirmed failures** on the initial implementation. After fixes: **163 tests, 162 passed, one Windows symlink-permission skip, no failures/errors**. Ubuntu CI at `033fd34` passed **all 163 tests, zero skips/failures/errors**, in 1.777 seconds, including the symlink test. [Verified run](https://github.com/edwardsage419/Psychohistory/actions/runs/34001418505); [machine evidence](../studies/gkg-indicators-v1/results/ci.json).

The 47 Phase 4 tests cover every definition field, invalid/unsupported policies, append-only initial history, generic non-GKG definitions, exact-token counting, empty and zero denominators, quarantine exclusion, weighted aggregation, entirely missing windows, midnight boundaries, all six historical years, duplicate batches/archives, identifier repetition, provenance, identity/version changes, ordering, malformed metrics, sidecar tampering and replay tampering. A 96-batch synthetic end-to-end fixture runs twice offline and records exactly one machine-readable failure after one temporary fixture archive is corrupted. No retained research archive is modified by tests.

Adversarial details: [machine-readable self-review](evidence/gkg-phase4-self-review.json). The seven repaired gaps were contradictory nonempty-row accounting; acquisition chronology; parser/version contradictions; URL/batch contradictions; indicator numerator/input mismatch; removable mandatory quality warnings; and source-quality count contradictions. Each regression failed before its fix. Review also checked literal semantics, retrospective rules and the absence of prototype-category inputs. This is evidence of specific checks, not proof that no other bugs exist.

## Exact corpus and inventory

No new GKG batch was acquired. The original manifest is unchanged: [96-batch manifest](../studies/gkg-continuity-v1/manifest.json), canonical SHA-256 `443f60269a89251655b0636799988e15034b55a8ceb58ffea57c8d236bf2ef15`. Every range below includes both endpoints, with one batch every 15 minutes, UTC.

| Cohort | Batch interval | Batches | Accepted rows | Distinct tokens |
|---|---|---:|---:|---:|
| historical_2015 | 2015-03-02 00:00–00:45 | 4 | 6,662 | 3,016 |
| historical_2016 | 2016-09-05 06:00–06:45 | 4 | 7,748 | 4,219 |
| historical_2020 | 2020-09-05 12:00–12:45 | 4 | 3,494 | 3,280 |
| historical_2023 | 2023-09-05 18:00–18:45 | 4 | 9,919 | 4,434 |
| historical_2025 | 2025-09-05 00:00–00:45 | 4 | 6,084 | 3,621 |
| historical_2026 | 2026-08-05 12:00–12:45 | 4 | 5,335 | 4,076 |
| recent | 2026-09-04 00:00–17:45 | 72 | 79,173 | 8,460 |

All **96 archive/hash/member/ledger checks passed in both final runs**, with zero failed batches or skipped failures. The source has 118,420 physical rows: **118,415 accepted and five quarantined**. There are **9,927 distinct literal tokens**, **12,729 empty-theme rows (10.7495%)**, and **105,686 nonempty-theme rows**. Within-row deduplication removes 141 repeated token occurrences from presence counts. The parser ignores 105,686 empty delimiter fragments, preserving all other literal strings, including case and whitespace. It does not use enhanced-theme offsets as V1 tokens.

The full [inventory](../studies/gkg-indicators-v1/results/inventory.json.gz) contains a fixed batch-order vector, per-token counts and prevalence for all 96 slots, first/last sampled occurrence, cohort denominators, years present, lexical prefix, documentation/semantic status and top co-occurrences against the bounded seven-token panel. Per-batch empty-theme denominators are included. Co-occurrence is explicitly panel-limited; it is not an exhaustive all-pairs graph. All accepted rows here have a nonempty document identifier, so its stated diagnostic eligibility excludes no accepted sample rows.

Largest lexical families by distinct literal token: TAX 7,662; WB 1,295; ECON 217; NATURAL 154; unprefixed 106. These are spelling groups, not a Psychohistory ontology. Only seven tokens are registered; the other **9,920 remain source metrics with unresolved semantics**.

## Documentation and interpretation boundaries

The [GKG 2.1 codebook](https://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf) defines V1THEMES as document-level theme labels separated by semicolons. Enhanced themes include mention offsets. GKG document rows are not unique real-world events; coverage by different outlets can produce different rows about the same event. Location fields concern extracted mentions and have geocoding limitations. Phase 4 measures column 8 exact row presence and uses the batch timestamp, without inferring event or publication time.

The [GDELT geographic search announcement](https://blog.gdeltproject.org/announcing-gdelt-geographic-news-search/) provides topical use examples for PROTEST, ECON_TAXATION, NATURAL_DISASTER_LANDSLIDE and AVIATION_INCIDENT. Its protest example includes prospective discussion, which supports the media-content boundary. These examples do not establish classifier precision, severity or temporal invariance. The [GeoJSON announcement](https://blog.gdeltproject.org/announcing-our-first-api-gkg-geojson/) explicitly associates FOOD_SECURITY with food-security coverage. No API query or geographic mapping from those services is used in our calculation.

The [World Bank taxonomy announcement](https://blog.gdeltproject.org/world-bank-group-topical-taxonomy-now-in-gkg/) explicitly names WB_345_SOVEREIGN_WEALTH_FUNDS and describes numeric topic IDs with labels. The [provider sample queries](https://blog.gdeltproject.org/google-bigquery-gkg-2-0-sample-queries/) discuss unemployment and list WB_2747_UNEMPLOYMENT; they also distinguish per-document presence from repeated theme mentions. This supports a limited topical label, not an unemployment-rate measure.

The [November 2021 lookup announcement](https://blog.gdeltproject.org/new-november-2021-gkg-2-0-themes-lookup/) describes an empirical theme histogram. A lookup histogram is not a versioned semantic dictionary. We did not infer stable classification rules or historical detection coverage from it. No paid BigQuery query was executed.

Five bounded official HTML snapshots were successfully retained locally, with URL, acquisition time, byte length and SHA-256 in [source-documents.json](../studies/gkg-indicators-v1/source-documents.json). Five initial sandbox-network failures are also recorded; the permitted second attempts succeeded. The pre-existing codebook PDF snapshot and hash remain intact. Full article content is not redistributed in Git; compact registry interpretations and source references are retained. The exact lexical match dictionaries, precision/recall and historical extractor versions remain unknown.

## Selection and exact experimental definitions

[The protocol](PHASE_4_PROTOCOL.md) was committed before selection. Gates: documented provider example, at least 12 sampled batches, at least three sampled years, and a diverse small panel. These are exploratory usability screens, not scientific acceptance thresholds. Candidate evaluation separately records frequency, sparsity, zero cohorts, coverage, denominator sensitivity, volume effects, repeated identifiers, media bias, geography, potential cross-source suitability and unvalidated definition stability.

All seven definitions are **experimental, version 0.1.0**. Indicator ID is `gkg.media_prevalence.` followed by the exact token lowercased. The transformation still matches the original uppercase token exactly; lowercasing applies only to the identifier name. Full definitions and pinned history: [definitions.json](../studies/gkg-indicators-v1/definitions.json), [definition-history.json](../studies/gkg-indicators-v1/definition-history.json).

| Exact token | Matching rows | Present batches / 96 | Years present | Pooled prevalence |
|---|---:|---:|---:|---:|
| `PROTEST` | 6,168 | 96 | 6 | 5.20880% |
| `ECON_TAXATION` | 3,518 | 96 | 6 | 2.97091% |
| `FOOD_SECURITY` | 924 | 96 | 6 | 0.78031% |
| `WB_345_SOVEREIGN_WEALTH_FUNDS` | 80 | 46 | 5 | 0.06756% |
| `WB_2747_UNEMPLOYMENT` | 857 | 92 | 5 | 0.72373% |
| `NATURAL_DISASTER_LANDSLIDE` | 181 | 69 | 6 | 0.15285% |
| `AVIATION_INCIDENT` | 170 | 74 | 6 | 0.14356% |

For each token **T** and requested UTC window **W**: numerator is the sum of accepted rows whose exact V1THEMES set contains T; denominator is every accepted row in W, including empty-theme rows. Each row contributes at most once to a token. Quarantined rows contribute to neither count. The result is numerator/denominator in fraction units, provided every expected slot exists and the denominator is positive; otherwise it is null. No aliases, semantic expansion, repeated-document removal, smoothing, lag correction or interpolation. Scope is sampled document rows; geography and entity fields are null. All present values are suspect because the definition and historical interpretation remain experimental.

The topical interpretations are respectively protest-related, taxation-related, food-security-related, sovereign-wealth-fund-related, unemployment-related, landslide-related and aviation-incident-related media tagging. None is an event count, severity, risk, public opinion, economic magnitude or conflict intensity. Neither the seven old UI categories nor their mappings are inputs.

[Deferred candidates](../studies/gkg-indicators-v1/results/deferred-candidates.json) include ELECTION, ARMEDCONFLICT and WB_1406_DISEASES: additional high-volume labels are not needed to establish this diverse bounded panel and lack the required classifier/historical validation. All unregistered tokens remain available for future source research. No token is scientifically rejected merely because it was not selected. Real-world severity and event interpretations are rejected for this phase; geographic indicators and independent outcome comparisons are deferred.

## Denominators, time and quality

Primary all-accepted prevalence answers: what fraction of accepted source rows contains this exact tag? The nonempty-theme diagnostic instead conditions on rows receiving any theme. Globally its denominator is 105,686 rather than 118,415, making pooled nonzero values 12.0442% larger relative to the primary denominator. This is selection sensitivity, not improved accuracy or a smoother-series criterion. Per-token maximum batch differences appear below.

| Token | Max alternative-minus-primary difference, percentage points | Count–volume Pearson r | Prevalence–volume Pearson r |
|---|---:|---:|---:|
| `PROTEST` | 1.1351 | 0.8694 | 0.2970 |
| `ECON_TAXATION` | 0.6741 | 0.7620 | 0.0553 |
| `FOOD_SECURITY` | 0.2333 | 0.6141 | 0.0001 |
| `WB_345_SOVEREIGN_WEALTH_FUNDS` | 0.0614 | 0.1104 | -0.1246 |
| `WB_2747_UNEMPLOYMENT` | 0.3896 | 0.5002 | 0.1482 |
| `NATURAL_DISASTER_LANDSLIDE` | 0.0789 | 0.0179 | -0.1286 |
| `AVIATION_INCIDENT` | 0.0938 | 0.2717 | -0.1349 |

For most panel tokens the magnitude of correlation with sample batch volume falls after normalization. This is not universal: landslide prevalence has greater absolute correlation than its raw count. Normalization removes the arithmetic scale of total rows but not outlet mix, language selection, taxonomy drift or news cycles. Counts and prevalence also reverse some batch rankings, recorded explicitly in candidate evaluation. These are descriptive convenience-sample comparisons; there are no causal, significance or predictive claims.

Hourly aggregation is the primary research layer. Daily aggregation is a coverage stress test. Configuration permits integer multiples of 15 minutes that divide 1,440 minutes, including windows above 15 minutes; no weekly or rolling window is silently approximated. UTC windows are half-open, with starts aligned from midnight. Ratios use summed counts, not an average of batch percentages. Expected slots derive from the requested window independently of arrivals. Explicit requested starts can represent wholly absent windows. Default output covers only the seven sampled dates, not an invented continuous 2015–2026 history.

The sample contains 24 complete hours: **168 non-null hourly values** for seven definitions. Its seven dates are all partial: recent coverage is 72/96 slots (75%); each historical date is 4/96 (4.1667%). Consequently **49 daily values are null**. Sampled counts and conditional prevalence diagnostics remain visible and explicitly partial. A missing slot means unobserved in this bounded sample, not proof of source unavailability.

Each value has observed/expected/missing batch lists, counts, coverage, accepted/quarantined rows, empty-theme rows and repetition diagnostics in its quality sidecar. Complete windows with quarantine, empty themes or repeated identifiers carry warnings. Zero denominator and incomplete window always yield missing status; all other indicator values remain suspect due to experimental semantics. Absent literal tokens can be numeric zero in complete windows, accompanied by historical-semantics warnings.

## Historical findings, repetition and geography

All accepted source rows retain the Phase 3 27-field schema and verified batch timestamps across all cohorts. This establishes structural compatibility for the selected field, not stable meaning. WB_345_SOVEREIGN_WEALTH_FUNDS and WB_2747_UNEMPLOYMENT are absent from all four 2015 batches. The taxonomy announcement is dated 2015-03-02, also the earliest sample date; this raises an introduction-timing question but does not establish the precise deployment time or explain the absence.

Observed cohort prevalence varies materially. PROTEST ranges from about 4.34% to 9.13%; FOOD_SECURITY from 0.40% to 0.99%. Among nonzero cohorts, the sovereign-wealth token ranges from about 0.0101% to 0.1420%. Such extremes may reflect sparse counts as well as reporting and classification changes. Lexical cohort Jaccard overlap ranges from 0.2997 to 0.5563; the 2015–2016 overlap is 0.3911. Different sample sizes confound those comparisons. These observations flag possible structural/taxonomy changes but cannot locate a break or validate stable concepts across years. Full per-token cohort distributions remain in machine evidence.

DocumentIdentifier (column 5) is distinct from the GKG record ID (column 1) used by ingestion. Exact DocumentIdentifier diagnostics find 118,412 distinct identifiers among 118,415 accepted rows: one identifier appears four times, giving three excess rows; no identifier is empty. The primary calculation retains them. None of these extra occurrences contributes a selected token numerator, so unique-identifier diagnostic prevalences differ only slightly through the denominator. This does not establish low repeated-event or syndicated-reporting risk: different URLs and outlets can repeat the same story, and URL normalization, article clustering and event deduplication were deliberately not introduced.

There are 8,781 literal source names; the largest, iheart.com, contributes 6,949 rows. This is an observed concentration diagnostic, not an outlet-quality or content-type judgment. Only the English filename family was sampled. Publication volume, provider selection, article length, outlet mix, translation coverage and extraction rules can bias media prevalence. The source collection cannot represent all news or all people.

Source outlet geography, mentioned place, actual event location and subject geography are different attributes. No country is inferred from outlet names or tag/location co-occurrence. The observation geography remains null with explicit collection-only scope; even “global” means a provider collection, not a representative geographic measurement.

## Architecture, identity and reproduction

The four layers are: immutable source archive and Phase 3 dispositions; directly measured source counts; normalized observation v1; explicitly registered indicator values with separate interpretation. The source metric inventory exists for every token; only the small registry emits indicator values. The source-independent IndicatorDefinition schema supports other datasets and transformations without GKG enums. The GKG computation adapter rejects methods and policies it cannot implement. No other source is integrated.

The existing observation v1 contract is unchanged. This run emits **672 normalized source-count observations**, **217 indicator-value records** embedding observation v1, **889 quality records**, **217 indicator provenance records**, and **96 batch receipts**. Their files are separate JSONL streams. Raw count observations use original archive hashes. Aggregate observation snapshot hashes identify the ordered receipt-hash manifest, explicitly not a fictitious single ZIP.

Provenance chains bind source URL/identity, batch, archive size/hash, acquisition times and HTTP metadata, member hash, row-ledger and full-ledger semantic hashes, parser/contract versions, transformation version, implementation file hashes, definition version/hash and window inputs. Source extraction validates the published Phase 3 ledger hash and reclassifies all rows against verified bytes before accepting any metrics. No alternative decoding or quarantine repair is performed.

Changing a definition under an existing ID/version fails its history pin; initial release pins also have an append-only regression guard. New versions require new fingerprints with previous identities retained. This is a reviewed Git version-history rule, not a tamper-proof ledger against an actor able to rewrite code and every trust anchor. Retrospective outputs explicitly apply the current experimental measurement rule; they do not claim it was deployed or semantically validated in historical years.

Two independent final runs read every original ZIP: the first uses Phase 3 run3 ledgers in ascending order, the second run4 ledgers in descending order. **All 14 stable output files and input/definition/implementation pins are identical.** Semantic SHA-256: `2f381e429bafa6e6c59b9739b32bd014e3b80a014005939d65d33ce6f427b5fd`. Measured durations: 83.136s and 83.094s. Runtime clocks and duration appear only in execution evidence. Original acquisition times remain pinned provenance. Observation identity also follows the existing contract exclusion of retrieved_at.

[Replay evidence](../studies/gkg-indicators-v1/results/replay.json) verifies file hashes, distinct run evidence and semantic manifests, rejecting alias/self-comparison and mutated files. The exact implementation bytes and registry inputs are also retained under `artifacts/gkg-phase4/source-snapshot/`; byte-level code pins include the current checkout line endings. Cross-platform replays must restore those pins or declare a new implementation fingerprint. Scoped `.gitattributes` rules preserve canonical LF bytes for published Phase 4 JSON/JSONL evidence on Windows as well as Linux. The published result directory adds report/verification evidence; replay validation itself applies to the two original local run directories, whose exact artifact sets are preserved.

## Measured storage and cost

| Artifact class | Measured bytes | Scope |
|---|---:|---|
| Raw ZIP archives | 494,483,985 | Original 96, retained unchanged |
| Existing exact quarantine evidence | 74,338 | Five rows plus associated metadata; already retained |
| Normalized observations | 471,888 | 672 records |
| Indicator values | 285,285 | 168 hourly + 49 partial daily |
| Quality metadata | 497,621 | Source and indicator quality |
| Indicator provenance | 419,549 | 217 records |
| Batch receipts | 168,274 | 96 records |
| Definition and version-history files | 20,025 | Seven experimental definitions |
| Full inventory, uncompressed / gzip | 21,748,076 / 2,420,658 | All 9,927 tokens and 96-slot distributions |
| Local full source metrics, gzip | 16,060,713 | Includes hashed identifier/row-token diagnostics; not committed |

The inventoried compact result files total 4,351,076 bytes before storage/manifest/replay/test/report evidence is added. The 2.42 MB lossless inventory is justified in Git because it permits full-token review without committing 494 MB of source ZIPs or 16 MB of local diagnostic caches. JSONL and standard-library gzip suffice; no database or always-on process is justified by these sizes.

**Extrapolations, not measured annual volumes:** the full 96-batch mixed-cohort mean at 96 slots/day implies raw ZIPs of 494.48 MB/day, 14.83 GB/30 days and 180.49 GB/365 days. This differs from Phase 2’s recent-only estimate because the basis includes all historical batches. A repeat of the measured seven-indicator record sizes, retaining source observations, source quality, batch receipts and both hourly and daily value/quality/provenance layers, totals approximately **526.95 MB/year** (about 5.27 GB over ten years before additional evidence and vocabulary growth). Normalized observations alone extrapolate to 172.24 MB/year; source quality 57.51 MB/year; batch receipts 61.42 MB/year.

Hourly values/quality/provenance extrapolate to 80.45/52.22/78.85 MB/year; daily equivalents to 3.38/10.27/10.61 MB/year. Daily records were all partial, so their missing-list representation is not a measured complete-day profile. Local full diagnostic caches extrapolate separately to 5.86 GB/year. Inventory growth, future theme count, replication, filesystem overhead and changing compression ratios are not modeled. Exact formulas, daily/monthly/yearly estimates and measured byte counts are in [storage.json](../studies/gkg-indicators-v1/results/storage.json).

Keep compact irreplaceable quarantine bytes, source/definition/version receipts and study decisions permanently; normally retain derived observations and quality; ordinary public raw archives may only follow a future configurable retention policy. Hashes can verify recovered bytes but cannot recreate missing bytes or guarantee upstream retention. All 96 research archives and Phase 3 ledgers remain intact. No deletion, reduced fields, reduced acquisition frequency or paid dependency was introduced. Git is appropriate for compact review evidence and code; future accumulating histories can remain local files. Free execution/storage still needs explicit backup and capacity planning; no unmeasured perpetual-free capacity is assumed.

## Protected scope, unresolved questions and next issue

[Protected-file evidence](../studies/gkg-indicators-v1/results/protected-files.json) confirms identical baseline/current Git blobs for app.js, index.html, style.css, data/gdelt.json, scripts/update_gdelt.py and .github/workflows/update-gdelt.yml. Windows working copies use CRLF and match those blobs after the documented checkout line-ending conversion. No source data was line-ending-normalized for validation. No production workflow, dashboard behavior, legacy updater, ingestion contract or existing research evidence was changed. No merge to main.

Unresolved: historic dictionary/extractor version boundaries; per-token precision and recall; whether empty themes reflect content or detection coverage; representativeness across outlets/languages; syndicated and repeated-story bias; event/publication lag; geographic attribution; sustained full-day continuity; and future archive retention. Independent external validation was explicitly deferred: zero additional series acquired, with no defensible paired complete daily/geographic comparison in this sparse corpus.

**Next recommended issue: bounded human semantic audit and historical extractor evidence for three representative tokens** (PROTEST, FOOD_SECURITY, WB_2747_UNEMPLOYMENT). Preregister sampling and annotation rules before inspecting article meaning; use at most 120 retained-corpus document references across all six years, with positive and negative rows, exact provenance, independently reviewed labels where feasible, unavailable documents explicitly recorded, and no repaired or fabricated text. Distinguish mention/topic detection from actual events. Investigate provider taxonomy/version evidence and stratify missing-token periods. Do not compute recall from positive-only samples or treat unavailable article text as a negative. Report whether token-level interpretation can be validated; any additional continuity acquisition needs its own bounded sampling plan. No forecast, final ontology, geography inference or production activation.
