# Repeated Issue: Over-Routing Via Missing Lifecycle-Touch Gate In Non-Primary Branch

## Issue Name

Over-Routing Via Missing Lifecycle-Touch Gate In Non-Primary Branch

## Symptom

A routing decision procedure has a lifecycle-touch gate in the primary (canonical) branch — routing proceeds only if the task touches launcher, config, inventory, setup, or smoke — but an equivalent gate is absent from the adjacent or temporarily-routed branch.

Result: a task that simply *uses* an adjacent tool (e.g., calls `imagegen`, reads from `filesystem`, dispatches via `agent-task-manager`) incorrectly routes to the owner skill because it matched the adjacent-surface branch before the lifecycle-touch condition was checked.

## Scope

- Quick pre-routing check in owner-family maps (`references/tool-owner-family-map.md`)
- Routing decision tree branch conditions
- Any numbered or bulleted routing procedure that branches on surface type before branching on lifecycle contact

## Guardrail

Every routing branch that routes to the owner skill — not just the primary charter branch — must carry an explicit lifecycle-touch gate:

```
only if the task also touches launcher, config, inventory, setup, or smoke for that surface
```

If the task only uses the surface's output, it must fall through to the consumer-only path, regardless of which surface type it uses.

Treat a routing branch without a lifecycle-touch gate as structurally incomplete, not as a style choice.

## Follow-up

- Add a drift prevention check to the family-map self-check section: "Does every non-consumer routing branch carry a lifecycle-touch gate?"
- Related task: `TASK_lifecycle_surface_routing_tree_rewrite.md`
- Apply gate symmetry rule whenever a new branch is added to any routing procedure: if one branch has a gate, all non-consumer branches must have the same gate type
