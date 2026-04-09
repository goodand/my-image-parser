# Checklist: fabriqa + Foam Integration Validation

## Status

Draft

## Purpose

`fabriqa - markdown editor - obsidian style`와 `Foam`을 함께 사용할 때,

- `fabriqa`는 same-page live editing
- `Foam`은 backlink and graph shell

로 역할 분담이 실제로 가능한지 검증하기 위한 체크리스트.

## Intended Operating Model

1. 두 extension을 모두 설치한다.
2. `.md` 기본 editor는 VS Code 기본 editor 또는 `fabriqa`를 option으로 유지한다.
3. 필요할 때 `Open With -> fabriqa`로 연다.
4. `Foam`의 `Backlinks`, `Graph`, `References Explorer`는 side panel로 사용한다.

## Validation Questions

### 1. Backlinks Follow Current Note

목표:

- `fabriqa`로 연 현재 note를 기준으로 Foam의 `Backlinks Panel`이 정상적으로 따라오는지 확인한다.

체크:

- [ ] `fabriqa`로 `.md` note를 연다.
- [ ] Foam `Backlinks Panel`을 연다.
- [ ] 현재 note를 참조하는 다른 note가 panel에 표시된다.
- [ ] 다른 note로 전환했을 때 panel이 현재 문서를 기준으로 갱신된다.

판정:

- pass: `fabriqa`에서 열린 note와 Foam backlinks가 일관되게 동기화된다.
- fail: backlinks가 갱신되지 않거나, 기본 text editor에서만 정상 동작한다.

### 2. Wikilink Autocompletion In fabriqa

목표:

- `[[wikilink]]` 자동완성이 `fabriqa` live editing 상태에서도 usable한지 확인한다.

체크:

- [ ] `fabriqa`에서 note를 연다.
- [ ] `[[`를 입력한다.
- [ ] note 후보 자동완성이 뜬다.
- [ ] 링크를 선택하면 정상 삽입된다.
- [ ] 저장 후 링크 navigation이 정상 동작한다.

판정:

- pass: wikilink autocomplete와 insertion이 `fabriqa`에서도 실용 수준으로 동작한다.
- fail: autocomplete가 뜨지 않거나, text mode로 내려가야만 동작한다.

### 3. Rename And Link Sync Stability

목표:

- note rename 시 Foam과 VS Code link handling이 계속 안정적으로 맞물리는지 확인한다.

체크:

- [ ] 상호 참조 note 2개 이상을 준비한다.
- [ ] 한 note를 rename한다.
- [ ] 기존 wikilink가 자동 갱신된다.
- [ ] `fabriqa`에서 연 상태에서도 링크가 깨지지 않는다.
- [ ] Foam graph/backlinks가 rename 이후에도 정상 반영된다.

판정:

- pass: rename 이후 링크, graph, backlinks가 모두 유지된다.
- fail: 링크 일부가 깨지거나 graph/backlinks 갱신이 늦거나 실패한다.

### 4. Image Embed With Foam Navigation

목표:

- `fabriqa`에서 이미지 embed를 보고 편집하는 상태에서도 Foam graph/navigation이 계속 usable한지 확인한다.

체크:

- [ ] 이미지 embed가 있는 markdown note를 `fabriqa`로 연다.
- [ ] 이미지가 same-page에서 보인다.
- [ ] Foam graph view를 열 수 있다.
- [ ] Foam references explorer를 열 수 있다.
- [ ] note navigation과 image-bearing note 편집이 동시에 크게 충돌하지 않는다.

판정:

- pass: image live editing과 Foam navigation을 함께 쓸 수 있다.
- fail: custom editor 충돌, focus 문제, navigation 붕괴 등으로 workflow가 깨진다.

## Suggested Test Notes

- `note_a.md`
- `note_b.md`
- `note_with_image_embed.md`

## Final Verdict

- [ ] Fully usable together
- [ ] Usable with minor friction
- [ ] Split workflow required
- [ ] Not recommended

## Notes

```md
[record concrete friction, bugs, or workarounds here]
```
