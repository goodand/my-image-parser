# Task Packet: Phase 1 Caption Experiment W1

## Goal

Run the phase-1 extracted-media OpenAI caption experiment for shard `W1` only, using the exact shard JSONL and writing only the exact ledger stem bound in this packet.

## Packet Basis

This issued packet is derived from these source artifacts:

- `control/project_domain/resources/experiment_plans/PLAN_phase1_caption_experiment_parallel_execution-at2026-03-27-18-31.md`
- `control/project_agent_ops/resources/task_packets/canonical/image_caption_experiment_canonical_packet.json`
- `control/project_agent_ops/resources/task_packets/standard/image_caption_experiment_standard_packet.json`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_master_plan_consolidation-at2026-03-27-16-56.md`

## Fixed Execution Binding

- worker id: `W1`
- shard JSONL: `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt1_w1.jsonl`
- output ledger: `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
- derived sidecars:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_responses/`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_execution_records.jsonl`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_evaluation_decisions.jsonl`
- expected rows: `7`
- first image id: `01_full_presentation_2026-03-17:image1.png`
- last image id: `01_full_presentation_2026-03-17:image15.png`

Exact command contract:

```bash
python3 scripts/caption_images_openai.py \
  --dataset-jsonl control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt1_w1.jsonl \
  --output control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json \
  --model gpt-4.1 \
  --detail high
```

## In-Scope Inputs

- required read inputs:
  - `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt1_w1.jsonl`
  - `control/project_domain/resources/experiment_plans/PLAN_phase1_caption_experiment_parallel_execution-at2026-03-27-18-31.md`
  - `control/project_agent_ops/resources/task_packets/canonical/image_caption_experiment_canonical_packet.json`
  - `control/project_agent_ops/resources/task_packets/standard/image_caption_experiment_standard_packet.json`
  - `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
  - `control/project_domain/resources/knowledge_bases/KB_caption_experiment_foundation.md`
  - `control/project_domain/resources/checklists/CHECKLIST_caption_experiment_readiness.md`
  - `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`
  - `control/project_domain/registry/caption_experiment_resource_index.json`
- allowed write targets:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_responses/`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_execution_records.jsonl`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_evaluation_decisions.jsonl`

## Required Rules

1. Process only shard `W1`; do not read from or write to another worker shard, ledger, or sidecar path.
2. Treat the shard JSONL path, ledger path, and command line in this packet as exact bindings, not examples.
3. Keep the packet immutable. If shard ownership, output binding, or rerun authority changes, stop and request a new issued packet.
4. Do not modify canonical docs, packet templates, registry indexes, aggregate reports, or other workers' outputs.
5. Do not use `--overwrite`. If the bound ledger stem already exists and explicit rerun authorization is absent, stop and escalate instead of widening scope.
6. Keep failure evidence in the bound sidecars instead of dropping rows, widening the packet, or silently retrying broad scope.
7. Return only a short completion summary with processed count, failed count, and the bound output paths.

## Non-Goals

- Do not aggregate results across shards.
- Do not create or edit packet templates, plans, reports, or shared summaries.
- Do not perform screenshot-arm work, human review, metadata commit, or rename work.
- Do not mutate files outside the bound ledger stem.

## Expected Outputs

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_responses/`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_execution_records.jsonl`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_evaluation_decisions.jsonl`

## Done Definition

- The bound ledger exists and is readable.
- The bound sidecars exist and share the same ledger stem.
- The run covers exactly the `7` rows in shard `W1` and nothing outside that shard.
- No other worker ledger or shared canonical artifact was modified.
- The completion summary reports processed count, failed count, and the bound output paths.

## Stop Conditions

- The shard JSONL is missing, ambiguous, or shows duplicate `image_id`.
- API auth fails or the caption runner cannot start.
- The bound ledger path or sidecars already exist without explicit rerun approval.
- Any required write would land outside the bound ledger stem.
- More than packet-bounded scope is required to finish the run safely.

## Verification

1. Confirm the four packet-basis source artifacts exist.
2. Confirm the shard JSONL exists and contains `7` rows bounded from `01_full_presentation_2026-03-17:image1.png` through `01_full_presentation_2026-03-17:image15.png`.
3. Confirm the bound ledger stem is the only intended write target.
4. Run the caption worker against the shard JSONL only.
5. Verify the ledger and all bound sidecars exist after completion.
6. Verify no other phase-1 ledger path was touched.

## Suggested Working Order

1. read the packet basis and shard
2. confirm the no-overwrite condition and write boundary
3. execute the bound caption command
4. verify the ledger plus sidecars
5. return the short completion summary

## Handoff Note

This packet is immutable for shard `W1`. If scope, rerun authority, or output binding changes, publish a new issued packet instead of widening this one.
