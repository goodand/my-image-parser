# Repeated Issue: Repo-Specific Rules Hardcoded In Generic Skill Script

## Pattern

A classifier, scanner, or helper script written for one target repo gets placed in a "reusable" shared skill without parameterizing the matching rules. The script works perfectly for the original repo but fails silently (returns `unclassified` for everything) when pointed at a different repo.

## Recurrence Signal

- a shared skill in `Skills-Create-Project/` contains scripts with path-matching or naming rules tied to a single repo's directory structure
- the script produces correct results for the original target but meaningless results for any other

## Failure Signature

- `review_file_classifier.py` classifies `src/decision/decision-contract.js` correctly as `data_contract` for `vscode-markdown-review-surface`, but any file from a different repo gets `unclassified` because the rules check for `src/decision/`, `session-config`, `decision-contract`, `feedback-ledger` etc.

## Current Workaround

- add a docstring marking the script as a reference implementation for the specific repo
- note that reuse for a different repo requires replacing the matching rules or extracting them into an external config

## Structural Fix Candidate

- extract classification rules into a JSON/YAML config file alongside the script
- script reads rules from config, making it repo-agnostic
- each target repo provides its own rule file

## Escalation Trigger

- another shared skill bundles a script with repo-specific assumptions that break on a second repo

## Current Proven Evidence

- on 2026-04-08, `cross-repo-product-review/scripts/review_file_classifier.py` had `src/decision/`, `session-config`, `decision-contract`, `feedback-ledger`, `slide-`, `webview-`, `host-`, `mode-router` hardcoded for `vscode-markdown-review-surface`; fixed by adding a reference-impl docstring
