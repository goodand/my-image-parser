# Slides-Grab Surface Adaptation Priority Note

## Purpose

`my-image-parser`의 주요 실험들에서 이제는 **이미지-캡션 평가 진행**이 시의성 우선순위가 되었다는 점을 고정한다.

이 note는 다음 결정을 다시 읽기 위한 user decision note다.

- 무엇을 지금 우선 구현할 것인가
- `slides-grab`을 어떤 역할로 활용할 것인가
- 무엇을 이번 phase의 비목표로 둘 것인가
- 상세 요구사항은 누가 제안하고, 구현은 어느 workspace에서 담당하는가

## Current Decision

현재 phase의 우선 구현 방향은 다음과 같다.

- `slides-grab`의 **bbox selection / annotated screenshot / structured selection prompt** 아이디어를 활용한다.
- 하지만 `slides-grab`을 그대로 제품 본체로 삼지 않는다.
- primary implementation host는 계속 **VS Code**다.
- 즉 구조는 다음과 같다.

`VS Code surface host + slides-grab donor UX/adaptation + manifest-driven evaluation flow`

## Why Now

현재 `my-image-parser`에서 urgency가 높은 것은 broad surface exploration이 아니라:

- 여러 이미지에 대한 비교 평가
- 특정 이미지의 특정 영역을 지시하고 검토
- baseline / winner / pending / decision reason을 사람이 빠르게 읽고 에이전트에게 명확히 지시하는 흐름

이다.

즉 지금 필요한 것은:

1. image review surface
2. region selection / pointing surface
3. decision capture surface

를 먼저 usable하게 만드는 것이다.

## Priority Framing

### First Axis: User Productivity

- Obsidian/PPT에서 유용했던 일부 surface 기능을 VS Code 안으로 가져온다.
- 목적은 사용자가 review / selection / decision 작업을 한 workspace 안에서 빠르게 수행하는 것이다.

### Second Axis: Agent Effectiveness

- 문서 검색, link resolution, context recall 같은 것은 adapter로 연결한다.
- 그러나 현재 긴급도는 document retrieval 확장보다 **image-caption evaluation surface**에 있다.

### Third Axis: Communication Clarity

- drag / bbox / 영역 지시는 사용자가 에이전트에게 “어디를 보라”를 명확히 전달하는 데 중요하다.
- 지금 phase에서 `slides-grab` 차용 가치가 가장 큰 이유도 여기에 있다.

## Role Boundary

### VS Code

- primary host
- same-page review surface
- source + rendered view
- selection / annotation UI
- decision capture UI

### slides-grab

- donor / adaptation source
- 특히 활용 가치가 큰 부분:
  - bbox selection UX
  - selection payload schema
  - annotated screenshot generation
  - structured prompt/context assembly

### Obsidian

- search / context / vault-intelligence adapter
- current phase의 primary build target은 아님

### Control-Plane Program Steward

- 상세 요구사항 owner
- 다음을 proposal로 내릴 역할:
  - 어떤 review card/row schema를 쓸지
  - 어떤 decision state를 canonical로 둘지
  - 어떤 selection payload를 machine truth로 저장할지
  - 어떤 비교 축이 현재 실험의 최소 단위인지

## Non-goals For This Phase

### State Non-goals

이번 phase에서는 다음 상태를 보장하려고 하지 않는다.

- Obsidian parity 전체 달성
- generalized PPT editing product 완성
- broad graph / dashboard / daily note system 완성
- 완전한 agent retrieval platform 완성

### Type Non-goals

이번 phase에서 직접 커버하지 않는 에러/문제 유형:

- Obsidian plugin host를 VS Code 안에서 직접 재현하는 문제
- `slides-grab` 전체 기능군을 우리 목적에 맞지 않게 통째로 제품화하는 문제
- broad document-search orchestration을 image-evaluation priority보다 먼저 푸는 문제

### Performance Non-goals

- Null: 지금은 과도한 general optimization이 목표가 아니다.
- Over: generic, beautiful, all-purpose editor로 확장하는 과최적화는 지양한다.
- Under: 현재는 image-caption evaluation workflow가 usable하면 되고, broad product polish 부족 자체를 당장 blocker로 보지 않는다.

## Practical Build Rule

지금은 `slides-grab`을 다음처럼 읽는다.

- adopt the interaction pattern
- adapt the payload contract
- reuse the strongest donor ideas
- do **not** treat the donor repo as the canonical runtime body

즉 구현 원칙은:

1. `slides-grab` donor repo는 reference/donor로 읽는다
2. 필요한 selection/annotation behavior만 harvest한다
3. canonical runtime body는 VS Code-centered surface에 둔다
4. evaluation machine truth는 manifest/schema로 고정한다

## Immediate Next-Step Contract

다음 단계에서 `Control-Plane Program Steward`가 제안해야 할 것은 상세 UI 그 자체보다 먼저:

- review unit
- selection unit
- decision unit
- state enum
- non-goal boundary

를 명시한 control-plane proposal이다.

그 다음 implementation workspace는 그 proposal을 기준으로 surface를 수정한다.

## Short Form

현재 시점의 한 줄 결정:

**우리는 broad surface exploration보다 image-caption evaluation을 우선하며, `slides-grab`은 VS Code-centered surface를 위한 donor/adaptation source로 활용한다.**
