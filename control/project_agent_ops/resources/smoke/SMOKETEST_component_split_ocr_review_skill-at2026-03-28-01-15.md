# Smoke Test: Component Split OCR Review Skill

## Command

```bash
/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/vendor/mcp/imagesorcery-mcp/.venv/bin/python -B \
  skills/component-split-ocr-review/scripts/build_component_split_ocr_report.py \
  --image-path control/project_domain/resources/pptx_jobs/02_1/media/image11.png
```

## Expected

- skill-local wrapper should resolve the shared root builder
- default output root should stay at `control/project_domain/archive/component_split_ocr/`
- one markdown report, one JSON report, alpha component crops, and per-component OCR JSON files should exist

## Observed

- wrapper `--help`: `0`
- live smoke exit: `0`
- image_id: `02_1:image11.png`
- alpha_component_count: `3`
- output_dir: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/component_split_ocr/02_1/image11`
- component 01:
  - pixel_count: `10844`
  - ocr_status: `weak_text`
  - ocr_annotation_count: `1`
  - ocr_text_excerpt: `÷|ll`
- components 02 and 03:
  - `ocr_status = no_text`
  - `ocr_annotation_count = 0`

## Output Paths

- markdown report: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/component_split_ocr/02_1/image11/COMPONENT_SPLIT_OCR_REPORT.md`
- json report: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/archive/component_split_ocr/02_1/image11/COMPONENT_SPLIT_OCR_REPORT.json`
- skill: `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/component-split-ocr-review`

## Interpretation

- the repo-specific skill wrapper works and reuses the shared root builder correctly
- the skill is ready for single-image reviewed component inspection
- this does not change the reviewed-only boundary for semantic promotion
