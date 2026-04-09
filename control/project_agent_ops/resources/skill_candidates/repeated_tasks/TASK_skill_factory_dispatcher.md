# Repeated Task: Skill Factory Dispatcher

## Pattern

The most repeated workflow is not "tool list wrapping" but packetized skill creation itself:

- choose a repeated pattern worth promotion
- decide whether it becomes a new skill or a page-split expansion of an existing one
- keep `SKILL.md` and shared registries main-agent-owned
- issue disjoint sidecar packets to subagents
- integrate, verify, and record smoke evidence centrally

## Stable Recipe

1. triage the repeated pattern first
2. decide `new skill` versus `existing skill page-split expansion`
3. materialize a standard or canonical sidecar packet
4. issue one packet per disjoint artifact family
5. keep tool inventory as a reference input, not as the owned workflow
6. keep the main agent responsible for `SKILL.md`, `session_paths.json`, `tool_inventory.json`, and master plans
7. validate sidecars and smoke before promotion

## Why It Repeats

- repeated tasks often become skills
- repeated skills often need sidecar splitting
- subagent use only becomes efficient when the packet and ownership contract is already fixed

## Promotion Target

- reusable `skill-factory-dispatcher` skill
- standard and canonical packet templates for sidecar creation

## Current Canonical Inputs

- `control/project_agent_ops/resources/task_packets/standard/skill_creation_sidecar_standard_packet.json`
- `control/project_agent_ops/resources/task_packets/canonical/skill_creation_sidecar_canonical_packet.json`
- `control/project_agent_ops/resources/references/REFERENCE_subagent_xhigh_skill_creation_strategy.md`
