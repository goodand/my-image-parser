# Repeated Task: Async Migration Verification

## Pattern Name

- sync→async 전환 후 Expert 검증 체크포인트

## Trigger

- Codex 또는 개발자가 sync I/O를 async로 전환한 패치를 제출
- `readFileSync` / `writeFileSync` / `existsSync` → `fs.promises.*` / `await` 전환

## Stable Steps

1. **죽은 import 스캔**: 이전 API import(`const fs = require('fs')`)가 직접 호출 없이 남아 있는지 확인. 파생 전용(derivation-only)이면 직접 destructure로 교체
2. **중복 로직 식별**: sync/async 양쪽에 동일한 파싱/정규화/검증 블록이 복제되어 있는지 확인. 복제 발견 시 공통 pure helper로 추출
3. **동시 접근 보호**: async 전환된 함수를 호출하는 host 측에 concurrent call guard가 있는지 확인. guard가 있다면 UX 피드백(statusMessage, spinner)이 동반되는지 확인
4. **에러 경로 테스트**: async 전환된 경로에 대해 최소 2건의 에러 테스트 추가 — malformed input rejection + ENOENT/missing file handling
5. **TOCTOU 개선 확인**: sync 버전에 `existsSync → readFileSync` 같은 TOCTOU가 있었다면 async 버전에서 try-catch 패턴으로 해소됐는지 확인
6. **에러 메시지 품질**: catch 블록에서 파일 경로가 에러 메시지에 포함되는지 확인. 포함되지 않으면 `SyntaxError(`Invalid JSON in ${filePath}: ...`)` 식으로 보강

## Candidate Promotion

- checklist: `CHECKLIST_async_migration_verification.md` — sync→async 전환 시 6개 체크포인트
- script: grep 기반 dead import / duplication 자동 탐지
- promotion status: promoted on 2026-04-07 to `claude-gemini-communicator/skills/Skills-Create-Project/async-migration-verify`

## Promotion Trigger

- 동일 async 전환 검증 패턴이 다른 모듈이나 다른 repo에서 2회 이상 반복될 때

## Current Proven Evidence

- 2026-04-07 `decision-session-artifacts.js` async 전환 검증에서 6개 체크포인트 모두 해당:
  - 죽은 `fs` import 발견 → 제거
  - `readFeedbackLedger` / `readFeedbackLedgerAsync` 파싱 중복 → `parsePersistedFeedbackLedger` 추출
  - `onSaveDecisionFeedback` 동시 저장 guard 누락 → `feedbackSaveInFlight` + UX 피드백 추가
  - malformed JSON/JSONL rejection 테스트 2건 추가 (81 → 83 passing)
  - sync `existsSync` TOCTOU → async `catch ENOENT` 패턴으로 해소 확인
  - `parsePersistedFeedbackLedger`에 파일 경로 포함 에러 메시지 추가
