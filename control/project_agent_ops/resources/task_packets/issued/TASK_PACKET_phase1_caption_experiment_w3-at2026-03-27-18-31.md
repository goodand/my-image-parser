# Task Packet: Phase 1 Caption Experiment W3

## Goal

Run the phase-1 extracted-media OpenAI caption experiment for shard `W3` only, with one fixed shard-to-ledger binding and no writes outside this worker's output stem.

## Packet Sources

- active execution plan:
  - `control/project_domain/resources/experiment_plans/PLAN_phase1_caption_experiment_parallel_execution-at2026-03-27-18-31.md`
- canonical packet profile:
  - `control/project_agent_ops/resources/task_packets/canonical/image_caption_experiment_canonical_packet.json`
- standard packet profile:
  - `control/project_agent_ops/resources/task_packets/standard/image_caption_experiment_standard_packet.json`
- markdown issued-packet reference:
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_master_plan_consolidation-at2026-03-27-16-56.md`

## Bound Shard And Ledger

- shard JSONL:
  - `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w3.jsonl`
- output ledger:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3.json`
- required sidecars:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_responses/`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_execution_records.jsonl`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_evaluation_decisions.jsonl`
- shard facts:
  - `12` rows
  - first `image_id` in shard order: `02_1:image1.png`
  - last `image_id` in shard order: `02_1:image2.png`

## Canonical Inputs

- source of truth:
  - `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
  - `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`
  - `control/project_domain/resources/knowledge_bases/KB_caption_experiment_foundation.md`
  - `control/project_domain/resources/checklists/CHECKLIST_caption_experiment_readiness.md`
  - `control/project_domain/registry/caption_experiment_resource_index.json`

## Allowed Paths

- read:
  - `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w3.jsonl`
  - `control/project_domain/resources/pptx_jobs/02_1/media/`
  - `control/project_domain/resources/`
  - `control/project_domain/registry/`
  - `control/project_agent_ops/resources/task_packets/canonical/image_caption_experiment_canonical_packet.json`
  - `control/project_agent_ops/resources/task_packets/standard/image_caption_experiment_standard_packet.json`
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_master_plan_consolidation-at2026-03-27-16-56.md`
- write:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_responses/`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_execution_records.jsonl`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_evaluation_decisions.jsonl`

## Required Rules

1. Process only shard `W3`.
2. Use exactly the ledger path fixed in this packet.
3. Use only the sidecar paths derived from the fixed ledger stem in this packet.
4. Do not modify canonical docs, packet templates, registry indexes, scripts, or other workers' outputs.
5. You are not alone in the codebase. Do not revert others' edits. If the fixed output stem already contains unexpected files or conflicting content, stop and escalate instead of cleaning it up.
6. Network use is limited to the caption runner calls required for this shard only.
7. Do not use broad retry or overwrite scope. Keep per-row failure evidence if any record fails.

## Non-Goals

- Do not aggregate results across shards.
- Do not edit packet templates or the active execution plan.
- Do not perform human review, metadata commit, rename work, or final comparison reporting.

## Execution Hint

Use the phase-1 worker command pattern with the fixed shard and ledger bindings from this packet:

```bash
python3 scripts/caption_images_openai.py \
  --dataset-jsonl control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w3.jsonl \
  --output control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3.json \
  --model gpt-4.1 \
  --detail high
```

Do not add `--overwrite`. Use `--retry-failed` only if a superseding packet explicitly authorizes a rerun.

## Expected Outputs

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_responses/`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_execution_records.jsonl`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3_evaluation_decisions.jsonl`

## Done Definition

- The worker ledger exists.
- The sidecar artifacts exist.
- The run covers only the `12` rows in shard `W3`.
- Failure evidence remains captured for any failed row.
- A short completion summary includes processed count, failed count, and fixed output paths.

## Verification

1. Confirm the shard file and canonical context files exist before running.
2. Confirm the fixed ledger stem does not collide with another worker's ownership before writing.
3. Run the caption worker against the shard JSONL only.
4. Verify ledger and sidecars exist after completion.
5. Verify no other phase-1 ledger stem or canonical control document was touched.

## Suggested Working Order

1. preflight the shard path
2. execute the shard run
3. verify output artifacts and any failed-row evidence
4. return a short summary with fixed paths

## Handoff Note

This packet is immutable for shard `W3` and ledger stem `phase1_ppt2_w3`. If shard, ledger, model, or scope changes, publish a new packet instead of widening this one.
