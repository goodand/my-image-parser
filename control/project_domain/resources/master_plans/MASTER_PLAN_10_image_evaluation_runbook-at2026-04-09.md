# MASTER_PLAN_10_image_evaluation_runbook-at2026-04-09

## Intent

이 문서는 `my-image-parser` master plan completion에 필요한 **10-image bootstrap/open + session-local writeback proof state**를 고정하는 runbook이다.

Steward response 이후, 이 문서는 더 이상 final human evaluation completion runbook이 아니다. 현재 역할은:

1. bootstrap/open 경로와 writeback 경로가 어디까지 닫혔는지 고정
2. 어떤 session artifact가 이미 생성되었는지 고정
3. current first-10 bootstrap set의 comparison readiness가 partial임을 명시
4. final acceptance 전 남은 구현/운영 경계를 명시

## Proven Readiness

아래는 이미 완료되었다.

1. `vscode-markdown-review-surface`에 bootstrap command가 추가되었다.
   - command: `Review Surface: Open Bootstrap Evaluation Session`
2. bootstrap helper가 contract-valid session artifacts를 생성한다.
3. helper/unit/smoke가 통과했다.
4. 실제 `my-image-parser` review markdown 기준으로 10-image bootstrap session이 생성되었다.
5. session-local candidate bundle artifacts가 생성되고 first-10 session에 backfill되었다.
6. `decision-slides` surface에서 local image preview와 session-local metadata projection이 보이는 상태까지 올렸다.
7. `image7` - `image10`에 대해서는 candidate comparison payload가 session-local bundle에 존재한다.
8. source review markdown는 read-only source로 유지되고, 저장은 session dir의 `decision-seed.jsonl` / `feedback-ledger.json`에 누적된다.
9. context / decision form label을 operator-readable copy로 정리했다.

검증 baseline:

- `node --check` 통과
- `npm test` 통과
- latest exact pass count는 stale reference drift 방지를 위해 의도적으로 여기 적지 않는다.

## Source Review Markdown

- `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md`

## Generated Session

session dir:

- `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.review-surface-session/phase2-caption-decision-slides-first-10`

generated artifacts:

- `session-config.json`
- `review-surface-manifest.json`
- `decision-seed.jsonl`
- `feedback-ledger.json`
- `bundles/`

current candidate bundle availability snapshot:

- `image1` - `image5`: `excluded`
- `image6`: `missing_source_record`
- `image7` - `image10`: `ready` with 4 candidate arms

operational interpretation:

- `image1` - `image5`는 source markdown에 caption/alt text는 있지만, four-arm comparison candidate set에서는 명시적으로 제외되었다.
- `image6`는 `unsupported_media_type` source라 current bootstrap session에서 comparison bundle을 만들지 못했다.
- 따라서 current first-10 bootstrap set 전체를 `comparison-ready`라고 부를 수는 없다.

bootstrap image order:

1. `image1`
2. `image2`
3. `image3`
4. `image4`
5. `image5`
6. `image6`
7. `image7`
8. `image8`
9. `image9`
10. `image10`

## Current Bootstrap Reproduction

1. VS Code에서 아래 markdown를 연다.
   - `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md`
2. Command Palette를 연다.
3. `Review Surface: Open Bootstrap Evaluation Session` 실행
4. 열린 `decision-slides` surface에서 bootstrap/open 상태와 session-local artifact projection을 재현
5. 현재 상태에서는 이 session을 final acceptance evaluation로 간주하지 않는다.
6. source markdown 본문 자체는 이 경로에서 직접 덮어쓰지 않는다.

## Where Current Bootstrap Results Accumulate

source markdown는 read-only source다.

- source markdown:
  - `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md`

평가 결과는 아래 session-local 파일에 누적된다.

- decision rows:
  - `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.review-surface-session/phase2-caption-decision-slides-first-10/decision-seed.jsonl`
- feedback ledger:
  - `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.review-surface-session/phase2-caption-decision-slides-first-10/feedback-ledger.json`

## What Counts As Final Completion

Steward response 이후, 이 runbook만으로는 완료를 선언할 수 없다.

final completion은 아래를 모두 만족해야 한다.

1. reviewer가 surface 안에서 candidate caption/alt-text comparison을 읽고 bounded decision을 내릴 수 있다.
2. actual 10-image evaluation 대상 집합이 current first-10 bootstrap set으로 괜찮은지, 아니면 refreshed set이 필요한지 운영적으로 확정한다.
3. accepted 10-image set에 대해 actual human evaluation을 수행한다.
4. 표 중심 이미지에서는 `table-internal value coverage`를 명시적으로 검토한다.
5. 평가 완료 사실을 별도 acceptance/reference 문서로 남긴다.
   - template:
     - `control/project_domain/resources/reports/REPORT_phase2_review_surface_10_image_human_evaluation_template-at2026-04-09.md`

completion gate question format:

- completion declaration에 사용하는 질문은 모두 폐쇄형으로 작성한다.
- allowed answers:
  - `yes`
  - `no`
  - `blocked`
  - `not_applicable`

## Remaining Gap

Steward response note:

- `control/user_decisions/resources/notes/NOTE_review_surface_requirement_response_by_control-plane-program-steward-at2026-04-09-14-17.md`

현재 남은 것은 아래 순서다.

1. `artifact contract extension`
2. `candidate-text comparison section`
3. `label readability / operator clarity`
4. actual 10-image evaluation run on the refreshed comparison-ready surface
5. acceptance/reference evidence 정리
6. cross-mode consolidation

current known friction:

- current first-10 bootstrap set은 `excluded`, `missing_source_record`, `ready`가 섞여 있다.
- `decision-seed.jsonl`에는 excluded/missing slide에도 generic comparison metadata가 남아 있어 operator를 혼란스럽게 할 수 있다.
- table-heavy images에서 후보 caption이 표 내부 값이나 row/column-level 수치를 충분히 묘사하지 않는 경향이 반복된다.

즉 현재 `10-image bootstrap entry`는 **source markdown read-only + session-local writeback proof + partial comparison readiness** 상태다. 남은 핵심 병목은 contract extension, comparison UX completion, 그리고 table-value coverage를 포함한 actual human evaluation run이다.

## Supporting References

상위 진행/평가 packet:

- `<VSCODE_REVIEW_SURFACE_ROOT>/control/project_domain/resources/references/REFERENCE_review_surface_progress_and_expert_evaluation_packet-at2026-04-08.md`

상세 writeback packet:

- `<VSCODE_REVIEW_SURFACE_ROOT>/control/project_domain/resources/references/REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md`

acceptance report template:

- `control/project_domain/resources/reports/REPORT_phase2_review_surface_10_image_human_evaluation_template-at2026-04-09.md`

steward response note:

- `control/user_decisions/resources/notes/NOTE_review_surface_requirement_response_by_control-plane-program-steward-at2026-04-09-14-17.md`

completion gate policy note:

- `control/user_decisions/resources/notes/NOTE_completion_gate_closed_question_policy-at2026-04-09-18-41.md`

## 2026-04-09 Scope Freeze And Closure Reclassification

scope freeze note:

- `control/user_decisions/resources/notes/NOTE_review_surface_cross_validation_scope_freeze-at2026-04-09-19-03.md`

closure report:

- `control/project_domain/resources/reports/REPORT_phase2_review_surface_cross_validation_slice_closure-at2026-04-09-19-03.md`

The earlier sections in this runbook remain historically accurate, but their blocker interpretation is now superseded for the current workspace slice.

The user froze the purpose of this lane as:

- image captioning on extracted images is the main test
- review-surface evaluation is bounded cross-validation for that main test

Therefore this runbook is now considered **closed for the current `my-image-parser` slice** because:

1. source markdown stayed read-only
2. session-local writeback succeeded
3. the accepted first-10 bootstrap cohort was frozen
4. every row now has a terminal state
5. ready images have approved caption and alt text
6. non-ready images are explicitly deferred to the manual lane
7. remaining external review-surface UX work no longer blocks this workspace slice

effective current status:

- `closed for my-image-parser review-surface cross-validation slice`

remaining follow-up status:

- `external/non-blocking` for this slice
