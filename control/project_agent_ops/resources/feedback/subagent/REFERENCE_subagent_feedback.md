# Subagent Feedback

## Purpose

Store project-start and ongoing feedback specific to spawned workers and subagents.

## Source Of Truth

- This file is the canonical subagent feedback surface under `project_agent_ops/resources/feedback/subagent/`.
- Append new entries instead of rewriting prior entries unless an entry is clearly invalid.

## Entry Format

For each entry, record:

- date
- worker scope
- positive signal
- coordination risk
- follow-up action

## Current Entries

- 2026-03-27
  - worker scope: phase-1 caption experiment shard execution
  - positive signal: shard-based task partitioning prevented output overlap and allowed independent ledger paths
  - coordination risk: shard-specific packet and ledger naming must stay stable or later aggregation becomes error-prone
  - follow-up action: keep shard generation centralized in the main agent and only hand out bounded shard packets to workers
