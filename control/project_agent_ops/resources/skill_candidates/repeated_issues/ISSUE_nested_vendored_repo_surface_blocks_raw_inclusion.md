# Repeated Issue: Nested Vendored Repo Surface Blocks Raw Inclusion

## Symptom

- a vendored tool directory appears as an untracked candidate for Git packaging
- the directory still contains its own `.git` repository and local install residue
- raw `git add vendor/...` would pull a misleading or oversized surface into the host repo

## Scope

- vendored MCP repos
- vendored OCR or helper repos
- host repos that already provide launcher or wrapper ownership separately from vendor source ownership

## Guardrail

- do not raw-add a vendored repo that still contains nested `.git`
- measure size first and classify whether the repo is source, install residue, or model payload
- prefer `wrapper/launcher stays in host repo, vendor absorption stays explicit and separate`
- keep model weights, caches, and local installs out of the host packaging pass

## Follow-Up

- decide whether to absorb selected vendor source, keep the vendor as an external dependency, or add a dedicated vendor-ingestion workflow
- document that nested vendored repos are a separate boundary decision, not a normal untracked-file commit

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` found `vendor/mcp/imagesorcery-mcp` (`1.9G`), `vendor/mcp/macos-ocr-mcp`, `vendor/mcp/tigaweb-image-edit-sample-mcp`, and `vendor/ocr/macOCR` all still carrying nested `.git`
- the packaging pass therefore excluded them from the public-surface commit wave and kept only the host-side launchers and references in scope

## Step-By-Step Evidence Trace

1. The remaining untracked surface was reduced until `vendor` stood out as the last large unresolved class.
2. Each vendored directory was then measured and inspected directly.
   - `vendor/mcp/imagesorcery-mcp`: about `1.9G`
   - `vendor/mcp/macos-ocr-mcp`: about `42M`
   - `vendor/mcp/tigaweb-image-edit-sample-mcp`: about `82M`
   - `vendor/ocr`: about `6.5M`
3. Nested repo state was confirmed by reading the filesystem, not inferred.
   - nested `.git` evidence: `vendor/mcp/imagesorcery-mcp/.git`, `vendor/mcp/macos-ocr-mcp/.git`, `vendor/mcp/tigaweb-image-edit-sample-mcp/.git`, `vendor/ocr/macOCR/.git`
4. The host repo's own launcher ownership was then checked.
   - launcher evidence: `scripts/mcp/start-imagesorcery-mcp.sh`, `scripts/mcp/start-macos-ocr-mcp.sh`, `scripts/mcp/start-tigaweb-image-edit-sample-mcp.sh`
5. That split proved the raw vendor trees were a separate ingestion decision, not normal untracked files for the current packaging pass.
