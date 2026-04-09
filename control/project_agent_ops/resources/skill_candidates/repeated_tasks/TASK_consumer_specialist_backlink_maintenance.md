# Repeated Task: Consumer Specialist Backlink Maintenance

## Pattern Name

Consumer Specialist Backlink Maintenance

## Trigger

- An owner-family skill's charter is updated, narrowed, or expanded, and adjacent consumer specialists must be updated to reflect the new routing contract
- A reviewer reports that they could not find the owner skill starting from a consumer specialist SKILL.md
- More than two consumer specialists share the same owner skill and their routing sections have drifted out of sync

## Stable Steps

1. Identify all consumer specialist skills whose primary lifecycle surface is managed by the owner skill (use `references/tool-owner-family-map.md` as the source).
2. For each consumer skill, locate the `Do Not Use This Skill When` section and add or update a single short routing line:
   - Pattern: `the underlying tool lifecycle is broken — route to <owner-skill-name>`
   - Keep it as the last bullet in that section.
3. For each consumer skill, locate the `Not Owned Here` section and ensure the routing entry is a noun phrase only:
   - Pattern: `tool lifecycle integrity (launcher, registration, inventory, setup state)`
   - Remove any full routing sentence with `if` clauses from this section; those belong in step 2.
4. Verify that the two sections are not duplicating a full routing sentence. The split is: `Do Not Use This Skill When` = verb phrase with routing target, `Not Owned Here` = noun phrase only.
5. Apply the same pattern to all consumer specialists in one pass to avoid partial alignment.

## Candidate Promotion

- Checklist: per-consumer-skill audit checklist that verifies the two-section pattern
- Skill: thin wrapper that lists the owner skill, finds all consumer specialists in the family map, and validates that both sections are consistent with the current routing contract
- Packet template: standard consumer-specialist update packet for owner-family re-scoping events
