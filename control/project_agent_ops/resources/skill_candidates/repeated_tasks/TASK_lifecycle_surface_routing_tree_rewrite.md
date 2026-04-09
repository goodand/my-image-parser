# Repeated Task: Lifecycle-Surface-First Routing Tree Rewrite

## Pattern Name

Lifecycle-Surface-First Routing Tree Rewrite

## Trigger

- A routing decision tree's root question is tool-type-specific (e.g., `Task involves an MCP?`) but the owner skill's scope has grown to include non-vendored adjacent surfaces or consumer-only paths
- A new surface type was added to the family map but the routing tree still routes using the old gate
- A reviewer reaches the correct branch only after reading the body, not from the tree alone

## Stable Steps

1. Change the routing tree root from a domain-type question to a lifecycle-surface question:
   - Before: `Task involves an MCP?`
   - After: `Task involves a tool lifecycle surface?`
2. Split the first-level branches by ownership class, not by surface type:
   - Branch 1: primary surface is in the canonical owner's primary charter AND the task touches lifecycle surfaces (launcher, config, inventory, setup, smoke) → owner skill (canonical)
   - Branch 2: primary surface is an adjacent non-primary tool or system skill AND the task touches lifecycle surfaces for that surface → owner skill (temporarily routed adjacent)
   - Branch 3: task only uses tool outputs, no lifecycle surface contact → consumer specialist (consumer-only)
3. Add a lifecycle-touch gate to both Branch 1 and Branch 2. The gate condition is identical: "only if the task also touches launcher, config, inventory, setup, or smoke." Missing it from Branch 2 is the most common defect.
4. Add the `Lifecycle Routing Status` enum label in parentheses at each branch terminus so the tree and the family map use the same vocabulary.
5. In Branch 3, list the consumer specialist routing options (OCR, caption, component review, etc.) as sub-branches.

## Candidate Promotion

- Checklist: routing-tree review check that verifies each non-consumer branch has an explicit lifecycle-touch gate
- Template: standard lifecycle-surface-first routing tree skeleton for any new owner-family skill
- Linter rule: detect routing tree branch labels that use domain-type gate language (MCP, filesystem, imagegen) at the root level
