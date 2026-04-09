# Object Isolation Tool Reference

## Purpose

Summarize the currently most relevant component-isolation and OCR-support tool options for the PPT-extracted image experiment.

This document is reference-only.

## Why This Matters

The current raw PPT media extract can bundle multiple semantic objects into one image.

If the experiment goal moves from slide-media captioning to object-level captioning or retrieval, a preprocessing stage is needed before caption generation and evaluation.

## Candidate Tool A: ImageSorcery MCP

Upstream:

- <https://github.com/sunriseapps/imagesorcery-mcp>

Observed utility from the upstream README:

- local `detect`, `find`, `crop`, `fill`, and `ocr` tools
- can detect or find components and then derive crop-like outputs
- can keep processing inside one MCP surface rather than splitting isolation and OCR across unrelated tools
- runs locally without sending images to a remote service

Practical fit for this workspace:

- strongest MCP-first candidate for current component isolation
- well suited when raw PPT extracts already preserve transparency and only need component detection plus bounded crops
- can support OCR collection close to the isolation stage

Observed limit from workspace smoke:

- MCP registration and boot are verified, but automatic semantic selection is not yet reliable enough for unattended batch use
- on real PPT-extracted assets, `find("bar chart")` and `find("table")` did not return usable matches
- generic `detect` fallback can produce mechanically valid but semantically wrong crops
- current role is therefore review-gated isolation, not default batch preprocessing

## Candidate Tool A-1: Alpha Connected-Components First

Workspace basis:

- `skills/object-isolation-correction/scripts/run_object_isolation_correction_worker.py`

Practical fit for this workspace:

- first path for transparent PNGs whose objects are already disconnected in the alpha channel
- avoids unnecessary new dependency installs because the worker uses the existing vendored ImageSorcery runtime
- exports one bounded crop per alpha component before model-backed fallback is attempted

Current role:

- primary deterministic split path when the image is already transparent and visually separated
- if alpha split is insufficient, the same worker falls back to ImageSorcery and then prepares a bounded imagegen request
- best fit is still reviewed selection, not automatic promotion into the next caption baseline
- the workspace now also has a reusable `component -> table -> OCR` surface:
  - builder: `scripts/build_component_split_ocr_report.py`
  - library: `scripts/component_split_ocr_lib.py`
  - shared alpha module: `scripts/alpha_component_lib.py`
  - output: per-component PNGs, component table markdown, component OCR JSON sidecars

Observed alpha-only batch classification:

- report: `control/project_domain/resources/reports/REPORT_phase0_alpha_split_batch_classification-at2026-03-27-15-05.md`
- summary: `control/project_domain/resources/manifests/phase0_alpha_split_batch_classification_summary.json`
- current counts on PPT-extracted media:
  - `alpha_split_sufficient`: `9`
  - `single_component_only`: `50`
  - `non_alpha_source_or_opaque_surface`: `1`
  - `unsupported_source_format`: `1`
- interpretation:
  - this is a mechanical alpha-connectivity pass, not a semantic object-selection guarantee
  - the `alpha_split_sufficient` subset is the only immediate deterministic candidate pool
  - even that subset should stay review-gated before downstream caption reruns or object-level promotion

## Candidate Tool B: Image Capture Surface

Workspace basis:

- `skills/pptx-slide-screenshot-capture`
- existing screenshot or rendered-view capture paths

Practical fit for this workspace:

- useful when a rendered component boundary is easier to isolate than the raw extracted media
- useful for panels, cards, charts, or visible popup surfaces
- can produce a cleaner crop before OCR and caption rerun

## Candidate Tool C: OCR Support After Isolation

Workspace basis:

- `macos-ocr-mcp`
- `macOCR` reference path

Practical fit for this workspace:

- collect text evidence after a component crop has been chosen
- support chart, table, and UI text grounding before the next caption pass
- feed OCR evidence into a later context package for the API call

Current workspace interpretation:

- standalone OCR on the full original image is the current safer baseline than OCR on automatically isolated crops
- isolated-object OCR should remain experimental until the component-selection gate improves

## Candidate Tool D: rembg / rembg-mcp Fallback

Upstream:

- <https://github.com/danielgatis/rembg>
- <https://github.com/holocode-ai/rembg-mcp>

Current role:

- fallback-only
- not the preferred primary path for current PPT assets because many extracted media files already preserve transparency

## Candidate Tool E: Segment Anything Model (SAM)

Upstream:

- <https://github.com/facebookresearch/segment-anything>

Practical fit for this workspace:

- fallback for ambiguous multi-object images when ImageSorcery plus capture is not enough

## Current Workspace Constraint

The older sample image-edit MCP surface is only:

- brightness adjustment
- cropping
- compression

So that older sample MCP is not a canonical component-isolation surface by itself.

This means phase-0 component isolation should prefer one of:

- `imagesorcery-mcp` as the first MCP wrapper candidate
- image capture plus bounded crop on a rendered surface
- `macos-ocr-mcp` after the component boundary has been chosen
- `rembg` or `SAM` only when the first paths are insufficient

## Planning Implication

The current active baseline should be:

- `PPT extracted image -> full-image standalone OCR -> reviewed context package`

Object isolation remains a candidate branch, but it is not batch-ready in this workspace today.

Use object isolation only when one of the following is true:

- the image is transparently separated and alpha components are obviously valid
- a human reviews the selected crop before downstream reuse
- a later selection gate can prove the isolated crop is semantically aligned with the intended object

Only after that should the project rerun:

- object-level caption generation with context injection
- object-level evaluation overlay

## Workspace Skill Layer

This workspace now also has a repo-specific correction skill at:

- `skills/object-isolation-correction`

Its role is not to replace the underlying tool surfaces.
Its role is to choose and package the retry route:

- `imagesorcery-first`
- `imagegen-first`
- `hybrid`

The new worker under the same skill also gives the workspace a bounded execution path:

- alpha split first for transparent PNGs
- ImageSorcery fallback second
- imagegen request artifact third when repair still needs multimodal cleanup

Use it when the main question is how to correct an imperfect isolation result, not merely which low-level MCP exists.

## Workspace Skill Layer: Component Split OCR Review

This workspace now also has a repo-specific review skill at:

- `skills/component-split-ocr-review`

Its role is narrower than object-isolation correction.
It exists to expose deterministic evidence for one image:

- alpha-connected component crops
- component table markdown/json
- per-component OCR sidecars

Use it when the question is:

- "how many disconnected alpha components are there?"
- "what does each component look like?"
- "does any separated component contain text worth carrying forward?"

Do not use it as proof that each exported component is semantically meaningful.
Treat it as a reviewed evidence surface only.

## Workspace Skill Layer: Transparent Component Triage

This workspace also has a repo-specific batch triage skill at:

- `skills/transparent-component-triage`

Its role is to keep preprocessing conservative while still surfacing the small subset of files that are mechanically sufficient for alpha-only splitting.

Use it when the question is:

- "which PPT-extracted files are even worth one-image component review?"
- "which files should stay on the full-image baseline?"

Do not use it as a semantic isolation engine.
Its output is a reviewed candidate subset only.

## Source Basis

- <https://github.com/sunriseapps/imagesorcery-mcp>
- <https://github.com/danielgatis/rembg>
- <https://github.com/holocode-ai/rembg-mcp>
- <https://github.com/facebookresearch/segment-anything>
