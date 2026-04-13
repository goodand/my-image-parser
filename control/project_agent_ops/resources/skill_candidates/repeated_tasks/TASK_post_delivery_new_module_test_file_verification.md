# Repeated Task: Post-Delivery New Module Test File Verification

## Recurrence Signal

Codex/subagent가 새 모듈(source file)을 생성할 때, 관련 모듈의 테스트 파일은 작성하지만 새 모듈 자체의 테스트 파일은 누락. 새 모듈의 핵심 기능이 통합 테스트에서 간접적으로만 검증됨.

## Current Manual Handling

새 모듈 delivery 후:
1. 새로 생성된 `.js` 파일 목록 확인
2. 각 파일에 대응하는 `*.test.js` 파일이 `test/suite/`에 존재하는지 확인
3. 없으면 핵심 export 함수에 대한 단위 테스트 파일 생성 요구

## Repeated Invariant

- Codex/subagent는 기존 테스트 파일을 확장하는 경향이 강하지만, 새 모듈의 독립 테스트 파일을 생성하는 경향은 약함
- 통합 테스트의 간접 커버리지는 개별 함수의 edge case와 error path를 보호하지 못함

## Current Proven Evidence

- On 2026-04-08, `slide-renderer.js` (121 lines, 6 exported functions)가 생성되었으나 `slide-renderer.test.js`는 존재하지 않음
- `slide-parser.test.js`는 동시에 생성됨 — parser는 테스트가 있지만 renderer는 없는 비대칭
- renderer의 핵심 기능 (`data-source-start-line` injection, `toSourceLineRange` conversion, `resolveSlideImages` mapping, mermaid fence handling) 전부 미검증
- 특히 `data-source-start-line`은 Phase 4 writeback의 전제인 visual→source mapping의 핵심

## Promotion Target

Codex/subagent delivery 후 새 모듈 test coverage 확인 체크리스트.

## Promotion Trigger

또 다른 새 모듈이 생성되었으나 대응 테스트 파일이 누락되고, 리뷰에서 발견.
