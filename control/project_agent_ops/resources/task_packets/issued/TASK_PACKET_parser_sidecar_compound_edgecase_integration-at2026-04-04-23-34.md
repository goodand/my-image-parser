# Task Packet: Parser Sidecar Compound Edge-Case Integration

## Goal

Extend `parser-sidecar-to-canonical-schema-promotion` so the skill explicitly documents the bounded compound-dashboard edge-case route now used for `image4`-style failures.

## Why This Fits

The skill already owns:

- alternate parser closure routes
- normalized parser truth as downstream source of truth
- single-source fallback when one helper backend fails

The repeated edge-case patterns now worth absorbing are:

- projection-profile component decomposition probe for compound dashboards
- objective-profile scoring for regrouped component candidates
- table-seed dependency blocks compound dashboard reentry

## Scope

Document the bounded decomposition-first route as a parser-sidecar troubleshooting and reference surface, not as a broad new automation promise.

## Owned Write Surfaces

- `skills/parser-sidecar-to-canonical-schema-promotion/SKILL.md`
- `skills/parser-sidecar-to-canonical-schema-promotion/references/alternate_closure_routes.md`
- `skills/parser-sidecar-to-canonical-schema-promotion/references/troubleshooting.md`
- `skills/parser-sidecar-to-canonical-schema-promotion/references/runtime.md`
- optional new reference under `skills/parser-sidecar-to-canonical-schema-promotion/references/`
- optional KB patch under `skills/parser-sidecar-to-canonical-schema-promotion/knowledge_bases/`

## Required Inputs

- [KB_repeated_task_patterns.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/skill_candidates/repeated_tasks/KB_repeated_task_patterns.md)
- [KB_repeated_issue_patterns.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/skill_candidates/repeated_issues/KB_repeated_issue_patterns.md)
- [REPORT_phase1_image4_four_mode_reentry_waiver-at2026-03-30-21-27.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REPORT_phase1_image4_four_mode_reentry_waiver-at2026-03-30-21-27.md)

## Expected Changes

1. skill body acknowledges compound-dashboard decomposition as a bounded fallback when no stable table seed exists
2. alternate-closure reference distinguishes:
   - normal table-seeded promotion
   - decomposition-first edge-case path
3. troubleshooting explains when to stop retrying table-seeded recrop and switch to decomposition/objective-profile analysis
4. if needed, add one dedicated reference for decomposition-first parser edge cases

## Non-Goals

- do not promise unattended recovery for all compound dashboards
- do not add new parser runtime code unless documentation cannot otherwise reflect the route
- do not change aggregate experiment truth

## Done Definition

- the skill documents the current compound-dashboard fallback route clearly enough that a future bounded session can start from the skill without re-deriving the strategy
- the ownership boundary stays clear: bounded parser-sidecar evidence only, not full semantic image judging

## Verification

1. re-read the updated skill and references
2. confirm the skill still prefers canonical parser outputs over raw sidecars
3. confirm the new edge-case route remains bounded and exception-oriented
