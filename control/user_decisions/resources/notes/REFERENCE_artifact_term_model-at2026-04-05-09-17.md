# Artifact Term Model

## Purpose

Decision-support 문서와 surface를 만들 때 반복해서 쓰는 용어를 같은 뜻으로 다시 읽기 위한 reference.

## Core View

이 모델은 artifact를 다음 두 축으로 본다.

1. artifact type
2. role / state / tag

즉:

- `Manual`, `Reference`, `Template`, `Example`는 artifact type 쪽에 가깝다.
- `baseline`, `canonical`, `active`, `archived`, `legacy`는 role / state / tag 쪽에 가깝다.

## Artifact Type

### Manual

수행 중심의 상위 artifact 종류.

- 기능:
  - 수행을 돕는다
  - 다시 읽는다
  - 따라 한다
- 해석:
  - `Reference`, `Example`, `Template`를 포괄하는 상위 artifact로 볼 수 있다.

### Reference

lookup 중심의 manual subtype.

- 기능:
  - 찾기
  - 다른 artifact를 지시
  - 다시 읽기
- 용도:
  - 규칙
  - 설명
  - 구조
  - 사용법의 이해를 돕는다

정의:

> `Reference = 기능("찾기" + 어떠한 Artifact를 "지시" + 다시 읽기) + 용도("규칙, 설명, 구조, 사용법의 이해를 돕는")`

### Template

작성 중심의 manual subtype.

- 기능:
  - 복사
  - 다시 읽기
  - 채우기
- 용도:
  - 같은 구조의 새 artifact를 만들기 위한 틀

### Example

사례 중심의 manual subtype.

- 기능:
  - 보기
  - 비교하기
  - 추상 규칙을 concrete instance로 이해하기

subtype:

- `good-case`
- `bad-case`
- `worked example`

### Worked Example

process 표현이 포함된 example.

- 단순 example:
  - 입력과 출력만 보일 수 있다
- worked example:
  - 입력
  - 중간 단계
  - 판단 과정
  - 출력
    이 드러난다

즉:

> `worked = process 그 자체`라기보다, `process 표현을 포함한 example`

## Role / State / Tag

### baseline

`baseline`은 artifact type이라기보다 role / state / tag에 가깝다.

- 무엇이냐보다 무엇을 기준으로 비교하느냐에 붙는 태그
- “이게 어떤 용도로 쓰이는가?”를 보이게 하는 label
- 핵심:
  - 비교 기준
  - 판정 기준
  - 변화 측정 기준

더 정확히는:

> `baseline = 특정 context에서 비교와 판단의 기준 역할을 수행하는 기준점`

`baseline`은 일반적으로 “비교군”보다 더 넓다.

- 값 하나도 baseline일 수 있다
- 상태 snapshot도 baseline일 수 있다
- 정책도 baseline일 수 있다
- example도 baseline일 수 있다

종류:

- Value baseline
- Snapshot baseline
- Policy baseline
- Process baseline
- Artifact baseline

### canonical

공식 기준으로 채택된 상태를 가리킨다.

쉽게 말하면:

> 여러 후보 중에서 “이걸 공식 기준으로 쓰자”라고 채택된 것

### active

현재 효력이 살아 있고 실제로 사용 중인 상태.

### archived

과거 기록으로 보존하지만 현재 active truth는 아닌 상태.

### legacy

과거 구조나 과거 규칙에 속하지만 여전히 읽거나 참조할 수 있는 상태.

## Example Artifact Expression

아래 표현은 하나의 artifact를 type / subtype / tag / state로 동시에 읽는 예다.

```text
- (Artifact)type: Example
- (Artifact)subtype: Worked Example
- tags: canonical, baseline
- state: approved, active
```

문장으로 풀면:

> 이 artifact는 절차 표현이 포함된 예시이며, 공식 기준으로 채택되었고, 현재 승인되어 활성 상태에 있는 기준 예시다.

## Set Model

- `U` = 다시 읽는 모든 artifact 집합
- `C` = context
- `M ⊂ U` = Manual
- `R ⊂ M` = Reference
- `T ⊂ M` = Template
- `E ⊂ M` = Example

`baseline`은 위와 같은 type 집합과 조금 다르게 본다.

- `B_c ⊂ U`
- 여기서 `c`는 context

즉 `baseline`은 고정된 artifact family라기보다:

> 어떤 artifact가 특정 context에서 기준 역할을 수행하는 상태/태그

## Interpretation Notes

### Manual 과 Reference

`Manual` 전체를 `Reference`라고 부르지는 않는다.

하지만 `Reference`는 `Manual`의 부분집합으로 볼 수 있다.

- `Reference` = 조회형 manual
- `Template` = 작성형 manual
- `Example` = 사례형 manual

### baseline 과 anchor

이 문맥에서 `anchor`는 `지시체`보다 `기준점`에 가깝다.

혼동을 줄이려면 앞으로는 `anchor`보다 아래 표현을 우선한다.

- 기준점
- 비교 기준
- 기준 역할

### baseline 과 representative value

통계로 치면 평균이나 중앙값이 baseline이 될 수는 있다.

하지만 baseline의 핵심은 대표값 그 자체가 아니라:

- 비교 기준선
- 판정 기준

이라는 점이다.

즉:

> 대표값이 baseline일 수는 있지만, baseline은 대표값과 동의어는 아니다.

## Practical Rule

이 workspace에서 다음처럼 읽으면 된다.

- `Reference`
  - 찾아보는 지식
- `Manual`
  - 수행을 돕는 상위 artifact
- `Template`
  - 작성/복제를 위한 틀
- `Example`
  - 사례를 통한 이해 artifact
- `baseline`
  - 비교와 판정의 기준 역할을 수행하는 태그
