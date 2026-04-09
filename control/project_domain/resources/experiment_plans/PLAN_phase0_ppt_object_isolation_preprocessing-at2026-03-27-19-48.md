# Phase 0 PPT Object Isolation Preprocessing Plan

## Purpose

Define a review-gated component-isolation branch and decide when it is safe to use before the next caption or evaluation experiment.

The trigger for this plan is the discovery that raw PPT-extracted image assets often bundle multiple semantic objects into a single extracted media file.

## Why This Comes Before The Next Experiment

The current phase-1 baseline remains useful as a slide-media comparison baseline.

It is no longer sufficient as the primary next-step surface when the experiment goal is object-level caption quality, retrieval, or later object-grounded evaluation.

Therefore the current operational sequence becomes:

1. raw PPT-extracted image set
2. full-image standalone OCR baseline
3. reviewed context package build from OCR evidence plus PPT-local summary
4. optional reviewed component isolation branch
5. reviewed OCR/context package on the isolated candidate
6. caption rerun only after the reviewed branch is accepted

Automatic component isolation is now a gated branch, not the immediate default next step.

## Scope

In scope:

- evaluate whether meaningful components can be isolated reliably enough from PPT-extracted image assets
- persist crops, masks when useful, OCR evidence, and provenance records
- define a stable manifest and context package for downstream caption reruns
- validate whether current transparent-background assets can skip dedicated background removal
- define the review gate required before any batch object-isolation fanout

Out of scope:

- metadata write-back
- rename commit
- screenshot arm
- final multi-arm comparison

## Canonical Inputs

- PPT-extracted media resources:
  - `control/project_domain/resources/assets/caption_experiment/extracted_media/01_full_presentation_2026-03-17`
  - `control/project_domain/resources/assets/caption_experiment/extracted_media/02_1`
- raw extraction run artifacts:
  - `control/project_domain/resources/pptx_jobs/`
- reference basis:
  - [REFERENCE_object_isolation_tools.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/REFERENCE_object_isolation_tools.md)

## Current Status

Phase0 smoke on two real PPT-extracted images produced this decision:

- `find("bar chart")` and `find("table")` did not yield usable semantic matches
- fallback `detect` produced mechanically valid but semantically wrong crops
- full-image standalone OCR outperformed OCR on cropped or isolated outputs
- automatic object isolation is therefore not batch-ready in this workspace today

This plan remains active only as a review-gated branch.

## Current Reviewed Skill Supports

This branch now has explicit repo-local reviewed skill surfaces:

- `skills/transparent-component-triage`
- `skills/component-split-ocr-review`
- `skills/object-isolation-correction`

Interpretation:

- `transparent-component-triage` is the conservative batch prefilter
- `component-split-ocr-review` is the one-image deterministic evidence surface
- `object-isolation-correction` is the bounded correction-and-retry surface after a visible isolation failure

These skills support this branch but do not make the branch batch-default.

## Candidate Tool Profiles

### Profile A. ImageSorcery MCP Component Isolation

Candidate implementation:

- `imagesorcery-mcp`
- primary tool family: `detect`, `find`, `crop`, `fill`, `ocr`

Expected output:

- component crop
- optional segmentation-like mask or filled background variant
- OCR text when visible text exists

Best fit:

- UI cards, chart panels, popups, logos, and bounded visual components
- component selection via object detection or text-guided find
- MCP-first orchestration when local tool chaining is preferred

### Profile B. Image Capture Assisted Isolation

Candidate implementation:

- existing image capture surface
- screenshot-derived crop or visually bounded capture pass

Expected output:

- rendered-view crop
- component-local image surface that is easier to OCR and caption

Best fit:

- visible components that are easier to isolate after rendering
- chart regions, panels, and modal surfaces
- cases where raw extracted media is too bundled but the rendered view is cleaner

### Profile C. Background Removal Fallback

Candidate implementation:

- `rembg`
- optional MCP path: `rembg-mcp`

Current position:

- not a primary path for this workspace
- only use when a specific asset still needs alpha-matting despite already-transparent source characteristics

### Profile D. Promptable Segmentation Fallback

Candidate implementation:

- `SAM`
- future MCP wrapper or bounded local integration

## Proposed Output Layout

All raw preprocessing outputs should stay in `runs/`.

Recommended layout:

- `control/project_domain/archive/object_isolation/phase0_candidates/`
- `control/project_domain/archive/object_isolation/phase0_masks/`
- `control/project_domain/archive/object_isolation/phase0_cutouts/`
- `control/project_domain/resources/manifests/phase0_object_isolation_manifest.jsonl`
- `control/project_domain/resources/manifests/phase0_component_ocr_evidence.jsonl`
- `control/project_domain/resources/manifests/phase0_component_context_packages.jsonl`
- `control/project_domain/resources/reports/REPORT_phase0_object_isolation_smoke-atYYYY-MM-DD-HH-MM.md`

If a subset is later approved as the next canonical experiment surface, it can be promoted into:

- `control/project_domain/resources/assets/caption_experiment/object_isolated_media/`

## Required Record Fields

Each isolated-object row should carry at least:

- `source_image_id`
- `source_image_path`
- `source_pptx`
- `source_slide_numbers`
- `isolation_profile`
- `isolated_object_id`
- `mask_path`
- `cutout_path`
- `bbox`
- `selection_method`
- `selection_prompt` or `selection_rule`
- `ocr_text`
- `ocr_engine`
- `ocr_status`
- `ppt_context_summary`
- `context_bundle_path`
- `quality_status`
- `notes`

## MCP Preference

Preferred order for this workspace:

1. `imagesorcery-mcp` for component detection, crop, fill, and local OCR
2. image capture surface when visible rendered boundaries are easier to isolate than raw extracted media
3. `macos-ocr-mcp` for OCR evidence on isolated or captured components
4. `rembg` or `SAM` only as bounded fallback paths

Current note:

- the already registered `tigaweb-image-edit-sample-mcp` is not sufficient for component isolation because it only exposes brightness, crop, and compression tools
- `rembg` is not a preferred primary profile because many current PPT-extracted assets already preserve transparency
- the reviewed skill layer should be preferred over ad hoc commands when this branch is actually exercised

## Parallel Subagent Orchestration

This section is provisional and must not be activated until the review gate below is satisfied.

When activation is eventually needed, prefer issued task packets plus the promoted review skills above rather than direct ad hoc worker loops.

This phase should use subagents only through bounded issued packets.

Current execution assumption:

- `run_imagesorcery_mcp` runtime debugging is handled in another session
- phase-0 workers must not patch launcher, vendor source, or MCP bootstrap logic
- this plan covers only shard ownership, packet boundaries, and output layout

Maximum available subagents:

- `20`

Recommended staged allocation:

1. Stage A. component-isolation workers: up to `10`
2. Stage B. OCR and context-package workers: up to `8`
3. Stage C. audit or recovery workers: up to `2`

The full ceiling is `10 + 8 + 2 = 20`, but the stages should not overlap on the same output family.

### Stage A. Component-Isolation Workers

Worker ids:

- `ISO-W01` through `ISO-W10`

Ownership:

- each worker owns exactly one shard of source images
- each worker writes only its own candidate, cutout, mask, and shard ledger paths

Recommended write roots:

- `control/project_domain/archive/object_isolation/phase0_candidates/<worker_id>/`
- `control/project_domain/archive/object_isolation/phase0_cutouts/<worker_id>/`
- `control/project_domain/archive/object_isolation/phase0_masks/<worker_id>/`
- `control/project_agent_ops/registry/jobs/component_isolation_jobs/phase0_isolation_<worker_id>.json`

Deliverable per worker:

- one shard-local ledger
- one shard-local candidate manifest or equivalent bounded artifact
- bounded notes for rejected or ambiguous components

### Stage B. OCR And Context Workers

Worker ids:

- `CTX-W01` through `CTX-W08`

Precondition:

- Stage A aggregation is complete
- the main agent has published a promoted component manifest with no duplicate `isolated_object_id`

Ownership:

- each worker owns exactly one promoted-component shard
- each worker writes only shard-local OCR and context artifacts

Recommended write roots:

- `control/project_domain/resources/manifests/phase0_component_ocr_evidence_<worker_id>.jsonl`
- `control/project_domain/resources/manifests/phase0_component_context_packages_<worker_id>.jsonl`
- `control/project_agent_ops/registry/jobs/component_isolation_jobs/phase0_context_<worker_id>.json`

Deliverable per worker:

- OCR evidence rows
- context-package rows
- no-text or weak-text decision when OCR is not useful

### Stage C. Audit Or Recovery Workers

Worker ids:

- `AUD-W01`
- `AUD-W02`

Use only when needed:

- ambiguous component boundary
- conflicting OCR outputs
- component crop loses too much chart or UI context
- rerun authority is explicitly granted by a new issued packet

### Main-Agent Responsibilities

The main agent should remain the only writer for shared aggregate artifacts.

Main-agent-only outputs:

- `control/project_domain/resources/manifests/phase0_object_isolation_manifest.jsonl`
- `control/project_domain/resources/manifests/phase0_component_ocr_evidence.jsonl`
- `control/project_domain/resources/manifests/phase0_component_context_packages.jsonl`
- `control/project_domain/resources/reports/REPORT_phase0_object_isolation_smoke-atYYYY-MM-DD-HH-MM.md`
- any cross-worker summary, promotion decision, or phase transition note

### Packet Rules

Every subagent packet should bind:

- exact worker id
- exact input shard path
- exact allowed write roots
- exact expected row count or candidate count
- exact stop conditions

Every subagent packet must forbid:

- edits to `MASTER_PLAN_presentation_image_pipeline.md`
- edits to launcher scripts
- edits to vendored MCP source
- edits to shared aggregate manifests
- writes into another worker's shard directory

If a shard needs rerun or wider scope:

- do not mutate the old packet
- publish a new issued packet with a new timestamp

### Overlap Prevention

The following overlap rules are mandatory:

1. one source-image shard belongs to one isolation worker only
2. one promoted-component shard belongs to one OCR/context worker only
3. only the main agent writes aggregate manifests and reports
4. worker-local ledgers must use worker-specific stems
5. fallback or audit reruns require a new packet instead of widening an existing worker scope

## Execution Order

### Step 0. Candidate Selection

Start with a bounded sample rather than all extracted images.

Recommended first sample:

- chart-like image
- dashboard-like image
- UI screenshot with one dominant card or popup
- image with obvious foreground object

### Step 1. Full-Image OCR Baseline

Run one or two images through:

- full-image standalone OCR
- PPT-local context package build

Compare:

- OCR readability
- context usefulness
- ambiguity that still remains after full-image OCR

### Step 2. Reviewed Component Isolation Smoke

Run one or two images through:

- Profile A: ImageSorcery component isolation
- Profile B: capture-assisted isolation

Compare:

- crop usefulness
- OCR readability
- failure rate
- manual correction burden
- semantic alignment between intended prompt and selected crop

### Step 3. OCR Evidence Extraction

For promoted component candidates, collect OCR evidence and a no-text decision when needed.

### Step 4. Context Package Build

Build one bounded context package per promoted component candidate:

- OCR evidence summary
- PPT-local summary or surrounding slide context
- notes about omitted or unsupported text

### Step 5. Manifest Build

Persist one row per isolated object into:

- `phase0_object_isolation_manifest.jsonl`

### Step 6. Caption Surface Promotion Decision

Decide whether isolated or captured components plus their context packages are good enough to become the next caption surface.

If yes:

- rerun caption generation on context-enriched component assets

If no:

- revise profile selection or defer the component-isolation path

## Pass Criteria

- bounded smoke sample produces usable component crops or masks
- selected crop is semantically aligned with the intended object under explicit review
- every isolated asset has provenance back to the original extracted image
- OCR evidence and PPT-local summary are sufficient to build a later caption input without path ambiguity
- isolation outputs are written without overlapping worker ownership

## Failure Criteria

- crops or masks lose critical visible text or chart context
- OCR evidence is too weak to support context-enriched caption reruns
- one source image produces multiple variants with no stable selection rule
- downstream caption surface becomes less interpretable than the raw baseline
- `find` misses the target semantic object and `detect` falls back to unrelated classes or subregions

## Review Gate

Do not start batch object-isolation fanout unless all of the following are true:

1. reviewed smoke cases show semantically correct crop selection
2. isolated or cropped OCR is at least neutral relative to full-image OCR on the promoted cases
3. the worker packet clearly limits writes and promotion authority
4. the main agent can explain why the isolated surface is better than the full-image baseline for that case

## Planning Consequence

Until this phase is complete or explicitly waived:

- the raw extracted-media baseline remains a historical comparison baseline
- the evaluation overlay should not be treated as the next primary experiment arm
- the next primary rerun should assume full-image OCR and PPT-local context injection before caption generation
- object isolation should be used only behind a reviewed selection gate
