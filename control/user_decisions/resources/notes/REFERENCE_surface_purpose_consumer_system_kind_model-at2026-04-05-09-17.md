# Surface Purpose / Consumer / System Kind Model

## Purpose

이 문서는 decision-and-execution support workspace에서 `surface`, `layer`, `adapter`를 다시 읽을 때,
상위 목적과 소비 주체를 먼저 두고 해석하기 위한 reference다.

여기서 `decision-and-execution`은:

- 결정 자체
- 결정의 실행 계약화
- 수행 지원
- 운영과 재검토

까지를 함께 다룬다는 뜻이다.

핵심 문제의식은 다음과 같다.

- 기존 `surface` 후보들을 나열하면, 어떤 것은 사용자-facing 용도이고, 어떤 것은 내부 기능이며, 어떤 것은 외부 adapter였다.
- 따라서 단순 기능 나열은 MECE하지 않다.
- 먼저 `왜 존재하는가`, `누가 보는가`, `무슨 종류의 시스템인가`를 분리해야 한다.

## Core View

이 모델은 다음 순서로 읽는다.

1. `Purpose`
2. `Consumer`
3. `System Kind`
4. 필요하면 그 아래에 세부 surface / layer / adapter / artifact를 둔다.

즉:

- 최상위에는 사용자 의도와 상위 목적 축이 있다.
- `Surface / Layer / Adapter`는 그 아래의 구현 분류다.
- 여기에 포함되지 않는 중요한 예외로 `Workflow / Protocol`, `Artifact / Truth`, `Host / Runtime`가 있다.

---

## 1. Purpose

최상위 목적 축.

### 1.1 User Productivity

사용자가 하나의 작업공간 안에서 더 빨리 읽고, 고치고, 비교하고, 승인하게 한다.

예:

- Obsidian의 일부 문서 탐색/링크 기능을 VS Code로 가져오기
- PPT식 특정 영역 지시를 VS Code surface에서 재사용하기
- same-page review + edit + compare 흐름을 줄이기

### 1.2 Agent Effectiveness

에이전트가 문서와 artifact를 더 정확히 검색하고, 더 좋은 컨텍스트를 조립하고,
더 정확한 판단 재료를 얻도록 한다.

예:

- Obsidian Search 연동
- link resolution / context recall
- structured region manifest
- OCR / caption / grounding 결과를 agent-facing truth로 제공

### 1.3 Communication Clarity

사용자와 에이전트가 `무엇을 보고`, `어디를 가리키며`, `무엇을 바꾸는지`를 더 명확하게 소통한다.

예:

- drag / bbox / click / point / selection
- ambiguous 대상 disambiguation
- pending / accept / rerun 상태를 표면화

---

## 2. Consumer

어떤 주체가 그 projection을 읽고 판단하는가.

### 2.1 User-facing

사용자가 직접 보고 조작하는 surface.

예:

- markdown review surface
- image review surface
- decision surface

### 2.2 Agent-facing

에이전트가 읽고 판단하는 surface.

예:

- screenshot capture
- annotated screenshot
- OCR summary
- region manifest
- DOM snapshot
- rendered HTML preview snapshot

즉:

> 에이전트가 capture 이미지를 보며 frontend를 최적화하는 것도 `surface`다.
> 다만 `agent-facing observation surface`로 읽어야 한다.

### 2.3 Shared

사용자와 에이전트가 둘 다 참조하는 shared projection.

예:

- review markdown
- decision cards
- selection labels
- manifest 일부 projection

---

## 3. System Kind

이제 실제 시스템 종류를 나눈다.

### 3.1 Surface

어떤 주체가 직접 읽고 판단하도록 만든 projection.

중요:

- `Surface`는 사용자 전용이 아니다.
- 사용자-facing일 수도 있고, agent-facing일 수도 있다.

#### Surface subtype by interaction mode

##### Interactive Surface

직접 조작 가능한 surface.

예:

- edit
- drag
- click
- approve / reject / rerun

##### Observation Surface

읽고 판단하기 위한 surface.

예:

- rendered preview
- screenshot
- annotated crop
- mermaid rendered view

##### Coordination Surface

사용자와 에이전트 사이의 공동 판단 / 지시 surface.

예:

- review markdown
- decision table
- selection overlay
- human-facing projection of manifest

### 3.2 Layer

내부 기능층.

예:

- machine truth handling
- selection logic
- intelligence / grounding
- sync
- indexing
- rendering internals

### 3.3 Adapter

외부 시스템이나 능력을 현재 workspace에 연결하는 층.

예:

- Obsidian CLI / API
- CV / VLM model
- donor repo capability
- third-party search engine

---

## 4. Missing Categories Beyond Surface / Layer / Adapter

`Surface / Layer / Adapter`만으로는 충분하지 않다.

### 4.1 Workflow / Protocol

이건 surface도, layer도, adapter도 아니다.

이건:

- 어떤 순서로 진행되는가
- 어떤 상태 전이가 있는가
- 승인 / 보류 / 재실행 규칙이 무엇인가

를 다룬다.

예:

- compare -> decide -> promote
- approve / reject / pending
- rerun / confirm / accept
- human-in-the-loop review

즉:

> `Interactive Decision Surface`의 핵심은 화면 모양보다도 decision protocol에 있다.

### 4.2 Artifact / Truth

이것도 별도다.

이건:

- 무엇이 canonical truth인가
- 무엇이 projection인가
- 무엇이 runtime-only state인가

를 다룬다.

예:

- markdown
- manifest
- sidecar
- registry
- report
- bundle

즉:

- `Surface`는 artifact를 보여주는 projection일 수 있다.
- 하지만 artifact 자체는 별도 축이다.

### 4.3 Host / Runtime

실행 환경과 runtime plane.

예:

- VS Code
- Obsidian desktop
- browser editor
- CLI
- local server

구분:

- `Adapter` = 외부 능력을 연결하는 것
- `Host / Runtime` = 실제로 실행되는 환경

---

## 5. Why The Earlier 1-9 List Was Not MECE

초기 surface 나열은 다음 문제가 있었다.

1. 서로 다른 레벨이 섞였다.
   - 어떤 것은 user-facing surface였다.
   - 어떤 것은 feature였다.
   - 어떤 것은 scale variant였다.
   - 어떤 것은 adapter였다.

2. 특수화 관계가 섞였다.
   - `Region Evaluation Surface`와 `Component Separation Surface`는 별개의 peer라기보다 downstream specialization 관계다.

3. 범위 차이가 섞였다.
   - `Image Review Surface`와 `Multi-Image Evaluation Surface`는 본질적으로 같은 family의 scope variant다.

4. surface가 아닌 것이 섞였다.
   - `Obsidian Search/Context Surface`는 surface라기보다 adapter/capability로 보는 것이 맞다.

즉:

> 기존 1-9는 `surface / feature / specialization / adapter / scope variant`가 섞여 있어 MECE하지 않았다.

---

## 6. Normalized User-Facing Surface Families

이제 실제 user-facing surface를 큰 family로 줄이면 다음이 더 적절하다.

### 6.1 Document Review Surface

문서, note, markdown, backlink, mermaid, same-page edit/review를 다루는 surface family.

포함 예:

- markdown review surface
- backlink subview
- mermaid structural interaction

### 6.2 Visual Review Surface

이미지, 슬라이드, screenshot, crop, 비교 카드 같은 시각 중심 review surface family.

포함 예:

- image review surface
- multi-image evaluation surface
- single-image compare card

### 6.3 Selection / Annotation Surface

사용자가 특정 대상 또는 영역을 더 구체적으로 지시하기 위한 surface family.

포함 예:

- bbox drag
- point / click selection
- candidate disambiguation
- region labeling

### 6.4 Decision Surface

사람이 승인, 보류, 재실행, promote 같은 판단을 내리는 surface family.

포함 예:

- approve / reject / pending
- winner vs default separation
- promotion state capture
- why-default-stays-default

---

## 7. Practical Mapping To Current Goals

### Goal A. Bring Obsidian / PPT-like capabilities into VS Code

상위 목적:

- `User Productivity`

주로 관련되는 것:

- `User-facing Surface`
- `Interactive Surface`
- `Selection / Annotation Surface`
- `Decision Surface`

예:

- backlinks
- wikilinks
- same-page review/edit
- bbox/drag-based pointing

### Goal B. Improve Agent Document Search / Retrieval

상위 목적:

- `Agent Effectiveness`

주로 관련되는 것:

- `Adapter`
- `Layer`
- `Artifact / Truth`

예:

- Obsidian Search
- vault context recall
- manifest-driven retrieval

### Goal C. Let User Instruct The Agent More Precisely

상위 목적:

- `Communication Clarity`

주로 관련되는 것:

- `Selection / Annotation Surface`
- `Shared Surface`
- `Workflow / Protocol`

예:

- drag to point at a region
- choose target candidate from a selected area
- mark pending / accepted / rerun explicitly

---

## 8. Compact Model

```text
Purpose
├─ User Productivity
├─ Agent Effectiveness
└─ Communication Clarity

Consumer
├─ User-facing
├─ Agent-facing
└─ Shared

System Kind
├─ Surface
├─ Layer
├─ Adapter
├─ Workflow / Protocol
├─ Artifact / Truth
└─ Host / Runtime
```

이 모델을 우선 적용한 뒤, 각 purpose 아래에서 필요한 surface family를 다시 배치한다.

---

## 9. Interpretation Rule

이 workspace에서 새로운 후보를 볼 때는 다음 순서로 읽는다.

1. 이것은 어떤 상위 목적을 위해 존재하는가?
2. 누가 이 projection을 소비하는가?
3. 이것은 surface인가, layer인가, adapter인가?
4. 아니라면 workflow / artifact / host 중 무엇인가?
5. 기존 surface family 안으로 흡수 가능한가, 아니면 truly new family인가?

이 순서를 거치면:

- 기능 나열식 분류 drift
- surface와 adapter의 혼동
- 범위 차이를 새로운 종류로 오해하는 문제

를 줄일 수 있다.

---

## 10. Current Non-Goals

### 10.1 Definition

`Non-goals`는 이번 결정의 책임 범위 밖임을 명시하여 미래의 논쟁을 차단하는 장치다.

즉:

- 지금 해결하지 않는 범위를 고정한다.
- 그 범위를 `실패`로 오독하지 않게 한다.
- 부작용은 인지하되, 이번 결정의 최적화 대상과 분리한다.

### 10.2 What Non-goals Are Not

비목표는 다음과 동일하지 않다.

- 실패 상태
- 무시해도 되는 문제
- 중요하지 않은 side-effect

즉:

> 비목표는 `이번 책임 범위 밖`이라는 뜻이지, `존재하지 않는 문제`라는 뜻이 아니다.

### 10.3 Practical Criteria For Setting Non-goals

비목표를 정할 때는 최소한 다음 네 기준을 본다.

#### 4. Responsibility Boundary

타 팀, 타 프로젝트, 타 host의 결정이 필요한가?

#### 5. Solution Unit Boundary

현재 solution 구조를 깨지 않고 해결 가능한가?

#### 6. Trade-off Boundary

이 항목을 포함하면 이번 의사결정 자체가 멈추거나, scope가 비정상적으로 커지는가?

#### 7. Side-effect Management Boundary

부작용은 인지하지만, 이번 라운드의 최적화 대상에서는 제외하는가?

### 10.4 Non-goal Cases

#### Case: State

이번 결정이 보장하지 않는 상태의 상한선을 고정한다.

예:

- 특정 host 밖에서 동일 UX를 보장하지 않음
- 특정 adapter가 연결되지 않은 상태까지 지원하지 않음

#### Case: Type

설계적으로 커버하지 않는 error type 또는 product family를 명시한다.

예:

- Obsidian plugin ecosystem 전체 복제
- PPT editor 전체 재구현

#### Case: Performance

기대치를 관리하는 non-goal.

##### Null

이번 라운드에서 성능 목표를 별도로 두지 않는다.

##### Over

과도한 최적화를 목표로 삼지 않는다.

##### Under

최소 기준 미달을 지금 라운드의 blocker로 삼지 않는다.

### 10.5 Current Phase Non-goals

현재 phase에서의 비목표는 다음과 같다.

- VS Code 바깥에서 별도의 primary host를 새로 만들지 않는다.
- Obsidian 자체를 주 host/editor로 다시 삼지 않는다.
- `slides-grab`를 독립 제품으로 확장하지 않는다.
- Obsidian plugin ecosystem 전체를 VS Code 안으로 복제하지 않는다.
- PPT / slide 편집기 전체를 새로 만들지 않는다.
- graph view, timeline, daily note 같은 lateral expansion을 먼저 하지 않는다.
- surface family를 늘리는 것보다 현재 목적 축에 직접 기여하는 기능을 우선한다.

즉 현재의 focus는:

> `VS Code` 안에서 작업하고,
> `VS Code`와 연결할 수 있는 기존 프로그램인 `slides-grab`, `Obsidian`을 활용하여
> 사용자 생산성, 에이전트 효과성, 사용자-에이전트 소통 명확성을 높이는 것이다.

---

## 11. Current Role Boundary

### 11.1 VS Code

현재의 primary host / primary work surface.

역할:

- 문서 읽기/쓰기의 중심 workspace
- same-page review / edit surface
- selection / annotation / decision interaction의 중심
- human-facing + agent-facing projection이 만나는 곳

즉:

> 현재는 `VS Code`가 중심 host다.

### 11.2 slides-grab

`slides-grab`는 primary host가 아니라, 연결 가능한 기존 프로그램이자 donor/adapter다.

역할:

- bbox selection UX donor
- selection payload / annotated screenshot / prompt-assembly 참고 구현
- region 지시와 시각적 grounding을 위한 reusable capability source

비역할:

- 현재 workspace의 primary editor host 아님
- primary truth store 아님

### 11.3 Obsidian

`Obsidian`도 primary host가 아니라, 연결 가능한 기존 프로그램이자 search/context adapter다.

역할:

- vault search
- linkpath / context recall
- document retrieval fidelity 향상
- note graph semantics의 참고 모델

비역할:

- 현재 workspace의 primary editing host 아님
- VS Code surface를 대체하는 제품 본체 아님

### 11.4 Surface / Adapter 경계

현재 경계는 다음처럼 읽는다.

- `VS Code` = host + surface 실행 중심
- `slides-grab` = visual selection / prompt structuring donor-adapter
- `Obsidian` = document search / context adapter

즉:

- surface의 본체는 `VS Code` 안에 만든다.
- `slides-grab`와 `Obsidian`은 기존 능력을 연결해 쓰는 쪽이다.
- 따라서 이 둘은 `Surface`라기보다 현재 맥락에서는 `Adapter` 또는 `Donor Capability`에 더 가깝다.

---

## 12. Practical Reading Rule For This Phase

현재 phase에서는 새로운 후보를 보았을 때 먼저 이렇게 읽는다.

1. 이것이 `VS Code` 안의 primary surface를 강화하는가?
2. 아니면 `slides-grab` / `Obsidian` 같은 기존 프로그램의 능력을 adapter로 끌어오는가?
3. 두 경우가 아니라면, 지금의 상위 목적 축에 직접 기여하는가?
4. 아니라면 현재 phase에서는 deferred candidate로 본다.

이 규칙을 쓰면:

- host와 adapter의 경계가 흐려지는 문제
- donor repo를 제품 본체처럼 오해하는 문제
- surface family를 과도하게 늘리는 문제

를 줄일 수 있다.
