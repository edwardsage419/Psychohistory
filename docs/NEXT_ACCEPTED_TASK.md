# Next Accepted Task

Last updated: 2026-09-11

## Task name

Forecast Trust Core v0.1 contracts and deterministic verifier.

## Goal

Implement the minimum machine readable contracts and deterministic verification infrastructure required before Psychohistory can later create a genuine prospective Forecast Ledger Genesis.

This task creates no real forecast, performs no network retrieval, resolves no outcome, calculates no performance score, and changes no accepted historical GKG evidence.

The purpose is to make future issuance fail closed unless target semantics, resolution semantics, point in time evidence, method identity, run provenance, and immutable forecast content are bound coherently.

## Strategic asset strengthened

Primary assets:

1. provenance integrity
2. prospective longitudinal readiness
3. trust and comparison infrastructure
4. low cost durability

## Classification

Risk: L2 for deterministic implementation under already accepted forecast architecture and schema requirements.

Recommended Codex model: GPT 5.6 Terra High.

Escalate to Sol High before implementation continues if execution exposes a new semantic choice that can alter target meaning, resolution meaning, point in time admissibility, trusted root semantics, forecast immutability, correction semantics, or future scoring eligibility.

Astra is not authorized for routine execution.

## Authoritative inputs

Read only what is required, in this order:

1. `AGENTS.md`
2. `CURRENT_STATE.md`
3. `docs/DECISION_2026_09_11_STRATEGIC_REACTIVATION.md`
4. `SCIENTIFIC_INVARIANTS.md`
5. `docs/DEVELOPMENT_GOVERNANCE.md`
6. `docs/ARCHITECTURE.md`
7. `docs/FORECAST_OUTCOME_EVALUATION_ARCHITECTURE.md`
8. `docs/GATE7_9_SCHEMA_REQUIREMENTS.md`
9. `docs/FUTURE_EVALUATION_SAFEGUARDS.md`
10. `docs/DECISION_2026_09_07_POINT_IN_TIME_EVALUATION.md`
11. existing repository schema and contract helpers only as implementation conventions require

Do not scan GKG studies or historical recovery code unless a shared repository utility must be reused and the reason is documented.

## Scientific invariants

At minimum, enforce the implications of:

1. I1 No future information
2. I2 Forecast immutability
3. I3 Versioned semantics
4. I4 Historical reproducibility
5. I5 Independent outcome resolution
6. I6 Evidence traceability
7. I8 Explicit uncertainty
8. I9 No silent historical rewrite
9. I10 Evaluation integrity
10. I12 Missing evidence cannot be reasoned into existence

## Scope

### 1. Target definition contract

Implement a versioned contract representing at least:

1. `target_id`
2. `target_version`
3. forecast class
4. formal semantics
5. allowed outcome or category space
6. geography or entity rule where applicable
7. reference period and horizon rules
8. target measurement or source rule
9. vintage or revision rule where applicable
10. ambiguity policy
11. unresolved policy
12. resolution deadline rule
13. substantive content hash

The first implementation may support binary and categorical or directional target classes. Continuous targets remain out of scope unless the existing accepted design can support them without introducing new semantics.

### 2. Resolution rule contract

Implement a versioned contract representing at least:

1. `resolution_rule_id`
2. version
3. compatible target identities or compatibility contract
4. source hierarchy
5. source conflict policy
6. evidence sufficiency rule
7. allowed resolution states
8. vintage selection rule where applicable
9. resolution deadline
10. ambiguity and unresolved handling
11. substantive content hash

The contract must permit explicit unresolved states. It must not silently coerce missing evidence into a resolved negative outcome.

### 3. Point in time evidence snapshot contract

Implement a contract representing or binding at least:

1. snapshot ID
2. information cutoff
3. snapshot close or creation time
4. deterministic member list
5. source identity for each member
6. observation, publication, availability, retrieval, or vintage time fields required by the member type
7. transformation or definition version where derived
8. content identity or source reference
9. trusted upstream root or independent authentication reference where needed
10. snapshot root

The validator must enforce member admissibility against the information cutoff under explicit timestamp semantics.

Do not guess availability when it is unknown. Unknown admissibility must fail issuance validation or remain an explicitly ineligible state under the accepted contract.

### 4. Forecast method contract

Implement a versioned method definition representing at least:

1. method ID and version
2. method family
3. compatible forecast classes
4. required inputs
5. implementation identity
6. fitted state reference where applicable
7. model identity where applicable
8. prompt or configuration identity where applicable
9. retrieval and tool policy
10. randomness and seed policy where applicable
11. probability and post processing semantics
12. limitations
13. substantive content hash

A method that requires fitted state must fail validation when that state is absent.

### 5. Forecast run attempt contract

Implement a record representing at least:

1. attempt ID
2. method identity
3. start and end timestamps
4. information cutoff
5. input snapshot references
6. run status
7. failure or abort reason where applicable
8. output reference if successful
9. configuration or seed where applicable
10. tool or evidence log reference where applicable

Supported terminal states must include:

1. `issued`
2. `failed_pre_issue`
3. `aborted_pre_issue`
4. `invalid_pre_issue`

Retries must require distinct attempt IDs.

### 6. Issued forecast contract

Implement the formal immutable issuance record representing at least:

1. forecast ID
2. issued timestamp
3. information cutoff
4. forecast class
5. target ID, version, and hash
6. horizon start and end
7. geography or entity scope where applicable
8. probability or categorical distribution
9. method ID, version, and hash
10. model or configuration identity where applicable
11. evidence and feature snapshot roots as applicable
12. resolution rule ID, version, and hash
13. code identity where consequential
14. run attempt reference
15. substantive content hash
16. lifecycle status

Validation must enforce:

1. `information_cutoff <= issued_at`
2. valid probability semantics
3. target and horizon compatibility
4. exact trusted target, method, resolution, and snapshot bindings
5. successful admissibility verification of the point in time snapshot
6. valid issued run attempt reference
7. prohibition of backdated issuance under the accepted issuance API or verifier boundary
8. deterministic substantive content identity
9. failure on substantive mutation

### 7. Forecast correction contract

Implement append only correction semantics representing at least:

1. correction ID
2. original forecast ID
3. correction timestamp
4. correction type
5. reason
6. affected fields
7. authority or reviewer reference where applicable
8. linked corrected metadata or replacement forecast where applicable
9. future scoring consequence classification
10. substantive content hash

The original issuance must remain unchanged.

Probability, target, or horizon changes cannot be accepted as ordinary metadata correction.

## Trusted root rule

A scientific object cannot authenticate its own upstream semantics merely by repeating a hash inside itself.

The verifier must accept independently supplied trusted definitions or roots for consequential bindings where circular self authentication would otherwise occur.

At minimum, issuance verification must compare the forecast bound target, resolution rule, method, and evidence snapshot identities against independently supplied or independently authenticated objects.

A test must demonstrate that modifying an upstream object and resealing downstream hashes does not pass when the trusted external root remains unchanged.

## Canonicalization and hashing

Use one deterministic repository documented canonical JSON representation for new forecast trust objects.

Requirements:

1. UTF 8
2. deterministic key ordering
3. deterministic separators and newline policy
4. no wall clock values injected by canonicalization
5. no random identifiers generated inside validation
6. substantive content hash excludes its own hash field
7. hash coverage is explicit per object type
8. repeated validation of identical bytes and trusted inputs produces identical results

Use SHA 256 unless an existing repository invariant requires another accepted digest.

Do not create a new cryptographic protocol.

## Validation architecture

Prefer small standard library Python modules consistent with the current repository.

Separate:

1. structural contract validation
2. canonicalization and content identity
3. cross object referential integrity
4. point in time admissibility
5. issuance verification
6. correction verification

Unknown required semantics must fail closed.

Validation errors should be machine readable enough for future audit tooling.

## Fixed output footprint

Create exactly these new files unless a concrete repository constraint requires a documented deviation:

1. `schemas/forecast-target.v1.schema.json`
2. `schemas/forecast-resolution-rule.v1.schema.json`
3. `schemas/forecast-method.v1.schema.json`
4. `schemas/forecast-evidence-snapshot.v1.schema.json`
5. `schemas/forecast-run-attempt.v1.schema.json`
6. `schemas/forecast-issuance.v1.schema.json`
7. `schemas/forecast-correction.v1.schema.json`
8. `scripts/forecast_ledger_contracts.py`
9. `scripts/verify_forecast_ledger.py`
10. `scripts/test_forecast_ledger_contracts.py`
11. `docs/FORECAST_LEDGER_CORE.md`

Existing shared contract helpers may be changed only when necessary for clean reuse and only with regression tests proving existing contracts remain unchanged in meaning.

Do not add a database, web server, workflow, frontend, or live model integration.

## Required adversarial tests

At minimum test rejection of:

1. duplicate target, method, attempt, forecast, or correction IDs within a verification package where uniqueness is required
2. invalid target version or changed target semantic hash
3. incompatible target and resolution rule
4. probability outside the allowed range
5. categorical probabilities that do not satisfy the declared normalization tolerance
6. invalid horizon
7. `information_cutoff > issued_at`
8. evidence member available after information cutoff
9. unknown evidence availability required for issuance admissibility
10. altered evidence snapshot membership
11. changed method version or fitted state
12. missing required fitted state
13. run attempt with a non issued terminal state referenced by an issuance
14. reused attempt ID for a retry
15. substantive forecast mutation after issuance
16. correction timestamp before or equal to issuance when later time is required
17. probability, target, or horizon mutation disguised as metadata correction
18. unknown referenced object
19. independently trusted root mismatch
20. resealed altered upstream object attempting circular self authentication
21. nondeterministic canonical output
22. unsupported required semantic value

Map the applicable tests to the accepted FCT, PTI, RES, EVAL, and AI safeguard identifiers where those mappings already exist. Do not invent a new safeguard meaning merely to obtain a complete identifier list.

## Positive fixtures

Tests may create synthetic fixtures under temporary directories.

Synthetic fixtures must be clearly labelled and must never be written into a real prospective ledger or presented as issued forecasts.

No genuine Forecast Ledger Genesis record is created by this task.

## Preservation requirements

Before and after implementation, verify that this task does not modify:

1. frozen GKG samples
2. GKG evidence artifacts
3. accepted human review artifacts
4. accepted historical study outputs
5. existing scientific invariants

Existing offline tests must continue to pass.

## Acceptance criteria

Accept only if:

1. all seven new contracts are versioned and documented
2. deterministic canonicalization and SHA 256 identities are implemented
3. point in time admissibility fails closed
4. cross object trusted binding is verified independently
5. issuance mutation is detectable
6. corrections are append only in semantics
7. all required positive and adversarial tests pass
8. the complete existing offline test suite passes
9. repeated runs on identical synthetic fixtures are byte and result deterministic
10. no real forecast or network action occurs
11. no existing historical evidence is modified
12. `docs/FORECAST_LEDGER_CORE.md` documents trust boundaries, object relationships, validation entry points, and the exact boundary before Genesis

## Stop conditions

Stop and escalate to Sol High if:

1. implementation requires choosing new target or resolution semantics not already constrained by accepted documents
2. timestamp semantics are insufficient to determine point in time admissibility
3. trusted root validation would be circular
4. content hash coverage is ambiguous for a scientifically consequential field
5. correction semantics could permit silent forecast rewriting
6. current accepted forecast architecture and schema requirements materially conflict
7. a requirement would make retrospective synthetic fixtures indistinguishable from genuine prospective issuance
8. compatibility with existing contract infrastructure would require weakening existing validation
9. implementation would need network access, paid infrastructure, or a production database
10. any accepted historical scientific artifact would need reinterpretation or modification

Otherwise complete with Terra High.

## Explicitly out of scope

This task does not authorize:

1. Forecast Ledger Genesis
2. real forecast issuance
3. choosing the first target family
4. external LLM calls
5. market data subscriptions
6. outcome resolution
7. scoring or calibration
8. failure corpus records
9. external model leaderboards
10. GKG recovery
11. new source family integration
12. frontend or API development
13. scheduled production workflows
14. multi user authentication

## After this task

After acceptance, the next governance task is an adversarial Trust Core review followed by a separate Forecast Ledger Genesis protocol design.

Genesis should select a deliberately small set of objectively resolvable, low cost targets and transparent baselines. The first genuine prospective issuance occurs only after that protocol is accepted.
