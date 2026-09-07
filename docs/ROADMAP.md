# Psychohistory Roadmap

## Roadmap rule

Psychohistory advances by evidence gates, not by old phase numbering. Historical Phase reports remain valid records of completed work, but their numbering does not determine the next task.

At every gate, the project may:

* advance when acceptance criteria are met
* remain experimental when evidence is incomplete
* restrict an indicator to a narrower time range or use case
* reject a candidate when evidence shows it is unsuitable

Failure or rejection is a valid scientific outcome.

## Candidate lifecycle rule

Gates 1 through 5 are normally applied to the relevant source/measurement candidate, not as a permanent global lock requiring every existing candidate to succeed before another candidate can be researched.

The current GKG work is one candidate lifecycle. Failure, restriction or pause of GKG does not constitute failure of Psychohistory.

A new source family may begin a separately authorized Gate 1/2 admission and measurement-validation path when governance selects it. This does not authorize multi-source state construction; Gate 6B still requires multiple sufficiently validated and sufficiently independent indicators.

For the current GKG path, recovery must remain bounded. After each explicitly authorized network-recovery batch, governance reassesses whether another batch can materially change the scientific decision. Possible outcomes are continue, restrict, pause or reject. See `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`.

## Current position

Authoritative branch: `main`.

Accepted work includes Phase 1-4 data/measurement foundation, Phase 5 preregistered semantic audit, Phase 6A bounded historical evidence recovery, Phase 6A.1 targeted identity recovery, completed model-assisted human identity review with final human adjudication, and the evidence-sufficiency `1.0.1` correction.

Current gate: Gate 3A, historical document identity and evidence sufficiency for the GKG candidate.

Readiness before independent semantic review requires at least 24 review-ready E2/E3 contexts per token and at least 4 review-ready E2/E3 contexts per allocated year. Exact current counts are maintained in `CURRENT_STATE.md` and the machine-readable correction contract rather than duplicated here.

The immediate accepted task is the deterministic recovery-target manifest in `docs/NEXT_ACCEPTED_TASK.md`.

## Gate 1: source and evidence integrity

Status for the GKG research path: substantially established for the bounded research corpus.

Required capabilities:

* reproducible acquisition or exact source references
* byte/integrity validation
* lossless parsing and quarantine
* source/version provenance
* deterministic replay
* explicit failure states

Completed work in Phase 1-3 provides the current foundation. New source families must independently pass equivalent integrity requirements before promotion.

## Gate 2: measurement validity

Status for current GKG exact-token media-prevalence measurements: experimental foundation established, stronger interpretation not established.

Required capabilities:

* explicit versioned IndicatorDefinition
* reproducible transformation
* defined denominator, aggregation, missingness and lag policies
* quality and provenance records
* documented known biases and limitations

Current GKG token metrics remain media-attention measurements. They do not measure event counts, public opinion, severity or real-world risk without further validation.

## Gate 3A: historical document identity and evidence sufficiency

Status: current bottleneck for the GKG candidate.

Goal: obtain sufficient objective, replayable historical context for the immutable frozen 120-reference Phase 5 sample.

Immediate work:

1. Generate the deterministic recovery-target manifest across all 120 references using evidence-sufficiency version `1.0.1`.
2. Preserve the accepted machine identity states and historical evidence artifacts; recompute current E0/E1/E2/E3 classification mechanically rather than rewriting historical evidence files.
3. Prioritize deficient token/year cells using review-ready E2/E3 coverage under the accepted protocol.
4. Treat E1 as identity-confirmed but context-insufficient evidence that may still require bounded context recovery.
5. Use human `SAME_ARTICLE` judgments only as recovery guidance, never as automatic E2/E3 promotion.
6. Keep human `DIFFERENT_ARTICLE` and objective identity mismatches visible and exclude current mismatches from promotion targeting under the accepted task rules.
7. Perform bounded objective publisher/archive recovery only after the manifest and batch are accepted and network recovery is explicitly authorized.
8. Recompute review-ready E2/E3 coverage mechanically after each bounded accepted batch.
9. Reassess recovery viability after each batch; do not authorize indefinite recovery merely because deficits remain.

Hard constraints:

* no replacement sampling
* no syndicated substitution
* no guessed archive identity
* no unrelated search-result substitution
* no silent change to the frozen identity hierarchy
* no rewriting machine evidence with human judgments
* no treating a non-empty fallback paragraph as review-ready context unless it satisfies the accepted context-sufficiency contract

Possible outcomes:

* readiness threshold reached
* partial progress with another bounded batch justified
* restricted historical validity/use case
* pause pending a genuinely new recovery capability
* rejection of the GKG candidate for historical-indicator promotion

Evidence standards must not be weakened to force advancement.

## Gate 3B: historical semantic stability and selection robustness

Status: blocked by Gate 3A evidence sufficiency.

Goal: determine whether the audited token meaning is defensible across the intended historical period and whether the semantic evidence is too selected by survivorship/recoverability to support promotion.

Questions include:

* Does the same token represent sufficiently similar topical content across allocated years?
* Is there evidence of provider taxonomy or extractor drift?
* Are ambiguous or context-dependent uses frequent enough to invalidate a historical series?
* Is a restricted historical validity period more defensible than full-period continuity?
* Does reviewability vary materially by year, outlet, cohort, frozen selection role or recovery method?
* Could unresolved/unreviewable frozen cases plausibly change the semantic conclusion?

The Phase 5 report already warned that survivor-only semantic comparisons would be biased. Therefore the 24/4 E2/E3 readiness threshold is an evidence-volume threshold, not a representativeness claim.

Before any Gate 5 promotion, apply `docs/GATE3_RECOVERY_SELECTION_AND_PIVOT_GUARD.md`. Keep reviewed and full selected denominators visible, preserve unresolved cases, and use explicit missingness sensitivity where the unresolved share can affect the conclusion.

Each token may end as:

* promotable over the intended period
* promotable only over a restricted period
* experimental only
* rejected

No production semantics follow automatically from token-string continuity or a favorable survivor-only review rate.

## Gate 4: independent semantic validation

Status: blocked until the frozen review-ready E2/E3 readiness threshold is met.

Goal: obtain genuine independent human semantic review under a preregistered protocol.

Requirements:

* genuine human reviewers
* sufficient objective review-ready context
* preserved reviewer independence where required
* explicit disagreement and ambiguity handling
* no LLM output counted as human evidence
* reproducible review import and provenance
* full frozen denominator accounting retained alongside actually reviewed cases

The completed 22-case model-assisted identity review with final human adjudication does not satisfy this later independent semantic-review requirement.

Passing Gate 4 semantic-label thresholds does not override an unresolved Gate 3B selection/missingness problem.

## Gate 5: experimental historical indicator promotion

Status: future.

Only measurements passing the applicable integrity, semantic, selection/missingness and independent-validation gates may enter an experimental historical indicator registry.

Promotion records should include:

* indicator ID and definition version
* validated interpretation
* applicable time range
* source family and transformation
* evidence basis
* known biases and limitations
* unresolved uncertainty
* quality requirements
* provenance requirements
* promotion status

Promotion to experimental does not imply production decision authority.

## Gate 6A: independent source-family expansion

Status: future. Research planning exists, but no new source integration is currently authorized.

Gate 6A is the portfolio-level expansion decision that selects new source families for their own bounded Gate 1/2 admission and measurement-validation lifecycle. It does not require the GKG candidate to have succeeded, but it does require explicit authorization.

Priority is diversity of evidence-generation mechanisms rather than adding many provider names or correlated news feeds.

Current planning documents:

* `docs/MULTI_SOURCE_STRATEGY.md`
* `docs/SOURCE_FAMILY_RESEARCH_2026_09.md`
* `docs/GATE6A_SOURCE_ADMISSION.md`

The current research recommendation for a first future expansion wave is to study BIS financial/monetary statistics, EIA energy statistics and ILOSTAT labor statistics as three materially different source families after Gate 6A is explicitly activated. This order is planning guidance only.

Candidate families include:

* official macroeconomic statistics
* labor-market data
* prices, rates and financial-market data
* trade and industrial activity
* energy production, consumption and prices
* food and commodity data
* conflict and security event datasets
* disasters and climate observations
* public-health data
* demographic data
* surveys and confidence measures
* technology-adoption signals
* news/media attention as one observation family

Each family must pass its own access/license, provenance, time-semantics, revision/vintage, historical-continuity, measurement and upstream-lineage review. Provider diversity must not be counted as evidence independence when the same upstream series or documentary sources are reused.

## Gate 6B: interpretable state representation

Status: future.

Composite or latent state construction begins only when multiple sufficiently independent validated indicators exist.

Candidate dimensions may include economic stress, social tension, institutional stress, geopolitical stress, resource stress and technology transition, but names and definitions require evidence rather than intuition alone.

Requirements:

* transparent component list
* explicit weighting or model specification
* decomposition into contributing indicators
* versioned historical semantics
* missingness and revision policy
* uncertainty representation
* tests against simple transparent baselines

Do not publish a single opaque global risk score.

## Gate 7: forecast registry and baselines

Status: future and blocked for production use. Architecture planning is complete enough to constrain a later bounded implementation, but no forecast schema or engine is currently authorized.

Planning documents:

* `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md`
* `docs/GATE7_9_SCHEMA_REQUIREMENTS.md`
* `docs/FUTURE_EVALUATION_SAFEGUARDS.md`
* `docs/DECISION_2026_09_07_POINT_IN_TIME_EVALUATION.md`

Gate 7 should be decomposed rather than implemented as one forecast object:

### Gate 7A: target and resolution semantics

Define versioned target definitions and compatible resolution rules before probabilities are issued.

### Gate 7B: point-in-time snapshot and method contracts

Require admissible information cutoffs, vintage-aware feature/evidence snapshots, versioned forecast methods and transparent baseline methods.

### Gate 7C: forecast issuance registry

Implement append-only issuance, immutable substantive forecast content, explicit run attempts and append-only corrections.

Formal forecast records should bind at least:

* forecast ID
* issue timestamp
* information cutoff
* forecast class
* target definition ID/version/hash
* horizon
* probability or predictive distribution
* method/model version/hash
* feature snapshot
* evidence snapshot
* resolution rule ID/version/hash
* run-attempt reference
* immutable substantive content hash

Binary event forecasts and directional/categorical trend forecasts may share issuance/provenance machinery, but their target and scoring semantics remain distinct.

All formally issued forecasts remain discoverable, including forecasts later superseded for future use or difficult to resolve. Simple transparent baselines are first-class forecast methods and should exist before AI forecasting is evaluated.

## Gate 8: outcome resolution

Status: future.

Outcome resolution must be specified independently enough to prevent hindsight-driven reinterpretation and remain bound to the target/rule versions fixed at issuance.

Required design:

* resolution source hierarchy
* resolution date and deadline
* event/trend criteria
* target-data vintage/reference
* ambiguity policy
* unresolved policy
* source-conflict policy
* resolver/version provenance
* append-only correction trail

Resolution states must permit explicit unresolved, ambiguity, insufficient-evidence and source-conflict conditions where the rule cannot support a defensible outcome.

Forecast generation and outcome resolution should be separated where practical. A missing or conflicting resolution cannot be converted into a negative outcome merely to increase the scoreable sample.

## Gate 9: scoring, calibration and historical evaluation

Status: future.

Only forecasts with valid immutable issuance records and independently defined outcomes may enter scoring.

Confirmatory evaluation must use a frozen evaluation-cohort manifest that records inclusion/exclusion policy, unresolved treatment, failed-run treatment, target/method versions, horizon grouping, primary metrics and baseline methods before result inspection.

Potential metrics include:

* Brier score
* log score
* calibration/reliability curves
* discrimination
* interval/distribution scoring for future continuous forecasts
* baseline-relative performance
* performance by horizon and event class where sample size permits

Every evaluation must disclose enough registry accounting to reconstruct its denominator, including issued, eligible, resolved, unresolved, excluded and failed counts where applicable.

Historical evaluation must use only information, vintages, transformation states, retrieval corpora, models/tools and rules admissible at the simulated historical timestamp. Look-ahead leakage is a blocking failure.

Repeated forecasts sharing one underlying event cannot automatically be treated as independent samples. Repeated tuning on one historical cohort converts that cohort into development data for stronger confirmatory claims.

Calibration is an evaluation over immutable forecasts, not a mechanism for retroactively changing their probabilities. Any learned calibration transform used prospectively becomes part of a new causally fitted forecast-method version.

## Gate 10: AI forecasting and decision support

Status: future.

AI value must be measured against transparent baselines rather than assumed.

Potential comparisons include:

* historical base rate
* persistence
* simple trend rules
* simple statistical models
* market-implied probabilities where appropriate
* expert priors

AI may support evidence synthesis, contradiction detection, scenario generation and forecast reasoning, but unsupported facts must remain detectable and consequential model/prompt/tool provenance must be recorded.

A current LLM applied to an old date is normally a retrospective model experiment because parameter-level future knowledge may exist. It cannot be labelled as a genuine contemporaneous historical forecast without independently establishing historical model availability and information boundaries.

Decision-support outputs for investing or personal planning remain downstream artifacts and must stay distinguishable from observations, forecasts and forecast-resolution outcomes.

## Product layer

A user-facing product should follow scientific capability rather than lead it.

When justified, the interface should expose:

* current observations
* indicator values and trends
* source quality and freshness
* state estimates with decomposition
* active forecasts
* evidence and uncertainty
* resolution history
* calibration and baseline comparisons

The retired V0.2 frontend is not a design constraint. A new interface should be designed from validated research outputs when the underlying gates justify it.

## Infrastructure rule

Default to zero or near-zero recurring cost while the research foundation is being validated.

Paid infrastructure is justified only when a free approach materially harms data integrity, reproducibility, reliability, analytical quality or product capability and the benefit is supported by evidence.

Do not weaken evidence retention, scientific thresholds or historical reproducibility to save infrastructure cost.

## Next bounded work

The only currently accepted advancement task is defined in `docs/NEXT_ACCEPTED_TASK.md`.

Do not use this roadmap, the Gate 3 guard, or future Gate 6-10 design documents as authorization to start later gates. Each later gate or new candidate source requires a separately bounded task and applicable acceptance review.
