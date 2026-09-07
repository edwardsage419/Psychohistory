# Psychohistory Roadmap

## Roadmap rule

Psychohistory advances by evidence gates, not by old phase numbering. Historical Phase reports remain valid records of completed work, but their numbering does not determine the next task.

At every gate, the project may:

* advance when acceptance criteria are met
* remain experimental when evidence is incomplete
* restrict an indicator to a narrower time range or use case
* reject a candidate when evidence shows it is unsuitable

Failure or rejection is a valid scientific outcome.

## Current position

Authoritative branch: `main`.

Accepted work includes Phase 1-4 data/measurement foundation, Phase 5 preregistered semantic audit, Phase 6A bounded historical evidence recovery, Phase 6A.1 targeted identity recovery, completed model-assisted human identity review, and the confirmed-context coverage audit.

Current gate: semantic and historical stability with independent evidence validation incomplete.

Current frozen 120-reference E3 state:

* `PROTEST`: 0
* `FOOD_SECURITY`: 5
* `WB_2747_UNEMPLOYMENT`: 1

Readiness before independent semantic review requires:

* at least 24 E3 contexts per token
* at least 4 E3 contexts per allocated year

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

Status: current bottleneck.

Goal: obtain sufficient objective, replayable historical context for the immutable frozen 120-reference Phase 5 sample.

Immediate work:

1. Generate the deterministic recovery-target manifest across all 120 references.
2. Preserve the existing six E3 contexts exactly.
3. Prioritize deficient token/year cells under the frozen protocol.
4. Use human `SAME_ARTICLE` judgments only as recovery guidance, never as automatic E3 promotion.
5. Exclude human `DIFFERENT_ARTICLE` and objective identity mismatches from promotion targets.
6. Perform bounded objective publisher/archive recovery only after the manifest and batch are accepted.
7. Recompute E3 coverage mechanically after each bounded batch.

Hard constraints:

* no replacement sampling
* no syndicated substitution
* no guessed archive identity
* no unrelated search-result substitution
* no silent change to the frozen identity hierarchy
* no rewriting machine evidence with human judgments

Possible outcomes:

* readiness threshold reached
* partial progress with further bounded recovery justified
* formal recovery infeasibility for some cells or tokens

Evidence standards must not be weakened to force advancement.

## Gate 3B: historical semantic stability

Status: blocked by Gate 3A evidence sufficiency.

Goal: determine whether the audited token meaning is defensible across the intended historical period.

Questions include:

* Does the same token represent sufficiently similar topical content across allocated years?
* Is there evidence of provider taxonomy or extractor drift?
* Are ambiguous or context-dependent uses frequent enough to invalidate a historical series?
* Is a restricted historical validity period more defensible than full-period continuity?

Each token may end as:

* promotable over the intended period
* promotable only over a restricted period
* experimental only
* rejected

No production semantics follow automatically from token-string continuity.

## Gate 4: independent semantic validation

Status: blocked until the frozen E3 readiness threshold is met.

Goal: obtain genuine independent human semantic review under a preregistered protocol.

Requirements:

* genuine human reviewers
* sufficient objective context
* preserved reviewer independence where required
* explicit disagreement and ambiguity handling
* no LLM output counted as human evidence
* reproducible review import and provenance

The completed 22-case human identity review does not satisfy this later semantic-review requirement.

## Gate 5: experimental historical indicator promotion

Status: future.

Only measurements passing the applicable integrity, semantic and independent-validation gates may enter an experimental historical indicator registry.

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

Status: future, but research planning may begin after the current evidence bottleneck is controlled.

Priority is diversity of evidence families rather than adding many correlated news feeds.

Candidate families may include:

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

Each family must pass its own provenance, time-semantics, revision and historical-continuity review.

## Gate 6B: interpretable state representation

Status: future.

Composite or latent state construction begins only after multiple sufficiently independent validated indicators exist.

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

Status: future and blocked for production use.

Before issuing formal forecasts, define versioned forecast objects containing at least:

* forecast ID
* issue timestamp
* target and target-definition version
* horizon
* probability or predictive distribution
* method/model version
* feature snapshot
* evidence snapshot
* resolution rule reference
* status and immutable content hash

Substantive forecast content becomes immutable after issuance.

Simple transparent baselines should exist before AI forecasting is evaluated.

## Gate 8: outcome resolution

Status: future.

Outcome resolution must be specified independently enough to prevent hindsight-driven reinterpretation.

Required design:

* resolution source
* resolution date and deadline
* event or trend criteria
* ambiguity policy
* unresolved policy
* resolver/version provenance
* audit trail for metadata corrections

Forecast generation and outcome resolution should be separated where practical.

## Gate 9: scoring, calibration and historical evaluation

Status: future.

Only forecasts with valid immutable records and independently defined outcomes may enter scoring.

Potential metrics include:

* Brier score
* log score
* calibration/reliability curves
* discrimination
* interval coverage
* directional accuracy
* baseline-relative performance
* performance by horizon and event class where sample size permits

Historical evaluation must use only information that was actually available at the simulated historical timestamp. Look-ahead leakage is a blocking failure.

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

AI may support evidence synthesis, contradiction detection, scenario generation and forecast reasoning, but unsupported facts must remain detectable and model/prompt versions must be recorded.

Decision-support outputs for investing or personal planning remain downstream artifacts and must stay distinguishable from observations and forecasts.

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

Do not use this roadmap as authorization to start later gates. Each later gate requires a separately bounded task and applicable acceptance review.