# ISSUE: Regrouping-Only Fix Stalls Without Component Decomposition

## Summary

Some composite images cannot be fixed by better regrouping alone. If the system never decomposes the image into meaningful components first, regrouping logic stalls because it is still choosing among incomplete or semantically mixed regions.

## Recurrence signal

This issue is present when:
- the image is a multi-panel analytical or dashboard-like composite
- better crop union helps a little but does not resolve the semantic ambiguity
- the real question is still "what are the components?" before "which grouping should win?"

## Current workaround

Pause at the regrouping layer and gather external decomposition/layout references before continuing implementation. Treat decomposition and regrouping as separate stages.

If the mainline already has a stable working cohort, keep decomposition in a parallel research lane instead of blocking downstream work.

## Structural fix candidate

A dedicated decomposition stage before regrouping:
- layout proposal
- component typing
- candidate regrouping
- bounded tie-break

Current strategy reference:
- `../../../../project_domain/resources/references/REFERENCE_component_decomposition_strategy-at2026-03-30.md`

## Escalation trigger

Escalate when another composite image remains ambiguous after recrop/regrouping improvements because the codebase still lacks a strong component decomposition stage.
