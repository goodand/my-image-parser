# Repeated Issue: True Small-Batch Bundle Absent For Nonregenerative Eval

## Symptom

An evaluation consumer can run on a frozen bundle, but the workspace does not yet contain a true multi-image bundle that satisfies the requested arm set without regenerating upstream artifacts.

## Current Proven Example

- `phase1` caption four-mode auto-eval lane was implemented
- only the `phase0` single-image eval bundle existed
- the consumer therefore ran as a `1-image template consumer`
- no true `phase1 small-batch` bundle existed under the allowed nonregenerative scope

## Why This Is Dangerous

- it can make a template-based closure look more general than it is
- it can blur the difference between `consumer-ready` and `batch-ready`
- it encourages accidental regeneration pressure on already-frozen deterministic lanes

## Guardrail

When the shared four-arm closure set has size `1`:

- allow the consumer lane to close on the template
- emit an explicit waiver that true small-batch coverage is not yet available
- keep the scoring contract frozen
- wait for more shared closed images before claiming multi-image batch readiness

## Linked Pattern

- `True Small-Batch Four-Mode Bundle Assembly From Shared Closure Set`
