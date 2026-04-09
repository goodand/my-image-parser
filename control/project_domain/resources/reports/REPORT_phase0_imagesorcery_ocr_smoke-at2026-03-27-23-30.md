# Phase0 ImageSorcery + OCR Smoke Report

## Purpose

Validate whether the revised pre-caption path is good enough to proceed:

1. PPT-extracted image
2. ImageSorcery-based component isolation
3. OCR evidence
4. context package candidate

This smoke was intentionally bounded to two real PPT-extracted images from `01_full_presentation_2026-03-17`.

## Cases

1. `ppt1_image1_bar_chart`
   - source: `image1.png`
   - intended prompt: `bar chart`
   - baseline role: multi-chart component-isolation candidate
2. `ppt1_image11_table`
   - source: `image11.png`
   - intended prompt: `table`
   - baseline role: table OCR/context candidate

## Verification Surface

- script:
  - `scripts/run_phase0_imagesorcery_ocr_smoke.py`
- ImageSorcery runtime:
  - in-process FastMCP client against vendored `imagesorcery-mcp`
- OCR runtime:
  - direct standalone invocation of `vendor/mcp/macos-ocr-mcp/main.py`
- machine-readable summary:
  - [phase0_imagesorcery_ocr_smoke_summary_at2026_03_27.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase0_imagesorcery_ocr_smoke_summary_at2026_03_27.json)

## Findings

### 1. ImageSorcery detect works, but promptable `find` did not return usable semantic matches on these two real PPT assets.

- `bar chart` on `image1.png`: `found = false`
- `table` on `image11.png`: `found = false`

As a result, both cases fell back to generic `detect`.

### 2. Generic detect fallback produced semantically bad component boundaries.

- `image1.png`
  - fallback class: `darkness`
  - selected region: lower note / mostly empty black region
  - result: not a chart panel
- `image11.png`
  - fallback class: `cancer`
  - selected region: one small cell fragment
  - result: not the full table

This means the current fully automatic selection logic is not good enough for phase0 batch execution.

### 3. Standalone OCR on the full original image was better than OCR on cropped or isolated outputs in both smoke cases.

- `image1.png`
  - full-image OCR annotations: `29`
  - crop OCR annotations: `0`
  - isolated OCR annotations: `0`
- `image11.png`
  - full-image OCR annotations: `18`
  - crop OCR annotations: `1`
  - isolated OCR annotations: `1`

For `image11.png`, full-image OCR recovered metric headers and numeric values, while crop/isolation collapsed to only `650`.

### 4. A combined-runner drift exists.

Inside the combined smoke script, the OCR subprocess came back as fallback failure after ImageSorcery had already executed.
However, the same OCR target files succeeded when OCR was invoked directly in a separate standalone step.

Current interpretation:

- ImageSorcery stage: usable
- standalone OCR stage: usable
- one-process combined orchestration: not yet trustworthy

## Decision

- do **not** start phase0 batch object-isolation fanout yet
- do **not** treat isolated crops as the new default caption input yet
- keep full-image OCR as the immediate context source candidate
- require a reviewed or smarter component-selection layer before object-level reruns

## Recommended Next Step

### Near-term execution

1. Keep `full image + standalone OCR` as the next context package baseline.
2. Use object isolation only on manually approved or high-confidence candidates.
3. Treat the current `run_phase0_imagesorcery_ocr_smoke.py` as ImageSorcery-stage evidence, not final OCR truth.

### xhigh subagent usage

Recommended use of `gpt-5.4 xhigh` subagents is not bulk tool invocation. It is ambiguity resolution.

Best use cases:

- `selection triage`
  - inspect original image, detect fallback crop, and intended prompt
  - decide whether the crop actually matches the target semantic object
- `prompt rewrite`
  - propose better `find(description=...)` candidates such as `chart panel`, `metric table`, `dashboard panel`, `bar graph`
- `boundary audit`
  - decide whether to keep full image, crop, isolated image, or skip object isolation for that case
- `context package ranking`
  - choose whether `full-image OCR`, `crop OCR`, or no OCR should be passed into the later caption API call

Not recommended:

- assigning all 20 subagents directly to raw auto-isolation
- letting workers commit crop outputs without review gates

### Updated operational interpretation

The current evidence supports this ordering:

1. PPT-extracted image
2. full-image OCR baseline
3. optional reviewed component isolation
4. reviewed OCR/context package
5. caption rerun

Object isolation remains valuable, but only after a stronger selection gate is in place.
