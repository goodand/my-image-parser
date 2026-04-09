# ISSUE: Master-Plan Reread Overhead On Parallel Bounded Sessions

## Summary

Parallel bounded sessions lose time and produce interpretation drift when each session re-enters through the full master plan instead of through a frozen slice-level packet.

## Recurrence signal

This issue is present when:
- two or more sessions work on the same experiment in different lanes
- each session starts by re-reading broad planning docs
- the real work only needs a narrow truth subset
- session startup time becomes dominated by context reconstruction instead of execution

## Current workaround

Use a fast-start packet that fixes:
- current canonical truth
- fixed interpretation
- owned paths
- non-goals
- validation

## Structural fix candidate

Reusable packet-first session split workflow for bounded experiment slices.

## Escalation trigger

Escalate when another producer/consumer split starts with repeated master-plan reread instead of a slice-level truth packet.
