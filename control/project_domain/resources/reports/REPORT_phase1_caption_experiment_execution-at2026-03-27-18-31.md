# Phase 1 Caption Experiment Execution Report

## Summary

Phase 1 ran the `extracted media + OpenAI caption` baseline on 6 non-overlapping shards.

Result:

- total records: `61`
- completed: `60`
- unsupported_media_type: `1`
- expected unsupported case: one `.emf` item

The observed failure pattern matches the expected unsupported-media boundary.

## Smoke Gate

Smoke command:

```bash
python3 scripts/caption_images_openai.py \
  --dataset-jsonl control/project_domain/resources/manifests/phase1_caption_shards/phase1_ppt2_w3.jsonl \
  --output control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_smoke_w3.json \
  --limit 1
```

Smoke artifacts:

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_smoke_w3.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_smoke_w3_execution_records.jsonl`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_smoke_w3_evaluation_decisions.jsonl`

Smoke verdict:

- pass

## Shard Outputs

- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w2.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w3.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w4.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w5.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt2_w6.json`

Each shard also produced:

- `_responses/`
- `_execution_records.jsonl`
- `_evaluation_decisions.jsonl`

## Aggregated Counts

| Ledger | Records | Status |
|---|---:|---|
| `phase1_ppt1_w1.json` | 7 | `completed=7` |
| `phase1_ppt1_w2.json` | 8 | `completed=7`, `unsupported_media_type=1` |
| `phase1_ppt2_w3.json` | 12 | `completed=12` |
| `phase1_ppt2_w4.json` | 12 | `completed=12` |
| `phase1_ppt2_w5.json` | 12 | `completed=12` |
| `phase1_ppt2_w6.json` | 10 | `completed=10` |

## Packet Surface

Issued packets were created for the 6 workers:

- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w1-at2026-03-27-18-31.md`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w2-at2026-03-27-18-31.md`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w3-at2026-03-27-18-31.md`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w4-at2026-03-27-18-31.md`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w5-at2026-03-27-18-31.md`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_caption_experiment_w6-at2026-03-27-18-31.md`

## Notes

- Overlap prevention worked: each worker wrote to a unique ledger path.
- Aggregation used record-level statuses, not `processed_count`.
- `processed_count` in the per-shard ledgers was not used as the truth source because it did not align with the final record totals.

## Canonical Summary Artifact

- `control/project_domain/resources/manifests/phase1_caption_experiment_summary_at2026_03_27.json`

## Next Actions

1. inspect a sample of completed captions for quality
2. decide whether to run the evaluation overlay on this baseline
3. decide whether screenshot-based comparison should proceed after viewer-surface setup
