# Phase 1 Caption Experiment Parallel Execution Report

## Verdict

Phase 1 extracted-media OpenAI baseline completed successfully.

## Scope

- arm: `extracted media + OpenAI caption`
- mode: 6 shard parallel execution
- source datasets:
  - `control/project_domain/resources/cross_validation/01_full_presentation_2026-03-17/openai_api/media_extract_dataset.jsonl`
  - `control/project_domain/resources/cross_validation/02_1/openai_api/media_extract_dataset.jsonl`

## Smoke Gate

Smoke output:

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_smoke_w3.json`

Smoke result:

- pass

## Shard Results

- `phase1_ppt1_w1.json`
  - records: 7
  - status: `completed = 7`
- `phase1_ppt1_w2.json`
  - records: 8
  - status: `completed = 7`, `unsupported_media_type = 1`
- `phase1_ppt2_w3.json`
  - records: 12
  - status: `completed = 12`
- `phase1_ppt2_w4.json`
  - records: 12
  - status: `completed = 12`
- `phase1_ppt2_w5.json`
  - records: 12
  - status: `completed = 12`
- `phase1_ppt2_w6.json`
  - records: 10
  - status: `completed = 10`

## Aggregate Totals

- total records: 61
- completed: 60
- unsupported_media_type: 1

## Overlap Check

- shard JSONL inputs were disjoint
- output ledgers were disjoint
- only the main agent wrote the shared plan and this report

## Important Notes

- the only known unsupported case was the `.emf` item in the first PPT dataset
- no additional unexpected unsupported-media case appeared
- phase 1 is now a usable baseline for later evaluation or comparison arms

## Canonical Output Paths

- ledgers:
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w2.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w4.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w5.json`
  - `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6.json`
- shard manifests:
  - `control/project_domain/resources/manifests/phase1_caption_shards/`
- issued packets:
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w1-at2026-03-27-18-31.md`
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w2-at2026-03-27-18-31.md`
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w3-at2026-03-27-18-31.md`
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w4-at2026-03-27-18-31.md`
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w5-at2026-03-27-18-31.md`
  - `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w6-at2026-03-27-18-31.md`

## Next Step

Use this baseline to:

1. run evaluation overlay on selected subsets
2. compare against screenshot-based caption paths
3. decide whether to promote a comparison report into canonical project-domain resources
