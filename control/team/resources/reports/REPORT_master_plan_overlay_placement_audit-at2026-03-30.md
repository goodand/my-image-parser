# Master Plan Overlay Placement Audit

## Purpose

Record the 2026-03-30 audit that separated stable master-plan documents from user-facing decision-support overlays.

## Audit question

Which documents under `control/project_domain/resources/master_plans/` should remain there, and which should move into `control/user_decisions/resources/`?

## Method

- reviewed the relevant master-plan and draft documents locally
- used 10 subagents to independently classify the current files
- compared subagent verdicts against the workspace-structure rules
- normalized the result into explicit placement rules and lint coverage

## Result

### Keep in `control/project_domain/resources/master_plans/`

These are stable plan or architecture documents and should remain in `master_plans`.

- `MASTER_PLAN_presentation_image_pipeline.md`
- `drafts/PLAN_canva_presentation_image_mapping_data_flow-at2026-03-27-15-29.md`
- `drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md`
- `drafts/PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md`
- `drafts/PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md`
- `drafts/PLAN_image_obsidian_style_parsing-at2026-03-27-15-27.md`
- `drafts/PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md`
- `drafts/PLAN_presentation_image_mapping_extension-at2026-03-27-15-29.md`
- `drafts/PLAN_vscode_markdown_review_surface_replacement_strategy-at2026-03-30.md`

### Move to `control/user_decisions/resources/notes/`

These are decision-support overlays rather than stable master plans.

- progress dashboard
- task graph view
- scoreboard-style status snapshot
- current-state snapshot overlays

Canonical moved files:

- [REFERENCE_master_plan_progress_dashboard-at2026-04-05-09-17.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/REFERENCE_master_plan_progress_dashboard-at2026-04-05-09-17.md)
- [REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md)
- [NOTE_presentation_image_pipeline_current_state_snapshot-at2026-03-30-09-21.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/NOTE_presentation_image_pipeline_current_state_snapshot-at2026-03-30-09-21.md)

Redirect stubs remain in `master_plans/` only when needed for path continuity.

## Rule extracted from the audit

- `master_plans/` is the canonical home for stable plan meaning, architecture, rollout flow, and experiment framing.
- `user_decisions/resources/notes/` is the canonical home for user-facing overlays that explain current status, bottlenecks, progress, tradeoffs, or next decisions.

## Lint follow-up

The lint layer now warns on misplaced decision-support overlays under `master_plans/`.

- warning code: `DOC003`
- exception: redirect stubs that clearly contain `## Moved`

The linter was also hardened to tolerate Unicode normalization differences in absolute paths so the control-tree lint no longer crashes on NFC/NFD pathname drift.

## Outcome

- no additional master-plan moves are currently justified
- the stable-plan / decision-overlay split is now explicit in rules, references, and lint behavior
- future drift should surface as a warning instead of silently accumulating
