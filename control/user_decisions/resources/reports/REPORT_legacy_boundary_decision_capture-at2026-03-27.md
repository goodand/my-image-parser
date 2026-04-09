# Legacy Boundary Decision Capture Report

## Purpose

Capture the current workspace decision artifacts for the legacy-boundary question set and place the result under the `user_decisions/runs` bucket.

## Inputs

- `ADR_0000_decision_inbox.md`
- `Legacy_Boundary_Decision_Checklist.md`
- `Legacy_Boundary_Decision_Answers-at2026-03-27.md`
- `legacy_boundary_decision_map.svg`

## Result

- decision source artifacts remain under `control/user_decisions/resources/`
- a machine-readable index now exists at `control/user_decisions/registry/decision_index.json`
- no deletion candidates were identified from the current workspace decision set

## Scope

This report covers only current-workspace decision artifacts. External workspaces and reference repositories are not part of this capture.
