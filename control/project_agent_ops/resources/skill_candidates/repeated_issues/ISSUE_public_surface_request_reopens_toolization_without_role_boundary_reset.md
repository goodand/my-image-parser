# Repeated Issue: Public Surface Request Reopens Toolization Without Role Boundary Reset

## Symptom

- a request sounds like simple public-facing packaging
- the same artifact set already contains routing design, handoff contracts, and machine-readable execution surfaces
- without an explicit boundary, the packaging pass starts drifting into toolization, owner-family reinterpretation, or contract edits

## Scope

- public entry docs
- review indexes
- start-here packaging
- handoff prompts that sit on top of existing control-plane artifacts

## Guardrail

- freeze the boundary between toolization owner and readable-surface packager first
- record the boundary in one note and use that note as the next packet's source of truth
- forbid contract, manifest, script, and deck edits inside the public-surface pass

## Follow-Up

- write the boundary note first
- then write the entry packet or `Start Here` surface under that note
- stop if the improvement requires control-plane reinterpretation

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` had to write `NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md` before `Public Surface Architect` could safely package the lean `02_1` public entry surface

## Step-By-Step Evidence Trace

1. The request was for a cleaner public-entry surface, not a new tool or owner-family.
2. Existing artifacts already carried routing, handoff, and execution semantics.
   - evidence: `control/project_agent_ops/resources/references/REFERENCE_image_skill_family_to_ppt_page_link_mapping_design-at2026-04-13.md`
3. That overlap created a real risk that entry packaging would mutate control-plane meaning.
4. The boundary was then frozen in one explicit note.
   - note evidence: `control/user_decisions/resources/notes/NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md`
5. The later entry packet and chained prompt both cited that note as their control surface.
   - packet evidence: `control/project_agent_ops/resources/task_packets/issued/TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY.json`
   - prompt evidence: `control/project_agent_ops/resources/references/REFERENCE_public_surface_architect_chained_dispatch_prompt-at2026-04-13.md`
