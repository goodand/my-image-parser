# Repeated Task: Context Package Builder To Caption Runner Injection

## Pattern Name

- connect a reviewed context-package artifact to a caption runner without breaking the original no-context baseline

## Trigger

- a new reviewed OCR or context-package builder is added and its outputs must be injected into a later caption rerun
- the runner already works and should be extended additively rather than rewritten
- the same workspace needs both baseline mode and context-enriched mode

## Stable Steps

1. define an explicit additive input surface such as `--context-package-json` or `--context-package-manifest-jsonl`
2. load context packages by `source_image_path` so the mapping does not depend on fragile batch-local ordering
3. keep the existing baseline prompt unchanged when no context package is supplied
4. sanitize context fields before prompt injection so prior captions or review-only notes do not leak back into generation
5. persist the resolved context package on the ledger row for later audit
6. verify the integration with a fake client or local fixture before any live API smoke

## Candidate Promotion

- checklist
- script
- skill
- packet template
