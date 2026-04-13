# Repeated Issue: Review Surface Session Bundle Absolute Path Residue

## Symptom

- a session bundle is logically valid and useful as evidence
- but nearly every file in the bundle embeds machine-local absolute paths to markdown, session files, images, or source manifests
- the bundle cannot be committed as a portable review artifact until those paths are normalized

## Scope

- review-surface session bundles
- session manifests, config files, decision rows, feedback ledgers, and per-item bundle JSON files
- JSON and JSONL evidence trees that preserve runtime provenance

## Guardrail

- preserve the bundle semantics; sanitize only the path prefix
- use one explicit placeholder such as `<REPO_ROOT>/` for repo-bound evidence references
- revalidate every JSON and JSONL file before claiming the bundle is committable
- do not treat evidence bundles like prose docs; bulk relative-link rewriting is the wrong tool here

## Follow-Up

- add a reusable sanitizer for session bundles before public packaging
- document that evidence bundles require format-aware path normalization, not markdown-style cleanup

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` found absolute-path residue across `session-config.json`, `review-surface-manifest.json`, `decision-seed.jsonl`, `feedback-ledger.json`, and ten `image*.bundle.json` files inside the review-surface session bundle
- the fix normalized those paths to `<REPO_ROOT>/`, revalidated the payloads, and then committed the bundle in `3d1e4a1`

## Step-By-Step Evidence Trace

1. The bundle first appeared as a small but still-untracked evidence tree.
   - size evidence: about `100K`
2. The path problem was then confirmed from concrete fields, not assumed.
   - `session-config.json`: `review_markdown_path`, `review_surface_manifest_path`, `decision_seed_jsonl`, `feedback_json_path`
   - `review-surface-manifest.json`: `review_markdown_path`, `source_image_path`
   - `bundles/image*.bundle.json`: `source_image_path`, `source_manifest_path`, `source_bundle_path`
3. The same residue also appeared in decision rows and feedback-oriented artifacts.
   - `decision-seed.jsonl`
   - `feedback-ledger.json`
4. Because the files were machine-readable evidence rather than prose docs, relative-link cleanup was rejected in favor of placeholder prefix normalization.
5. The bundle became committable only after the full tree validated cleanly and `rg` no longer found raw machine-local paths.
