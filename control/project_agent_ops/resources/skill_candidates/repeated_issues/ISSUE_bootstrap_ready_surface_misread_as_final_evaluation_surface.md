# Repeated Issue: Bootstrap-Ready Surface Misread As Final Evaluation Surface

## Symptom

A review surface can already bootstrap a session, open the UI, and render at least some slides or images, so operators start treating that operational success as proof that the lane is ready for the intended human evaluation.

## Current Proven Example (2026-04-09)

`vscode-markdown-review-surface` reached a valid `decision-slides` bootstrap/open path for the first 10 images, but the Steward response still froze the lane as incomplete because the surface did not yet render arm-by-arm candidate caption and alt-text comparison in-bounds.

## Later Session Extension (2026-04-09)

Even after the artifact contract extension and candidate comparison section landed, the same class of mistake reappeared at the session-truth layer:

1. the first-10 bootstrap session opened successfully and displayed image previews
2. operators could therefore assume the set was ready for a full 10-image human run
3. session-local bundle audit showed the actual state was narrower:
   - `image1`-`image5`: `availability = excluded`
   - `image6`: `availability = missing_source_record`
   - `image7`-`image10`: `availability = ready`
4. the canonical phase2 comparison truth set still pointed to a different 9-image closure set (`image11`, `image7`, `image8`, `image10`, `image12`, `image13`, `image14`, `image9`, `image15`)

This means `bootstrap/open works` and even `comparison UI renders somewhere` still did not prove that the current first-10 session was a valid final evaluation set.

## Later Session Extension II (2026-04-09)

The same class of confusion reappeared during live operator testing after the surface was reopened:

1. `image1` rendered correctly, so the operator expected caption candidates to appear immediately
2. `image6` showed `Preview unavailable for .emf in the webview.`
3. when `image1`-`image6` still showed no comparison-ready candidate cards, the missing body could be misread as `caption generation failed`
4. the real cause was narrower and structural:
   - `image1`-`image5` were intentionally excluded from the four-arm comparison set
   - `image6` had `missing_source_record`
   - only `image7`-`image10` were `ready`

This proved again that a surface can look operational enough for manual testing while still being the wrong execution set for the intended evaluation task.

## Why This Matters

- open-path success is visible immediately, so teams over-trust it
- a partially ready session can quietly become the de facto execution set if the ready/non-ready split is not audited
- later operator evidence becomes hard to interpret if the session itself was not a valid final run target

## Guardrail

Before declaring a review surface ready for human execution:

- verify session-local bundle availability for every slide
- compare the current session image set against the canonical comparison truth set
- state the exact `ready / excluded / missing` counts
- distinguish `surface opens` from `session is valid for the intended evaluation run`
- if the operator sees `image preview exists but candidate texts do not`, verify bundle availability and truth-set membership before treating it as a rendering bug

## Escalation Trigger

Another evaluation lane reaches successful open/navigation/image preview, but the actual comparison-ready image set has not been audited against the intended truth set before operators start the run.
