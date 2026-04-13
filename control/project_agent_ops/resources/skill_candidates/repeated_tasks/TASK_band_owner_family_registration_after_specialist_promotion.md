# Repeated Task: Band Owner Family Registration After Specialist Skill Promotion

## Pattern Name

- Band owner family registration after specialist skill promotion

## Trigger

- a new skill is promoted and assigned to a Band as a direct-call specialist
- an existing specialist changes Band ownership

## Stable Steps

1. identify the target Band and its owner skill (e.g., Band 1 → `verification-decision-gate`)
2. add the new specialist to the owner's `SKILL.md` → `Family Roles` → `direct-call specialists` list
3. **critical**: update the owner's YAML `description` frontmatter with a routing clause for the new specialist — the YAML description is the primary routing surface for agent skill selection
4. update `owner-task-bands-at*.md` → target Band → `direct-call specialists` list
5. add `direct-call specialist notes` with Band adjacency if applicable (e.g., "primary Band 1, secondary adjacency Band 3/Band 2")
6. verify the owner's `Do not use` section still correctly excludes the new specialist's narrow concern

## Candidate Promotion

- checklist: `CHECKLIST_band_owner_family_registration.md` — 6-step registration after specialist promotion
- linter: scan all Band owner YAML descriptions for specialist names not listed in Family Roles

## Promotion Trigger

- another specialist is promoted to a Band but the owner SKILL.md description or owner-task-bands document is not updated, causing routing failure

## Current Proven Evidence

- on 2026-04-08, `cross-repo-product-review` and `async-migration-verify` were promoted as Band 1 specialists but initially missing from:
  - `verification-decision-gate/SKILL.md` description and Family Roles
  - `owner-task-bands-at2026-04-02.md` Band 1 direct-call specialists list
  - fixed by updating all three locations with routing clauses and specialist notes
- detail file: this file
