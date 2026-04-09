# Repeated Task: True Small-Batch Four-Mode Bundle Assembly From Shared Closure Set

## Recurrence Signal

A consumer lane is ready to score or compare a four-arm experiment, but only a subset of images have all required arms closed. The workspace needs a true small-batch bundle assembled only from the shared closure set.

## Current Proven Example

- `phase1` auto-eval consumer was ready
- only `image11.png` had all four arm surfaces closed
- the consumer therefore ran on a `1-image template bundle`, not a true multi-image batch

## Repeatable Pattern

1. inspect the available comparison-ready arm manifests
2. intersect them on shared image ids
3. assemble a bounded batch only from images with all required arms closed
4. if the shared set has size `1`, emit a waiver instead of overstating small-batch coverage
5. rerun the existing consumer unchanged once the shared set grows

## Promotion Candidate

- reusable shared-closure-set bundle assembler for multi-arm experiments

## Why It Matters

This avoids:

- treating a single-image template as if it were a batch-generalized result
- regenerating arms just to satisfy an evaluation consumer
- losing parity between deterministic readiness and downstream consumer claims
