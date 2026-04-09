# Task Packet: Phase 0 Table Triage Selection Gate

## Goal

Produce the bounded Step 0 triage-selection output that decides which PPT-extracted image surfaces, if any, may advance into the first `PaddleOCR` parser smoke.

This packet is for the **selection gate coordinator**.
Read-only subagents may be used for ambiguity resolution, but only the coordinator writes the final selection manifest.

## Packet Basis

This issued packet is derived from these source artifacts:

- `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
- `control/project_domain/resources/experiment_plans/PLAN_phase0_table_branch_activation-at2026-03-27-23-57.md`
- `control/project_domain/resources/specs/contracts/phase0_table_triage_selection.contract.json`
- `control/project_agent_ops/resources/task_packets/canonical/table_branch_triage_selection_canonical_packet.json`
- `control/project_agent_ops/resources/task_packets/standard/table_branch_triage_selection_standard_packet.json`
- `control/project_domain/resources/reports/REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md`

## Fixed Execution Binding

- coordinator id: `PHASE0-TBL-TRIAGE-COORD`
- seed manifest: `control/project_domain/resources/manifests/phase0_table_triage_candidates_seed_at2026_03_28.jsonl`
- output manifest: `control/project_domain/resources/manifests/phase0_table_triage_selection.jsonl`
- contract: `control/project_domain/resources/specs/contracts/phase0_table_triage_selection.contract.json`
- expected seed rows: `2`
- maximum promoted parser-smoke candidates: `2`
- allowed triage subagent ceiling: `6`

There is no single mandatory shell command for this packet.
The execution contract is the manifest row set, not a specific CLI.

## In-Scope Inputs

- required read inputs:
  - `control/project_domain/resources/manifests/phase0_table_triage_candidates_seed_at2026_03_28.jsonl`
  - `control/project_domain/resources/experiment_plans/PLAN_phase0_table_branch_activation-at2026-03-27-23-57.md`
  - `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
  - `control/project_domain/resources/specs/contracts/phase0_table_triage_selection.contract.json`
  - `control/project_domain/resources/reports/REPORT_phase0_imagesorcery_ocr_smoke-at2026-03-27-23-30.md`
  - `control/project_domain/resources/manifests/phase0_imagesorcery_ocr_smoke_summary_at2026_03_27.json`
- allowed write targets:
  - `control/project_domain/resources/manifests/phase0_table_triage_selection.jsonl`

## Required Rules

1. Process only the `2` seed rows bound in this packet.
2. Write exactly one output row per seed row. Do not drop a candidate silently.
3. Use one of these four decisions only:
   - `use_full_image`
   - `use_reviewed_crop`
   - `not_a_table_candidate`
   - `needs_manual_audit`
4. Prefer `use_full_image` unless a reviewed crop is clearly justified by evidence.
5. Do not promote any automatic crop that has not been explicitly reviewed.
6. Keep triage subagents read-only with respect to the output manifest; the coordinator alone writes the final manifest.
7. Do not run `PaddleOCR`, do not create parser raw outputs, and do not design wrappers under this packet.
8. If evidence is insufficient, choose `needs_manual_audit` instead of widening scope.

## Non-Goals

- Do not run `PaddleOCR` boot smoke.
- Do not generate broad object-isolation fanout.
- Do not modify master plans, packet templates, registry indexes, or smoke reports.
- Do not create more than `2` promoted parser-smoke candidates.

## Expected Outputs

- `control/project_domain/resources/manifests/phase0_table_triage_selection.jsonl`

## Done Definition

- The output manifest exists and is readable.
- The manifest contains exactly `2` rows, matching the `2` seed rows one-to-one.
- Every row satisfies the bound contract.
- The number of promoted parser-smoke candidates is between `1` and `2`.
- No shared canonical artifact outside the bound manifest path was modified.

## Stop Conditions

- The seed manifest is missing or unreadable.
- Any source image path in the seed manifest is missing.
- A decision cannot be justified from the current evidence surfaces.
- More than `2` candidates seem required for the first parser smoke.
- Completing the task would require writing outside the bound manifest path.

## Verification

1. Confirm the packet-basis source artifacts exist.
2. Confirm the seed manifest exists and contains exactly `2` rows.
3. Confirm every seed row has a readable `source_image_path`.
4. Produce one output row per seed row using the bound decision enum only.
5. Verify the output manifest promotes at least `1` and at most `2` parser-smoke candidates.
6. Verify the coordinator was the only writer to the output manifest.

## Suggested Working Order

1. read the plan, contract, smoke report, and seed manifest
2. inspect each seed candidate with existing evidence only
3. optionally use read-only `gpt-5.4 xhigh` subagents for ambiguity resolution
4. merge the decisions in the coordinator thread
5. write the final bounded output manifest
6. verify row count, enum usage, and promotion ceiling

## Handoff Note

This packet is immutable for the current Step 0 gate. If the seed candidate set grows, if reviewed crop authority changes, or if a broader parser-smoke scope is needed, publish a new issued packet instead of widening this one.
