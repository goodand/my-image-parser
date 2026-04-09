# Caption Experiment Readiness Checklist

> 목적: caption experiment를 시작하기 전에 자원, 규칙, 실행 경로가 닫혀 있는지 확인한다.
> source of truth: `KB_caption_experiment_foundation.md`와 `MASTER_PLAN_presentation_image_pipeline.md`

## A. Canonical Resources

- [ ] PPT 원본 2종이 `control/project_domain/resources/assets/caption_experiment/pptx/`에 있다
- [ ] 추출 이미지 2세트가 `control/project_domain/resources/assets/caption_experiment/extracted_media/`에 있다
- [ ] `caption_experiment_resource_index.json`이 존재한다

## B. Canonical Documents

- [ ] master plan이 1개만 존재한다
- [ ] caption experiment KB가 존재한다
- [ ] OpenAI caption runner spec가 존재한다
- [ ] full-image standalone OCR context-package baseline spec가 존재한다
- [ ] 실험에 필요한 draft 또는 reference가 current workspace 안에 있다

## C. Runnable Paths

- [ ] component isolation preprocessing path가 정의되어 있다
- [ ] object-level 실험을 할 경우 raw extracted-media를 그대로 다음 active arm으로 쓰지 않는다
- [ ] component isolation tool surface가 문서화되어 있다 (`ImageSorcery MCP`, image capture, or equivalent)
- [ ] 현재 PPT 자산에서는 `rembg`를 기본 경로로 쓰지 않는다는 판단이 문서화되어 있다
- [ ] `ImageSorcery MCP` 또는 capture surface를 먼저 검토한다
- [ ] OCR evidence extraction path가 정의되어 있다
- [ ] OCR evidence와 PPT-local summary를 묶는 context-package path가 정의되어 있다
- [ ] extracted media + OpenAI 경로는 simulator 없이 실행 가능하다
- [ ] screenshot 경로는 viewer surface가 정의된 경우에만 실행한다
- [ ] evaluation gate를 쓸 경우 decision state와 audit or error artifact를 남긴다
- [ ] unsupported media는 `unsupported_media_type`로 분기되고 manifest 또는 동등한 evidence를 남긴다

## D. Packet Readiness

- [ ] standard packet template이 존재한다
- [ ] canonical packet template이 존재한다
- [ ] issued packet은 표준 또는 canonical packet을 기반으로 발행한다
- [ ] parallel subagent 실행 전 issued packet마다 `locked_paths`가 있다
- [ ] parallel shard manifest가 unique `image_id`와 unique output ledger를 보장한다

## E. Evidence And Storage

- [ ] 실행 결과는 `runs/`에 저장한다
- [ ] reusable 기준 문서는 `resources/`에 저장한다
- [ ] registry JSON은 현재 경로와 상태를 반영한다
- [ ] project-local `.codex/config.toml`이 병렬 실험 thread cap을 고정한다
- [ ] phase-1 summary artifact가 존재하고 현재 baseline truth로 연결돼 있다
- [ ] 다음 phase 진입 전 active machine-readable artifact에서 hard lint fail이 새로 남아 있지 않다

## F. Phase Transition Gate

- [ ] component isolation이 필요한 실험이면 `phase0_object_isolation_manifest.jsonl` 또는 동등한 bounded smoke evidence가 존재한다
- [ ] raw extracted-media baseline을 comparison-only로 둘지, component isolation을 waive할지, isolation 후 rerun할지 결정이 기록되어 있다
- [ ] OCR evidence와 context package를 caption 입력에 넣을지 그 경계가 기록되어 있다
- [ ] `.emf` 등 unsupported media 사례가 설명 가능한 상태로 기록돼 있다
- [ ] legacy `phase1_caption_10w` packet 또는 ledger JSON은 cleanup, reclassification, or archive decision이 내려졌다

## Reference basis

- `/Users/jaehyuntak/Desktop/Project_____현재_진행중인/claude-gemini-communicator/skills/Skills-Create-Project/python-static-diagnostic-fixer/checklist-forconsistency-evaluation/consistency-checklist-at2026-03-17-01-18.md`
