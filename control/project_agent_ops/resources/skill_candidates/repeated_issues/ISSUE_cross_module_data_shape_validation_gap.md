# Repeated Issue: Cross-Module Data Shape Validation Gap

## Symptom

Two modules share a data shape (one produces, one consumes), but the consumer validates only the outer container and accepts the inner payload as `any object`. Invalid inner payloads are persisted and only discovered later during downstream processing.

## Current Proven Example

- `feedback-ledger.js` `validateFeedbackEntry()` checked `decision_patch` with `isObject()` only
- `decision-contract.js` defined strict field rules for human-supplied decision fields
- an invalid patch (`{ image_id: 'image99' }`) would be accepted by the ledger, persisted to disk, and only fail when a downstream consumer tried to apply it
- fixed 2026-04-07 by adding `validateDecisionPatch()` to `decision-contract.js` and calling it inside `validateFeedbackEntry()`

## Why This Is Dangerous

- invalid data is persisted before validation catches it
- the error surfaces far from the point of entry, making diagnosis hard
- the producer module gives a false sense of safety ("it validated successfully")

## Guardrail

When module A produces a payload that embeds a shape owned by module B:

- module A must import module B's validator and apply it at entry time
- if module B's validator is too heavy, at minimum validate the field set (no unknown keys) and type constraints
- add a cross-module validation test: construct an invalid inner payload and confirm it is rejected before persistence

## Escalation Trigger

Another module accepts a nested payload from an external shape owner without importing the owner's validator.
