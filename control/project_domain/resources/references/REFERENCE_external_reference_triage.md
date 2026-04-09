# External Reference Triage

## Purpose

Record the external workspace references that should remain indexed-only and note which control bucket each one informs.

## Machine-Readable Index

- local/private index at `control/project_agent_ops/registry/external_reference_index.json`

## Classified References

### Team / Resources

- Decision framework template
  Source: `<EXTERNAL_TEMPLATE_ROOT>/decision_framework.md`
  Target bucket: `team/resources/templates`
- Template directory
  Source: `<EXTERNAL_TEMPLATE_ROOT>`
  Target bucket: `team/resources/templates`
- Development playbook good case
  Source: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/codebase-analysis/references/codebase-analysis-development-playbook-at2026-03-23-03-36.md`
  Target bucket: `team/resources/rules`

### Project Domain / Resources

- Knowledge-base good case
  Source: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/agent-tool-benchmark/knowledge_bases/agent-tool-benchmark-kb-at2026-03-24.md`
  Target bucket: `project_domain/resources/knowledge_bases`
- Spec good case
  Source: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/codebase-analysis/references/codebase-analysis-spec-at2026-03-23-03-14.md`
  Target bucket: `project_domain/resources/specs/prose`

### Project Agent Ops / Resources

- Codebase-analysis directory reference
  Source: `<EXTERNAL_SKILLS_ROOT>/Skills-Create-Project/codebase-analysis`
  Target bucket: `project_agent_ops/resources/codebase_graph`

## Boundary

- These references stay outside the active workspace tree.
- `control/` keeps only the index and the classification note.
- If one of these references is later promoted into an internal artifact, create a new local file under the target bucket instead of editing the external source in place.
