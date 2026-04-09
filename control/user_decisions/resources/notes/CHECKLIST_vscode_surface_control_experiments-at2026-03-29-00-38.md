# Checklist: VSCode Surface Control Experiments

## Status

Draft

## Purpose

이 체크리스트는 `VSCode-first surface model`을 실제 제어 가능한 운영 모델로 검증하기 위한 실험 단위를 정리한다.

핵심 질문은 다음이다.

- 이미지 평가용 surface와 의사결정용 surface를 분리할 수 있는가
- 그 분리를 VS Code CLI와 workspace settings 수준에서 재현 가능하게 만들 수 있는가
- 완전 통합 editor가 아니라 `surface control plane`으로 운영할 수 있는가

Related artifacts:

- [NOTE_vscode_first_surface_model-at2026-03-29-01-04.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/NOTE_vscode_first_surface_model-at2026-03-29-01-04.md)
- [CHECKLIST_fabriqa_foam_integration_validation-at2026-03-28-14-17.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/user_decisions/resources/notes/CHECKLIST_fabriqa_foam_integration_validation-at2026-03-28-14-17.md)
- [vscode-fabriqa-foam-workflow/SKILL.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/skills/vscode-fabriqa-foam-workflow/SKILL.md)
- `/tmp/vscode-openwith-bridge-experiment/`

## Current Baseline

이미 확인된 baseline:

- `fabriqa` same-page image render: pass
- Foam `Connections` / backlinks: pass
- rename sync after note rename: pass
- `[[wikilink]]` autocomplete in `Text Editor`: pass
- `[[wikilink]]` autocomplete in `fabriqa`: fail
- `Foam: Update Wikilink Definitions` in `Text Editor`: pass
- `Foam: Update Wikilink Definitions` with `fabriqa` active: fail

즉 baseline 결론은:

- `Image Review Surface`는 `fabriqa`가 담당
- `Interactive Decision Surface`, `Instant Memory`, `Prompt Reference`는 `Text Editor`가 담당
- Foam은 navigation shell

## Experiment Rule

각 실험은 다음 형식으로 판정한다.

- `pass`
- `partial`
- `fail`

기록할 것:

- exact command
- workspace path
- active profile
- active extensions
- expected behavior
- observed behavior
- blocker or manual step

## Module 1. Review Profile Module

### Goal

이미지 평가용 surface를 review 전용 profile로 고정할 수 있는지 확인한다.

### Target

- `Image Review Surface`
- image-heavy markdown dossier
- preferred editor: `fabriqa`

### Checks

1. `code --profile <review-profile>`로 workspace를 열 수 있는가
2. review profile에서 `fabriqa`가 기본 markdown editor로 유지되는가
3. 이미지가 많은 문서가 one-document surface로 usable한가
4. same-page image render가 profile 분리 후에도 유지되는가

### Candidate commands

```bash
code --profile "review-surface" --new-window /path/to/workspace
```

```bash
python3 skills/vscode-fabriqa-foam-workflow/scripts/switch_vscode_markdown_mode.py \
  --workspace /path/to/workspace \
  --mode fabriqa
```

### Pass criteria

- review profile을 명시적으로 열 수 있다
- `fabriqa` 기반 image review가 안정적으로 유지된다
- decision/prompt memory용 설정과 섞이지 않는다

## Module 2. Decision Profile Module

### Goal

질문 기반 decision artifact를 다루는 surface를 decision 전용 profile로 고정할 수 있는지 확인한다.

### Target

- `Interactive Decision Surface`
- `Instant Memory Task Sequence Surface`
- `Prompt Reference Surface`
- preferred editor: `Text Editor`

### Checks

1. `code --profile <decision-profile>`로 workspace를 열 수 있는가
2. `Text Editor`가 기본 markdown surface로 유지되는가
3. `Foam: Update Wikilink Definitions`가 안정적으로 실행되는가
4. backlink / prompt reference / task sequence 문서가 같은 profile 안에서 작동하는가

### Candidate commands

```bash
code --profile "decision-surface" --new-window /path/to/workspace
```

```bash
python3 skills/vscode-fabriqa-foam-workflow/scripts/switch_vscode_markdown_mode.py \
  --workspace /path/to/workspace \
  --mode text
```

### Pass criteria

- decision profile에서 wikilink authoring과 Foam command가 안정적이다
- review profile과 설정 충돌 없이 분리된다

## Module 3. Window Routing Module

### Goal

chat에서 특정 artifact를 열 때, 원하는 창/탭/문서 위치로 routing할 수 있는지 확인한다.

### Target

- new window vs reuse window
- target file open
- file focus and workspace focus

### Checks

1. `code -n`과 `code -r` 차이가 surface 분리에 유효한가
2. `code -g <file>`가 적절한 target routing으로 충분한가
3. review artifact와 decision artifact를 다른 창으로 나눌 수 있는가

### Candidate commands

```bash
code --profile "review-surface" --new-window /path/to/workspace
code --profile "decision-surface" --new-window /path/to/workspace
```

```bash
code --reuse-window -g /path/to/workspace/review.md
code --reuse-window -g /path/to/workspace/decision.md
```

### Pass criteria

- review용 창과 decision용 창을 의도적으로 분리할 수 있다
- artifact opening이 사용자에게 예측 가능하다

## Module 4. URL Launch Module

### Goal

chat 또는 외부 script가 `vscode://...` URI를 통해 artifact와 설정 화면을 여는 방식이 실용적인지 확인한다.

### Checks

1. `vscode://file/...`가 target markdown를 직접 여는가
2. `vscode://settings/...`가 필요한 설정 진입점으로 이동하는가
3. chat-led decision surface에서 supporting artifact를 여는 용도로 충분한가

### Candidate commands

```bash
open "vscode://file/ABSOLUTE/PATH/TO/review.md"
```

```bash
open "vscode://settings/workbench.editorAssociations"
```

### Pass criteria

- artifact jump가 빠르다
- 사용자 설명 비용이 낮다
- chat에서 artifact를 여는 control hook으로 쓸 수 있다

## Module 5. Extension Isolation Module

### Goal

surface별로 꼭 필요한 extension만 남겼을 때 충돌이 줄어드는지 확인한다.

### Checks

1. review surface에서 불필요한 extension을 끄면 `fabriqa` 충돌이 줄어드는가
2. decision surface에서 `Foam` 중심 구성이 더 안정적인가
3. `--disable-extension` 또는 profile별 extension set이 practical한가

### Candidate commands

```bash
code --new-window --disable-extension foam.foam-vscode /path/to/workspace
```

```bash
code --new-window --disable-extension fabriqaai.fabriqa-markdown-editor /path/to/workspace
```

### Pass criteria

- 어떤 extension 조합이 review surface에 좋은지 분명해진다
- 어떤 extension 조합이 decision surface에 좋은지 분명해진다

## Module 6. OpenWith Command Bridge Module

### Goal

CLI와 settings만으로 부족한 부분을 `vscode.openWith` command/API layer로 메울 수 있는지 확인한다.

### Target

- 특정 markdown resource를 원하는 editor `viewId`로 열기
- `fabriqa.markdownEditor`
- `vscode.markdown.preview.editor`

### Current experiment artifact

- `/tmp/vscode-openwith-bridge-experiment/package.json`
- `/tmp/vscode-openwith-bridge-experiment/extension.js`
- `/tmp/vscode-openwith-bridge-experiment/README.md`

### Checks

1. command palette에서 bridge command가 정상 등록되는가
2. active file 또는 picked file에 대해 `vscode.openWith`가 호출되는가
3. `fabriqa.markdownEditor`로 정확히 열리는가
4. `vscode.markdown.preview.editor`로 정확히 열리는가
5. 실패 시 error message가 충분히 설명적인가

### Pass criteria

- direct `openWith`가 실제 surface 제어 레버로 작동한다
- `editorAssociations` 우회 없이 특정 editor 지정이 가능해진다

## Module 7. MCP Control Module

### Goal

chat이 VS Code artifact를 더 직접적으로 열거나 제어하는 방법이 practical한지 검토한다.

### Checks

1. MCP-based VS Code control이 local workflow에 과한지 아닌지
2. file open, artifact reveal, profile launch 정도만으로 충분한지
3. direct editor manipulation이 꼭 필요한지

### Pass criteria

- direct control이 꼭 필요한 경우와 아닌 경우가 분리된다
- CLI + settings + URL launch만으로 충분한지 판단할 수 있다

## Manual Validation Priority

사용자 수동 검증이 특히 필요한 부분:

- `Reopen Editor With...` 관련 behavior
- already-open tab이 editor association 변경을 실제로 반영하는지
- profile별 extension/UI 상태가 실제로 다르게 보이는지
- review window와 decision window의 체감 충돌 여부

## Suggested Execution Order

1. `review-profile module`
2. `decision-profile module`
3. `window-routing module`
4. `url-launch module`
5. `extension-isolation module`
6. `openwith-command-bridge module`
7. `mcp-control module`

## Recording Template

```md
experiment:
surface:
workspace:
profile:
command:
expected:
observed:
result: pass | partial | fail
manual_step:
notes:
```

## One-Line Conclusion

다음 단계의 핵심은 editor 교체가 아니라, `Image Review Surface`와 `Interactive Decision Surface`를 VS Code 안에서 더 작게 분해된 control modules로 검증하는 것이다.
