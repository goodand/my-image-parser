# Repeated Issue: Metadata-Only Decision Form Masks Missing Candidate Comparison

## Symptom

A review surface shows rich decision metadata such as default arm, leading arm, or promotion state, and that makes the slide look semantically evaluation-ready even when the underlying candidate-text comparison is absent or unavailable for the current item.

## Current Proven Example (2026-04-09)

The Steward response for `decision-slides` explicitly rejected `decision metadata form only` as sufficient UX. The evaluator had to compare actual arm-by-arm caption and alt-text payloads inside the surface, not infer judgment from labels such as `active default` or `comparison winner`.

## Later Session Extension (2026-04-09)

The same issue reappeared one layer deeper after candidate comparison support landed:

1. the first-10 bootstrap session carried session-local bundles
2. `image1` bundle reported `availability = excluded` with `candidate_arms = []`
3. `image6` bundle reported `availability = missing_source_record` with `candidate_arms = []`
4. but the shared `decision-seed.jsonl` still gave `image1`-`image6` generic metadata such as:
   - `active_default_arm = full_image_baseline`
   - `comparison_winner = full_image_ocr_context_rerun`
5. the UI therefore looked like a comparison-ready review form even though those slides had no comparison-ready candidate set

This was patched by gating the context and decision form on `candidate_bundle.availability`, replacing misleading comparison metadata with availability/reason fields, and hiding source-arm controls when the bundle is not `ready`.

## Later Session Extension II (2026-04-09)

After non-ready slide gating and candidate comparison support landed, the same issue persisted at the evaluator-flow layer:

1. the surface technically contained image preview, candidate comparison, and save behavior
2. but the default reading path still pulled the operator toward system metadata such as session state, leading arm, and advanced review fields
3. the operator had to ask where the actual caption-comparison body was and where save output was written
4. the UX then had to be cut again around the real evaluator task:
   - top: image stage
   - below: arm-by-arm candidate caption cards
   - one primary question
   - problem note
   - advanced metadata folded away
   - save-target explanation clarified as `decision-seed.jsonl` + `feedback-ledger.json` in the session directory, not the source markdown

This shows that `candidate comparison exists somewhere` is still weaker than `the operator is naturally reading and answering the evaluation question first`.

## Why This Matters

- reviewers can be pushed toward false decisions on slides that are not actually comparable
- metadata labels can outlive the real candidate state and quietly contaminate the UX
- once the operator trusts the form, missing comparison payloads become less obvious

## Guardrail

If `candidate_bundle.availability !== "ready"`:

- never render `baseline arm`, `comparison winner`, or equivalent comparison outcome labels as if they were actionable
- never render source-arm approval controls as if a bounded choice is available
- render only:
  - comparison availability
  - comparison reason
  - defer/exclusion guidance

If `candidate_bundle.availability === "ready"`:

- show candidate captions before system metadata
- keep the primary task as one question with bounded choices
- fold debug or session-state metadata into an advanced panel
- make the persistence target explicit if the operator can reasonably assume the source markdown is being edited directly

## Escalation Trigger

Another review slide has no comparison-ready candidate bundle, but the UI still renders leading-arm metadata or source-arm approval controls that imply a valid bounded choice exists.
