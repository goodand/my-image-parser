# Repeated Task: Bounded Public Surface Packaging After Partial Prior Commits

## Pattern Name

- bounded public surface packaging after partial prior commits

## Trigger

- a reviewable slice already landed across multiple earlier commits
- a follow-up packaging pass must determine what still remains uncommitted
- the next agent must avoid over-staging old or unrelated pending changes

## Stable Steps

1. Reconstruct the already-landed commit history for the bounded slice before touching the worktree.
2. Freeze the bounded artifact set as `candidate files to inspect`, not as a mandatory stage list.
3. Recheck `git status` and `git diff` only against that bounded slice.
4. Commit only the still-uncommitted safe remainder in small topical batches.
5. Stop when the bounded slice reaches clean status instead of creating an empty follow-up commit.
6. Leave unrelated pending tracked files, heavy vendor trees, and risky semantic edits out of the packaging pass.

## Candidate Promotion

- handoff template: bounded artifact packaging after partial prior commits
- checklist: `already committed / still pending / risky / out-of-scope` split before stage
- review rule: do not infer a mandatory stage set from a candidate inspection list

## Promotion Trigger

- another repo slice already has partial commits and a new agent must package only the remaining public surface safely

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` had already landed lean `02_1` portfolio commits such as `7874c72`, `2a7beb6`, and `999e72b`
- the later packaging pass therefore had to inspect remaining lean surfaces first, then commit only the safe remainder such as `2b09aae` for the stale QA report pointer fix
- the handoff rule was tightened so the next agent reports clean status instead of inventing an empty follow-up commit

## Step-By-Step Evidence Trace

1. The bounded slice was first reconstructed from repo history, not from memory.
   - commit evidence: `7874c72`, `2a7beb6`, `999e72b`
   - later handoff evidence: `control/project_agent_ops/resources/task_packets/issued/TASK_PACKET_lean_02_1_system_first_portfolio_public_surface_packaging-at2026-04-13.md`
2. The candidate public-surface set was frozen as an inspection list, not as a mandatory stage list.
   - packet evidence: `Expected Candidate Files To Inspect`
3. The remaining worktree was then compared against that bounded slice.
   - residual lean plan evidence: `control/project_domain/resources/master_plans/drafts/PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md`
4. Safe remainder commits were then taken in narrow batches:
   - bounded review summaries: `2a7beb6`
   - binary review evidence: `999e72b`
   - sanitized session bundle: `3d1e4a1`
   - handoff packet: `1cdbfda`
5. The final lean-specific delta was reduced to one stale pointer correction.
   - pointer-fix commit: `2b09aae`
6. The slice then stopped on clean-status logic for lean-specific pending changes instead of manufacturing another follow-up commit.
