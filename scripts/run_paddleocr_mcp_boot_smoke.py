#!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import traceback
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from table_parser_sidecar_promotion_lib import (
    load_slide_usages,
    normalize_first_table_from_text_items,
    resolve_manifest_for_image,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = (
    ROOT_DIR
    / "control"
    / "project_domain"
    / "resources"
    / "pptx_jobs"
    / "01_full_presentation_2026-03-17"
    / "media"
    / "image11.png"
)
DEFAULT_OUTPUT = (
    ROOT_DIR
    / "control"
    / "project_agent_ops"
    / "resources"
    / "smoke"
    / "artifacts"
    / "paddleocr_mcp_boot_smoke_at2026_03_28.json"
)
SERVER_COMMAND = str(ROOT_DIR / "scripts" / "mcp" / "start-paddleocr-mcp.sh")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a bounded PaddleOCR MCP stdio boot smoke and one PP-StructureV3 call."
    )
    parser.add_argument(
        "--image-path",
        default=str(DEFAULT_IMAGE),
        help="Absolute path to a real PPT-extracted image used for bounded PP-StructureV3 smoke.",
    )
    parser.add_argument(
        "--output-json",
        default=str(DEFAULT_OUTPUT),
        help="Path to write the machine-readable smoke result.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=240,
        help="Client initialize and call timeout in seconds.",
    )
    parser.add_argument(
        "--output-mode",
        choices=["simple", "detailed"],
        default="simple",
        help="PP-StructureV3 output mode.",
    )
    parser.add_argument(
        "--raw-content-json",
        default="",
        help="Optional path to persist raw content items from the tool call.",
    )
    parser.add_argument(
        "--normalized-output-json",
        default="",
        help="Optional path to persist the first-table normalization into canonical Table->Row->Cell JSON.",
    )
    return parser.parse_args()


def _extract_text_preview(tool_result: Any) -> str | None:
    for item in getattr(tool_result, "content", []) or []:
        text = getattr(item, "text", None)
        if text:
            return text[:1200]
    structured = getattr(tool_result, "structured_content", None)
    if structured is not None:
        return str(structured)[:1200]
    return None


def _serialize_tool_content(tool_result: Any) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []
    for item in getattr(tool_result, "content", []) or []:
        entry: dict[str, Any] = {"type": getattr(item, "type", None)}
        if hasattr(item, "text"):
            entry["text"] = getattr(item, "text")
        if hasattr(item, "mimeType"):
            entry["mimeType"] = getattr(item, "mimeType")
        if hasattr(item, "data"):
            data = getattr(item, "data")
            entry["data_length"] = len(data) if isinstance(data, str) else None
        serialized.append(entry)
    return serialized


async def _run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    image_path = Path(args.image_path).resolve()
    if not image_path.is_file():
        raise FileNotFoundError(f"Smoke image not found: {image_path}")

    output_path = Path(args.output_json).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    experiment_name = (
        "paddleocr_table_parse_smoke"
        if args.output_mode == "detailed" or args.raw_content_json or args.normalized_output_json
        else "paddleocr_mcp_boot_smoke"
    )

    result: dict[str, Any] = {
        "experiment": experiment_name,
        "server_command": SERVER_COMMAND,
        "image_path": str(image_path),
        "status": "started",
        "tool_names": [],
        "call_tool": "pp_structurev3",
        "call_args": {
            "input_data": str(image_path),
            "output_mode": args.output_mode,
            "return_images": False,
        },
    }

    params = StdioServerParameters(command=SERVER_COMMAND, args=[], cwd=str(ROOT_DIR))

    try:
        async with stdio_client(params) as streams:
            async with ClientSession(*streams) as session:
                await asyncio.wait_for(session.initialize(), timeout=args.timeout_seconds)
                result["initialized"] = True

                tools = await asyncio.wait_for(session.list_tools(), timeout=args.timeout_seconds)
                result["tool_names"] = [tool.name for tool in tools.tools]

                tool_result = await asyncio.wait_for(
                    session.call_tool(
                        "pp_structurev3",
                        {
                            "input_data": str(image_path),
                            "output_mode": args.output_mode,
                            "return_images": False,
                        },
                    ),
                    timeout=args.timeout_seconds,
                )
                result["status"] = "completed"
                result["content_item_count"] = len(getattr(tool_result, "content", []) or [])
                result["text_preview"] = _extract_text_preview(tool_result)
                text_items = [
                    item["text"]
                    for item in _serialize_tool_content(tool_result)
                    if item.get("type") == "text" and item.get("text")
                ]
                manifest_path = resolve_manifest_for_image(image_path)
                slide_usages = load_slide_usages(manifest_path, image_path.name)
                result["slide_usages"] = slide_usages

                if args.raw_content_json:
                    raw_output_path = Path(args.raw_content_json).resolve()
                    raw_output_path.parent.mkdir(parents=True, exist_ok=True)
                    raw_output_path.write_text(
                        json.dumps(
                            {
                                "image_path": str(image_path),
                                "output_mode": args.output_mode,
                                "content": _serialize_tool_content(tool_result),
                            },
                            ensure_ascii=False,
                            indent=2,
                        ),
                        encoding="utf-8",
                    )
                    result["raw_content_json"] = str(raw_output_path)

                if args.normalized_output_json:
                    normalized = normalize_first_table_from_text_items(
                        image_path=image_path,
                        text_items=text_items,
                        slide_usages=slide_usages,
                    )
                    normalized_output_path = Path(args.normalized_output_json).resolve()
                    normalized_output_path.parent.mkdir(parents=True, exist_ok=True)
                    normalized_output_path.write_text(
                        json.dumps(normalized, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    result["normalized_output_json"] = str(normalized_output_path)
                    result["normalized_status"] = "completed" if normalized else "no_table_found"
    except Exception as exc:
        result["status"] = "failed"
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
        result["traceback"] = traceback.format_exc(limit=8)

    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


def main() -> None:
    args = _parse_args()
    result = asyncio.run(_run_smoke(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
