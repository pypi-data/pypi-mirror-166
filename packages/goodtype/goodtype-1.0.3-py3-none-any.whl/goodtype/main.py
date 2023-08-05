from __future__ import annotations

from typing import Sequence
import argparse


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Welcome to goodtype, a simple static type checker for Python.")
    parser.add_argument('file_name')
    args = parser.parse_args(argv)

    print(f"Running static type checker on {args.file_name}")
    return 0
