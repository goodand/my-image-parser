# Completion Gate Closed-Question Policy

## Purpose

Freeze the policy that any evaluation or question used to declare completion in the current workspace must be phrased as a closed-ended gate.

This policy exists so completion judgment does not drift into vague narrative interpretation.

## Fixed Decision

- completion declaration questions must be `closed-ended`

Allowed answer forms:

- `yes`
- `no`
- `blocked`
- `not_applicable`

Disallowed forms for the gate itself:

- open-ended prompts
- essay-style questions
- vague qualitative prompts without an explicit gate outcome

## Interpretation

When asking whether a slice is complete, the gate should not ask:

- "How did the review go?"
- "Was the evaluation good enough?"
- "What remains?"

Instead, the gate should ask things like:

1. `Was the accepted evaluation set explicitly frozen?`
2. `Did the reviewer complete all rows in that accepted set?`
3. `Were approved_caption and approved_alt_text filled for all completed rows?`
4. `Was the decision written to session-local artifacts instead of the source markdown?`
5. `Was table-internal value coverage explicitly checked for table-heavy images?`

Each of those questions must be answerable with:

- `yes`
- `no`
- `blocked`
- `not_applicable`

## Operational Effect

After this policy:

- completion reports should expose gate questions as closed-ended check items
- runbooks should describe completion criteria in a way that can be reduced to closed-ended gate checks
- open qualitative feedback remains allowed, but only in supporting sections such as:
  - friction
  - rationale
  - notes
  - blocker details

## Directly Related Files

- [10-image evaluation runbook](../../../../project_domain/resources/master_plans/MASTER_PLAN_10_image_evaluation_runbook-at2026-04-09.md)
- [10-image human evaluation template](../../../../project_domain/resources/reports/REPORT_phase2_review_surface_10_image_human_evaluation_template-at2026-04-09.md)
- [Current evaluation gate verdict](../../../../project_domain/resources/reports/REPORT_phase2_review_surface_current_evaluation_gate_verdict-at2026-04-09-18-37.md)
