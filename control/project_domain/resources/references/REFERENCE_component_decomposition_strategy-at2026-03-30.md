# Reference: Component Decomposition Strategy

## Purpose

Define the implementation strategy for `component decomposition` in the current image parsing experiment stack.

Canonical KB:
- [`KB_component_decomposition_strategy.md`](../knowledge_bases/KB_component_decomposition_strategy.md)

This document exists because `image4`-style composite analytical figures are not blocked only by weak regrouping. The harder missing stage is:

`decomposition -> regrouping -> scoring -> tie-break`

## Problem Framing

The current workspace can already do some useful things:
- split alpha-connected foreground components
- build bounded reviewed crops from parser cell unions
- compare candidate caption surfaces with rule-based scoring

That is enough for:
- single table images
- transparent multi-component images where nearby fragments belong to one dominant region

That is **not** enough for compound figures such as `image4`, where the image meaning is distributed across multiple panels.

For those images, the system must first answer:
- what are the semantic components?
- which components belong together?
- which regrouped surface best matches the current experiment goal?

## Current Local State

### What already exists

- alpha-component extraction:
  - [`scripts/alpha_component_lib.py`](../../../../scripts/alpha_component_lib.py)
- reviewed-crop recrop reinforcement:
  - [`scripts/reviewed_component_context_package_lib.py`](../../../../scripts/reviewed_component_context_package_lib.py)
- bounded direct read of the current edge case:
  - [`REPORT_phase1_image4_edge_case_direct_read_and_recrop_status-at2026-03-30-20-39.md`](../reports/REPORT_phase1_image4_edge_case_direct_read_and_recrop_status-at2026-03-30-20-39.md)
- external research cache:
  - [`REFERENCE_image4_component_decomposition_research-at2026-03-30.md`](./REFERENCE_image4_component_decomposition_research-at2026-03-30.md)

### What is still missing

- a first-class decomposition stage for compound analytical figures
- semantic typing for decomposed regions
- regrouping logic that can reason over dashboard-level intent
- a stable controller that decides when to:
  - keep full image
  - choose table-centric crop
  - choose chart-set crop
  - keep the image excluded

## Strategy Summary

The strategy is:

1. decompose the image into semantically meaningful regions
2. type those regions
3. regroup them into experiment-relevant candidate surfaces
4. score candidates with deterministic rules
5. use model-backed tie-break only when deterministic scoring cannot separate the top candidates

## Stage 0: Eligibility Gate

Before decomposition, classify the source image into a coarse handling family:

- `single_table_like`
- `single_chart_like`
- `transparent_object_like`
- `compound_dashboard_like`
- `unknown`

The purpose is not perfect classification. The purpose is to avoid wasting decomposition effort on images that are already handled by simpler paths.

Suggested signals:
- alpha component count
- OCR density map
- layout block count
- table parser presence
- chart-like axis / legend / bar distribution hints

## Stage 1: Decomposition Proposals

This stage should generate candidate components, not final answers.

### 1A. Deterministic proposals

Use cheap, reproducible methods first:

- alpha connected components
- proximity-based alpha unions
- whitespace gap segmentation
- title-band detection near the top of the image
- OCR token density clustering
- table bbox union from parser output when table evidence exists

These proposals are useful even when they are imperfect. They provide anchors for later regrouping.

### 1B. Model-backed proposals

Use existing or future model-backed tools to add richer blocks:

- `PP-StructureV3` layout/table proposals
- document-layout proposals inspired by `DocLayout-YOLO`
- compound-figure style panel proposals inspired by semantic segmentation literature

Important boundary:
- model-backed proposals should add candidate blocks
- they should not directly replace deterministic evidence

## Stage 2: Component Typing

Each proposed component should be typed into a small stable schema.

Suggested types:
- `title_block`
- `chart_panel`
- `metrics_table`
- `legend_block`
- `axis_text_block`
- `paragraph_text_block`
- `note_block`
- `unknown_block`

Each component should carry:
- `bbox`
- `source`
  - `alpha`
  - `parser`
  - `layout_model`
  - `hybrid`
- `confidence`
- `text_excerpt`
- `pixel_area`
- `component_kind`

## Stage 3: Regrouping

Regroup typed components into candidate caption surfaces.

For the current experiment family, the minimum candidate set should be:
- `full_dashboard`
- `title_plus_table`
- `table_only`
- `chart_set`
- `title_plus_chart_set`

Optional candidates:
- `dominant_panel_only`
- `table_plus_nearby_summary`
- `top_half_dashboard`

The point of regrouping is not to generate all combinations. The point is to generate only experiment-meaningful candidates.

## Stage 4: Scoring

Selection should remain rule-based by default.

Suggested scoring axes:
- OCR evidence support
- metric mention coverage
- parser structure support
- title/context fidelity
- non-target noise suppression
- dashboard meaning preservation
- promotion-state penalty

Key rule:
- `comparison winner` is not automatically `default replacement`

## Stage 5: Tie-Break

When the top candidates are close, use a model-backed tie-break.

Preferred ordering:
1. `subagent` as orchestration controller
2. direct vision/API verification as final fallback

Why:
- the subagent can inspect proposal evidence, reject obviously bad candidates, and decide whether a wider or narrower regrouping should be retried
- the direct vision step should be reserved for cases where deterministic scores and subagent reasoning still leave ambiguity

Important boundary:
- subagent is not the decomposition engine
- subagent is the controller that decides how to use decomposition outputs

## Tool Priority

### Default path

1. deterministic decomposition
2. model-backed proposal enrichment
3. deterministic regrouping
4. rule-based scoring

### Escalation path

5. subagent orchestration
6. direct vision verification

This ordering keeps the system reproducible while still allowing bounded recovery on hard edge cases.

## Evidence Contract

Every decomposition run should leave evidence for later audit.

Minimum artifacts:
- decomposition manifest
- regrouped candidate manifest
- score summary
- selected surface decision
- explicit exclusion or escalation reason when selection fails

Minimum fields:
- `source_image_path`
- `image_kind`
- `component_proposals`
- `typed_components`
- `candidate_surfaces`
- `score_breakdown`
- `selected_surface`
- `selection_reason`
- `needs_tie_break`
- `final_status`

## Success Criteria

The strategy is successful when it can do all of the following on an `image4`-style composite input:

1. decompose the image into more than one semantically meaningful block
2. identify at least:
   - title-level context
   - chart-panel region or chart-set region
   - embedded metrics table region
3. generate regrouped candidates that preserve dashboard semantics
4. avoid over-promoting a narrow table crop when the experiment needs the dashboard meaning
5. explain, with stored evidence, why a candidate was selected or why the image remains excluded

## Recommended Next Slice

Implement a bounded `component decomposition` slice before reopening `image4`:

1. build a decomposition manifest generator
2. type components into the stable schema above
3. generate the minimum regrouped candidate set
4. run rule-based scoring on candidates
5. only then decide:
   - re-enter
   - stay excluded
   - escalate to subagent tie-break

## One-Line Summary

The next real fix is not just `better crop`. It is a proper `component decomposition` stage that makes regrouping and scoring meaningful on compound analytical figures.
