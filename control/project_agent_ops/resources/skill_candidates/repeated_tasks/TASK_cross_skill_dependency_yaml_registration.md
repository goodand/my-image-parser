# Repeated Task: Cross-Skill Dependency YAML Registration After Skill Creation

## Pattern Name

- cross-skill dependency YAML 등록 after new skill creation

## Trigger

- a new skill is created that references or is referenced by other skills
- a skill is promoted from repeated-task KB to shared family skill
- an existing skill gains a new cross-skill dependency (e.g., escalation route, fallback path)

## Stable Steps

1. identify all skills that the new skill references (provider dependencies)
2. identify all skills that reference the new skill (consumer dependencies)
3. create `references/cross_skill_dependencies.yaml` in the new skill
4. for each provider: record contract file, consumed facts, sync timestamp
5. for each consumer: add corresponding entry in the consumer's `cross_skill_dependencies.yaml`
6. verify bidirectional consistency — every `provider` entry in skill A has a matching `consumer` awareness in skill B

## Candidate Promotion

- checklist: `CHECKLIST_cross_skill_dependency_registration.md` — post-creation dependency audit
- script: YAML validator that checks bidirectional consistency across all skill directories

## Promotion Trigger

- another skill is created without cross_skill_dependencies.yaml and the missing link is discovered during review

## Current Proven Evidence

- on 2026-04-08, both `cross-repo-product-review` and `async-migration-verify` were created without `cross_skill_dependencies.yaml`; both reference each other (API-surface change trigger) and both are Band 1 specialists under `verification-decision-gate`; fixed by creating YAML for both with bidirectional entries
- detail file: this file
