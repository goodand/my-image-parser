# VSCode-First Surface Model Note

## Status

Draft

## Purpose

이 문서는 현재 `my-image-parser` workspace의 의사결정 지원과 review 운영을 `VSCode-first` 기준으로 다시 정리한다.

핵심 목적은 다음 세 가지다.

- 왜 `obsidian-caption-review-builder`와 `vscode-fabriqa-foam-workflow`를 만들었는지 다시 묶는다
- 사람이 실제로 수행하는 판단 작업을 `surface` 단위로 분리한다
- 이후 실험을 `editor 통합`이 아니라 `surface control plane` 실험으로 재정의한다

Related artifacts:

- [REFERENCE_decision_support_prompt.md](../closed_questions/REFERENCE_decision_support_prompt.md)
- [NOTE_decision_support_uxui_design-at2026-03-28-15-58.md](./NOTE_decision_support_uxui_design-at2026-03-28-15-58.md)
- [CHECKLIST_vscode_surface_control_experiments-at2026-03-29-00-38.md](./CHECKLIST_vscode_surface_control_experiments-at2026-03-29-00-38.md)
- [NOTE_vscode_openwith_bridge_experiment_results-at2026-03-30-01-04.md](./NOTE_vscode_openwith_bridge_experiment_results-at2026-03-30-01-04.md)
- [obsidian-caption-review-builder/SKILL.md](../../../../skills/obsidian-caption-review-builder/SKILL.md)
- [vscode-fabriqa-foam-workflow/SKILL.md](../../../../skills/vscode-fabriqa-foam-workflow/SKILL.md)
- `<TMP_DIR>/vscode-openwith-bridge-experiment/`

## Why These Skills Exist

이 skill들은 editor를 하나로 통합하기 위해 만든 것이 아니다.

목적은 다음과 같다.

1. 원시 caption/run 결과를 사람이 판단 가능한 review artifact로 바꾼다
2. 그 artifact를 상황에 맞는 VS Code surface에서 연다
3. 사람이 이미지 평가와 의사결정을 섞지 않고 수행하게 한다

즉:

- `obsidian-caption-review-builder`
  - `caption ledger -> markdown review artifact`
  - producer surface
- `vscode-fabriqa-foam-workflow`
  - `existing markdown review artifact -> VS Code operating surface`
  - operator surface

이 둘은 경쟁 관계가 아니라 생산과 운영의 분업이다.

## Surface Definition Rule

surface는 앱 이름이 아니라 다음 4가지를 기준으로 정의한다.

- dominant action
- dominant artifact
- interaction style
- host and control model

즉, 같은 VS Code 안에서도 서로 다른 surface가 존재할 수 있다.

## VSCode-First Surface Set

### 1. Image Review Surface

- dominant action: `review / compare / annotate / judge`
- dominant artifact: `image + nearby text`
- purpose: 이미지 자체가 평가 대상일 때 검토와 수정 판단
- host: `VS Code`
- preferred editor: `fabriqa`
- canonical form: 이미지가 많은 경우 하나의 긴 markdown review 문서

이 surface에서는 문서 하나 안에서 많은 이미지를 계속 보는 것이 중요하다.
note-per-image보다 batch review dossier가 더 적합하다.

### 2. Interactive Decision Surface

- dominant action: `ask / explain / narrow / decide`
- dominant artifact: `closed questions + tables + optional images`
- purpose: 폐쇄형 질문과 설명, 비교를 통해 의사결정을 좁히기
- host: `chat + VS Code`
- preferred editor in VS Code: `Text Editor`

중요한 점:

- 질문 자체의 interactive UX는 chat이 담당한다
- LLM은 필요할 때 VS Code를 제어해서 표, 이미지, markdown artifact를 새 창이나 기존 창에 띄운다
- VS Code는 decision artifact와 supporting artifact의 표시 장치다

즉 이 surface는 `chat-led decision surface with VS Code artifact control`이다.

### 3. Instant Memory Task Sequence Surface

- dominant action: `stash / defer / reorder / resume`
- dominant artifact: `messages, task units, session-linked notes`
- purpose: LLM task sequence를 임시 저장하고 순서를 조정하기
- host: `VS Code`
- preferred editor: `Text Editor`
- navigation shell: `Foam`

이 surface는 장기 지식 저장소가 아니라 working memory buffer다.

### 4. Prompt Reference Surface

- dominant action: `lookup / reuse / promote / refine`
- dominant artifact: `prompt markdown, promoted prompt candidates`
- purpose: 자주 쓰는 프롬프트와 승격된 prompt 후보 관리
- host: `VS Code`
- preferred editor: `Text Editor`
- navigation shell: `Foam`

## Backlink Role

backlink의 주요 역할은 사용자의 기억 연상을 돕는 것이다.

즉 backlink는:

- 정답 검색보다 `문맥 회상`
- 구조 검증보다 `이전 판단 복구`
- 현재 작업과 과거 메모의 연결

에 더 가깝다.

그래서 backlink는 특히 다음 surface에 중요하다.

- Instant Memory Task Sequence Surface
- Prompt Reference Surface

반대로 Interactive Decision Surface에서는 backlink보다 질문 구조와 supporting artifact가 더 중요하다.

## Validated Runtime Facts

실제 운영 검증까지 확인된 부분:

- `fabriqa` same-page 이미지 표시: pass
- Foam `Connections` / backlinks: pass
- note rename 후 링크 갱신: pass
- `[[wikilink]]` 자동완성: `Text Editor`에서는 pass, `fabriqa`에서는 fail
- `Foam: Update Wikilink Definitions`: `Text Editor`에서는 pass, `fabriqa` active editor에서는 fail

이 결과 때문에 현재 운영 모델은 완전 통합형이 아니라 `split workflow`다.

현재 가장 현실적인 역할 분담:

- `fabriqa` = Image Review Surface
- `Text Editor` = Interactive Decision Surface + Instant Memory + Prompt Reference
- `Foam` = backlink and graph shell

## Control Plane View

현재 문제의 본질은 editor가 부족한 것이 아니라, VS Code control plane을 더 잘 분해해야 한다는 점이다.

현재까지 확인된 제어 레버는 세 계층으로 나뉜다.

### 1. CLI layer

- `code --profile`
- `code --user-data-dir`
- `code --new-window`
- `code --reuse-window`
- `code -g`
- `--disable-extension`
- `vscode://file/...`
- `vscode://settings/...`

### 2. Settings layer

- workspace `.vscode/settings.json`
- `workbench.editorAssociations`

### 3. Command/API layer

- `vscode.open`
- `vscode.openWith`

즉, 현재까지 확인된 제어 레버를 합치면:

- workspace `.vscode/settings.json`
- `workbench.editorAssociations`
- `code --profile`
- `code --user-data-dir`
- `code --new-window`
- `code --reuse-window`
- `code -g`
- `--disable-extension`
- `vscode://file/...`
- `vscode://settings/...`
- `vscode.open`
- `vscode.openWith`

반면 아직 직접적인 CLI 제어가 없는 것:

- `Reopen Editor With...`

따라서 다음 실험의 목표는 `한 editor로 모든 걸 해결`이 아니라:

- surface를 분리하고
- 그 분리를 CLI와 설정으로 재현 가능하게 만드는 것

이다.

## Next Experiment Modules

다음 실험은 더 작은 모듈로 쪼개야 한다.

1. `review-profile module`
- Image Review Surface 전용 profile

2. `decision-profile module`
- Interactive Decision Surface 전용 profile

3. `window-routing module`
- 창/탭/파일 배치를 `code -n/-r/-g` 조합으로 검증

4. `url-launch module`
- `vscode://file/...`, `vscode://settings/...` 활용 검증

5. `extension-isolation module`
- surface별 extension 충돌 줄이기

6. `openwith-command-bridge module`
- `vscode.openWith`를 직접 호출하는 최소 extension/command bridge 검토
- current bounded experiment: `<TMP_DIR>/vscode-openwith-bridge-experiment/`

7. `mcp-control module`
- chat이 VS Code artifact를 더 직접적으로 여는 통로 검토

## One-Line Conclusion

이 workspace에서 VS Code는 단일 editor가 아니라 여러 surface를 담는 host다.

현재 기준으로 가장 타당한 모델은:

`Image Review Surface는 fabriqa 중심`
`Interactive Decision Surface는 chat이 주도하고 VS Code artifact를 호출`
`Instant Memory와 Prompt Reference는 Text Editor + Foam 중심`

이다.
