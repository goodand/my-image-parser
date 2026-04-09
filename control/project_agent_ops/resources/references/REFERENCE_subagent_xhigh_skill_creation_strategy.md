# Subagent XHigh Skill Creation Strategy

## Purpose

Define a practical strategy for using `gpt-5.4 xhigh` subagents during repeated skill creation and adjacent workspace artifact work without creating context drift, overlapping edits, or registry inconsistency.

This is an operations guide, not a runtime packet.

## Core Position

Use subagents aggressively for:

- read-heavy discovery
- bounded draft generation
- evidence gathering
- ambiguity resolution
- disjoint-file artifact production

Do **not** use subagents as uncontrolled multi-writer editors over the same canonical files.

The main agent remains the only source of truth for:

- final `SKILL.md`
- shared registry updates
- `session_paths.json`
- `tool_inventory.json`
- master plan or cross-document synchronization

## Best Fit For `gpt-5.4 xhigh`

`gpt-5.4 xhigh` should be used where reasoning quality matters more than raw throughput:

- deciding skill boundaries
- converting repeated-task patterns into stable ownership rules
- resolving ambiguous runtime or troubleshooting cases
- reviewing whether a new skill should own a script, wrapper, or only documentation
- judging whether an artifact belongs in `references/`, `knowledge_bases/`, `checklists/`, or `evals/`

It is **not** the preferred path for bulk tool invocation or simple registry patching.

## Recommended Parallel Shape For Skill Creation

### Main Agent

Owns:

- skill boundary decision
- final file structure
- shared path ownership map
- final integration
- final smoke interpretation
- registry and repeated-pattern updates

### Subagent A: Runtime And Invocation

Owns only:

- `references/runtime.md`
- wrapper command examples
- CLI contract review

### Subagent B: Troubleshooting And Failure Surfaces

Owns only:

- `references/troubleshooting.md`
- likely failure cases
- stop conditions and escalation notes

### Subagent C: Knowledge Base And Rationale

Owns only:

- `knowledge_bases/*.md`
- recurrence rationale
- why-the-skill-exists notes

### Subagent D: Evals And Shape Checks

Owns only:

- `evals/evals.json`
- case matrix
- expected boundaries

Do not treat `evals/evals.json` as random prompt examples.
When the skill affects orchestration, tool-use quality, or packetized worker behavior, shape the eval axes so they can later map into the benchmark registry defined by:

- `claude-gemini-communicator/skills/Skills-Create-Project/agent-tool-benchmark/SKILL.md`

Preferred split:

- `evals/evals.json`: skill-local acceptance and boundary cases
- `agent-tool-benchmark`: metric formulas and scoring logic such as AST Accuracy, Pass Rate, F1, SR@k, Resolve Rate, GED, or Action Score

### Optional Subagent E: Wrapper Or Smoke Sidecar

Use only if the write set is disjoint:

- skill-local thin wrapper
- bounded smoke artifact draft

The main agent should still keep ownership of the root script and shared libraries.

### Optional Read-Only Auditor

Use only as a secondary checker:

- independent file-tree audit
- claim verification against smoke artifacts
- sidecar drift spotting

This auditor is nonblocking. If it times out while the main agent already has enough local evidence, the main agent should finish the canonical verdict directly and close the subagent.

## Overlap Prevention Rules

1. Every subagent must receive an explicit write set.
2. No two subagents may own the same file.
3. Shared files stay with the main agent:
   - `SKILL.md`
   - `session_paths.json`
   - `tool_inventory.json`
   - master plan files
4. If a subagent needs to suggest a patch to a shared file, it should report the suggestion, not apply it.
5. The main agent integrates all shared-file changes after reviewing subagent outputs.

## Task Packet Contract

Every subagent should receive a packet with at least:

- `goal`
- `scope`
- `non_goals`
- `owned_paths`
- `reference_paths`
- `done_definition`
- `required_checks`
- `evidence_output_paths`

Prefer file-backed packets under:

- `control/project_agent_ops/resources/task_packets/issued/`

Do not rely on long free-form chat context as the handoff medium.

## Context Minimization Rule

Pass the smallest useful context:

- one source repeated-task or spec file
- one existing script or wrapper if relevant
- one target output directory
- one packet file

Do not paste whole master plans or long feedback threads into every worker prompt.

If a subagent needs more context, the main agent should add one more file path, not a giant prose summary.

## Skill-Creation Workflow

1. Main agent decides whether the repeated pattern is really skill-worthy.
2. Main agent fixes the target structure and ownership map.
3. Main agent writes or issues task packets.
4. Subagents produce disjoint artifacts in parallel.
5. Main agent reviews outputs and normalizes tone and boundaries.
6. Main agent patches shared files and registry.
7. Main agent runs smoke and records canonical evidence.
8. Main agent appends repeated-task or repeated-issue promotions if the pattern recurs.

## Eval Layering Rule

For repeated skill creation, treat evals as two layers:

1. local acceptance layer
- file: `evals/evals.json`
- purpose: prove the skill boundary, ownership rule, failure policy, and non-goals

2. benchmark layer
- source: `agent-tool-benchmark`
- purpose: provide reusable formulas and scoring logic when the skill later needs quantitative orchestration or tool-use evaluation

Use the local layer by default.
Pull in the benchmark layer when:

- the skill measures tool-call quality
- the skill governs packetized orchestration
- the skill introduces Langfuse or score-bearing runtime traces

## Recommended Concurrency

For repeated skill creation:

- default: `3` to `4` subagents
- high-confidence disjoint artifact mode: up to `5`
- avoid `10` unless the work is shard-like and each worker owns a fully isolated packet

Good `10-way` fan-out cases:

- one-image-one-worker caption packets
- batch review over disjoint shard manifests
- read-only ambiguity classification

Bad `10-way` fan-out cases:

- one skill directory with shared files
- registry synchronization
- master plan consolidation

## Failure Patterns To Watch

### Context Drift

Symptom:

- subagent writes something locally coherent but misaligned with repo policy

Mitigation:

- pass canonical reference paths
- keep packet scope narrow
- require file evidence in the return summary

### Multi-Writer Collision

Symptom:

- two subagents edit the same skill or registry file differently

Mitigation:

- explicit write-set ownership
- main-agent-only integration for shared files

### Over-Delegation

Symptom:

- subagents spend tokens rediscovering context faster than the main agent could have handled the task directly

Mitigation:

- only delegate sidecar work
- keep blocking critical-path work local

### Read-Only Auditor Timeout

Symptom:

- an explorer or read-only auditor subagent times out before returning findings

Mitigation:

- keep the audit nonblocking
- finish the verdict with local file reads, tests, and artifact checks
- close the subagent instead of waiting indefinitely

### Registry Drift

Symptom:

- new skill exists but `session_paths.json` or tool inventory was not updated

Mitigation:

- registry updates remain main-agent-owned
- final integration checklist must include registry sync

## Practical Recommendation For This Workspace

When adding or promoting a skill:

- keep the main agent as architect and integrator
- use `gpt-5.4 xhigh` subagents only for disjoint sidecar pages
- use file-backed task packets
- do not let subagents patch shared registries or master plans

This gives most of the speed benefit without losing canonical control.
