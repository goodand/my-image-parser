# Repeated Task Candidate: Component Split Table And OCR Surface Generation

## Why This Repeats

When a transparently extracted image might contain multiple disconnected parts, the workspace often needs the same bounded artifact set:

- split the image into alpha components
- output a reviewable component table
- run OCR on each separated component

This is narrower than full object isolation and safer than automatic semantic selection.

## Current Manual Handling

1. run alpha connected-components on the source image
2. export one PNG per component
3. OCR each component image separately
4. write a markdown table plus JSON sidecar for review

## Current Workspace Surface

- builder: `scripts/build_component_split_ocr_report.py`
- library: `scripts/component_split_ocr_lib.py`
- shared alpha module: `scripts/alpha_component_lib.py`

## Promotion Target

- reusable review builder skill or standard pre-caption component packet

## Promotion Trigger

Promote this pattern if another phase0 or reviewed-isolation branch needs the same:

- disconnected-component split
- per-component OCR
- markdown review surface

## Current Promotion Status

- promoted into repo-local skill: `skills/component-split-ocr-review`
- root implementation remains shared under `scripts/build_component_split_ocr_report.py`
- skill-local wrapper exists to keep policy/defaults separate from the reusable core
