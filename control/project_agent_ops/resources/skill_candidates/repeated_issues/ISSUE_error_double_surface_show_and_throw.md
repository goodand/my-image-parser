# Repeated Issue: Error Double-Surface (Show + Throw)

## Symptom

에러 핸들링이 사용자에게 `showErrorMessage`/`showWarningMessage`로 알림을 표시한 뒤 같은 에러를 다시 `throw`하여, 호출자의 에러 핸들러가 추가 알림을 표시. 사용자가 동일한 에러를 두 번 보게 됨.

## Current Proven Example

- `extension.js:325-332` (2026-04-08):
  ```js
  try {
    validatedSessionConfig = validateEvaluationSessionConfig(...);
  } catch (error) {
    void vscode.window.showErrorMessage(error.message);
    throw error;  // VS Code registerCommand 콜백이 이 throw를 잡으면 추가 알림
  }
  ```
- VS Code의 `registerCommand` 콜백에서 unhandled rejection이 발생하면 VS Code 자체가 에러 알림을 표시할 수 있음
- 수정: `throw error` → `return` (에러를 보여준 후 조용히 종료)

## Relationship To Existing Patterns

- `ISSUE_concurrency_guard_without_ux_feedback`의 대칭(inverse) 패턴
  - 기존: guard가 피드백 없이 조용히 return → 사용자가 왜 안 되는지 모름 (too little feedback)
  - 이번: 에러를 보여준 후 다시 throw → 사용자가 같은 에러를 두 번 봄 (too much feedback)
- 둘 다 "에러 경로에서의 UX 피드백 수량 불일치" 클래스

## Why This Matters

- 사용자가 같은 에러 메시지를 두 번 보면 "두 번 실패한 건가?" 혼란 유발
- VS Code extension에서 특히 흔함: command callback의 throw가 VS Code에 의해 별도 처리됨

## Guardrail

에러 핸들링에서 `showErrorMessage`와 `throw`를 같은 catch 블록에 두지 않기:
- 사용자에게 보여주고 끝낼 거면 `return`
- 호출자에게 전파할 거면 `throw`만 하고 호출자가 표시

## Escalation Trigger

또 다른 에러 핸들러가 `showErrorMessage` + `throw` 조합을 사용하여 사용자에게 이중 알림이 표시됨.

## Promotion Status

- standalone issue, 1 proven case
- `ISSUE_concurrency_guard_without_ux_feedback`와 함께 "error UX feedback quantity" skill로 흡수 가능
