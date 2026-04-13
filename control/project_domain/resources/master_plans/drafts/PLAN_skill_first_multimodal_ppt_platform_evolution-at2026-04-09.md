# PLAN_skill_first_multimodal_ppt_platform_evolution-at2026-04-09

## Purpose

Design the next program after the closed caption-experiment cycle.

The goal is to evolve from a proven experiment into a reusable capability that can:

- understand PPT images with context
- preserve multimodal form where it matters
- evaluate and cross-validate image understanding
- use approved image understanding to help regenerate or author PPT artifacts

## Planning Stance

Start with `Agent Skills`.

Do **not** begin by building:

- one monolithic all-in-one MCP
- one Docker-first end-to-end platform
- one tightly coupled ML-runtime bundle

Those may become later packaging steps, but they should not be the first productization move.

## Program Thesis

The most efficient next move is:

`existing providers -> stable contracts -> orchestration skills -> narrow MCP promotion -> broader platform packaging`

This keeps the first productization slice small while preserving the ability to support heavier ML-backed provider paths later.

Companion architecture reference:

- [REFERENCE_skill_owner_family_platform_architecture-at2026-04-10.md](../../../../project_agent_ops/resources/references/REFERENCE_skill_owner_family_platform_architecture-at2026-04-10.md)

## User-Facing Outcome

The final capability should support a workflow where:

1. a PPT is opened or extracted into image units
2. each image is parsed with the right context strategy
3. captions and alt text are generated with form-aware constraints
4. review and cross-validation can approve or reject those outputs
5. approved outputs can feed later PPT regeneration or authoring

The user-facing value is not `caption everything blindly`.

It is:

- `understand the image in context`
- `preserve meaningful structure`
- `use that understanding to build better PPT outputs`

## Existing Skill Base To Extend

### `pptx-slide-screenshot-capture`

Owns PPT slide extraction and screenshot capture.

### `image-job-dispatcher`

Owns bounded fanout and provider-aware job dispatch.

### `image-result-auditor`

Owns bundle freeze, comparison output, review bridge, and dry-run consumer prep.

### `obsidian-caption-review-builder`

Owns human-readable markdown review surfaces.

### `parser-sidecar-to-canonical-schema-promotion`

Owns structured parser evidence normalization and compound edge-case routing.

### `image-commit-manager`

Owns approved metadata and rename commit only after human or policy approval.

## Required New Contract Layer

Before broader packaging, the workspace should freeze a small set of canonical contracts.

### 1. Image Context Contract

Defines the minimal shared image-understanding record.

Suggested fields:

- `image_id`
- `source_pptx_path`
- `slide_numbers`
- `visual_type`
- `context_strategy`
- `form_preservation_required`
- `form_risk_flags`
- `structured_regions_present`
- `table_like`
- `diagram_like`
- `ui_like`
- `logo_like`

### 2. Caption Output Contract

Defines approved output shape independent of provider.

Suggested fields:

- `caption`
- `alt_text`
- `caption_arm`
- `promotion_state`
- `evidence_refs`
- `form_preservation_notes`

### 3. Review Decision Contract

This already partially exists and should be extended rather than replaced.

It should remain the canonical human or agent judgment bridge.

### 4. PPT Regeneration Handoff Contract

Defines what a downstream PPT-writing skill or runtime may consume.

Suggested fields:

- `approved_caption`
- `approved_alt_text`
- `approved_image_context`
- `placement_hint`
- `presentation_role`
- `regeneration_notes`

## Provider Matrix Rule

The orchestration layer must remain provider-backed, not provider-bound.

That means:

- keep OCR, parser, table, and vision providers replaceable
- do not hardcode one ML-backed provider as the only legal path
- measure provider effectiveness through evidence-backed comparisons
- promote only proven repeated paths into a narrower MCP later

## Phase Plan

### Phase 1. Skill-First Orchestration Hardening

Goal:

- extend existing skills so the end-to-end workflow can be orchestrated without inventing a new platform layer first

Outputs:

- updated skill ownership boundaries
- cross-skill dependency map
- provider matrix reference
- contract gap list

### Phase 2. Multimodal Context Contract Freeze

Goal:

- define the canonical image context contract with explicit form-preservation semantics

Outputs:

- prose spec
- contract JSON
- sample manifests

### Phase 3. Review And Validation Surface Tightening

Goal:

- ensure review surfaces show the right candidate comparison and form-preservation cues

Outputs:

- review surface contract patch
- operator checklist patch
- dry-run measurement rules that include form risk

### Phase 4. PPT Regeneration Handoff

Goal:

- define how approved image understanding is handed off to PPT authoring or regeneration lanes

Outputs:

- regeneration handoff spec
- sample bundle
- explicit non-goals for what is still manual

### Phase 5. Narrow MCP Promotion

Goal:

- promote one or two stable provider paths into narrower MCP surfaces only if repetition justifies it

Candidates:

- stable multimodal image-context extraction
- stable review-to-regeneration handoff packaging

### Phase 6. Platform Packaging

Goal:

- only after the above stabilizes, evaluate Docker or broader runtime packaging

## Non-Goals

- do not create a giant `do everything` MCP first
- do not package all ML dependencies into one mandatory runtime first
- do not force Docker before contracts and skill boundaries stabilize
- do not treat multimodal document form as generic noise when downstream use depends on that form

## First Recommended Deliverables

1. a `skill integration plan` for the existing image-related skills
2. a `multimodal image context contract` draft
3. a `provider matrix` reference that maps tasks to existing MCPs/scripts
4. a `ppt regeneration handoff` concept note

## Completion Criteria For This Plan

This planning phase is complete when:

1. the workspace has a frozen direction note saying `skill-first, provider-backed, platform-later`
2. the existing-skill extension map is explicit
3. the required new contracts are named and scoped
4. the MCP promotion boundary is deferred until stability evidence exists
5. the form-preservation requirement is explicit in downstream measurement language

## One-Line Summary

Build the next capability as a `skill-first orchestration layer` over existing providers, then harden contracts, then selectively promote stable slices into MCPs, and only after that consider full platform packaging.
