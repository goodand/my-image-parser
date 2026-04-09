# VSCode OpenWith Bridge Experiment Results

## Status

Draft

## Purpose

`vscode.openWith(resource, viewId, { preview: false })`가 실제로 surface control plane으로 usable한지 검증한 결과를 정리한다.

Related artifacts:

- [NOTE_vscode_first_surface_model-at2026-03-29-01-04.md](./NOTE_vscode_first_surface_model-at2026-03-29-01-04.md)
- [CHECKLIST_vscode_surface_control_experiments-at2026-03-29-00-38.md](./CHECKLIST_vscode_surface_control_experiments-at2026-03-29-00-38.md)
- `<TMP_DIR>/vscode-openwith-bridge-experiment/`

## Experiment Setup

- development extension path: `<TMP_DIR>/vscode-openwith-bridge-experiment`
- validation workspace: `<TMP_DIR>/vscode_fabriqa_foam_validation`
- test target: `<TMP_DIR>/vscode_fabriqa_foam_validation/note_with_image_embed.md`
- command/API: `vscode.commands.executeCommand('vscode.openWith', target, viewId, { preview: false })`

## Result 1. Built-in Markdown Preview

- target viewId: `vscode.markdown.preview.editor`
- result file: `<TMP_DIR>/vscode-openwith-bridge-experiment/results/markdown-preview-result.json`
- verdict: `pass`

Observed facts:

- `commandError`: `null`
- post-state tab input: `TabInputCustom`
- `viewType`: `vscode.markdown.preview.editor`
- `heuristicSuccess`: `true`

Interpretation:

- built-in custom editor target에는 `vscode.openWith`가 의도대로 작동했다
- command/API layer 자체는 실제로 usable하다

## Result 2. Fabriqa Custom Editor

- target viewId: `fabriqa.markdownEditor`
- result file: `<TMP_DIR>/vscode-openwith-bridge-experiment/results/fabriqa-result-fresh.json`
- activated retry result: `<TMP_DIR>/vscode-openwith-bridge-experiment/results/fabriqa-result-activated.json`
- verdict: `fail` under current development-host conditions

Observed facts:

- `commandError`: `null`
- post-state tab input: `TabInputText`
- `heuristicSuccess`: `false`
- `fabriqaai.fabriqa-markdown-editor` contribution is visible in extension state
- 하지만 `vscode.openWith(..., 'fabriqa.markdownEditor', ...)` 호출 후에도 target file은 text tab으로 남았다

Interpretation:

- `vscode.openWith`는 built-in preview에는 잘 작동하지만, 현재 실험 조건에서는 third-party `fabriqa` custom editor target을 정확히 열지 못했다
- 최소한 현 시점에서는 `openWith bridge`가 `fabriqa`까지 완전히 대체한다고 말할 수 없다

## Practical Conclusion

1. command/API layer는 실제로 존재하고 built-in editor에는 usable하다
2. 따라서 `Interactive Decision Surface` 쪽 supporting artifact control에는 `openWith bridge`가 유효하다
3. 하지만 `Image Review Surface`를 `fabriqa`로 정확히 강제하는 용도로는 아직 불충분하다
4. 현재 `Image Review Surface`는 여전히 `editorAssociations`와 user-visible mode control이 더 현실적이다

## Decision Impact

- `Interactive Decision Surface`
  - `chat-led + artifact routing + built-in preview control` 방향은 유효
- `Image Review Surface`
  - `fabriqa`는 여전히 강력한 review surface지만, 현재 `openWith bridge`만으로 정확 제어된다고 보기는 어렵다
- 따라서 현재 control plane 전략은:
  - built-in preview류: `command/API layer` 활용
  - `fabriqa`: `settings layer`와 manual/reopen flow 병행

## Suggested Next Step

다음 실험은 둘 중 하나다.

1. `fabriqa` 쪽이 왜 `vscode.openWith` target으로 정확히 열리지 않는지 더 파고든다
2. 또는 decision surface에는 `openWith bridge`, review surface에는 `editorAssociations`를 채택하고 이원화 전략으로 굳힌다

현재로서는 `2`가 더 실용적이다.
