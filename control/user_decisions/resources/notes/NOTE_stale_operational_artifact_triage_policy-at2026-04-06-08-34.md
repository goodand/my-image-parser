# Stale Operational Artifact Triage Policy

## Purpose

Freeze the current operating rule for stale `handoff md` and `issued task packets`.

The goal is **not** early cleanup.
The goal is to:

1. detect stale operational artifacts quickly
2. attempt LLM continuation first
3. preserve in-flight work that was interrupted by network or session instability
4. clean up only after resume value is ruled out

## Scope

This policy applies to:

- `control/project_agent_ops/resources/handoffs/*.md`
- `control/project_agent_ops/resources/task_packets/issued/*.json`

This policy does **not** define cleanup rules for:

- canonical references
- KB documents
- master plans
- evidence-backed reports

## Core Interpretation

Most unit tasks should finish within one hour.

If a handoff or issued task packet remains stale beyond that point, the more likely cause is:

- internet / session / agent interruption

and **not** a long intended execution horizon.

Preparation-heavy work is usually expected to happen earlier in a master-plan unit, so a stale operational artifact is treated first as a likely interrupted lane, not as a long-running normal state.

## Primary Rule

If a tracked operational artifact still exists and has not been updated for **1 hour**, run LLM triage immediately.

There is no multi-hour backoff ladder such as `3h / 12h / 24h`.

The single stale threshold is:

- `1 hour`

## Triage Order

The triage sequence is fixed.

1. detect stale artifact
2. inspect code state and linked artifacts
3. ask whether the artifact is resumable
4. ask whether the artifact was intentionally held
5. ask whether it drifted away from the intended plan
6. ask whether the work is already completed and promoted upward
7. only then ask whether cleanup is safe

## Resume-First Rule

Artifacts that look ambiguous or incomplete should not be treated as cleanup candidates first.

If a stale artifact appears to be less than roughly complete, the default interpretation is:

- `resume_candidate`

This means the system should first:

- push the current file back into an LLM continuation loop
- re-inject relevant context
- ask what is missing
- ask whether the lane should resume, hold, or close

## Classification

### `active`

- recently updated
- or currently still moving
- or clearly not stale

### `resume_candidate`

- stale beyond 1 hour
- code or artifacts exist
- progress looks partial
- missing validation, missing summary, or interrupted finish is plausible

### `intentional_hold`

- stale beyond 1 hour
- but the artifact was deliberately paused
- not safe to delete

### `drifted_abandon_candidate`

- stale beyond 1 hour
- no convincing continuation value
- appears to have drifted away from the intended plan

### `completed_cleanup_candidate`

- stale beyond 1 hour
- work appears finished
- core result has already been promoted into higher-level artifacts
- operational file is now mostly residue

### `user_review_candidate`

- stale beyond 1 hour
- neither safe resume nor safe cleanup is obvious
- user should decide

## LLM Triage Questions

Use these questions in order.

1. Is there any missing completion condition, validation, or evidence for this artifact?
2. Was this artifact intentionally put on hold?
3. Did this work drift away from the intended plan?
4. Has the work already been completed and promoted into higher-level artifacts?
5. What is the next action: `resume`, `keep`, `archive`, or `delete`?

## Warning-Only Rule

Hooks or lint-style checks should only emit warnings.

They must **not**:

- auto-delete stale handoffs
- auto-delete stale issued packets
- auto-archive stale operational artifacts

Their role is:

- stale detection
- recommended action hinting
- escalation into LLM triage

## Warning Messages

### Resume

- `OPS-RESUME: stale operational artifact older than 1h; code-state recovery and context reinjection recommended before cleanup.`

### Intentional Hold

- `OPS-HOLD: stale operational artifact older than 1h appears intentionally paused; keep unless plan ownership changes.`

### Drift

- `OPS-DRIFT: stale operational artifact older than 1h may have drifted from the intended plan; review before keeping.`

### Completed Cleanup

- `OPS-CLEANUP: stale operational artifact older than 1h appears completed and already promoted; archive or delete may be safe.`

### User Review

- `OPS-REVIEW: stale operational artifact older than 1h remains ambiguous; user review is recommended before cleanup.`

## Suggested LLM Output Shape

```json
{
  "path": "control/project_agent_ops/resources/task_packets/issued/TASK-RENDER-0001.json",
  "status": "resume_candidate",
  "missing_items": [
    "validation result not recorded",
    "owned output files not materialized"
  ],
  "intentional_hold": false,
  "drifted": false,
  "completed_and_promoted": false,
  "safe_to_archive": false,
  "safe_to_delete": false,
  "next_action": "resume",
  "reason": "packet is stale but continuation value remains high"
}
```

## Cleanup Rule

Cleanup is the final step, not the first step.

Cleanup becomes eligible only after triage determines:

- `completed_cleanup_candidate`
- or `drifted_abandon_candidate`

Even then:

- `archive`
- `delete`

should remain explicit actions, not hidden hook side effects.

## Operating Conclusion

The governing rule is:

- `stale -> inspect code state -> LLM triage -> resume/hold/drift/completed classification -> cleanup only at the end`

The most important invariant is:

- **resume-first, cleanup-last**

## Design Intent

This policy exists because most operational artifacts in the current workspace are expected to finish within `1 hour`.

Therefore, a stale `handoff md` or `issued task packet` should not be read first as:

- a long normal execution
- an automatic cleanup target

It should be read first as:

- an interrupted execution
- a context-loss candidate
- a code-state recovery candidate

The most common real-world stale cause is:

- network interruption
- model/API interruption
- agent session drop

This means the design must prefer:

- recovery
- context reinjection
- explicit user judgment for ambiguous cases

over:

- hidden cleanup
- aggressive archive/delete automation

## Step-By-Step Operating Flow

### Step 1. Detect stale operational artifact

The system checks whether:

- the artifact still exists
- it is an operational artifact such as `handoff md` or `issued task packet`
- it has not been updated for `1 hour`

If all are true, the artifact becomes a stale triage candidate.

### Step 2. Inspect code-state reality first

Before asking whether the file should be deleted, the system checks:

- whether owned paths or related code artifacts exist
- whether partial implementation already happened
- whether validation evidence is missing
- whether a newer final artifact superseded the current one

This step is critical because code-state reality is often more reliable than session continuity.

### Step 3. Build LLM triage context

The system prepares a bounded triage input containing:

- artifact path
- last modified time
- related code paths
- recent validation evidence or lack of it
- prior triage result if one exists
- any newer packet/reference that may supersede it

The goal is to ask the LLM a narrow operational judgment question, not a broad redesign question.

### Step 4. Ask LLM triage questions

The LLM is asked, in order:

- whether completion conditions or validation are still missing
- whether the artifact was intentionally held
- whether the task drifted away from the intended plan
- whether the task was already completed and promoted elsewhere
- whether the next action should be `resume`, `keep`, `archive`, or `delete`

Deletion is not asked first.

Deletion is only asked after recovery value has been checked.

### Step 5. Classify the stale artifact

The artifact is classified into one of the following:

- `resume_candidate`
- `intentional_hold`
- `drifted_abandon_candidate`
- `completed_cleanup_candidate`
- `user_review_candidate`

This classification controls all later action.

### Step 6. Resume before cleanup whenever possible

If the classification is `resume_candidate`, the system should:

- prepare context reinjection
- identify missing checks
- identify missing evidence
- relaunch or repacket the work

This is the default branch for ambiguous or partially completed stale files.

### Step 7. Escalate ambiguous cases to the user

If the artifact cannot be safely resumed or safely cleaned, it becomes:

- `user_review_candidate`

In that case, the system should present:

- current classification
- reason for ambiguity
- suggested next action

The user then decides whether to:

- keep
- resume
- archive
- delete

### Step 8. Cleanup only after explicit eligibility

Cleanup is allowed only when the triage result is:

- `completed_cleanup_candidate`
- or `drifted_abandon_candidate`

Even then, cleanup should remain:

- explicit
- reviewable
- non-hidden

This prevents accidental deletion of interrupted but recoverable work.

## Script Responsibility Split

### 1. Warning-only hook or lint layer

This layer only:

- detects stale artifacts
- emits warning messages
- recommends triage

It must not:

- delete files
- archive files
- mutate operational artifacts

### 2. `triage_operational_artifacts.py`

This script should:

- collect stale artifacts
- inspect related code-state signals
- ask or prepare LLM triage
- emit structured classifications

Its role is:

- classification
- not cleanup

### 3. `resume_operational_artifacts.py`

This script should:

- target `resume_candidate`
- rebuild missing context
- collect related code/evidence
- prepare a relaunch packet or reinjection prompt

Its role is:

- recovery
- not archival judgment

### 4. `cleanup_operational_artifacts.py`

This script should:

- only process explicit cleanup candidates
- support `--archive` or `--delete`
- skip `resume_candidate`
- skip `user_review_candidate`

Its role is:

- explicit cleanup execution
- not classification

## Minimal End-To-End Example

### Situation

- `TASK-RENDER-0001.json` still exists
- it has not changed for `1 hour`
- owned output files partially exist
- no validation result was recorded

### Triage interpretation

This should not be read as:

- safe to delete

It should first be read as:

- likely interrupted
- likely missing final validation
- likely recoverable by reinjecting context

### Correct outcome

The LLM should classify it as:

- `resume_candidate`

The next action should be:

- resume
- not delete

Only if later evidence shows that the task drifted or was already completed elsewhere should cleanup become eligible.

## Reading Rule

This document should be read top-down in this order:

1. `Design Intent`
2. `Step-By-Step Operating Flow`
3. `Classification`
4. `Warning Messages`
5. `Suggested LLM Output Shape`
6. `Cleanup Rule`

The purpose of this order is to make the planning intent legible before the operational mechanics.
