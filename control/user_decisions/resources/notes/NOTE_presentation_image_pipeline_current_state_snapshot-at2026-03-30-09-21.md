# Note: Presentation Image Pipeline Current State Snapshot

## Purpose

이 문서는 canonical master plan 본문을 대체하지 않는다.

역할은 다음 두 가지다.

- 현재 어디까지 왔는지 빠르게 읽게 하기
- 현재 병목과 다음 판단 지점을 decision-support surface로 분리하기

canonical contract와 phase flow는 계속:

- [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)

를 따른다.

## Current State

- `bounded 4-mode readiness` on `image11`: complete
- `phase1` small-batch `5-image` closure: complete
- corpus-wide `14-image` eligibility scan: complete
- full corpus execution and final arm-promotion decision: still open

## Stable Ready Subset

- `image7`
- `image8`
- `image9`
- `image10`
- `image11`

## Current Bottlenecks

### 1. Broader Corpus Artifact Gap

- stable subset 밖 이미지들은 frozen derived-arm artifact가 아직 충분히 닫히지 않았다
- 따라서 전체 corpus 기준 비교는 아직 execution-ready가 아니다

### 2. Mixed Chart-Table Edge Case

- `image4`는 mixed chart-table edge case로 남아 있다
- 이 이미지는 subset 기반 판단과 full-corpus 판단 사이의 대표적 차이점이다

### 3. Default Promotion Is Still Open

- `comparison winner`와 `default replacement`는 아직 같은 결정이 아니다
- 현재 baseline policy는 여전히 `full_image_baseline` 유지다

## Recommended Reading

1. [REFERENCE_master_plan_progress_dashboard-at2026-04-05-09-17.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/REFERENCE_master_plan_progress_dashboard-at2026-04-05-09-17.md)
2. [REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md)
3. [MASTER_PLAN_presentation_image_pipeline.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md)

## Practical Decision Point

지금 가장 현실적인 다음 판단은 둘 중 하나다.

- `stable 5-image subset`만으로 arm comparison verdict를 먼저 닫는다
- 전체 corpus coverage 자체가 중요하다면 missing derived-arm artifact를 더 채운 뒤 확장한다

현재 추천은:

- coverage 자체가 목적이 아니면 `stable 5-image subset`으로 먼저 판단을 닫는 것
