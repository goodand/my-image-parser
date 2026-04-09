#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path

from caption_runner_lib import (
    ApiConfig,
    CaptionGeneration,
    CaptionJobRunner,
    build_caption_prompt,
    parse_args,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
SAMPLE_IMAGE = ROOT_DIR / "control" / "project_domain" / "runs" / "pptx_jobs" / "01_full_presentation_2026-03-17" / "media" / "image11.png"


class FakeCaptionClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def generate_caption(
        self,
        image_path: Path,
        *,
        source_context: dict | None = None,
        context_package: dict | None = None,
    ) -> CaptionGeneration:
        self.calls.append(
            {
                "image_path": str(image_path),
                "source_context": source_context,
                "context_package": context_package,
            }
        )
        return CaptionGeneration(
            response_json={
                "id": "resp_test_context",
                "status": "completed",
                "output": [
                    {
                        "type": "message",
                        "content": [
                            {
                                "type": "output_text",
                                "text": json.dumps(
                                    {
                                        "caption": "A table compares metric values and deltas.",
                                        "alt_text": "Metrics table with delta values.",
                                        "structured_metadata": {
                                            "content_type": "document",
                                            "primary_subject": "metrics table",
                                            "notable_elements": ["rows", "columns", "delta"],
                                            "visible_text": ["DH@10", "MRR", "CR@10"],
                                        },
                                    },
                                    ensure_ascii=False,
                                ),
                            }
                        ],
                    }
                ],
                "usage": {"input_tokens": 1, "output_tokens": 1},
            },
            caption="A table compares metric values and deltas.",
            alt_text="Metrics table with delta values.",
            structured_metadata={
                "content_type": "document",
                "primary_subject": "metrics table",
                "notable_elements": ["rows", "columns", "delta"],
                "visible_text": ["DH@10", "MRR", "CR@10"],
            },
        )


def test_prompt_sanitizes_prior_caption() -> None:
    prompt = build_caption_prompt(
        {
            "source_slide_numbers": [24],
            "ocr_status": "usable",
            "ocr_text_excerpt": "DH@10 MRR CR@10 70Q 65Q Delta",
            "ppt_local_summary": (
                "Source PPT: `full_presentation_2026-03-17.pptx`. Slides: 24. "
                "Existing phase-1 caption: This must not leak."
            ),
        }
    )
    assert "OCR excerpt from the full image" in prompt
    assert "Source slide numbers: 24." in prompt
    assert "This must not leak" not in prompt
    assert "Existing phase-1 caption" not in prompt


def test_runner_passes_context_package_and_persists_it() -> None:
    fake_client = FakeCaptionClient()
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        context_package_path = tmpdir_path / "CONTEXT_PACKAGE.json"
        context_package = {
            "image_id": "01_full_presentation_2026-03-17:image11.png",
            "source_image_path": str(SAMPLE_IMAGE.resolve()),
            "source_dataset": "01_full_presentation_2026-03-17",
            "source_pptx": "dummy.pptx",
            "source_slide_numbers": [24],
            "image_surface": "full_image_original",
            "ocr_surface": "full_image_standalone_ocr",
            "ocr_status": "usable",
            "ocr_engine": "ocrmac",
            "ocr_annotation_count": 18,
            "ocr_text_excerpt": "DH@10 MRR CR@10 70Q 65Q Delta",
            "ocr_text_full_path": "/tmp/OCR_FULL_TEXT.txt",
            "ppt_local_summary": "Source PPT: `full_presentation_2026-03-17.pptx`. Slides: 24.",
            "context_package_markdown_path": "/tmp/CONTEXT_PACKAGE.md",
            "context_package_json_path": "/tmp/CONTEXT_PACKAGE.json",
            "review_status": "pending_review",
            "notes": ["fixture context package"],
        }
        context_package_path.write_text(
            json.dumps(context_package, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        output_path = tmpdir_path / "job.json"
        args = parse_args(
            [
                "--image",
                str(SAMPLE_IMAGE),
                "--output",
                str(output_path),
                "--context-package-json",
                str(context_package_path),
            ]
        )
        runner = CaptionJobRunner(
            args,
            root_dir=ROOT_DIR,
            config=ApiConfig(
                api_key="test-key",
                api_key_name="OPENAI_API_KEY",
                model="gpt-4.1",
                detail="high",
                max_output_tokens=700,
            ),
            client=fake_client,
            sleep_fn=lambda _: None,
        )
        summary = runner.run()
        assert summary["processed_count"] == 1
        assert len(fake_client.calls) == 1
        injected_context = fake_client.calls[0]["context_package"]
        assert isinstance(injected_context, dict)
        assert injected_context["ocr_status"] == "usable"
        injected_source_context = fake_client.calls[0]["source_context"]
        assert isinstance(injected_source_context, dict)
        assert injected_source_context["file"] == "image11.png"
        ledger = json.loads(output_path.read_text(encoding="utf-8"))
        assert ledger["prompt_version"] == "openai-gpt-4.1-caption-context-v1"
        assert ledger["records"][0]["source_context"]["file"] == "image11.png"
        assert ledger["records"][0]["context_package"]["image_id"] == context_package["image_id"]


def main() -> int:
    test_prompt_sanitizes_prior_caption()
    test_runner_passes_context_package_and_persists_it()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
