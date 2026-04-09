---
name: caption-experiment-foundation-kb
kb_profile: canonical_design_kb
role: presentation caption experiment foundation
ver: 1
created_at: 2026-03-27
updated_at: 2026-03-27
source_scope: my-image-parser workspace
purpose: PPT 2종과 추출 이미지 자산을 기준으로 caption generation experiment의 자원 경계와 실행 가정을 고정한다
---

# Caption Experiment Foundation KB

## Canonical design takeaways

1. 본 실험의 기준 자원은 PPT 원본 2종과 해당 PPT에서 추출된 이미지 세트다.
2. 자원 alias와 삭제 방지 정책의 source of truth는 `caption_experiment_resource_index.json`이다.
3. 실험 흐름의 source of truth는 `MASTER_PLAN_presentation_image_pipeline.md`다.
4. raw extracted-media baseline은 비교용으로 유효하지만, object-level 실험으로 진행하려면 component isolation, OCR evidence, context-package 전처리가 선행되어야 한다.
5. 현재 PPT 추출 자산은 이미 투명 배경을 가진 경우가 많으므로 rembg-style background removal은 기본 경로로 채택하지 않는다.
6. component isolation의 기본 경로는 ImageSorcery MCP와 image capture surface다.
7. OCR evidence와 PPT-local summary는 API caption 생성 전 context package로 묶어 주입하는 것이 다음 활성 실험 방향이다.
8. OpenAI caption on extracted media는 simulator 없이 실행 가능하다.
9. slide screenshot 계열 실험은 별도 viewer surface 또는 screenshot source가 필요하다.
10. 실험 결과는 `runs/`에 저장하고, 재사용 가능한 기준 문서는 `resources/`에 둔다.

## Canonical experiment resources

- PPT 원본:
  - `<LOCAL_CAPTION_EXPERIMENT_ASSET_ROOT>/pptx/full_presentation_2026-03-17.pptx`
  - `<LOCAL_CAPTION_EXPERIMENT_ASSET_ROOT>/pptx/탁재현(자기소개서)-최신 (1).pptx`
- 추출 이미지 세트:
  - `<LOCAL_CAPTION_EXPERIMENT_ASSET_ROOT>/extracted_media/01_full_presentation_2026-03-17`
  - `<LOCAL_CAPTION_EXPERIMENT_ASSET_ROOT>/extracted_media/02_1`
- 자원 인덱스:
  - `<LOCAL_DOMAIN_REGISTRY>/caption_experiment_resource_index.json`

## Core experiment arms

| Arm | Input surface | Purpose |
|---|---|---|
| Component isolation preprocessing | PPT 내부 추출 이미지 | component-level 실험을 위한 crop/mask/manifest 생성 |
| OCR + context package | isolated or captured component | OCR evidence와 PPT summary를 caption 입력용 context로 정리 |
| Extracted media + OpenAI | PPT 내부 추출 이미지 | raw slide-media baseline 생성 |
| Component-isolated + context-enriched caption | isolated or captured component | object-level caption baseline 생성 |
| Screenshot + caption | slide screenshot | viewer surface 기준 캡션 비교 |
| Evaluation path | cv-mcp / judge / review | accept or rewrite or audit 판단 |
| Comparison | multi-arm 비교 | arm 간 품질 차이 측정 |

## Source-of-truth rule

- 실험 자원 경로: `caption_experiment_resource_index.json`
- 파이프라인 흐름: `MASTER_PLAN_presentation_image_pipeline.md`
- OpenAI caption 실행 규격: `SPEC_openai_image_caption_runner.md`
- 교차검증 입력과 산출물: `control/project_domain/resources/`

## Simplification boundary

| Item | Current boundary | Expand when |
|---|---|---|
| Reference | draft도 reference 대체 가능 | 별도 canonical reference가 꼭 필요할 때 |
| Component isolation | next preprocessing prerequisite | bounded smoke에서 crop/OCR/context quality가 검증될 때 |
| Screenshot path | optional experiment arm | viewer surface가 확정될 때 |
| Caption judge | optional evaluation overlay | judge 경로를 canonical main flow로 승격할 때 |

## Not part of this KB

- 개별 arm의 세부 prompt 설계
- 최종 human approval 결과 자체
- 외부 workspace 문서의 직접 복제

## Reference basis

- `<EXTERNAL_TEMPLATE_ROOT>/template/knowledge_base.md`
- `<EXTERNAL_SKILLS_ROOT>/agent-tool-benchmark/knowledge_bases/agent-tool-benchmark-kb-at2026-03-24.md`
