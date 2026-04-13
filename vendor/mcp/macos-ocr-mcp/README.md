# macOS OCR MCP Tool

This project provides a MetaCall Protocol (MCP) tool to perform Optical Character Recognition (OCR) on images using macOS's built-in Vision framework. It exposes an `ocr_image` tool that takes an image file path and returns the recognized text along with confidence scores and bounding boxes.

## Project Setup

### Dependencies
This project relies on Python 3.13+ and the following main dependencies:
- `ocrmac`: For accessing macOS OCR capabilities. See [ocrmac](https://github.com/straussmaximilian/ocrmac).
- `Pillow`: For image manipulation.
- `mcp[cli]>=1.7.1`: For the MetaCall Protocol server and client.

### Installation
It is recommended to use a virtual environment.

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install dependencies using `uv`:**
    ```bash
    uv sync
    ```

## Running the MCP Server

To start the MCP server, run `main.py`:
```bash
uv run main.py
```
This will start the MCP server, making the `ocr_image` tool available.

## Available MCP Tools

### `ocr_image`
-   **Description:** Conducts OCR on the provided image file using macOS's built-in capabilities. Returns recognized text segments, their confidence scores, and bounding box coordinates.
-   **Input:** `file_path: str` - The absolute or relative path to the image file.
-   **Output (Example Success):**
    ```json
    {
      "filename": "path/to/your/image.png",
      "annotations": [
        {
          "text": "Hello World",
          "confidence": 0.95,
          "bounding_box": [0.1, 0.1, 0.5, 0.05] 
        },
        // ... more annotations
      ]
    }
    ```
-   **Output (Example Error):**
    ```json
    {
      "error": "OCR functionality is only available on macOS."
    }
    ```
    or
    ```json
    {
      "error": "File not found: path/to/nonexistent/image.png"
    }
    ```

**Note:** This tool will only function correctly on a macOS system due to its reliance on the Vision framework.

## Testing with MCP Inspector

You can use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector) to connect to the running MCP server and test the tool.

## Cursor MCP Configuration

To configure this MCP server in Cursor, you can add the following to your MCP JSON configuration file (e.g., `~/.cursor/mcp.json` or project-specific `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "ocrmac": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/macos-ocr-mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

This configuration tells Cursor how to start your MCP server. You can then call the `ocrmac.ocr_image` tool from within Cursor.
