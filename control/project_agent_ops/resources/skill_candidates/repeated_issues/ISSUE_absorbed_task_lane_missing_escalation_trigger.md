# Repeated Issue: Absorbed Task Lane Missing Escalation Trigger

## Pattern

A repeated task pattern is absorbed into a parent skill as a sidecar checklist item or implementation step. The absorption is documented in KB `Absorbed Inputs`, but the standalone re-separation criteria ("when should this become its own skill?") is not recorded. The absorbed pattern grows silently until someone manually notices it deserves independent treatment.

## Recurrence Signal

- a KB `Absorbed Inputs` section lists an absorbed task but does not include an escalation trigger
- the absorbed task's implementation step in the parent checklist is a single line without standalone-promotion criteria

## Failure Signature

- the absorbed task is executed independently 3+ times but nobody notices because no trigger threshold is documented
- the parent skill's checklist becomes overloaded with absorbed lanes that are individually large enough to warrant their own skill

## Current Workaround

- explicitly add an escalation trigger line in both the implementation checklist and the KB entry
- format: "if this step is executed independently (no parent-skill context) N+ times, promote to standalone skill"

## Structural Fix Candidate

- skill creation workflow requires every absorbed task lane to have an explicit escalation trigger at absorption time
- skill template includes an `escalation_trigger` field in the absorbed inputs section

## Escalation Trigger

- another task is absorbed into a parent skill without a documented standalone-promotion threshold

## Current Proven Evidence

- on 2026-04-08, `TASK_decision_contract_cross_field_test_expansion.md` was absorbed into `async-migration-verify` as implementation step 7, but initially had no escalation trigger; fixed by adding step 8 ("if step 7 is executed independently 3+ times, promote to standalone skill") and KB escalation annotation
