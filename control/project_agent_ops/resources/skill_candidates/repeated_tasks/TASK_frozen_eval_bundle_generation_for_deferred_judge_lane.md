# Repeated Task: Frozen Eval Bundle Generation For Deferred Judge Lane

## Recurrence Signal

A multi-arm comparison is mechanically ready, but the repo does not yet expose a semantic judge harness. The workspace still needs a stable downstream-consumable bundle so the qualitative lane can close without regenerating ledgers later.

## Current Proven Example

- bounded `4-mode` caption comparison on `image11.png`
- comparison runner produced:
  - judge input manifest
  - frozen eval bundle
- the semantic judge lane closed by waiver, not by execution

## Repeatable Pattern

1. reuse the existing ledger-backed comparison runner
2. emit a read-only judge input surface
3. emit a frozen eval bundle for later consumption
4. close the current lane with a waiver plus manual qualitative summary
5. keep the default baseline decision separate from the comparison winner

## Promotion Candidate

- reusable eval-bundle production helper for deferred judge overlays

## Why It Matters

This avoids:

- re-running prior arms just to feed a later judge lane
- conflating comparison readiness with local judge availability
- losing parity fields between deterministic and qualitative evaluation surfaces
