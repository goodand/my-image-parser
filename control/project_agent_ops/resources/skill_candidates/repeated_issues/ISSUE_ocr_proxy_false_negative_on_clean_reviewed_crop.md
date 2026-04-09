# Repeated Issue: OCR Proxy False Negative On Clean Reviewed Crop

## Symptom

A reviewed crop is visually cleaner than the full image, but the OCR proxy comparator still says it is not better because the baseline already has zero proxy extras or because the crop introduces a few harmless OCR artifacts.

## Current Proven Example

- source image: `image10.png`
- full-image OCR proxy had `full_image_extra_token_count = 0`
- reviewed crop OCR proxy had `reviewed_component_extra_token_count = 2`
- the strict proxy rule therefore returned `reviewed_component_better_for_caption_input = false`
- direct GPT image verification still promoted the reviewed crop with `high` confidence because the crop preserved the full table and removed irrelevant slide noise

## Why This Is Dangerous

- it can incorrectly block a good reviewed branch
- it can treat OCR noise as stronger evidence than visible table completeness
- it can delay true small-batch bundle assembly even when the image pair is semantically clear

## Guardrail

When a reviewed crop remains visually complete but the OCR proxy says `false` for a near-tie case:

- keep the proxy result as evidence
- escalate the edge case to direct GPT image verification
- only promote the branch if the direct verification explicitly prefers the reviewed crop

## Linked Pattern

- `GPT Direct Image Verification For Reviewed Component Edge Cases`
