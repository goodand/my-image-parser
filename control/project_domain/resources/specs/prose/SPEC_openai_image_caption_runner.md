# OpenAI Image Caption Runner

This workspace now includes a sequential OpenAI caption runner at:

- `scripts/caption_images_openai.py`

It processes one image at a time with the OpenAI Responses API and writes a JSON ledger under:

- `control/project_agent_ops/registry/jobs/image_caption_jobs/`

## Default behavior

- Model: `gpt-4.1`
- API key lookup order:
  - `OPEN_DATA_API_KEY`
  - `OPENAI_API_KEY`
- Input mode:
  - one image with `--image`
  - dataset JSONL with `--dataset-jsonl`
  - one directory with `--input-dir`
  - optional reviewed context package with `--context-package-json`
  - optional per-image context-package manifest with `--context-package-manifest-jsonl`
- Output fields per image:
  - `image_id`
  - `path`
  - `status`
  - `attempt_count`
  - `started_at`
  - `finished_at`
  - `caption`
  - `alt_text`
  - `structured_metadata`
  - `new_filename_candidate`
  - `context_package`
  - `api_response_id`
  - `usage`

## Sidecar artifacts

Alongside the main ledger, the runner also writes:

- `<job_stem>_execution_records.jsonl`
- `<job_stem>_evaluation_decisions.jsonl`
- `<job_stem>_responses/<image_id>.json`

The default evaluation decision sidecar is a lightweight orchestration artifact:

- `completed` -> `review_ready`
- `failed` or `unsupported_media_type` -> `error`
- `queued` or `running` -> `pending`

## Example commands

Single image:

```bash
python3 scripts/caption_images_openai.py \
  --image control/project_domain/resources/assets/added_screenshots/image5.png
```

Whole directory:

```bash
python3 scripts/caption_images_openai.py \
  --input-dir control/project_domain/resources/assets/added_screenshots
```

Single image with reviewed context package:

```bash
python3 scripts/caption_images_openai.py \
  --image control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png \
  --context-package-json control/project_domain/resources/context_packages/full_image_ocr_baseline/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json
```

Whole directory with a context-package manifest:

```bash
python3 scripts/caption_images_openai.py \
  --input-dir control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media \
  --context-package-manifest-jsonl control/project_domain/resources/manifests/phase0_full_image_ocr_context_package_manifest.jsonl
```

Cross-validation dataset JSONL:

```bash
python3 scripts/caption_images_openai.py \
  --dataset-jsonl control/project_domain/resources/cross_validation/02_1/openai_api/media_extract_dataset.jsonl \
  --output control/project_domain/resources/cross_validation/02_1/openai_api/gpt41_media_extract_job.json
```

Resume an existing ledger but retry failed rows:

```bash
python3 scripts/caption_images_openai.py \
  --input-dir control/project_domain/resources/assets/added_screenshots \
  --output control/project_agent_ops/registry/jobs/image_caption_jobs/my_job.json \
  --retry-failed
```

Force all rows to re-run:

```bash
python3 scripts/caption_images_openai.py \
  --input-dir control/project_domain/resources/assets/added_screenshots \
  --output control/project_agent_ops/registry/jobs/image_caption_jobs/my_job.json \
  --overwrite
```

## Notes

- The runner uses OpenAI structured JSON output and keeps the ledger plus sidecar orchestration artifacts updated after each image so interrupted runs can be resumed.
- Structured JSON alone is not treated as sufficient success. The runner now applies a local completeness guard and fails captions that remain semantically incomplete, such as truncated sentence endings or incomplete API outputs.
- `manifest.json` in the same directory is auto-detected and copied into each record as `source_context` when present.
- for single-image or media-directory runs under `runs/pptx_jobs/<dataset>/media/`, the runner also checks the parent dataset directory for `manifest.json`
- reviewed context packages are mapped by `source_image_path`, then persisted on each ledger row as `context_package`
- prompt injection uses OCR excerpt and sanitized PPT-local summary only; prior baseline caption or alt-text phrasing from review-oriented fields must not be re-injected into the next generation prompt
- Unsupported image formats are marked as `unsupported_media_type` instead of crashing the whole batch.
- Long `alt_text` values are also checked for incomplete endings before a record is accepted as `completed`.
