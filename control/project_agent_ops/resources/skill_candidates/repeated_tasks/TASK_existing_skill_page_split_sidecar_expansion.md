# Repeated Task: Existing Skill Page-Split Sidecar Expansion

## Pattern

Take an already-working `SKILL.md` that has grown too dense and split it into linked sidecar pages without rewriting the underlying runtime surface.

## Stable Recipe

1. keep `SKILL.md` thin
2. move execution details into `references/runtime.md`
3. move failure handling into `references/troubleshooting.md`
4. add topic-specific sidecars such as shard strategy, packet contract, or review gate docs
5. add one checklist, one knowledge base, and `evals/evals.json`
6. shape `evals/evals.json` as a skill-local acceptance layer and align the axes with `agent-tool-benchmark` when the skill affects orchestration or tool-use quality
7. keep the root script or wrapper unchanged unless a real contract bug exists
8. verify that the inventory and actual skill file tree still agree

## Why It Repeats

- early skills are often created as one-file surfaces first
- later sessions add shard rules, packet rules, and review boundaries
- the right fix is usually page-splitting, not another rewrite of the runtime logic

## Promotion Target

- reusable page-split checklist
- sidecar skeleton template for expanding an existing skill
- benchmark-aware eval authoring rule tied to `agent-tool-benchmark`

## Current Proven Example

- `skills/image-job-dispatcher`
  - `references/runtime.md`
  - `references/troubleshooting.md`
  - `references/shard-strategy.md`
  - `references/task-packet-contract.md`
  - `checklists/parallel-preflight.md`
  - `knowledge_bases/image-job-dispatcher-knowledge-base-at2026-03-28-10-55.md`
  - `evals/evals.json`
- `skills/image-worker`
  - `references/runtime.md`
  - `references/troubleshooting.md`
  - `references/record-contract.md`
  - `checklists/worker-preflight.md`
  - `knowledge_bases/image-worker-knowledge-base-at2026-03-28-11-20.md`
  - `evals/evals.json`
- `skills/image-result-auditor`
  - `references/runtime.md`
  - `references/troubleshooting.md`
  - `references/review-queue-contract.md`
  - `checklists/audit-preflight.md`
  - `knowledge_bases/image-result-auditor-knowledge-base-at2026-03-28-11-20.md`
  - `evals/evals.json`
