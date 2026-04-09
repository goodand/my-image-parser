# Repeated Task Candidate: Shared Deterministic Image Processing Core Extraction

## Why This Repeats

When the same deterministic image-processing step is needed by more than one workspace surface, copying the logic into each script creates drift quickly.

Recent examples in this workspace:

- alpha connected-components needed by the object-isolation worker
- the same alpha split needed again by the component split + OCR review builder

## Current Manual Handling

1. identify duplicated deterministic logic in scripts or skills
2. extract the core routine into a workspace-level library module
3. keep thin entrypoints for each workflow surface
4. add a service/config layer when the same core needs different orchestrations
5. rerun both unit-level and live smoke checks after the extraction

## Current Workspace Surface

- shared alpha module: `scripts/alpha_component_lib.py`
- service/config wrapper: `scripts/component_split_ocr_lib.py`
- consumer surfaces:
  - `skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py`
  - `scripts/build_component_split_ocr_report.py`

## Promotion Target

- reusable refactor checklist for deterministic image-processing logic
- possible future helper skill for extracting shared local processing cores before adding new workflow scripts

## Promotion Trigger

Promote this pattern if another deterministic local step is reused across:

- caption preparation
- OCR packaging
- component split review
- object-isolation correction
