# Corpus Review Decision Capture

## Purpose

Define the machine-readable bridge between the existing human-facing corpus review surface and the downstream retrieval or mapping preflight lanes.

This capture surface exists so that a human reviewer can compare explicit arm-by-arm candidate text inside the evaluation surface, make a bounded caption decision, and write the result once in a structured row that later consumers can re-read without reopening external comparison bundles.

## Scope

This spec applies to:

- the active `phase2` corpus review surface
- one decision row per reviewed image
- caption approval and retrieval-entry preflight only

This spec does not change:

- arm generation
- corpus bundle contents
- retrieval execution
- mapping finalization
- master-plan wording

## Canonical Inputs

- review surface manifest:
  - [phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json](../../manifests/phase2_caption_four_mode_corpus_review_surface_at2026_03_30.json)
- review markdown:
  - [REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md](../../reports/REVIEW_phase2_caption_four_mode_corpus_review-at2026-03-30-22-45.md)
- frozen candidate bundle artifacts:
  - per-image bundle JSON carried through the review-surface session artifact contract
- promotion policy:
  - [SPEC_caption_arm_promotion_policy.md](./SPEC_caption_arm_promotion_policy.md)
- master plan vocabulary:
  - [MASTER_PLAN_presentation_image_pipeline.md](../../master_plans/MASTER_PLAN_presentation_image_pipeline.md)

## Design Rule

The contract captures exactly one `human caption decision row` per image.

The row must be self-contained enough that:

- Session A outputs can map into it directly from the review surface
- a human can fill it after reading the in-surface candidate comparison, with review markdown treated as supporting context
- Session B can read it for retrieval or mapping preflight without reopening the full comparison workflow

## Row Lifecycle

1. A seed row is generated from the review surface.
2. Machine-prefilled fields remain stable unless the review surface itself changes.
3. The reviewer fills the human decision fields.
4. Downstream consumers ingest only rows that are safe for their lane.

The canonical seed JSONL assumes one active writer at a time.

If multiple reviewers are needed, split owned image ids ahead of time or use reviewer-local working copies and merge them back into the canonical seed before ingestion.

## Machine-Prefilled Fields

These fields are copied from the review surface and should not be edited during ordinary review:

- `image_id`
- `source_image_path`
- `review_surface_path`
- `review_markdown_path`
- `bundle_path`
- `active_default_arm`
- `comparison_winner`
- `comparison_winner_promotion_state`
- `baseline_retained`
- `review_priority_label`
- `pending_context_review_arms`

The `bundle_path` must resolve to an explicit session-local candidate bundle artifact that carries per-arm caption and alt-text payloads for the current image.

## Human Decision Fields

These fields are expected to be filled during review:

- `selected_caption_arm`
- `selected_caption_promotion_state`
- `caption_decision`
- `caption_edit_required`
- `approved_caption`
- `approved_alt_text`
- `use_for_retrieval`
- `mapping_review_required`
- `outlier_candidate`
- `review_status`
- `reviewer_id`
- `reviewed_at`
- `decision_rationale`
- `retrieval_block_reason`
- `outlier_reason`
- `reviewer_notes`

## Field Semantics

### Core Selection

- `selected_caption_arm`
  - Which caption arm the reviewer chose as the human-approved source arm.
  - May be `null` only while `review_status` is `pending` or `deferred`.
  - If no existing arm text is good enough, the reviewer may approve a bounded LLM-assisted rewrite and record it as `llm_edited_caption`.

- `selected_caption_promotion_state`
  - Promotion state of the selected arm at the moment of review.
  - This is intentionally separate from the machine-prefilled `comparison_winner_promotion_state`.

- `caption_decision`
  - Human decision about how the final caption was chosen.
  - Supported values:
    - `select_active_default`
    - `select_comparison_winner`
    - `select_other_arm`
    - `approve_edited_caption`
    - `defer`
    - `exclude_from_retrieval`

### Final Text

- `approved_caption`
  - Final caption text that downstream retrieval should use if retrieval is allowed.
  - A completed review row must carry this field, even when the selected arm text is unchanged.

- `approved_alt_text`
  - Required final alt text for every completed row.
  - This stage now treats alt text as part of the formal experiment output, not as an optional follow-up artifact.

- `caption_edit_required`
  - Whether the final approved text came from an edit path instead of approving the selected arm text as-is.
  - In the current policy, edited rows should come from a bounded LLM-assisted rewrite path rather than direct freehand rewriting.

### Retrieval Or Mapping Preflight

- `use_for_retrieval`
  - Whether the approved caption may feed retrieval input generation.

- `mapping_review_required`
  - Optional downstream hint.
  - This field is kept for preflight convenience, but it is not the primary gating field.
  - The primary gate is still `use_for_retrieval`.

- `outlier_candidate`
  - Whether the reviewer suspects the image may need downstream outlier handling.
  - This is only a preflight signal, not a final mapping decision.

### Review State

- `review_status`
  - Supported values:
    - `pending`
    - `completed`
    - `deferred`

- `reviewer_id`
  - Human or delegated reviewer identifier.

- `reviewed_at`
  - ISO-like decision timestamp written when review completes or is deferred.

## Cross-Field Rules

The contract consumer must apply these rules:

1. `review_status = completed` requires:
   - `selected_caption_arm`
   - `selected_caption_promotion_state`
   - `caption_decision`
   - `caption_edit_required`
   - `approved_caption`
   - `approved_alt_text`
   - `use_for_retrieval`
   - `reviewer_id`
   - `reviewed_at`

2. `caption_edit_required = true` requires:
   - non-empty `approved_caption`

3. `use_for_retrieval = true` requires:
   - `review_status = completed`
   - non-empty `approved_caption`

4. `use_for_retrieval = false` requires:
   - non-empty `retrieval_block_reason`

5. `outlier_candidate = true` requires:
   - non-empty `outlier_reason`

6. `caption_decision = defer` requires:
   - `review_status = deferred`
   - `use_for_retrieval = false`

7. `caption_decision = exclude_from_retrieval` requires:
   - `use_for_retrieval = false`

8. `selected_caption_arm = llm_edited_caption` requires:
   - `selected_caption_promotion_state = null`
   - `caption_edit_required = true`
   - `caption_decision = approve_edited_caption`

9. `caption_decision = approve_edited_caption` requires:
   - `selected_caption_arm = llm_edited_caption`

## Downstream Ingestion Rules

### Retrieval Preflight

Retrieval preflight may ingest only rows where:

- `review_status = completed`
- `use_for_retrieval = true`
- `approved_caption` is non-empty

### Mapping Preflight

Mapping preflight may ingest only rows where:

- retrieval preflight eligibility already holds
- `mapping_review_required` is either `true` or omitted

The bridge contract does not finalize mapping decisions.

## Non-Goals

- Do not regenerate any arm.
- Do not rewrite any per-image or corpus bundle.
- Do not execute retrieval.
- Do not finalize mapping.
- Do not rewrite the master plan from this spec.

## Operational Result

The in-surface candidate comparison becomes the primary human evaluation body for this phase.

The review markdown remains supporting context, not the canonical comparison payload.

This decision-capture contract becomes the machine-readable handoff surface between:

- corpus review
- approved caption capture
- retrieval or mapping preflight
