# Phase 0 Isolated-Component Caption Arm Waiver

## Purpose

Decide whether the reviewed isolated-component caption arm should be promoted into the current core comparison set for `image11.png`.

## Evidence Reviewed

- object isolation smoke:
  - `control/project_domain/resources/reports/REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md`
- target image:
  - `control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- reviewed component-split surface pattern:
  - `control/project_domain/archive/component_split_ocr/02_1/image11/COMPONENT_SPLIT_OCR_REPORT.md`

## Findings

### 1. The current semantic selection path is not reliable enough on the target table image.

From the bounded ImageSorcery smoke on the real target image:

- `find(description="table")` returned `found = false`
- fallback `detect` selected one small cell fragment rather than the full table

### 2. Full-image OCR recovered materially better text evidence than crop or isolation.

On `image11.png` in the existing smoke:

- full-image OCR annotations: `18`
- crop OCR annotations: `1`
- isolated OCR annotations: `1`

The current evidence therefore favors the full original image as the caption input surface.

### 3. Reviewed component surfaces on similar table-like material still look fragment-heavy.

The existing reviewed component report shows:

- `alpha_component_count = 3`
- one weak-text component
- two no-text components

This is supporting evidence that raw component extraction currently over-fragments table-like assets instead of producing a clearly superior caption surface.

## Waiver Decision

Waive the isolated-component caption arm for the current core 4-mode comparison.

Status:

- `comparison_ready = false`
- `waiver_type = explicit`
- `scope = current phase0 bounded comparison set`

## Reason

The arm fails the bounded requirement:

- it does not currently provide a reviewed isolated component that is better than the original full image for captioning on the target image

Promoting it now would violate the current operating rule:

- object isolation remains a reviewed branch only
- it must not be promoted into the unattended default path

## Re-entry Gate

Re-open this arm only if at least one of the following becomes true:

1. a reviewed component surface on the target image preserves more table text than the full-image OCR baseline
2. component selection becomes semantically reliable enough to isolate the full intended object rather than a fragment
3. a bounded isolated rerun shows better caption quality than the full-image baseline on a shared source image

## Conclusion

For the current comparison round, the isolated-component caption arm is intentionally closed by waiver, not by implementation.

