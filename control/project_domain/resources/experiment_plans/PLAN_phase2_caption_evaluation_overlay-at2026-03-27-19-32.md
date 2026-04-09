# Phase 2 Caption Evaluation Overlay Plan

## Purpose

Design the next experiment after the completed phase-1 extracted-media baseline.

This phase adds an evaluation overlay on top of the existing OpenAI-generated caption set without committing metadata or renames.

Primary goals:

- classify the 60 completed phase-1 captions into `accept`, `rewrite`, `audit`, or `error`
- preserve the `.emf` unsupported boundary as an explicit non-candidate
- measure whether the current baseline is strong enough to produce a commit-ready subset
- keep all decisions in run artifacts before any mutation phase

## Why This Is Phase 2

The master plan names the next active path as an optional evaluation overlay after sample review.

This plan operationalizes that path using:

- the completed phase-1 baseline
- the sample quality review findings
- the caption completeness validator and live smoke evidence

Current planning note:

- if the next active experiment targets object-level captioning, this phase stays paused until `phase0` component isolation, OCR evidence extraction, and context-package preparation are completed or explicitly waived
- if the next active experiment targets table or worksheet structure, this phase stays paused until the bounded table-branch activation sequence is completed or explicitly waived:
  - `xhigh` triage-worker selection gate
  - `paddleocr-mcp` full boot smoke
  - `PP-StructureV3` smoke on `1` to `2` real PPT images
  - canonical `Table -> Row -> Cell` normalization

## Scope

In scope:

- evaluation only on the phase-1 completed extracted-media baseline
- independent evidence collection against the original image files
- atomic evaluation plus final decision gate
- per-record decision artifacts and batch summary
- identification of the commit-ready subset candidate

Out of scope:

- metadata write-back
- rename commit
- screenshot arm execution
- table branch execution
- cross-arm final comparison

## Canonical Inputs

- master plan:
  - [MASTER_PLAN_presentation_image_pipeline.md](../master_plans/MASTER_PLAN_presentation_image_pipeline.md)
- implementation profile draft:
  - [PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md](../master_plans/drafts/PLAN_cv_mcp_caption_eval_metadata_flow-at2026-03-27-15-29.md)
- phase-1 execution truth:
  - [REPORT_phase1_caption_experiment_execution-at2026-03-27-18-31.md](../reports/REPORT_phase1_caption_experiment_execution-at2026-03-27-18-31.md)
  - [phase1_caption_experiment_summary_at2026_03_27.json](../manifests/phase1_caption_experiment_summary_at2026_03_27.json)
- phase-1 quality evidence:
  - [REPORT_phase1_caption_quality_sample_review-at2026-03-27-19-07.md](../reports/REPORT_phase1_caption_quality_sample_review-at2026-03-27-19-07.md)
  - [REPORT_caption_completeness_validator_smoke-at2026-03-27-19-14.md](../reports/REPORT_caption_completeness_validator_smoke-at2026-03-27-19-14.md)
- phase-1 shard boundaries:
  - `control/project_domain/resources/manifests/phase1_caption_shards/`
- completed phase-1 ledgers:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w2.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w4.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w5.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6.json`

## Preflight Gate

Phase 2 must not start until all of the following are true:

1. phase-1 summary remains the current truth artifact
2. the single unsupported `.emf` case remains explicitly explained and excluded from candidate records
3. caption completeness validator remains active in the runner path
4. active machine-readable hard fails caused by legacy `phase1_caption_10w` filenames are cleaned up, reclassified, or archived out of the active surface

If item 4 is not satisfied, this plan stays in `designed but not executable` state.

## Candidate Set

The evaluation overlay consumes:

- exactly `60` phase-1 records with `status=completed`
- excludes the single `.emf` record with `status=unsupported_media_type`

The evaluation candidate manifest should be materialized as:

- `control/project_domain/resources/manifests/phase2_caption_eval_candidates.jsonl`

Each row should include at minimum:

- `image_id`
- `image_path`
- `caption`
- `alt_text`
- `raw_response_path`
- `phase1_ledger_path`
- `source_dataset`
- `source_worker`

## Orchestration Model

- main agent:
  - builds the candidate manifest
  - materializes phase-2 shards
  - publishes issued packets
  - launches and monitors workers
  - aggregates final decisions
- evaluation worker:
  - owns exactly one phase-2 shard
  - reads only assigned image and caption records
  - writes only assigned evaluation outputs
- optional judge subagent:
  - can be used inside one worker when the worker needs a second bounded reasoning pass

Recommended bounded parallelism:

- reuse the same 6 logical shard boundaries from phase 1
- do not overlap image ownership across workers

## Tool Surface

Recommended evaluation surface:

- image evidence collection:
  - `cv-mcp`
  - `moondream-mcp`
- artifact persistence:
  - filesystem MCP or local file writes through approved scripts
- post-run audit:
  - filesystem MCP

Generation is out of scope for this phase except when a record is explicitly sent to `rewrite`.

## Decision Taxonomy

Each completed caption record must end in exactly one final decision:

- `accept`
  - caption is sufficiently grounded and complete
- `rewrite`
  - caption is usable as a retry candidate but not acceptable yet
- `audit`
  - caption requires human inspection because confidence or evidence is conflicted
- `error`
  - evaluation pipeline failed to produce a reliable decision artifact

## Execution Order

### Step 0. Phase-2 Candidate Build

Main agent collects the 6 phase-1 ledgers and writes one merged candidate manifest containing only the 60 completed records.

### Step 1. Shard Reuse

Phase 2 reuses the same logical shard boundaries as phase 1 so there is no overlap drift between generation and evaluation ownership.

Recommended artifact:

- `control/project_domain/resources/manifests/phase2_caption_eval_shards/`

### Step 2. Per-Image Independent Evidence

For each record, the worker collects independent evidence from the original image.

Minimum evidence targets:

- independent description
- visible text or OCR-like observation when present
- object or layout grounding cues
- contradiction check against the generated caption

### Step 3. Atomic Checks

Break the caption into atomic units where possible:

- visible objects
- attributes
- relations
- counts
- visible text
- scene or chart label

### Step 4. Score And Decide

Each record produces:

- grounding score
- completeness score
- hallucination indicator
- final decision
- brief rationale

### Step 5. Persist Per-Record Output

Each worker writes only its own outputs:

- shard decision ledger
- shard audit queue
- shard error queue

Recommended path family:

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase2_eval_<shard>.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase2_eval_<shard>_evaluation_decisions.jsonl`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase2_eval_<shard>_audit_queue.jsonl`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase2_eval_<shard>_error_queue.jsonl`

### Step 6. Batch Aggregation

The main agent aggregates all shard outputs into:

- `phase2_caption_eval_summary.json`
- `phase2_caption_eval_accept_candidates.jsonl`
- `phase2_caption_eval_rewrite_candidates.jsonl`
- `phase2_caption_eval_audit_candidates.jsonl`
- `phase2_caption_eval_error_candidates.jsonl`

## Metrics

Minimum batch metrics:

- candidate_count
- accept_count
- rewrite_count
- audit_count
- error_count
- accept_rate
- audit_rate
- hallucination_flag_count
- completeness_flag_count
- unsupported_count carried forward from phase 1

Secondary metrics:

- count of captions requiring rewrite due to completeness problems
- count of taxonomy drift cases such as chart/table ambiguity
- count of records with visible text disagreement

## Pass / Fail Criteria

Pass:

- all 60 candidate records receive a persisted final decision
- unsupported `.emf` remains explicitly excluded rather than silently dropped
- no shard overlap occurs
- no decision artifacts are missing

Soft success:

- the batch completes but a significant `audit` set remains

Fail:

- candidate manifest does not match the 60 completed phase-1 records
- any worker writes outside its shard boundary
- decision artifacts are incomplete
- active lint hard fails from legacy machine-readable files remain unresolved and pollute the active phase-2 surface

## Expected Outputs

- one canonical phase-2 plan:
  - this file
- one phase-2 candidate manifest
- one phase-2 shard directory
- shard decision ledgers
- shard audit queues
- shard error queues
- batch summary report

## Next Decision After Phase 2

If `accept_rate` is high enough and audit volume is bounded:

- promote the accepted subset into the pre-commit review surface

If rewrite volume is high:

- design a rewrite-focused retry arm before any metadata commit

If audit volume is high:

- keep the batch in human-review mode and do not start commit operations
