import sys
import importlib.metadata
from typing import Optional, Sequence


def introduction():
    print("Welcome to goodtype, a simple static type checker for Python.")


def main(argv: Optional[Sequence[str]] = None) -> int:
    introduction()
    return 0
