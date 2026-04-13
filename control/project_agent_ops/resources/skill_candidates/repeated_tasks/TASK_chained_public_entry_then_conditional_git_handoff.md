# Repeated Task: Chained Public Entry Then Conditional Git Handoff

## Pattern Name

- chained public entry then conditional git handoff

## Trigger

- one packet is responsible for readable entry packaging only
- a second packet is responsible for git packaging only if the first packet leaves relevant repo-local changes
- the next agent must not collapse the two packets into one scope

## Stable Steps

1. Execute the entry-packaging packet first and do not commit during that packet.
2. Inspect `git status` after the entry result exists.
3. Determine whether the remaining uncommitted change is inside the later packet's allowed paths.
4. Run the required JSON and file-existence checks before any commit.
5. Stage only the repo-local entry artifact or lean-slice remainder that actually changed.
6. Exclude unrelated scratch notes, sibling-workspace files, and packet/meta artifacts that are outside the bounded packaging scope.
7. Commit exactly once if a relevant repo-local change remains; otherwise stop with a no-op report.

## Candidate Promotion

- reusable chained dispatch prompt for `ENTRY first -> conditional GIT HANDOFF`
- packet rule: do not merge `make it readable` and `commit it` into one mental scope
- follow-up git checklist: `allowed path / required checks / no empty commit`

## Promotion Trigger

- another documentation or public-surface pass must sometimes end in a commit, but only when the first packet really leaves a bounded repo-local delta

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` created `REFERENCE_public_surface_architect_chained_dispatch_prompt-at2026-04-13.md` and two explicit packets so `Public Surface Architect` would first build the `Start Here` surface, then commit only if that step left relevant repo-local changes
- the resulting chain committed only the new `Start Here` doc in `c496b83`

## Step-By-Step Evidence Trace

1. The chained dispatch rule was formalized in one reusable reference.
   - prompt evidence: `control/project_agent_ops/resources/references/REFERENCE_public_surface_architect_chained_dispatch_prompt-at2026-04-13.md`
2. The entry packet forbade git commit and restricted work to readable entry packaging.
   - packet evidence: `control/project_agent_ops/resources/task_packets/issued/TASK-PUBLIC-SURFACE-LEAN-02_1-ENTRY.json`
3. The follow-up packet then narrowed git work to one bounded lean public-surface packaging pass.
   - packet evidence: `control/project_agent_ops/resources/task_packets/issued/TASK-LEAN-02_1-GIT-HANDOFF-V2.json`
4. After the `Start Here` document was created, the worktree was inspected again rather than assuming a commit was required.
5. Validation was run before commit:
   - `python3 -m json.tool control/project_domain/resources/manifests/ppt_page_link_matrix_v0_1.json`
   - `python3 -m json.tool control/project_domain/resources/manifests/ppt_regeneration_handoff_bundle_v0_1_at2026_04_13.json`
   - deck and render existence checks for `v2`
6. Only the repo-local `Start Here` document was then committed.
   - commit evidence: `c496b83`
