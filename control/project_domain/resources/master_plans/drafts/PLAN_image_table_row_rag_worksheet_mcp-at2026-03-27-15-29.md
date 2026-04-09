# Image Table, Row/Column, RAG, and Worksheet Data Flow Plan

## Status

Draft

Current use in this workspace: inherited reference draft, not the active baseline.

## Purpose

이 문서는 이미지 기반 문서에서 표 정보를 추출하여 다음 네 가지 소비 경로로 연결하는 공통 데이터 플로우를 정의한다.

1. `Image -> Table`
   - 표 단위 객체를 추출하고 구조를 보존한 `JSON`, `HTML`, `Markdown`으로 변환한다.
2. `Image -> Row/Column`
   - 행, 열, 셀, 병합셀 구조를 복원하여 질의 가능한 구조 데이터로 정규화한다.
3. `Image -> Worksheet`
   - 복원된 표 구조를 `CSV`, `XLSX`와 같은 편집 가능한 워크시트로 재구성한다.
4. `Image -> RAG`
   - 동일한 구조 데이터를 기반으로 grounded retrieval과 후속 질의를 위한 chunk 및 metadata를 생성한다.

이 문서는 원래 `RAG용 구조화 파싱`을 우선순위로 둔 reference draft였다. 현재 `my-image-parser` workspace에서는 parser-first baseline이 master plan에 별도로 정의되어 있으므로, 이 문서는 active execution order가 아니라 inherited reference로 읽어야 한다. Worksheet export와 MCP read surface는 동일한 canonical structure를 재사용하는 downstream branch로 취급한다.

## Relationship To Existing Plans

이 문서는 기존 presentation-image 중심 master plan을 대체하지 않는다. 역할은 다음과 같다.

- presentation pipeline에서 추출된 `table_candidate` 이미지에 재사용 가능한 인접 확장 draft
- 스캔 문서, 스크린샷, rasterized PDF page에도 적용 가능한 범용 table-structure parsing slice
- caption, retrieval, mapping, presentation regeneration과는 별개로 동작 가능한 구조화 parsing plan

현재 workspace 기준 해석:

- parser-first active baseline은 `MASTER_PLAN_presentation_image_pipeline.md`의 appended parser-first patch가 우선한다.
- 이 draft의 RAG-first phrasing은 historical reference context로 남기고, 실행 우선순위 판단에는 직접 사용하지 않는다.

정렬 대상 상위 문서:

- `MASTER_PLAN_presentation_image_pipeline.md`
- `PLAN_image_caption_pipeline_data_flow-at2026-03-27-15-29.md`
- `PLAN_canva_presentation_image_mapping_data_flow-at2026-03-27-15-29.md`

## Scope

### Inputs

- `PNG`, `JPG`, `JPEG`, `TIFF`, `WebP`
- PDF의 rasterized page image
- 스캔 문서 이미지
- 스크린샷 기반 표 이미지

### Outputs

- table-level `JSON`, `HTML`, `Markdown`
- row, column, cell 단위 `JSON`
- `CSV`, `XLSX` worksheet
- `RAG` chunk metadata
- 품질 점검용 `bbox`, `confidence`, `trace`, `retry_reason`

### Out Of Scope

- 자유서식 전체 문서 이해
- 차트, 도형, 수식의 완전한 의미 해석
- 비표 영역의 정교한 문서 논리 구조 복원
- Excel 원본 파일의 구조 파싱

## Operational Priorities

- Canonical structure first:
  - `Table -> Row/Column -> Cell` 또는 동등한 logical table model을 먼저 고정한다.
- RAG first:
  - 최소 운영 가치는 table 구조와 retrieval metadata에서 먼저 나온다.
- Export later:
  - worksheet export는 canonical structure의 파생 산출물이어야 한다.
- Evidence retention:
  - OCR token, `bbox`, `confidence`, `span`, `retry log`를 함께 저장한다.
- Strategy branching:
  - 격자형, 무선형, 병합셀-heavy table을 동일 파이프라인 안에서 분기 처리한다.

## Core Data Objects

### Request Record

요청 진입 시점의 실행 단위.

Suggested fields:

- `job_id`
- `source_uri`
- `mime_type`
- `mode`
- `page_range`
- `language_hint`
- `requested_outputs`
- `created_at`

### Document Asset

원본 파일과 page image registry.

Suggested fields:

- `document_id`
- `source_hash`
- `source_path`
- `page_ids`
- `page_count`
- `ingest_status`

### Page Asset

페이지 단위 raster 처리 단위.

Suggested fields:

- `page_id`
- `document_id`
- `page_index`
- `original_image_path`
- `normalized_image_path`
- `document_type`

### Detected Table

페이지 안에서 검출된 표 영역.

Suggested fields:

- `table_id`
- `document_id`
- `page_id`
- `table_index`
- `table_bbox`
- `crop_image_path`
- `detection_confidence`

### Structural Cell

구조 추출 이후의 최소 셀 단위.

Suggested fields:

- `cell_id`
- `table_id`
- `row_start`
- `row_end`
- `col_start`
- `col_end`
- `bbox`
- `is_header`
- `row_span`
- `col_span`
- `structure_confidence`

### Logical Table Model

OCR 정렬과 header or body 판별까지 끝난 canonical structure.

Suggested fields:

- `table_id`
- `caption`
- `header_rows`
- `body_rows`
- `summary_rows`
- `stub_columns`
- `cells`
- `average_confidence`
- `quality_status`

## Common End-To-End Data Flow

### Step 0. Request Intake

Input:

- file path or URI
- mime type
- optional `page_range`, `language_hint`, `output_format`
- mode:
  - `table`
  - `row_column`
  - `worksheet`
  - `rag`

Process:

- validate request
- issue stable `job_id`
- persist request metadata

Output:

- `job_id`
- `request_manifest.json`

### Step 1. Input Registration and Identification

Input:

- raw file

Process:

- generate file hash
- detect duplicate processing candidates
- persist source metadata
- split into page images when needed

Output:

- `document_id`
- `page_id[]`
- image asset registry

### Step 2. Image Normalization

Process:

- resolution adjustment
- grayscale or binarization
- noise removal
- skew correction
- rotation correction
- contrast normalization
- optional table-line enhancement

Goal:

- stabilize OCR quality
- stabilize line and cell-boundary detection

Output:

- `normalized_page_image`
- `preprocessing_log.json`

### Step 3. Document Type and Table Candidate Classification

Process:

- decide whether the input is:
  - single-table image
  - mixed-layout page
  - multi-table page
- branch into direct table parsing or region detection

Output:

- `document_type`
- `table_candidate_regions`

### Step 4. Table Region Detection

Process:

- detect table bounding boxes
- count table instances
- crop each table region

Output:

- `table_id[]`
- `table_bbox`
- `table_crop_image`

### Step 5. Parsing Strategy Selection

Strategy branches:

- Grid table:
  - line-based row and column segmentation
- Borderless table:
  - text alignment, whitespace, and clustering based inference
- Merge-heavy table:
  - cell spanning inference with stronger conflict checks

Output:

- `selected_parsing_strategy`
- `structure_model_config`

### Step 6. Cell Structure Extraction

Process:

- estimate row count
- estimate column count
- generate cell bounding boxes
- infer merged cells and spans
- mark header row candidates

Output:

- `structural_grid`
- cells with coordinates
- row and column indices
- span metadata

Example:

```json
{
  "table_id": "t1",
  "rows": 12,
  "cols": 5,
  "cells": [
    {
      "cell_id": "t1_r0_c0",
      "row_start": 0,
      "row_end": 0,
      "col_start": 0,
      "col_end": 1,
      "bbox": [100, 220, 320, 280],
      "is_header": true
    }
  ]
}
```

### Step 7. OCR Execution

Process:

- run OCR on the full page or cell crops
- apply language hint
- capture token confidence
- normalize numeric, symbol, and unit recognition

Output:

- `text_tokens`
- `token_bbox`
- `ocr_confidence`

### Step 8. Cell-Text Alignment

Process:

- map OCR tokens into cell boxes
- merge multi-line text
- normalize internal line breaks
- restore cell-level reading order

Output:

- `cell_text`
- `token_to_cell_mapping`
- `unresolved_tokens`

Example:

```json
{
  "cell_id": "t1_r2_c3",
  "text": "2025 Q4",
  "confidence": 0.94
}
```

### Step 9. Logical Table Reconstruction

Process:

- identify header rows
- separate body rows
- classify summary or footnote rows
- identify stub columns
- decide whether title or caption is internal or external to the table

Output:

- `logical_table_model`
- `header_rows`
- `body_rows`
- `summary_rows`
- `caption_link`

### Step 10. Quality Validation and Retry Gate

Process:

- detect too many empty cells
- check column alignment anomalies
- verify OCR confidence threshold
- detect span conflicts
- validate typed values when possible
- trigger fallback or retry when needed

Retry examples:

- average confidence below threshold
- unstable row or column count
- excessive cell duplication
- header or body separation failure

Output:

- `quality_report`
- `retry_flag`
- `corrected_table_model`

### Step 11. Output Branching

모든 downstream output은 Step 10 이후의 corrected logical table model을 기준으로 생성한다.

## Mode A. Image To Table

### Goal

표 단위 구조를 보존한 기본 산출물을 만든다. 이 모드는 RAG와 worksheet의 공통 upstream이다.

### Execution Order

1. request intake
2. input registration
3. image normalization
4. table region detection
5. cell structure extraction
6. OCR execution
7. cell-text alignment
8. logical table reconstruction
9. table export generation
10. table summary and retrieval metadata generation
11. persistence and indexing

### Outputs

- `table.json`
- `table.html`
- `table.md`
- `table_summary.txt`
- `retrieval_metadata.json`

### Recommended Schema

```json
{
  "table_id": "t1",
  "source_document_id": "doc123",
  "page": 4,
  "caption": "매출 현황",
  "headers": [
    ["구분", "2024", "2025"]
  ],
  "rows": [
    ["A사업부", "120", "148"],
    ["B사업부", "98", "131"]
  ],
  "bbox": [100, 220, 920, 1380],
  "confidence": 0.91
}
```

### Table-Level RAG Enrichment

- link the preceding or following paragraph when available
- attach caption and section title
- generate a short natural-language summary
- optionally build numeric key-value flatten records

## Mode B. Image To Row / Column

### Goal

행, 열, 셀 수준의 정규화 구조를 만들어 질의 가능성과 grounding 품질을 높인다.

### Execution Order

1. finish the table pipeline
2. assign stable row indices
3. assign stable column indices
4. finalize merged-cell spans
5. map headers to columns
6. assign semantic roles:
   - `header`
   - `row_label`
   - `data_cell`
   - `summary_cell`
7. build row objects
8. build column objects
9. build normalized cell matrix
10. persist query-ready index

### Outputs

- `rows.json`
- `columns.json`
- `cells.json`
- `normalized_matrix.json`

### Example Schema

```json
{
  "table_id": "t1",
  "columns": [
    {"col_index": 0, "name": "구분"},
    {"col_index": 1, "name": "2024"},
    {"col_index": 2, "name": "2025"}
  ],
  "rows": [
    {
      "row_index": 1,
      "label": "A사업부",
      "values": {
        "2024": "120",
        "2025": "148"
      }
    }
  ]
}
```

### Post-Normalization Rules

- cast numeric values when confidence is sufficient
- normalize date values
- extract units when separately present
- normalize thousand separators
- unify blank, hyphen, and null-like values

## Mode C. Image To Worksheet

### Goal

사람이 다시 편집 가능한 worksheet file을 만든다.

### Execution Order

1. finish the row or column pipeline
2. generate worksheet layout
3. map row and column positions
4. apply merged-cell ranges
5. assign header style candidates
6. assign value types:
   - `string`
   - `number`
   - `date`
7. call `CSV` or `XLSX` writer
8. save export files
9. validate:
   - column count consistency
   - no merge range conflict
   - non-empty worksheet
10. persist export metadata

### Outputs

- `output.csv`
- `output.xlsx`
- `worksheet_manifest.json`

### Worksheet Manifest Example

```json
{
  "worksheet_id": "ws_001",
  "source_table_id": "t1",
  "sheet_name": "page_4_table_1",
  "rows": 12,
  "cols": 5,
  "merged_ranges": ["A1:B1"],
  "file_path": "/exports/doc123_page4_table1.xlsx"
}
```

### Optional XLSX Features

- bold header style
- approximate column width
- freeze pane
- minimal number formatting

## Mode D. Image To RAG

### Goal

동일한 logical table model을 retrieval-friendly chunk set으로 변환한다.

### Recommended Chunk Layers

- table summary chunk
- row-level chunk as primary retrieval unit
- optional cell-grounding metadata
- optional numeric question optimization records

### Example Row Chunk

```json
{
  "content": "A사업부의 2025 매출은 148이다.",
  "metadata": {
    "table_id": "t1",
    "row_index": 1,
    "column_name": "2025",
    "page": 4,
    "source_document_id": "doc123"
  }
}
```

### Query-Time Assumption

1. retrieve table or row chunks
2. resolve grounding metadata
3. optionally call exact cell lookup or table read tool
4. answer with table-grounded citations

## Canonical Structure Principle

모든 downstream branch는 다음 canonical model을 공유한다.

```json
{
  "document_id": "doc123",
  "page": 4,
  "table_id": "t1",
  "rows": [
    {
      "row_index": 0,
      "cells": [
        {
          "cell_id": "t1_r0_c0",
          "col_index": 0,
          "text": "매출",
          "row_span": 1,
          "col_span": 1,
          "bbox": [100, 220, 180, 260],
          "confidence": 0.97
        }
      ]
    }
  ]
}
```

이 canonical record는 table export, row or column export, worksheet export, RAG indexing, MCP read surface의 공통 source of truth다.

## MCP Surface Draft

### Tools

- `register_input(source_uri, mime_type, options)`
- `normalize_image(document_id, page_id, profile)`
- `detect_tables(document_id, page_id)`
- `extract_table_structure(table_id, strategy)`
- `ocr_cells(table_id, language_hint)`
- `build_logical_table(table_id)`
- `export_table(table_id, format)`
- `export_row_column(table_id)`
- `export_worksheet(table_id, format)`
- `index_for_rag(table_id, granularity)`

### Resources

- `doc://parsed/{document_id}`
- `table://{table_id}.json`
- `row://{table_id}.rows.json`
- `cell://{table_id}.cells.json`
- `rag://chunks/{document_id}`
- `file://exports/{document_id}/{table_id}.xlsx`

## Suggested Storage Layout

```text
/project
  /inputs
  /normalized
  /detections
  /structures
  /ocr
  /logical_tables
  /exports
    /json
    /html
    /markdown
    /csv
    /xlsx
  /rag
    /chunks
    /metadata
  /logs
```

## Quality Criteria

### Table Level

- table bounding-box accuracy
- missed-table rate
- caption linkage success rate

### Row/Column Level

- row-count accuracy
- column-count accuracy
- merged-cell reconstruction accuracy
- header-mapping accuracy

### Worksheet Level

- cell-value preservation rate
- merge-range preservation rate
- CSV and XLSX reopen success rate
- human-readable structural parity

### Retrieval Level

- row retrieval accuracy
- cell grounding accuracy
- numeric question support quality

## Failure and Retry Policy

### Case 1. Table Detection Failure

- retry by treating the whole page as a single table
- relax detection threshold

### Case 2. Structure Extraction Failure

- fall back from line-based segmentation to text-alignment inference

### Case 3. OCR Instability

- rerun OCR on cell crops
- apply numeric-specialized correction
- branch on language configuration

### Case 4. Merged-Cell Conflict

- degrade to a simpler grid model without merge spans
- persist both merged and unmerged worksheet variants when needed

### Case 5. Worksheet Export Failure

- keep JSON and HTML outputs as authoritative fallbacks
- mark worksheet export as retryable, not terminal

## Recommended Implementation Order

### Phase 1. Image To Table

- table detection
- structure extraction
- OCR
- table `JSON`, `HTML`, `Markdown`
- retrieval metadata generation

This phase already yields usable RAG artifacts.

### Phase 2. Image To Row / Column

- header and body separation
- row and column semantic mapping
- typed cell normalization
- query-ready `rows.json`, `columns.json`, `cells.json`

### Phase 3. Image To Worksheet

- `CSV` export
- `XLSX` export
- merged-cell application
- minimal formatting support

### Phase 4. MCP Productization

- stabilize tool contracts
- expose resources
- add retry and audit hooks
- align return schemas with external agent consumption

## Minimum Operational Outputs

Recommended minimum set:

1. `table.json`
2. `cells.json`
3. `table.html`
4. `retrieval_metadata.json`

If worksheet reconstruction is required, add:

5. `output.xlsx`

## Success Criteria

- stable canonical table structure for at least one dominant input class
- retrieval-ready metadata generated from the same structure without duplicate parsing logic
- worksheet export derived from normalized structure, not ad hoc OCR text lists
- fallback and retry reasons recorded as machine-readable artifacts

## One-Line Summary

입력 이미지를 정규화하고 표 구조를 복원한 뒤, 하나의 canonical table model에서 `Table`, `Row/Column`, `RAG`, `Worksheet`, `MCP` 산출물을 순차적으로 파생시키는 계획이다.
