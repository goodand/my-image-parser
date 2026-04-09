# Legacy Boundary Linting Rules

## Purpose

Legacy 경계를 "읽게 해서 지키는" 방식이 아니라 "잘못 만들 수 없게 하는" 방식으로 강제한다.

Parent umbrella rule:

- [RULES_filename_and_linting.md](./RULES_filename_and_linting.md)

## Source Of Truth

- Primary:
  - [Legacy_Boundary_Decision_Answers-at2026-03-27.md](../../../user_decisions/resources/closed_questions/Legacy_Boundary_Decision_Answers-at2026-03-27.md)
- Supporting:
  - [Legacy_Boundary_Decision_Checklist.md](../../../user_decisions/resources/closed_questions/Legacy_Boundary_Decision_Checklist.md)
  - [legacy_boundary_decision_map.svg](../../../user_decisions/resources/assets/legacy_boundary_decision_map.svg)

## Rule Ordering

1. Runtime gate first.
2. Static and lint gate second.
3. Safe static fixes may be autofixed.
4. Unsafe fixes require explicit review.
5. Behavior change is out of scope for lint-only work.

## Hard Rules

### Shim Re-export Only

- Legacy shim file must remain bridge-only.
- Allowed shape: re-export only.
- New business logic inside shim is forbidden.
- Violation severity: `error`

### Generator-Only New Module Creation

- New module creation must go through `npm run new:module`.
- Direct empty-file creation is forbidden for governed directories.
- Generator must block creation before file write when duplicate-like names are detected.
- Violation severity: `error`

### Directory Boundary Hard Block

- `services -> components` import is hard-blocked.
- Directory boundary rules are not warnings when they define architectural direction.
- Violation severity: `error`

### Machine-Readable Directory Contract Required

- Governed directories must expose machine-readable boundary rules.
- Accepted forms:
  - `CONTRACT.json`
  - `ALLOWED.md`
- Missing contract file is a lint failure when the directory is under governance.
- Violation severity: `error`

## Warning Rules With Required Annotation

### Legacy Import Exception

- If a legacy import is temporarily allowed, the import must have a justification comment immediately above it.
- Required marker:

```js
// LEGACY-IMPORT: <reason>
```

- Missing marker on an allowed legacy-path import is a lint failure.

### Migration-Period Warning Edges

- `legacy -> services`: `warn` plus required `LEGACY-IMPORT:` comment
- `components -> legacy`: `warn` plus required `LEGACY-IMPORT:` comment

Warnings here are migration allowances, not silent acceptance.

## Generator Pre-Create Checks

Before a new file is created, the generator must check:

1. Similar file name collision
2. Similar export name collision
3. Legacy shim presence
4. Target directory ownership fit
5. Directory contract availability

If any hard rule fails, generation must stop before file creation.

## Allowlist And Removal Policy

- New-file allowlist is allowed and should be refreshed periodically.
- Allowlist refresh may be LLM-assisted.
- Legacy removal criteria must be explicit:
  - zero references
  - replacement path stabilized
  - quiet period without warnings

## Safe Fix Boundary

Lint-only work may do the following without escalation:

- add missing `LEGACY-IMPORT:` comment when the reason is already explicitly documented nearby
- replace shim body with pure re-export form when behavior is unchanged
- add missing directory contract file path reference

Lint-only work must not do the following automatically:

- move runtime logic across layers
- rewrite architectural ownership
- create a new public entrypoint
- remove legacy code without satisfying removal criteria

## Evidence Required

Every lint rule change or lint-driven fix should leave evidence for:

1. rule that fired
2. file or import edge involved
3. whether the fix was safe or unsafe
4. whether runtime gate had already passed

## Companion Contract

Machine-readable companion:

- [legacy_boundary_lint.contract.json](../../../project_domain/resources/specs/contracts/legacy_boundary_lint.contract.json)
