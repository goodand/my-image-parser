from __future__ import annotations

import builtins
import sys


def _redirect_prints_to_stderr() -> None:
    original_print = builtins.print

    def stderr_print(*args, **kwargs):
        kwargs.setdefault("file", sys.stderr)
        return original_print(*args, **kwargs)

    builtins.print = stderr_print


def main() -> None:
    _redirect_prints_to_stderr()
    from imagesorcery_mcp.server import main as server_main

    server_main()


if __name__ == "__main__":
    main()
