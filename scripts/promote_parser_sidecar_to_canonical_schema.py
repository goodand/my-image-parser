#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from table_parser_sidecar_promotion_lib import promote_raw_sidecar_to_canonical


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT_DIR / "control" / "project_domain" / "resources" / "manifests"
DEFAULT_RESULT_ROOT = ROOT_DIR / "control" / "project_agent_ops" / "resources" / "smoke" / "artifacts"


def _default_normalized_output(raw_sidecar_json: Path, output_root: Path) -> Path:
    stem = raw_sidecar_json.stem
    if "_raw_" in stem:
        stem = stem.replace("_raw_", "_normalized_")
    else:
        stem = f"{stem}_normalized"
    return output_root / f"{stem}.json"


def _default_result_output(raw_sidecar_json: Path, output_root: Path) -> Path:
    return output_root / f"{raw_sidecar_json.stem}_promotion_result.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Promote a parser raw sidecar artifact into the canonical Table -> Row -> Cell JSON shape."
    )
    parser.add_argument("--raw-sidecar-json", required=True, help="Raw parser sidecar JSON artifact.")
    parser.add_argument(
        "--normalized-output-json",
        default="",
        help="Output path for the canonical normalized JSON. Defaults under control/project_domain/resources/manifests/.",
    )
    parser.add_argument(
        "--output-json",
        default="",
        help="Machine-readable promotion result output. Defaults under control/project_agent_ops/resources/smoke/artifacts/.",
    )
    parser.add_argument(
        "--image-path",
        default="",
        help="Optional override for the source image path. Defaults to raw sidecar image_path.",
    )
    parser.add_argument("--table-id", default="t1", help="Canonical table_id to emit.")
    parser.add_argument(
        "--parser-backend",
        default="paddleocr-mcp/pp_structurev3",
        help="Parser backend label written into the canonical record.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_sidecar_json = Path(args.raw_sidecar_json).resolve()
    normalized_output_json = (
        Path(args.normalized_output_json).resolve()
        if args.normalized_output_json
        else _default_normalized_output(raw_sidecar_json, DEFAULT_OUTPUT_ROOT.resolve())
    )
    output_json = (
        Path(args.output_json).resolve()
        if args.output_json
        else _default_result_output(raw_sidecar_json, DEFAULT_RESULT_ROOT.resolve())
    )

    result = promote_raw_sidecar_to_canonical(
        raw_sidecar_json=raw_sidecar_json,
        image_path=Path(args.image_path).resolve() if args.image_path else None,
        table_id=args.table_id,
        parser_backend=args.parser_backend,
    )

    normalized_output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)

    if result.normalized_record is not None:
        normalized_output_json.write_text(
            json.dumps(result.normalized_record, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    rows = result.normalized_record.get("rows", []) if result.normalized_record else []
    cell_count = sum(len(row.get("cells", [])) for row in rows)
    payload = {
        "experiment": "parser_sidecar_to_canonical_schema_promotion",
        "raw_sidecar_json": str(result.raw_sidecar_json),
        "image_path": str(result.image_path),
        "manifest_path": str(result.manifest_path) if result.manifest_path else "",
        "normalized_status": result.normalized_status,
        "normalized_output_json": str(normalized_output_json) if result.normalized_record else "",
        "document_id": result.normalized_record.get("document_id") if result.normalized_record else "",
        "page": result.normalized_record.get("page") if result.normalized_record else None,
        "table_id": result.normalized_record.get("table_id") if result.normalized_record else "",
        "row_count": len(rows),
        "cell_count": cell_count,
        "parser_backend": result.normalized_record.get("parser_backend") if result.normalized_record else args.parser_backend,
    }
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
