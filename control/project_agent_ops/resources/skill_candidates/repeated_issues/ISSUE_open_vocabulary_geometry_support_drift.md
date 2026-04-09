# Repeated Issue: Open-Vocabulary Geometry Support Drift

## Purpose

Capture the recurring risk that a model-backed open-vocabulary `find` surface appears usable for object retrieval, but does not reliably support geometry return in the same workspace/runtime.

## Recurrence Signal

This issue appears when:

- text-prompted object finding succeeds or at least runs inference
- the same tool path fails or degrades when `return_geometry=true` is requested
- the workflow still needs geometry for crop, fill, or cutout steps

## Current Workaround

- treat text-prompted `find` as a bbox-oriented selector unless geometry support is explicitly re-verified
- use `detect` when a segmentation mask or polygon is required
- if bbox-only fallback is still insufficient, hand off to a bounded imagegen repair request instead of forcing the same geometry path

## Structural Fix Candidate

- keep a workspace-specific capability note for each model-backed MCP tool, not just the upstream README contract
- add a smoke that separately verifies:
  - text match success
  - bbox return
  - geometry return

## Escalation Trigger

- another model-backed open-vocabulary tool claims geometry support, but the same feature fails or regresses in workspace smoke

## Related Evidence

- `control/project_agent_ops/resources/smoke/SMOKETEST_object_isolation_correction_worker-at2026-03-27-23-26.md`
- `control/project_agent_ops/resources/skill_candidates/repeated_issues/KB_repeated_issue_patterns.md`
