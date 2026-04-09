# Caption Runner Context Injection Smoke

## Purpose

Verify that the local OpenAI caption runner can consume the new full-image standalone OCR context-package artifacts directly and preserve both:

- `source_context` from the PPT extraction manifest
- `context_package` from the reviewed OCR baseline artifact

## Script Surface

- runner:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/caption_images_openai.py`
- runner library:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/caption_runner_lib.py`
- context-package builder:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/build_full_image_ocr_context_package.py`
- fake-client test:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/test_caption_runner_context_injection.py`

## Static Verification

- command:
  - `python3 scripts/test_caption_runner_context_injection.py`
- result:
  - `OK`

## Live Smoke Input

- image:
  - `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png`
- context package:
  - `/private/tmp/full-image-ocr-context-smoke-unsandboxed/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json`

## Live Command

```bash
python3 scripts/caption_images_openai.py \
  --image control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image11.png \
  --context-package-json /private/tmp/full-image-ocr-context-smoke-unsandboxed/01_full_presentation_2026-03-17/image11/CONTEXT_PACKAGE.json \
  --output /tmp/context_injected_caption_smoke_v2.json
```

## Observed Result

- `processed_count = 1`
- `status_counts.completed = 1`
- top-level `prompt_version = openai-gpt-4.1-caption-context-v1`
- record `source_context.file = image11.png`
- record `source_context.slide_usages = [{slide: 24, occurrence: 1}]`
- record `context_package.image_id = 01_full_presentation_2026-03-17:image11.png`

Observed caption:

- `A table compares the performance of Two-Phase Hyde-PC on 70Q and 65Q datasets across three metrics: DH@10, MRR, and CR@10, showing improvements (Delta values) for 65Q.`

Observed alt text:

- `Table with metrics DH@10, MRR, CR@10 for Two-Phase Hyde-PC on 70Q and 65Q, including delta values.`

Observed visible text included:

- `Two-Phase Hyde-PC (65Q, 오류 5건 제외)`
- `Metric 70Q 65Q Delta`
- `DH@10 0.757 0.815 +0.058`
- `MRR 0.622 0.670 +0.048`
- `CR@10 0.514 0.554 +0.040`

## Conclusion

- direct context-package injection is operational
- the runner preserves the reviewed OCR baseline artifact on the ledger row
- the runner also restores PPT extraction manifest context for single-image runs inside `runs/pptx_jobs/<dataset>/media/`
- prompt-safe sanitization is in place so review-only summary fields can be consumed without blindly re-injecting prior baseline caption phrasing
