# Caption Completeness Validator Smoke

Date: 2026-03-27 19:14 KST

## Purpose

Verify that the newly added caption completeness validator works in both:

- local replay against previously saved raw OpenAI responses
- live OpenAI API execution through the normal runner path

## Inputs

- Known-good baseline image:
  - [image1.png](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image1.png)
- Previously truncated sample image:
  - [image2.png](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_domain/resources/pptx_jobs/01_full_presentation_2026-03-17/media/image2.png)
- Known-good saved raw response:
  - [img_000001.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w1_responses/img_000001.json)
- Previously truncated saved raw response:
  - [img_000001.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/jobs/image_caption_jobs/phase1_ppt1_w2_responses/img_000001.json)

## Local Replay Validation

- good saved response: passed validator
- previously truncated saved response: blocked by validator
- observed error:
  - `Caption completeness validation failed: caption ends with an unfinished token.`

## Live OpenAI Smoke

Runner:

- [caption_images_openai.py](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/scripts/caption_images_openai.py)

Outputs:

- good image ledger:
  - [validator_smoke_good_image1.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/jobs/image_caption_jobs/validator_smoke_good_image1.json)
- truncation rerun ledger:
  - [validator_smoke_truncation_image2.json](/Users/jaehyuntak/Desktop/Project_____현재_진행중인/my-image-parser/control/project_agent_ops/registry/jobs/image_caption_jobs/validator_smoke_truncation_image2.json)

Execution result:

- good image: `completed`
- previous truncation image rerun: `completed`

Observed live captions:

- `image1.png`
  - `The image displays a set of bar charts comparing the latest structure metrics for the Hete family across various measures: IC Mean, CC Parent Mean, SR Mean, and ACR Mean. Each chart shows values for Hete, Hete-PC, and Hete-PC-HyDE.`
- `image2.png`
  - `Dashboard showing bar charts and a summary table for 'Core 70Q Metrics Overview'. Metrics displayed include DocHit@10, MRR, ChunkRec1@10, and Rerank Delta: DocHit@10 for various modes (HyDE, A3, Sequential, HyDE+r, A3+r, Seq+r). Core Summary Table consolidates all results.`

## Interpretation

- The validator correctly rejects the previously saved truncated response.
- The same image can still succeed on a fresh API call when OpenAI returns a complete caption.
- This means the guard is suitable as a phase-2 preflight quality barrier and does not inherently block valid reruns.

## Conclusion

The caption completeness validator is now:

- code-integrated
- locally replay-verified
- live-run verified on a minimal 2-image smoke

Remaining non-validator blocker before broader phase-2 rollout:

- legacy `phase1_caption_10w` machine-readable filename cleanup or reclassification
