# Task Packet: Image Job Dispatcher Fast-Start Packet Integration

## Goal

Extend `image-job-dispatcher` so the skill explicitly owns packet-first startup for bounded parallel experiment slices.

## Why This Fits

`image-job-dispatcher` already owns:

- one-image-per-worker dispatch
- shard materialization
- task-packet contract
- owned-path discipline

The repeated pattern now worth absorbing is:

- fast-start packet for parallel experiment session split

## Scope

Teach the skill how to start bounded experiment sessions from frozen truth and narrow owned paths instead of from full-plan rereads.

## Owned Write Surfaces

- `skills/image-job-dispatcher/SKILL.md`
- `skills/image-job-dispatcher/references/task-packet-contract.md`
- `skills/image-job-dispatcher/references/runtime.md`
- `skills/image-job-dispatcher/references/troubleshooting.md`
- `skills/image-job-dispatcher/checklists/parallel-preflight.md`
- optional new reference under `skills/image-job-dispatcher/references/`
- optional KB patch under `skills/image-job-dispatcher/knowledge_bases/`

## Required Inputs

- [KB_repeated_task_patterns.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/skill_candidates/repeated_tasks/KB_repeated_task_patterns.md)
- [TASK_PACKET_phase1_image4_multi_component_recrop_reentry_slice-at2026-03-30.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_phase1_image4_multi_component_recrop_reentry_slice-at2026-03-30.md)

## Expected Changes

1. skill body mentions packet-first bounded session startup as an owned extension of dispatch
2. task-packet contract reference explains:
   - fixed truth sources
   - fixed interpretation
   - owned write surfaces
   - non-goals for bounded slices
3. parallel preflight checklist adds one check for fast-start packet readiness before worker fanout
4. troubleshooting covers the failure mode where a session re-enters through the master plan instead of the packet

## Non-Goals

- do not change current worker runtime contracts
- do not rewrite existing issued packets
- do not alter auditor or parser skills

## Done Definition

- a future bounded parallel slice can start from `image-job-dispatcher` references without reconstructing the full experiment history
- the packet-first rule is discoverable from the skill itself

## Verification

1. re-read the updated skill
2. confirm the skill still owns dispatch, not semantic judging
3. confirm the packet-first guidance stays bounded to startup and owned-path discipline
