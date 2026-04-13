# Repeated Issue: Chained Entry And Git Handoff Scope Collapse

## Symptom

- an agent receives one `entry packaging` task and one `git handoff` task
- the two packets get mentally merged into one scope
- commit pressure appears too early, or the agent stages meta artifacts and scratch files that belong outside the first packet

## Scope

- chained dispatch prompts
- public entry packaging tasks
- conditional git handoff tasks
- follow-up commit waves after documentation work

## Guardrail

- write the chained rule explicitly: `ENTRY first, GIT HANDOFF only if relevant repo-local changes remain`
- do not commit during the first packet
- after entry work, inspect `git status` again before staging
- exclude unrelated scratch notes and packet/meta files unless they are the current packaging target

## Follow-Up

- keep one prompt or reference that explains the chain
- keep the entry packet and git packet separate
- stop with no-op status if the first packet leaves no bounded repo-local change

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` had to create `REFERENCE_public_surface_architect_chained_dispatch_prompt-at2026-04-13.md` because the public entry work and the git packaging work were close enough to collapse without an explicit chain rule

## Step-By-Step Evidence Trace

1. The first packet explicitly forbade git work and restricted the agent to readable entry packaging.
   - packet evidence: `control/project_agent_ops/resources/task_packets/issued/TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY.json`
2. The second packet explicitly allowed one bounded commit only if the first packet left relevant repo-local changes.
   - packet evidence: `control/project_agent_ops/resources/task_packets/issued/TASK-LEAN-02_1-GIT-HANDOFF-V2.json`
3. The two were then tied together by one chained dispatch prompt.
   - prompt evidence: `control/project_agent_ops/resources/references/REFERENCE_public_surface_architect_chained_dispatch_prompt-at2026-04-13.md`
4. The actual execution then followed the intended sequence: create `Start Here`, inspect remaining changes, validate bounded requirements, and commit only the resulting entry doc.
   - entry commit evidence: `c496b83`
5. The remaining packet, note, and scratch artifacts were then left out of that first commit instead of being pulled in prematurely.
