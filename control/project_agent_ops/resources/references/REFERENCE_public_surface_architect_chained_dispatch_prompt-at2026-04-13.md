# REFERENCE_public_surface_architect_chained_dispatch_prompt-at2026-04-13

## Purpose

This is the ready-to-send chained dispatch prompt for `Public Surface Architect`.

Use it when the agent should:

1. package a clearer public entry surface first
2. run git packaging only if that first step leaves relevant repo-local changes

## Chained Dispatch Prompt

```text
Agent: Public Surface Architect

Use these packets in order:

1. TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY
2. TASK-LEAN-02_1-GIT-HANDOFF-V2 only if step 1 leaves relevant repo-local changes inside allowed paths

Execution rule:
- Do not collapse the two packets into one mental scope.
- Finish the ENTRY packet first.
- If ENTRY produces no repo-local changes, stop and report no-op.
- If ENTRY produces repo-local changes inside allowed paths, continue to the GIT HANDOFF packet.

Current role boundary:
- Control-Plane Program Steward owns toolization, contracts, routing, and handoff semantics.
- Public Surface Architect owns readable public entry packaging and, only when needed, repo-local git packaging of that public surface.
- Do not reinterpret owner-family or MCP lifecycle boundaries.

Start with TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY:

## Goal
Task: TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY — lean 02_1 public surface entry packaging
Create or tighten one readable Start Here public-entry surface for the lean 02_1 multimodal PPT stack so another agent can find the right deck, matrix, handoff bundle, review indexes, and local external-tool references without re-deriving the routing model.
Why: The tool-facing surfaces are already in place, but they are spread across multiple references. Public Surface Architect should package these into a simpler navigational surface without changing contracts, scripts, or ownership boundaries.

### Non-goals
- Do not change owner-family semantics, skill routing, MCP lifecycle ownership, or bundle contracts.
- Do not modify decks, renders, scripts, or machine-readable manifests.
- Do not do git commit, push, or PR work in this packet.

### Success condition
- One Start Here surface exists or the current v2 review index is tightened enough that another agent can discover the stack in one pass.
- Local slides-grab clone and skills are linked as donor/reference surfaces.
- Upstream GitHub remains provenance only.

Then conditionally continue with TASK-LEAN-02_1-GIT-HANDOFF-V2:

## Goal
Task: TASK-LEAN-02_1-GIT-HANDOFF-V2 — lean 02_1 portfolio git handoff v2
Inspect the current lean 02_1 portfolio public-surface artifacts, verify whether any relevant uncommitted files remain, and create exactly one intentional git commit only if safe and necessary.
Why: This is the chained follow-up after TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY when that entry-packaging step leaves relevant repo-local changes.

### Non-goals
- Do not reinterpret or edit portfolio content, deck layout, or control-plane meaning.
- Do not push, open a PR, or change branch strategy.
- Do not stage files from outside this repository, including symbolic_links and sibling-workspace clones.

### Commit condition
- Commit only if relevant repo-local lean 02_1 public-surface files remain uncommitted after ENTRY.
- If all relevant artifacts are already committed, report no-op and do not create an empty commit.
- Exclude unrelated pending files, especially repo-root 2026-04-09.md.

Required local reference surfaces:
- control/user_decisions/resources/notes/NOTE_role_boundary_reset_between_control_plane_program_steward_and_public_surface_architect-at2026-04-13-16-07.md
- control/project_domain/resources/references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md
- control/project_domain/resources/references/REFERENCE_lean_02_1_system_first_portfolio_v2_review_index-at2026-04-13.md
- control/project_domain/resources/references/REFERENCE_ppt_page_link_matrix_v0_1_step_by_step-at2026-04-13.md
- control/project_domain/resources/references/REFERENCE_ppt_regeneration_handoff_bundle_v0_1-at2026-04-13.md

Local donor surface:
- /Users/jaehyuntak/Desktop/Project_____현재_진행중인/vscode-markdown-review-surface/control/team/resources/external_repos/slides-grab

Upstream provenance only:
- https://github.com/vkehfdl1/slides-grab

Report back:
- ENTRY result
- whether chaining to GIT HANDOFF was necessary
- staged file list if commit happened
- validation results
- final commit sha if commit happened
- excluded files and reasons
```

## Packet Links

- [TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY.json](../task_packets/issued/TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY.json)
- [TASK-LEAN-02_1-GIT-HANDOFF-V2.json](../task_packets/issued/TASK-LEAN-02_1-GIT-HANDOFF-V2.json)

## One-Line Summary

Use this prompt when `Public Surface Architect` should first improve the readable public entry surface and only then, if that work leaves relevant repo-local changes, perform one bounded git packaging pass.
