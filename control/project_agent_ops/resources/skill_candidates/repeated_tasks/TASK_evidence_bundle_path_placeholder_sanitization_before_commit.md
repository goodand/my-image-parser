# Repeated Task: Evidence Bundle Path Placeholder Sanitization Before Commit

## Pattern Name

- evidence bundle path placeholder sanitization before commit

## Trigger

- a bounded evidence bundle is worth committing
- the bundle is structurally valid but embeds machine-local absolute paths
- preserving the evidence matters more than regenerating the bundle from scratch

## Stable Steps

1. Enumerate every file in the bundle and validate the format classes first: JSON, JSONL, or mixed metadata files.
2. Search the full bundle for machine-local absolute paths and classify them as repo-root-bound references.
3. Replace the machine-local prefix with one stable placeholder such as `<REPO_ROOT>/`.
4. Revalidate every JSON file and every JSONL row after replacement.
5. Commit the sanitized bundle as evidence, not as live runtime configuration.
6. Keep the sanitization bounded to path fields only; do not rewrite session semantics or review outcomes.

## Candidate Promotion

- helper: bundle-wide path placeholder sanitizer for JSON + JSONL evidence trees
- checklist: `enumerate -> sanitize -> validate -> commit`
- review rule: evidence bundles may be preserved if machine-local paths are normalized without altering semantics

## Promotion Trigger

- another review, audit, or experiment bundle is small enough to preserve but contains machine-local absolute paths throughout

## Current Proven Evidence

- on 2026-04-13, `my-image-parser` sanitized the 14-file review-surface session bundle under `REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.review-surface-session`
- the pass replaced absolute local prefixes with `<REPO_ROOT>/`, revalidated the JSON and JSONL payloads, and then committed the bundle in `3d1e4a1`

## Step-By-Step Evidence Trace

1. The bundle was first treated as evidence worth preserving, not as scratch output.
   - session root: `control/project_domain/resources/reports/REVIEW_phase1_caption_10w_obsidian_caption_review-at2026-03-27-19-08.review-surface-session`
2. The concrete payload classes were enumerated before any edit:
   - `session-config.json`
   - `review-surface-manifest.json`
   - `decision-seed.jsonl`
   - `feedback-ledger.json`
   - `bundles/image1.bundle.json` through `bundles/image10.bundle.json`
3. Absolute-path residue was then verified across the whole bundle.
   - representative evidence: `review_markdown_path`, `decision_seed_jsonl`, `source_image_path`, `source_manifest_path`
4. Only the repo-root path prefix was normalized.
   - replacement shape: `/Users/.../my-image-parser/` -> `<REPO_ROOT>/`
5. Validation was rerun after normalization.
   - JSON validation targets: `session-config.json`, `review-surface-manifest.json`, `bundles/*.bundle.json`
   - JSONL validation target: `decision-seed.jsonl`
6. After the tree validated cleanly and no raw machine-local path remained, the bundle was committed as evidence in `3d1e4a1`.
