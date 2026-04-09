# OpenAI Image Caption Validation Smoke Test

## Scope

Validate the local OpenAI caption runner on one extracted image through the new `--dataset-jsonl` path.

## Input

- Dataset: [media_extract_dataset.jsonl](../../../project_domain/resources/cross_validation/02_1/openai_api/media_extract_dataset.jsonl)
- Smoke output ledger: [smoke_gpt41_media_extract_job.json](../../../project_domain/resources/cross_validation/02_1/openai_api/smoke_gpt41_media_extract_job.json)
- Raw response: [img_000001.json](../../../project_domain/resources/cross_validation/02_1/openai_api/smoke_gpt41_media_extract_job_responses/img_000001.json)

## Command

```bash
python3 scripts/caption_images_openai.py \
  --dataset-jsonl control/project_domain/resources/cross_validation/02_1/openai_api/media_extract_dataset.jsonl \
  --limit 1 \
  --output control/project_domain/resources/cross_validation/02_1/openai_api/smoke_gpt41_media_extract_job.json
```

## Result

- CLI surface with `--dataset-jsonl`: passed
- One-image OpenAI API run: passed
- Ledger write: passed
- Raw response archive: passed
- Source context copied from dataset JSONL: passed

## Observed Output

- Model: `gpt-4.1`
- Processed count: `1`
- Status: `completed`

## Notes

- This smoke path does not require a simulator.
- The runner can operate directly on extracted media assets.
- For Codex-driven execution, network access required an unsandboxed run.
