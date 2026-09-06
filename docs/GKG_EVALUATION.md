# GKG production-candidate evaluation — Issue 2

Recommendation: **continue_validation**. Acquisition is technically promising;
production ingestion and indicator semantics have not passed their gates.

## Verified structure

The [official GKG 2.1 codebook](https://data.gdeltproject.org/documentation/GDELT-Global_Knowledge_Graph_Codebook-V2.1.pdf)
was consulted on 2026-09-06 (local date), especially extracted fields on pages
5–15. It defines the ordered 27-field record, tab delimiters, publication date
(field 2, including the `0` unknown sentinel), and semicolon-separated V1THEMES
(field 8). Document rows are not deduplicated real-world events. The
[provider data page](https://gdeltproject.org/data.html) documents batch access.
We validate this structure; the remaining fields stay uninterpreted.

## Empirical acquisition

A live integration run at `2026-09-05T22:16:56Z` (2026-09-06 local time)
completed with process exit 0. The initial sandbox-denied network attempt is an
environment permission failure, not evidence of GDELT unreliability. The approved
network run succeeded. No credentials, paid service or production write was used.

Exact retained evidence: [versioned report](evidence/gkg-20260905221500.report.json).

| Measurement | Observed result |
| --- | --- |
| Batch reference | http://data.gdeltproject.org/gdeltv2/20260905221500.gkg.csv.zip |
| ZIP bytes | 2,102,833 |
| Expanded bytes | 6,456,954 |
| Data members | 1: 20260905221500.gkg.csv |
| SHA-256 | df4305ae9f18ee73cc84241c7b5e18b56c754dd051000df58f1feb01ca74c402 |
| Discovery MD5 | 787964f8f06061cb63bf1e4e3a125936; matched downloaded bytes |
| Decoded / valid / rejected rows | 479 / 479 / 0 |
| Field distribution | All 479 rows have 27 fields |
| Date distribution | All 479 rows: 20260905221500 |
| Unknown date / duplicate ID / encoding errors | 0 / 0 / 0 |
| Empty theme rows | 76 of 479 (15.87%) |
| Unique literal theme tokens | 1,459 |
| Validation scope | Entire member read, CRC checked, statistics complete |

Most frequent literal tokens: TAX_FNCACT 358, CRISISLEX_CRISISLEXREC 193,
EPU_POLICY 166, UNGP_FORESTS_RIVERS_OCEANS 148, TAX_ETHNICITY 147.
ECON_INFLATION appears in 4 rows. ARMEDCONFLICT appears in 68; the old synthetic
fixture's ARMED_CONFLICT appears in zero. These are literal frequency findings,
not endorsed meanings, indicator mappings or proof that an absent code never
exists. The new synthetic fixtures use clearly fictional TEST_A/TEST_B codes.

All 1,459 counts are retained with their denominator and source checksum.
The ZIP itself is not committed; replay requires re-fetching the exact reference
and verifying SHA-256. Provider retention/immutability is not guaranteed. A
follow-up must decide raw retention from measured volume and usage rights.
The discovered URL uses HTTP; MD5 from HTTPS discovery detects disagreement but
does not authenticate a publisher. HTTPS batch acquisition should be evaluated
explicitly before promotion; this run preserved the literal discovery reference.

## What the evidence supports

Strict parsing, missingness measurement, complete frequency collection and
machine-readable acquisition failure handling work locally. The baseline
DECISIONS.md records an earlier successful Actions run, but its artifact was not
retrieved here. This local success does not establish Actions reliability.
Offline tests establish behavior on controlled malformed data, not source quality.

No evidence supports rejecting the entire source. Equally, one recent batch does
not support production promotion. No thematic interpretation, seven-topic mapping,
observation adapter, composite index or forecast has been introduced.

## Unknowns and promotion gates

* Sustained success rate, latency, missed batches and resource peaks across time.
* Historical backfill availability, revisions and long-term reproducibility.
* Exact usage and redistribution constraints, including publisher rights.
* Representativeness across languages, geography, sources and collection types.
* Duplicate documents across batches, syndication effects and extraction accuracy.
* Theme semantics and measured precision/recall for any proposed construct.
* Storage cost/retention policy and metric-specific missingness thresholds.

Empty themes are legal and empirically common in this sample. Passing structural
validation cannot turn those records into zero-valued societal conditions. The
numeric observation schema is a foundation, not a claim that GKG already yields
a meaningful normalized societal measurement.

## Recommended next issue

**GKG bounded continuity and reproducibility study.** Collect a fixed manifest of
96 consecutive 15-minute batches plus a small explicitly dated historical sample.
Record every attempt, absence, checksum, size, duration and validation report;
replay retained references and compare content hashes and frequency outputs.
Produce coverage/missingness and resource summaries, evaluate HTTPS, document
usage terms and historical access, and propose a storage/retention budget.
Keep all outputs outside the dashboard and add no theme-to-topic mappings.
Acceptance: every manifest slot accounted for, failures visible, replays compared,
measured gaps and costs published, and a revised promotion recommendation. This
is a single acquisition research phase, not the entire production ingestion system.
