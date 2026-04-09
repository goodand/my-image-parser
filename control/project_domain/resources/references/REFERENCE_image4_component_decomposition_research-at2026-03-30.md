# Reference: Image4 Component Decomposition Research

## Purpose

Cache a bounded external research set for the `image4`-style composite dashboard problem.

The goal is not just better regrouping. The harder open problem is:
- first decompose a composite image into semantically meaningful components
- then regroup those components into candidate caption surfaces

Follow-on implementation strategy:
- `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/REFERENCE_component_decomposition_strategy-at2026-03-30.md`

Canonical KB:
- `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/knowledge_bases/KB_component_decomposition_strategy.md`

## Current Conclusion

Yes, `regrouping` is part of the answer, but it is not the whole answer.

For `image4`, the missing capability is still **component decomposition**:
- separate title, chart panels, embedded table, and supporting text
- decide whether the experiment wants:
  - full dashboard
  - table-centric crop
  - chart-set crop
  - title + selected analytical surface

So the research stack should be read in two layers:

1. **decomposition / layout proposal**
2. **grouping / regrouping / scoring**

## Saved Papers

### 1. Docling Technical Report

- local PDF:
  - [docling_technical_report_2408.09869.pdf](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/papers/image4_component_decomposition/docling_technical_report_2408.09869.pdf)
- source:
  - https://github.com/docling-project/docling
  - https://arxiv.org/abs/2408.09869
- why it matters:
  - strong for document ingestion, unified document representation, reading order, table structure
  - useful for future paper ingestion and canonicalization
  - not a direct `image4` fix because chart understanding is still not the primary strength

### 2. LayoutParser: A Unified Toolkit for Deep Learning Based Document Image Analysis

- local PDF:
  - [layoutparser_2103.15348.pdf](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/papers/image4_component_decomposition/layoutparser_2103.15348.pdf)
- source:
  - https://github.com/Layout-Parser/layout-parser
  - https://arxiv.org/abs/2103.15348
- why it matters:
  - strongest fit for the `regrouping` half of the problem
  - gives a block/layout abstraction that can support:
    - `title + table`
    - `chart set`
    - `full dashboard`
    candidate grouping
- limitation:
  - not a decomposition engine by itself

### 3. PubTables-1M / Table Transformer Line

- local PDF:
  - [pubtables1m_table_transformer_2110.00061.pdf](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/papers/image4_component_decomposition/pubtables1m_table_transformer_2110.00061.pdf)
- source:
  - https://github.com/microsoft/table-transformer
  - https://arxiv.org/abs/2110.00061
- why it matters:
  - useful after table panel detection
  - highlights canonical table structure recovery and oversegmentation/undersegmentation issues
- limitation:
  - solves table extraction better than composite dashboard decomposition

### 4. DocLayout-YOLO

- local PDF:
  - [doclayout_yolo_2410.12628.pdf](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/papers/image4_component_decomposition/doclayout_yolo_2410.12628.pdf)
- source:
  - https://arxiv.org/abs/2410.12628
- why it matters:
  - strong candidate for the **decomposition / proposal** half
  - relevant idea: combine global and local perception to detect document elements robustly
  - likely useful for extracting title, table-like region, and chart/image regions before regrouping

### 5. Semantic Segmentation for Compound Figures

- local PDF:
  - [semantic_segmentation_for_compound_figures_1912.07142.pdf](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/references/papers/image4_component_decomposition/semantic_segmentation_for_compound_figures_1912.07142.pdf)
- source:
  - https://arxiv.org/abs/1912.07142
- why it matters:
  - this is the most directly relevant paper for the still-open problem
  - key idea: compound figures should be decomposed into **master images** rather than treated as one flat image
  - the paper uses semantic segmentation + label-aware structure cues
- why it matters for us:
  - `image4` behaves more like a compound analytical figure than a simple table crop problem
  - this supports building a `panel decomposition` stage before any reviewed-crop promotion

## Practical Reading Order

If the goal is to improve `image4` handling in the current codebase, read in this order:

1. `semantic_segmentation_for_compound_figures_1912.07142.pdf`
2. `doclayout_yolo_2410.12628.pdf`
3. `layoutparser_2103.15348.pdf`
4. `pubtables1m_table_transformer_2110.00061.pdf`
5. `docling_technical_report_2408.09869.pdf`

## Actionable Ideas For Our Codebase

### A. Decomposition first

The paper set suggests that `image4` should not be treated as:
- one crop
- or one table-like region

Instead, create a decomposition stage that proposes:
- title block
- chart panel blocks
- embedded table block
- supporting text blocks

### B. Then regroup

After decomposition, candidate surfaces should be regrouped as:
- `full_dashboard`
- `title + table`
- `table_only`
- `chart_set`
- `title + chart_set`

### C. Then score

The existing rule-based comparison logic can stay downstream:
- OCR evidence
- parser structure support
- noise suppression
- promotion-state penalty

### D. Then use tie-break only if needed

If top candidates are still close:
- use subagent or direct vision tie-break
- do not let tie-break replace deterministic decomposition

## Recommendation

The key insight from the papers is **not just regrouping**.

The stronger takeaway is:
- we still need a proper **component decomposition** stage for compound analytical figures
- regrouping should happen only after decomposition

So the next implementation slice should target:

`decomposition -> regrouping -> scoring`

not just `better reviewed crop`.
