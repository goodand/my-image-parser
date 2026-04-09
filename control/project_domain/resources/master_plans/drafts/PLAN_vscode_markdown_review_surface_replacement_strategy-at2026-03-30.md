# Plan: VS Code Markdown Review Surface Replacement Strategy

## Status

Draft

Current use in this workspace:

- parked reference draft for replacement strategy
- not the active implementation status surface
- current implementation progress should be read from decision-support overlays and the dedicated `vscode-markdown-review-surface` workspace reports

## Summary

이 문서는 `fabriqa`를 장기적으로 대체할 수 있는 자체 VS Code editor 전략을 저장하기 위한 draft다.

핵심 방향은 다음과 같다.

- 새 editor는 별도 plugin/repo로 만든다.
- 최종 목표는 `Image Review Surface`, `Interactive Decision Surface`, backlink surface를 포괄하는 완전 통합형이다.
- 다만 source of truth는 계속 Markdown으로 유지한다.
- UI 상태와 파생 인덱스는 sibling sidecar JSON으로 둔다.
- UI 구조는 `CustomTextEditorProvider` 중심 + side view 보조의 혼합형으로 간다.
- 초기에는 Foam fallback을 허용하지만 장기적으로는 자체 backlink 인덱싱으로 이동한다.

## Core Decisions

### 1. Repository Boundary

- 구현 대상은 현재 workspace 안의 임시 스크립트가 아니라 별도 plugin/repo다.
- `<TMP_DIR>/vscode-openwith-bridge-experiment`는 seed prototype로만 유지한다.

### 2. Data Model

- canonical content는 Markdown `TextDocument`
- sidecar는 `<basename>.surface.json`
- sidecar는 UI 상태와 파생 정보만 저장
- markdown 본문을 sidecar에 중복 저장하지 않음

### 3. UI Architecture

- 중심 editor: `reviewSurface.editor`
- 구현 방식: `CustomTextEditorProvider`
- 보조 view:
  - `reviewSurface.backlinksView`
  - `reviewSurface.documentOutlineView`
  - `reviewSurface.decisionArtifactsView`
- 따라서 “완전 통합”은 VS Code-native 혼합형으로 정의한다.

### 4. Control Plane

- CLI layer: window/profile/file routing
- settings layer: `workbench.editorAssociations`
- command/API layer: `vscode.openWith`
- 정확한 editor open은 `vscode.openWith(uri, 'reviewSurface.editor', { preview: false })`를 표준으로 사용한다.

### 5. Backlink Strategy

- 초기 전략은 혼합형
- 단기:
  - Foam은 비교/보조용으로 허용
- 중장기:
  - extension이 workspace markdown를 직접 스캔해 backlink index를 생성
  - `[[wikilink]]`와 일반 markdown link를 모두 지원

## MVP Direction

첫 MVP는 구현을 단계적으로 가더라도 최종 아키텍처를 훼손하지 않도록 다음 방향으로 고정한다.

- image-heavy markdown dossier를 한 문서에서 same-page review 가능해야 함
- `vscode.openWith`로 안정적으로 열려야 함
- source edit와 rendered canvas sync가 되어야 함
- image section jump와 outline navigation이 가능해야 함
- backlink는 v1에서 최소 read-only index부터 시작 가능

## Phases

### Phase 1. Review Core MVP

- 새 extension repo bootstrap
- `reviewSurface.editor` 등록
- markdown render + source sync
- image embed review 안정화

### Phase 2. Backlink and Sidecar

- sibling sidecar read/write
- workspace backlink indexer
- outline/backlinks side view

### Phase 3. Decision Artifact Integration

- decision artifact side view
- chat/controller가 띄운 artifact와 현재 문서 연결

### Phase 4. Full Replacement Hardening

- built-in preview / default / review surface round-trip
- table / mermaid render
- large dossier performance tuning
- `fabriqa` 의존 제거 후 동일 workflow 재검증

## Known Context

현재까지 검증된 사실:

- `vscode.openWith(..., 'vscode.markdown.preview.editor', ...)`는 성공
- `vscode.openWith(..., 'fabriqa.markdownEditor', ...)`는 현재 실험 조건에서 안정적으로 강제되지 않음
- `fabriqa` same-page image review는 유효하지만 Foam 명령과 `activeTextEditor` 연동에 제약이 있음
- 따라서 third-party custom editor를 bridge로 제어하기보다, 제어권이 있는 자체 editor를 갖는 것이 장기 해법이다

## Decision-Support Companion

Current progress and bottleneck reading should use:

- [REFERENCE_master_plan_progress_dashboard-at2026-04-05-09-17.md](../../../../user_decisions/resources/notes/REFERENCE_master_plan_progress_dashboard-at2026-04-05-09-17.md)
- [REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md](../../../../user_decisions/resources/notes/REFERENCE_master_plan_task_graphs-at2026-04-05-09-17.md)
