# Closed Question Responses Inbox

Use this file for closed-form answers from the user before they are normalized into canonical decision or contract records.

## Status

active

## How To Use

- Paste each closed-form response under a new heading.
- Preserve the exact answer first.
- Add interpretation only below the raw answer when needed.

## Responses

### 2026-03-27 Response 01

**Question**

```md
[paste question here]
```

**Answer**

```md
[paste answer here]
```

**Notes**

```md
[optional normalization notes]
```

### 2026-03-27 Response 02

**Question**

```md
[paste question here]
```

**Answer**

```md
[paste answer here]
```

**Notes**

```md
[optional normalization notes]
```

### 2026-04-05 Response 01

**Question**

```md
Current higher-level goal:
- make the repository clean enough to upload to GitHub now
- prevent machine-local and portability blockers that would later interfere with Docker or Codex Web

Closed questions and answers:
1. First GitHub repo scope? -> as much as reasonably possible
2. First upload visibility? -> private-first but publicable
3. Include `scripts/` and `skills/`? -> include both
4. `vendor/` policy? -> explanation needed first
5. `.codex/`, `.claude/`, `.vscode/`? -> exclude `.codex/` and `.claude/`
6. `runs/` and `registry/`? -> keep some only if they are explanatory
7. Absolute-path TOML/MD/JSON handling? -> placeholder substitution
8. Heavy local ML tools? -> include as much as possible because they may later run on Codex Web servers if possible
9. Docker readiness now? -> only remove blockers
10. First success criterion? -> clean enough to upload to GitHub
11. `tool_inventory` and handoff docs in first upload? -> exclude
12. First cleanup order? -> ignore/scope, then TOML/path sanitization, then docs

Follow-up decisions:
1. `vendor` default policy? -> include broadly
2. Agent-facing surface priority? -> preserve almost everything including selected registry snapshots, but do not include handoff docs; local and web agents should exchange information through commit messages or merge flow
3. `tool_inventory` in public repo? -> exclude
4. `project_agent_ops/resources` scope? -> preserve almost all
5. `runs/` exceptions? -> keep only a few manifest/report files
6. `.vscode/`? -> exclude all
7. Absolute-path TOML replacement style? -> choose between env-var placeholders and repo-relative examples; prefer env-var placeholder over markdown-only documentation
8. Heavy ML public surface? -> launcher + contract + install docs + runtime code + selected vendor source
9. README audience? -> both human and agent
10. File moves/restructure during cleanup? -> allowed if they reflect codebase rules and intent well
```

**Answer**

```md
User-approved direction:
- prioritize GitHub-ready curation now
- preserve agent-facing execution and reasoning surfaces as much as possible
- exclude machine-local agent settings
- keep portability blockers low without committing to Docker implementation yet
```

**Notes**

```md
Normalization notes:
- `.codex/`, `.claude/`, `.vscode/` are treated as excluded local surfaces
- `tool_inventory` stays out of the public repo
- `handoff` documents stay out of the public repo
- `project_agent_ops/resources` is mostly preserved
- only selected explanatory manifests and reports may remain from `runs/`
- for portable config examples, use env-var placeholders rather than absolute paths
```
