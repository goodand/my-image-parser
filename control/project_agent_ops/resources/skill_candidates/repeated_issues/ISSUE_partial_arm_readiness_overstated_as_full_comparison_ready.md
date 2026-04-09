# Repeated Issue: Partial Arm Readiness Overstated As Full Comparison Ready

## Symptom

One or more new arms become runnable and mechanically valid, but the workspace starts speaking as if the full planned comparison is ready even though another required arm is still blocked or waived.

## Current Proven Example

- `full_image_baseline`: ready
- `full_image_ocr_context_rerun`: ready
- `parser_table_enriched_rerun`: ready
- `reviewed_isolated_component_caption_arm`: waived

The workspace therefore supports a bounded `3-mode` comparison, not the intended `4-mode` comparison.

## Why This Is Dangerous

- it hides the remaining block
- it makes plan state look more complete than it is
- it can trigger premature evaluation or default-path discussion

## Guardrail

Always publish:

- ready arm count
- blocked arm list
- waiver status
- final yes/no readiness verdict

## Linked Pattern

- `Anchor-Ready But Full-Comparison-Incomplete Drift`

