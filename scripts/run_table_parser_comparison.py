from __future__ import annotations

import argparse
import json
from pathlib import Path

from table_parser_comparison_lib import compare_normalized_tables, load_normalized_table


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare Apple and Paddle normalized table outputs.")
    parser.add_argument("--apple-normalized-json", required=True)
    parser.add_argument("--paddle-normalized-json", required=True)
    parser.add_argument("--output-json", required=True)
    args = parser.parse_args()

    apple = load_normalized_table(args.apple_normalized_json)
    paddle = load_normalized_table(args.paddle_normalized_json)
    comparison = compare_normalized_tables(apple, paddle)
    Path(args.output_json).write_text(json.dumps(comparison, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(comparison, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
