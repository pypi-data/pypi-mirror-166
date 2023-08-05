from __future__ import annotations

from typing import Sequence
import argparse


def introduction():
    print("Welcome to goodtype, a simple static type checker for Python.")


def main(argv: Sequence[str] | None = None) -> int:
    introduction()
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args(argv)

    print(f"Running static type checker on {args.file}")
    return 0
