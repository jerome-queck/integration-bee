#!/usr/bin/env python3
"""Must-fail regressions for audit finding E.

Each case calls the checker that owns the false pass. Exit 1 while that
checker still accepts the bad input. Exit 0 once the checker rejects it.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [
    str(ROOT / "verify"),
    str(ROOT / "verify" / "audit" / "confirm125"),
    str(ROOT / "solutions"),
    str(ROOT / "scripts"),
]


def fail(message: str) -> int:
    print(f"FAIL {message}")
    return 1


def ok(message: str) -> int:
    print(f"PASS {message}")
    return 0


def test_primitive_abs() -> int:
    import sympy as sp

    import check_math

    x = check_math.NS["x"]
    if check_math.is_antiderivative(x**2 / 2, sp.Abs(x)):
        return fail("primitive of |x|: x**2/2 was accepted")
    if not check_math.is_antiderivative(x * sp.Abs(x) / 2, sp.Abs(x)):
        return fail("primitive of |x|: the real primitive was rejected")
    return ok("primitive of |x|")

CASES = {
    "primitive-abs": test_primitive_abs,
}


def main(argv: list[str]) -> int:
    names = argv or list(CASES)
    unknown = [name for name in names if name not in CASES]
    if unknown:
        print("unknown " + ", ".join(unknown), file=sys.stderr)
        return 2
    status = 0
    for name in names:
        status = CASES[name]() or status
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
