# Task Packet: Lean 02_1 System-First Portfolio Public Surface Packaging

## Agent

`Public Surface Architect`

## Goal

현재까지 확정된 `lean 02_1 system-first portfolio v1` 산출물을 reviewable public surface 기준으로 점검하고, 아직 미커밋 상태인 관련 산출물이 있으면 git commit까지 수행하라.

## Role Boundary

- public/review-facing artifact packaging만 담당
- control-plane 의미 변경 금지
- 산출물 내용 재해석 금지
- 새로운 설계 추가 금지
- commit 대상 선정, staging, commit message 작성, commit 수행만 담당

## In-Scope

- repo 내부 산출물만 다룬다
- 다음 후보 파일들의 git status 확인
- 변경 diff 검토
- 필요한 파일만 stage
- commit message 작성
- commit 수행

## Expected Candidate Files To Inspect

- `control/project_domain/resources/master_plans/drafts/PLAN_lean_ppt_image_character_portfolio_slice-at2026-04-11.md`
- `scripts/build_lean_02_1_system_first_portfolio.py`
- `scripts/render_lean_02_1_system_first_portfolio.py`
- `control/project_domain/resources/references/REFERENCE_lean_02_1_system_first_portfolio_review_index-at2026-04-13.md`
- `control/project_domain/resources/reports/REPORT_lean_02_1_system_first_portfolio_visual_qa-at2026-04-13-13-30.md`
- `control/project_domain/resources/manifests/lean_02_1_system_first_v1_image_role_matrix_at2026_04_11.json`
- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v1/lean_02_1_system_first_v1.pptx`
- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v1/render_sources/*`
- `control/project_domain/resources/assets/portfolio_drafts/lean_02_1_system_first_v1/renders/*`
- `control/project_domain/registry/domain_artifact_index.json` only if modified and safe to include

## Out-Of-Scope

- repo 밖 symbolic_links 경로
- 추가 문서 작성
- deck 내용 수정
- 이미지 교체
- branch 전략 변경
- push / PR 생성

## Required Checks Before Commit

- `git diff` 확인
- `domain_artifact_index.json` JSON 문법 확인
- deck 존재 확인
- render jpg 6개 존재 확인
- role matrix row 수 `6` 확인
- repo 밖 파일이 stage되지 않았는지 확인

## Commit Message Style

`feat: add lean 02_1 system-first portfolio v1 artifacts`

## Report Back

- staged file list
- validation result
- final commit sha
- 제외한 파일이 있으면 이유

## Safety Rule

If any file appears semantically risky, stop before commit and report instead of guessing.

## Empty-Commit Rule

If all `lean 02_1` portfolio artifacts are already committed, do not create an empty follow-up commit; report clean status instead.
