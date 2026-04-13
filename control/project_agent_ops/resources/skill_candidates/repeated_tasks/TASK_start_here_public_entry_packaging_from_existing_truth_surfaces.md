# Repeated Task: Start Here Public Entry Packaging From Existing Truth Surfaces

## Pattern Name

- start here public entry packaging from existing truth surfaces

## Trigger

- a slice already has multiple review indexes, guides, manifests, and QA artifacts
- another agent needs to enter that slice quickly without re-deriving routing or ownership
- the requested improvement is navigational packaging rather than new tool or deck design

## Stable Steps

1. Read the role-boundary note first.
2. Read the current review indexes and identify the actual local truth surfaces.
3. Read the page-link guide and regeneration handoff guide only as supporting entry surfaces, not as replacements for local truth.
4. Create one `Start Here` document that orders the reading path from review truth to bridge artifacts to regeneration surfaces.
5. Link local decks, renders, role matrices, and QA reports explicitly.
6. Link external donor tools as donor/reference only and keep upstream GitHub as provenance only.
7. Avoid touching scripts, manifests, deck assets, or routing contracts.

## Candidate Promotion

- reusable `Start Here` template for multimodal PPT stacks
- navigation rule: `local review truth first -> machine-readable bridge second -> regeneration handoff third -> routing design only if needed`
- donor-tool boundary section for public entry docs

## Promotion Trigger

- another portfolio or review stack becomes hard to enter because truth surfaces exist but are spread across multiple references

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` packaged the lean `02_1` stack into `REFERENCE_lean_02_1_multimodal_ppt_start_here-at2026-04-13.md`
- that entry surface linked the `v1` and `v2` review indexes, the page-link guide, the regeneration handoff guide and checklist, local deck outputs, and donor-only `slides-grab` links without altering tool-facing artifacts

## Step-By-Step Evidence Trace

1. The packaging task was explicitly constrained to readable entry work only.
   - packet evidence: `control/project_agent_ops/resources/task_packets/issued/TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY.json`
2. The current local truth surfaces were gathered first:
   - `control/project_domain/resources/references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md`
   - `control/project_domain/resources/references/REFERENCE_lean_02_1_system_first_portfolio_v2_review_index-at2026-04-13.md`
3. The supporting bridge artifacts were then gathered:
   - `control/project_domain/resources/references/REFERENCE_ppt_page_link_matrix_v0_1_step_by_step-at2026-04-13.md`
   - `control/project_domain/resources/references/REFERENCE_ppt_regeneration_handoff_bundle_v0_1-at2026-04-13.md`
4. A single readable entry surface was then written around those existing truths.
   - output evidence: `control/project_domain/resources/references/REFERENCE_lean_02_1_multimodal_ppt_start_here-at2026-04-13.md`
5. The entry surface kept local decks and role matrices as truth while demoting `slides-grab` to donor/reference only.
6. The entry artifact then landed as its own bounded commit.
   - commit evidence: `c496b83`
