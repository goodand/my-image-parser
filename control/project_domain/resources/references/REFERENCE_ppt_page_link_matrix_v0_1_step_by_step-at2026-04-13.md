# REFERENCE_ppt_page_link_matrix_v0_1_step_by_step-at2026-04-13

## Purpose

This is the step-by-step completed guide for:

- [ppt_page_link_matrix_v0_1.json](../manifests/ppt_page_link_matrix_v0_1.json)

The matrix connects:

- image-side workflow skills
- machine-truth and review pages
- PPT target pages
- publication pages

without redefining owner-family responsibilities.

## Canonical Routing

- Band 8 owner:
  - [`multimodal-evidence-refinement-loop`](<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/multimodal-evidence-refinement-loop/SKILL.md)
- Band 8 specialist:
  - [`image-text-cot-review`](<CLAUDE_SKILLS_ROOT>/Skills-Create-Project/image-text-cot-review/SKILL.md)
- MCP lifecycle owner:
  - [`vendored-mcp-onboarding`](../../../../skills/vendored-mcp-onboarding/SKILL.md)
- PPT authoring surface:
  - [`pptx`](<CODEX_HOME>/skills/pptx/SKILL.md)

## External Tool Donor Linkage

Local clone used for practical reference:

- [`slides-grab` local clone](<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab)
- [`slides-grab` skill](<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab/skills/slides-grab/SKILL.md)
- [`slides-grab-export` skill](<EXTERNAL_REVIEW_SURFACE_ROOT>/control/team/resources/external_repos/slides-grab/skills/slides-grab-export/SKILL.md)

Upstream provenance:

- [vkehfdl1/slides-grab](https://github.com/vkehfdl1/slides-grab)

Boundary:

- `slides-grab` is a donor/reference surface for export and review patterns
- it is not the owner of the current `my-image-parser` page-link matrix
- current truth remains the local matrix, local review pages, and local deck artifacts

## Step By Step

### Step 1. Freeze routing first

Do not start from slide copy or visual polish.

Start from:

- owner family
- specialist
- MCP lifecycle owner
- PPT authoring surface

This is already frozen in:

- [REFERENCE_image_skill_family_to_ppt_page_link_mapping_design-at2026-04-13.md](../../../../project_agent_ops/resources/references/REFERENCE_image_skill_family_to_ppt_page_link_mapping_design-at2026-04-13.md)

The external donor surface is secondary:

- use the local `slides-grab` clone only as a compatible adjacent reference
- do not let it replace local owner-family routing or local artifact truth

### Step 2. Attach source pages

Each slide row in the matrix points to:

- the `02_1` source manifest
- the actual source image file
- the source slide number(s)

### Step 3. Attach current evidence pages

Current supporting evidence is linked through:

- [REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md](../reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md)

This keeps the matrix tied to real current artifacts.

### Step 4. Attach current bridge pages

Current bridge state is linked through:

- [lean_02_1_system_first_v1_image_role_matrix_at2026_04_11.json](../manifests/lean_02_1_system_first_v1_image_role_matrix_at2026_04_11.json)

Important current truth:

- standalone approved-caption rows do not exist yet for these 6 portfolio slides
- the matrix marks that as `not_separately_promoted`

That is intentional.

It prevents false completion claims.

### Step 5. Attach PPT target pages

Each slide row then points to:

- the target deck
- the per-slide rendered review image

Current deck:

- [lean_02_1_system_first_v1.pptx](../assets/portfolio_drafts/lean_02_1_system_first_v1/lean_02_1_system_first_v1.pptx)

### Step 6. Attach publication pages

Each row closes with:

- [REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md](../references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md)
- [REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md](../reports/REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md)

This gives the full chain:

`source -> evidence -> loop/review -> PPT target -> publication`

### Step 7. Read `linked_skills` correctly

The matrix includes `linked_skills` per slide.

These fields mean:

- which image-side skill is related to that slide
- which page class it links into
- whether the link is already current or still a future bridge

They do not mean:

- that the linked skill now owns the PPT page
- that a future bridge is already implemented

### Step 8. Use the matrix as the first reusable bridge

This artifact should be read before:

- creating a new image/PPT skill
- inventing a new owner-family
- opening a regeneration-specific slice

Because it already tells you:

1. where source truth starts
2. which evidence page is current
3. where loop/review state is still partial
4. which PPT page consumes the result

## Current Verification State

- matrix exists: `yes`
- 6 target slide rows exist: `yes`
- source/evidence/loop_review/ppt_target/publication chain exists per slide: `yes`
- standalone approved-caption promotion for these slides exists: `no`
- future OCR/table/component links are explicitly separated from current links: `yes`

## Deletion Candidates

None in this slice.

Reason:

- this work adds one machine-readable matrix and one step-by-step reference only
- no current artifact was deleted or replaced

## One-Line Summary

`ppt_page_link_matrix_v0_1.json` is the reusable completed bridge that links current image skills and page classes to the 6-slide lean portfolio deck while keeping owner-family, specialist, MCP lifecycle, and PPT authoring responsibilities separate.
