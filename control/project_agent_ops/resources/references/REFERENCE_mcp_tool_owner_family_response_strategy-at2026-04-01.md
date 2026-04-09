# MCP Tool Owner Family Response Strategy

## Purpose

Respond to the current feedback about weak `MCP/tool inventory owner` coverage without over-fragmenting the skill layer.

This strategy treats the feedback as largely correct:

- the current workspace has several strong MCP-consuming specialist skills
- but it has only one skill that is close to a true MCP/tool owner family
- the canonical inventory and setup sources are broader than the current onboarding-only ownership wording

The goal is to close that ownership gap with the smallest safe change.

## Canonical Sources

- tool inventory:
  - local/private canonical inventory at `control/project_agent_ops/registry/tools/tool_inventory.json`
- MCP setup reference:
  - local/private setup reference at `control/project_agent_ops/resources/tools_inventory/REFERENCE_mcp_setup.md`
- closest current owner skill:
  - [`skills/vendored-mcp-onboarding/SKILL.md`](../../../../skills/vendored-mcp-onboarding/SKILL.md)

## Verified Assessment

### What the feedback gets right

1. `vendored-mcp-onboarding` is the only current skill whose boundary naturally touches:
   - vendoring under `vendor/mcp/`
   - thin launchers under `scripts/mcp/`
   - inventory and registry updates
   - bounded smoke evidence

2. `macos-ocr-evidence`, `component-split-ocr-review`, and `openai-image-caption-validation` are not tool-owner skills.
   They are downstream tool consumers and should remain specialists.

3. The current owner gap is not about "how to use MCPs".
   It is about "who owns ongoing integrity between launcher, registration, inventory, setup docs, and smoke evidence".

### What should not happen in response

- Do not absorb consumer specialist skills into a broad tool-owner family.
- Do not create multiple new MCP owner skills prematurely.
- Do not turn `image-job-dispatcher`, `image-worker`, or pipeline skills into tool inventory owners.

## Strategic Response

### Primary Decision

Use `vendored-mcp-onboarding` as the seed of the `MCP/tool owner family`.

Do not create a brand-new standalone owner skill yet.

Instead:

1. broaden the interpreted charter of `vendored-mcp-onboarding`
2. add missing owner references and checklists under that existing skill
3. keep consumer skills separate
4. postpone any new sibling owner skill until real recurring work proves that onboarding and ongoing maintenance must split

This is the smallest change that addresses the feedback without creating unnecessary skill sprawl.

## Owner Family Model

### Owner layer

`vendored-mcp-onboarding` should be treated as owning the following verbs:

- onboard a new vendored MCP
- verify an already vendored MCP still boots correctly
- ensure `scripts/mcp/`, `.codex/config.toml`, `.vscode/mcp.json`, inventory, and setup references stay aligned
- update activation state based on bounded smoke evidence
- record whether a tool is:
  - registered only
  - launcher-wired
  - boot-verified
  - heavy-smoke-verified
  - active for workspace use

### Consumer layer

These remain consumers, not owners:

- [`skills/macos-ocr-evidence/SKILL.md`](../../../../skills/macos-ocr-evidence/SKILL.md)
- [`skills/component-split-ocr-review/SKILL.md`](../../../../skills/component-split-ocr-review/SKILL.md)
- [`skills/openai-image-caption-validation/SKILL.md`](../../../../skills/openai-image-caption-validation/SKILL.md)

They may depend on MCPs, but they must not become canonical inventory owners.

## Recommended Changes

### Phase 1. Minimal skill hardening

Apply only bounded documentation and checklist strengthening under `skills/vendored-mcp-onboarding/`.

Add:

- `references/owner-boundary.md`
  - explains that this skill owns workspace MCP lifecycle integrity, not only first-time onboarding
- `references/tool-owner-family-map.md`
  - maps owner vs consumer skills
- `references/inventory-setup-sync.md`
  - defines canonical sync targets:
    - `scripts/mcp/`
    - `.codex/config.toml`
    - `.vscode/mcp.json`
    - `tool_inventory.json`
    - `REFERENCE_mcp_setup.md`
    - bounded smoke evidence
- `checklists/mcp_inventory_sync_checklist.md`
  - one-pass checklist for:
    - launcher exists
    - vendor runtime exists
    - config registration exists
    - inventory status updated
    - setup reference updated
    - smoke evidence linked

This phase should not change runtime behavior.

### Phase 2. Inventory integrity helper

If the maintenance burden repeats, add one thin helper under the existing skill or shared scripts:

- suggested future helper:
  - `scripts/check_mcp_inventory_sync.py`

Its job should be limited to auditing drift between:

- `scripts/mcp/`
- vendored MCP roots
- `.codex/config.toml`
- `.vscode/mcp.json`
- `tool_inventory.json`
- `REFERENCE_mcp_setup.md`

This is an audit helper, not a mutating reconciler.

### Phase 3. Only then evaluate a sibling owner skill

Create a sibling skill only if recurring evidence shows a stable split between:

- onboarding a new vendored MCP
- maintaining already onboarded MCP inventory/setup integrity

Candidate future split:

- `vendored-mcp-onboarding`
  - new MCP adoption
- `mcp-inventory-integrity-audit`
  - ongoing workspace MCP status maintenance

Until that evidence exists, one owner skill is preferable.

## Immediate Policy

For current workspace operations:

1. treat `vendored-mcp-onboarding` as the canonical owner-family entrypoint
2. treat `tool_inventory.json` and `REFERENCE_mcp_setup.md` as canonical owner outputs
3. keep MCP-using workflow skills as consumer specialists
4. route ongoing drift findings back into the owner-family references/checklist, not into unrelated pipeline skills

## Success Criteria

This feedback is considered addressed when all of the following are true:

1. a reviewer can identify exactly one current owner-family skill for workspace MCP lifecycle work
2. the distinction between owner and consumer skills is explicit
3. the owner-family skill references the canonical inventory/setup sources directly
4. recurring MCP drift can be handled without inventing a new skill for every MCP consumer

## Non-Goals

- redesigning all MCP-consuming skills
- merging consumer skills into one large MCP meta-skill
- creating a broad "tool owner" umbrella with weak boundaries
- changing pipeline behavior unrelated to MCP lifecycle ownership

## Recommended Next Action

Do one bounded follow-up:

- expand `skills/vendored-mcp-onboarding/` with owner-boundary, family-map, inventory-sync reference, and one checklist

Do not create a new owner skill unless repeated maintenance evidence justifies the split.
