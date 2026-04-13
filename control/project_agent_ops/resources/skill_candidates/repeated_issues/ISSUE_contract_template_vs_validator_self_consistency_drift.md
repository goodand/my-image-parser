# Repeated Issue: Contract Template Vs Validator Self-Consistency Drift

## Symptom

A factory or template function produces a default object that fails the same module's own validation rules. Tests pass only because test helpers silently patch the incompatible fields.

## Current Proven Example

- `decision-contract.js` `buildDecisionRowTemplate()` returned `use_for_retrieval: false` + `retrieval_block_reason: null`
- `validateDecisionRow()` required `retrieval_block_reason` to be non-empty whenever `use_for_retrieval === false`
- template output was always invalid by its own contract
- test helper `buildBaseRow()` silently injected `retrieval_block_reason: 'manual_lane'` to mask the problem
- fixed 2026-04-07 by adding `review_status !== 'pending'` guard to the retrieval_block_reason constraint

## Why This Is Dangerous

- the template is the first thing new consumers reach for
- the failure is invisible because tests override the template before validating
- downstream agents that call `buildDecisionRowTemplate()` directly will hit immediate validation errors

## Guardrail

When a module exports both a template/factory and a validator:

- add a self-consistency test: `validate(template())` must pass with zero overrides
- test helpers that override template fields should be audited for fields that mask template-level bugs
- any validation rule change should be followed by a template compatibility check

## Escalation Trigger

Another schema module introduces a factory or template whose output fails its own validator, or test helpers inject silent fixes that hide the mismatch.
