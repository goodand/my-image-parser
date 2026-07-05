# my-image-parser

Ongoing workspace for presentation-image extraction, captioning, OCR-backed context packaging, and downstream PPT-facing regeneration support.

This repository is organized around two surfaces:

- `control/`: control plane, canonical plans, contracts, reports, and operational truth
- `scripts/`, `skills/`, `vendor/`: execution plane, runnable code, agent-facing skill surfaces, and selected vendored tool source

## Lineage

This workspace was **derived from [`goodand/my-second-identity`](https://github.com/goodand/my-second-identity)** (a personal-blog Korean RAG system). The presentation-image workstream started inside that repo and was split out here; the two repos remain a pipeline pair:

```
my-second-identity ──(spawned: image-pipeline drafts, 2026-03)──▶ my-image-parser
        ▲                                                              │
        └──(consumes: reviewed captions / OCR context packages)────────┘
```

- **Upstream origin** — the initial drafts originated in `my-second-identity` and were migrated out of its planning surface (see `control/project_domain/resources/reports/REPORT_draft_classification_and_migration-at2026-03-27-15-29.md`; the old workspace keeps the export record under `plans/.../exported_to_my_image_parser/`).
- **Downstream consumer** — `my-second-identity` ingests this parser's reviewed captions and context packages into its RAG corpus. The caption-review gate here explicitly preserves multimodal form for that consumer (see `control/user_decisions/resources/notes/NOTE_presentation_image_pipeline_active_scope_freeze-at2026-04-09-19-11.md`).

## Current Scope

The active codebase supports work such as:

- PPT or presentation image extraction
- image caption generation and review support
- OCR and context-package assembly
- per-image experiment orchestration
- PPT-facing multimodal tool contracts and example IO
- MCP wrapper launchers for local or hosted agent workflows

This is still an active experiment workspace. The goal of the current Git history is to keep it recoverable and portable, not to pretend every surface is finalized.

## Repository Shape

- `control/project_domain/resources/`: domain specs, master plans, references, reports, manifests
- `control/project_agent_ops/resources/`: agent operations, smoke notes, references, task packets
- `scripts/`: runnable Python and shell entrypoints
- `scripts/mcp/`: MCP wrapper launchers
- `skills/`: agent-facing skill surfaces and runtime notes
- `vendor/`: vendored tool source only

Local state, caches, logs, weights, nested vendor installs, and machine-local config are intentionally ignored by Git.

## First Files To Read

Human and agent onboarding should start here:

- `control/project_domain/resources/master_plans/MASTER_PLAN_presentation_image_pipeline.md`
- `control/project_domain/resources/specs/contracts/presentation_image_pipeline_spec.json`
- `skills/image-job-dispatcher/SKILL.md`
- `skills/image-result-auditor/SKILL.md`

## Quick Start

1. Copy `.env.example` to `.env`.
2. Set `OPENROUTER_API_KEY` or `OPENAI_API_KEY`.
3. Optionally set shared runtime roots:
   - `MCP_STATE_DIR`
   - `MCP_CACHE_DIR`
4. Launch the wrapper you need.

Examples:

```bash
./scripts/mcp/start-filesystem-mcp.sh
./scripts/mcp/start-conport-mcp.sh
./scripts/mcp/start-exiftool-mcp.sh
./scripts/mcp/start-imagesorcery-mcp.sh
./scripts/mcp/start-paddleocr-mcp.sh
```

## MCP Wrapper Notes

All wrappers under `scripts/mcp/` now prefer env-driven state and cache roots instead of writing directly into repo-local runtime paths.

Shared defaults:

- `MCP_STATE_DIR`: defaults to `${XDG_STATE_HOME:-$HOME/.local/state}/my-image-parser/mcp`
- `MCP_CACHE_DIR`: defaults to `${XDG_CACHE_HOME:-$HOME/.cache}/my-image-parser/mcp`

Useful per-wrapper overrides:

- `AGENT_TASK_MANAGER_BIN` or `AGENT_TASK_MANAGER_ENTRYPOINT`
- `CONPORT_WORKSPACE_ID`, `CONPORT_LOG_FILE`
- `CV_MCP_ENV_FILE`
- `EXIFTOOL_BIN`
- `IMAGESORCERY_MCP_BIN`, `IMAGESORCERY_CONFIG_FILE`, `IMAGESORCERY_LOG_FILE`
- `MACOS_OCR_PYTHON`, `MACOS_OCR_ENTRYPOINT`
- `PADDLEOCR_MCP_BIN`, `PADDLEOCR_MCP_DEVICE`
- `TIGAWEB_IMAGE_EDIT_SAMPLE_ENTRYPOINT`, `TIGAWEB_IMAGE_EDIT_SAMPLE_IMAGE_DIR`

## Platform Notes

- `macos-ocr-mcp` is macOS-only.
- `paddleocr-mcp` is the most realistic hosted or Docker-facing OCR path in the current repo.
- `imagesorcery` source is vendored, but local installs, model weights, and runtime logs are not tracked.
- `tigaweb-image-edit-sample-mcp` expects a built JavaScript entrypoint unless you override it.

## Git Boundary

The current `.gitignore` is intentionally strict about:

- local runtimes and caches
- `.codex/`, `.claude/`, `.vscode/`, `.history/`
- `logs/`, `tmp/`, `context_portal/`
- vendor-local installs such as `.venv/`, `node_modules/`, model files, and nested `.git/`

If something looks missing from Git, check `.gitignore` before assuming the file was lost.
