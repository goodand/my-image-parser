# Repeated Issue: Subagent Read-Only Audit Timeout Nonblocking

## Pattern

Read-only explorer or auditor subagents can time out while the main agent is doing direct file verification. This should not block the main agent from reaching a final canonical verdict.

## Recurrence Signal

- a subagent is launched as a secondary auditor
- the main agent already has local file access and can verify directly
- the subagent times out or returns no useful finding before the direct audit is complete

## Current Workaround

- treat the subagent as a secondary or independent audit path only
- complete the canonical verification with direct file reads, tests, and artifact checks
- close the timed-out subagent instead of waiting indefinitely

## Structural Fix Candidate

- standardize read-only audit delegation as nonblocking
- state explicitly in strategy docs that the main agent owns the final verdict when local evidence is already available

## Escalation Trigger

- if a future workflow begins depending on a subagent audit result before the main agent can proceed
- if repeated timeouts are caused by oversized packets or ambiguous audit scope
