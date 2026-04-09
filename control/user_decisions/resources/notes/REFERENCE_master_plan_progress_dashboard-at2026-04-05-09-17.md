# Reference: Master Plan Progress Dashboard

## Purpose

이 문서는 현재 master plan 진행률과 병목을 한 장에서 보이게 하기 위한 운영용 dashboard다.

문제는 현재 다음과 같다.

- canonical master plan은 append-oriented라서 현재 상태가 문서 뒤쪽 patch에 숨어 있다
- draft plan들은 각자 `Status`와 `Phase`를 갖지만 cross-plan 우선순위가 한곳에 모여 있지 않다
- 새 VS Code review-surface 구현 진행은 별도 workspace의 `runs/reports`에 저장되어 있어 old workspace의 master-plan surface에서는 바로 안 보인다

따라서 이 문서는:

- 활성 plan
- 현재 완료 범위
- 병목
- 다음 의사결정

만 빠르게 보여주는 상위 scoreboard로 사용한다.

Task dependency와 병목을 Mermaid로 보려면:

- [REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md](./REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md)

## Executive Summary

현재 기준으로 가장 큰 병목은 **구현 자체보다 progress visibility drift**다.

- `Presentation Image Pipeline`은 설계와 bounded comparison 준비가 많이 진척됐지만, corpus-wide 실행과 최종 승격 결정은 아직 닫히지 않았다.
- `VS Code Markdown Review Surface`는 실제 구현이 이미 시작되었고 MVP도 진척됐지만, old workspace master-plan surface에는 그 진척이 반영되어 있지 않다.
- 따라서 사용자의 다음 의사결정은 “무엇을 할 수 있나”보다 **“지금 활성 priority를 어느 lane에 둘 것인가”**를 먼저 고정하는 것이다.

## Scoreboard

### 1. Presentation Image Pipeline

- canonical document:
  - [MASTER_PLAN_presentation_image_pipeline.md](../../../project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)
- current lane:
  - `4-mode comparison readiness and expansion`
- progress shape:
  - core contract and pipeline architecture: complete enough for active use
  - bounded 4-mode readiness on `image11`: complete
  - phase1 small-batch `5-image` closure: complete
  - corpus-wide `14-image` eligibility scan: complete
  - full corpus execution and final arm-promotion decision: not closed
- current bottleneck:
  - ready subset 밖 이미지들은 frozen derived-arm artifact가 부족함
  - `image4`는 mixed chart-table edge case로 계속 예외 처리됨
  - 따라서 corpus-wide lane은 “실행 가능 이미지 subset”과 “의도한 전체 corpus” 사이에 간극이 있음
- current practical reading:
  - `bounded comparison infrastructure`: high progress
  - `corpus-wide operational closure`: medium progress
  - `default arm replacement decision`: still open
- key evidence:
  - [MASTER_PLAN_presentation_image_pipeline.md:1468](../../../project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md#L1468)
  - [MASTER_PLAN_presentation_image_pipeline.md:1498](../../../project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md#L1498)
  - [MASTER_PLAN_presentation_image_pipeline.md:1519](../../../project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md#L1519)

### 2. VS Code Markdown Review Surface

- source plan:
  - [PLAN_vscode_markdown_review_surface_replacement_strategy-at2026-03-30.md](../../../project_domain/resources/master_plans/drafts/PLAN_vscode_markdown_review_surface_replacement_strategy-at2026-03-30.md)
- actual implementation repo:
  - `<EXTERNAL_REVIEW_SURFACE_ROOT>`
- progress shape:
  - migration pass: complete
  - smoke gate: complete
  - renderer replacement to `markdown-it`: complete
  - sibling sidecar state: complete
  - direct hardening patch round: complete
  - language-service integration: partial / active
  - backlink and decision-artifact layers: not started
- current bottleneck:
  - extension-host test stability is weaker than syntax/lint confidence
  - copied skills still contain old-root drift
  - language-service rename lifecycle and richer editor protocol are not fully hardened yet
- current practical reading:
  - `review core MVP`: high progress
  - `editor protocol hardening`: medium progress
  - `backlink / decision integration`: low progress
- key evidence:
  - [PLAN_vscode_markdown_review_surface_replacement_strategy-at2026-03-30.md:68](../../../project_domain/resources/master_plans/drafts/PLAN_vscode_markdown_review_surface_replacement_strategy-at2026-03-30.md#L68)
  - Review-surface MVP smoke: `<EXTERNAL_REVIEW_SURFACE_ROOT>/control/project_domain/runs/smoke/SMOKE_review_surface_mvp-at2026-03-30.md`
  - Renderer replacement report: `<EXTERNAL_REVIEW_SURFACE_ROOT>/control/project_domain/runs/reports/REPORT_renderer_replacement_markdown_it-at2026-03-30.md`
  - Sidecar state report: `<EXTERNAL_REVIEW_SURFACE_ROOT>/control/project_domain/runs/reports/REPORT_sidecar_state-at2026-03-30.md`
  - Direct patch round-2 report: `<EXTERNAL_REVIEW_SURFACE_ROOT>/control/project_domain/runs/reports/REPORT_codex_direct_patch_round2_sync_gate-and-fixture-isolation-at2026-03-30.md`

## Current Bottleneck Classification

### Bottleneck A. Progress Visibility Drift

- severity: highest
- why it matters:
  - you cannot tell “what is active now” from the canonical master-plan surface without rereading appended sections and separate repo reports
- immediate fix:
  - keep this dashboard as the top reading entry before opening detailed plans

### Bottleneck B. Corpus-Wide Comparison Readiness Gap

- severity: high
- why it matters:
  - pipeline architecture is ready, but broad execution is gated by incomplete frozen arm artifacts outside the stable subset
- immediate fix:
  - decide whether the next decision should be made on the ready subset or whether artifact completion for the excluded corpus is worth the cost first

### Bottleneck C. Review-Surface State Drift Between Plan And Repo

- severity: high
- why it matters:
  - the design draft understates actual implementation progress, so planning decisions are made on stale status
- immediate fix:
  - keep the implementation progress in `user_decisions` overlays and repo run reports, not in the plan body

### Bottleneck D. Extension-Host Confidence Gap

- severity: medium
- why it matters:
  - review-surface code is moving, but `npm test` stability is weaker than `check`/`lint`
- immediate fix:
  - treat `check + lint + bounded smoke evidence` as current gate, and keep test-harness hardening as a separate explicit lane

## Recommended Decision Order

### Decision 1. Which lane is the current top priority?

- option A:
  - `Presentation Image Pipeline` comparison and arm-promotion decision
- option B:
  - `VS Code Review Surface` productization

Current recommendation:

- choose A if your immediate need is caption-arm comparison and production pipeline judgment
- choose B if your immediate need is human review UX and decision-support tooling

### Decision 2. If pipeline stays first, what is the next bounded target?

- option A:
  - decide using the already stable `5-image` ready subset
- option B:
  - spend more time closing missing derived-arm artifacts for broader corpus coverage

Current recommendation:

- choose A unless corpus coverage itself is the thing under test

### Decision 3. If review-surface stays first, what is the next bounded target?

- option A:
  - language-service hardening and test confidence
- option B:
  - backlink/wikilink layer
- option C:
  - decision-artifact side views

Current recommendation:

- choose A
  - the editor core is already real
  - protocol hardening and language-service correctness are the next leverage point

## Reading Order

1. this dashboard
2. [MASTER_PLAN_presentation_image_pipeline.md](../../../project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)
3. [PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md](../../../project_domain/resources/master_plans/drafts/PLAN_codebase_per_image_caption_experiment_comparison-at2026-03-27-16-46.md)
4. [PLAN_vscode_markdown_review_surface_replacement_strategy-at2026-03-30.md](../../../project_domain/resources/master_plans/drafts/PLAN_vscode_markdown_review_surface_replacement_strategy-at2026-03-30.md)
5. the latest `vscode-markdown-review-surface` run reports

## Operator Note

이 dashboard의 역할은 “세부 설계를 대체”하는 것이 아니라:

- 어디까지 왔는지
- 지금 뭐가 막고 있는지
- 다음 질문을 어디에 던져야 하는지

를 빠르게 보이게 하는 것이다.
