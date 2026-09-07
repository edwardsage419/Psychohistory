# Source Family Research 2026-09

Date: 2026-09-07
Status: future Gate 6A research only. No source is admitted or promoted by this report.

## Research question

Which public or low-cost source families are currently suitable candidates for expanding Psychohistory beyond the existing GDELT GKG media-attention family while preserving source traceability, historical reproducibility, point-in-time correctness and a path toward a future product?

The review favors official provider documentation and current provider terms. Access, license and product conditions can change and must be rechecked immediately before implementation.

## Executive result

Recommended first implementation sequence after Gate 6A becomes an accepted task:

1. BIS financial and monetary statistics
2. EIA international energy statistics
3. ILOSTAT labor statistics

Recommended second wave:

4. World Bank WDI / Indicators API
5. FAOSTAT
6. UCDP
7. USGS ComCat plus carefully scoped GDACS
8. UN Comtrade, subject to product-license/cost review

EM-DAT is scientifically valuable but should remain deferred for normal product integration under the current zero/near-zero-cost policy because free access is non-commercial and redistribution is restricted. IMF and OECD remain useful secondary official-statistics candidates where they add genuinely new series rather than duplicate upstream data.

## Evaluation dimensions

Each candidate was reviewed qualitatively for:

* construct value
* evidence-generation mechanism
* programmatic access
* historical coverage
* update cadence
* revision and vintage behavior
* geographic coverage
* licensing and future-product compatibility
* known overlap with other source families
* reproducibility risk
* near-zero-cost fit

No numeric score is used. A weighted score would create false precision before empirical source studies exist.

## 1. Financial and monetary conditions

### Preferred provider: BIS Data Portal

Constructs potentially supported:

* policy-rate conditions
* bilateral and effective exchange rates
* credit to the non-financial sector
* credit-to-GDP gaps
* debt-service ratios
* international banking exposures
* global liquidity
* debt securities
* residential/commercial property prices
* central-bank balance-sheet measures

Access:

The BIS Data Portal exposes an SDMX REST API for both data and metadata and supports JSON, XML and CSV. Bulk downloads are also available.

Current cadence:

The September 2026 BIS release calendar shows daily/monthly exchange-rate and policy-rate updates alongside monthly and quarterly financial datasets. Cadence therefore varies by series and must remain per-series metadata.

Revision behavior:

BIS reporting authorities may submit revisions. Banking-statistics revisions are incorporated in scheduled releases, and BIS publishes information on revisions and breaks. Structural breaks can reflect reporting-population changes, sector-classification changes or methodological improvements.

Lineage:

Most BIS statistical datasets rely on national statistics supplied by central banks and other national authorities. Therefore BIS should not automatically be counted as independent from the same national series obtained through another international aggregator.

License/product fit:

BIS says use of statistics is unrestricted subject to conditions and attribution. Its terms include a condition concerning commercial products and additional charges to users. This deserves a specific legal/product interpretation before a paid Psychohistory product includes BIS-derived data.

Research assessment:

High priority. Strongly complementary to GKG, mature machine access, explicit release/revision infrastructure, good current-state value.

Official references:

* https://data.bis.org/help/tools
* https://data.bis.org/release-calendar
* https://www.bis.org/about/legal/permitted-use-statistics
* https://data.bis.org/faq

## 2. Energy production, consumption and prices

### Preferred provider: U.S. Energy Information Administration Open Data

Constructs potentially supported:

* energy production
* energy consumption
* petroleum, gas, coal and electricity conditions
* selected energy prices
* import/export and supply relationships
* energy-system stress and structural transition signals

Access:

EIA API v2 is RESTful and supports metadata, facets and date-range queries. The API is a free public service but requires registration/API credentials for normal access. Bulk files are available for several datasets.

Coverage:

EIA reports tens of thousands of international energy series. Its current international visualization exposes annual, quarterly and monthly options; many current international histories extend approximately from 1980 through 2024, depending on series.

License/product fit:

EIA states that U.S. government publications and its own data/files/databases are generally public domain and may be used or distributed with acknowledgment. Third-party protected material remains an exception.

Revision risk:

Methods, source inputs and historical values can change. Forecast products and observed statistics coexist on EIA systems, so the source adapter must distinguish observed data from projections structurally, not by naming convention alone.

Independence:

Physical energy statistics offer strong conceptual independence from media attention. Some international observations may originate from national statistical or energy authorities, so cross-provider lineage still matters.

Research assessment:

High priority. Strong low-cost/product fit and high complementary value. Recommended as the second new source family after BIS.

Official references:

* https://www.eia.gov/opendata/
* https://www.eia.gov/opendata/documentation.php
* https://www.eia.gov/about/copyrights_reuse.php
* https://www.eia.gov/international/data/world/total-energy/more-total-energy-data

## 3. Labor-market conditions

### Preferred provider: ILOSTAT

Constructs potentially supported:

* unemployment
* employment-to-population ratio
* labor-force participation
* youth NEET
* earnings
* informal employment
* labor underutilization
* occupational and industrial-relations measures

Access:

ILOSTAT recommends its bulk download facility, R package and SDMX-based APIs for automated use.

License/use:

ILOSTAT states that its data are free to use and provides citation formats.

Historical and semantic risk:

Labor statistics require unusually strong definition/version control. The 19th International Conference of Labour Statisticians changed core definitions of work and employment. ILOSTAT explicitly warns that these revisions create major breaks in some countries and that users should not compare series across databases based on incompatible concepts.

Modelled-estimate revisions:

ILO modelled estimates may change when countries release new data, when upstream databases such as UN population projections or IMF WEO are revised, or when historical estimates are reworked.

Lineage overlap:

ILOSTAT itself notes that World Bank WDI reuses ILOSTAT data. Therefore a WDI unemployment series derived from ILOSTAT and the corresponding ILOSTAT series are one upstream evidence lineage for independence accounting.

Research assessment:

High priority but scientifically demanding. Recommended third new family because labor is central to the project and the definitional-break problem is exactly the kind of issue Psychohistory should solve explicitly rather than hide.

Official references:

* https://ilostat.ilo.org/about/get-started/
* https://ilostat.ilo.org/about/dissemination-and-analysis/
* https://ilostat.ilo.org/methods/concepts-and-definitions/forms-of-work/
* https://ilostat.ilo.org/methods/concepts-and-definitions/ilo-modelled-estimates/

## 4. Macroeconomic conditions

### Preferred first provider: World Bank WDI / Indicators API

Potential constructs:

* GDP and growth
* inflation and price measures
* debt and debt service
* investment and savings
* external balances
* population-normalized structural indicators
* development and institutional context variables

Access:

World Bank Indicators API v2 requires no API key. The provider states that it exposes nearly 16,000 time-series indicators across more than 45 databases and that many series extend back more than 50 years.

License:

World Bank-produced open datasets default to CC BY 4.0 subject to additional terms. Third-party indicators can carry different restrictions and must be checked at indicator/dataset level.

Revision risk:

WDI explicitly states that historical data may change with each database update. Revisions can reflect better surveys, improved methods, new source data and deletion of previously published values judged no longer robust. This makes point-in-time snapshots mandatory before using WDI in forecasting evaluation.

Lineage risk:

WDI is an aggregator as well as a producer. Individual indicators can originate with ILO, IMF, national statistics offices or other organizations. Source organization metadata must therefore be captured for every series.

Research assessment:

Strong broad-coverage candidate, but lower initial priority than BIS/EIA/ILOSTAT because it aggregates many heterogeneous lineages and much of its core structural data are annual. It is valuable as a macro context family once the lineage/vintage layer exists.

Official references:

* https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
* https://datahelpdesk.worldbank.org/knowledgebase/articles/898599-indicator-api-queries
* https://datacatalog.worldbank.org/public-licenses
* https://datahelpdesk.worldbank.org/knowledgebase/articles/114939-how-are-revisions-managed

### Secondary macro candidate: IMF Data

IMF Data exposes SDMX 2.1 and 3.0 APIs. Current API documentation uses portal-account sign-in for API exploration. IMF special terms permit broad reuse of published statistical data with attribution, while systematic access and third-party content still require attention to the detailed terms.

Use IMF where it adds unique high-frequency or specialized macro series. Do not import an IMF version of a series merely to duplicate the same upstream national observation already present elsewhere.

Official references:

* https://data.imf.org/en/Resource-Pages/IMF-API
* https://www.imf.org/en/about/copyright-and-terms

## 5. Food and agricultural conditions

### Preferred provider: FAOSTAT and related FAO statistical databases

Potential constructs:

* food production
* crop and livestock output
* agricultural input conditions
* food prices
* food balances
* trade and food availability
* water/agricultural resource conditions through related FAO databases

Access and history:

FAOSTAT provides free access for more than 245 countries and territories and states that coverage extends from 1961 to the latest available year. It offers an API developer portal and bulk downloads.

License:

FAO corporate statistical databases are generally CC BY 4.0 unless metadata says otherwise, subject to additional FAO terms and third-party exceptions. The terms also restrict uses that imply promotion or endorsement of commercial enterprises/products, so future commercial-product use requires a targeted legal interpretation.

Independence:

Much of the data originates in national reporting systems. This is different from GKG media extraction but may overlap upstream with World Bank or national official series.

Research assessment:

Strong second-wave candidate, especially because food/resource stress is a central Psychohistory construct and the current GKG FOOD_SECURITY token should eventually be compared against real food/agricultural observations rather than treated as the same thing.

Official references:

* https://www.fao.org/faostat/en/
* https://www.fao.org/contact-us/terms/db-terms-of-use/en

## 6. International trade and industrial linkage

### Preferred provider: UN Comtrade

Potential constructs:

* total exports/imports
* bilateral trade dependence
* product-specific supply exposure
* trade concentration
* trade-network changes
* commodity-flow disruptions

Coverage:

UN Comtrade describes itself as a global platform covering approximately 200 countries and more than 99% of merchandise trade, with annual and monthly official trade statistics by product and partner.

Access:

The current free registered tier advertises downloads of up to 100,000 records per call and up to 500 API calls per day. Preview endpoints can work without a subscription key but are intentionally limited. Bulk endpoints are premium.

Revision/timing:

Country data are released as official submissions become available and there is no fixed posting schedule for every country. The system offers data-availability and live-update endpoints. Historical trade data therefore need explicit release-time and revision snapshots.

License/product friction:

Current UN Comtrade policy distinguishes internal use, visualization, transformed data and re-dissemination. Its help center states that transformed-data redistribution can still require an active premium subscription and that for-profit applications may require premium institutional access and distribution fees. This is a significant future-product constraint.

Research assessment:

Scientifically valuable, operationally feasible for bounded research, but do not make it one of the first three production-path source families until the intended product/re-dissemination model is clear.

Official references:

* https://comtrade.un.org/
* https://uncomtrade.org/docs/un-comtrade-api/
* https://uncomtrade.org/docs/faqs-on-use-and-re-dissemination/
* https://comtradeplus.un.org/LicenseAgreement

## 7. Conflict and organized violence

### Preferred provider: UCDP

Potential constructs:

* state-based conflict events
* non-state conflict
* one-sided violence
* battle-related deaths
* event geography and dates
* conflict intensity and actor structure under explicit UCDP definitions

Access:

UCDP's API is REST/JSON and free of charge, but authenticated access now requires an access token requested from the maintainer. Current quota is 5,000 requests per day.

Versioning:

This is an unusually strong feature. UCDP requires a version number and states that a versioned API URL is guaranteed to return the same data version indefinitely. That is directly aligned with Psychohistory reproducibility goals.

History:

Current yearly UCDP/PRIO armed-conflict data cover 1946-2025, while several organized-violence datasets cover 1989-2025. GED and Candidate releases provide event-level and more current data.

Independence caveat:

UCDP is human-coded documentary/event data. GED records include source-article references such as BBC Monitoring and AFP. Therefore UCDP and GKG can share underlying news evidence. UCDP adds human coding, event definitions and validation, but cross-source agreement cannot automatically be called independent confirmation.

License unresolved item:

The retrieved current API and download documentation establishes free research access and versioned retrieval, but this review did not locate sufficiently explicit current redistribution/commercial license language for the full datasets. License/product rights must be verified before admission beyond bounded internal research.

Research assessment:

High scientific value and excellent version semantics. Recommended in the second wave after the first three source families, with explicit documentary-lineage tracking.

Official references:

* https://ucdp.uu.se/apidocs/
* https://ucdp.uu.se/downloads/

## 8. Natural hazards and disasters

This family should be split into physical-hazard observations and human-impact disaster coding. Combining them into one source would blur distinct constructs.

### Preferred physical-hazard subfamily: USGS ComCat

The USGS FDSN Event Web Service supports parameterized historical earthquake queries and multiple machine-readable formats. ComCat records include event and product update times, and products can have superseding versions.

USGS states that U.S. government datasets are generally public domain in the United States, while third-party material can have separate rights.

Strength:

Earthquake observations are generated by geophysical monitoring systems and are therefore highly independent of media attention.

Limitation:

Earthquakes are one hazard class and cannot stand in for total disaster burden.

Official references:

* https://earthquake.usgs.gov/fdsnws/event/1/
* https://earthquake.usgs.gov/data/comcat/index.php
* https://www.usgs.gov/data-management/data-licensing

### Broader multi-hazard candidate: GDACS

GDACS exposes a current documented API with event lists and event detail endpoints. Its 2025 API quick-start states that GDACS data are free and requests source acknowledgment. API examples support date-bounded multi-hazard searches.

Strength:

Broader event coverage than USGS and useful alert/severity metadata.

Risks:

GDACS integrates information from multiple upstream systems. Exact lineage, historical retention, event-version semantics and provider-specific hazard methods must be established empirically before using it as an independent family.

Official references:

* https://www.gdacs.org/gdacsapi/swagger/index.html
* https://www.gdacs.org/Documents/2025/GDACS_API_quickstart_v2.pdf

### Deferred impact database: EM-DAT

EM-DAT is scientifically important for disaster impacts and contains more than 27,000 disaster records from 1900 onward. The living public data are updated weekly and include entry/last-update fields.

However, current free access is explicitly non-commercial after registration. The research archive is distributed under CC BY-NC-ND, and EM-DAT terms restrict redistribution and derivative/substitute databases. Commercial use requires a separate paid agreement.

Under Psychohistory's current cost and future-product constraints, EM-DAT should remain a research/deferred candidate unless a later license decision justifies integration.

Official references:

* https://doc.emdat.be/docs/data-accessibility/
* https://doc.emdat.be/docs/legal/terms-of-use/
* https://doc.emdat.be/docs/introduction/

## Existing family: GDELT GKG news/media attention

Current registry source:

`gdelt-gkg-2.1`

The current research foundation has established bounded acquisition, parsing and provenance behavior. It has not established full historical semantics for the experimental exact-token measurements.

Future multi-source design must preserve the following interpretation:

GKG media prevalence measures observed media tagging/attention behavior under the relevant GKG semantics. It cannot serve as ground truth for unemployment, conflict severity, food insecurity, disaster impact or other real-world constructs without independent validation.

## Cross-source lineage examples

### ILOSTAT and World Bank

ILOSTAT states that World Bank WDI reuses ILOSTAT data. A matching labor series from both portals is therefore duplicated upstream evidence.

### BIS and national central banks

BIS statistics often rely on central-bank/national-authority submissions. If Psychohistory later ingests the same central-bank statistic directly, the two records share upstream evidence even if transformations differ.

### UCDP and GKG

UCDP event coding may rely on news articles that could also appear in GDELT. The coding methodology adds structure but does not erase shared documentary origins.

### World Bank and other international organizations

WDI exposes source-organization metadata and contains many third-party indicators. Every selected series needs its own lineage, license and revision assessment.

## Point-in-time data risk by family

High revision/vintage concern:

* World Bank WDI
* ILOSTAT modelled estimates
* BIS banking and related revised official statistics
* UN Comtrade
* UCDP candidate/current event datasets
* GDACS/EM-DAT impact records

Potentially lower but still version-sensitive:

* EIA observations
* FAOSTAT
* USGS event products

No family should be assumed immutable simply because it is public or official.

## Recommended first source studies

When Gate 6A becomes active, do not integrate all candidates together. Run independent bounded studies in this order.

### Study 1: BIS

Test:

* API discovery and metadata
* exact byte/content preservation
* release-time semantics
* historical query consistency
* revisions/break metadata
* a small fixed set of policy-rate, exchange-rate and credit series
* source lineage to national authorities

### Study 2: EIA

Test:

* API v2 and bulk retrieval
* API key/secret handling without committing credentials
* observed-versus-forecast dataset separation
* international historical continuity
* revision behavior
* physical-unit semantics

### Study 3: ILOSTAT

Test:

* SDMX/bulk reproducibility
* standard/concept version boundaries
* observed versus modelled series
* publication/retrieval timestamps
* breaks caused by ICLS changes
* upstream model dependencies

Only after each study passes should a proposed IndicatorDefinition be designed.

## Research conclusion

The project has enough credible low-cost public data infrastructure to support a future multi-source system. The main difficulty is not finding APIs. The difficult work is preserving lineage, publication time, revisions, definitions and licensing so that later forecasts and backtests remain falsifiable.

For that reason, the recommended near-term architecture remains conservative: build three deeply validated, different source families rather than a large shallow data catalog.
