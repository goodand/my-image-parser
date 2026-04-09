# Task Packet: Phase 1 Caption Experiment W6

## Goal

Run the phase-1 extracted-media OpenAI caption experiment for shard `W6` only, with the shard input and worker ledger fixed in advance.

## Packet Basis

- active plan:
  - `control/project_domain/resources/experiment_plans/PLAN_phase1_caption_experiment_parallel_execution-at2026-03-27-18-31.md`
- canonical packet template:
  - `control/project_agent_ops/resources/task_packets/canonical/image_caption_experiment_canonical_packet.json`
- standard packet template:
  - `control/project_agent_ops/resources/task_packets/standard/image_caption_experiment_standard_packet.json`
- reference issued packet style:
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_master_plan_consolidation-at2026-03-27-16-56.md`

## Fixed Contract

- worker shard input:
  - `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w6.jsonl`
- worker ledger output:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6.json`
- required sidecars derived from the ledger stem:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_responses/`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_execution_records.jsonl`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_evaluation_decisions.jsonl`

## Canonical Inputs

- shard JSONL:
  - `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w6.jsonl`
- active plan:
  - `control/project_domain/resources/experiment_plans/PLAN_phase1_caption_experiment_parallel_execution-at2026-03-27-18-31.md`
- source of truth:
  - `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
  - `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`
  - `control/project_domain/resources/knowledge_bases/KB_caption_experiment_foundation.md`
  - `control/project_domain/resources/checklists/CHECKLIST_caption_experiment_readiness.md`
  - `control/project_domain/registry/caption_experiment_resource_index.json`

## Allowed Paths

- read:
  - `control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w6.jsonl`
  - `control/project_domain/resources/experiment_plans/PLAN_phase1_caption_experiment_parallel_execution-at2026-03-27-18-31.md`
  - `control/project_agent_ops/resources/task_packets/canonical/image_caption_experiment_canonical_packet.json`
  - `control/project_agent_ops/resources/task_packets/standard/image_caption_experiment_standard_packet.json`
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_master_plan_consolidation-at2026-03-27-16-56.md`
  - `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
  - `control/project_domain/resources/specs/prose/SPEC_openai_image_caption_runner.md`
  - `control/project_domain/resources/knowledge_bases/KB_caption_experiment_foundation.md`
  - `control/project_domain/resources/checklists/CHECKLIST_caption_experiment_readiness.md`
  - `control/project_domain/registry/caption_experiment_resource_index.json`
- write:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_responses/`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_execution_records.jsonl`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_evaluation_decisions.jsonl`

## Forbidden Paths

- `.env`
- `.venv/`
- `control/archive/`
- `control/project_agent_ops/resources/task_packets/canonical/`
- `control/project_agent_ops/resources/task_packets/standard/`
- `control/project_agent_ops/resources/task_packets/issued/`
- any shard, ledger, or sidecar path not explicitly listed in this packet

## Constraints

- treat this packet as immutable for the current run
- do not modify canonical docs, packet templates, registry indexes, or another worker's outputs
- use the local caption runner only for the fixed shard in this packet
- allow network use only as required by the caption API call path used by `scripts/caption_images_openai.py`
- do not use broad retries or `--overwrite` unless the main agent republishes scope with a new packet

## Required Rules

1. Process only shard `W6`.
2. Use exactly the shard JSONL and ledger output fixed in `Fixed Contract`.
3. Keep the write set bounded to the ledger stem for `phase1_ppt2_w6` only.
4. Preserve failure evidence in the worker ledger and sidecars instead of widening scope.
5. Escalate rather than improvising if the shard definition, ledger path, or ownership boundary is ambiguous.

## Non-Goals

- Do not aggregate results across shards.
- Do not edit packet templates or canonical references.
- Do not perform human review, metadata commit, rename work, or summary-report publication.

## Expected Outputs

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_responses/`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_execution_records.jsonl`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6_evaluation_decisions.jsonl`

## Done Definition

- The worker ledger exists at the fixed output path.
- The response, execution-record, and evaluation-decision sidecars exist for the same ledger stem.
- The run only covers the rows present in shard `W6`.
- The completion summary reports processed count, failed count, and the exact output paths used.

## Stop Conditions

- the shard JSONL is missing, unreadable, or does not resolve to `phase1_ppt2_w6.jsonl`
- the fixed ledger path would overwrite ambiguous or unrelated artifacts
- the run requires writes outside the allowed paths listed in this packet
- API auth fails or the caption runner cannot preserve worker-local evidence
- duplicate ownership or overlap is detected for the shard, ledger, or sidecar paths

## Verification

1. Confirm the shard JSONL exists before execution.
2. Confirm the fixed ledger path and sidecar stem match this packet exactly.
3. Run the caption worker against the shard JSONL only.
4. Verify the ledger and all three sidecars exist after completion.
5. Verify no other phase-1 shard, ledger, or sidecar path was touched.

## Suggested Command

```bash
python3 scripts/caption_images_openai.py \
  --dataset-jsonl control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w6.jsonl \
  --output control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6.json \
  --model gpt-4.1 \
  --detail high
```

## Suggested Working Order

1. preflight the fixed shard and ledger paths
2. execute the shard run with the exact command shape above
3. verify the ledger-stem artifacts
4. return a short completion summary with counts and paths

## Handoff Note

This packet is immutable for shard `W6`. If scope, ownership, or output paths change, publish a new issued packet instead of widening this one.
