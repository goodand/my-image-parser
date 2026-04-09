#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from alpha_component_lib import (
    DEFAULT_ALPHA_THRESHOLD,
    DEFAULT_MIN_COMPONENTS_FOR_SUCCESS,
    DEFAULT_MIN_PIXELS,
    DEFAULT_PADDING,
    run_alpha_split,
)
from full_image_ocr_context_package_lib import (
    build_ocr_text_excerpt,
    determine_ocr_status,
    find_manifest_record,
    run_full_image_ocr,
)


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = ROOT_DIR / "control" / "project_domain" / "runs" / "component_split_ocr"


@dataclass(frozen=True)
class ComponentRow:
    component_index: int
    pixel_count: int
    bbox: list[int]
    output_path: str
    ocr_status: str
    ocr_annotation_count: int
    ocr_text_excerpt: str
    ocr_result_json_path: str | None
    notes: list[str]


@dataclass(frozen=True)
class ComponentSplitPackage:
    image_id: str
    source_image_path: str
    source_dataset: str
    source_pptx: str | None
    source_slide_numbers: list[int]
    alpha_component_count: int
    alpha_reason: str
    output_dir: str
    component_table_markdown_path: str
    component_table_json_path: str
    rows: list[ComponentRow]


@dataclass(frozen=True)
class ComponentSplitOcrConfig:
    alpha_threshold: int = DEFAULT_ALPHA_THRESHOLD
    min_pixels: int = DEFAULT_MIN_PIXELS
    padding: int = DEFAULT_PADDING
    min_components_for_success: int = DEFAULT_MIN_COMPONENTS_FOR_SUCCESS
    ocr_runner: Callable[[Path], dict[str, Any]] = run_full_image_ocr


def repo_root_from_script() -> Path:
    return ROOT_DIR


def default_output_root() -> Path:
    return DEFAULT_OUTPUT_ROOT


def image_identity(image_path: Path) -> tuple[str, str, str | None, list[int]]:
    manifest_record = find_manifest_record(image_path)
    if manifest_record is None:
        return image_path.stem, "unknown", None, []
    return (
        f"{manifest_record.dataset}:{image_path.name}",
        manifest_record.dataset,
        manifest_record.source_filename,
        manifest_record.slide_numbers,
    )


def _safe_excerpt(text: str) -> str:
    if "|" in text:
        text = text.replace("|", "\\|")
    return text


class ComponentSplitOcrService:
    def __init__(self, config: ComponentSplitOcrConfig | None = None) -> None:
        self.config = config or ComponentSplitOcrConfig()

    def build_component_rows(
        self,
        image_path: Path,
        output_dir: Path,
    ) -> tuple[dict[str, Any], list[ComponentRow]]:
        alpha_result = run_alpha_split(
            source_image=image_path,
            output_dir=output_dir,
            alpha_threshold=self.config.alpha_threshold,
            min_pixels=self.config.min_pixels,
            padding=self.config.padding,
            min_components_for_success=self.config.min_components_for_success,
        )
        rows: list[ComponentRow] = []
        ocr_dir = output_dir / "component_ocr"
        ocr_dir.mkdir(parents=True, exist_ok=True)
        for component in alpha_result.get("components", []):
            component_path = Path(component["output_path"])
            ocr_result = self.config.ocr_runner(component_path)
            ocr_status = determine_ocr_status(ocr_result)
            ocr_result_json_path = ocr_dir / f"component_{component['index']:02d}_OCR_RESULT.json"
            ocr_result_json_path.write_text(json.dumps(ocr_result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            rows.append(
                ComponentRow(
                    component_index=int(component["index"]),
                    pixel_count=int(component["pixel_count"]),
                    bbox=[int(value) for value in component["bbox"]],
                    output_path=str(component_path),
                    ocr_status=ocr_status,
                    ocr_annotation_count=int(ocr_result.get("annotation_count") or 0),
                    ocr_text_excerpt=build_ocr_text_excerpt(ocr_result),
                    ocr_result_json_path=str(ocr_result_json_path),
                    notes=[str(ocr_result.get("error"))] if ocr_result.get("error") else [],
                )
            )
        return alpha_result, rows

    def write_component_package(
        self,
        image_path: Path,
        output_root: Path,
    ) -> ComponentSplitPackage:
        image_id, dataset, source_pptx, slide_numbers = image_identity(image_path)
        package_dir = output_root / dataset / image_path.stem
        package_dir.mkdir(parents=True, exist_ok=True)
        alpha_result, rows = self.build_component_rows(
            image_path=image_path,
            output_dir=package_dir,
        )
        component_table_markdown_path = package_dir / "COMPONENT_SPLIT_OCR_REPORT.md"
        component_table_json_path = package_dir / "COMPONENT_SPLIT_OCR_REPORT.json"
        package = ComponentSplitPackage(
            image_id=image_id,
            source_image_path=str(image_path.resolve()),
            source_dataset=dataset,
            source_pptx=source_pptx,
            source_slide_numbers=slide_numbers,
            alpha_component_count=int(alpha_result.get("component_count") or 0),
            alpha_reason=str(alpha_result.get("reason") or ""),
            output_dir=str(package_dir.resolve()),
            component_table_markdown_path=str(component_table_markdown_path.resolve()),
            component_table_json_path=str(component_table_json_path.resolve()),
            rows=rows,
        )
        component_table_markdown_path.write_text(render_component_table_markdown(package), encoding="utf-8")
        component_table_json_path.write_text(json.dumps(asdict(package), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return package


def build_component_rows(
    image_path: Path,
    output_dir: Path,
    *,
    alpha_threshold: int = DEFAULT_ALPHA_THRESHOLD,
    min_pixels: int = DEFAULT_MIN_PIXELS,
    padding: int = DEFAULT_PADDING,
    min_components_for_success: int = DEFAULT_MIN_COMPONENTS_FOR_SUCCESS,
    ocr_runner: Callable[[Path], dict[str, Any]] = run_full_image_ocr,
) -> tuple[dict[str, Any], list[ComponentRow]]:
    service = ComponentSplitOcrService(
        ComponentSplitOcrConfig(
            alpha_threshold=alpha_threshold,
            min_pixels=min_pixels,
            padding=padding,
            min_components_for_success=min_components_for_success,
            ocr_runner=ocr_runner,
        )
    )
    return service.build_component_rows(image_path=image_path, output_dir=output_dir)


def render_component_table_markdown(package: ComponentSplitPackage) -> str:
    slides = ", ".join(str(item) for item in package.source_slide_numbers) or "n/a"
    lines = [
        "# Component Split OCR Report",
        "",
        "## Source",
        "",
        f"- image_id: `{package.image_id}`",
        f"- source_image_path: `{package.source_image_path}`",
        f"- source_dataset: `{package.source_dataset}`",
        f"- source_pptx: `{package.source_pptx or 'n/a'}`",
        f"- source_slide_numbers: `{slides}`",
        f"- alpha_component_count: `{package.alpha_component_count}`",
        f"- alpha_reason: {package.alpha_reason}",
        "",
        "## Component Table",
        "",
        "| index | pixels | bbox | image | ocr_status | annotations | ocr_excerpt |",
        "| --- | ---: | --- | --- | --- | ---: | --- |",
    ]
    if not package.rows:
        lines.append("| - | - | - | - | - | - | no components exported |")
    else:
        for row in package.rows:
            rel_image = Path(row.output_path).resolve().relative_to(Path(package.output_dir).resolve())
            excerpt = _safe_excerpt(row.ocr_text_excerpt or "")
            lines.append(
                f"| {row.component_index} | {row.pixel_count} | `{row.bbox}` | "
                f"[`{rel_image}`]({rel_image.as_posix()}) | `{row.ocr_status}` | "
                f"{row.ocr_annotation_count} | {excerpt or '_empty_'} |"
            )

    lines.extend(["", "## Component Details", ""])
    for row in package.rows:
        rel_image = Path(row.output_path).resolve().relative_to(Path(package.output_dir).resolve()).as_posix()
        lines.extend(
            [
                f"### Component {row.component_index:02d}",
                "",
                f"![component_{row.component_index:02d}]({rel_image})",
                "",
                f"- pixel_count: `{row.pixel_count}`",
                f"- bbox: `{row.bbox}`",
                f"- ocr_status: `{row.ocr_status}`",
                f"- ocr_annotation_count: `{row.ocr_annotation_count}`",
                f"- ocr_result_json_path: `{row.ocr_result_json_path or 'n/a'}`",
                "",
                "OCR excerpt:",
                "",
                row.ocr_text_excerpt or "_empty_",
                "",
            ]
        )
        if row.notes:
            lines.append("Notes:")
            lines.append("")
            for note in row.notes:
                lines.append(f"- {note}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_component_package(
    image_path: Path,
    output_root: Path,
    *,
    alpha_threshold: int = DEFAULT_ALPHA_THRESHOLD,
    min_pixels: int = DEFAULT_MIN_PIXELS,
    padding: int = DEFAULT_PADDING,
    min_components_for_success: int = DEFAULT_MIN_COMPONENTS_FOR_SUCCESS,
    ocr_runner: Callable[[Path], dict[str, Any]] = run_full_image_ocr,
) -> ComponentSplitPackage:
    service = ComponentSplitOcrService(
        ComponentSplitOcrConfig(
            alpha_threshold=alpha_threshold,
            min_pixels=min_pixels,
            padding=padding,
            min_components_for_success=min_components_for_success,
            ocr_runner=ocr_runner,
        )
    )
    return service.write_component_package(image_path=image_path, output_root=output_root)
