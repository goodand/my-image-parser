from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request

from caption_runner_lib import (
    API_URL,
    EnvironmentConfigLoader,
    encode_image_as_data_url,
    extract_output_text,
    parse_json_text,
)


DIRECT_VERIFICATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "decision",
        "winner_surface",
        "confidence",
        "full_image_scores",
        "reviewed_component_scores",
        "key_observations",
        "rationale",
    ],
    "properties": {
        "decision": {
            "type": "string",
            "enum": [
                "promote_reviewed_component",
                "keep_full_image",
                "inconclusive",
            ],
        },
        "winner_surface": {
            "type": "string",
            "enum": [
                "full_image_original",
                "reviewed_table_component_crop",
                "inconclusive",
            ],
        },
        "confidence": {
            "type": "string",
            "enum": ["high", "medium", "low"],
        },
        "full_image_scores": {
            "type": "object",
            "additionalProperties": False,
            "required": ["table_completeness", "caption_fitness", "noise_suppression"],
            "properties": {
                "table_completeness": {"type": "integer", "minimum": 1, "maximum": 5},
                "caption_fitness": {"type": "integer", "minimum": 1, "maximum": 5},
                "noise_suppression": {"type": "integer", "minimum": 1, "maximum": 5},
            },
        },
        "reviewed_component_scores": {
            "type": "object",
            "additionalProperties": False,
            "required": ["table_completeness", "caption_fitness", "noise_suppression"],
            "properties": {
                "table_completeness": {"type": "integer", "minimum": 1, "maximum": 5},
                "caption_fitness": {"type": "integer", "minimum": 1, "maximum": 5},
                "noise_suppression": {"type": "integer", "minimum": 1, "maximum": 5},
            },
        },
        "key_observations": {
            "type": "array",
            "items": {"type": "string", "maxLength": 240},
            "minItems": 2,
            "maxItems": 6,
        },
        "rationale": {"type": "string", "maxLength": 900},
    },
}


@dataclass(frozen=True)
class DirectVerificationConfig:
    model: str = "gpt-4.1"
    detail: str = "high"
    max_output_tokens: int = 900


def load_json(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _context_brief(label: str, context_package: dict[str, Any]) -> str:
    if not context_package:
        return f"{label}: no context package provided."
    selected = context_package.get("selected_text_evidence") or []
    slides = context_package.get("source_slide_numbers") or []
    fields = [
        f"{label} review_status={context_package.get('review_status') or 'n/a'}",
        f"{label} context_variant={context_package.get('context_variant') or 'n/a'}",
        f"{label} image_surface={context_package.get('image_surface') or 'n/a'}",
        f"{label} source_slide_numbers={slides or 'n/a'}",
        f"{label} ocr_excerpt={context_package.get('ocr_text_excerpt') or 'n/a'}",
        f"{label} selected_text_evidence={selected or 'n/a'}",
    ]
    return "\n".join(fields)


def build_direct_verification_prompt(
    *,
    full_context_package: dict[str, Any],
    reviewed_context_package: dict[str, Any],
) -> str:
    return (
        "You are judging whether a reviewed table crop should be promoted as a better image input "
        "for caption generation than the original full extracted image of the same slide.\n\n"
        "Image 1 is the full original image.\n"
        "Image 2 is the reviewed isolated table crop from Image 1.\n\n"
        "Decide which image is better for generating a factual caption of the table content.\n"
        "Focus on:\n"
        "1. preserving the full table and important cells\n"
        "2. keeping metric names and relation structure visible\n"
        "3. suppressing non-table noise\n"
        "4. avoiding over-tight crops that lose useful context\n\n"
        "If Image 2 is clearly better and still preserves the full table, return "
        "`promote_reviewed_component`.\n"
        "If Image 1 remains safer or more complete, return `keep_full_image`.\n"
        "If too close or ambiguous, return `inconclusive`.\n"
        "Judge from visible pixels first. Use the supplied context notes only as secondary clues.\n\n"
        f"{_context_brief('Full image', full_context_package)}\n\n"
        f"{_context_brief('Reviewed crop', reviewed_context_package)}"
    )


def run_direct_verification(
    *,
    root_dir: Path,
    full_image_path: Path,
    reviewed_component_image_path: Path,
    full_context_package: dict[str, Any],
    reviewed_context_package: dict[str, Any],
    config: DirectVerificationConfig,
) -> dict[str, Any]:
    class Args:
        model = config.model
        detail = config.detail
        max_output_tokens = config.max_output_tokens

    api_config = EnvironmentConfigLoader.resolve_api_config(root_dir, Args())
    _, full_url = encode_image_as_data_url(full_image_path)
    _, reviewed_url = encode_image_as_data_url(reviewed_component_image_path)
    payload = {
        "model": api_config.model,
        "instructions": "Return structured JSON only.",
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": build_direct_verification_prompt(
                            full_context_package=full_context_package,
                            reviewed_context_package=reviewed_context_package,
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": full_url,
                        "detail": api_config.detail,
                    },
                    {
                        "type": "input_image",
                        "image_url": reviewed_url,
                        "detail": api_config.detail,
                    },
                ],
            }
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "reviewed_component_direct_verification",
                "strict": True,
                "schema": DIRECT_VERIFICATION_SCHEMA,
            }
        },
        "max_output_tokens": api_config.max_output_tokens,
        "metadata": {
            "pipeline": "reviewed_component_direct_verification",
            "source_image_path": str(full_image_path.resolve()),
            "reviewed_component_image_path": str(reviewed_component_image_path.resolve()),
        },
    }
    req = request.Request(
        API_URL,
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_config.api_key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=180) as response:
            response_json = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {body}") from exc

    parsed = parse_json_text(extract_output_text(response_json))
    return {
        "source_image_path": str(full_image_path.resolve()),
        "reviewed_component_image_path": str(reviewed_component_image_path.resolve()),
        "model": api_config.model,
        "prompt_kind": "reviewed_component_direct_verification_v1",
        "full_context_review_status": full_context_package.get("review_status"),
        "reviewed_context_review_status": reviewed_context_package.get("review_status"),
        "result": parsed,
        "api_response_id": response_json.get("id"),
        "usage": response_json.get("usage"),
        "raw_response": response_json,
    }


def render_direct_verification_report(result: dict[str, Any]) -> str:
    payload = result["result"]
    lines = [
        "# Reviewed Component Direct Verification",
        "",
        "## Scope",
        "",
        f"- source_image_path: `{result['source_image_path']}`",
        f"- reviewed_component_image_path: `{result['reviewed_component_image_path']}`",
        f"- model: `{result['model']}`",
        f"- prompt_kind: `{result['prompt_kind']}`",
        f"- full_context_review_status: `{result['full_context_review_status'] or 'n/a'}`",
        f"- reviewed_context_review_status: `{result['reviewed_context_review_status'] or 'n/a'}`",
        "",
        "## Verdict",
        "",
        f"- decision: `{payload['decision']}`",
        f"- winner_surface: `{payload['winner_surface']}`",
        f"- confidence: `{payload['confidence']}`",
        "",
        "## Scores",
        "",
        f"- full_image_scores: `{payload['full_image_scores']}`",
        f"- reviewed_component_scores: `{payload['reviewed_component_scores']}`",
        "",
        "## Observations",
        "",
    ]
    for observation in payload["key_observations"]:
        lines.append(f"- {observation}")
    lines.extend(
        [
            "",
            "## Rationale",
            "",
            payload["rationale"],
            "",
        ]
    )
    return "\n".join(lines)
