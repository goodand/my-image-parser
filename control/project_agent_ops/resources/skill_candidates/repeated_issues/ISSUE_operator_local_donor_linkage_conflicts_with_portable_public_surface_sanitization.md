# Repeated Issue: Operator-Local Donor Linkage Conflicts With Portable Public Surface Sanitization

## Symptom

- the same donor surface needs to be portable for tracked references and machine-readable artifacts
- the user also wants a fast local entry surface with clickable local clone links
- the result oscillates between placeholder-based portability and raw workstation-local absolute paths

## Scope

- local external-tool donor links
- tracked manifests and references
- operator-facing `Start Here` surfaces
- sibling-workspace donor clones

## Guardrail

- keep machine-readable and reusable tracked artifacts on placeholders such as `<EXTERNAL_REVIEW_SURFACE_ROOT>`
- allow literal local clone links only in explicitly operator-facing entry surfaces when the user asks for local truth first
- keep upstream GitHub as provenance only, never as replacement truth

## Follow-Up

- decide whether the artifact is `portable tracked surface` or `operator-local entry surface`
- use placeholder linkage for the first case and literal local links for the second case
- do not let donor-tool links replace local deck, role matrix, or QA truth

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` first sanitized `slides-grab` references in tracked manifests and references to `<EXTERNAL_REVIEW_SURFACE_ROOT>` in `fbec43f`, then later created a `Start Here` doc that intentionally restored literal local donor links for operator entry speed

## Step-By-Step Evidence Trace

1. `slides-grab` donor links first appeared as raw workstation-local absolute paths across tracked artifacts.
2. The portable tracked surfaces were then normalized to placeholders.
   - commit evidence: `fbec43f`
   - artifact evidence: `control/project_domain/resources/manifests/ppt_page_link_matrix_v0_1.json`
   - artifact evidence: `control/project_domain/resources/manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json`
3. The user then explicitly requested local truth and local donor links in the public entry surface.
4. A dedicated operator-facing entry document reintroduced literal local donor links on purpose, while keeping local deck and QA artifacts as truth.
   - entry evidence: `control/project_domain/resources/references/REFERENCE_lean_02_1_multimodal_ppt_start_here-at2026-04-13.md`
5. That split showed the real issue was not `absolute path always bad`, but `portable tracked surface` versus `operator-local entry surface` having different linkage rules.
