# Psychohistory Multi-Source Strategy

Date: 2026-09-07
Status: future Gate 6A architecture research only. This document does not authorize source integration, production promotion, composite-state construction, forecasting, calibration, or backtesting.

## Purpose

Psychohistory ultimately needs multiple observation families whose upstream evidence-generation mechanisms are sufficiently different that agreement across them can add information rather than merely repeat the same signal through different providers.

The current GDELT GKG path remains a media-attention observation family. It is scientifically useful only within the semantic and historical limits established by the current evidence program. Future source expansion must complement that family with measurements generated from other institutional, physical, transactional, survey, or coded-event processes.

## Core strategy

The project should count independent evidence mechanisms, not provider names.

Two providers are not independent merely because their APIs and organizations differ. A downstream aggregator that republishes an upstream source inherits that upstream lineage for the relevant series. A coded conflict dataset built partly from news reports is only partially independent from a media-monitoring dataset. Two official-statistics portals may both originate from the same national statistical office.

Every admitted observation or indicator therefore needs an explicit upstream lineage record sufficient to answer:

* who originally generated the underlying fact or estimate
* which organizations transformed or harmonized it
* whether another Psychohistory source uses the same upstream data
* whether the observation is measured, estimated, modelled, coded, reported, or inferred
* which timestamp describes the real-world reference period
* when the value first became publicly available
* whether historical values can later be revised

Cross-source confirmation may only be described as independent when upstream lineage supports that claim.

## Initial source-family map

The first expansion wave should concentrate on eight families plus the existing news/media family.

1. Financial and monetary conditions
2. Energy production, consumption and prices
3. Labor-market conditions
4. Macroeconomic conditions
5. Food and agricultural conditions
6. International trade and industrial linkage
7. Conflict and organized violence
8. Natural hazards and disasters
9. News and media attention, already represented experimentally by GDELT GKG

Public health, demographics, surveys/confidence, technology adoption, climate reanalysis and additional market microstructure can be evaluated in later waves. They should not be added simply to increase source count.

## Recommended implementation order after Gate 6A is authorized

### First new family: BIS financial and monetary statistics

Preferred initial provider: Bank for International Settlements Data Portal.

Why first:

* Strong conceptual separation from media attention.
* Machine-readable SDMX API exposes data and metadata.
* Useful series include policy rates, bilateral/effective exchange rates, credit, debt service, banking exposures, global liquidity and property prices.
* Release calendars and revision/break information are explicit.
* Many series update monthly or quarterly, making the family useful for current-state monitoring.

Main risks:

* Many BIS series ultimately come from central banks or national authorities, so lineage must be tracked when combined with other official macro sources.
* Historical values can be revised and series can contain structural breaks.
* BIS terms permit statistical use with attribution but impose conditions on commercial-product use; commercial deployment requires a specific license review.

### Second new family: EIA energy statistics

Preferred initial provider: U.S. Energy Information Administration Open Data API, especially International Energy data.

Why second:

* Physical production and consumption measures provide a highly different evidence mechanism from news and financial statistics.
* EIA offers a free API with registration and bulk data options.
* International energy data include annual, quarterly and monthly series and currently expose long histories, with many international series reaching back to about 1980.
* U.S. government EIA data are generally public-domain material, subject to attribution and third-party exceptions.

Main risks:

* Coverage, methods and update latency vary by country and series.
* Forecast datasets such as STEO/AEO must never be mixed with observed historical series without explicit type separation.
* Revisions and source changes require snapshot/vintage handling.

### Third new family: ILOSTAT labor statistics

Preferred initial provider: International Labour Organization ILOSTAT.

Why third:

* Labor conditions are central to social stress and economic state.
* ILOSTAT supports bulk downloads and SDMX APIs and states that its published data are free to use with citation.
* The family provides unemployment, employment, labor-force participation, earnings, informal employment, youth NEET and related measures.
* It adds survey and administrative evidence that differs substantially from media and energy signals.

Main risks:

* Statistical standards change. The 19th ICLS introduced material breaks in employment and unemployment concepts in some countries.
* ILO modelled estimates are revised when national data, population projections, IMF data or model methods change.
* Some World Bank indicators directly reuse ILOSTAT, so those duplicate series cannot be counted as independent World Bank confirmation.

### Subsequent families

After those three families pass source admission and measurement validation, evaluate the remaining families in bounded tasks:

* World Bank WDI for broad macroeconomic and development statistics
* FAOSTAT for food, agriculture and resource conditions
* UN Comtrade for bilateral and product-level international trade
* UCDP for organized violence and georeferenced conflict events
* USGS ComCat and GDACS for physical hazard and multi-hazard event observations

No later family is automatically authorized by this document.

## Independence model

Future multi-source analysis should use at least four lineage classes.

### A. Direct physical or transactional measurement

Examples: earthquake instrument observations, measured energy production, some market/central-bank transaction or balance-sheet statistics.

These are often highly complementary to news attention.

### B. Official survey or administrative statistics

Examples: labor force surveys, national accounts, customs reports, agricultural statistics.

These can be high quality but may share national upstream authorities across multiple international organizations.

### C. Harmonized or modelled international statistics

Examples: international organizations that transform national submissions, impute gaps, harmonize definitions or produce modelled estimates.

The transformation itself can add value, but it does not create a fully independent underlying observation.

### D. Human-coded documentary/event data

Examples: UCDP conflict coding and similar event datasets.

These add structured interpretation but may share documentary sources with news/media systems. Their source lists and coding process must therefore be included in the lineage graph.

GDELT GKG currently belongs primarily to a media/document-extraction family and should not be used as an independent confirmation of another dataset when both ultimately derive from the same articles.

## Vintage and revision architecture

Point-in-time reproducibility is mandatory for future forecasting and backtesting.

Many official APIs return the latest revised history rather than the values that were visible on a historical date. World Bank WDI explicitly states that historical observations may change with each database update. BIS accepts revisions from reporting authorities. ILO modelled estimates can revise historical periods. Comtrade updates official trade data as countries report or revise it.

Therefore every admitted mutable source must support one of these patterns:

1. Provider-native version or vintage retrieval.
2. Immutable provider release files or archived editions.
3. Psychohistory-owned retrieval snapshots captured at acquisition time with exact content hashes, retrieval timestamps and metadata.

A current API response must never be used to claim what the system would have known at an earlier forecast timestamp unless the corresponding historical vintage is independently established.

For live operation, preserve compact point-in-time source snapshots or sufficient immutable release artifacts from the first day a source is admitted. This is more valuable than attempting to reconstruct vintages years later.

## Source versus indicator independence

Admission of a source family does not validate any indicator derived from it.

The required chain remains:

source integrity -> normalized observation -> measurement definition -> historical continuity -> semantic/construct validation -> experimental indicator

A source may be reliable while a proposed indicator is invalid. A valid indicator may also depend on several non-independent raw series. Source count and indicator count therefore must never be used as evidence-quality proxies.

## Geographic strategy

Do not force every family into one common global geographic resolution prematurely.

Each observation retains its native geographic or entity scope. Country-level macro data, bank-counterparty exposures, geolocated conflict events and earthquake coordinates are fundamentally different objects.

Cross-family geographic aggregation should occur only through explicit versioned transformations. Unknown geography remains unknown.

## Update-frequency strategy

The mature system should contain multiple temporal scales rather than forcing every source into daily updates.

Potential roles:

* Daily or weekly: exchange rates, policy rates, some market/physical hazard data, media attention.
* Monthly: labor subsets, trade, energy, consumer prices and other official releases where available.
* Quarterly: GDP, banking statistics, many labor and financial indicators.
* Annual: structural development, agriculture, demographic and some conflict statistics.

Slow data can still contribute to state estimates if its age and information timestamp remain explicit. Forward-filling a slow series into daily data does not create new information and must be labeled as persistence rather than a new observation.

## Candidate provider posture

### Strong research candidates

* BIS Data Portal
* EIA Open Data
* ILOSTAT
* World Bank Indicators API / WDI
* FAOSTAT
* UCDP
* USGS ComCat
* GDACS

### Useful but with higher access or product constraints

* UN Comtrade: strong data value, but bulk access and re-dissemination/commercial rules create product friction.
* IMF Data: broad high-value macroeconomic data, but API access and systematic-use terms should be reviewed for the exact workflow before admission.
* OECD Data Explorer: high-quality SDMX data, especially for advanced economies, but geographic scope overlaps strongly with other official-statistics families.
* EM-DAT: important disaster-impact database, but current free access is non-commercial and redistribution is constrained; commercial use requires a paid agreement.

These constraints do not make a source scientifically weak. They change its fit with the project's zero/near-zero-cost and future-product requirements.

## No provider substitution rule

If a preferred source later becomes unavailable, paid, legally unsuitable or historically irreproducible, do not silently replace it with another provider while keeping the same source or indicator identity.

A replacement provider is a new source version or new source definition and requires explicit continuity analysis.

## Future registry implications

The current source registry can continue to hold provider-level metadata. Before Gate 6A implementation, consider extending the source-family representation with explicit fields or companion records for:

* source_family_id
* upstream_lineage
* evidence_generation_class
* reference_time_semantics
* public_release_time_semantics
* revision_policy
* vintage_support
* historical_snapshot_policy
* license/product_constraints
* independence_notes

This document does not change the existing schema. Any schema modification remains a separately reviewed L3 task.

## Success condition for Gate 6A expansion

The goal is not a large catalog of APIs. A useful first multi-source milestone would be three additional validated source families whose measurements are demonstrably different from GKG and from one another, with point-in-time provenance and at least one defensible experimental indicator from each.

The recommended initial target is therefore:

GKG media attention + BIS financial/monetary + EIA energy + ILOSTAT labor.

Only after those families survive their own integrity, historical and measurement gates should Psychohistory consider a broader state representation.

## Official research references inspected 2026-09-07

* World Bank Indicators API: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
* World Bank dataset terms: https://datacatalog.worldbank.org/public-licenses
* World Bank revision policy: https://datahelpdesk.worldbank.org/knowledgebase/articles/114939-how-are-revisions-managed
* BIS developer/API tools: https://data.bis.org/help/tools
* BIS permitted use: https://www.bis.org/about/legal/permitted-use-statistics
* BIS release calendar: https://data.bis.org/release-calendar
* ILOSTAT automated access: https://ilostat.ilo.org/about/get-started/
* ILOSTAT reuse/citation: https://ilostat.ilo.org/about/dissemination-and-analysis/
* ILOSTAT standards/breaks: https://ilostat.ilo.org/methods/concepts-and-definitions/forms-of-work/
* EIA Open Data: https://www.eia.gov/opendata/
* EIA API documentation: https://www.eia.gov/opendata/documentation.php
* EIA copyrights/reuse: https://www.eia.gov/about/copyrights_reuse.php
* FAOSTAT: https://www.fao.org/faostat/en/
* FAO statistical database terms: https://www.fao.org/contact-us/terms/db-terms-of-use/en
* UN Comtrade: https://comtrade.un.org/
* UN Comtrade API: https://uncomtrade.org/docs/un-comtrade-api/
* UN Comtrade use/re-dissemination FAQ: https://uncomtrade.org/docs/faqs-on-use-and-re-dissemination/
* UCDP API: https://ucdp.uu.se/apidocs/
* UCDP downloads: https://ucdp.uu.se/downloads/
* USGS earthquake catalog API: https://earthquake.usgs.gov/fdsnws/event/1/
* USGS data licensing: https://www.usgs.gov/data-management/data-licensing
* GDACS API: https://www.gdacs.org/gdacsapi/swagger/index.html
* EM-DAT accessibility: https://doc.emdat.be/docs/data-accessibility/
