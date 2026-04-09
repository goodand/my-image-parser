# Repeated Issue: Repo-Local Semantic Judge Harness Absent

## Symptom

A bounded comparison surface is implemented and comparison-ready, but the repo does not yet expose a first-party semantic judge runner for the same scope.

## Current Proven Example

- `image11.png` `4-mode` caption comparison
- comparison runner and frozen eval bundle exist
- semantic judge execution does not
- the qualitative lane therefore closes through `waiver + manual summary`

## Why This Is Dangerous

- it can make comparison-ready surfaces look less reusable than they are
- it can tempt ad hoc judging without a stable frozen input
- it can blur the distinction between deterministic comparison and semantic evaluation

## Guardrail

When no repo-local judge harness exists:

- emit a frozen eval bundle
- write an explicit waiver
- write a qualitative summary
- do not mutate shared registries or promotion state

## Linked Pattern

- `Frozen Eval Bundle Generation For Deferred Judge Lane`
