# Image Caption Pipeline Data Flow Plan

## Status

Draft

## Purpose

This plan defines an MCP-first image caption pipeline where each image is processed as an isolated unit.
The operating rule is simple: Skills orchestrate subagents, MCPs hold state and data, and completion is recognized only from MCP-backed records.

## Core Principles

- One image equals one job equals one subagent.
- The parent orchestrator passes only stable identifiers such as `job_id` and `image_id`.
- Registry and execution state are the source of truth.
- Free-form subagent output is advisory and never sufficient for completion.
- Rename and metadata mutation happen only after caption data is safely stored.

## System Roles

### Orchestrator Skill

Responsible for:

- collecting input images
- issuing stable identifiers
- creating jobs and subtasks
- dispatching workers
- enforcing retry policy
- aggregating results
- controlling the commit gate

### Execution Management MCP

Recommended: `agent-task-manager-mcp`

Owns:

- task and subtask records
- state transitions
- attempts and retries
- locks
- sessions
- checkpoints
- evidence references

### Image Registry MCP

Recommended: `ConPort`

Owns:

- image path records
- caption records
- rename candidates
- metadata status
- last error fields
- progress logs

### Worker MCPs

Own the actual side effects:

- caption generation MCP
- metadata write MCP
- filesystem MCP

## Data Models

### Image Registry Record

```json
{
  "image_id": "img_000123",
  "source_path": "/images/a.jpg",
  "current_path": "/images/a.jpg",
  "caption": null,
  "caption_status": "pending",
  "metadata_status": "pending",
  "rename_status": "pending",
  "rename_candidate": null,
  "last_error": null,
  "updated_at": "2026-03-26T12:00:00+09:00"
}
```

### Execution Record

```json
{
  "job_id": "job_20260326_001",
  "image_id": "img_000123",
  "phase": "caption",
  "state": "queued",
  "attempt": 0,
  "worker_agent": "image-caption-worker",
  "evidence": [],
  "started_at": null,
  "finished_at": null
}
```

### Worker Result Payload

```json
{
  "job_id": "job_20260326_001",
  "image_id": "img_000123",
  "caption": "a brown dog running on grass",
  "rename_candidate": "a-brown-dog-running-on-grass.jpg",
  "metadata_write_requested": false,
  "success": true,
  "error": null
}
```

## Execution Flow

### Phase 0. Environment Preparation

1. Register the required MCPs.
   - execution management MCP
   - image registry MCP
   - caption MCP
   - metadata MCP
   - filesystem MCP
2. Register the orchestration skill and the `image-caption-worker` subagent.

### Phase 1. Input Registration

1. Collect input image paths.
2. Assign one stable `image_id` per image.
3. Create initial registry records.
4. Create queued execution records for the caption phase.

At this point, the parent stops relying on local memory and starts using MCP state as the working index.

### Phase 2. Dispatch Preparation

1. Query queued jobs from the execution MCP.
2. Acquire a lock for the selected job.
3. Transition the job from `queued` to `running`.
4. Stamp `started_at` and increment `attempt`.

### Phase 3. Worker Caption Phase

1. Launch `image-caption-worker` with only `job_id` and `image_id`.
2. The worker queries the registry to resolve `current_path` and prior state.
3. The worker calls the caption MCP.
4. The worker derives a slugified `rename_candidate`.
5. The worker updates the registry first.
6. The worker updates the execution record second with evidence.

The required invariant is: registry write first, execution completion second.

### Phase 4. Parent Verification

1. Receive the worker response.
2. Re-read the registry.
3. Re-read the execution record.
4. Mark the job complete only if both systems agree.

Minimum completion checks:

- `caption` exists
- `caption_status = completed`
- `rename_candidate` exists
- `state = completed`
- `finished_at` exists
- `evidence` is non-empty

If these checks fail, mark the job failed and enqueue it for retry.

### Phase 5. Post-Caption Branches

#### Branch A. Caption Storage Only

Default safe mode.

- caption saved
- original file retained
- metadata unchanged
- rename unchanged

#### Branch B. Metadata Write

Optional follow-up phase.

- call metadata MCP
- update `metadata_status`
- persist failure details on error

#### Branch C. Filename Rename

Optional final mutation phase.

1. check collisions
2. apply rename
3. update `current_path`
4. set `rename_status = completed`

### Phase 6. Commit Gate

Only pass into mutation or finalization when:

- `caption_status = completed`
- `metadata_status` is safe for the selected mode
- `rename_status` is safe for the selected mode

Recommended initial operating mode: manual approval.

- automatic mode is possible but riskier
- manual mode keeps caption review, metadata write, and rename under explicit approval

### Phase 7. Aggregation and Reporting

Aggregate only from MCP state.

Required outputs:

- total image count
- caption completed count
- metadata completed count
- rename completed count
- failed count
- failed item list
- retry queue

## Operating Rules

1. Keep worker inputs minimal.
2. Treat MCP records as authoritative.
3. Defer file mutation until after caption persistence.
4. Keep path and caption state in a single authoritative registry.
5. Keep attempts, transitions, and evidence in the execution MCP.

## Recommended Initial Rollout

Start with the narrowest safe slice.

1. caption generation only
2. parent-side MCP verification
3. manual review queue
4. metadata write as optional phase
5. rename as last approved phase

This reduces rollback risk and makes failure localization simpler.

## Architecture Summary

### Skills

- parent orchestration skill
- `image-caption-worker` subagent skill

### MCPs

- execution management: `agent-task-manager-mcp`
- image registry: `ConPort`
- side-effect tools: caption MCP, metadata MCP, filesystem MCP

## One-Line Conclusion

Skills run subagents, but MCP state decides truth.

## References

- Customization: https://developers.openai.com/codex/concepts/customization/
- MCP: https://developers.openai.com/codex/mcp/
- Skills: https://developers.openai.com/codex/skills/
- agent-task-manager-mcp: https://github.com/mlnima/agent-task-manager-mcp
- ConPort: https://github.com/GreatScottyMac/context-portal
