# Repeated Issue: Dead Code Residue After Guard Consolidation

## Symptom

A helper function's only call site is removed during a refactor or consolidation, but the function definition itself is left in place. The dead function compiles without error and passes all tests, making it invisible without static analysis or careful review.

## Current Proven Example

- `decision-slides.js` had `clearDecisionSlidesFeedbackNotes()` function (lines 170-175)
- Its only call site was in `submitDecisionSlidesFeedback()` line 291
- When the double DOM update was fixed (Issue 3), the call site was removed because the subsequent `setDecisionSlidesUiState()` already handled both `statusMessage` and `errorMessage`
- The function body remained, triggering a TypeScript/diagnostic warning: `'clearDecisionSlidesFeedbackNotes' is declared but its value is never read`
- Fixed 2026-04-08 by deleting the function definition

## Why This Matters

- Dead code increases cognitive load for future readers who may assume the function is used elsewhere
- In closure-scoped runtimes (like this webview), dead functions still occupy memory
- The function name suggests a meaningful operation, which could mislead a developer into re-adding calls to it rather than using the direct approach

## Guardrail

When removing a call site during refactor:
- Immediately search for other call sites of the same function
- If zero remaining call sites: delete the function definition in the same patch
- If the function is exported: check all importers before deletion

## Escalation Trigger

Another refactor removes a call site but leaves the function definition, and the dead code is only discovered later during unrelated review.

## Variant: Configuration-Mismatch Dead Code

A different path to the same outcome — code is syntactically reachable but semantically dead because a configuration flag or predicate condition makes it impossible to execute.

### Proven Examples (2026-04-08)

1. **`slide-parser.js` — `html: false` makes HTML image extraction dead code**
   - `new MarkdownIt()` at line 3 defaults to `html: false`
   - Lines 138-145 extract `<img>` tags from `token.content` via regex
   - But with `html: false`, markdown-it never produces `html_block` or `html_inline` tokens containing raw `<img>` tags — the extraction code is unreachable
   - Fix: either set `html: true` if HTML images are expected, or delete the HTML extraction branch

2. **`evaluation-session-open.js` — `toString` always-true predicate**
   - `typeof resourceOrOptions.toString === 'function'` was used as a URI detection guard
   - Every JavaScript object inherits `toString` from `Object.prototype`, so this predicate is always true — the URI branch fires for all inputs, making the non-URI branch dead
   - Fix: replaced with `typeof resourceOrOptions.fsPath === 'string'` to test an actual URI-specific property

### Why This Variant Is the Same Pattern

Both are dead code created not by removing a call site, but by setting a guard condition that can never (or always) be satisfied. The residue compiles, passes tests, and misleads future readers into thinking the branch is functional.

### Extended Guardrail

When writing conditional branches:
- Verify that the guard condition can actually produce both `true` and `false` for realistic inputs
- For library configuration flags: confirm the downstream token types or data shapes match the extraction code
- For type-check predicates: confirm the checked property is distinctive to the intended type, not inherited universally

## Promotion Status

- standalone issue, not yet absorbed into a skill
