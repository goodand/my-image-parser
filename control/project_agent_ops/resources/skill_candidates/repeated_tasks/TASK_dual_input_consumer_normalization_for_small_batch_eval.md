# Repeated Task: Dual-Input Consumer Normalization For Small-Batch Eval

## Recurrence Signal

A downstream comparison or auto-eval consumer should stay reusable even when canonical aggregate bundle freshness is uncertain, so it needs to accept either a ready aggregate bundle or a list of per-image frozen bundles.

## Current Proven Example

- `phase1` four-mode small-batch auto-eval lane initially faced aggregate truth drift
- the consumer was patched to accept both:
  - aggregate small-batch bundle input
  - per-image bundle list fallback
- canonical regeneration then closed on `image11`, `image7`, `image9` without depending on stale aggregate state

## Repeatable Pattern

1. inspect the downstream consumer and isolate where it assumes a single aggregate bundle shape
2. add an input normalizer that can expand aggregate bundle entries into per-image bundle paths
3. keep direct per-image bundle paths supported as a first-class fallback input
4. regenerate the downstream artifact using the current truth-source that is least drift-prone
5. record the actual consumed input mode so later readers can distinguish aggregate consumption from per-image fallback

## Promotion Candidate

- reusable input-normalization helper for small-batch consumers
- standard consumer contract requiring `actual_input_mode` and resolved bundle paths

## Why It Matters

This avoids:

- blocking the consumer on producer aggregate freshness
- silently reusing stale image members such as an old `image10` carry-over
- losing provenance about whether the lane consumed aggregate truth or per-image fallback truth
