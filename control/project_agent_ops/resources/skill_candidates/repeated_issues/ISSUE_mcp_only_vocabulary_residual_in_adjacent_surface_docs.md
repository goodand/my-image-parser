# Repeated Issue: MCP-Only Vocabulary Residual In Adjacent-Surface Documents

## Issue Name

MCP-Only Vocabulary Residual In Adjacent-Surface Documents

## Symptom

After an owner skill's charter is broadened to include non-vendored adjacent surfaces, MCP-specific vocabulary persists in:
- table headers (`Primary MCP Surface` instead of `Primary Lifecycle Surface`)
- Consumer Layer intro sentences (`These skills use MCPs` when some rows have `—` for their primary surface)
- pre-routing check phrasing (`The task involves a MCP that lives under vendor/mcp/` as the only gate)
- individual `What It Does Not Own` cells (`MCP lifecycle` for a row whose primary surface is not an MCP)

Each review pass finds a new residual site even after previous sites were corrected.

## Scope

- Owner skill family map (`references/tool-owner-family-map.md`)
- Consumer Layer table headers and intro sentences
- Quick pre-routing check phrasing
- Individual consumer table cells where the `What It Does Not Own` column mirrors the wrong noun

## Guardrail

Before finalizing any owner-family document update:
1. Grep the family map for `MCP` and review every occurrence — check whether the row or section it appears in actually requires MCP-specific language or should use a broader noun (`tool`, `lifecycle surface`)
2. Check the Consumer Layer table header: if any row has `—` for its primary surface, the header must not say `Primary MCP Surface`
3. Check the intro sentence of the Consumer Layer: replace `These skills use MCPs` with `These skills consume MCPs or adjacent tool surfaces` if any row has a non-MCP primary surface
4. Check individual `What It Does Not Own` cells for `MCP lifecycle` — if the row's primary surface is `—`, the cell should say `tool lifecycle` instead

## Follow-up

- Add a vocabulary audit step to the family-map drift prevention checklist
- The drift prevention check should include: "Does the table header, intro sentence, and each individual cell use the broadest correct noun for its actual scope?"
- Related task: `TASK_owner_family_routing_enum_hardening.md`
