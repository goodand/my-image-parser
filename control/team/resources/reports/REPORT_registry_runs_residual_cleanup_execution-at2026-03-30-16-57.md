# Report Registry Runs Residual Cleanup Execution

## Date

2026-03-30 16:57 Asia/Seoul

## Scope

Remove the residual internal namespace:

- `control/project_agent_ops/registry/runs/`

and replace it with explicit canonical registry targets:

- `control/project_agent_ops/registry/runtime/session_paths.json`
- `control/project_agent_ops/registry/jobs/image_caption_jobs/`

## Reason

After the control-tree migration, `runs` was no longer a primary action unit.

The remaining `registry/runs/` subtree mixed two different registry roles:

- runtime path synchronization
- image-caption job registry bodies

That naming drift was no longer needed.

## Actions Taken

1. moved:
   - `control/project_agent_ops/registry/runs/session_paths.json`
   - to `control/project_agent_ops/registry/runtime/session_paths.json`
2. moved:
   - `control/project_agent_ops/registry/runs/image_caption_jobs/`
   - to `control/project_agent_ops/registry/jobs/image_caption_jobs/`
3. removed the empty residual directory:
   - `control/project_agent_ops/registry/runs/`
4. patched active references across:
   - `control/`
   - `scripts/`
   - `skills/`
5. updated structure rules to mark the new paths as canonical

## Result

- `registry/runtime/` is now the canonical registry home for runtime path synchronization
- `registry/jobs/` is now the canonical registry home for image-caption job ledgers
- `registry/runs/` is no longer canonical

## Verification

- `control/project_agent_ops/registry/runs/` removed
- `control/project_agent_ops/registry/runtime/session_paths.json` exists
- `control/project_agent_ops/registry/jobs/image_caption_jobs/` exists
- active references under `control/`, `scripts/`, and `skills/` were rewritten to the new canonical paths

## Follow-Up

- keep migration/history documents that intentionally mention the old `registry/runs/` path as historical evidence
- do not reintroduce `registry/runs/` as a generic namespace
