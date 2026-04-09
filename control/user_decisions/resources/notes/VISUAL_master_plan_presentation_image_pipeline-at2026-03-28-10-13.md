# Visualization Companion: Master Plan Presentation Image Pipeline

## Status

Draft

## Purpose

This companion document translates the canonical master plan into Obsidian-friendly Mermaid diagrams.
It is a visualization aid, not the source of truth.
The diagrams below follow the current parser-first active baseline rather than the older caption-first reading.

Canonical source:

- [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)

## VSCode Viewing

- Open this file in VSCode.
- Use `Markdown: Open Preview` or `Ctrl+Shift+V`.
- `Markdown Preview Mermaid Support` should render the Mermaid blocks directly in preview.
- `Live Server` is optional and not required for this markdown-based companion.

## Diagram 1. Active Parser-First Baseline

```mermaid
flowchart TD
    A[Presentation or direct image intake] --> B[Extract image assets]
    B --> C[Register per-image records]
    C --> D[Component isolation when needed]
    D --> E[Per-component table extraction attempt]
    E --> F[OCR extraction on full image and components]
    F --> G[Normalize parser or OCR sidecars<br/>into canonical parsed record]
    G --> H[Run four-mode caption comparison]
    H --> I[Human review of parser and caption evidence]
    I --> J[Accepted canonical parsed record]

    J --> K[Optional worksheet export]
    J --> M[Optional MCP consumer surface]
    J --> L[Optional late-stage RAG preparation]
    J --> N[Optional metadata or rename]
    J --> O[Optional presentation regeneration]
```

## Diagram 2. Component Isolation And Parser Evidence Flow

```mermaid
flowchart LR
    A[Full extracted image] --> B{Compound or dense image?}
    B -->|No| C[Use full image as one component]
    B -->|Yes| D[Split into isolated components]
    C --> E[Table candidate triage]
    D --> E
    E -->|table-like| F[Table extraction attempt]
    E -->|non-table or ambiguous| G[OCR-first evidence path]
    F --> H[Structural grid and span inference]
    H --> I[Cell-text alignment]
    G --> J[OCR evidence extraction]
    I --> K[Parser sidecar]
    J --> L[OCR sidecar]
    K --> M[Canonical parsed record]
    L --> M
```

## Diagram 3. Four-Mode Caption Comparison

```mermaid
flowchart TD
    A[Image and evidence ready] --> B[Arm A<br/>Full image baseline caption]
    A --> C[Arm B<br/>Isolated component caption]
    A --> D[Arm C<br/>OCR-evidence-enriched caption]
    A --> E[Arm D<br/>Parser or table-structure-enriched caption]
    B --> F[Comparison record]
    C --> F
    D --> F
    E --> F
    F --> G[Human review or judge layer]
    G --> H[Selected caption plus evidence package]
```

## Diagram 4. Late-Stage Consumer Ordering

```mermaid
flowchart TD
    A[Accepted canonical parsed record] --> B[Worksheet export]
    A --> C[MCP read surface]
    A --> D[Caption and review package]
    A --> E[Optional late-stage RAG preparation]

    D --> F[Optional retrieval or mapping path]
    B --> G[Final content assembly]
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H[Packaging or presentation regeneration]

    classDef late fill:#f7f3d0,stroke:#666,color:#111;
    class E late;
```

## Diagram 5. Table-Branch State Flow With Retry

```mermaid
stateDiagram-v2
    [*] --> table_candidate
    table_candidate --> layout_analyzed
    layout_analyzed --> table_extracted
    table_extracted --> structure_recognized
    structure_recognized --> table_normalized
    table_normalized --> row_chunked
    row_chunked --> worksheet_built
    row_chunked --> mcp_exposed

    layout_analyzed --> table_retry_pending: recoverable failure
    table_extracted --> table_retry_pending: recoverable failure
    structure_recognized --> table_retry_pending: recoverable failure
    table_normalized --> table_retry_pending: recoverable failure

    table_retry_pending --> layout_analyzed: re-enter early phase
    table_retry_pending --> table_extracted: re-enter detection output
    table_retry_pending --> structure_recognized: re-enter structure phase
    table_retry_pending --> table_normalized: re-enter validation phase

    table_retry_pending --> table_manual_review_required: retry budget exhausted
    table_candidate --> table_manual_review_required: unrecoverable failure
    table_manual_review_required --> [*]
    worksheet_built --> [*]
    mcp_exposed --> [*]
```

## Reading Notes

- Diagram 1 is the active parser-first baseline for the workspace.
- Diagram 2 shows how component isolation and parser or OCR evidence feed canonical records.
- Diagram 3 places the four-mode caption experiment after parser and OCR evidence collection.
- Diagram 4 shows that worksheet, MCP, and caption are immediate late-stage consumers, while RAG is deferred even further.
- Diagram 5 remains the table-branch retry state machine.
