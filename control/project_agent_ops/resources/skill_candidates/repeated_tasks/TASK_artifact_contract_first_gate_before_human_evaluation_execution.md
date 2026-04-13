# Repeated Task: Artifact-Contract-First Gate Before Human Evaluation Execution

## Recurrence Signal

A review surface already boots and can show images or forms, but the actual human evaluation depends on candidate payloads and session truth that are not yet fully encoded, audited, or ready for the intended run.

## Current Proven Example (2026-04-09)

The Steward response froze the next implementation order for `decision-slides` as:

1. artifact contract extension
2. candidate-text comparison section
3. label readability / operator clarity
4. actual 10-image evaluation run

This established the first gate: do not start the human run while the decision body still lives outside the artifact contract.

## Later Session Extension (2026-04-09)

After the contract extension and comparison section landed, a second gate was still required before telling the operator to evaluate:

1. reread the Steward response and decision index to freeze the acceptance bar
2. backfill or load the session-local candidate bundles for the current bootstrap session
3. audit bundle availability slide by slide
4. compare the bootstrap image set against the canonical comparison truth set
5. classify slides as `ready`, `excluded`, or `missing_source_record`
6. patch the UI so non-ready slides do not expose misleading comparison metadata or source-arm controls
7. only after that decide whether the current session is a valid run target or needs a refreshed ready-only set

## Later Session Extension II (2026-04-09)

One more gate was required even after bundle truth and non-ready slide gating were closed:

1. reread the Steward requirement note to freeze the operator task, not just the artifact contract
2. confirm that the primary evaluator action is `choose the best caption / reject all / request rewrite`
3. restructure the surface so the image and candidate cards are read before session/debug metadata
4. collapse comparison metadata, session summary, and bridge/debug material into advanced panels
5. localize or simplify visible operator copy so the question and choices are obvious in the live surface
6. verify the save boundary explicitly: writeback goes to `decision-seed.jsonl` and `feedback-ledger.json` inside the session directory, not back into the source review markdown

This means the preflight is not done when the contract becomes machine-readable; it is done when the evaluator can actually follow the intended judgment path without reading system metadata first.

## Repeatable Pattern

1. prove the open/bootstrap path
2. freeze contract-first requirements from the current control decision
3. emit or load explicit candidate artifacts
4. audit session truth against bundle availability and canonical comparison scope
5. gate non-ready slides in the operator surface
6. refit the visible evaluator flow so image + candidate captions are the primary reading path
7. make the persistence boundary explicit
8. start the human run only on a session that passes artifact, truth-set, and operator-flow checks

## Promotion Candidate

- reusable `evaluation session truth + operator-flow preflight` for human-review surfaces

## Why It Matters

This avoids:

- treating `session opens` as equivalent to `session is valid for execution`
- running a human evaluation on excluded or unresolved slides
- letting seed defaults or stale metadata outrun the real candidate bundle truth
