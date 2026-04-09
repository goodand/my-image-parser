#!/usr/bin/env python3
"""Reusable classes for the local OpenAI per-image caption runner."""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import re
import time
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib import error, request


SUPPORTED_MIME_TYPES = {
    "image/gif",
    "image/jpeg",
    "image/png",
    "image/webp",
}

DEFAULT_MODEL = "gpt-4.1"
DEFAULT_DETAIL = "high"
DEFAULT_MAX_OUTPUT_TOKENS = 700
API_URL = "https://api.openai.com/v1/responses"

PROMPT_VERSION = "openai-gpt-4.1-caption-v1"
PROMPT_VERSION_WITH_CONTEXT = "openai-gpt-4.1-caption-context-v1"
WORKER_AGENT = "openai-caption-runner"
CAPTION_PHASE = "caption"

RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["caption", "alt_text", "structured_metadata"],
    "properties": {
        "caption": {
            "type": "string",
            "description": "One or two factual sentences that describe the image clearly.",
            "maxLength": 320,
        },
        "alt_text": {
            "type": "string",
            "description": "A concise accessibility-style description, ideally under 160 characters.",
            "maxLength": 180,
        },
        "structured_metadata": {
            "type": "object",
            "additionalProperties": False,
            "required": [
                "content_type",
                "primary_subject",
                "notable_elements",
                "visible_text",
            ],
            "properties": {
                "content_type": {
                    "type": "string",
                    "enum": [
                        "photo",
                        "screenshot",
                        "chart",
                        "diagram",
                        "document",
                        "illustration",
                        "mixed",
                    ],
                },
                "primary_subject": {"type": "string", "maxLength": 120},
                "notable_elements": {
                    "type": "array",
                    "items": {"type": "string", "maxLength": 80},
                    "maxItems": 6,
                },
                "visible_text": {
                    "type": "array",
                    "items": {"type": "string", "maxLength": 100},
                    "maxItems": 5,
                },
            },
        },
    },
}


@dataclass
class ApiConfig:
    api_key: str
    api_key_name: str
    model: str
    detail: str
    max_output_tokens: int


@dataclass
class CaptionGeneration:
    response_json: dict[str, Any]
    caption: str
    alt_text: str
    structured_metadata: dict[str, Any]


class CaptionValidationError(RuntimeError):
    """Raised when a structured caption payload is syntactically valid but semantically incomplete."""


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate per-image captions with OpenAI gpt-4.1 and save them to a JSON ledger."
    )
    target_group = parser.add_mutually_exclusive_group(required=True)
    target_group.add_argument("--image", type=Path, help="Single image file to process.")
    target_group.add_argument(
        "--dataset-jsonl",
        type=Path,
        help="JSONL dataset with one image record per line. Uses the `image_path` field.",
    )
    target_group.add_argument(
        "--input-dir",
        type=Path,
        help="Directory of images to process sequentially.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Optional manifest JSON that contains image metadata such as slide numbers.",
    )
    parser.add_argument(
        "--context-package-json",
        type=Path,
        help=(
            "Optional single context-package JSON produced by "
            "build_full_image_ocr_context_package.py."
        ),
    )
    parser.add_argument(
        "--context-package-manifest-jsonl",
        type=Path,
        help=(
            "Optional JSONL manifest of context-package rows produced by "
            "build_full_image_ocr_context_package.py."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Ledger output path. Defaults to "
            "control/project_agent_ops/registry/jobs/image_caption_jobs/<job_id>.json"
        ),
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"OpenAI model to use. Defaults to {DEFAULT_MODEL}.",
    )
    parser.add_argument(
        "--detail",
        choices=["low", "high", "auto"],
        default=DEFAULT_DETAIL,
        help="OpenAI image detail setting.",
    )
    parser.add_argument(
        "--max-output-tokens",
        type=int,
        default=DEFAULT_MAX_OUTPUT_TOKENS,
        help=f"Response token cap. Must be >= 16. Defaults to {DEFAULT_MAX_OUTPUT_TOKENS}.",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Re-run records that previously ended in failed state.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-run all existing records, including completed ones.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Optional maximum number of images to process from the discovered set.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.0,
        help="Optional delay between requests.",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_arg_parser().parse_args(argv)


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_path_key(path_value: str | Path) -> str:
    return unicodedata.normalize("NFC", str(Path(path_value).resolve()))


def natural_sort_key(path: Path) -> list[Any]:
    parts = re.split(r"(\d+)", path.name.lower())
    key: list[Any] = []
    for part in parts:
        if part.isdigit():
            key.append(int(part))
        else:
            key.append(part)
    return key


def infer_mime_type(image_path: Path) -> str | None:
    mime_type, _ = mimetypes.guess_type(image_path.name)
    if mime_type in SUPPORTED_MIME_TYPES:
        return mime_type
    return None


def slugify_filename(text: str, fallback: str, extension: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if not slug:
        slug = fallback
    slug = "-".join(slug.split("-")[:12])[:80].strip("-")
    return f"{slug}{extension.lower()}"


def extract_output_text(response_json: dict[str, Any]) -> str:
    texts: list[str] = []
    for output_item in response_json.get("output", []):
        if output_item.get("type") != "message":
            continue
        for content_item in output_item.get("content", []):
            if content_item.get("type") == "output_text" and isinstance(
                content_item.get("text"), str
            ):
                texts.append(content_item["text"])
    if texts:
        return "\n".join(texts).strip()

    fallback: list[str] = []

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "output_text" and isinstance(node.get("text"), str):
                fallback.append(node["text"])
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(response_json)
    return "\n".join(fallback).strip()


def parse_json_text(raw_text: str) -> dict[str, Any]:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find("{")
        end = raw_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw_text[start : end + 1])
        raise


def has_balanced_pairs(text: str, opening: str, closing: str) -> bool:
    depth = 0
    for char in text:
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def validate_caption_text(caption: str) -> None:
    stripped = caption.strip()
    if not stripped:
        raise CaptionValidationError("Caption completeness validation failed: caption is empty.")

    if len(stripped) < 12:
        raise CaptionValidationError(
            "Caption completeness validation failed: caption is too short to be reliable."
        )

    if stripped[-1] in {"'", '"', "(", "[", "{", ":", ";", ",", "-", "–", "—", "/"}:
        raise CaptionValidationError(
            "Caption completeness validation failed: caption ends with an unfinished token."
        )

    if not has_balanced_pairs(stripped, "(", ")"):
        raise CaptionValidationError(
            "Caption completeness validation failed: caption contains unbalanced parentheses."
        )

    if stripped.count('"') % 2 != 0 or stripped.count("'") % 2 != 0:
        raise CaptionValidationError(
            "Caption completeness validation failed: caption contains unbalanced quotation marks."
        )

    lowered = stripped.lower().rstrip(".?!")
    dangling_patterns = [
        r"\bfor$",
        r"\bwith$",
        r"\bof$",
        r"\band$",
        r"\bor$",
        r"\bto$",
        r"\bin$",
        r"\bon$",
        r"\bat$",
        r"\bby$",
        r"\bfrom$",
        r"\bthe$",
        r"\ba$",
        r"\ban$",
        r"\bcorresponding values for$",
        r"\bdisplays performance metrics for different$",
    ]
    if any(re.search(pattern, lowered) for pattern in dangling_patterns):
        raise CaptionValidationError(
            "Caption completeness validation failed: caption appears to stop mid-phrase."
        )

    terminal_ok = stripped.endswith((".", "!", "?"))
    if len(stripped) >= 80 and not terminal_ok:
        raise CaptionValidationError(
            "Caption completeness validation failed: long caption does not end with terminal punctuation."
        )


def validate_alt_text_text(alt_text: str) -> None:
    stripped = alt_text.strip()
    if not stripped:
        raise CaptionValidationError("Caption completeness validation failed: alt_text is empty.")
    if len(stripped) >= 80 and not stripped.endswith((".", "!", "?")):
        raise CaptionValidationError(
            "Caption completeness validation failed: alt_text appears incomplete."
        )


def validate_generation_payload(
    *,
    response_json: dict[str, Any],
    caption: str,
    alt_text: str,
) -> None:
    if response_json.get("status") == "incomplete":
        reason = (response_json.get("incomplete_details") or {}).get("reason", "unknown")
        raise CaptionValidationError(
            f"Caption completeness validation failed: OpenAI response remained incomplete ({reason})."
        )
    validate_caption_text(caption)
    validate_alt_text_text(alt_text)


def prompt_version_for_context(context_package: dict[str, Any] | None) -> str:
    if context_package:
        return PROMPT_VERSION_WITH_CONTEXT
    return PROMPT_VERSION


def sanitize_context_package_summary(summary: str) -> str:
    cleaned = summary.strip()
    if not cleaned:
        return ""
    marker = " Existing phase-1 caption:"
    if marker in cleaned:
        cleaned = cleaned.split(marker, 1)[0].strip()
    return cleaned


def build_caption_prompt(context_package: dict[str, Any] | None = None) -> str:
    base_prompt = (
        "Return JSON for this image. "
        "Write factual captions only. "
        "Do not speculate about hidden details. "
        "If the image is a screenshot, chart, diagram, or document, describe the visible structure and key labels. "
        "Copy only text that is clearly legible into visible_text. "
        "Keep visible_text short: at most 5 snippets, and each snippet should be brief."
    )
    if not context_package:
        return base_prompt

    context_lines: list[str] = [
        "Supplemental context is provided below.",
        "Use it only to clarify visible text, abbreviations, metric names, or slide-local provenance.",
        "If the supplemental context conflicts with the visible image, trust the image.",
    ]
    slides = context_package.get("source_slide_numbers") or []
    if slides:
        context_lines.append(f"Source slide numbers: {', '.join(str(item) for item in slides)}.")
    ocr_status = context_package.get("ocr_status")
    if isinstance(ocr_status, str) and ocr_status:
        context_lines.append(f"OCR status on the full image: {ocr_status}.")
    ocr_excerpt = (context_package.get("ocr_text_excerpt") or "").strip()
    if ocr_excerpt:
        context_lines.append(f"OCR excerpt from the full image: {ocr_excerpt}")
    summary = sanitize_context_package_summary(str(context_package.get("ppt_local_summary") or ""))
    if summary:
        context_lines.append(f"PPT-local summary: {summary}")
    return base_prompt + "\n\n" + "\n".join(context_lines)


def encode_image_as_data_url(image_path: Path) -> tuple[str, str]:
    mime_type = infer_mime_type(image_path)
    if not mime_type:
        raise ValueError(f"Unsupported image type for OpenAI input: {image_path.suffix}")
    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return mime_type, f"data:{mime_type};base64,{encoded}"


class EnvironmentConfigLoader:
    """Resolve API settings from environment variables or the workspace .env file."""

    @staticmethod
    def load_dotenv(env_path: Path) -> dict[str, str]:
        values: dict[str, str] = {}
        if not env_path.exists():
            return values
        pattern = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$")
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = pattern.match(raw_line)
            if not match:
                continue
            key, value = match.group(1), match.group(2).strip()
            if value and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            values[key] = value
        return values

    @classmethod
    def resolve_api_config(cls, root_dir: Path, args: argparse.Namespace) -> ApiConfig:
        env_map = cls.load_dotenv(root_dir / ".env")
        key_order = ["OPEN_DATA_API_KEY", "OPENAI_API_KEY"]
        for key_name in key_order:
            key_value = os.environ.get(key_name) or env_map.get(key_name)
            if key_value:
                return ApiConfig(
                    api_key=key_value,
                    api_key_name=key_name,
                    model=args.model,
                    detail=args.detail,
                    max_output_tokens=args.max_output_tokens,
                )
        raise RuntimeError(
            "Missing OpenAI API key. Set OPEN_DATA_API_KEY or OPENAI_API_KEY in the environment or .env."
        )


class ImageDiscoveryService:
    """Discover input images and the optional nearby manifest."""

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args

    def discover_images(self) -> list[Path]:
        if self.args.image:
            image_path = self.args.image.resolve()
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            return [image_path]
        if self.args.dataset_jsonl:
            dataset_path = self.args.dataset_jsonl.resolve()
            if not dataset_path.exists():
                raise FileNotFoundError(f"Dataset JSONL not found: {dataset_path}")
            images = []
            for row in SourceContextCatalog.load_dataset_rows(dataset_path):
                image_path = row.get("image_path")
                if not image_path:
                    continue
                path = Path(image_path).resolve()
                if not path.exists():
                    raise FileNotFoundError(f"Dataset image not found: {path}")
                images.append(path)
            return images
        if not self.args.input_dir:
            return []
        input_dir = self.args.input_dir.resolve()
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
        images = [path for path in input_dir.iterdir() if path.is_file()]
        return sorted(images, key=natural_sort_key)

    def discover_manifest(self, images: list[Path]) -> Path | None:
        if self.args.manifest:
            return self.args.manifest.resolve()
        if self.args.dataset_jsonl:
            return None
        search_roots: list[Path] = []
        if self.args.image:
            search_roots.append(self.args.image.resolve().parent)
        if self.args.input_dir:
            search_roots.append(self.args.input_dir.resolve())
        for root in search_roots:
            candidate_paths = [root / "manifest.json", root.parent / "manifest.json"]
            for candidate in candidate_paths:
                if candidate.exists():
                    return candidate.resolve()
        if images:
            candidate_paths = [images[0].parent / "manifest.json", images[0].parent.parent / "manifest.json"]
            for candidate in candidate_paths:
                if candidate.exists():
                    return candidate.resolve()
        return None


class SourceContextCatalog:
    """Build a stable per-image source-context lookup from manifest and dataset artifacts."""

    def __init__(
        self,
        manifest_lookup: dict[str, dict[str, Any]],
        dataset_lookup: dict[str, dict[str, Any]],
    ) -> None:
        self.manifest_lookup = manifest_lookup
        self.dataset_lookup = dataset_lookup

    @classmethod
    def load_dataset_rows(cls, dataset_path: Path) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for line in dataset_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            rows.append(json.loads(stripped))
        return rows

    @classmethod
    def build_manifest_lookup(cls, manifest_path: Path | None) -> dict[str, dict[str, Any]]:
        if not manifest_path or not manifest_path.exists():
            return {}
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        lookup: dict[str, dict[str, Any]] = {}
        for item in data.get("exported_images", []):
            output_path = item.get("output_path")
            if not output_path:
                continue
            lookup[normalize_path_key(output_path)] = item
        return lookup

    @classmethod
    def build_dataset_lookup(cls, dataset_path: Path | None) -> dict[str, dict[str, Any]]:
        if not dataset_path or not dataset_path.exists():
            return {}
        lookup: dict[str, dict[str, Any]] = {}
        for row in cls.load_dataset_rows(dataset_path):
            image_path = row.get("image_path")
            if not image_path:
                continue
            lookup[normalize_path_key(image_path)] = row
        return lookup

    @classmethod
    def from_sources(
        cls, manifest_path: Path | None, dataset_path: Path | None
    ) -> "SourceContextCatalog":
        return cls(
            manifest_lookup=cls.build_manifest_lookup(manifest_path),
            dataset_lookup=cls.build_dataset_lookup(dataset_path),
        )

    def as_lookup(self) -> dict[str, dict[str, Any]]:
        keys = set(self.manifest_lookup) | set(self.dataset_lookup)
        combined: dict[str, dict[str, Any]] = {}
        for key in keys:
            dataset_entry = self.dataset_lookup.get(key)
            manifest_entry = self.manifest_lookup.get(key)
            if dataset_entry and manifest_entry:
                merged = dict(dataset_entry)
                merged["manifest_entry"] = manifest_entry
                combined[key] = merged
            elif dataset_entry:
                combined[key] = dataset_entry
            elif manifest_entry:
                combined[key] = manifest_entry
        return combined

    def lookup_for(self, image_path: Path) -> dict[str, Any] | None:
        return self.as_lookup().get(normalize_path_key(image_path))


class ContextPackageCatalog:
    """Load optional per-image context packages built from standalone OCR baseline artifacts."""

    def __init__(self, context_lookup: dict[str, dict[str, Any]]) -> None:
        self.context_lookup = context_lookup

    @classmethod
    def _rows_from_jsonl(cls, jsonl_path: Path | None) -> list[dict[str, Any]]:
        if not jsonl_path or not jsonl_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in jsonl_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            rows.append(json.loads(stripped))
        return rows

    @classmethod
    def _rows_from_json(cls, json_path: Path | None) -> list[dict[str, Any]]:
        if not json_path or not json_path.exists():
            return []
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            return [payload]
        if isinstance(payload, list):
            return [item for item in payload if isinstance(item, dict)]
        return []

    @classmethod
    def from_sources(
        cls,
        *,
        context_package_json: Path | None,
        context_package_manifest_jsonl: Path | None,
    ) -> "ContextPackageCatalog":
        lookup: dict[str, dict[str, Any]] = {}
        rows = cls._rows_from_jsonl(context_package_manifest_jsonl) + cls._rows_from_json(context_package_json)
        for row in rows:
            source_image_path = row.get("source_image_path")
            if not source_image_path:
                continue
            lookup[normalize_path_key(source_image_path)] = row
        return cls(lookup)

    def lookup_for(self, image_path: Path) -> dict[str, Any] | None:
        return self.context_lookup.get(normalize_path_key(image_path))


class LedgerStore:
    """Persist the main ledger plus sidecar execution and evaluation artifacts."""

    def __init__(
        self,
        *,
        output_path: Path,
        job_id: str,
        config: ApiConfig,
        input_args: argparse.Namespace,
        manifest_path: Path | None,
    ) -> None:
        self.output_path = output_path
        self.job_id = job_id
        self.config = config
        self.input_args = input_args
        self.manifest_path = manifest_path

    @classmethod
    def resolve_output_path(cls, root_dir: Path, output_path: Path | None, job_id: str) -> Path:
        if output_path is None:
            return (
                root_dir
                / "control"
                / "project_agent_ops"
                / "registry"
                / "runs"
                / "image_caption_jobs"
                / f"{job_id}.json"
            )
        return output_path.resolve()

    def raw_response_path_for(self, image_id: str) -> Path:
        return self.output_path.parent / f"{self.output_path.stem}_responses" / f"{image_id}.json"

    def execution_records_path_for(self) -> Path:
        return self.output_path.parent / f"{self.output_path.stem}_execution_records.jsonl"

    def evaluation_decisions_path_for(self) -> Path:
        return self.output_path.parent / f"{self.output_path.stem}_evaluation_decisions.jsonl"

    def load_or_initialize(self) -> dict[str, Any]:
        if self.output_path.exists():
            return json.loads(self.output_path.read_text(encoding="utf-8"))
        return {
            "job_id": self.job_id,
            "created_at": utc_timestamp(),
            "updated_at": utc_timestamp(),
            "model": self.config.model,
            "api_key_env": self.config.api_key_name,
            "input": {
                "image": str(self.input_args.image.resolve()) if self.input_args.image else None,
                "dataset_jsonl": (
                    str(self.input_args.dataset_jsonl.resolve())
                    if self.input_args.dataset_jsonl
                    else None
                ),
                "input_dir": (
                    str(self.input_args.input_dir.resolve()) if self.input_args.input_dir else None
                ),
                "manifest": str(self.manifest_path) if self.manifest_path else None,
                "context_package_json": (
                    str(self.input_args.context_package_json.resolve())
                    if getattr(self.input_args, "context_package_json", None)
                    else None
                ),
                "context_package_manifest_jsonl": (
                    str(self.input_args.context_package_manifest_jsonl.resolve())
                    if getattr(self.input_args, "context_package_manifest_jsonl", None)
                    else None
                ),
            },
            "prompt_version": (
                PROMPT_VERSION_WITH_CONTEXT
                if (
                    getattr(self.input_args, "context_package_json", None)
                    or getattr(self.input_args, "context_package_manifest_jsonl", None)
                )
                else PROMPT_VERSION
            ),
            "records": [],
        }

    def build_record(
        self,
        *,
        index: int,
        image_path: Path,
        source_context_lookup: dict[str, dict[str, Any]],
        context_package_lookup: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        image_id = f"img_{index:06d}"
        source_context = source_context_lookup.get(normalize_path_key(image_path))
        context_package = context_package_lookup.get(normalize_path_key(image_path))
        return {
            "job_id": self.job_id,
            "image_id": image_id,
            "path": str(image_path.resolve()),
            "filename": image_path.name,
            "status": "queued",
            "attempt_count": 0,
            "started_at": None,
            "finished_at": None,
            "caption": None,
            "alt_text": None,
            "structured_metadata": None,
            "caption_model": self.config.model,
            "new_filename_candidate": None,
            "source_context": source_context,
            "context_package": context_package,
            "api_response_id": None,
            "usage": None,
            "raw_response_path": None,
            "last_error": None,
            "updated_at": utc_timestamp(),
        }

    def ensure_records(
        self,
        ledger: dict[str, Any],
        images: list[Path],
        source_context_lookup: dict[str, dict[str, Any]],
        context_package_lookup: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        existing_by_path = {
            normalize_path_key(record["path"]): record for record in ledger.get("records", [])
        }
        records: list[dict[str, Any]] = []
        for index, image_path in enumerate(images, start=1):
            existing = existing_by_path.get(normalize_path_key(image_path))
            if existing:
                if not existing.get("image_id"):
                    existing["image_id"] = f"img_{index:06d}"
                current_source_context = source_context_lookup.get(normalize_path_key(image_path))
                if current_source_context is not None:
                    existing["source_context"] = current_source_context
                current_context_package = context_package_lookup.get(normalize_path_key(image_path))
                if current_context_package is not None:
                    existing["context_package"] = current_context_package
                records.append(existing)
                continue
            records.append(
                self.build_record(
                    index=index,
                    image_path=image_path,
                    source_context_lookup=source_context_lookup,
                    context_package_lookup=context_package_lookup,
                )
            )
        ledger["records"] = records
        return records

    def save_raw_response(self, image_id: str, response_json: dict[str, Any]) -> Path:
        raw_path = self.raw_response_path_for(image_id)
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(
            json.dumps(response_json, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return raw_path

    def build_execution_record(self, record: dict[str, Any]) -> dict[str, Any]:
        status = record.get("status")
        if status == "unsupported_media_type":
            state = "failed"
        elif isinstance(status, str):
            state = status
        else:
            state = "unknown"
        evidence: list[str] = []
        raw_response_path = record.get("raw_response_path")
        if isinstance(raw_response_path, str) and raw_response_path:
            evidence.append(raw_response_path)
        return {
            "job_id": record.get("job_id"),
            "image_id": record.get("image_id"),
            "phase": CAPTION_PHASE,
            "state": state,
            "attempt": record.get("attempt_count", 0),
            "worker_agent": WORKER_AGENT,
            "evidence": evidence,
            "started_at": record.get("started_at"),
            "finished_at": record.get("finished_at"),
            "last_error": record.get("last_error"),
        }

    def build_evaluation_decision(self, record: dict[str, Any]) -> dict[str, Any]:
        status = record.get("status")
        if status == "completed":
            decision = "review_ready"
        elif status in {"failed", "unsupported_media_type"}:
            decision = "error"
        else:
            decision = "pending"
        evidence: list[str] = []
        raw_response_path = record.get("raw_response_path")
        if isinstance(raw_response_path, str) and raw_response_path:
            evidence.append(raw_response_path)
        return {
            "job_id": record.get("job_id"),
            "image_id": record.get("image_id"),
            "source_phase": CAPTION_PHASE,
            "decision": decision,
            "decision_source": "runner_default",
            "gate_enabled": False,
            "upstream_status": status,
            "evidence": evidence,
            "updated_at": record.get("updated_at"),
            "reason": record.get("last_error"),
        }

    def save(self, ledger: dict[str, Any]) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        ledger["updated_at"] = utc_timestamp()
        self.output_path.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        execution_lines = [
            json.dumps(self.build_execution_record(record), ensure_ascii=False)
            for record in ledger.get("records", [])
        ]
        evaluation_lines = [
            json.dumps(self.build_evaluation_decision(record), ensure_ascii=False)
            for record in ledger.get("records", [])
        ]
        self.execution_records_path_for().write_text(
            ("\n".join(execution_lines) + "\n") if execution_lines else "",
            encoding="utf-8",
        )
        self.evaluation_decisions_path_for().write_text(
            ("\n".join(evaluation_lines) + "\n") if evaluation_lines else "",
            encoding="utf-8",
        )

    @staticmethod
    def should_process_record(
        record: dict[str, Any],
        *,
        overwrite: bool,
        retry_failed: bool,
    ) -> bool:
        if overwrite:
            return True
        status = record.get("status")
        if status == "completed":
            return False
        if status == "failed":
            return retry_failed
        if status == "unsupported_media_type":
            return False
        return True

    @staticmethod
    def summarize_statuses(records: list[dict[str, Any]]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for record in records:
            status = record.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
        return counts


class OpenAIResponsesCaptionClient:
    """Thin Responses API client that returns already-parsed caption payloads."""

    def __init__(self, config: ApiConfig) -> None:
        self.config = config

    def _openai_request(
        self,
        image_path: Path,
        *,
        context_package: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        mime_type, data_url = encode_image_as_data_url(image_path)
        prompt = build_caption_prompt(context_package)
        token_budgets = [
            self.config.max_output_tokens,
            max(self.config.max_output_tokens * 2, 900),
        ]
        last_response: dict[str, Any] | None = None
        for token_budget in token_budgets:
            payload = {
                "model": self.config.model,
                "instructions": (
                    "You are an image captioning system for asset management. "
                    "Return structured JSON only."
                ),
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {
                                "type": "input_image",
                                "image_url": data_url,
                                "detail": self.config.detail,
                            },
                        ],
                    }
                ],
                "text": {
                    "format": {
                        "type": "json_schema",
                        "name": "image_caption_record",
                        "strict": True,
                        "schema": RESPONSE_SCHEMA,
                    }
                },
                "max_output_tokens": token_budget,
                "metadata": {
                    "pipeline": "per_image_caption_runner",
                    "mime_type": mime_type,
                    "prompt_version": prompt_version_for_context(context_package),
                },
            }
            req = request.Request(
                API_URL,
                method="POST",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json",
                },
            )
            try:
                with request.urlopen(req, timeout=120) as response:
                    response_json = json.loads(response.read().decode("utf-8"))
            except error.HTTPError as exc:
                body = exc.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"OpenAI API error {exc.code}: {body}") from exc

            last_response = response_json
            reason = (response_json.get("incomplete_details") or {}).get("reason")
            if response_json.get("status") != "incomplete" or reason != "max_output_tokens":
                return response_json

        if last_response is None:
            raise RuntimeError("OpenAI API returned no response.")
        return last_response

    def generate_caption(
        self,
        image_path: Path,
        *,
        source_context: dict[str, Any] | None = None,
        context_package: dict[str, Any] | None = None,
    ) -> CaptionGeneration:
        del source_context
        response_json = self._openai_request(image_path, context_package=context_package)
        raw_text = extract_output_text(response_json)
        parsed = parse_json_text(raw_text)
        caption = parsed["caption"].strip()
        alt_text = parsed["alt_text"].strip()
        validate_generation_payload(
            response_json=response_json,
            caption=caption,
            alt_text=alt_text,
        )
        return CaptionGeneration(
            response_json=response_json,
            caption=caption,
            alt_text=alt_text,
            structured_metadata=parsed["structured_metadata"],
        )


class CaptionJobRunner:
    """End-to-end orchestration for a resumable local per-image caption job."""

    def __init__(
        self,
        args: argparse.Namespace,
        *,
        root_dir: Path | None = None,
        config: ApiConfig | None = None,
        client: OpenAIResponsesCaptionClient | Any | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self.args = args
        self.root_dir = root_dir or Path(__file__).resolve().parents[1]
        self.config = config or EnvironmentConfigLoader.resolve_api_config(self.root_dir, args)
        self.client = client or OpenAIResponsesCaptionClient(self.config)
        self.sleep_fn = sleep_fn

    def run(self) -> dict[str, Any]:
        if self.args.max_output_tokens < 16:
            raise ValueError("--max-output-tokens must be at least 16.")

        discovery = ImageDiscoveryService(self.args)
        images = discovery.discover_images()
        if not images:
            raise RuntimeError("No input images found.")
        if self.args.limit is not None:
            images = images[: self.args.limit]

        manifest_path = discovery.discover_manifest(images)
        catalog = SourceContextCatalog.from_sources(
            manifest_path=manifest_path,
            dataset_path=self.args.dataset_jsonl.resolve() if self.args.dataset_jsonl else None,
        )
        source_context_lookup = catalog.as_lookup()
        context_catalog = ContextPackageCatalog.from_sources(
            context_package_json=self.args.context_package_json.resolve()
            if self.args.context_package_json
            else None,
            context_package_manifest_jsonl=self.args.context_package_manifest_jsonl.resolve()
            if self.args.context_package_manifest_jsonl
            else None,
        )
        context_package_lookup = context_catalog.context_lookup

        generated_job_id = f"job_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        output_path = LedgerStore.resolve_output_path(self.root_dir, self.args.output, generated_job_id)
        store = LedgerStore(
            output_path=output_path,
            job_id=generated_job_id,
            config=self.config,
            input_args=self.args,
            manifest_path=manifest_path,
        )
        ledger = store.load_or_initialize()
        if ledger.get("job_id"):
            store.job_id = str(ledger["job_id"])
        records = store.ensure_records(ledger, images, source_context_lookup, context_package_lookup)
        store.save(ledger)

        processed_count = 0
        for record in records:
            image_path = Path(record["path"])
            if not store.should_process_record(
                record,
                overwrite=self.args.overwrite,
                retry_failed=self.args.retry_failed,
            ):
                continue

            mime_type = infer_mime_type(image_path)
            if not mime_type:
                record["status"] = "unsupported_media_type"
                record["last_error"] = f"Unsupported type: {image_path.suffix}"
                record["finished_at"] = utc_timestamp()
                record["updated_at"] = utc_timestamp()
                store.save(ledger)
                continue

            record["status"] = "running"
            record["attempt_count"] = int(record.get("attempt_count", 0)) + 1
            record["started_at"] = utc_timestamp()
            record["finished_at"] = None
            record["last_error"] = None
            record["updated_at"] = utc_timestamp()
            store.save(ledger)

            try:
                generation = self.client.generate_caption(
                    image_path,
                    source_context=record.get("source_context"),
                    context_package=record.get("context_package"),
                )
                raw_path = store.save_raw_response(record["image_id"], generation.response_json)
                candidate_name = slugify_filename(
                    generation.caption,
                    fallback=record["image_id"],
                    extension=image_path.suffix or ".png",
                )
                record["status"] = "completed"
                record["caption"] = generation.caption
                record["alt_text"] = generation.alt_text
                record["structured_metadata"] = generation.structured_metadata
                record["new_filename_candidate"] = candidate_name
                record["api_response_id"] = generation.response_json.get("id")
                record["usage"] = generation.response_json.get("usage")
                record["raw_response_path"] = str(raw_path)
                record["last_error"] = None
                record["finished_at"] = utc_timestamp()
                record["updated_at"] = utc_timestamp()
                processed_count += 1
            except Exception as exc:  # noqa: BLE001
                record["status"] = "failed"
                record["last_error"] = str(exc)
                record["finished_at"] = utc_timestamp()
                record["updated_at"] = utc_timestamp()
            finally:
                store.save(ledger)

            if self.args.sleep_seconds > 0:
                self.sleep_fn(self.args.sleep_seconds)

        return {
            "job_id": ledger["job_id"],
            "output_path": str(output_path),
            "execution_records_path": str(store.execution_records_path_for()),
            "evaluation_decisions_path": str(store.evaluation_decisions_path_for()),
            "model": self.config.model,
            "api_key_env": self.config.api_key_name,
            "processed_count": processed_count,
            "status_counts": store.summarize_statuses(records),
        }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        summary = CaptionJobRunner(args).run()
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0
