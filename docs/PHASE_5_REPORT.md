# Phase 5 report: cross-year semantic audit

**Recommendation: `continue_semantic_validation` for each token and Phase 5.**
The method produces an auditable sample and review packet, but has not established
historically stable semantics. `human_validation_not_completed`;
`recall_not_estimated`. Phase 4's accepted numerical outputs remain unchanged.

## Baseline, protocol and commits

Baseline `046a43f299f56c7122e9cc488a86732e295dc00d`, clean, on
`codex/project-reset-architecture`. Startup read AGENTS, Phase 4 report/integrity
review and relevant architecture/decisions; dependencies and hashes are in the
[context index](../studies/gkg-semantics-v1/context-index.json). Baseline offline
suite: 191 tests, 190 passed, one Windows symlink-permission skip.

| Commit | Reviewable change |
|---|---|
| `5ddf7e3` | Preregister concepts, labels, sampling, retrieval and gates before article inspection |
| `77fe85a` | Freeze authenticated 120-reference sample; deterministic contracts and retrieval |
| `ea22f67` | Preserve every retrieval outcome, taxonomy evidence and machine annotations; initial adversarial repairs |
| `ab78c78` | Complete assessment, packet, replay, preservation checks and 64 new offline tests |
| Final documentation commit | This report, architecture, storage and CI evidence; exact SHA in Git/final response |

[Preregistration](../studies/gkg-semantics-v1/preregistration.json) and
[annotation protocol](../studies/gkg-semantics-v1/annotation-protocol.json) are v1.0.0.
Canonical protocol root:
`b0a00fa7574fa60241c0adbec56a1469171070a218127db63605dd5d95eb5e41`.
No criteria, sample references or replacement policy changed after retrieval.

## Exact sample

Authenticated all original **96 ZIPs / 494,483,985 bytes**, Phase 3 row ledgers and
Phase 4 source-metric pins. The sample frame contains **7,793 accepted rows** with
at least one panel token. [Sample manifest](../studies/gkg-semantics-v1/sample.json)
records every population, exclusion, reference, rank and original batch/member/row
locator, source/ledger/metric hash and selected case identity. Sample root:
`3a8710caabb8d571edbbd5f80276e00f25cec26c9622655d3b3db8d7045b9a46`.

| Original batch cohort (UTC, inclusive 15-minute slots) | PROTEST | FOOD_SECURITY | WB_2747_UNEMPLOYMENT |
|---|---:|---:|---:|
| 2015-03-02 00:00–00:45 | 6 | 6 | 0 |
| 2016-09-05 06:00–06:45 | 6 | 6 | 8 |
| 2020-09-05 12:00–12:45 | 6 | 6 | 8 |
| 2023-09-05 18:00–18:45 | 6 | 6 | 8 |
| 2025-09-05 00:00–00:45 | 6 | 6 | 8 |
| 2026-08-05 12:00–12:45 | 5 | 5 | 4 |
| 2026-09-04 00:00–17:45 | 5 | 5 | 4 |
| **Total** | **40** | **40** | **40** |

Algorithm `sha256-ranked-theme-richness-edges-v1`, seed
`psychohistory-phase5-2026-09-06-v1`: one lowest and one highest distinct-theme-count
row per nonempty token/cohort cell, then seeded hash-ranked rows. Thus **40 metadata
edge cases + 80 ranked cases**, not handpicked semantic examples. Fixed token/cohort
order and canonical earliest row per exact DocumentIdentifier prevent duplicate
references improving selection rank. There are 120 distinct references across 112
literal outlet names; zero replacements, shortfalls or exact complete-body duplicates.
The World Bank token has no 2015 positives; that cell is untested, not a negative.
All cases are token-positive. No independent relevant-document frame supports recall.

## Retrieval and availability bias

One bounded public HTTP(S) GET per original reference, up to five redirects,
12-second socket timeout and 2 MiB body bound; concurrency four. No HTTPS rewrite,
search replacement, archive-service lookup or paid API was silently substituted.
These are outcomes of this bounded method, **not proof of permanent article loss**.

| Year | Selected | Candidate context | Insufficient context | Unavailable |
|---|---:|---:|---:|---:|
| 2015 | 12 | 0 | 4 | 8 |
| 2016 | 20 | 0 | 5 | 15 |
| 2020 | 20 | 4 | 3 | 13 |
| 2023 | 20 | 7 | 2 | 11 |
| 2025 | 20 | 3 | 7 | 10 |
| 2026 | 28 | 7 | 11 | 10 |
| **Total** | **120** | **21** | **32** | **67** |

Only **17.5%** have provisional extracted context. There were 53 HTTP-200 responses;
HTTP success alone is not reviewability. Five redirects require article-identity
review. Same-path responses can also have changed since the original GKG record.
Early-year context availability is particularly poor, so survivor-only semantic
comparisons would be biased. The extractor's English cues and 25-word quote budget
also limit context recovery; failure to extract does not establish irrelevance.

Failure categories: HTTP error 39; network error 22; timeout 1; nonpublic DNS/address
blocked 3; redirect limit 1; non-200 status 1; insufficient automatic context 26;
article identity review 5; decoding failure 1. The remaining 21 have candidate
context. [Availability](../studies/gkg-semantics-v1/results/availability.json) retains
selected and unique-context denominators by token, year and outlet, HTTP statuses,
all failure categories and archived/retrievable status. [Receipts](../studies/gkg-semantics-v1/retrieval.json)
retain original/final URLs, redirects, times, status, byte counts, hashes, locators
and minimal text. No full publisher article corpus is retained.

## Annotation and semantic findings

Seven labels separate direct, contextual, incidental, mismatch, ambiguous,
insufficient-context and unavailable cases. Cue matching only locates complete
sentences/paragraphs; it never produces topical judgments. If context cannot be
located conservatively, manual review is required. Titles exceeding the compact
quote budget are explicitly marked available-but-omitted, rather than fabricated.

Reviewer registry: **one machine preprocessor, zero humans, zero LLM reviewers**.
The 99 machine annotations describe unavailability/insufficient context only;
there are **zero semantic judgments**. The unblinded
[120-row human packet](../studies/gkg-semantics-v1/results/human-review-packet.csv)
shows source/year/concept, reference, minimal excerpt and blank human labels;
its [JSON form](../studies/gkg-semantics-v1/results/human-review-packet.json) includes
fixed choices. No aggregate prevalence or expected conclusion appears in it.
No user judgment is assumed, and no machine/model output is labeled human.

| Token | Candidate / selected | Insufficient / unavailable | Semantic finding and decision |
|---|---:|---:|---|
| PROTEST | 4 / 40 | 12 / 24 | Topic documented; prospective/historical vs incidental/metaphorical distinctions unreviewed. `continue_semantic_validation` |
| FOOD_SECURITY | 7 / 40 | 10 / 23 | Food-access topic documented; agriculture/price/humanitarian vs generic-food relevance unreviewed. `continue_semantic_validation` |
| WB_2747_UNEMPLOYMENT | 10 / 40 | 10 / 20 | Unemployment topic documented; generic employment/macroeconomic distinctions unreviewed; 2015 absence unresolved. `continue_semantic_validation` |

Direct, direct+contextual, mismatch and ambiguity rates are **null**, with selected,
unique candidate-context and genuinely reviewed denominators recorded separately.
They are not fabricated zero match rates. Agreement/confusion matrices are
`not_estimated`: no independent human review pairs exist. No cross-year semantic
stability, classifier precision, recall, event counts, hunger severity or
unemployment-rate validity is established.

## Taxonomy and extractor evidence

[Eleven classified findings](../studies/gkg-semantics-v1/taxonomy-evidence.json)
distinguish provider statements, repository observations, engineering inference
and unresolved questions; snapshots/references have hashes.

* Provider topical examples support [PROTEST](https://blog.gdeltproject.org/announcing-gdelt-geographic-news-search/),
  [FOOD_SECURITY](https://blog.gdeltproject.org/announcing-our-first-api-gkg-geojson/)
  and [WB_2747_UNEMPLOYMENT](https://blog.gdeltproject.org/google-bigquery-gkg-2-0-sample-queries/).
  They do not document classifier accuracy or temporal invariance.
* [World Bank incorporation](https://blog.gdeltproject.org/world-bank-group-topical-taxonomy-now-in-gkg/)
  was announced March 2, 2015. The retained 00:00–00:45 hour has no unemployment
  token. Intraday deployment timing is unknown; a segmentation boundary is not proven.
* [Theme additions in December 2014](https://blog.gdeltproject.org/over-100-new-gkg-themes-added/)
  establish that the theme universe evolved, not that these three meanings changed.
* [2019](https://blog.gdeltproject.org/new-august-2019-gkg-2-0-themes-lookup/) and
  [2021](https://blog.gdeltproject.org/new-november-2021-gkg-2-0-themes-lookup/)
  lookup updates report empirical histograms. A lookup refresh is not an extractor
  dictionary release or historical version ledger.

Bounded official-source searches did not establish version-resolved dictionaries
or classifier configurations across sampled years. Absence of located documentation
is not stability evidence. GKG 2.1 field schema continuity is a separate engineering
finding; unrelated GDELT LLM/entity-extraction experiments are not theme-version proof.

## Preregistered gates and recommendation

Thresholds were fixed before retrieval: per human, at least 24 semantic reviews,
direct+contextual >=85%, mismatch <=10%; at least three reviews per required year,
year match-rate spread <=25%; availability >=60% pooled and >=4 contexts per
required year; two independent humans with >=24 paired reviews and >=80% agreement.
These are bounded exploratory gates, not population guarantees.

| Gate | All three tokens |
|---|---|
| Provider topic documentation | Pass |
| Positive semantic consistency / cross-year consistency | Pending human review |
| Availability | Fail |
| Historical taxonomy stability | Unresolved |
| Captured-evidence auditability | Pass, within documented source-revision limits |
| Reviewer quality | Pending human review |
| Material uncertainty | Unresolved |

No token qualifies for a historical pilot. None is scientifically rejected merely
because its articles are unavailable. All three and Phase 5 remain
**`continue_semantic_validation`**. The method's integrity checks work, so the result
is not forced into `redesign_semantic_validation`; retrieval and human evidence need
improvement before semantic conclusions can be made.

## Efficiency, retention and verification

Deterministically processed 120 documents; zero article LLM calls, zero full articles
sent to a model, zero semantic cases resolved by model/human, zero cached review
hits. Full-context requirements remain unknown pending human review. The compact
context cache is configuration/content-addressed. Article-model token use is zero;
Codex engineering token usage is unavailable and was not fabricated. Details:
[efficiency](../studies/gkg-semantics-v1/results/efficiency.json).

Measured publication categories: compact semantic evidence **260,789 bytes**;
derived records/packets/cache **295,644**; manifests/provenance **192,920**; new raw
GKG archives **0**; new quarantine evidence **0**. Total **749,353 bytes** for the
explicit file sets, excluding code/docs, Git history and backups. If an equally
sized 120-case audit were repeated monthly, that representation extrapolates to
**8,992,236 bytes/year**; this is not a selected schedule or a raw-data forecast.
Original 96 ZIPs and 72,355-byte Phase 3 quarantine payload remain preserved.
[Storage](../studies/gkg-semantics-v1/storage.json) separates all retention classes.
No paid dependency, deletion, acquisition-frequency or retained-field reduction.

All **94 checked original artifacts** and all **96 raw archive hashes** remain
unchanged; this includes Phase 2/3/4 evidence, schemas, original scripts and protected
production behavior. Two final offline assessments match all eight artifacts and
manifest root `7776721638beeecb7eb235c3bded17f439abaa1e831dbd81d44371c652d532d4`.
No network is used in replay or CI. Original Phase 4 outputs were not regenerated.
See [preservation](../studies/gkg-semantics-v1/preservation.json) and
[replay](../studies/gkg-semantics-v1/replay.json).

**255 offline tests:** Windows 254 passed, one symlink-permission skip; zero
failures/errors. **Ubuntu 255/255**, zero skips, at implementation/evidence commit
`ab78c78ec9020b1f6d1abd743d24d6bb023eccbc`, verified in
[CI run 34006777030](https://github.com/edwardsage419/Psychohistory/actions/runs/34006777030),
3.753 seconds. The final documentation HEAD is tested separately; its exact SHA
and CI result are supplied in the final response, not attributed to this ancestor.

The 64 new tests cover required sampling, contracts, trust, cache, denominators,
agreement, gates and replay. Adversarial tests reproduced block-page classification,
partial-hash deduplication, missing LLM configuration, lost/conflicting duplicate
reviews and incomplete HTTP handling; all were repaired. Additional guards prevent
shortfall years disappearing, false blinding and favorable-reviewer-pair selection.
[Review](../studies/gkg-semantics-v1/adversarial-review.json) and
[supplement](../studies/gkg-semantics-v1/adversarial-review-supplement.json) distinguish
confirmed reproductions from added guards. No retained numeric results changed.
This is specific regression evidence, not a claim that all possible bugs are absent.

## Remaining work

Unresolved: exact historical article revisions, sufficient early-year context,
independent human labels, lexical dictionary/extractor versions, translation/outlet
bias and generalization beyond the convenience corpus. The conservative extraction
budget and original-address-only method require separate empirical improvement.

**Next recommended issue:** preregister dated archive/HTTPS recovery for the same
frozen references, preserving all original failures, then obtain two independent
genuine human reviews of sufficient context. Do not replace inconvenient cases or
start historical backfill/forecasting. No production behavior changed; no main merge.
Implementation and trust instructions: [architecture](SEMANTIC_AUDIT_ARCHITECTURE.md).
