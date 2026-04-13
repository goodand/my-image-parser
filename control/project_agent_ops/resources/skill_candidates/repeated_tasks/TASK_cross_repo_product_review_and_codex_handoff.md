# Repeated Task: Cross-Repo Product Review And Codex Handoff

## Pattern Name

- cross-repo product review → finding handoff → Codex fix → verification

## Trigger

- a downstream surface repo (e.g., `vscode-markdown-review-surface`) reaches a milestone
- the surface is consumed by `my-image-parser` and needs quality validation before integration
- the user requests a product review from the expert agent (Claude)

## Stable Steps

1. **의도 파악**: 제품 정의, 사용자 워크플로우, surface 모드, data contract 계층 확인
2. **파일 분류**: Host/Entry, Data Contract, Slide Seams, Webview/Render, Host State, Tests로 분류
3. **심층 읽기**: 모듈별 line-by-line 리뷰, public API, data shape, cross-module 연결 검증
4. **문제 분류**: Critical / Major / Minor로 발견 사항 분류, 우선순위순 권장 조치 작성
5. **Codex 핸드오프**: 발견 사항을 Codex에게 전달, 수정 요청
6. **수정 검증**: Codex 수정 결과를 line-by-line으로 재검증, 잔여 항목을 checklist에 기록
7. **반복 패턴 기록**: 리뷰 중 발견된 반복 issue/task를 `repeated_issues/`, `repeated_tasks/`에 기록

## Candidate Promotion

- checklist: `CHECKLIST_cross_repo_product_review.md` — 리뷰 전 준비사항 + 리뷰 관점 + 핸드오프 포맷
- skill: `cross-repo-product-review` — 파일 분류 자동화 + 리뷰 관점 프롬프트 생성
- promotion status: promoted on 2026-04-07 to `claude-gemini-communicator/skills/Skills-Create-Project/cross-repo-product-review`

## Multi-Round Convergence Pattern (2026-04-07 보강)

단일 핸드오프로 끝나지 않는 경우의 반복 패턴:

1. **1차**: Expert(Claude) 리뷰 → 3C + 5M + 7m 발견 → Codex 핸드오프
2. **2차**: Codex 12건 수정 → Expert 재검증 → 3건 잔여 우려(innerHTML escape, spread collision, webpack 설정) → checklist 기록
3. **3차**: Codex 3건 수정 → Expert 재검증 → 1건 실질 버그(`node:` prefix 누락) + 1건 코드 스멜(이중 null 방어) → Expert가 직접 수정
4. **4차**: Codex async 전환 → Expert 재검증 → 죽은 import, sync/async 중복, 동시성 가드 미비, 에러 경로 테스트 부재 → Expert가 4건 직접 수정
5. **수렴**: build + check + test 전부 통과 (83 passing) → checklist 전항목 resolved

관찰된 불변량:
- Codex 패치는 지적된 항목만 수정하는 경향이 있다 — 같은 구조적 클래스의 형제 필드를 놓칠 수 있음 (`ISSUE_partial_structural_fix_same_class_different_fields.md`)
- 3차 이후 Expert가 직접 수정하는 것이 효율적이었음 — 잔여 항목이 1-2건이면 핸드오프 비용이 직접 수정 비용을 초과
- 매 라운드의 발견 건수: 15건 → 3건 → 2건 → 4건(async 전환 부산물) — async 전환 같은 API surface 변경은 새로운 이슈 카테고리를 유입시킴
- async 전환은 기능 등가성 이상의 검증이 필요함 — 죽은 import, 중복 로직, 동시성 보호, 에러 경로가 새로운 체크포인트 (`TASK_async_migration_verification.md`)

## Promotion Trigger

- 동일 패턴이 `vscode-markdown-review-surface` 또는 다른 surface repo에서 2회 이상 반복될 때
