# Draft Classification And Migration Report

## Purpose

`my-second-identity`에서 유입된 old draft 원본과 현재 `my-image-parser/control` 안의 draft copies를 current-domain relevance 기준으로 분류하고, active draft와 legacy draft를 분리한다.

## Classification Rules

- `keep-active`
  - current `my-image-parser` presentation image pipeline과 직접 연결됨
- `keep-adjacent`
  - 현재 domain과 인접하지만 아직 master plan에 합류하지 않은 확장 탐색안
- `move-legacy`
  - provenance는 보존하되 active draft 목록에서는 제거
- `archive-old-workspace`
  - source workspace에서는 더 이상 active로 둘 이유가 없으므로 old workspace의 archive/pending_delete로 이동

## Current Control Active Drafts

| File | Classification | Reason |
|---|---|---|
| `PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md` | `keep-active` | current image pipeline core |
| `PLAN_canva_presentation_image_mapping_data_flow-at2026-03-27-15-29.md` | `keep-active` | Canva upstream and human review backbone |
| `PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md` | `keep-active` | tool-profile specific implementation branch |
| `PLAN_presentation_image_mapping_extension-at2026-03-27-15-29.md` | `keep-active` | retrieval/reranker extension summary |
| `PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md` | `keep-active` | appended structured-table extension |
| `PLAN_image_obsidian_style_parsing-at2026-03-27-15-27.md` | `keep-adjacent` | related PPT/PPTX parsing exploration, but broader than current pipeline |

## Current Control Legacy Imports

These were raw numbered imports and are now preserved only for provenance:

- `control/project_domain/resources/legacy/master_plan_drafts/raw_imports/PLAN_DRAFT_01-at2026-03-27-15-29.md`
- `control/project_domain/resources/legacy/master_plan_drafts/raw_imports/PLAN_DRAFT_02-at2026-03-27-15-29.md`
- `control/project_domain/resources/legacy/master_plan_drafts/raw_imports/PLAN_DRAFT_03-at2026-03-27-15-29.md`
- `control/project_domain/resources/legacy/master_plan_drafts/raw_imports/PLAN_DRAFT_04-at2026-03-27-15-29.md`

## Old Workspace Originals Archived

The following files originated in `my-second-identity` but belong to the current `my-image-parser` pipeline lineage. They were moved out of the old workspace's active planning surface:

- `PLAN_image_caption_pipeline_data_flow_2026-03-26.md`
- `PLAN_canva_presentation_image_mapping_data_flow_2026-03-26.md`
- `PLAN_cv_mcp_caption_eval_metadata_flow_2026-03-26.md`
- `PLAN_presentation_image_mapping_extension_2026-03-26.md`
- `inbox/PLAN_DRAFT_01_2026-03-26.md`
- `inbox/PLAN_DRAFT_02_2026-03-26.md`
- `inbox/PLAN_DRAFT_03_2026-03-26.md`
- `inbox/PLAN_DRAFT_04_2026-03-26.md`

Archive location in old workspace:

- `.../my-second-identity/plans/codex/docs/plans/archive/pending_delete/exported_to_my_image_parser/`

## Result

- active drafts now stay inside current workspace control root
- raw imports are preserved under current workspace legacy
- old workspace originals were moved to the old workspace archive/pending_delete area
- verification completed: the old workspace active `plans/` directory no longer contains those four named plan files
- verification completed: the old workspace `plans/inbox/` directory is empty after the move
