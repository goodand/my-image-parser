# Repeated Task: Decision Contract Cross-Field Test Expansion

## Pattern Name

- decision contract validation rule 추가/변경 후 cross-field 테스트 확충

## Trigger

- `decision-contract.js`에 새 validation rule 추가 또는 기존 rule 변경
- cross-field constraint (e.g., `caption_decision='defer'` → `review_status='deferred'`) 추가
- `validateDecisionPatch()` 또는 `applyDecisionPatch()` 로직 변경

## Stable Steps

1. 새로 추가/변경된 rule 목록 확인
2. 각 rule에 대해 최소 3개 테스트 작성:
   - valid 경로 (rule을 만족하는 조합)
   - invalid 경로 (rule을 위반하는 조합)
   - 경계값 (null, undefined, 빈 문자열 등)
3. cross-field constraint는 양방향 테스트:
   - A가 B를 요구하는 경우: A는 있고 B가 없는 케이스
   - B가 A를 요구하는 경우: B는 있고 A가 없는 케이스
4. `buildDecisionRowTemplate()` 자기 일관성 테스트 유지 확인
5. patch validation도 동일 rule 커버리지 확인

## Candidate Promotion

- checklist: decision-contract rule 변경 시 테스트 확충 체크리스트
- script: rule 목록에서 테스트 skeleton 자동 생성
- promotion status: absorbed on 2026-04-07 into `claude-gemini-communicator/skills/Skills-Create-Project/async-migration-verify/checklist-forimplementation/async-migration-implementation-checklist.md`

## Promotion Trigger

- decision-contract에 새 cross-field rule이 추가될 때마다 동일 테스트 작성 패턴 반복
