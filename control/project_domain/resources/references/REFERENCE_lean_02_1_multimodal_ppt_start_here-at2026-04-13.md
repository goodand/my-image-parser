# REFERENCE_lean_02_1_multimodal_ppt_start_here-at2026-04-13

## Start Here

Use this public entry surface when another agent needs to enter the current lean `02_1` multimodal PPT stack quickly without re-deriving routing, tool ownership, or regeneration intent.

Read local truth first.

Treat external tools as donor/reference surfaces only.

## Role Boundary

- `Control-Plane Program Steward`
  - owns tool-facing promotion such as routing design, page-link matrices, regeneration bundles, and machine-readable execution surfaces
- `Public Surface Architect`
  - owns readable entry packaging, review navigation, and cross-linking so another agent can enter the stack in one pass

Boundary note:

- [NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md](../../../user_decisions/resources/notes/NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md)

## Fast Entry Order

### 1. Read the current review truth

Start with these two review indexes:

- [REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md](../references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md)
- [REFERENCE_lean_02_1_system_first_portfolio_v2_review_index-at2026-04-13.md](../references/REFERENCE_lean_02_1_system_first_portfolio_v2_review_index-at2026-04-13.md)

These tell you:

- which deck is current for `v1` and `v2`
- which render set belongs to each deck
- which role matrix and QA report belong to each slice

### 2. Read the page-link guide

Use this when you need to understand where PPT pages come from and how image-side evidence reaches publication surfaces:

- [REFERENCE_ppt_page_link_matrix_v0_1_step_by_step-at2026-04-13.md](../references/REFERENCE_ppt_page_link_matrix_v0_1_step_by_step-at2026-04-13.md)

This is the bridge for:

- `source -> evidence -> loop/review -> PPT target -> publication`

### 3. Read the regeneration handoff guide

Use this when the task is regeneration-safe deck reuse rather than first-pass review:

- [REFERENCE_ppt_regeneration_handoff_bundle_v0_1-at2026-04-13.md](../references/REFERENCE_ppt_regeneration_handoff_bundle_v0_1-at2026-04-13.md)
- [CHECKLIST_ppt_regeneration_handoff_bundle_execution_v0_1.md](../checklists/CHECKLIST_ppt_regeneration_handoff_bundle_execution_v0_1.md)

This is the correct entry point when the next lane must:

- rebuild the deck safely
- preserve dominant image/form roles
- keep current manual gates intact

### 4. Read the routing design only if you need owner-family semantics

If the task is about why the routing is shaped this way, read:

- [REFERENCE_image_skill_family_to_ppt_page_link_mapping_design-at2026-04-13.md](../../../../project_agent_ops/resources/references/REFERENCE_image_skill_family_to_ppt_page_link_mapping_design-at2026-04-13.md)

Do not start here unless you actually need routing semantics.

## Local Truth Surfaces

### Current deck outputs

`v1`

- deck: [lean_02_1_system_first_v1.pptx](../assets/portfolio_drafts/lean_02_1_system_first_v1/lean_02_1_system_first_v1.pptx)
- renders: [renders](../assets/portfolio_drafts/lean_02_1_system_first_v1/renders)
- role matrix: [lean_02_1_system_first_v1_image_role_matrix_at2026_04_11.json](../manifests/lean_02_1_system_first_v1_image_role_matrix_at2026_04_11.json)
- QA report: [REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md](../reports/REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md)

`v2`

- deck: [lean_02_1_system_first_v2.pptx](../assets/portfolio_drafts/lean_02_1_system_first_v2/lean_02_1_system_first_v2.pptx)
- renders: [renders](../assets/portfolio_drafts/lean_02_1_system_first_v2/renders)
- role matrix: [lean_02_1_system_first_v2_image_role_matrix_at2026_04_13.json](../manifests/lean_02_1_system_first_v2_image_role_matrix_at2026_04_13.json)
- QA report: [REPORT_lean_02_1_system_first_portfolio_v2_visual_qa-at2026-04-13-15-37.md](../reports/REPORT_lean_02_1_system_first_portfolio_v2_visual_qa-at2026-04-13-15-37.md)

### Machine-readable bridge artifacts

- [ppt_page_link_matrix_v0_1.json](../manifests/ppt_page_link_matrix_v0_1.json)
- [ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json](../manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json)

These are local truth artifacts.

Do not replace them with prose-only interpretation.

## External Tool Donor Surface

These links are practical donor/reference entry points only:

- [`slides-grab` local clone](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/vscode-markdown-review-surface/control/team/resources/external_repos/slides-grab)
- [`slides-grab` skill](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/vscode-markdown-review-surface/control/team/resources/external_repos/slides-grab/skills/slides-grab/SKILL.md)
- [`slides-grab-export` skill](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/vscode-markdown-review-surface/control/team/resources/external_repos/slides-grab/skills/slides-grab-export/SKILL.md)
- upstream provenance: [vkehfdl1/slides-grab](https://github.com/vkehfdl1/slides-grab)

Boundary:

- `slides-grab` is donor/reference only
- it does not replace local deck truth
- it does not replace local role matrices
- it does not replace local QA reports

## Public Entry Rules

- Start from local review truth, not from external tooling.
- Use page-link and handoff guides before proposing new routing.
- If the task starts to require manifest, script, or deck edits, stop and hand back to the toolization owner lane.
- If the task is only about readable navigation, stay inside this public entry surface and linked review indexes.

## One-Line Summary

This Start Here public entry surface is the fastest safe entry into the lean `02_1` multimodal PPT stack: local review truth first, local machine-readable bridge second, external donor tooling third.
