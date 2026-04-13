# Control-Plane Program Steward 제출용
## Review Surface 요구사항 재확인 + 현재 상태 제출 Packet

작성일: 2026-04-09
작성 목적:
- `my-image-parser` Master Plan 완료를 위해 `vscode-markdown-review-surface` 기반 10-image human evaluation surface의 요구사항을 다시 확인받기 위함
- 지금까지 구현/검증된 범위와 남은 요구사항 경계를 한 번에 확인할 수 있도록 관련 산출물과 주요 코드 모듈을 제출하기 위함

## Status

이 제출 문서에 대한 Steward 응답은 아래 note로 고정되었다.

- `my-image-parser/control/user_decisions/resources/notes/NOTE_review_surface_requirement_response_by_control-plane-program-steward-at2026-04-09-14-17.md`

따라서 이 문서는 open question packet으로 남기되, 현재의 authoritative requirement answer는 위 note를 따른다.

## 1. 이번 요청의 핵심
현재 `Review Surface: Open Bootstrap Evaluation Session` 경로로 10개 이미지 평가 세션을 실제로 열 수 있는 상태까지는 올라왔습니다. 다만 실제 사용성 확인 과정에서, 현재 surface가 제공하는 정보가 "모드별 caption/alt text 후보를 직접 비교하는 UX"인지, 아니면 "기존 markdown 본문을 읽으면서 decision metadata를 입력하는 UX"인지가 아직 명확하지 않다는 점이 드러났습니다.

특히 실제 테스트에서 다음이 확인되었습니다.
- `decision-slides` surface 자체는 열리고, local image resolution도 동작합니다.
- 그러나 오른쪽 패널은 현재 `active default`, `comparison winner`, `promotion state` 같은 decision metadata 중심입니다.
- 사용자는 "각 mode 별 caption이 잘 생성됐는지 실제 텍스트를 비교하며 평가하는 UX"를 기대하고 있습니다.
- 현재 surface에는 arm별 실제 caption/alt text 후보를 나란히 비교하는 전용 섹션이 없습니다.

따라서 지금 시점에서는 구현을 더 밀기 전에, **이 surface가 최종적으로 무엇을 보여주고 어떤 방식으로 사람이 평가해야 하는지**를 Program Steward에게 다시 확인받는 것이 필요합니다.

## 2. Program Steward에게 재확인받고 싶은 요구사항
아래 항목들에 대해 우선순위와 기대 UX를 명시적으로 다시 확인 부탁드립니다.

1. 평가의 본문은 무엇입니까?
- A안: 기존 review markdown의 `Caption` / `Alt Text` 본문을 읽고 오른쪽 decision form에 판정만 입력하는 구조
- B안: `full_image_baseline`, `full_image_ocr_context_rerun` 등 arm별 실제 caption/alt text 후보를 surface 안에서 직접 비교하는 구조

2. 오른쪽 패널의 역할은 무엇입니까?
- decision metadata 입력 전용이어야 합니까?
- 아니면 후보 텍스트 비교 + 결정 입력을 동시에 포함해야 합니까?

3. 이번 Master Plan의 완료 기준에서 꼭 필요한 것은 무엇입니까?
- 10-image human evaluation을 실제로 끝내는 것
- arm별 caption quality comparison UX를 제공하는 것
- feedback ledger / decision seed writeback만 정확하면 되는 것
- 한국어/비개발자 친화 라벨로 운영 가능한 수준까지 포함하는 것

4. `decision-slides`와 `slide-preview`의 역할 분리는 유지합니까?
- 현재는 `decision-slides`가 human evaluation lane, `slide-preview`가 selection/writeback proof lane입니다.
- 이 분리를 유지할지, 아니면 하나의 평가 surface로 더 합칠지 확인이 필요합니다.

5. 모드별 후보 텍스트가 필요하다면, source of truth는 무엇입니까?
- 현재 bootstrap artifact에는 arm id / winner / selected arm 같은 metadata는 있으나, arm별 실제 caption/alt text 본문은 없습니다.
- 후보 텍스트 비교 UX가 요구사항이라면, bootstrap/session artifact contract 자체를 확장해야 합니다.

## 3. 현재까지 확인된 상태
### 이미 닫힌 범위
- `reviewSurface.openBootstrapEvaluationSession` command로 첫 10개 image evaluation session bootstrap 가능
- bootstrap session artifact 생성 가능
  - `session-config.json`
  - `review-surface-manifest.json`
  - `decision-seed.jsonl`
  - `feedback-ledger.json`
- `decision-slides` surface open 가능
- local image resolution 동작 가능
- stale-safe bounded writeback vertical slice는 `slide-preview` lane에서 별도로 검증됨
- reference packet 2종은 최신 상태에 맞게 정리됨

### 이번 실사용 확인에서 새로 드러난 점
- image preview는 현재 보입니다.
- 다만 현재 평가 UX는 "모드별 후보 텍스트를 직접 비교"하는 구조가 아니라, source markdown + metadata form 조합입니다.
- 따라서 이 상태를 그대로 final UX로 볼지, 아니면 candidate-text comparison section을 추가해야 하는지 요구사항 재확인이 필요합니다.

## 4. 제출 산출물
### A. 현재 상태/평가 문서
- `vscode-markdown-review-surface/control/project_domain/resources/references/REFERENCE_review_surface_progress_and_expert_evaluation_packet-at2026-04-08.md`
- `vscode-markdown-review-surface/control/project_domain/resources/references/REFERENCE_slide_preview_writeback_evaluation_packet-at2026-04-08.md`
- `my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_10_image_evaluation_runbook-at2026-04-09.md`
- `my-image-parser/control/project_domain/resources/reports/REPORT_phase2_review_surface_10_image_human_evaluation_template-at2026-04-09.md`

### B. 실제 10-image bootstrap session artifact
- source markdown:
  - `my-image-parser/control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.md`
- session dir:
  - `my-image-parser/control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.review-surface-session/phase2-caption-decision-slides-first-10`
- artifact files:
  - `session-config.json`
  - `review-surface-manifest.json`
  - `decision-seed.jsonl`
  - `feedback-ledger.json`

### C. 스크린샷 첨부 지점
아래 3장을 첨부해 주시면 현재 상태를 가장 빠르게 이해할 수 있습니다.
- Screenshot 1: `decision-slides` open 상태 전체 화면
  - 권장 파일명: `SCREENSHOT_01_decision_slides_open-at2026-04-09.png`
- Screenshot 2: 상단 hero image + 하단 decision form 배치가 보이는 화면
  - 권장 파일명: `SCREENSHOT_02_decision_slides_layout-at2026-04-09.png`
- Screenshot 3: source markdown과 surface를 같이 보여주는 split view
  - 권장 파일명: `SCREENSHOT_03_source_vs_surface_split-at2026-04-09.png`

## 5. 주요 코드 모듈
### bootstrap / open path
- `vscode-markdown-review-surface/src/decision/evaluation-session-bootstrap.js`
- `vscode-markdown-review-surface/src/extension.js`
- `vscode-markdown-review-surface/src/test/suite/evaluation-session-bootstrap.test.js`
- `vscode-markdown-review-surface/src/test/suite/smoke.test.js`

### decision-slides UI / data projection
- `vscode-markdown-review-surface/src/decision/slide-shell.js`
- `vscode-markdown-review-surface/src/decision/webview-html.js`
- `vscode-markdown-review-surface/src/decision/slide-decision-form.js`
- `vscode-markdown-review-surface/src/decision/slide-context.js`

### local image resolution / host document state
- `vscode-markdown-review-surface/src/decision/host-document-state.js`
- `vscode-markdown-review-surface/src/test/suite/host-document-state.test.js`

### slide-preview selection / writeback proof lane
- `vscode-markdown-review-surface/src/slides/slide-preview-runtime.js`
- `vscode-markdown-review-surface/src/slides/slide-preview-host-sync.js`
- `vscode-markdown-review-surface/src/slides/slide-preview-selection-runtime.js`
- `vscode-markdown-review-surface/src/slides/slide-preview-selection-binder.js`
- `vscode-markdown-review-surface/src/slides/slide-preview-navigation-binder.js`
- `vscode-markdown-review-surface/src/slides/slide-preview-writeback-binder.js`
- `vscode-markdown-review-surface/src/slides/slide-preview-linked-state.js`
- `vscode-markdown-review-surface/src/slides/slide-preview-bridge.js`
- `vscode-markdown-review-surface/src/slides/slide-source-snapshot.js`
- `vscode-markdown-review-surface/src/slides/slide-writeback-host.js`

### 관련 검증 파일
- `vscode-markdown-review-surface/src/test/suite/slide-preview-visual-hit-accuracy.test.js`
- `vscode-markdown-review-surface/src/test/suite/slide-preview-writeback-acceptance.test.js`
- `vscode-markdown-review-surface/src/test/suite/slide-preview-interaction-state.test.js`

## 6. 현재 판단
현재 surface는 다음 두 사실을 동시에 만족합니다.
- 구현/검증 측면에서는: 10-image bootstrap and open path가 실제로 동작하는 수준까지 올라왔습니다.
- UX 요구사항 측면에서는: 사용자가 기대하는 "mode별 caption text 비교 평가"가 현재 surface에 직접적으로 표현되지는 않습니다.

따라서 지금 필요한 것은 추가 구현을 무조건 진행하는 것이 아니라, **이 평가 surface의 최종 사용자 경험과 완료 기준을 다시 명확히 받는 것**입니다.

## 7. Steward에게 요청하는 응답 형식
아래 4개만 명확히 답해 주시면 다음 구현 우선순위를 바로 고정할 수 있습니다.
- `평가 본문`: source markdown reading vs arm-by-arm candidate comparison
- `필수 UX`: decision metadata form only vs candidate text comparison included
- `Master Plan 완료 기준`: 10-image run completion only vs comparison UX completion included
- `다음 구현 우선순위`: label readability / candidate-text section / artifact contract extension / cross-mode consolidation 중 무엇이 먼저인지

## 8. Steward Response 이후 다음 단계
Steward 답변으로 아래 순서가 고정되었다.

1. artifact contract extension
2. candidate-text comparison section
3. label readability / operator clarity
4. actual 10-image evaluation run
5. cross-mode consolidation

즉 더 이상 `현재 contract 유지 + immediate evaluation` 경로는 정답이 아니고, `artifact contract extension + comparison UX completion + then evaluation` 경로가 정답이다.
