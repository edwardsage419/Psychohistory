# Psychohistory Human Identity Review Packet

Last updated: 2026-09-06

Purpose: provide a compact, mobile-friendly review surface for the 22 Phase 6A.1 cases that still require genuine human identity judgment.

This packet does not contain semantic labels. It asks only whether the recovered/current publisher evidence can be treated as the same underlying historical article/reference as the original GKG-linked document.

## Decision labels

For each case choose exactly one:

* `SAME_ARTICLE` — evidence is sufficient to judge that the recovered/current page represents the same underlying article/reference.
* `DIFFERENT_ARTICLE` — evidence is sufficient to judge that it is a different article/reference or a redirect/substitution that breaks identity.
* `INSUFFICIENT_EVIDENCE` — available evidence is not strong enough to decide either way.

Also record confidence as `HIGH`, `MEDIUM`, or `LOW`, plus an optional note.

Do not infer identity merely from same domain, similar topic, similar headline, or a current page occupying the same path. When in doubt choose `INSUFFICIENT_EVIDENCE`.

The source of record for machine evidence is `studies/gkg-semantics-v2/phase6a1-triage.json`. This packet is a human-facing derivative and must not replace the underlying receipts/hashes.

## Review cases

### HIR-01

Case ID: `1602276b4e50ed386070fddf0c50016774f3c09bd0d036a221df2a1d4141ea51`
Token/year: `PROTEST`, 2015
Source: `gazettelive.co.uk`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original: `http://www.gazettelive.co.uk/all-about/proms`
Recovered: `https://www.gazettelive.co.uk/all-about/proms`
Evidence note: publisher content changed from Phase 5; no dated article metadata established.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-02

Case ID: `a09f8e635c68d00d02c82f6030a069a7d664ccd5b370c11121e88b19e430ca65`
Token/year: `PROTEST`, 2020
Source: `msn.com`
Machine state: `identity_mismatch`
Reason: `publisher_path_changed`
Original: `https://www.msn.com/en-gb/news/world/hundreds-of-thai-students-rally-to-demand-school-reform/ar-BB18JwVt`
Recovered: `https://www.msn.cn/zh-cn`
Evidence note: recovered destination is a generic MSN landing destination rather than the original article path.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-03

Case ID: `fdf4e8e8fd4387f8734c40cffd6936c0ee5fb1897b6fe378d8225ba0880c4eaa`
Token/year: `PROTEST`, 2020
Source: `bizpacreview.com`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original: `https://www.bizpacreview.com/2020/09/05/troopers-rip-belligerent-blm-protester-from-vehicle-arrests-defiant-road-blockers-near-seattle-968299`
Recovered: `https://www.bizpacreview.com/2020/09/05/troopers-rip-belligerent-blm-protester-from-vehicle-arrests-defiant-road-blockers-near-seattle-968299/`
Evidence note: dated canonical article path exists, but current bytes differ from Phase 5 capture.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-04

Case ID: `e6a28be6a9faf1c3fd76e41313504842e221e5b21a476f2c617fbfd5aecee8db`
Token/year: `PROTEST`, 2025
Source: `channelstv.com`
Machine state: `identity_mismatch`
Reason: `canonical_identity_conflict`
Original: `https://www.channelstv.com/2025/09/04/tinubu-approves-%E2%82%A61-85bn-for-education-rehabilitation-of-rescued-chibok-girls/`
Recovered: same encoded publisher URL; an alternate decoded-naira URL did not yield usable evidence.
Evidence note: canonical identity conflict remains unresolved.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-05

Case ID: `1ec0c4b40166feadfc0f984e68a4ea712c386ff88656039ce697b93dca22dedc`
Token/year: `PROTEST`, 2025
Source: `tennesseedaily.com`
Machine state: `identity_mismatch`
Reason: `publisher_path_changed`
Original path ID: `278553778`
Recovered path ID: `278553779`
Slug: `electric-metals-usa-limited-announces-results-of-annual-and-special-shareholder-meeting`
Evidence note: adjacent numeric article ID changed despite matching slug.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-06

Case ID: `194bde000746759edf4a787b6c7794c5153068695b5e7df3f74f308a69c1b654`
Token/year: `PROTEST`, 2026
Source: `arabherald.com`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `http://www.arabherald.com/news/279223164/international-exhibitions-add-cultural-appeal-to-china-summer-travel-season`
Evidence note: same path/canonical article reference, but response bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-07

Case ID: `fe06652e1d34ae9808843795bc3d7cbdbb40e7684a82819e68d5a2db6d01d0e0`
Token/year: `PROTEST`, 2026
Source: `finanznachrichten.de`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://www.finanznachrichten.de/nachrichten-2026-08/69223821-lodestar-metals-corp-lodestar-metals-reports-bulk-tonnage-gold-silver-potential-at-the-gold-run-project-in-nevada-296.htm`
Evidence note: same dated path, changed response bytes.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-08

Case ID: `da06132eebc199a31debb4dec3b1d7d8d219ead51f657ce36e67f791b357281a`
Token/year: `PROTEST`, 2026
Source: `bnionline.net`
Machine state: `identity_probable_manual_review_required`
Reason: `identity_metadata_incomplete`
Original/recovered: `https://www.bnionline.net/en/news/thandwe-residents-flee-intense-myanmar-military-airstrikes-batter-arakan-state`
Evidence note: response body continuity exists, but identity metadata is incomplete.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-09

Case ID: `edbc803ec616278c7558e78af730e80e569da4259c446e53115641ec1aa59408`
Token/year: `FOOD_SECURITY`, 2020
Source: `reliefweb.int`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://reliefweb.int/report/zimbabwe/world-bank-supports-continued-health-services-provision-cylclone-idai-affected`
Evidence note: dated article metadata exists, but current retrieval was not usable enough for objective confirmation and content changed from prior capture.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-10

Case ID: `9dabe88f50f13946b4300f59fdf7e38a77f14607faf2ea0e327be8da96bd3a95`
Token/year: `FOOD_SECURITY`, 2023
Source: `abc13.com`
Machine state: `identity_mismatch`
Reason: `publisher_path_changed`
Original: `https://abc13.com/millions-of-dollars-pledged-as-africas-landmark-climate-summit-ent/13738625/`
Recovered canonical evidence points toward ABC News article ID `102928582`; current abc13 path also changed to `/post/.../13738625/` with tracking parameters.
Evidence note: likely related/syndicated content, but identity path changed and independent equivalence was not established.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-11

Case ID: `eb1ebf5f941b79628ac2d4238285747436e9d2f612f92e5bba43c89c9187815d`
Token/year: `FOOD_SECURITY`, 2023
Source: `saudigazette.com.sa`
Machine state: `identity_mismatch`
Reason: `canonical_identity_conflict`
Original: `https://saudigazette.com.sa/article/635545/World/Asia/Afghanistan-WFP-forced-to-cut-food-aid-for-2-million-more`
Recovered/canonical candidate: `https://saudigazette.com.sa/article/635545`
Evidence note: same article numeric ID but canonical identity conflict was not objectively resolved.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-12

Case ID: `bd15553ad11249ff596865b3989d098c94ada012f3e1d97e68f7dfc2883d246a`
Token/year: `FOOD_SECURITY`, 2025
Source: `wctv.tv`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://www.wctv.tv/2025/09/04/give-them-access-new-grocery-store-griffin-heights-aims-develop-local-economy/`
Evidence note: dated publisher path and metadata exist; response bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-13

Case ID: `e57372329cda46d28c0a73c0c736fe3ee4b972637c1fe25a4dbe705331b60948`
Token/year: `FOOD_SECURITY`, 2026
Source: `havanatimes.org`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://havanatimes.org/news/international-news-briefs-for-friday-september-4-2026/`
Evidence note: dated publisher article exists; current bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-14

Case ID: `144fa4dcca5c9b0b0e10d4d75d7652603832ff23bf92760aebc3861ba0fd7ca7`
Token/year: `WB_2747_UNEMPLOYMENT`, 2016
Source: `msn.com`
Machine state: `identity_mismatch`
Reason: `publisher_path_changed`
Original: `http://www.msn.com/en-nz/travel/tripideas/an-epic-road-trip-through-australias-cape-york/ar-AAivbrs`
Recovered: `https://www.msn.cn/zh-cn`
Evidence note: generic current MSN destination does not preserve the original article path.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-15

Case ID: `745ce5ea9b3a0e51f50d97462aac8078fa91098c90b12e4e77414578a6310c67`
Token/year: `WB_2747_UNEMPLOYMENT`, 2016
Source: `iol.co.za`
Machine state: `identity_mismatch`
Reason: `publisher_path_changed`
Original: `http://www.iol.co.za/business/news/outlook-gloomy-as-infrastructure-spend-falls-short-2064399`
Recovered: `https://iol.co.za/business-report/economy/2016-09-05-outlook-gloomy-as-infrastructure-spend-falls-short/`
Recovered title: `Outlook gloomy as infrastructure spend falls short`
Evidence note: title/subject align, but publisher path and section changed; independent article identity was not established.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-16

Case ID: `c53b0be8810a53fd1c46c0fa9107188b6dbdfc63af09b9cf9c5adabe43e981ec`
Token/year: `WB_2747_UNEMPLOYMENT`, 2016
Source: `finanznachrichten.de`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered path: `nachrichten-2016-09/38486308-asian-markets-in-positive-territory-020.htm`
Recovered title: `Asian Markets In Positive Territory`
Evidence note: same dated article path/title, response bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-17

Case ID: `3c5e776fc8d12f0e141e02af5b93b4aeaa51f6ee32dbe0c0466e5ee4bbd6cd54`
Token/year: `WB_2747_UNEMPLOYMENT`, 2020
Source: `standard.net`
Machine state: `identity_probable_manual_review_required`
Reason: `identity_metadata_incomplete`
Original/recovered: `https://www.standard.net/online_features/money_and_finance/five-ways-to-help-protect-yourself-from-unemployment-insurance-fraud/article_cf86e1c1-55d4-565f-abe6-8148b2a3eaad.html`
Current title observed: `News, Sports, Jobs - Standard-Examiner`
Evidence note: current metadata date appears inconsistent with the historical sample; identity metadata is incomplete.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-18

Case ID: `5c4aa90d7b080ec8063905db4414e74c31c17c3bfee3bd6e9e04c0cdad3400cb`
Token/year: `WB_2747_UNEMPLOYMENT`, 2020
Source: `vanguardngr.com`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://www.vanguardngr.com/2020/09/they-turned-us-to-prostitutes-starved-us-for-days-libya-returnee-victims/`
Evidence note: dated publisher metadata exists; response bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-19

Case ID: `2485b3733f5a41a3244eac8d6fa53fdb4bef5fc7cb95e6177809b76ff7481d46`
Token/year: `WB_2747_UNEMPLOYMENT`, 2023
Source: `news4jax.com`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://www.news4jax.com/news/local/2023/09/05/florida-lottery-winners-are-losing-money-to-deo-overpayments-has-this-happened-to-you/`
Evidence note: dated publisher metadata exists; response bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-20

Case ID: `e2a8726e66aabb9c17236bdeb90ff6e6b1e1414ceeb5516d9c8aad8a8f9e6826`
Token/year: `WB_2747_UNEMPLOYMENT`, 2026
Source: `standardmedia.co.ke`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://www.standardmedia.co.ke/rift-valley/article/2001554589/decline-in-lake-naivasha-fish-stocks-sparks-calls-for-annual-fishing-ban`
Evidence note: same canonical path is visible, but article metadata was not sufficient and bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-21

Case ID: `9f8db6b75f5c0051eed87eb830e6e60dcf761759471b017beb84c5829dce74d7`
Token/year: `WB_2747_UNEMPLOYMENT`, 2026
Source: `lethbridgeherald.com`
Machine state: `identity_probable_manual_review_required`
Reason: `publisher_content_changed_requires_review`
Original/recovered: `https://lethbridgeherald.com/news/national-news/2026/09/04/heres-a-quick-glance-at-unemployment-rates-for-august-by-canadian-city/`
Evidence note: dated publisher article metadata exists; response bytes changed from Phase 5.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

### HIR-22

Case ID: `b665673d306568e903dd6499c3bd5ff5f6b6ddde960b33fec5a2a94d9f6cdd36`
Token/year: `WB_2747_UNEMPLOYMENT`, 2026
Source: `moneycontrol.com`
Machine state: `identity_probable_manual_review_required`
Reason: `identity_metadata_incomplete`
Original/recovered: `https://www.moneycontrol.com/world/us-debt-keeps-climbing-is-the-bond-market-finally-losing-patience-article-14022849.html`
Evidence note: canonical path exists, but metadata was insufficient for objective identity confirmation.
Human decision: `[ ] SAME_ARTICLE  [ ] DIFFERENT_ARTICLE  [ ] INSUFFICIENT_EVIDENCE`
Confidence: `[ ] HIGH  [ ] MEDIUM  [ ] LOW`
Notes:

## Completion rule

A completed human packet must preserve the reviewer identity/attestation required by the existing review-import contract. Merely editing this Markdown file is not, by itself, proof of reviewer identity or independence.

After all 22 cases are reviewed, the decisions should be imported through the versioned contract rather than manually rewriting machine evidence artifacts.
