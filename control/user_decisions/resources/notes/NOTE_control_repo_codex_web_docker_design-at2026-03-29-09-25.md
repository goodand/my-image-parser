# Control Repo Codex Web Docker Design

## Context

This note captures the current design direction for turning the `control/` tree into a standalone repository that can run inside Codex Web and Docker.

The current `control/` tree is document-heavy and execution-history-heavy:

- active value is concentrated in `project_domain/resources`, `project_agent_ops/resources`, and `team/resources`
- `runs/`, `registry/`, `.obsidian/`, and private input assets should stay outside the tracked portable runtime surface
- many active documents and contracts still point at absolute local paths and root-level `scripts/`

## Chosen Defaults

- repository root: `control/`
- runtime source strategy: move the minimal required runtime code into the new `control` repo
- tracked content policy: keep `resources`-centric content in Git and keep `runs` plus `registry` out of Git
- path policy: sanitize active documents and contracts to repo-relative paths
- external and Mac-specific references: move to an archived reference lane
- v1 input boundary: local exported `PPTX`
- v1 review mode: fully automated
- v1 retrieval corpus: local corpus only
- v1 output mode: sidecar bundle, not regenerated `PPTX`
- Mac-only features: excluded from v1

## Target V1

The first portable runtime should be a Docker-safe and Codex-Web-safe end-to-end pipeline that:

1. accepts a local `PPTX`
2. extracts embedded images
3. generates captions automatically
4. creates retrieval input from approved captions
5. retrieves and reranks candidates from a local corpus
6. auto-selects mappings or generates outlier descriptions
7. writes a sidecar output bundle with manifests and artifacts

The v1 runtime should not require:

- Canva live integration
- macOS OCR
- `simctl`
- metadata write-back
- filename rename
- original deck patching

## Repository Shape

The standalone `control` repo should contain:

- `project_domain/`
- `project_agent_ops/`
- `team/`
- `user_decisions/`
- `runtime/`
- `tests/`
- `pyproject.toml`
- `Dockerfile`
- `README.md`

The active runtime should expose one CLI surface, for example:

```bash
python -m runtime.pipeline run \
  --input-pptx /work/input/source.pptx \
  --corpus-dir /work/corpus \
  --output-dir /work/output \
  --profile docker_v1
```

## Required Refactoring Direction

### 1. Sanitize the active control tree

- replace absolute machine paths with repo-relative paths or placeholders
- remove active references to root-level `scripts/`
- keep only Docker-safe and repo-local references in active documents
- move historical, external-repo, and Mac-only guidance into archived references

### 2. Define the portable runtime inside the repo

Minimal runtime subsystems:

- `intake`
- `extract`
- `caption`
- `corpus`
- `retrieve`
- `rerank`
- `mapping`
- `outlier`
- `bundle`

### 3. Keep the table branch optional

- preserve the table branch in design
- feature-flag it in v1
- do not depend on Mac-only OCR helpers

## Expected V1 Outputs

The final deliverable should be a sidecar bundle containing at minimum:

- `job_manifest.json`
- `image_manifest.jsonl`
- `caption_draft.jsonl`
- `caption_approved.jsonl`
- `retrieval_input.jsonl`
- `retrieval_candidates.jsonl`
- `reranked_top5.jsonl`
- `mapping_results.jsonl`
- `outlier_descriptions.jsonl`
- `final_content_manifest.jsonl`
- `bundle_manifest.json`

## Deferred Beyond V1

- live Canva export or download
- human review gates
- Mac OCR and Apple helper flows
- metadata write-back
- rename flow
- regenerated presentation rendering
- original deck patching

## Notes

- `team/resources/scripts/lint_control_tree.py` is the clearest existing executable surface inside `control`, but it currently assumes the broader workspace shape and will need adaptation when `control` becomes repo root.
- active contracts such as `project_domain/resources/specs/contracts/*` still refer to root-level `scripts/`; those contracts must move with the runtime refactor.
