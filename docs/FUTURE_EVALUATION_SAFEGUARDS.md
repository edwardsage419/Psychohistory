# Future Evaluation Safeguards

Date: 2026-09-07
Status: future scientific specification. This document does not authorize Gate 7, Gate 8, Gate 9, or Gate 10 implementation.

## Purpose

Define the minimum point-in-time, forecast, resolution, and evaluation safeguards that must exist before Psychohistory can make defensible historical backtest, calibration, or AI-performance claims.

This specification operationalizes `SCIENTIFIC_INVARIANTS.md` and `docs/SCIENTIFIC_RISK_REGISTER.md` for future implementation.

## 1. Point-in-time data contract

A future observation used in forecasting or historical simulation must be able to distinguish, where applicable:

* `reference_start`
* `reference_end`
* `published_at`
* `available_at`
* `retrieved_at`
* `revision_id` or equivalent provider vintage
* `revision_published_at` when known
* provider/source version
* immutable source snapshot or trusted source reference
* transformation version

Definitions:

`reference_*` describes when the measured phenomenon occurred.

`published_at` describes when the provider released the value.

`available_at` is the earliest defensible time Psychohistory could have known the value under the source contract. It may equal `published_at`, but that must not be assumed when embargoes, delayed APIs, batch publication, or market fixing rules exist.

`retrieved_at` describes when Psychohistory actually acquired the value.

A historical forecast may use a record only when its admissible `available_at` is no later than the forecast information cutoff.

When `available_at` cannot be established with enough precision for a use case, the observation is restricted from that point-in-time use.

### Existing schema compatibility

`schemas/observation.v1.schema.json` is retained unchanged for accepted current research artifacts.

Its `observed_at` plus `retrieved_at` representation must not be silently overloaded to mean publication time, availability time, and vintage simultaneously.

Future revised statistical source work should design a versioned successor contract if these semantics cannot be represented without ambiguity.

## 2. Vintage resolution contract

For a historical cutoff `T`, the feature builder must resolve only a version that was available by `T`.

Required behavior:

1. identify the metric/reference period
2. enumerate admissible revisions/vintages
3. select the latest revision with `available_at <= T`
4. preserve the selected vintage identity in feature provenance
5. return missing/unknown if no admissible vintage can be established

Forbidden behavior:

* query today's API and assume the returned history equals the historical information set
* replace a missing old vintage with the current revised value
* mutate a prior stored observation when a revision arrives

## 3. Causal transformation contract

Every transform used in historical simulation must declare whether it is fitted or stateless.

For fitted transforms preserve:

* fit-window start/end
* fit information cutoff
* input snapshot root
* transformation parameters/state hash
* code/version identifier

The transform must reject inputs whose availability exceeds the simulation cutoff.

Examples requiring causal treatment:

* rolling normalization
* z-scores
* ranking across entities
* PCA/factor models
* detrending
* seasonal adjustment performed by Psychohistory
* learned embeddings/classifiers
* threshold optimization
* imputation

Centered filters and full-sample statistics are prohibited for historical forecast inputs unless the experiment explicitly studies an offline descriptive method and does not label the result point-in-time forecasting.

## 4. Forecast issuance contract

A formal forecast record should bind at minimum:

* `forecast_id`
* `issued_at`
* `information_cutoff`
* target definition ID/version/hash
* horizon start/end
* probability or predictive distribution
* method/model ID and version
* model/prompt/configuration hash where applicable
* feature snapshot root
* evidence snapshot root
* resolution rule ID/version/hash
* code version
* substantive forecast content hash

Required temporal relation:

`all input available_at <= information_cutoff <= issued_at`

Issuance must be append-only.

A correction cannot overwrite the original forecast. It creates a linked correction/version with a reason and timestamp.

## 5. Historical simulation classes

Future evaluation must distinguish at least three classes.

### Class A: genuine contemporaneous forecast

The forecast was actually issued at the stated time with a preserved information snapshot.

This is the strongest evidence.

### Class B: faithful historical replay

The method existed and is fully reconstructable, and the replay uses only an authenticated point-in-time information set that was available then.

This may support historical method evaluation if model availability and other assumptions are defensible.

### Class C: retrospective experiment

A current method or model is applied to historical inputs after the outcome occurred.

This can be scientifically useful but must not be presented as a forecast that actually existed historically.

Current LLMs used on old dates normally fall into Class C because their trained parameters may contain later facts even when prompts are closed-book.

## 6. AI historical-evaluation contract

Historical AI evaluation has an additional model-information problem beyond dataset timestamps.

A model can be treated as contemporaneously available only if:

* the exact model/version existed at the simulated time
* its deployment/configuration is identified
* the evaluation can defend that no unavailable tool/retrieval context is injected
* any training-information limitations relevant to the claim are documented

For modern LLM retrospective experiments:

* label results `retrospective_model_experiment`
* do not claim they represent what the model would have forecast at the historical date
* do not use live web search or current connected sources
* supply only a frozen point-in-time evidence packet when testing closed-book reasoning
* treat parameter-level future knowledge contamination as unresolved unless independently controlled

A prompt such as "pretend it is 2020" is never a leakage control.

## 7. Retrieval boundary contract

For any historical simulation using retrieval:

* corpus membership must be frozen
* every document must have an admissible availability timestamp
* index build must exclude post-cutoff documents and post-cutoff metadata
* ranking features must not use later popularity/citation/outcome information
* retrieved document IDs/hashes are included in the evidence snapshot

Live web search is incompatible with a strict historical simulation unless the system is querying a preserved historical search/index environment with defensible cutoff semantics.

## 8. Outcome resolution contract

Before scoring a target class, define:

* target/event definition version
* resolution source hierarchy
* resolution deadline
* positive/negative criteria
* ambiguity policy
* unresolved policy
* source conflict policy
* resolver provenance

Resolution records bind the exact rule version used.

If the rule does not support a defensible outcome, mark unresolved. Do not force an outcome to increase scoreable sample size.

## 9. Evaluation cohort contract

Every confirmatory evaluation must define before result inspection:

* forecast cohort start/end
* included target classes
* horizon classes
* eligible model/method versions
* inclusion/exclusion rules
* unresolved-outcome treatment
* failed-run treatment
* primary score(s)
* baseline(s)
* minimum sample requirements where relevant

The evaluation output must disclose:

* forecasts issued
* forecasts eligible
* forecasts resolved
* forecasts unresolved
* forecasts excluded with reason codes
* failures
* scoreable final cohort

A forecast must not disappear from the registry because it is inconvenient to score.

## 10. Development versus confirmatory evaluation

Repeated model, prompt, feature, threshold, or indicator tuning on one historical corpus converts that corpus into development data.

After material tuning:

* results on the tuning corpus are exploratory
* a new untouched cohort is required for a stronger confirmatory claim
* consequential tuning attempts should be recorded sufficiently to understand selection pressure

Walk-forward or nested schemes may be used when appropriate, but their split rules must be fixed and causal.

## 11. Baseline parity contract

Model comparisons must distinguish information advantage from modeling advantage.

Each compared method records:

* allowed information cutoff
* feature set or evidence set
* target definition/version
* forecast horizon
* evaluation cohort

A baseline should receive the same admissible underlying information needed for a fair comparison unless the experiment explicitly studies the value of an additional information source.

Recommended transparent baseline families may include:

* historical base rate
* persistence
* simple trend/rule
* simple regression/classification model
* market-implied probability where appropriate

## 12. Calibration safeguards

Calibration claims require compatible forecast cohorts.

Do not pool probabilities across materially incompatible target definitions, resolution versions, or horizons without explicit justification.

Report where appropriate:

* reliability/calibration by horizon or target class
* Brier/log score with cohort definition
* nominal count and effective dependency concerns
* unresolved/excluded counts
* uncertainty intervals when sample size permits

Repeated forecasts for the same underlying event must not automatically be treated as independent samples.

## 13. Timezone and market-time safeguards

For market/rate/event data preserve:

* canonical UTC time
* source timezone
* session/fixing/close semantics
* holiday calendar where material
* publication delay where material

A daily bar or policy-rate observation is not automatically available at 00:00 on its date.

## 14. Point-in-time universe safeguards

Historical entity universes must be reconstructed as they existed at the cutoff.

Examples:

* equity index constituents
* listed securities
* country membership/classifications
* provider source lists
* monitored topics/categories

Current survivors cannot silently replace discontinued historical members.

## 15. Required adversarial test catalogue

These tests are specifications for future implementation. They should become executable only when the relevant module/schema exists.

### PTI-001 Future release rejection

Fixture: observation references 2020 but `available_at` is 2021.

Expected: a 2020 cutoff rejects it.

### PTI-002 Historical vintage selection

Fixture: two revisions for the same reference period, one released before cutoff and one after.

Expected: only the earlier revision is selected.

### PTI-003 Current-history substitution rejection

Fixture: historical vintage is unavailable but current revised API value exists.

Expected: missing/unknown, not substitution.

### PTI-004 Future-fit normalization rejection

Fixture: scaler parameters depend on a post-cutoff observation.

Expected: validation failure.

### PTI-005 Future-filled missingness rejection

Fixture: missing value is interpolated using the next-period observation.

Expected: validation failure for point-in-time use.

### PTI-006 Timezone boundary rejection

Fixture: source release at 16:00 New York is used by a 15:00 New York forecast.

Expected: rejection.

### FCT-001 Forecast mutation rejection

Fixture: issued probability or horizon is modified in place.

Expected: hash/version failure; correction must append.

### FCT-002 Non-atomic evidence snapshot rejection

Fixture: one feature was retrieved after issuance or lacks a snapshot binding.

Expected: issuance validation failure.

### FCT-003 Target-definition version mismatch

Fixture: forecast points to one target version while scorer resolves another.

Expected: scoring failure unless explicit compatibility rule exists.

### RES-001 Hindsight rule change rejection

Fixture: resolution rule changes after issue date and old forecast is rescored under the new rule without a new experiment version.

Expected: rejection.

### RES-002 Ambiguity preservation

Fixture: source evidence cannot satisfy positive or negative rule.

Expected: unresolved, not forced binary outcome.

### EVAL-001 Registry completeness

Fixture: one issued forecast is omitted from evaluation without preregistered exclusion.

Expected: cohort validation failure.

### EVAL-002 Baseline information parity

Fixture: model sees a feature unavailable to baseline in a claimed model-only comparison.

Expected: comparison invalid or explicitly reclassified as information-source experiment.

### EVAL-003 Post-hoc cohort filtering

Fixture: forecast removal reason is created after outcomes are visible and does not match accepted policy.

Expected: confirmatory evaluation failure.

### EVAL-004 Calibration version mixing

Fixture: incompatible target/resolution versions are pooled without declared aggregation policy.

Expected: validation failure.

### EVAL-005 Dependency disclosure

Fixture: many forecasts share one underlying event but evaluation claims independent sample size.

Expected: warning/blocking status according to claim strength.

### AI-001 Current-model historical-forecast mislabel

Fixture: a current LLM is run on historical evidence and record type is `genuine_historical_forecast`.

Expected: rejection; classify as retrospective experiment unless exact historical model availability is established.

### AI-002 Live-search historical leakage

Fixture: historical simulation performs unrestricted current web search.

Expected: rejection.

### AI-003 Retrieval corpus cutoff

Fixture: one indexed document is post-cutoff.

Expected: historical run invalid.

### SRC-001 Duplicate-upstream independence claim

Fixture: two provider series resolve to the same upstream series but both are marked independent.

Expected: lineage validation failure.

### SEM-001 Semantic break crossing

Fixture: historical indicator window crosses an explicit definition break without a version/restriction rule.

Expected: comparison failure or restricted-period output.

## 16. Gate requirements

### Before Gate 7 forecast registry acceptance

Require executable controls for:

* point-in-time input admissibility
* forecast immutability
* atomic evidence/feature snapshot
* target and resolution version binding

### Before Gate 8 resolution acceptance

Require executable controls for:

* resolution rule versioning
* independent evidence reference
* unresolved/ambiguity handling

### Before Gate 9 scoring/backtesting acceptance

Require executable controls for:

* vintage resolution
* causal transformations
* cohort completeness
* baseline parity
* no future information
* evaluation-version compatibility

### Before Gate 10 AI historical-performance claims

Require explicit review of:

* model historical availability
* training/parameter contamination limits
* retrieval cutoff
* prompt/model versioning
* tuning versus held-out evaluation

## 17. Current repository interpretation

Current GKG tests already provide strong evidence-chain protection, including external trust pins, duplicate/missing evidence rejection, definition pinning, and adversarial resealing tests.

Those controls should be reused conceptually, especially the principle that an artifact cannot authenticate itself.

No current module implements the future point-in-time forecast/evaluation contracts above. Therefore this document intentionally specifies future tests rather than adding meaningless test stubs that would pass without a real implementation.

## 18. Stop rule

If future implementation cannot establish an information cutoff, admissible vintage, immutable forecast snapshot, or compatible resolution/evaluation rule, preserve the unresolved state and stop the scientific claim.

Do not substitute current data, current LLM knowledge, post-hoc rules, or convenient cohort filtering for the missing historical contract.
