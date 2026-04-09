# Caption Arm Comparison Surface

This document defines the reusable local comparison surface for caption arms that share one source image but differ in input surface, context package, or parser enrichment.

It is a design and implementation spec for the current workspace comparison builder, not a claim that every planned arm is always available.

## Purpose

The comparison surface exists to answer one bounded question safely:

- can two or more caption arms be compared side by side on the same image without overstating promotion or readiness?

The surface is intended for:

- bounded two-mode comparison
- ready-arm anchor construction when only some planned arms exist
- later three-mode or four-mode merge preparation
- explicit review-gate handling before any rerun is treated as a default replacement

It is not intended to:

- make promotion decisions automatically
- replace the master readiness report
- mutate ledgers or context packages

## Current Implementations

The current implementation lives at:

- `scripts/caption_arm_comparison_lib.py`
- `scripts/run_caption_arm_comparison.py`
- `scripts/test_caption_arm_comparison_lib.py`

Current proven outputs:

- `control/project_domain/resources/manifests/phase0_caption_two_mode_comparison_at2026_03_28.json`
- `control/project_domain/resources/reports/REPORT_phase0_caption_two_mode_comparison-at2026-03-28-10-56.md`
- `control/project_domain/resources/manifests/phase0_caption_three_mode_comparison_at2026_03_28.json`
- `control/project_domain/resources/reports/REPORT_phase0_caption_three_mode_comparison-at2026-03-28-11-35.md`

## Source Of Truth

The comparison surface reads caption ledgers and treats each compared arm as one ledger-backed record resolved by `source_image_path`.

Primary sources are:

- `control/project_agent_ops/registry/jobs/image_caption_jobs/*.json`

Each arm record is resolved from:

- one ledger file
- one shared `source_image_path`

The comparison surface must not synthesize arm records without a real ledger-backed source.

## Required Comparison Record Shape

Each compared arm is reduced into a `CaptionModeRecord`-like shape with these minimum fields:

- `execution_arm`
- `ledger_path`
- `job_id`
- `model`
- `prompt_version`
- `image_id`
- `source_image_path`
- `status`
- `input_surface`
- `caption`
- `alt_text`
- `context_package_present`
- `context_review_status`
- `ocr_status`
- `context_package_json_path`
- `context_variant`

The comparison surface may expose more fields later, but these are the current stable minimum.

Current source-based grouped context names are:

- `ppt_provenance_context`
- `ocr_evidence_context`
- `structured_parse_context`

For `parser_table_enriched` arms, parser-specific structured context is currently grouped under:

- `structured_parse_context`
  - `table_summary`
  - `selected_text_evidence`
  - `table_structure_info`

Legacy compatibility fields such as `table_summary`, `selected_text_evidence`, `parser_enrichment`,
and `parser_structured_context` may still be present for backward compatibility, but new readers
should prefer the source-based grouped context names above.

## Core Rules

### 1. Same Source Image First

Comparability is anchored on `source_image_path`, not on `image_id`.

Reason:

- different ledgers can assign different `image_id` values to the same source image
- that difference is nonblocking drift, not a hard comparison failure

### 2. Review-Gate Promotion Rule

Promotion state is derived from `context_review_status`.

Current mapping:

- `accepted` -> `candidate_ready`
- `reviewed_candidate` -> `comparison_ready_reviewed_branch`
- `pending_review` -> `comparison_only_pending_context_review`
- `null` or anything unresolved -> `blocked_by_context_review`

This surface is allowed to compare a rerun even when it is not yet default-ready.

It must not silently promote a rerun into the current default while review is still pending.

### 3. Parity Audit Rule

The comparison output must expose a `parity_audit` block.

Current parity audit checks:

- required fields are present
- same `source_image_path`
- same model family
- visible drift in:
  - `image_id`
  - `prompt_version`
  - `input_surface`
  - `review_status`
  - `context_variant`
  - `ocr_status`
  - `context_package_present`

Current blocking rule:

- missing required fields
- different source image

Current nonblocking drift:

- different `image_id`
- different `prompt_version`
- different `input_surface`
- different `review_status`

### 4. Anchor Construction Rule

If only some planned arms exist, the comparison surface may still produce an anchor artifact.

That anchor must:

- list only the ready arms
- carry explicit promotion-state information per rerun arm
- keep the current default tied to the baseline arm
- avoid implying that all planned arms are available

## Current Surfaces

### Two-Mode Comparison

Current function:

- `compare_caption_modes(baseline, rerun)`

Current use:

- baseline versus one rerun

Output characteristics:

- single `promotion_state`
- signal delta versus baseline
- parity audit
- report text for bounded two-arm reading

### Ready-Arm Anchor Comparison

Current function:

- `compare_ready_caption_arms(baseline, *candidate_arms)`

Current use:

- baseline plus multiple completed rerun arms that are comparison-ready but may still be pending review

Output characteristics:

- `per_arm_promotion`
- `ready_arms`
- `blocked_arms`
- `comparison_scope = ready_arm_anchor`
- parity audit across every included arm

### Generic CLI Candidate-Arm Injection

The current runner also supports a reusable candidate-arm CLI surface.

Current flag:

- `--candidate-arm execution_arm=ledger_path::fallback_input_surface`

Rules:

- the flag may be repeated
- the runner must keep `full_image_baseline` as the fixed baseline anchor
- each candidate arm must have a unique `execution_arm`
- omitted `fallback_input_surface` currently defaults to `full_image_original`
- when `--candidate-arm` is present, `--rerun-ledger` is no longer required

### Reviewed-Component Parent Anchor Rule

Some future arms may use a bounded crop as the executed image surface while still belonging to the same original source image.

Current comparison rule:

- if a ledger record exposes `reviewed_component_enrichment.parent_source_image_path`, the comparison surface must treat that parent image as the anchor path
- the crop image may still remain the executed surface through `input_surface` and `context_variant`
- this lets a reviewed isolated-component arm join the same multi-arm comparison without pretending the crop is a different source image

Purpose:

- add a fourth or later arm without patching the runner again
- keep later reviewed isolated-component or other future arms on the same comparison surface
- preserve the same promotion gate and parity audit semantics

### Frozen Eval Bundle Output

The current runner may also emit a frozen eval bundle alongside the comparison artifact.

Current optional flags:

- `--bundle-json`
- `--bundle-report-md`

Purpose:

- freeze one comparison-ready multi-arm surface into a downstream-consumable bundle
- give deterministic or judge evaluation lanes a stable input that does not require re-reading the original ledgers
- keep Session A and Session B outputs separated while preserving the same comparison truth

## Current Bounded Interpretation

The current three-mode anchor means:

- `full_image_baseline` is the current default
- `full_image_ocr_context_rerun` is comparison-ready but not default-ready
- `parser_table_enriched_rerun` is comparison-ready but not default-ready

This does not mean:

- the workspace is already four-mode ready
- an isolated-component arm may be omitted forever
- pending-review reruns can replace the baseline automatically

## Non-Goals

This surface does not own:

- isolated-component crop selection
- parser execution
- OCR execution
- context package construction
- master readiness verdicts
- registry mutation

## Immediate Extension Path

When a fourth arm becomes real, the next extension should:

1. reuse the existing `CaptionModeRecord` shape
2. keep `source_image_path` as the comparison anchor
3. keep promotion-state logic unchanged
4. preserve `parity_audit` semantics
5. emit either:
   - a four-mode anchor
   - or a four-mode readiness artifact that explicitly carries `waived` or `blocked` arms
6. prefer `--candidate-arm` injection over new runner branches when a new arm already has a ledger-backed record
