# Review Surface Manifest To Retrieval Preflight Bridge

## Recurrence Signal

A human-facing review surface already exists, but downstream retrieval and mapping work still needs a machine-readable bridge so later consumers do not reopen markdown or re-derive the same per-image review state.

## Current Manual Handling

Use the review-surface manifest as the only machine truth, then project it into:

- one review decision seed
- one retrieval input seed
- one mapping review seed
- one preflight summary manifest and report

Keep retrieval and mapping execution out of scope.

## Promotion Target

Reusable bridge from review manifest to downstream preflight seeds.

## Promotion Trigger

Another corpus or bounded batch closes on a review surface and the next lane needs human decision capture plus retrieval-ready placeholders without touching upstream bundle truth.

## Current Proven Example

2026-03-30 `phase2` corpus review surface was bridged into:

- `phase2_caption_review_decision_seed_at2026_03_30.jsonl`
- `phase2_retrieval_input_seed_at2026_03_30.jsonl`
- `phase2_mapping_review_seed_at2026_03_30.jsonl`
- `phase2_caption_review_to_retrieval_preflight_at2026_03_30.json`

