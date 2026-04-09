# Phase 1 Caption Experiment Parallel Execution Plan

## Purpose

Run the first operational caption experiment on the most ready arm:

- `extracted media + OpenAI caption`

This phase is designed to:

- avoid screenshot-viewer dependency
- maximize parallel throughput with bounded shard workers
- preserve clean write boundaries
- leave canonical evidence for later comparison arms

## Why This Is Phase 1

This arm is the safest first slice because:

1. the canonical PPT resources already exist
2. extracted image datasets already exist
3. the OpenAI runner already has a smoke result
4. it does not require simulator or viewer-surface setup

The screenshot arm and broader multi-arm comparison stay out of phase 1.

## Phase 1 Scope

In scope:

- one-image smoke gate
- full extracted-media batch for both PPT datasets
- 6 parallel worker execution pass
- ledger and sidecar aggregation

Out of scope:

- screenshot arm execution
- final human review completion
- rename or metadata commit
- final cross-arm comparison report

## Canonical Inputs

- PPT resources:
  - `control/project_domain/resources/assets/caption_experiment/pptx/`
- extracted media resources:
  - `control/project_domain/resources/assets/caption_experiment/extracted_media/`
- dataset JSONL:
  - `control/project_domain/resources/cross_validation/01_full_presentation_2026-03-17/openai_api/media_extract_dataset.jsonl`
  - `control/project_domain/resources/cross_validation/02_1/openai_api/media_extract_dataset.jsonl`
- source of truth documents:
  - `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
  - `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`
  - `control/project_domain/resources/knowledge_bases/KB_caption_experiment_foundation.md`
  - `control/project_domain/resources/checklists/CHECKLIST_caption_experiment_readiness.md`

## Readiness Facts

- dataset count:
  - `01_full_presentation_2026-03-17`: 15 rows
  - `02_1`: 46 rows
  - total: 61 rows
- known unsupported case:
  - one `.emf` row exists in the first dataset
  - expected handling: `unsupported_media_type` or equivalent failed-state artifact

## Orchestration Model

Project-local agent config for this phase:

- `.codex/config.toml`
- `model = "gpt-5.4"`
- `model_reasoning_effort = "xhigh"`
- `[agents].max_threads = 10`
- `[agents].max_depth = 1`

Execution note:

- thread cap stayed at `10`
- actual bounded worker count for the completed phase-1 run was `6`

- main agent:
  - performs preflight
  - materializes shard JSONL inputs
  - publishes issued task packets
  - launches and monitors workers
  - aggregates ledgers and sidecars
- worker agents:
  - exactly one shard each
  - no shared output path
  - no canonical doc mutation
- MCP usage:
  - use MCP for filesystem inspection, registry verification, and post-run evidence collection
  - keep per-image caption generation on the local runner to reduce write contention

## Overlap Prevention Rules

1. one shard JSONL belongs to exactly one worker
2. one output ledger path belongs to exactly one worker
3. one response sidecar directory belongs to exactly one worker
4. only the main agent writes shared summary artifacts
5. workers do not patch canonical docs during the execution pass

## Execution Order

### Step 0. Preflight

The main agent confirms:

- API key is available
- the two dataset JSONL files exist
- canonical docs and packet templates exist
- no output path collision exists in the planned phase-1 output directory

### Step 1. Smoke Gate

Run one-image smoke first from extracted media.

Recommended target:

- one supported PNG or JPEG from `02_1`

Pass condition:

- ledger written
- raw response sidecar written
- execution record sidecar written
- evaluation decision sidecar written

Fail condition:

- phase 1 does not scale to batch

### Step 2. Shard Materialization

The main agent first creates bounded shard JSONL files with explicit no-overlap guarantees.

For the completed phase-1 run, the actual shard set was:

- `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt1_w1.jsonl`
- `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt1_w2.jsonl`
- `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w3.jsonl`
- `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w4.jsonl`
- `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w5.jsonl`
- `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w6.jsonl`

Completed allocation:

- `01_full_presentation_2026-03-17`: 2 workers
- `02_1`: 4 workers

Legacy planning artifact retained for cleanup or reclassification:

- `control/project_domain/resources/manifests/phase1_caption_10w_shards/phase1_caption_10w_manifest.json`

### Step 3. Packet Publication

The main agent publishes bounded issued packets for the chosen shard set.

Each issued packet must fix:

- shard JSONL path
- explicit output ledger path
- allowed paths
- stop conditions
- evidence paths

Recommended issued packet location:

- `control/project_agent_ops/resources/task_packets/issued/`

### Step 4. Parallel Worker Execution

Launch bounded subagents in parallel.

Recommended model:

- `gpt-5.4`
- reasoning effort: `xhigh`

For the completed phase-1 run, 6 workers were used.

Each worker runs only one shard and writes only to its own ledger.

Recommended ledger naming:

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_caption_10w_01_full_presentation_2026-03-17_w01.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_caption_10w_01_full_presentation_2026-03-17_w02.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_caption_10w_02_1_w03.json`
- `...`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_caption_10w_02_1_w10.json`

Each ledger implies its own sidecars:

- `_responses/`
- `_execution_records.jsonl`
- `_evaluation_decisions.jsonl`

### Step 5. Main-Agent Aggregation

After all worker ledgers complete, the main agent:

1. verifies all expected ledgers exist
2. verifies total processed rows equals 61
3. verifies known unsupported count is exactly the expected `.emf` case unless more unsupported files are discovered
4. writes a phase-1 summary report
5. writes or updates a merged manifest for downstream comparison

### Step 6. Post-Phase Decision

If the phase-1 baseline is stable:

- proceed to evaluation overlay or comparison arm

If not stable:

- revise the packet context
- rerun only failed shards
- do not restart successful shards unnecessarily

## Observed Execution Result

Completed result:

- workers used: `6`
- total records: `61`
- completed: `60`
- unsupported_media_type: `1`
- expected unsupported case: one `.emf` item

Canonical result artifacts:

- `control/project_domain/resources/reports/REPORT_phase1_caption_experiment_execution-at2026-03-27-18-31.md`
- `control/project_domain/resources/manifests/phase1_caption_experiment_summary_at2026_03_27.json`

## Phase 2 Preflight Gate

Before phase 2 starts:

- sample quality review should be performed on a subset of completed captions
- the `.emf` unsupported case should remain explicitly explained
- legacy `phase1_caption_10w` packet and ledger JSON filenames should be cleaned up, reclassified, or archived so active machine-readable artifacts return to a hard-fail-free lint state

## Recommended Worker Commands

Pattern:

```bash
python3 scripts/caption_images_openai.py \
  --dataset-jsonl <shard_jsonl> \
  --output <worker_ledger_json> \
  --model gpt-4.1 \
  --detail high
```

Use `--retry-failed` only for a rerun pass.
Do not use `--overwrite` for all shards unless the main agent explicitly resets the phase.

## Stop Conditions

- smoke gate fails
- API auth fails
- multiple workers write to the same output path
- shard definition is ambiguous
- more than expected unsupported-media failures appear without explanation
- any packet or shard manifest shows duplicate `image_id`

## Done Definition

- bounded worker shards are defined without overlap
- smoke gate is defined before batch scale
- output paths and aggregation ownership are fixed
- no worker requires write access to shared canonical docs
- the plan records the completed phase-1 baseline and its phase-2 entry gate

## One-Line Summary

Phase 1 ran the extracted-media OpenAI baseline first, with one smoke gate, six non-overlapping shard workers, and a single main-agent aggregation pass that produced the current baseline summary for later comparison arms.
