# Filename And Linting Rules

## Purpose

Git-managed control tree 안에서 파일명 규칙과 lint/static 진단 순서를 고정해, agent가 자율적으로 움직이더라도 결과 형식과 안전 경계는 흔들리지 않게 한다.

## Source Of Truth

- Primary references:
  - [script-and-linter-writing-patterns-at2026-03-20-14-15.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/claude-gemini-communicator/skills/Skills-Create-Project/skill-creation-process/references/script-and-linter-writing-patterns-at2026-03-20-14-15.md)
  - [python-static-diagnostic-fixer-knowledge_base-at2026-03-17-01-18.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/claude-gemini-communicator/skills/Skills-Create-Project/python-static-diagnostic-fixer/knowledge_bases/python-static-diagnostic-fixer-knowledge_base-at2026-03-17-01-18.md)
  - [consistency-checklist-at2026-03-17-01-18.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/claude-gemini-communicator/skills/Skills-Create-Project/python-static-diagnostic-fixer/checklist-forconsistency-evaluation/consistency-checklist-at2026-03-17-01-18.md)
- Supporting reference for broader team operating policy:
  - [RULES_development_team_operating_playbook.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/rules/RULES_development_team_operating_playbook.md)
- Project-specific extension:
  - [RULES_legacy_boundary_linting.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/rules/RULES_legacy_boundary_linting.md)

## Scope

This document governs:

1. Git-managed file naming under `control/`
2. lint/static diagnostic ordering
3. safe vs unsafe static fixes
4. hard-fail vs warning classification

This document does not define domain-specific import boundaries. Those stay in profile-specific rule docs such as legacy boundary rules.
This document also does not replace the broader development playbook for workflow, TDD, smoke execution, task packet handling, or workspace/environment policy.

## Rule Ordering

1. Runtime gate first.
2. Static/linter diagnostics second.
3. Safe static fixes before unsafe static fixes.
4. Validation before mutation.
5. Evidence before completion.

## Naming Rules

### General

- Git-managed names must use ASCII only.
- No spaces in Git-managed names.
- No parentheses in Git-managed names.
- No mixed-case variants for the same artifact family.

### Canonical Prose Documents

- Canonical documents do not carry dates in filenames.
- Canonical prefixes must be stable and uppercase.
- For one domain pipeline, only one active `MASTER_PLAN_*.md` may exist.
- New strategy, branch, or extension material must be appended to the active master plan or stored as a dated draft, not as a second master plan.

Allowed families:

- `MASTER_PLAN_*.md`
- `SPEC_*.md`
- `RULES_*.md`
- `CHECKLIST_*.md`
- `REFERENCE_*.md`
- `KB_*.md`

Examples:

- `MASTER_PLAN_presentation_image_pipeline.md`
- `RULES_filename_and_linting.md`
- `SPEC_presentation_image_pipeline.md`

### Decision Records

- ADR files use ordered numbering.
- Pattern:

```text
ADR_0001_short_slug.md
```

### Dated Operational Documents

- Reports, audits, smoketests, and time-stamped answer records may carry dates.
- Draft plan files must carry minute-level timestamps.
- Preferred pattern:

```text
<PREFIX>_<subject>-atYYYY-MM-DD.md
```

- If minute-level separation is required:

```text
<PREFIX>_<subject>-atYYYY-MM-DD-HH-MM.md
```

Examples:

- `REPORT_openai_image_caption_validation-at2026-03-27.md`
- `SMOKETEST_pptx_slide_screenshot_capture-at2026-03-27.md`
- `PLAN_image_obsidian_style_parsing-at2026-03-27-15-27.md`

### Machine-Readable Files

- Machine-readable filenames must be lowercase.
- Use `snake_case`.
- Keep suffixes explicit.

Examples:

- `tool_inventory.json`
- `image_registry.schema.json`
- `cross_validation_manifest.json`
- `caption_review.contract.json`

### Skill Directories

- Skill directory names use `kebab-case`.
- Inside a skill directory, fixed names stay fixed:
  - `SKILL.md`
  - `agents/openai.yaml`

## Naming Lint Classes

### Hard Fail

- non-ASCII filename in Git-managed tree
- space in Git-managed filename
- parentheses in Git-managed filename
- canonical document carrying a date suffix
- machine-readable file not using lowercase snake_case
- duplicate canonical document for the same role
- more than one active `MASTER_PLAN_*.md` for the same domain

### Soft Warn

- document title and filename drift
- dated artifact stored in canonical-doc location
- legacy naming retained outside `legacy/`
- stale file under `archive/pending_delete/`
- decision-support overlay stored under `project_domain/resources/master_plans/` instead of `user_decisions/resources/notes/`

## Lint And Static Diagnostic Policy

### Runtime First

Static/linter cleanup never becomes the first gate.

Required runtime gate before static work:

1. `py_compile` or language-equivalent compile check
2. existing tests relevant to the touched surface
3. minimum smoke when the change touches execution flow

### Safe Static Fixes

Safe fixes include:

- unused import cleanup
- unused variable cleanup
- typing support additions
- `from __future__ import annotations`
- optional guard additions
- filename normalization without behavior change
- document filename normalization without content meaning change

### Unsafe Static Fixes

Unsafe fixes include:

- import graph rewrites disguised as lint cleanup
- moving runtime logic across directories
- deleting meaningful branching to silence warnings
- introducing no-op code only to satisfy a checker
- renaming files when references or contracts are not updated together

Unsafe fixes require explicit review.

## Validation Before Mutation

- Validate file tree rule first.
- Validate syntax second.
- Apply mutation only after validation passes.
- Re-run validation after mutation.

Lint or formatting tools must not silently mutate files before the contract is checked.

## Evidence Requirements

Every lint-related change should leave enough evidence to answer:

1. what rule fired
2. whether the issue was runtime or static
3. whether the fix was safe or unsafe
4. what validation was rerun after the fix

## Recommended Lint Surface

### Hard Gate

- filename invariants
- JSON syntax
- YAML syntax
- schema syntax
- machine-readable contract presence where required

### Secondary Gate

- Markdown structure
- heading ordering
- title/filename consistency
- stale pending-delete candidates

## Project-Specific Profiles

This document is the umbrella rule.

Project-specific policy layers may extend it for:

- legacy boundary import control
- directory ownership control
- generator-only file creation
- allowlist-based file creation

Current active profile:

- [RULES_legacy_boundary_linting.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/rules/RULES_legacy_boundary_linting.md)

## Companion Contract

Machine-readable companion:

- [filename_and_linting.contract.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/contracts/filename_and_linting.contract.json)

Automated checker:

- [lint_control_tree.py](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/team/resources/scripts/lint_control_tree.py)

## One-Line Summary

Filename rules stabilize the control tree, and lint rules follow runtime-first, safe-fix-first, evidence-backed enforcement.
