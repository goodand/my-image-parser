# Repeated Issue: Post-Delivery Test Assertion Weakness

## Symptom

Codex/subagent가 전달한 테스트가 모든 케이스를 통과하지만, assertion 전략이 약해서 regression 감지력이 부족하다. 테스트가 "통과"하더라도 실제 계약을 보호하지 못하는 상태.

## Weakness Patterns (4 sub-types)

1. **find() vs positional**: 순서 보존이 중요한 배열에서 `find()`로 요소를 찾아 검증 → 순서 뒤바뀜을 감지 못 함
2. **불완전 set coverage**: N개 항목 중 일부만 assert → 누락된 항목의 regression 미감지
3. **단일 필드 assertion**: 다중 필드 객체에서 한 필드만 assert → 나머지 필드 오염 미감지
4. **negative path 부재**: happy path만 테스트 → error path, null input, boundary condition 미보호

## Current Proven Examples

### 2026-04-08: evaluation-session-open.test.js

- 4개 테스트 모두 happy path, negative 0개
- `validateEvaluationSessionConfig(null)` → null 반환 분기 미테스트
- URI-like 객체 입력 시 `isUri` 분기 미테스트 (버그 있었으나 보호 안 됨)
- test #2가 반환 config 전체가 아닌 `image_order` 하나만 assert

### 2026-04-08: decision-slides-acceptance.test.js

- `persistedRows.find()` 사용 → JSONL 행 순서 보존 계약 미검증
- `image11.needs_row_update` assertion 누락 (3개 중 2개만 검증)
- temp cleanup이 assertion 뒤에 있어 실패 시 leak

### 2026-04-08: slide-parser.test.js

- `extractTitleAndImages` 단위 테스트 없음 (통합 테스트에서 간접만)
- frontmatter 음성 테스트 없음 (unclosed, empty, absent)
- HTML `<img>` 이미지 추출 테스트 없음
- 2-slide 분할만 검증, 5+ slide 연속성 미검증

## Why This Matters

- Codex/subagent는 "tests passing"을 성공 신호로 사용
- 약한 assertion은 false positive — 코드가 맞든 틀리든 통과
- 리뷰어가 assertion 약점을 발견하기 전까지 regression이 보호되지 않음

## Guardrail

Codex/subagent 테스트 delivery 후 4-point assertion review:
1. 순서 의존 배열은 positional assertion 사용했는가?
2. N개 항목 set은 전수 assert했는가?
3. 반환 객체의 핵심 필드 전부 assert했는가?
4. Negative path (null, invalid, boundary) 테스트가 있는가?

## Escalation Trigger

또 다른 Codex/subagent 테스트 delivery에서 위 4가지 중 2+ 패턴이 발견.

## Promotion Status

- standalone issue, not yet absorbed into a skill
- 7 instances across 3 test files in a single review session — strong signal
