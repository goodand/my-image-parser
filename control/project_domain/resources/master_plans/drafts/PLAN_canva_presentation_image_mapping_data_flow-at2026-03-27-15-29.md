# Canva Presentation Image Mapping Data Flow Plan

## Status

Draft

## Purpose

This plan defines the end-to-end pipeline that starts from a Canva presentation, extracts image assets, refines captions and document mappings through human review, and generates a new presentation from finalized image content.

The document fixes two boundaries:

1. where automation stops and human review begins
2. what each step consumes, produces, and must rerun after change

## Scope

Pipeline scope:

Canva presentation selection
→ presentation export
→ image extraction
→ draft caption generation
→ human caption review
→ retrieval input generation
→ candidate retrieval
→ reranked top-5 generation
→ human mapping review or outlier labeling
→ manual outlier description writing
→ final content assembly
→ new presentation rendering

Already implemented but still part of the flow:

- presentation file image extraction
- Gemini-based draft caption generation
- presentation generation from images and captions

## Operational Assumptions

### Source Assumption

- Canva is the upstream source only.
- The system reads from Canva and exports from Canva.
- Reverse sync back into Canva is out of scope.

### Human Review Assumption

Humans perform three review checkpoints:

- caption review and correction
- top-5 document mapping review
- outlier description writing

### Reprocessing Assumption

If the approved caption changes, retrieval and rerank outputs may change. Therefore downstream retrieval stages must be rerunnable.

## Core Data Objects

### Job

One pipeline execution for one source Canva design.

Suggested fields:

- `job_id`
- `source_design_id`
- `source_design_title`
- `source_export_file`
- `status`
- `created_at`
- `pipeline_version`

### Image Item

One extracted image from the source presentation.

Suggested fields:

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

Suggested fields:

- `image_id`
- `draft_caption`
- `approved_caption`
- `caption_review_status`
- `caption_edited_by_human`
- `caption_last_updated_at`

### Mapping Record

Stores retrieval and final mapping state.

Suggested fields:

- `image_id`
- `retrieval_query`
- `candidate_doc_ids`
- `reranked_top5`
- `selected_doc_id`
- `mapping_status`
- `outlier_label`
- `manual_description`

## Step-by-Step Data Flow

### Step 0. Job Initialization

Input:

- user-selected Canva presentation or search condition
- target document store
- pipeline configuration

Process:

- create `job_id`
- create job folder structure
- initialize job manifest

Output:

- `job_manifest.json`
- working directories
- job status `initialized`

### Step 1. Canva Presentation Resolution and Download

Input:

- Canva design ID or search condition

Process:

- identify target design through Canva MCP or design metadata
- export the presentation file
- store source metadata

Output:

- `source_presentation.pptx`
- `source_metadata.json`
- job status `source_downloaded`

Constraint:

- this is the only Canva-dependent step
- every later phase runs from local artifacts

### Step 2. Image Extraction

Input:

- `source_presentation.pptx`

Process:

- extract slide images
- assign stable image IDs
- record page number, element order, and hash
- optionally filter decorative or duplicate assets

Output:

- `images/`
- `image_manifest.jsonl`
- job status `images_extracted`

### Step 3. Draft Caption Generation

Input:

- extracted images

Process:

- generate one draft caption per image
- store generation metadata

Output:

- `caption_draft.jsonl`
- per-image state `caption_drafted`

Note:

- this phase reuses the existing captioning implementation

### Step 4. Human Review A: Caption Approval

Input:

- image
- draft caption

Process:

- approve draft caption as-is
- or edit draft caption and approve it
- optionally store review comments

Output:

- `caption_review.jsonl`
- final `approved_caption`
- per-image state `caption_approved` or `caption_edited`

Operating rule:

- only `approved_caption` is allowed into retrieval and final output
- draft captions are never authoritative

### Step 5. Retrieval Input Generation

Input:

- image
- approved caption

Process:

- generate image embedding if required
- generate retrieval query if required
- record model version and generation timestamp

Output:

- `image_embedding.parquet` or equivalent
- `retrieval_input.jsonl`
- state `retrieval_ready`

Preferred operating mode:

- image embedding + approved caption combined

### Step 6. Candidate Retrieval

Input:

- `retrieval_input.jsonl`
- document index

Process:

- retrieve a sufficiently broad candidate set
- store scores and retrieval evidence

Output:

- `retrieval_candidates.jsonl`
- state `candidates_retrieved`

Guideline:

- retrieve a wider pool such as top-20 to top-50 before reranking

### Step 7. Reranked Top-5 Generation

Input:

- candidate set
- image
- approved caption

Process:

- rerank candidate documents
- generate a final top-5 review list

Output:

- `reranked_top5.jsonl`
- state `reranked`

### Step 8. Human Review B: Mapping Decision

Input:

- image
- approved caption
- reranked top-5 candidates

Process:

- select one final document mapping from top-5
- or mark the image as outlier

Output:

- `mapping_review.jsonl`
- state `mapping_selected` or `outlier_labeled`

Recommendation:

- record both final selection and perceived quality of the candidate ranking itself
- this helps future reranker tuning

### Step 9. Human Review C: Outlier Description

Input:

- outlier-labeled image
- approved caption
- reviewer notes

Process:

- write manual descriptive text for images with no valid mapping

Output:

- `manual_description.jsonl`
- state `manual_description_done`

### Step 10. Final Content Assembly

Input:

- image
- approved caption
- selected document or manual description

Process:

- assemble the final per-image content block
- use selected document context when mapping exists
- use manual description when the image is outlier

Output:

- `final_content_manifest.jsonl`
- state `content_assembled`

### Step 11. Presentation Rendering

Input:

- final content manifest
- image files
- approved captions
- final descriptions

Process:

- generate the output presentation structure
- place image, caption, and description
- render and save the file

Output:

- `output_presentation.pptx`
- job status `rendered`

Note:

- this phase extends the already implemented presentation generation flow

### Step 12. Final Validation and Packaging

Input:

- rendered presentation
- all manifests

Process:

- verify there are no missing images
- verify no caption approval is missing
- verify no outlier is missing manual description
- package the final deliverables

Output:

- `output_presentation.pptx`
- `final_job_report.json`
- job status `completed`

## Human Review Summary

### Review A. Caption Review

- inspect draft caption
- edit when needed
- confirm final approved caption

### Review B. Mapping Review

- inspect reranked top-5
- choose final mapping or mark outlier

### Review C. Outlier Description

- write manual description for unmatched but retained images

## Image State Flow

```text
extracted
-> caption_drafted
-> caption_approved or caption_edited
-> retrieval_ready
-> candidates_retrieved
-> reranked
-> mapping_selected or outlier_labeled
-> manual_description_done
-> finalized
```

Important constraint:

- `mapping_selected` and `manual_description_done` are mutually exclusive terminal routes for the mapping branch
- mapped items end at `mapping_selected`
- outlier items must pass through `outlier_labeled` and then `manual_description_done`

## Rerun Rules

### When Source Presentation Changes

Rerun from Step 1.

### When Extraction Logic Changes

Rerun from Step 2.

### When Approved Caption Changes

Rerun from Step 5.

This recalculates retrieval input, candidates, and reranked outputs.

### When Only Mapping Changes

Rerun from Step 10.

### When Only Manual Outlier Description Changes

Rerun from Step 10.

## Recommended Artifact Layout

```text
/job/{job_id}/
  source/
    source_presentation.pptx
    source_metadata.json
  images/
    *.png
  manifests/
    image_manifest.jsonl
    caption_draft.jsonl
    caption_review.jsonl
    retrieval_input.jsonl
    retrieval_candidates.jsonl
    reranked_top5.jsonl
    mapping_review.jsonl
    manual_description.jsonl
    final_content_manifest.jsonl
    final_job_report.json
  output/
    output_presentation.pptx
```

## Final Operating Principles

1. Only approved captions are allowed into retrieval and output generation.
2. Unmatched images are treated as outliers and resolved with manual description.
3. Final presentation generation uses only human-confirmed values.

## One-Line Summary

Automation drafts and ranks; humans decide meaning and final presentation content.
