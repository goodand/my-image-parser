# REFERENCE_ppt_regeneration_handoff_bundle_v0_1-at2026-04-13

## Purpose

This reference explains how to use:

- [ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json](../manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json)

The bundle is the first concrete regeneration handoff for the lean `02_1` six-slide portfolio slice.

It is not a new skill.

It is the execution contract that tells a later PPT authoring lane what can be reused now and what is still manual.

## Ownership Boundary

- Band 8 owner:
  - [`multimodal-evidence-refinement-loop`](<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/multimodal-evidence-refinement-loop/SKILL.md)
- Band 8 specialist:
  - [`image-text-cot-review`](<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/image-text-cot-review/SKILL.md)
- MCP lifecycle owner:
  - [`vendored-mcp-onboarding`](../../../../skills/vendored-mcp-onboarding/SKILL.md)
- PPT authoring surface:
  - [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md)
- Claude copy-support skill explicitly carried in the handoff:
  - [`semantic-clarity-enhanced`](<CLAUDE_SKILLS_ROOT>/semantic-clarity-enhanced/SKILL.md)

PPT remains a consumer surface.

The bundle does not promote PPT into a new owner family.

## External Tool Linkage

Current external tool linkage is intentionally expressed in two layers:

- local clone used as the practical reference surface:
  - [`slides-grab` local clone](<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab)
  - [`slides-grab` skill](<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab/skills/slides-grab/SKILL.md)
  - [`slides-grab-export` skill](<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab/skills/slides-grab-export/SKILL.md)
- upstream provenance only:
  - [vkehfdl1/slides-grab](https://github.com/vkehfdl1/slides-grab)

Boundary:

- `slides-grab` is a reference/export donor surface for slide capture and HTML/PPT export ideas.
- It is not the source of truth for the current `my-image-parser` deck artifacts.
- Current source of truth remains the local deck, role matrix, handoff bundle, and QA reports in this workspace.

## Step By Step

### Step 1. Read the page-link matrix first

Start from:

- [ppt_page_link_matrix_v0_1.json](../manifests/ppt_page_link_matrix_v0_1.json)

That matrix tells you the routing chain:

`source -> evidence -> loop/review -> PPT target -> publication`

The handoff bundle does not replace that chain.

It freezes the regeneration-facing read of that chain.

### Step 2. Read the current deck and QA status as current truth

Current portfolio artifacts:

- [lean_02_1_system_first_v1.pptx](../assets/portfolio_drafts/lean_02_1_system_first_v1/lean_02_1_system_first_v1.pptx)
- [REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md](../reports/REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md)
- [REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md](../references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md)

The deck is the source of truth.

Quick Look preview caching is still only a preview caveat.

### Step 3. Use the bundle only for regeneration-safe reuse

For each slide row, read:

- `source_images`
- `current_pages`
- `text_promotion_state`
- `regeneration_handoff`

This gives the next lane enough information to:

- rebuild an equivalent slide
- edit the current deck safely
- preserve the correct image/form role

without pretending that a fuller text-promotion pipeline already exists.

### Step 4. Respect the current manual gates

The bundle keeps several items manual on purpose:

- standalone approved caption promotion
- standalone approved alt-text promotion
- final value-level readability judgment on table-heavy slides
- any MCP/provider reopen work

Those items are not missing by accident.

They are explicit non-goals in this slice.

### Step 5. Keep PPT authoring and image understanding separate

The bundle links image-side evidence and loop state into PPT targets.

It does not merge the two responsibilities.

That means:

- image-side loop logic still belongs to the Band 8 family
- PPT writing/editing still belongs to the global `pptx` surface

### Step 6. Treat deletion as closed out for this slice

Deletion candidates are intentionally empty here.

Reason:

- the user explicitly prioritized recoverability and verification over cleanup
- this slice adds reusable handoff artifacts only

## Current Bundle Verdict

- machine-readable bundle exists: `yes`
- slide rows exist for all 6 portfolio slides: `yes`
- current deck/QA/review surfaces are linked: `yes`
- standalone approved caption promotion exists: `no`
- bundle is usable for regeneration-safe handoff anyway: `yes`

## One-Line Summary

`ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json` is the first concrete handoff contract that lets a later PPT regeneration lane reuse the current lean `02_1` portfolio artifacts without collapsing owner-family boundaries or overstating text-promotion completion.
