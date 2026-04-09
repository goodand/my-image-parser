# Report Registry Skills Namespace Cleanup

## Date

2026-03-30 16:53 Asia/Seoul

## Scope

Remove the empty residual directory:

- `control/project_agent_ops/registry/skills/`

## Reason

The current workspace model places:

- skill package bodies at root `skills/`
- skill inventory and skill-path synchronization in registry bodies such as:
  - `control/project_agent_ops/registry/tools/tool_inventory.json`
  - `control/project_agent_ops/registry/runs/session_paths.json`

There were no active references to `control/project_agent_ops/registry/skills/`, and the directory contained no files.

Therefore it did not serve a distinct registry role.

## Evidence

- `rg -n "registry/skills|control/project_agent_ops/registry/skills" control scripts skills` returned no matches
- `ls -la control/project_agent_ops/registry/skills` showed an empty directory

## Result

- `control/project_agent_ops/registry/skills/` removed
- workspace structure rule updated to state that a separate `registry/skills/` namespace is not canonical unless a real registry body is introduced later

## Follow-Up

- keep skill package bodies at root `skills/`
- keep skill inventory in `registry/tools/tool_inventory.json`
- keep workspace path synchronization in `registry/runtime/session_paths.json`
