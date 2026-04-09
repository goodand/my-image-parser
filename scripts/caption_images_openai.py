#!/usr/bin/env python3
"""CLI wrapper for the modular OpenAI per-image caption runner."""

from __future__ import annotations

import sys

from caption_runner_lib import main


if __name__ == "__main__":
    sys.exit(main())
