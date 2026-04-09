# Master Plan: Presentation Image Pipeline

## Purpose

Canva presentation 또는 exported presentation file을 upstream asset source로 사용해:

1. presentation에서 이미지 자산을 추출하고
2. 이미지 캡션과 관련 문서 매핑 후보를 만든 뒤
3. 사람 검토를 거쳐
4. 필요 시 metadata 또는 filename을 반영하고
5. 이미지와 최종 텍스트를 기반으로 새 presentation 자산을 재생성한다.

This document is the append-oriented canonical master plan for the pipeline.

## Change Policy

- Update this master plan by patching and appending bounded sections.
- Do not replace the full document with a fresh rewrite unless the file is being created for the first time or the current file is unrecoverably invalid.
- Preserve prior accepted sections whenever possible.
- New pipeline slices should be added as appended extensions or clearly bounded section patches.

## Source Of Truth

- Pipeline contract:
  - [presentation_image_pipeline_spec.json](../specs/contracts/presentation_image_pipeline_spec.json)
- Supporting operational specs:
  - [SPEC_openai_image_caption_runner.md](../specs/prose/SPEC_openai_image_caption_runner.md)
  - [SPEC_full_image_standalone_ocr_context_package_baseline.md](../specs/prose/SPEC_full_image_standalone_ocr_context_package_baseline.md)
- Tooling and runtime references:
  - Tool Inventory (local/private registry): `<LOCAL_AGENT_REGISTRY>/tools/tool_inventory.json`
  - MCP Setup Reference (local/private tools inventory): `<LOCAL_AGENT_REFERENCE_ROOT>/tools_inventory/REFERENCE_mcp_setup.md`
  - [Object Isolation Tool Reference](../references/REFERENCE_object_isolation_tools.md)
  - [OCR Evidence Tool Reference](../references/REFERENCE_ocr_evidence_tools.md)
- Current appended extension:
  - [PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md](./drafts/PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md)
- Active implementation profiles:
  - [PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md](./drafts/PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md)
  - [PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md](./drafts/PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md)
- Active experiment-preparation profile:
  - [PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md](./drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md)

## Operational Assumptions

### Source Assumption

- Canva is the upstream source only.
- The system reads from Canva and exports from Canva.
- Reverse sync back into Canva is out of scope.

### Human Review Assumption

Humans perform three review checkpoints that cover the five mandatory review tasks listed later:

- caption review and correction
- top-5 document mapping review
- outlier description writing

No automated path may bypass these gates.

### Reprocessing Assumption

If the approved caption changes, retrieval and rerank outputs may change. Therefore downstream retrieval stages must be rerunnable from the caption change point.

## Core Data Objects

### Job

One pipeline execution for one source Canva design.

Fields:

- `job_id`
- `source_design_id`
- `source_design_title`
- `source_export_file`
- `status`
- `created_at`
- `pipeline_version`

### Image Item

One extracted image from the source presentation.

Fields:

- `image_id`
- `job_id`
- `source_page_no`
- `source_element_order`
- `image_path`
- `image_hash`
- `is_duplicate`
- `is_decorative`

### Caption Record

Stores draft and approved caption state.

Fields:

- `image_id`
- `draft_caption`
- `approved_caption`
- `caption_review_status`
- `caption_edited_by_human`
- `caption_last_updated_at`

### Mapping Record

Stores retrieval and final mapping state.

Fields:

- `image_id`
- `retrieval_query`
- `candidate_doc_ids`
- `reranked_top5`
- `selected_doc_id`
- `mapping_status`
- `outlier_label`
- `manual_description`

### Execution Record

Stores phase-level execution state that the orchestrator must re-read before advancing a job or image phase.

Fields:

- `job_id`
- `image_id`
- `phase`
- `state`
- `attempt`
- `worker_agent`
- `evidence`
- `started_at`
- `finished_at`
- `last_error`

### Worker Result Payload

Stores the minimal payload returned by a worker before the parent re-reads registry state and execution state.

Fields:

- `job_id`
- `image_id`
- `phase`
- `success`
- `caption`
- `rename_candidate`
- `evidence`
- `error`

## Completed Baseline

Already completed in the current broader workflow:

- presentation file에서 이미지 추출
- Gemini 기반 이미지 캡션 생성
- 이미지와 캡션 기반 presentation 생성
- extracted-media + OpenAI phase-1 baseline execution on 2026-03-27
  - total records: `61`
  - completed: `60`
  - unsupported_media_type: `1`
  - expected unsupported case: one `.emf` asset

## Core End-To-End Flow

1. Canva presentation 선택 또는 export 대상 식별
2. presentation file 다운로드 또는 export
3. presentation 내부 이미지 추출
4. 이미지 캡션 초안 생성
5. 사람 검토를 통한 caption 승인 또는 수정
6. 이미지 embedding 생성
7. candidate document retrieval
8. reranker top-5 후보 생성
9. 사람 검토를 통한 mapping 확정 또는 outlier 분류
10. outlier manual description 작성
11. metadata and rename candidate 관리
12. image plus approved text 기반 presentation regeneration

## Detailed End-To-End Data Flow

### Step 0. Job Initialization

- Input:
  - user-selected Canva presentation or search condition
  - target document store or document corpus
  - pipeline configuration
- Process:
  - create `job_id`
  - initialize working directories
  - initialize job manifest and execution records
- Output:
  - `job_manifest.json`
  - job state `initialized`

### Step 1. Canva Presentation Resolution And Download

- Input:
  - Canva design ID or search condition
- Process:
  - resolve the target presentation
  - export or download the presentation file
  - store source metadata
- Output:
  - `source_presentation.pptx`
  - `source_metadata.json`
  - job state `source_downloaded`

### Step 2. Image Extraction

- Input:
  - `source_presentation.pptx`
- Process:
  - extract embedded images
  - assign stable image IDs
  - record slide number, element order, and hash
  - optionally mark decorative or duplicate assets
  - mark `table_candidate` when lightweight heuristics or layout signals indicate table-like structure
- Output:
  - extracted image set
  - `image_manifest.jsonl`
  - optional `table_candidate_manifest.jsonl`
  - job state `images_extracted`

### Step 2A. Unsupported Media Detection And Routing

- Input:
  - extracted image and media set
  - extraction manifest
- Process:
  - detect unsupported embedded media types before automated caption generation
  - persist unsupported-media evidence and reason
  - exclude unsupported entries from the automated caption branch unless a separate conversion pass creates a supported asset
- Output:
  - optional `unsupported_media_manifest.jsonl`
  - per-image state `unsupported_media_type`

### Step 3. Draft Caption Generation

- Input:
  - caption-eligible extracted images
- Process:
  - generate one draft caption per image
  - store generation metadata
- Output:
  - `caption_draft.jsonl`
  - per-image state `caption_drafted`

### Step 3A. Optional Evaluation Decision Gate

- Input:
  - draft caption
  - image
  - evaluation profile configuration
- Process:
  - optionally score or judge the generated caption
  - branch into `review_ready`, `rewrite_pending`, `audit_pending`, or `error`
  - persist evaluation decision and evidence
- Output:
  - optional `evaluation_decisions.jsonl`
  - per-image state `review_ready`, `rewrite_pending`, `audit_pending`, or `error`

This gate is optional and implementation-profile dependent. It may enrich or defer review work, but it must not bypass the mandatory human review checkpoints.

### Step 4. Human Review A: Caption Approval

- Input:
  - image plus draft caption
- Process:
  - approve the draft caption
  - or edit and approve it
- Output:
  - `caption_review.jsonl`
  - `approved_caption`
  - per-image state `caption_approved` or `caption_edited`

### Step 5. Retrieval Input Generation

- Input:
  - image
  - approved caption
  - optional structured table outputs from the conditional table branch
- Process:
  - generate embedding input
  - generate retrieval query
  - merge row-level structured signals when the table branch is active
- Output:
  - `retrieval_input.jsonl`
  - per-image state `retrieval_ready`

Retrieval merge rule:

- if row-grounded structured output is already available, merge it into retrieval input generation
- if it is not yet available and table enrichment is optional, proceed with caption-only retrieval input and mark the structured enrichment as deferred
- if the current request explicitly requires table-grounded retrieval before candidate retrieval, do not advance to Step 6 until the row chunk artifact exists or the table branch transitions into retry or manual-review handling

### Step 6. Candidate Retrieval

- Input:
  - retrieval input
  - document store index
- Process:
  - retrieve broad candidates
  - store scores and retrieval evidence
- Output:
  - `retrieval_candidates.jsonl`
  - per-image state `candidates_retrieved`

### Step 7. Reranked Top-5 Generation

- Input:
  - candidate set
  - image
  - approved caption
- Process:
  - rerank candidates
  - produce final top-5 review list
- Output:
  - `reranked_top5.jsonl`
  - per-image state `reranked`

### Step 8. Human Review B: Mapping Decision

- Input:
  - image
  - approved caption
  - reranked top-5 candidates
- Process:
  - select final mapping
  - or mark the image as an outlier
- Output:
  - `mapping_review.jsonl`
  - per-image state `mapping_selected` or `outlier_labeled`

### Step 9. Human Review C: Outlier Description

- Input:
  - outlier-labeled image
  - approved caption
  - reviewer notes
- Process:
  - write manual description for unmatched images
- Output:
  - `manual_description.jsonl`
  - per-image state `manual_description_done`

### Step 9A. Mutation Commit Gate

- Input:
  - registry records
  - execution records
  - approved caption or approved review result
  - rename candidate when rename is enabled
- Process:
  - re-read registry state
  - re-read execution state
  - confirm evidence completeness
  - confirm mutation preconditions before metadata write or rename
- Output:
  - mutation-ready status
  - per-image state `mutation_ready` or `mutation_blocked`

Minimum checks:

- `caption` or approved review result exists
- phase-specific status is `completed`, `approved`, or equivalent success state
- execution `state = completed`
- `finished_at` exists
- `evidence` is non-empty
- `rename_candidate` exists when rename is enabled

### Step 10. Metadata Write-Back

- Input:
  - approved caption
  - image file
  - selected mapping or manual description context when applicable
- Process:
  - write metadata to the image file
  - verify the write-back
- Output:
  - updated file or failure record
  - per-image state `metadata_written` or `metadata_write_failed`

### Step 11. Filename Rename

- Input:
  - approved caption
  - image file
- Process:
  - build rename candidate
  - apply safety checks
  - rename through filesystem MCP when enabled
- Output:
  - updated `current_path`
  - per-image state `renamed` or `rename_failed`

### Step 12. Final Content Assembly

- Input:
  - image
  - approved caption
  - selected document or manual outlier description
  - optional worksheet or row-grounded structured outputs from the table branch
- Process:
  - assemble per-image or per-slide content block
  - merge mapped-document context for normal images
  - merge manual description for outliers
  - attach structured worksheet outputs when requested
- Output:
  - `final_content_manifest.jsonl`
  - per-image state `content_assembled`

### Step 13. Presentation Rendering

- Input:
  - final content manifest
  - image files
  - approved captions
  - descriptions
- Process:
  - render the output presentation
- Output:
  - `output_presentation.pptx`
  - job state `rendered`

### Step 14. Final Validation And Packaging

- Input:
  - rendered presentation
  - all manifests
- Process:
  - verify no missing images
  - verify no unapproved captions
  - verify no outlier missing manual description
  - package deliverables
- Output:
  - `output_presentation.pptx`
  - `final_job_report.json`
  - job state `completed`

### Conditional Table Branch

This branch is enabled only when an extracted or supplied image contains table-like or worksheet-like content.

#### Table Branch T1. File Normalization

- normalize PDF pages or table-bearing images into page-level inputs

#### Table Branch T2. Layout Analysis

- identify table, header, and text regions

#### Table Branch T3. Table Extraction

- crop table regions and prepare table images

#### Table Branch T4. Structure Recognition

- infer rows, columns, cells, and merged spans

#### Table Branch T5. Canonical Normalization

- normalize into `Table -> Row -> Cell` JSON

#### Table Branch T6. Row Chunking And Vectorization

- create row-grounded chunks
- embed and store them in the vector index

#### Table Branch T7. Worksheet Export

- build optional worksheet exports

#### Table Branch T8. MCP Exposure

- expose structured table outputs through MCP tools and resources

### Table Branch Merge Rules

- The table branch may begin after image extraction for eligible images.
- The table branch does not replace the caption-review path.
- Row-level table outputs may enrich retrieval input generation.
- Worksheet and table MCP outputs join the pipeline again at final content assembly and final output packaging.
- If the image has no usable table structure, the branch is skipped without blocking the primary image pipeline.
- If row-level table outputs are not ready by Step 5 and table enrichment is optional, retrieval proceeds with caption-only input and the structured merge is deferred.
- If row-level table outputs are mandatory for the active request, candidate retrieval must wait until row chunks exist or the table branch enters `table_retry_pending` or `table_manual_review_required`.

### Parent Verification Protocol

Before transitioning an image to the next phase, the orchestrator must re-read both the registry and execution records and verify:

1. required data for the current phase exists
2. phase-specific status field is `completed`, `approved`, or equivalent success state
3. execution `state` is `completed`
4. `finished_at` is populated
5. `evidence` is non-empty

For rename-enabled phases, `rename_candidate` must exist before rename can begin.

For table-branch phases, the corresponding structured artifact must exist before the branch can advance:

- canonical table JSON
- row chunk artifact
- worksheet export when worksheet output is enabled

If any verification check fails, the image or branch is marked failed and queued for retry or manual review.
For the table branch, this means transitioning into `table_retry_pending` for recoverable failures or `table_manual_review_required` when retries are exhausted or the failure is not safely recoverable.

### Aggregation Metrics

The final job report must contain at minimum:

- `total_images`
- `caption_completed`
- `mapping_completed`
- `outlier_completed`
- `metadata_completed`
- `rename_completed`
- `failed_count`
- `failed_items`
- `retry_queue`

When the table branch is active, also include:

- `table_candidate_count`
- `table_parsed_count`
- `row_chunked_count`
- `worksheet_exported_count`
- `table_mcp_exposed_count`

## Human Review Gates

The human-in-the-loop stages remain mandatory:

1. 이미지 캡션 적합 여부 검토
2. 부적합 캡션 직접 수정
3. reranker top-5 매핑 후보 순위 검토
4. 최종 매핑 결정 또는 outlier labeling
5. outlier 이미지 설명 직접 작성

## MCP / Skill / SubAgent Architecture

- Skill:
  - orchestration and subagent execution only
- MCP:
  - source of truth for execution state and data state
- SubAgent:
  - one image per worker when image-isolation is required

Reference:

- Tool Inventory (local/private registry): `<LOCAL_AGENT_REGISTRY>/tools/tool_inventory.json`
- MCP Setup Reference (local/private tools inventory): `<LOCAL_AGENT_REFERENCE_ROOT>/tools_inventory/REFERENCE_mcp_setup.md`

Recommended ownership split:

- execution state: `agent-task-manager-mcp`
- image registry and progress ledger: `conport`
- caption generation and metadata candidates: `cv-mcp`
- metadata write-back: `ExifTool_MCP`
- file rename or move: `filesystem`
- presentation download or export when available: `Canva MCP`

## Canonical Data Direction

The current image pipeline canonical direction is:

```text
Presentation
-> Extracted Image
-> Caption Record
-> Review Record
-> Retrieval / Rerank Candidate Record
-> Human Decision
-> Regenerated Presentation Asset
```

## Appended Extension: Table/Row/Column Worksheet And Optional RAG Path

The image pipeline is extended with a structured document-table path when the extracted or supplied image contains tables or worksheet-like content.

### Extended Purpose

- parse document images into `Table -> Row -> Cell`
- rebuild worksheet exports
- expose structured access over MCP
- support optional row-grounded retrieval after parser-side structure is stable

### Extended Canonical Model

For table-bearing images, the canonical structure becomes:

```text
Image
-> Table
-> Row
-> Cell
-> Canonical Parsed Record
-> Worksheet
-> MCP Tool / Resource
-> Optional Row Chunk
-> Optional Vector Index
```

### Extended Execution Flow

1. file intake
2. page normalization
3. image preprocessing
4. layout analysis
5. table crop extraction
6. row/column/cell recognition
7. canonical schema normalization
8. confidence and structure validation
9. structured persistence
10. worksheet export
11. MCP exposure
12. optional row-based chunking
13. optional embedding and vector indexing

### Extended Canonical Schema

For table-bearing images, the canonical `Table -> Row -> Cell` JSON structure is:

```json
{
  "document_id": "...",
  "page": 1,
  "table_id": "t1",
  "rows": [
    {
      "row_index": 0,
      "cells": [
        {
          "col_index": 0,
          "text": "...",
          "row_span": 1,
          "col_span": 1,
          "bbox": [0, 0, 0, 0],
          "confidence": 0.97
        }
      ]
    }
  ]
}
```

This structure is the shared source for worksheet export, MCP access, and optional later-stage RAG preparation.

### Optional RAG Consumer Policy

- row is the primary retrieval unit
- cell metadata is grounding evidence
- worksheet export is derived from the same canonical table structure

Row chunk example:

```json
{
  "content": "2023년 매출은 120억",
  "metadata": {
    "table_id": "t1",
    "row": 3,
    "column": "매출",
    "page": 2
  }
}
```

### Optional RAG Query-Time Flow

1. user question
2. vector search over row or table chunks
3. candidate row and table retrieval
4. optional MCP tool call for exact cell lookup
5. answer plus row or cell grounding

### Extended MCP Surface

Example tool family:

- `parse_document(file_uri, granularity)`
- `get_tables(document_id)`
- `get_table_rows(table_id)`
- `get_cells(table_id)`
- `build_worksheet(document_id)`

Example resource URIs:

- `doc://parsed/{id}`
- `table://{id}.json`
- `file://exports/{id}.xlsx`

### Extended Fallback Policy

- low OCR confidence: retry with alternative parser
- broken structure: switch to high-resolution parsing mode
- repeated failure: send to manual review queue

### Extended Success Criteria

- table structure accuracy above 90%
- row retrieval accuracy above 85%
- worksheet reconstruction error below 5%
- reduced hallucination in table-grounded RAG

## Output Families

- extracted images
- execution records
- caption ledgers
- evaluation decision artifacts
- unsupported-media artifacts
- review artifacts
- retrieval candidate artifacts
- mapping decisions
- outlier manual descriptions
- audit packages
- error records
- regenerated presentation outputs
- optional worksheet exports
- optional table-grounded MCP resources

## State Transitions

### Image-Level State Flow

```text
extracted
  -> unsupported_media_type
  -> [caption-eligible only] caption_drafted
  -> caption_approved | caption_edited
  -> retrieval_ready
  -> candidates_retrieved
  -> reranked
  -> mapping_selected | outlier_labeled
  -> [outlier only] manual_description_done
  -> [optional] metadata_written
  -> [optional] renamed
  -> content_assembled
  -> finalized
```

Constraints:

- `mapping_selected` and `outlier_labeled` are mutually exclusive
- outlier items must pass through `manual_description_done` before content assembly
- `metadata_written` and `renamed` are optional terminal enrichments
- `unsupported_media_type` items do not enter automated caption generation unless a separate conversion pass creates a supported asset

### Optional Evaluation-Gate State Overlay

When the optional evaluation gate is enabled, the image-level state flow may temporarily pass through:

```text
caption_drafted
  -> review_ready | rewrite_pending | audit_pending | error
  -> [rewrite path] caption_drafted
  -> [review path] caption_approved | caption_edited
```

Constraints:

- `review_ready` feeds into the same mandatory human review path
- `audit_pending` does not authorize metadata write or rename
- `error` is terminal for the affected automated branch until retry or manual intervention

### Table-Branch State Flow

```text
table_candidate
  -> layout_analyzed
  -> table_extracted
  -> structure_recognized
  -> table_normalized
  -> row_chunked
  -> [optional] worksheet_built
  -> [optional] mcp_exposed

recoverable branch failure
  -> table_retry_pending
  -> layout_analyzed | table_extracted | structure_recognized | table_normalized

non-recoverable failure or retry-budget exhaustion
  -> table_manual_review_required
```

Constraints:

- table-branch states apply only to eligible images
- the table branch may run in parallel with caption and mapping stages
- table-branch completion is not required for non-table images
- `table_retry_pending` is the only recoverable retry state for the branch
- `table_manual_review_required` is terminal until a human or a new bounded rerun reactivates the branch

### Job-Level State Flow

```text
initialized
  -> source_downloaded
  -> images_extracted
  -> captions_reviewed
  -> retrieval_completed
  -> mapping_reviewed
  -> content_assembled
  -> rendered
  -> completed
```

Job state advances only when all required image-level states for that phase are satisfied.

## Re-Run Rules

- source presentation changed:
  - rerun from export/download stage
- extraction logic changed:
  - rerun from image extraction
- caption changed:
  - rerun from retrieval input generation
- mapping changed:
  - rerun from final content assembly
- outlier description changed:
  - rerun from final content assembly
- table parser changed:
  - rerun from layout analysis for affected documents
- row chunk schema changed:
  - rerun from row chunking for affected table-bearing images
- worksheet export logic changed:
  - rerun from worksheet export for affected table-bearing images
- MCP table surface contract changed:
  - rerun MCP exposure packaging for affected table-bearing images

## Artifacts And Directory Layout

```text
/control/project_domain/resources/jobs/{job_id}/
  source/
    source_presentation.pptx
    source_metadata.json
  images/
    img_000001.png
    img_000002.png
    ...
  manifests/
    job_manifest.json
    image_manifest.jsonl
    unsupported_media_manifest.jsonl
    execution_records.jsonl
    table_candidate_manifest.jsonl
    caption_draft.jsonl
    evaluation_decisions.jsonl
    caption_review.jsonl
    retrieval_input.jsonl
    retrieval_candidates.jsonl
    reranked_top5.jsonl
    mapping_review.jsonl
    manual_description.jsonl
    final_content_manifest.jsonl
  structured/
    table_manifest.jsonl
    row_chunks.jsonl
    worksheet_manifest.json
  audit/
    audit_queue.jsonl
    {image_id}.audit.json
  errors/
    error_queue.jsonl
    {image_id}.error.json
  final/
    result_records.jsonl
    final_job_report.json
  output/
    output_presentation.pptx
    exports/
      {doc_id}.xlsx
  mcp/
    parsed_resources.json
  logs/
    run_{timestamp}.jsonl
```

Required human-review artifacts:

- `caption_review.jsonl`
- `mapping_review.jsonl`
- `manual_description.jsonl`

Required evaluation and mutation-control artifacts when those paths are enabled:

- `execution_records.jsonl`
- `evaluation_decisions.jsonl`
- `audit_queue.jsonl`
- `error_queue.jsonl`

Required final packaging artifacts:

- `final_job_report.json`
- `output_presentation.pptx`

## Operational Notes

- Master plan is append-oriented. Add new bounded extensions rather than rewriting prior canonical sections.
- MCP-backed records remain the truth source for state and result confirmation.
- Tool-specific execution details belong in spec, run, or troubleshooting docs, not in this master plan.
- Before phase 2 or later active arms begin, active machine-readable artifacts should return to hard-fail-free lint status; legacy `phase1_caption_10w` packet and ledger filenames must be renamed, reclassified, or archived out of the active surface.

## Current Reviewed Skill Supports

The current workspace now has explicit review-gated skill surfaces for the preprocessing and review layers:

- `openai-image-caption-validation`
- `obsidian-caption-review-builder`
- `object-isolation-correction`
- `component-split-ocr-review`
- `transparent-component-triage`
- `parser-sidecar-to-canonical-schema-promotion`
- `table-branch-activation-slice`
- `vendored-mcp-onboarding`

These skills support the master plan, but do not change the truth-source rule:

- runtime truth still belongs to bounded manifests, reports, ledgers, and smoke evidence
- reviewed object isolation remains a branch, not the default baseline

## Next Active Paths

Completion status on the bounded table branch:

- triage selection gate: completed
- `paddleocr-mcp` boot smoke: completed
- first real-image `PP-StructureV3` smoke: completed on `image11.png`
- first canonical `Table -> Row -> Cell` normalization: completed on `image11.png`
- read-only local wrapper implementation: completed
- bounded downstream consumer smoke on the wrapper: completed

Next active order:

1. build reviewed context packages on the `full-image + standalone OCR` baseline
2. rerun caption generation on the context-enriched full-image surface
3. run bounded evaluation overlay on top of that context-enriched full-image baseline
4. if needed, run a second bounded `PP-StructureV3` smoke on one more triage-approved table image
5. keep object isolation on a reviewed branch only:
   - `transparent-component-triage` for conservative batch prefiltering
   - `component-split-ocr-review` for one-image deterministic evidence
   - `object-isolation-correction` only after a visible failure or repair need
6. screenshot-based comparison arm after viewer-surface setup

Phase-2 preflight gate:

- `phase1_caption_experiment_summary_at2026_03_27.json` remains the current phase-1 truth artifact
- the single `.emf` unsupported case remains explicitly explained
- component isolation, OCR evidence, and context-package preparation have either been completed or explicitly waived for the next active experiment
- the bounded table-branch activation sequence has either been completed or explicitly waived for the current active arm
- legacy `phase1_caption_10w` machine-readable filenames are cleaned up or reclassified so new active runs do not inherit hard lint failures

## Current Appended Extensions

1. `Image -> Table/Row/Column -> Worksheet -> MCP -> Optional RAG`
2. `PPT extracted media -> component isolation/capture -> OCR/context package -> component caption/evaluation`
3. `full-image standalone OCR -> reviewed context package -> context-injected caption rerun`

## Appended Patch: Baseline Realignment At 2026-03-28

This bounded patch records the current active baseline after the recent phase0 object-isolation and OCR smokes.

### Current Baseline Decision

Use this baseline by default:

1. PPT-extracted full original image
2. standalone OCR on that full image
3. reviewed context package with OCR evidence plus PPT-local summary
4. context-injected caption rerun

### Current Object-Isolation Interpretation

Object isolation remains available, but only on a reviewed branch.

Reason:

- automatic semantic selection is still not reliable enough for unattended batch promotion
- transparent alpha-connected components are useful as deterministic evidence, not as automatic semantic truth
- component review and correction are now supported by dedicated skills, but they do not replace the default baseline

### Review-Gated Branches

Current reviewed branches are:

- `transparent-component-triage`
- `component-split-ocr-review`
- `object-isolation-correction`

These branches may inform later caption reruns, but only after bounded human review or explicit promotion criteria.

## Appended Patch: Table Branch Execution Plan At 2026-03-27

This bounded patch clarifies the operational execution plan for the existing table extension. It does not replace the earlier table-extension summary. It narrows the branch into explicit entry conditions, canonical data flow, merge points, and non-blocking failure rules.

### Patch Intent

- make the conditional table branch operational rather than aspirational
- define one canonical logical-table model before any RAG, worksheet, or MCP export
- let structured table outputs enrich the main pipeline without blocking non-table image flow

### Entry Conditions

The table branch may start in either of the following ways:

1. after Step 2 image extraction, when an extracted image is marked `table_candidate`
2. from a direct external request where the input is already a raster document page or table image

The branch should be activated by any of the following signals:

- lightweight heuristics from the extracted image
- manual operator flag
- explicit request mode requiring `table`, `row_column`, `worksheet`, or `rag`

If no credible table signal exists, the branch is skipped and the primary caption and mapping path continues unchanged.

### Table-Branch Source Of Truth

For table-bearing inputs, the branch should persist and re-read the following canonical objects:

- `request_record`
- `document_asset`
- `page_asset`
- `detected_table`
- `structural_cell`
- `logical_table_model`
- `quality_report`

The `logical_table_model` is the required shared source for:

- `table.json`, `table.html`, `table.md`
- `rows.json`, `columns.json`, `cells.json`
- row-grounded retrieval chunks
- `output.csv`, `output.xlsx`
- MCP tool and resource exposure

### Detailed Execution Order

#### TB0. Request Registration

- Input:
  - file path or URI
  - mime type
  - optional `page_range`, `language_hint`, `requested_outputs`
- Process:
  - issue stable `job_id`
  - register source asset
  - record requested structured-output mode
- Output:
  - `request_manifest.json`
  - `document_id`

#### TB1. Input Registration And Page Materialization

- Input:
  - raw file or extracted image
- Process:
  - hash the input
  - deduplicate against prior runs when applicable
  - split PDF or multi-page input into page images when needed
- Output:
  - `page_id[]`
  - page-level image registry

#### TB2. Image Normalization

- Process:
  - resolution adjustment
  - grayscale or binarization
  - denoise
  - skew and rotation correction
  - contrast normalization
  - optional line enhancement
- Output:
  - normalized page image
  - preprocessing log

#### TB3. Document-Type Classification And Table Detection

- Process:
  - classify single-table image vs mixed-layout page vs multi-table page
  - detect table bounding boxes
  - crop each table region
- Output:
  - `document_type`
  - `table_candidate_regions`
  - `table_id[]`
  - `table_crop_image`

#### TB4. Parsing Strategy Selection

- Process:
  - choose line-based segmentation for grid tables
  - choose text-alignment inference for borderless tables
  - enable stronger span recovery for merge-heavy tables
- Output:
  - `selected_parsing_strategy`
  - structure-model configuration

#### TB5. Structural Grid Extraction

- Process:
  - estimate row and column counts
  - generate cell boxes
  - infer merged spans
  - mark header candidates
- Output:
  - `structural_grid`
  - cell coordinate records
  - span metadata

#### TB6. OCR And Cell-Text Alignment

- Process:
  - run page-level or cell-level OCR
  - capture token confidence
  - map OCR tokens into cell boxes
  - merge multiline cell text
  - restore reading order
- Output:
  - `text_tokens`
  - `token_to_cell_mapping`
  - cell text records

#### TB7. Logical Table Reconstruction

- Process:
  - identify header rows
  - separate body rows
  - classify summary or footnote rows
  - identify stub columns
  - link internal or external caption when available
- Output:
  - `logical_table_model`
  - `header_rows`
  - `body_rows`
  - `summary_rows`
  - `caption_link`

#### TB8. Quality Validation And Retry Gate

- Process:
  - check empty-cell ratio
  - check row or column stability
  - check OCR confidence threshold
  - detect span conflicts
  - validate typed values when possible
- Retry or fallback conditions:
  - low average confidence
  - unstable row or column count
  - excessive duplicate cells
  - header/body separation failure
- Output:
  - `quality_report`
  - `retry_flag`
  - corrected logical table model

#### TB9. Output Branching

Once the corrected logical table model exists, downstream outputs branch as follows:

- Table export:
  - `table.json`
  - `table.html`
  - `table.md`
  - `table_summary.txt`
- Row and column export:
  - `rows.json`
  - `columns.json`
  - `cells.json`
  - `normalized_matrix.json`
- Retrieval export:
  - row-grounded chunks
  - `retrieval_metadata.json`
- Worksheet export:
  - `output.csv`
  - `output.xlsx`
  - `worksheet_manifest.json`
- MCP exposure:
  - structured table resources
  - exact lookup tools when enabled

### State-Flow Compression Rule

The earlier table-branch state flow remains valid as a compressed status model. The detailed steps above map into it as follows:

- `TB2` and the document-side portion of `TB3`:
  - `layout_analyzed`
- table crop creation in `TB3`:
  - `table_extracted`
- `TB4`, `TB5`, `TB6`, and `TB7`:
  - `structure_recognized`
- `TB8`:
  - `table_normalized`
- retrieval branch materialization in `TB9`:
  - `row_chunked`
- worksheet branch materialization in `TB9`:
  - `worksheet_built`
- MCP resource or tool exposure in `TB9`:
  - `mcp_exposed`
- recoverable failure after any branch phase:
  - `table_retry_pending`
- exhausted or non-recoverable branch failure:
  - `table_manual_review_required`

### Merge Points Back Into The Main Pipeline

The table branch rejoins the parent pipeline at the following points:

- Step 5 retrieval input generation:
  - row-grounded or table-grounded structure may enrich retrieval input after caption approval
- Step 12 final content assembly:
  - structured table summaries, HTML previews, or worksheet exports may be attached when requested
- Step 14 final validation and packaging:
  - structured table artifacts must be included only for images or requests where the branch was explicitly enabled

Step 5 decision rule:

- default:
  - do not block retrieval input generation on table enrichment
- exception:
  - when the active request requires table-grounded retrieval before candidate retrieval, Step 5 waits for the row chunk artifact
- failure handling while waiting:
  - if the table branch moves to `table_retry_pending`, retrieval remains blocked only for requests that explicitly require table-grounded retrieval
  - if the table branch moves to `table_manual_review_required`, the parent must either downgrade the request scope or escalate to manual review instead of silently continuing

### Non-Blocking Rule

The table branch is enrichment-first, not globally blocking.

- non-table images must not wait for table parsing
- caption review and mapping review must still proceed when the table branch is skipped
- worksheet export failure must not invalidate successful caption and mapping work
- table-branch failure becomes blocking only when the request explicitly requires structured table outputs as a deliverable

### Table-Branch Parent Verification

Before the orchestrator marks a table-bearing image phase as complete, it must re-read MCP-backed records and verify:

1. the required structured artifact exists for the current branch phase
2. the branch-specific status is `completed`, `approved`, or equivalent success state
3. execution `state = completed`
4. `finished_at` is present
5. `evidence` is non-empty

Minimum artifact checks by phase:

- after logical reconstruction:
  - corrected logical table model exists
- before row-grounded retrieval enrichment:
  - row chunk artifact exists
- before worksheet packaging:
  - worksheet manifest exists when worksheet output is enabled
- before MCP exposure completion:
  - exposed resource manifest exists when MCP exposure is enabled

Retry-state rule:

- `table_retry_pending` must include at minimum:
  - failed phase
  - attempt count
  - retry reason
  - planned re-entry phase
- `table_manual_review_required` must include at minimum:
  - blocking artifact
  - last error
  - evidence references

### Recommended Delivery Order

The implementation order for this branch remains:

1. `Image -> Table`
2. `Image -> Row/Column`
3. `Image -> Worksheet`
4. `Image -> RAG and MCP exposure hardening`

Reason:

- `table` output is the first reusable structured artifact
- `row` and `column` normalization stabilize grounding and filtering
- `worksheet` export should derive from normalized structure, not ad hoc OCR output
- MCP exposure should harden only after schemas and retry policy stabilize

## Appended Patch: Parser-First Active Baseline At 2026-03-28

This bounded patch reorients the active baseline of the workspace toward parser-first experimentation.
Where this patch conflicts with earlier caption-first or retrieval-first wording, this patch wins for active experimentation in this workspace.

### Reorientation Reason

The current workspace is `my-image-parser`.
The active objective is not early RAG optimization.
The active objective is to establish a reliable parser-oriented pipeline for image-derived components, tables, OCR evidence, and parser-conditioned caption comparison.

RAG remains an intended downstream use case, but it is no longer treated as an early or primary execution driver.

### Active Baseline Shift

Earlier sections describe a presentation-caption-mapping-regeneration baseline.
For current experiments, the active baseline becomes:

1. extract image assets from presentation or direct image inputs
2. isolate image components when the image is compound or visually dense
3. attempt table extraction on relevant isolated components
4. extract OCR evidence from full images or isolated components
5. normalize parser or OCR outputs into canonical records
6. run caption comparison experiments on top of parser and OCR evidence
7. defer RAG, retrieval enrichment, worksheet hardening, and MCP consumer hardening until parser quality is stable

### Active Canonical Data Direction

For current parser-first experiments, the canonical direction is:

```text
Presentation Or Direct Image
-> Extracted Image
-> Isolated Component
-> Table Parsing Attempt
-> OCR Evidence
-> Canonical Parsed Record
-> Caption Comparison Record
-> Optional Worksheet / RAG / MCP Consumer Surface
```

Interpretation:

- caption is now a downstream consumer of parser and OCR evidence, not the earliest core artifact
- RAG is now a later consumer of stabilized parsed structure, not the primary near-term driver
- worksheet export remains useful, but only after canonical parsed records are trustworthy

### Active Experimental Order

The current preferred execution order is:

1. presentation export or direct image intake
2. image extraction and per-image registration
3. component isolation or component split when needed
4. per-component table extraction attempt
5. OCR extraction on full image and isolated components
6. parser-sidecar or OCR-sidecar normalization into canonical schema
7. caption-arm comparison over at least four bounded modes
8. human review of parser and caption evidence as needed
9. optional worksheet export from accepted canonical structure
10. optional RAG preparation after parser-side correctness is accepted

### Four-Mode Caption Comparison Position

The current caption experiment should be described as parser-conditioned comparison, not caption-only generation.

Minimum comparison framing:

- caption from full image baseline
- caption from isolated component view
- caption from OCR-evidence-enriched input
- caption from parser or table-structure-enriched input

The exact arm names may vary by implementation profile, but the comparison position in the pipeline should remain after component isolation and parser or OCR evidence collection.

### RAG Deferral Rule

For active experiments in this workspace:

- do not position RAG as the main near-term success criterion
- do not force retrieval integration ahead of parser-quality stabilization
- treat row chunks, retrieval metadata, and vector indexing as downstream outputs that become meaningful after canonical parsed records are stable enough

This means the earlier RAG-oriented table branch is still valid as a consumer path, but it is not the active driver for the current experimental phase.

### Section Override Map

For active parser-first experiments, reinterpret earlier sections as follows:

- `Purpose`:
  - keep the historical presentation pipeline context, but read parser-first experimentation as the active operational baseline
- `Core End-To-End Flow`:
  - treat the earlier caption-to-retrieval sequence as a downstream consumer path, not the first experimental path
- `Canonical Data Direction`:
  - replace caption-first reading with the parser-first direction in this patch
- `Appended Extension: Table/Row/Column RAG And Worksheet Path`:
  - treat this as an active parser track, not merely a side extension
- `Next Active Paths`:
  - interpret component isolation, parser activation, OCR evidence, and comparison runs as the primary current work

### Immediate Master-Plan Consequence

The master plan title remains unchanged for continuity, but the workspace should now be understood operationally as:

- a parser-first image understanding workspace
- with caption, worksheet, and RAG paths as staged downstream consumers
- and with presentation regeneration kept as a later integration target rather than the only organizing center

## Draft Registry

Active drafts that inform but remain outside the canonical master plan:

### Implementation Profiles

- `PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md`
  - Role: implementation profile for cv-mcp + moondream independent evaluation path
  - Covers: per-image batch flow, decision gate (accept/rewrite/audit/error), evaluation metrics, metadata tag mapping, rename safety rules
- `PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md`
  - Role: implementation profile for MCP-first orchestration with one-image-one-subagent pattern
  - Covers: registry-first persistence, execution record model, commit gate, worker input minimization

### Source References

- `PLAN_canva_presentation_image_mapping_data_flow-at2026-03-27-15-29.md`
  - Role: original detailed data flow plan
  - Status: core content merged into this master plan (operational assumptions, data objects, step flow, state transitions)
- `PLAN_presentation_image_mapping_extension-at2026-03-27-15-29.md`
  - Role: original extension proposal adding retrieval and human review to the baseline
  - Status: fully absorbed into the master plan core flow
- `PLAN_image_table_row_rag_worksheet_mcp-at2026-03-27-15-29.md`
  - Role: inherited table-branch reference plan from a RAG-oriented framing
  - Status: partially merged into the appended table extension; retains detailed parser and fallback specifics, but should be read as a reference artifact rather than the active workspace baseline

### Reference Contamination Note

- Some wording in the table branch and downstream consumer sections originated from a RAG-oriented reference workspace and draft lineage.
- For the current `my-image-parser` workspace, that material should be interpreted as inherited reference context, not as the primary execution priority.
- The active operational baseline is defined by the parser-first patch above, where `component isolation -> table parsing attempt -> OCR evidence -> caption comparison` comes before optional RAG preparation.

### External Good-Case References

- External reference index (local/private registry): `<LOCAL_AGENT_REGISTRY>/external_reference_index.json`
  - Machine-readable index for external good-case references, template sources, and source directories that stay indexed-only outside the active workspace tree.
- Decision Framework Template: `<EXTERNAL_TEMPLATE_ROOT>/decision_framework.md`
  - Used as a reference for ADR and closed-question capture structure in user decision records.
- Template Directory: `<EXTERNAL_TEMPLATE_ROOT>`
  - Used as a reference source for reusable document forms that may later be promoted into team templates.
- Agent Tool Benchmark Knowledge Base Good Case: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/agent-tool-benchmark/knowledge_bases/agent-tool-benchmark-kb-at2026-03-24.md`
  - Used as a reference for clean frontmatter, a short purpose statement, source-of-truth rules, and simplification boundaries in reusable knowledge-style documents.
- Codebase Analysis Spec Good Case: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/codebase-analysis/references/codebase-analysis-spec-at2026-03-23-03-14.md`
  - Used as a reference for stable spec structure with source-of-truth, supporting appendix, functional spec, IO, constraints, API surface, and schema framing.
- Codebase Analysis Directory Reference: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/codebase-analysis`
  - Used as a source-directory reference for codebase graph artifacts and analysis workflow patterns in project-agent operations.
- Codebase Analysis Development Playbook Good Case: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/codebase-analysis/references/codebase-analysis-development-playbook-at2026-03-23-03-36.md`
  - Used as a reference for workflow, TDD, smoke-test ordering, task-packet operation, and workspace or environment policy.

### Exploratory Drafts

- `PLAN_image_obsidian_style_parsing-at2026-03-27-15-27.md`
  - Role: broader multi-format conversion architecture (PPT → Canonical IR → Obsidian/JS/Python/Worksheet)
  - Status: exploratory; extends beyond the current pipeline scope
- `PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md`
  - Role: 4-arm experiment comparison framework for caption execution paths
  - Status: exploratory; experiment plan, not pipeline architecture

### Apple Vision Helper Strategy

- Apple Vision document recognition is treated as a helper-script surface, not a new first-class MCP requirement.
- Its role is limited to recovering table skeleton hints such as table bbox, row and column grouping, span hints, and per-cell transcript candidates.
- Any Apple-derived structure sidecar must still pass through canonical normalization before downstream `get_tables`, `get_table_rows`, or `get_cells` consumers read it.
- The active parser path remains `paddleocr-mcp` for bounded table parsing, with Apple Vision reserved for helper evidence or disagreement resolution.

## One-Line Summary

The canonical presentation pipeline extracts images, builds parser and OCR evidence under MCP-backed control, compares caption paths on top of that parsed evidence, regenerates presentation assets, and only later exposes optional worksheet, MCP, and RAG consumer paths.

## Appended Patch: Core 4-Mode Readiness At 2026-03-28

- `full_image_baseline`: ready
- `full_image_ocr_context_rerun`: ready for comparison, still `pending_review`
- `parser_table_enriched_rerun`: ready for comparison, still `pending_review`
- `reviewed_isolated_component_caption_arm`: blocked by explicit waiver

Current operational interpretation:

- the workspace is now ready for a bounded `3-mode` comparison on `image11.png`
- it is not yet ready for the intended `4-mode` comparison because the isolated-component arm is still waived
- object isolation remains a reviewed branch only and must not be promoted into the unattended default path

## Appended Patch: Reviewed Isolated Component Arm Closure At 2026-03-28

- `reviewed_isolated_component_caption_arm` has now been reopened and closed on `01_full_presentation_2026-03-17:image11.png`
- the bounded reviewed surface is a table-only crop derived from merged table candidate evidence, not a raw alpha component
- reviewed component OCR preserved `16 / 16` expected table tokens and reduced extraneous tokens from `7` to `0`
- bounded rerun ledger closed successfully:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase0_reviewed_isolated_component_rerun_image11_at2026_03_28.json`
- current bounded 4-mode readiness is now:
  - `full_image_baseline`: ready
  - `full_image_ocr_context_rerun`: ready for comparison
  - `parser_table_enriched_rerun`: ready for comparison
  - `reviewed_isolated_component_rerun`: ready for comparison
- updated bounded 4-mode verdict: `Yes`
- baseline policy does not change:
  - full image remains the active default baseline
  - reviewed isolated components remain a reviewed branch only

## Appended Patch: Phase1 Small-Batch 4-Mode Closure At 2026-03-29

- `phase1` small-batch aggregate producer is now canonicalized on:
  - `image11`
  - `image7`
  - `image8`
  - `image10`
  - `image9`
- stale aggregate drift is closed:
  - `phase1_caption_four_mode_small_batch_bundle_at2026_03_28.json` is now a canonical aggregate bundle again
- downstream consumer truth is also closed:
  - `phase1_caption_four_mode_small_batch_auto_eval_true_batch_at2026_03_28.json` now evaluates the same `5-image` set
  - consumer input supports both aggregate bundle and per-image bundle fallback
- semantic judge remains waived for now:
  - the current lane is `proxy auto-eval + semantic judge waiver`
- default policy still does not change:
  - `full_image_baseline` remains the active default baseline
  - `comparison winner` remains separate from `default replacement`
- current policy source:
  - `control/project_domain/resources/specs/prose/SPEC_caption_arm_promotion_policy.md`

## Appended Patch: Phase1 Corpus-Wide 4-Mode Eligibility Scan At 2026-03-29

- request shape:
  - extend `4-mode` comparison toward a `20-image` batch
- actual available corpus:
  - `14` images are present under `pptx_jobs/01_full_presentation_2026-03-17/media`
- evidence-only corpus scan is now recorded:
  - canonical candidates: `phase1_caption_four_mode_corpus_candidates_at2026_03_29.json`
  - canonical ready-subset aggregate: `phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json`
  - canonical exclusions: `phase1_caption_four_mode_corpus_excluded_at2026_03_29.json`
  - scan report: `REPORT_phase1_caption_four_mode_corpus_scan-at2026-03-29-00-55.md`
- stable `4-mode`-ready subset remains:
  - `image7`
  - `image8`
  - `image9`
  - `image10`
  - `image11`
- exclusions are now explicit:
  - `image4` remains excluded as a mixed chart-table edge case
  - all other excluded images are missing one or more frozen derived-arm artifacts
- interpretation:
  - current repo supports a stable `5-image` `4-mode` cohort, not a stable `14-image` or `20-image` `4-mode` cohort
  - next expansion work is to freeze more derived arms, not to widen the default baseline policy

## Appended Patch: Phase1 Corpus Expansion Closure At 2026-03-30

- bounded expansion work after the `5-image` cohort has now been closed for the remaining non-edge-case table-centric images:
  - `image12`
  - `image13`
  - `image14`
  - `image15`
- canonical per-image `4-mode` bundles now exist for those images:
  - `phase1_image12_caption_four_mode_eval_bundle_at2026_03_30.json`
  - `phase1_image13_caption_four_mode_eval_bundle_at2026_03_30.json`
  - `phase1_image14_caption_four_mode_eval_bundle_at2026_03_30.json`
  - `phase1_image15_caption_four_mode_eval_bundle_at2026_03_30.json`
- corpus-level canonical truth is now:
  - candidates: `phase1_caption_four_mode_corpus_candidates_at2026_03_29.json`
  - ready bundle: `phase1_caption_four_mode_corpus_ready_bundle_at2026_03_29.json`
  - excluded set: `phase1_caption_four_mode_corpus_excluded_at2026_03_29.json`
  - auto-eval manifest: `phase1_caption_four_mode_corpus_auto_eval_true_batch_at2026_03_30.json`
  - auto-eval report: `REPORT_phase1_caption_four_mode_corpus_auto_eval_true_batch-at2026-03-30-22-20.md`
  - semantic waiver: `REPORT_phase1_caption_four_mode_corpus_semantic_judge_waiver-at2026-03-30-22-20.md`
  - corpus closure: `REPORT_phase1_caption_four_mode_corpus_closure-at2026-03-30-22-19.md`
- stable `4-mode`-ready subset is now:
  - `image7`
  - `image8`
  - `image9`
  - `image10`
  - `image11`
  - `image12`
  - `image13`
  - `image14`
  - `image15`
- explicit confirmed excludes are now:
  - `image1`: chart-dominant non-table
  - `image2`: mixed chart-table composite
  - `image3`: chart-dominant non-table
  - `image4`: mixed chart-table edge case; bounded deterministic re-entry failed and stays outside the stable cohort
  - `image5`: diagram / non-table
- corpus consumer truth now reports:
  - `image_count = 9`
  - `actual_input_mode = aggregate_bundle`
  - `batch_level_winner_frequency = {'full_image_ocr_context_rerun': 1, 'reviewed_isolated_component_rerun': 8}`
  - `default_baseline_retained = true`
- interpretation:
  - the current repo now supports a stable `9-image` `4-mode` cohort from the available `14-image` corpus
  - `image4` is no longer just a pending edge candidate; it is an explicitly waived manual/special-case lane until a new deterministic parser path exists
  - `reviewed_isolated_component_rerun` is the dominant comparison winner in the expanded cohort, but the active default remains `full_image_baseline`
