---
name: component-decomposition-strategy-kb
kb_profile: canonical_design_kb
role: component decomposition strategy for compound analytical figures
ver: 1
created_at: 2026-03-30
updated_at: 2026-03-30
source_scope: my-image-parser workspace
purpose: image4-style composite analytical figures를 decomposition -> regrouping -> scoring 구조로 다루기 위한 canonical strategy를 고정한다
---

# Component Decomposition Strategy KB

## Document map

| 문서 | 역할 |
|---|---|
| `KB_component_decomposition_strategy.md` | canonical strategy KB |
| [REFERENCE_image4_component_decomposition_research-at2026-03-30.md](../references/REFERENCE_image4_component_decomposition_research-at2026-03-30.md) | 외부 논문/도구 research cache |
| [REFERENCE_component_decomposition_strategy-at2026-03-30.md](../references/REFERENCE_component_decomposition_strategy-at2026-03-30.md) | implementation-facing strategy reference |
| [REPORT_phase1_image4_edge_case_direct_read_and_recrop_status-at2026-03-30-20-39.md](../reports/REPORT_phase1_image4_edge_case_direct_read_and_recrop_status-at2026-03-30-20-39.md) | current edge-case interpretation |
| [REPORT_phase1_image4_component_decomposition_probe-at2026-03-30-21-55.md](../reports/REPORT_phase1_image4_component_decomposition_probe-at2026-03-30-21-55.md) | bounded deterministic decomposition probe |
| [REPORT_phase1_image4_component_decomposition_candidate_scoring-at2026-03-30-22-05.md](../reports/REPORT_phase1_image4_component_decomposition_candidate_scoring-at2026-03-30-22-05.md) | objective-profile scoring over regrouped candidates |
| [image4_component_decomposition_paper_cache_at2026_03_30.json](../manifests/image4_component_decomposition_paper_cache_at2026_03_30.json) | saved paper cache manifest |

## Input evidence set

- local image case:
  - `<LOCAL_PPTX_JOBS_ROOT>/01_full_presentation_2026-03-17/media/image4.png`
- current decomposition-adjacent code:
  - `../../../../scripts/alpha_component_lib.py`
  - `../../../../scripts/reviewed_component_context_package_lib.py`
- bounded decomposition probe evidence:
  - `../manifests/phase1_image4_component_decomposition_probe_at2026_03_30.json`
  - `../reports/REPORT_phase1_image4_component_decomposition_probe-at2026-03-30-21-55.md`
- candidate scoring evidence:
  - `../manifests/phase1_image4_component_decomposition_candidate_scoring_at2026_03_30.json`
  - `../reports/REPORT_phase1_image4_component_decomposition_candidate_scoring-at2026-03-30-22-05.md`
- repeated issue memory:
  - `../../../project_agent_ops/resources/skill_candidates/repeated_issues/ISSUE_regrouping_only_fix_stalls_without_component_decomposition.md`

## Canonical design takeaways

1. `image4` 계열 문제의 핵심은 `regrouping`보다 먼저 `component decomposition`이 없다는 점이다.
2. 현재 codebase는 `alpha split`, `reviewed crop recrop`, `rule-based comparison`까지는 있지만 compound analytical figure를 위한 decomposition stage는 없다.
3. compound image 처리는 `decomposition -> regrouping -> scoring -> tie-break` 순서로 고정해야 한다.
4. deterministic proposal은 기본 경로로 유지하고, model-backed proposal은 보강 경로로 사용해야 한다.
5. `subagent`는 decomposition engine이 아니라 orchestration controller로 쓰는 것이 맞다.
6. direct vision/API verification은 deterministic score와 subagent reasoning으로도 top candidate가 갈리지 않을 때만 tie-break로 사용한다.
7. `comparison winner`는 `default replacement`가 아니며, component selection이 좋아 보여도 baseline 교체와는 분리해 해석해야 한다.
8. evidence contract가 반드시 필요하다. decomposition run은 proposal, typing, regrouping, score, selection reason을 남겨야 한다.
9. `image4` 같은 multi-panel dashboard는 table-only crop으로 과도하게 축소되면 실험 의미를 잃을 수 있다.
10. 다음 구현 우선순위는 “더 나은 crop”이 아니라 “decomposition manifest generator”다.

## Current workspace fit

### Existing assets

- alpha component extraction:
  - `../../../../scripts/alpha_component_lib.py`
- reviewed recrop reinforcement:
  - `../../../../scripts/reviewed_component_context_package_lib.py`
- image4 direct-read status:
  - `../reports/REPORT_phase1_image4_edge_case_direct_read_and_recrop_status-at2026-03-30-20-39.md`

### Current limitation

The current workspace can:
- separate transparent connected components
- widen a reviewed crop when nearby alpha fragments were omitted
- score candidate caption surfaces downstream

The current workspace cannot yet:
- decompose a compound analytical figure into typed semantic blocks
- regroup those blocks into dashboard-aware candidate surfaces
- select among those regrouped surfaces with stable evidence

## Strategy pipeline

| Stage | Goal | Current state |
|---|---|---|
| Decomposition | meaningful component proposals | missing as first-class stage |
| Typing | assign semantic role to each component | missing |
| Regrouping | build experiment-relevant candidate surfaces | partial only |
| Scoring | deterministic quality comparison | present |
| Tie-break | bounded escalation on ambiguity | partial |

## Decomposition stage

The first-class decomposition stage should propose components, not final answers.

### Deterministic proposal sources

- alpha connected components
- proximity-based alpha unions
- whitespace gap segmentation
- title-band heuristics
- OCR token-density clustering
- parser-derived table bbox unions when table evidence exists

### Model-backed proposal sources

- existing `PP-StructureV3` layout/table signals
- layout proposal ideas aligned with `DocLayout-YOLO`
- compound-figure panel proposal ideas aligned with semantic-segmentation literature

### Stable rule

Model-backed proposals should enrich proposal coverage, not erase deterministic evidence.

## Component typing schema

Every component proposal should be typed into a stable schema.

Minimum types:
- `title_block`
- `chart_panel`
- `metrics_table`
- `legend_block`
- `axis_text_block`
- `paragraph_text_block`
- `note_block`
- `unknown_block`

Minimum fields per component:
- `bbox`
- `source`
- `component_kind`
- `confidence`
- `pixel_area`
- `text_excerpt`

## Regrouping stage

Typed components should be regrouped into experiment-meaningful candidate surfaces.

Minimum candidate set:
- `full_dashboard`
- `title_plus_table`
- `table_only`
- `chart_set`
- `title_plus_chart_set`

Optional candidates:
- `dominant_panel_only`
- `table_plus_nearby_summary`
- `top_half_dashboard`

Regrouping should stay intentionally narrow. The goal is not to enumerate all combinations, only the combinations that preserve experiment meaning.

## Scoring stage

Candidate selection should remain rule-based by default.

Suggested scoring axes:
- OCR evidence support
- metric mention coverage
- parser structure support
- title/context fidelity
- non-target noise suppression
- dashboard meaning preservation
- promotion-state penalty

## Tie-break stage

Tie-break is allowed only after deterministic scoring fails to separate top candidates.

Preferred order:
1. subagent orchestration
2. direct vision/API verification

Interpretation rule:
- subagent decides how to inspect and retry candidate surfaces
- direct vision resolves only the last ambiguous cases

## Tool priority

### Default path

1. deterministic decomposition
2. model-backed proposal enrichment
3. deterministic regrouping
4. rule-based scoring

### Escalation path

5. subagent controller
6. direct vision fallback

## Evidence contract

Every decomposition run should leave:
- decomposition manifest
- typed component list
- regrouped candidate manifest
- score summary
- selected surface decision
- explicit exclusion or escalation reason when unresolved

Minimum decision fields:
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

## Success boundary for image4

The strategy is considered effective when it can:
- separate title-level context from chart and table regions
- identify chart-panel region or chart-set region
- identify embedded metrics table region
- generate regrouped surfaces that preserve dashboard semantics
- justify whether `image4` should re-enter or remain excluded

## Current operational decision

Until the decomposition stage exists, `image4` should remain an excluded edge case.

The new recrop logic is still useful, but it is not sufficient proof that a dashboard-like image should re-enter the stable phase1 cohort.

## Research-lane hold rule

`component decomposition` is currently a research-lane candidate, not a mainline blocker.

Operational interpretation:
- `Session A` may own the bounded `image4` re-entry slice
- other sessions should continue the current mainline using the already closed stable cohort
- no current master-plan lane should wait for a generalized compound-figure solver before moving forward

Promotion rule:
- keep decomposition in the research lane until either:
  - `image4` re-entry closes with evidence-backed manifests and reports
  - or the same decomposition pattern proves reusable on at least one additional composite edge case

Fast-path rule:
- while decomposition remains unresolved, keep `image4` excluded
- continue downstream consumer, review, mapping, and regeneration work on the stable cohort
- treat decomposition output as an optional upgrade path, not a precondition for the current master-plan mainline

## Recommended next slice

Build a bounded decomposition slice in this order:

1. decomposition manifest generator
2. component typing pass
3. regrouped candidate generator
4. rule-based score runner
5. bounded re-entry decision for `image4`

## Not part of this KB

- semantic judge implementation
- default baseline replacement policy
- screenshot-arm expansion
- arbitrary exhaustive crop enumeration

## Reference basis

- `../references/REFERENCE_image4_component_decomposition_research-at2026-03-30.md`
- `../references/REFERENCE_component_decomposition_strategy-at2026-03-30.md`
- `../reports/REPORT_phase1_image4_edge_case_direct_read_and_recrop_status-at2026-03-30-20-39.md`
- `../../../project_agent_ops/resources/skill_candidates/repeated_issues/ISSUE_regrouping_only_fix_stalls_without_component_decomposition.md`
