# Smoke Test: Component Split OCR Builder

## Command

```bash
<REPO_ROOT>/vendor/mcp/imagesorcery-mcp/.venv/bin/python -B \
  scripts/build_component_split_ocr_report.py \
  --image-path control/project_domain/resources/pptx_jobs/02_1/media/image11.png
```

## Expected

- split the source image into alpha-connected components
- write a markdown table and JSON sidecar under `control/project_domain/archive/component_split_ocr/`
- OCR each separated component and persist per-component OCR JSON

## Observed

- command exit: `0`
- image_id: `02_1:image11.png`
- alpha_component_count: `3`
- component 01:
  - pixel_count: `10844`
  - ocr_status: `weak_text`
  - ocr_annotation_count: `1`
  - ocr_text_excerpt: `÷|ll`
- components 02 and 03:
  - `ocr_status = no_text`
  - `ocr_annotation_count = 0`

## Output Paths

- markdown report: `control/project_domain/archive/component_split_ocr/02_1/image11/COMPONENT_SPLIT_OCR_REPORT.md`
- json report: `control/project_domain/archive/component_split_ocr/02_1/image11/COMPONENT_SPLIT_OCR_REPORT.json`
- component dir: `control/project_domain/archive/component_split_ocr/02_1/image11/alpha_components`
- component OCR dir: `control/project_domain/archive/component_split_ocr/02_1/image11/component_ocr`

## Interpretation

- the builder surface is working end-to-end
- this surface is useful for reviewed component-level triage
- OCR quality on tiny disconnected fragments remains limited, so downstream promotion still needs review
