# Repeated Task: Tracked-File-Only Raw Vendor Source Import From Nested Repos

## Pattern Name

- tracked-file-only raw vendor source import from nested repos

## Trigger

- the user explicitly chooses raw vendor inclusion
- vendored directories still contain nested `.git`
- local installs, model payloads, caches, or generated files must stay out of the host repo

## Stable Steps

1. Measure each vendored directory and confirm nested repo state before staging anything.
2. Check the host repo's ignore rules for `.git`, `.venv`, `node_modules`, model weights, and local residue.
3. Preserve the nested git metadata outside the vendor tree before importing files into the host repo.
4. Enumerate the vendor repo's originally tracked files through its preserved git metadata.
5. Stage only those tracked files into the host repo instead of recursively adding the whole directory.
6. Keep local runtime residue, weights, caches, and install outputs out of the host repo even during raw inclusion.
7. Commit the imported vendor source trees as one explicit ingestion batch.

## Candidate Promotion

- reusable vendor-ingestion workflow for `raw source wanted, local runtime residue forbidden`
- preflight: `size + nested git + ignore boundary + tracked-file-only staging`
- vendor import rule: preserve upstream tracked source, not workstation-local runtime state

## Promotion Trigger

- another repo wants to absorb vendored tool source directly, but the vendor tree still mixes source history with local installs and heavy payloads

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` imported four vendored tool trees in `2562031` by using tracked-file-only staging rather than `git add vendor/...`
- the host ignore rules already excluded `vendor/**/.git/`, `vendor/**/.venv/`, `vendor/**/node_modules/`, `vendor/**/.user_id`, and `vendor/**/models/`

## Step-By-Step Evidence Trace

1. The raw vendor request was explicit, so wrapper-only strategy was no longer sufficient.
2. The host repo's vendor ignore boundaries were confirmed first.
   - ignore evidence: `.gitignore` lines covering `vendor/**/.git/`, `vendor/**/.venv/`, `vendor/**/node_modules/`, `vendor/**/.user_id`, and `vendor/**/models/`
3. The target vendor trees were then measured and inspected.
   - commit evidence: `2562031`
   - representative scope: `vendor/mcp/imagesorcery-mcp`, `vendor/mcp/macos-ocr-mcp`, `vendor/mcp/tigaweb-image-edit-sample-mcp`, `vendor/ocr/macOCR`
4. Nested repo metadata was preserved outside the active vendor directories before staging.
5. Vendor-tracked files were then enumerated from the preserved git metadata instead of by recursive filesystem trust.
6. Only upstream-tracked source, docs, tests, and tracked support files were staged into the host repo; local runtime residue stayed excluded.
7. The import then landed as one explicit vendor-ingestion commit.
   - commit evidence: `2562031`
