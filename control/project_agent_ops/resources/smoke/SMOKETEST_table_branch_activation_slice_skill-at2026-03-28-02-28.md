# Table Branch Activation Slice Skill Smoke

## Purpose

Verify that the new `table-branch-activation-slice` skill was created through packetized parallel sidecar drafting and that its canonical sidecar structure is complete.

## Packetized Parallel Inputs

- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_table_branch_activation_slice_runtime-at2026-03-28-02-20.json`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_table_branch_activation_slice_troubleshooting-at2026-03-28-02-20.json`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_table_branch_activation_slice_kb-at2026-03-28-02-20.json`
- `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_table_branch_activation_slice_evals-at2026-03-28-02-20.json`

## Verified Skill Surface

- `skills/table-branch-activation-slice/SKILL.md`
- `skills/table-branch-activation-slice/references/runtime.md`
- `skills/table-branch-activation-slice/references/troubleshooting.md`
- `skills/table-branch-activation-slice/knowledge_bases/table-branch-activation-slice-knowledge-base-at2026-03-28-02-20.md`
- `skills/table-branch-activation-slice/evals/evals.json`

## Verification

- `evals/evals.json` is valid JSON
- all four sidecar files exist
- shared-file ownership remained with the main agent
- sidecar drafting used disjoint write sets through issued task packets

## Interpretation

This is a doc-heavy operational skill.

The smoke proves:

- packetized subagent sidecar drafting works for bounded skill creation
- the new skill has the expected `runtime / troubleshooting / KB / evals` structure
- the current table branch activation protocol now has a reusable skill surface
