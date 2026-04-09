# Task Packet: Master Plan Consolidation

## Goal

Consolidate the current presentation-image pipeline master plan by integrating the active draft set into the canonical master plan through bounded append-first patches.

## Canonical Target

- [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)

## In-Scope Inputs

### Active Drafts

- [PLAN_canva_presentation_image_mapping_data_flow-at2026-03-27-15-29.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_canva_presentation_image_mapping_data_flow-at2026-03-27-15-29.md)
- [PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md)
- [PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md)
- [PLAN_image_obsidian_style_parsing-at2026-03-27-15-27.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_image_obsidian_style_parsing-at2026-03-27-15-27.md)
- [PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md)
- [PLAN_presentation_image_mapping_extension-at2026-03-27-15-29.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_presentation_image_mapping_extension-at2026-03-27-15-29.md)
- [PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md)

### Supporting Contracts And Rules

- [presentation_image_pipeline_spec.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/contracts/presentation_image_pipeline_spec.json)
- [RULES_workspace_structure.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/rules/RULES_workspace_structure.md)
- [RULES_filename_and_linting.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/rules/RULES_filename_and_linting.md)

### External Indexed References

- [external_reference_index.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/external_reference_index.json)
- [REFERENCE_external_reference_triage.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/REFERENCE_external_reference_triage.md)

## Required Rules

1. Patch and append the existing master plan. Do not delete and rewrite the full file.
2. Preserve accepted sections unless they are directly contradicted by a higher-priority current draft.
3. Use current-workspace drafts first. Use external references only as style or good-case guidance.
4. Keep exactly one canonical master plan file.
5. Treat drafts as candidates for one of three outcomes:
   - merged into the canonical master plan
   - left in drafts as supporting source
   - reclassified into another bucket if it is clearly not a master-plan append candidate
6. Do not move user decision records into project-domain narrative sections.
7. Do not import outside-workspace files into the active control tree. Keep them indexed-only unless explicit promotion is required.
8. Keep file naming and markdown structure consistent with the existing workspace rules.

## Non-Goals

- Do not redesign the whole control taxonomy.
- Do not rewrite drafts into a brand-new standalone plan set.
- Do not create a second master plan.
- Do not edit external workspace source files.
- Do not convert historical run artifacts unless they are directly required for the consolidated plan.

## Consolidation Questions To Resolve

1. Which draft sections belong in the canonical master plan as workflow-bearing content?
2. Which draft sections are supporting appendix, implementation profile, or note material instead of core flow?
3. Which sections are duplicates and should remain only once in the master plan?
4. Where should table parsing, RAG, worksheet, and MCP-serving flow branch and rejoin the image pipeline?
5. Which draft content should be retained as a draft because it is exploratory rather than canonical?

## Expected Outputs

### Required

- Updated [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)

### Recommended

- Short consolidation report under:
  - `control/project_domain/resources/reports/`
- If draft roles changed, update:
  - [domain_artifact_index.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/registry/domain_artifact_index.json)

## Done Definition

- The canonical master plan includes all workflow-critical current draft content that should be canonical.
- The master plan remains append-oriented and structurally coherent.
- No duplicate master plan exists.
- The draft set is still readable, but each remaining draft has a clear reason to remain outside the canonical plan.
- No contradictions remain between the core flow, state transitions, artifacts, and branching sections.

## Verification

1. Read the current master plan and all active drafts before patching.
2. Verify that no new second canonical master plan file was created.
3. Verify that `MASTER_PLAN` still contains the patch/append policy.
4. Verify that workflow sections still read as one end-to-end flow instead of separate stitched notes.
5. If `domain_artifact_index.json` changes, validate it with `python3 -m json.tool`.

## Suggested Working Order

1. Extract unique claims and sections from each draft.
2. Group them into:
   - core flow
   - human review
   - implementation profile
   - appendix or notes
3. Patch the canonical master plan in bounded sections.
4. Re-read the full master plan for continuity.
5. Update indexes and add a brief consolidation report if needed.

## Handoff Note

This packet is immutable for the current consolidation pass. If the scope changes, create a new issued packet instead of silently expanding this one.
