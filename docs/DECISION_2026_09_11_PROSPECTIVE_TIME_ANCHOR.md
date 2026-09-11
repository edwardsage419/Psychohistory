# Prospective Time Anchor Decision

Decision date: 2026-09-11

Status: ACCEPTED DESIGN DECISION

## Problem

An immutable local forecast object with an `issued_at` field and a content hash can prove content consistency relative to a known root. By itself it cannot prove that the object actually existed before an outcome became known.

That distinction is critical to Psychohistory because prospective history is a primary long term asset.

## Decision

Formal prospective issuance requires two separate properties:

1. substantive forecast immutability
2. independently verifiable evidence that the committed forecast content existed no later than an externally observed anchoring time

The Forecast Trust Core must therefore support an issuance anchor or receipt object separate from the forecast object.

The core contract remains provider neutral. Forecast Ledger Genesis must choose at least one accepted low cost external anchoring mechanism before the first genuine prospective issuance.

## Issuance anchor contract

A future anchor or receipt object should bind at minimum:

1. anchor receipt ID
2. anchor scheme and scheme version
3. forecast substantive content hash or a batch root containing it
4. external anchor reference or proof material
5. externally observed or independently derived anchor time semantics
6. verifier identity or verification method version where applicable
7. verification status
8. proof content identity
9. any delay or finality semantics relevant to interpreting the anchor time

The receipt must not silently change the forecast's own `issued_at` value. It provides independent evidence about when the forecast content was externally committed or observed.

## Trust rule

A timestamp written by the local process is metadata rather than independent proof of existence time.

A Git author or committer timestamp, local file modification time, generated UUID time component, or other operator controlled clock is insufficient as the sole prospective time anchor.

A digital signature authenticates a signer and content according to its scheme. It does not by itself establish an independently trusted wall clock time.

The accepted Genesis anchor mechanism must provide an external trust property strong enough to make retrospective backdating materially detectable.

## Batch anchoring

The architecture may permit multiple forecast hashes to be committed through one deterministic batch or Merkle style root when this reduces operating cost or network dependence.

Batch membership must itself be deterministic and auditable. A forecast cannot be inserted later into an already anchored batch without changing the committed root.

No new cryptographic construction should be invented when a standard content hash and an established external anchoring mechanism are sufficient.

## Delay and finality

Some external anchoring mechanisms may establish proof only after a delay.

The contract must distinguish:

1. local issuance time claimed by the forecast system
2. submission or publication time when independently observable
3. anchor confirmation or finality time

Future scientific claims must use the semantics actually supported by the chosen mechanism.

## Failure handling

If external anchoring fails after a local forecast run:

1. the failed anchoring attempt remains visible when required by the accepted issuance protocol
2. the forecast must not silently receive prospective status
3. retry semantics must be explicit
4. an outcome becoming known before valid anchoring prevents the record from receiving genuine prospective classification

A record may remain a research artifact with a different classification.

## Genesis requirement

Forecast Ledger Genesis is blocked until a separate protocol selects and tests at least one accepted external anchor mechanism under the near zero recurring cost constraint.

The selection should evaluate:

1. external independence from the operator
2. resistance to backdating
3. long term verifiability
4. cost
5. operational simplicity
6. service continuity risk
7. proof portability
8. batch support where useful
9. privacy implications
10. offline verification capability where possible

## Current task consequence

Forecast Trust Core v0.1 should add a provider neutral issuance anchor or receipt schema and deterministic validation for its binding to forecast content.

Synthetic anchor fixtures are allowed for tests and must be clearly incapable of granting real prospective status.

No real external anchor service is selected or contacted by the current implementation task.
