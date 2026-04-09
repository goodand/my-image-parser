# Repeated Issue: Aggregate Bundle Truth-Source Drift For Downstream Consumer

## Symptom

A decision-level readiness claim is correct, but the aggregate bundle consumed by a downstream lane still reflects an older image set or stale composition, so the consumer risks evaluating the wrong batch.

## Current Proven Example

- `phase1` small-batch readiness moved to `image11`, `image7`, `image9`
- the downstream auto-eval lane still had a stale aggregate-oriented truth story from an older bundle shape
- the consumer had to be regenerated from per-image bundles to guarantee the correct image set before aggregate freshness caught up

## Why This Is Dangerous

- it lets an apparently canonical aggregate file override fresher per-image truth
- it can keep excluded residual images such as `image10` alive in downstream evaluation
- it obscures whether a consumer result is based on aggregate truth or a fallback assembly

## Guardrail

When aggregate freshness is uncertain:

- verify the aggregate bundle image set before downstream consumption
- allow per-image frozen bundles as an explicit fallback truth-source
- write the resolved bundle paths and actual input mode into the consumer artifact
- keep promotion-state interpretation unchanged during the fallback

## Linked Pattern

- `Dual-Input Consumer Normalization For Small-Batch Eval`
