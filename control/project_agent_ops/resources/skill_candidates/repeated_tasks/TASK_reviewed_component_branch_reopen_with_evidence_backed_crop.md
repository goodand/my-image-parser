# Repeated Task: Reviewed Component Branch Reopen With Evidence-Backed Crop

## Recurrence Signal

A reviewed branch is currently waived or blocked, but a bounded reopen becomes possible once a semantically selected crop can be proven better than the full-image evidence for the exact reading task.

## Current Proven Example

- source image: `image11.png`
- full-image OCR and reviewed crop OCR both retained the expected table tokens
- the reviewed crop removed seven extraneous full-image OCR tokens
- the bounded rerun succeeded on the reviewed crop surface and closed the isolated-component arm for one shared image
- source image: `image10.png`
- OCR proxy alone said the reviewed crop was not better because the full image already had zero proxy extras
- direct GPT image verification still judged the reviewed crop as higher-confidence caption input because it preserved the full table and removed surrounding slide noise
- the comparison artifact was promoted to `comparison_ready_reviewed_branch` without regenerating the arm

## Repeatable Pattern

1. start from a reviewed, semantically selected component surface
2. compare the reviewed crop against the full-image evidence on the same expected token set
3. require explicit evidence that the reviewed crop is better for the bounded task
4. build a bounded context package that preserves provenance and review status
5. run one bounded rerun before reclassifying the arm as comparison-ready
6. when OCR proxy and visible semantics diverge, escalate the tie-break to direct GPT image verification instead of forcing a waiver

## Promotion Candidate

- reusable reviewed-component reopen checklist or bounded comparison-arm packet

## Why It Matters

This pattern prevents:

- reopening waived branches from mechanical crops alone
- overstating isolated-component readiness from raw alpha split output
- losing provenance when a reviewed crop is used as the new caption input surface
