# ISSUE: Seed-BBox-Only Reviewed Crop Truncation On Multi-Component Images

## Summary

A reviewed crop can be technically valid but still too narrow when it relies only on a parser-derived seed bbox. This happens on multi-component or composite images where nearby disconnected alpha components contain title or context that should stay with the main table/chart region.

## Recurrence signal

This issue is present when:
- reviewed crop generation uses only a single seed bbox
- alpha split reveals one or more nearby external components
- the full image contains more useful context than the reviewed crop
- raw alpha components are too fragmented to promote individually

## Failure mode

The reviewed branch appears under-cropped because:
- parser/table union captures only the structural core
- nearby title/context components are omitted
- downstream comparison may incorrectly conclude the branch is not useful

## Current workaround

Do not promote raw multi-component alpha output directly. Instead:
1. keep the parser/merged seed bbox as the anchor
2. enumerate nearby alpha components
3. build bounded recrop candidates such as `alpha_nearby_union`
4. score them with the same OCR-proxy surface used for reviewed-branch comparison
5. preserve candidate metadata and selected bbox in the output context package

## Structural fix candidate

General reviewed-component candidate-selection logic that:
- supports seed + nearby union recrop candidates
- records why a union candidate was skipped or selected
- prefers bounded recrop over raw component promotion

## Escalation trigger

Escalate when another excluded or weak reviewed branch shows:
- more than one nearby alpha component
- visible context loss from seed-only crop
- no safe semantic selector yet, but bounded recrop remains possible
