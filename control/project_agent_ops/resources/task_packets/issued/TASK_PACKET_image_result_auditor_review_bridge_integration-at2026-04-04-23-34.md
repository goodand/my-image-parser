# Task Packet: Image Result Auditor Review Bridge Integration

## Goal

Extend `image-result-auditor` so the skill explicitly owns the current human-review bridge and downstream preflight preparation workflow without creating a new standalone skill.

## Why This Fits

`image-result-auditor` already owns:

- review-ready queue preparation
- comparison summaries
- proxy auto-eval outputs
- downstream consumer preparation without regenerating upstream artifacts

The recent repeated patterns now fit that ownership:

- aggregate bundle to human review surface flattening
- review surface manifest to retrieval preflight bridge
- review decision ingestion to ready subsets
- zero-ready downstream dry-run contract
- machine-prefilled review-seed drift validation before ingestion
- single-writer canonical JSONL review entry with owned-row split
- human-edited caption arm exception normalization

## Scope

Update the skill so a future operator can discover and execute the review-bridge-to-preflight workflow from the skill itself.

## Owned Write Surfaces

- `skills/image-result-auditor/SKILL.md`
- `skills/image-result-auditor/references/review-queue-contract.md`
- `skills/image-result-auditor/references/comparison-consumer-runtime.md`
- `skills/image-result-auditor/references/runtime.md`
- `skills/image-result-auditor/references/troubleshooting.md`
- `skills/image-result-auditor/checklists/audit-preflight.md`
- `skills/image-result-auditor/checklists/four-mode-consumer-readiness.md`
- optional new references under `skills/image-result-auditor/references/`
- optional KB patch under `skills/image-result-auditor/knowledge_bases/`
- optional eval patch under `skills/image-result-auditor/evals/evals.json`

## Required Inputs

- [KB_repeated_task_patterns.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/skill_candidates/repeated_tasks/KB_repeated_task_patterns.md)
- [KB_repeated_issue_patterns.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/resources/skill_candidates/repeated_issues/KB_repeated_issue_patterns.md)
- [SPEC_corpus_review_decision_capture.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/specs/prose/SPEC_corpus_review_decision_capture.md)
- [REVIEW_phase2_caption_review_decision_entry-at2026-03-30-23-23.md](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/reports/REVIEW_phase2_caption_review_decision_entry-at2026-03-30-23-23.md)
- [phase2_caption_review_decision_ingestion_at2026_03_30.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/manifests/phase2_caption_review_decision_ingestion_at2026_03_30.json)

## Expected Changes

1. skill overview mentions human review bridge and downstream preflight preparation
2. references explain:
   - review-surface manifest as machine truth
   - immutable machine-prefilled seed fields
   - single-writer canonical JSONL rule
   - zero-ready dry-run state
3. checklists include:
   - manifest-first readback
   - drift validator expectation
   - `human_edited_caption` exception
4. if useful, add one dedicated reference for review-decision bridge or zero-ready dry-run

## Non-Goals

- no new standalone skill
- no upstream corpus truth mutation
- no retrieval execution
- no mapping execution

## Done Definition

- `image-result-auditor` can be invoked for the full review-bridge-to-preflight workflow without rereading scattered project docs
- the skill still does not claim human approval or upstream mutation
- any new reference or checklist remains consistent with existing consumer-readiness rules

## Verification

1. re-read `skills/image-result-auditor/SKILL.md`
2. confirm the new references mention manifest-first truth, decision ingestion, and zero-ready dry-run
3. if `evals/evals.json` changes, validate JSON syntax
