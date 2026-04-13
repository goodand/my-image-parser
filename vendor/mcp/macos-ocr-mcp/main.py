import io
import json
import os
import platform
import subprocess

from mcp.server.fastmcp import FastMCP
from ocrmac import ocrmac as ocrmac_module
from PIL import Image

mcp = FastMCP()


def _normalize_image_for_ocr(pil_image: Image.Image) -> Image.Image:
    """Flatten alpha channels so macOS Vision sees an opaque RGB surface."""
    image = pil_image.copy()
    if image.mode in {"RGBA", "LA"} or (image.mode == "P" and "transparency" in image.info):
        rgba_image = image.convert("RGBA")
        background = Image.new("RGBA", rgba_image.size, (255, 255, 255, 255))
        image = Image.alpha_composite(background, rgba_image).convert("RGB")
    elif image.mode != "RGB":
        image = image.convert("RGB")
    return image


def _process_annotations(raw_annotations) -> list[dict]:
    if not raw_annotations:
        return []

    processed_annotations = []
    for ann in raw_annotations:
        if not ann:
            continue
        text = ann[0] if len(ann) > 0 else ""
        confidence = ann[1] if len(ann) > 1 else None
        bounding_box = ann[2] if len(ann) > 2 else None
        processed_annotations.append(
            {
                "text": text,
                "confidence": confidence,
                "bounding_box": bounding_box,
            }
        )
    return processed_annotations


def _workspace_root() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def _swift_fallback_script() -> str:
    return os.path.join(_workspace_root(), "scripts", "ocr", "macos_vision_ocr.swift")


def _run_swift_fallback(file_path: str) -> dict | None:
    script_path = _swift_fallback_script()
    if not os.path.isfile(script_path):
        return None

    completed = subprocess.run(
        ["xcrun", "swift", script_path, file_path],
        capture_output=True,
        text=True,
        check=False,
    )

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        return {
            "error": f"Fallback OCR failed: {stderr or 'unknown swift fallback error'}"
        }

    stdout = completed.stdout.strip()
    if not stdout:
        return {
            "error": "Fallback OCR failed: empty stdout from swift fallback."
        }

    try:
        parsed = json.loads(stdout)
    except json.JSONDecodeError:
        return {
            "error": "Fallback OCR failed: invalid JSON from swift fallback."
        }

    if isinstance(parsed, dict):
        return parsed
    return {
        "error": "Fallback OCR failed: unexpected payload type from swift fallback."
    }


@mcp.tool()
async def ocr_image(file_path: str) -> dict:
    """
    Conduct macOS built-in OCR and return the text
    """
    if platform.system() != 'Darwin':
        return {'error': 'OCR functionality is only available on macOS.'}

    try:
        with open(file_path, 'rb') as f:
            contents = f.read()
        pil_image = _normalize_image_for_ocr(Image.open(io.BytesIO(contents)))
        raw_annotations = ocrmac_module.OCR(pil_image).recognize()
        processed_annotations = _process_annotations(raw_annotations)
        full_text = "\n".join(
            annotation["text"] for annotation in processed_annotations if annotation["text"]
        )

        filename = os.path.basename(file_path)
        return {
            'filename': filename,
            'annotations': processed_annotations,
            'annotation_count': len(processed_annotations),
            'full_text': full_text,
            'engine': 'ocrmac',
        }
    except FileNotFoundError:
        return {'error': f'File not found: {file_path}'}
    except TypeError as e:
        if "NoneType" in str(e):
            fallback_result = _run_swift_fallback(file_path)
            if fallback_result is not None:
                return fallback_result
        return {'error': f'Error processing image: {str(e)}'}
    except Exception as e:
        return {'error': f'Error processing image: {str(e)}'}


if __name__ == '__main__':
    mcp.run()
