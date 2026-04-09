# Repeated Task: GPT Direct Image Verification For Reviewed Component Edge Cases

## Recurrence Signal

A reviewed component branch stays stuck in `pending_review` because OCR-proxy evidence is too coarse, but the actual image pair still needs a bounded semantic tie-break without human pixel review.

## Current Proven Example

- source image: `image10.png`
- full-image OCR proxy reported zero extraneous tokens
- reviewed crop OCR proxy reported two extra tokens and therefore failed the strict proxy comparator
- direct GPT image verification compared the full image and reviewed crop side-by-side and promoted the crop with `high` confidence because the full table was preserved and non-table noise was removed

## Repeatable Pattern

1. keep the deterministic OCR/proxy evidence as the first pass
2. escalate only the unresolved edge case to direct GPT image verification
3. require machine-readable JSON with explicit decision, winner surface, confidence, and rationale
4. apply the verdict as a bounded promotion adapter instead of regenerating the arm
5. preserve the original proxy evidence alongside the GPT tie-break result

## Promotion Candidate

- reusable direct-verification runner or escalation checklist for reviewed component edge cases

## Why It Matters

This pattern prevents:

- over-trusting brittle OCR proxy comparisons
- forcing a waiver on a visually cleaner reviewed crop
- confusing qualitative comparison winners with default baseline replacement
