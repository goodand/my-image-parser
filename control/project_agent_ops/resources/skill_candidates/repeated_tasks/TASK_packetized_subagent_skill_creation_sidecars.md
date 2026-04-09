# Packetized Subagent Skill Creation Sidecars

## Pattern

Use subagents only for disjoint sidecar artifacts during repeated skill creation, while the main agent keeps ownership of shared files and registry synchronization.

## Why It Repeats

- skill creation keeps producing the same artifact families:
  - `references/runtime.md`
  - `references/troubleshooting.md`
  - `knowledge_bases/*.md`
  - `evals/evals.json`
- these are often separable enough for bounded parallel drafting
- `SKILL.md`, registries, and master plans are not safe multi-writer surfaces

## Promotion Target

- reusable subagent strategy guide
- task-packet template for skill sidecars

## Current Guidance

- `control/project_agent_ops/resources/references/REFERENCE_subagent_xhigh_skill_creation_strategy.md`

## Current Proven Example

- `skills/table-branch-activation-slice`
  - `references/runtime.md`
  - `references/troubleshooting.md`
  - `knowledge_bases/table-branch-activation-slice-knowledge-base-at2026-03-28-02-20.md`
  - `evals/evals.json`
  were drafted through disjoint issued task packets and integrated by the main agent.
