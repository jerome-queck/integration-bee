#!/usr/bin/env python3
"""Regression for audit F1: learner answers must never reach Python eval.

Each payload below executed code (or hung) through sympify() at bcab5f2.
The check fails if any payload parses, if a marker file appears, or if
ordinary answers stop parsing.
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pack_gate  # noqa: E402
import safe_expr  # noqa: E402
import sympy as sp  # noqa: E402
import turn_contract  # noqa: E402

marker = Path(tempfile.mkdtemp()) / "pwned"
PAYLOADS = [
    f"__import__('pathlib').Path({str(marker)!r}).touch()",
    f"open({str(marker)!r}, 'w')",
    "x.__class__.__mro__",
    "().__class__",
    "eval('1')",
    "exec('1')",
    "getattr(x, 'func')",
    "[c for c in ()]",
    "lambda: 1",
    "'abc'",
    "x if x else 1",
    "sin(x, evaluate=False)",
    "9**9**9**9",
    "10**100000",
    "S('1')",
    "Symbol('x')",
]
GOOD = {"x**2/2 + C": True, "x^3/3": True, "sin(x)+cos(x)": True, "-log(Abs(x))": True,
        "pi/2": True, "sqrt(2)*E": True, "Rational(1,2)": True, "a*b": True}

fail = 0
for text in PAYLOADS:
    for name, fn in (("turn_contract.parse_expr", turn_contract.parse_expr),
                     ("expressions_match", lambda t: turn_contract.expressions_match("x", t, True)),
                     ("pack_gate._parse", lambda t: pack_gate._parse(t, "x"))):
        try:
            fn(text)
        except (safe_expr.UnsafeExpression, sp.SympifyError):
            continue
        except Exception as exc:  # any other error means eval may have run
            print(f"FAIL {name} raised {type(exc).__name__} instead of rejecting: {text!r}")
            fail = 1
            continue
        print(f"FAIL {name} accepted unsafe input: {text!r}")
        fail = 1
if marker.exists():
    print("FAIL payload executed code (marker file written)")
    fail = 1
for text in GOOD:
    try:
        turn_contract.parse_expr(text)
    except Exception as exc:
        print(f"FAIL ordinary answer rejected: {text!r}: {exc}")
        fail = 1
if fail:
    sys.exit(1)
print(f"PASS safe_expr: {len(PAYLOADS)} payloads rejected on 3 entry points, {len(GOOD)} answers parse")
