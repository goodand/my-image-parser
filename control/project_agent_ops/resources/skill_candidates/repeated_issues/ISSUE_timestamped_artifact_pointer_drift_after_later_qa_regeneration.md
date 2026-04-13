# Repeated Issue: Timestamped Artifact Pointer Drift After Later QA Regeneration

## Symptom

- a plan or index points at a timestamped artifact filename
- a later, more accurate artifact is generated with a new timestamp
- the original pointer silently becomes stale even though the bounded slice itself is otherwise complete

## Scope

- plans that name timestamped QA reports
- review indexes that point at timestamped summaries
- bounded public-surface slices where artifact names encode time rather than a stable alias

## Guardrail

- verify whether the old timestamped target still exists before trusting the pointer
- if the new artifact is already committed and semantically equivalent in role, patch only the pointer
- treat this as artifact-pointer correction, not as a content reinterpretation pass

## Follow-Up

- consider stable aliases or latest-pointer summaries for timestamped outputs
- add a packaging check that catches stale timestamped references before final public-surface commit

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` found that `PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md` still pointed to `REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-10-18.md`
- the old file was missing, the newer `...13-30.md` report was already committed, and the fix was a one-line pointer correction committed as `2b09aae`

## Step-By-Step Evidence Trace

1. The bounded lean slice was first checked for any remaining uncommitted files after the major packaging commits had landed.
2. One remaining lean-related diff was isolated:
   - `control/project_domain/resources/master_plans/drafts/PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md`
3. The diff itself was then read line-by-line and reduced to one pointer change in `Output artifacts`.
4. Existence was verified on both targets.
   - newer report exists: `control/project_domain/resources/reports/REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md`
   - older report missing: `...10-18.md`
5. Repo history confirmed the newer report was already canonical.
   - commit evidence: `2a7beb6`
6. Only after those checks did the one-line pointer correction land in `2b09aae`.
