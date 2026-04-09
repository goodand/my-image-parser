# Repeated Issue: Unconditional Checklist Item N/A Fatigue

## Issue Name

Unconditional Checklist Item N/A Fatigue

## Symptom

A checklist item that applies only to a minority of runs — typically one with an implicit `if this surface has...` or `if dependencies include...` condition — is added to a generic checklist without an explicit skip condition.

In most runs the item is always N/A, so operators start marking it without reading its body. The condition it was meant to catch is no longer being evaluated. The checklist item becomes invisible noise.

## Scope

- Any operational checklist with items that have conditional applicability
- Specifically: items that check for presence of system skills, optional dependencies, or surface types that are not present in every run
- Example: a system-skill coverage check in a vendored-MCP sync checklist that applies only when the MCP's adjacent workflow includes a system skill dependency

## Guardrail

When adding a conditional checklist item:
1. Lead the item with an explicit skip guard as the first token: `*(skip if X)* ` or `*(N/A unless X)*`
2. The skip condition must be evaluable before the item body is read, not embedded at the end of the body
3. The skip condition should reference a checkable state from an earlier section (e.g., "Supporting Tool Surface contains no system skills" — checkable from the inventory record)

Example of correct form:
```
- [ ] *(skip if Supporting Tool Surface contains no system skills)* System skill coverage check: ...
```

## Follow-up

- Audit the full checklist for items that lack explicit skip guards but have embedded conditional prose — convert them to the `*(skip if)*` pattern
- When writing new checklist items, ask: "Will this be N/A on more than half of runs?" If yes, add a skip guard before merging
- Related issue: `ISSUE_system_skill_registry_drift.md` — the system-skill coverage check that triggered this pattern was a direct follow-up to the system skill registry drift issue
