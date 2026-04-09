# Presentation Image Mapping Extension Plan

## Status

Draft

## Purpose

This plan extends an already working presentation pipeline with retrieval and human-review steps.

Already completed:

- presentation file download
- image extraction from presentation file
- Gemini-based image caption generation
- presentation regeneration from image plus caption

New scope added by this draft:

- image embedding generation
- reranker-based related-document candidate generation
- human review of captions and mapping results
- outlier handling with manual description

## Baseline Pipeline

```text
presentation download
-> image extraction
-> caption generation
-> presentation generation
```

## Extended Pipeline

```text
presentation download
-> image extraction
-> draft caption generation
-> caption review and correction
-> image embedding generation
-> candidate retrieval
-> reranked top-5 mapping candidates
-> human mapping review
-> outlier labeling when needed
-> manual outlier description
-> final presentation generation
```

## Human Review Tasks

### Review A. Caption Quality

1. verify whether the generated caption is appropriate
2. directly edit the caption when it is not appropriate

### Review B. Document Mapping Quality

1. inspect the reranker top-5 candidate ranking
2. decide the final mapping or mark the image as outlier

### Review C. Outlier Handling

1. write a manual description for outlier-labeled images

## Recommended Step Order

### Step 1. Source Presentation Handling

- download the presentation file
- extract images
- assign stable image IDs

### Step 2. Caption Baseline

- generate draft captions with the existing captioning flow
- store both raw caption and image reference

### Step 3. Caption Review Gate

- human reviews caption quality
- human edits when needed
- approved caption becomes the only caption allowed downstream

### Step 4. Retrieval Preparation

- generate image embeddings
- optionally combine embedding and approved caption into retrieval input

### Step 5. Candidate Retrieval

- search the related document store
- return a sufficiently broad candidate set before reranking

### Step 6. Reranker Top-5

- rerank the retrieved candidates
- produce a human review list limited to top-5

### Step 7. Mapping Review Gate

- human selects one final mapping from the top-5
- or marks the image as outlier when no candidate is acceptable

### Step 8. Outlier Description

- for outlier images, human writes the final descriptive text

### Step 9. Final Content Assembly

- combine image
- approved caption
- selected mapped document or manual outlier description

### Step 10. Presentation Regeneration

- generate the new presentation from finalized values only

## Operating Rules

1. Draft captions are never authoritative.
2. Approved captions are the only captions allowed into retrieval and output generation.
3. Mapped-document selection and outlier labeling are human decisions.
4. Outlier images stay in the flow, but they use manual descriptions instead of mapped documents.
5. Final presentation generation must use only approved and finalized values.

## Minimal Data Objects

### Image Item

- `image_id`
- `image_path`
- `source_page_no`
- `approved_caption`

### Retrieval Record

- `image_id`
- `embedding_ref`
- `candidate_doc_ids`
- `reranked_top5`
- `selected_doc_id`
- `outlier_label`

### Manual Review Record

- `image_id`
- `caption_review_status`
- `mapping_review_status`
- `manual_description`

## Immediate MVP Extension

Implement the extension in this order:

```text
1. keep the existing extraction and caption pipeline
2. add caption approval step
3. add image embedding step
4. add retrieval and reranker top-5 output
5. add human mapping review
6. add manual outlier description path
7. regenerate presentation from approved values
```

## One-Line Summary

The existing presentation pipeline stays intact, and the new work starts after caption generation: embed, retrieve, rerank, review, resolve outliers, then regenerate the presentation from finalized content.
