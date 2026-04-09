# CV MCP Caption Evaluation Metadata Flow Plan

## Status

Draft

## Purpose

This plan defines a sequential image-processing batch where each image is captioned, independently evaluated, approved or rejected through a decision gate, then optionally written back into metadata and renamed.

The plan is based on an A-path operating assumption:

- generation uses `cv-mcp.image_metadata`
- independent validation uses `moondream-mcp`
- persistence and rename use filesystem MCP
- metadata write-back uses ExifTool MCP

## System Roles

### MainAgent

Controls the entire batch.

Responsibilities:

- discover input images
- sort execution order
- launch one subagent per image in sequence
- apply decision rules
- trigger persistence, metadata write-back, and rename
- continue on per-image failure without aborting the entire batch

### CaptionSubAgent

Processes exactly one image.

Responsibilities:

- call `cv-mcp.image_metadata`
- receive `alt_text`, `caption`, and structured `metadata`
- normalize the result into the batch result format

### EvalSubAgent

Validates the generated caption independently.

Responsibilities:

- collect image-grounded evidence through `moondream-mcp`
- produce atomic evidence checks
- compute grounding metrics
- compute holistic judge metrics
- return a final decision candidate

### PersistenceAgent

Persists JSON artifacts and reports through filesystem MCP.

### MetadataWriteAgent

Writes approved metadata into files through ExifTool MCP.

## Batch Flow Overview

```text
Batch Start
  -> Input Discovery
  -> Preflight Validation
  -> For each image in sorted order:
       -> CaptionSubAgent
       -> EvalSubAgent
       -> Decision Gate
           -> accept  -> persist -> write metadata -> rename(optional)
           -> rewrite -> retry generation/eval
           -> audit   -> persist audit package
           -> error   -> persist error and continue
  -> Batch Summary
  -> Final Report
```

## Phase-by-Phase Data Flow

### Phase 0. Input Preparation

#### Step 0-1. Working Directory Validation

Use filesystem MCP to validate:

- input directory
- output directory
- audit directory
- log directory

#### Step 0-2. Image Discovery

Read the target image list from the input directory.

Recommended policy:

- keep supported extensions in a config file
- reject non-image files during preflight

#### Step 0-3. Execution Ordering

Default ordering:

- ascending filename order

Optional policies:

- created time
- modified time
- EXIF capture time

#### Step 0-4. Batch Manifest Creation

Create an initial batch manifest entry per image.

```json
{
  "sequence_no": 1,
  "image_path": "/input/img_0001.jpg",
  "status": "queued"
}
```

This manifest acts as a rerun checkpoint.

### Phase 1. Per-Image Generation

#### Step 1-1. Select One Pending Image

The MainAgent chooses the first not-yet-completed image in sorted order.

#### Step 1-2. Create CaptionSubAgent

The subagent receives exactly one image as its context boundary.

#### Step 1-3. Call `cv-mcp.image_metadata`

Example call:

```json
{
  "tool": "cv-mcp.image_metadata",
  "args": {
    "file_path": "/input/img_0001.jpg",
    "mode": "double"
  }
}
```

The expected result includes:

- `alt_text`
- `caption`
- `metadata`

#### Step 1-4. Normalize Generation Output

```json
{
  "sequence_no": 1,
  "image_path": "/input/img_0001.jpg",
  "status": "generated",
  "alt_text": "...",
  "caption": "...",
  "metadata": { ... }
}
```

#### Step 1-5. Persist Generated Output

Save to:

- `output/intermediate/0001.generated.json`

### Phase 2. Per-Image Evaluation

#### Step 2-1. Create EvalSubAgent

The evaluator receives:

- image path
- generated caption payload

#### Step 2-2. Collect Independent Evidence

Use `moondream-mcp` to collect at least three evidence types:

1. independent detailed caption
2. VQA answers
3. object detection or pointing results

Recommended prompts include:

- what are the key visible objects?
- how many people are visible?
- is there readable text?
- does the generated caption mention an object that is absent?

#### Step 2-3. Build Atomic Evaluation Units

Extract units such as:

- objects
- attributes
- relations
- counts
- visible text
- scene labels
- actions

#### Step 2-4. Grounding Evaluation

Compute:

- precision
- recall
- f1
- hallucination rate

#### Step 2-5. Holistic Judge Evaluation

Score:

- accuracy
- completeness
- conciseness
- relevance

#### Step 2-6. Produce Final Evaluation Payload

```json
{
  "sequence_no": 1,
  "image_path": "/input/img_0001.jpg",
  "status": "evaluated",
  "scores": {
    "precision": 0.86,
    "recall": 0.78,
    "f1": 0.82,
    "hallucination": 0.14,
    "judge_accuracy": 0.88,
    "judge_completeness": 0.80,
    "judge_conciseness": 0.84,
    "judge_relevance": 0.90,
    "final": 0.84
  },
  "decision": "accept"
}
```

#### Step 2-7. Persist Evaluation Output

Save to:

- `output/intermediate/0001.evaluated.json`

### Phase 3. Decision Gate

#### Accept Path

Example threshold:

- `precision >= 0.75`
- `judge_accuracy >= 0.80`
- `final >= 0.80`

Actions:

- persist canonical result
- proceed to metadata write-back
- optionally proceed to rename

#### Rewrite Path

Use when:

- correctness is salvageable
- hallucination is limited
- omission is the main issue

Actions:

- increment `rewrite_count`
- regenerate up to 1 or 2 times
- optionally use prompt correction or `caption_override`

#### Audit Path

Use when:

- judge score is high but grounding is weak
- counts, text, or key objects conflict
- OCR or counting reliability is too low

Actions:

- save audit package
- enqueue for manual review
- continue with next image

#### Error Path

Use when:

- MCP call fails
- file is corrupt
- output cannot be parsed

Actions:

- persist error record
- continue with next image
- do not abort the entire batch

### Phase 4. Canonical Result Persistence

#### Step 4-1. Build Final Accepted Record

```json
{
  "sequence_no": 1,
  "image_path": "/input/img_0001.jpg",
  "alt_text": "...",
  "caption": "...",
  "metadata": { ... },
  "scores": { ... },
  "decision": "accept",
  "version": "v1"
}
```

#### Step 4-2. Save Final Result JSON

Save to:

- `output/final/0001.result.json`

### Phase 5. Metadata Write-Back

#### Step 5-1. Map Fields To Tags

Example mapping:

- `caption` -> `XMP:Description`
- `alt_text` -> `IPTC:Caption-Abstract` or XMP equivalent
- `metadata.tags` -> `XMP:Subject`
- `metadata.scene` -> `XMP:Category` or custom namespace

#### Step 5-2. Call ExifTool MCP

Apply metadata to the image file.

#### Step 5-3. Verify Metadata Write

Read metadata back and verify it.

On mismatch:

- set `metadata_write_failed`
- keep the original file intact

### Phase 6. Filename Rename

#### Step 6-1. Build Filename Candidate

Example rule:

```text
{sequence_no}_{caption_slug}.jpg
```

Example output:

```text
0001_woman_walking_snowy_city_street.jpg
```

#### Step 6-2. Apply Safety Rules

- max length limit
- reserved character removal
- duplicate suffixing
- no personally identifying file names

#### Step 6-3. Rename Through Filesystem MCP

Use `move_file` semantics.

#### Step 6-4. Rewrite Final Path In Result JSON

Update the canonical result record with the new path.

### Phase 7. Batch Finalization

#### Step 7-1. Aggregate Batch Metrics

Collect:

- total
- accept
- rewrite
- audit
- error
- metadata_write_failed
- rename_failed

#### Step 7-2. Write Batch Summary

Save:

- `output/reports/batch_summary.json`
- `output/reports/batch_summary.md`

#### Step 7-3. Write Audit Queue Artifact

Store only audit-target images in a dedicated list.

## Detailed State Transition

```text
queued
  -> generating
  -> generated
  -> evaluating
  -> evaluated
  -> accept_pending | rewrite_pending | audit_pending | error
  -> persisted
  -> metadata_written
  -> renamed
  -> completed
```

Allowed terminal routes:

```text
accept -> persisted -> completed
accept -> persisted -> metadata_written -> renamed -> completed
```

## Failure Policy

### Generation Failure

- retry once for the same image
- on repeated failure, mark `error`

### Evaluation Failure

- retry evaluator once
- on repeated failure, mark `audit`

### Metadata Write Failure

- keep result JSON
- keep original file
- mark `metadata_write_failed`

### Rename Failure

- keep metadata and result JSON
- keep original file name
- mark `rename_failed`

## Artifact Layout

```text
/output
  /intermediate
    0001.generated.json
    0001.evaluated.json
  /final
    0001.result.json
  /audit
    0007.audit.json
  /reports
    batch_summary.json
    batch_summary.md
  /logs
    run_2026-03-26T....jsonl
```

## Recommended MCP Set

- `cv-mcp` for `alt_text`, `caption`, and structured metadata generation
- `moondream-mcp` for independent evaluation
- filesystem MCP for discovery, writes, and rename
- ExifTool MCP for metadata persistence

## Minimum Viable Rollout

Implement in this order:

```text
1. input discovery
2. image_metadata generation
3. independent evaluation
4. decision save
5. metadata write-back
```

Rename can wait for the second rollout.

## Recommended Later Additions

- OCR-specific evaluator
- separate count checkers for people and vehicles
- stronger audit rules for judge disagreement
- human review UI
- bilingual caption storage
- sidecar JSON and XMP dual-save mode

## One-Line Summary

Generate with `cv-mcp`, verify independently, persist the accepted result, then write metadata and rename only after approval.

## References

- cv-mcp: https://github.com/samhains/cv-mcp
- moondream-mcp: https://github.com/ColeMurray/moondream-mcp
- filesystem MCP: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- ExifTool MCP: https://github.com/joshmsimpson/ExifTool_MCP
