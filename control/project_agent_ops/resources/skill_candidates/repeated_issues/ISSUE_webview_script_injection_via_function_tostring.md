# Repeated Issue: Webview Script Injection Via Function ToString

## Symptom

Webview-side code is delivered by calling `function.toString()` on host-side functions and injecting the result as inline `<script>` content. This pattern breaks under minification, is impossible to test in isolation, and creates invisible coupling between host and webview.

## Current Proven Example

- `slide-view-model.js`, `slide-shell.js`, `slide-context.js`, `slide-feedback.js` all had `getReviewSurface*Script()` functions returning stringified code
- `webview-html.js` embedded these strings inside `<script nonce>` tags
- no type checking between host and webview function signatures
- any refactor or minification silently broke the webview
- fixed 2026-04-07 by switching to webpack bundle (`webpack.config.js`, entry `src/decision/webview-client.js`, output `dist/review-surface-webview.js`)
- all webview modules now use factory function pattern with `require()` imports

## Why This Is Dangerous

- `function.toString()` output is not stable across JS engines or minifiers
- no test can verify that the stringified code actually works in the webview context
- changes in one module's function signature silently break another module's stringified output
- makes source maps impossible

## Guardrail

- never use `function.toString()` to deliver code to a webview
- use a bundler (webpack, esbuild) to create a separate webview entry point
- test webview modules as regular Node.js modules via `require()`
- include `npm run build:webview` in the CI pipeline

## Escalation Trigger

Another webview or iframe receives code via `function.toString()` or template literal injection instead of a bundled entry point.
