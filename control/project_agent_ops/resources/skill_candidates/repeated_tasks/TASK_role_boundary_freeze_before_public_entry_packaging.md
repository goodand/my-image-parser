# Repeated Task: Role Boundary Freeze Before Public Entry Packaging

## Pattern Name

- role boundary freeze before public entry packaging

## Trigger

- a request asks for a clearer public or review-facing entry surface
- the workspace already contains tool-facing contracts, manifests, and routing artifacts
- the same change could easily drift into toolization or owner-family reinterpretation if boundaries stay implicit

## Stable Steps

1. Identify whether the requested work belongs to a readable entry surface or to control-plane toolization.
2. Freeze the boundary explicitly in one note before changing public-facing navigation docs.
3. State which role owns tool contracts, routing, and execution surfaces.
4. State which role owns readable entry packaging, review navigation, and git packaging of that readable surface.
5. Use the boundary note as the source of truth for any follow-up packet or handoff.
6. Stop if the requested improvement would require contract, script, manifest, or deck changes.

## Candidate Promotion

- reusable role-boundary note template for `toolization owner` vs `public surface packager`
- preflight rule: freeze role ownership before making a new `Start Here` or `public entry` document
- handoff packet rule: reference the boundary note as the controlling source of truth

## Promotion Trigger

- another workspace already has rich machine-readable artifacts and now needs a human- or agent-readable entry surface without reopening control-plane semantics

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` had to freeze the split between `Control-Plane Program Steward` and `Public Surface Architect` in `NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md` before the `Start Here` surface could be created safely
- the later entry packet and chained dispatch prompt both used that note as their boundary source of truth

## Step-By-Step Evidence Trace

1. The public-entry request first arrived as a navigation/packaging need, not as a tool-contract change.
   - request-shape evidence: `control/project_agent_ops/resources/task_packets/issued/TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY.json`
2. That request still risked reopening toolization and owner-family semantics because the same artifacts were already spread across manifests, review indexes, and routing references.
   - routing evidence: `control/project_agent_ops/resources/references/REFERENCE_image_skill_family_to_ppt_page_link_mapping_design-at2026-04-13.md`
3. The boundary was then frozen explicitly in one note.
   - boundary-note evidence: `control/user_decisions/resources/notes/NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md`
4. The note assigned tool contracts, routing, and machine-readable execution surfaces to `Control-Plane Program Steward`.
5. The same note assigned readable entry packaging, review navigation, and public-surface git packaging to `Public Surface Architect`.
6. Only after that freeze did the readable entry surface land safely.
   - entry-surface commit evidence: `c496b83`
