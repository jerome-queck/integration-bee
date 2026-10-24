#!/usr/bin/env python3
"""SymPy checker for unit drills (multi-unit harness).

Loads verify/drills_unit*.json (or --drills PATH).
Exit 0 iff every answer matches; exit 1 on mismatch.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import sympy as sp
except ImportError:
    sys.stderr.write("FAIL: sympy missing. Use /workspace/integration-bee/.venv\n")
    sys.exit(2)

VERIFY = Path(__file__).resolve().parent
ROOT = VERIFY.parent

NS = {
    "x": sp.symbols("x", real=True),
    "pi": sp.pi,
    "exp": sp.exp,
    "log": sp.log,
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "sec": sp.sec,
    "csc": sp.csc,
    "cot": sp.cot,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
    "sqrt": sp.sqrt,
    "Abs": sp.Abs,
    "E": sp.E,
    "oo": sp.oo,
}


def load_all_drills(paths: list[Path] | None = None) -> list[dict]:
    if paths:
        files = paths
    else:
        files = sorted(VERIFY.glob("drills_unit*.json"))
    if not files:
        raise FileNotFoundError("no drills_unit*.json under verify/")
    out: list[dict] = []
    for f in files:
        out.extend(json.loads(f.read_text()))
    return out


def check_drill(d: dict) -> None:
    x = NS["x"]
    expr = sp.sympify(d["sympy_expr"], locals=NS)
    ans = sp.sympify(d["answer_sympy"], locals=NS)
    kind = d["kind"]
    if kind == "definite":
        lo, hi = d["limits"]
        lo = sp.sympify(lo, locals=NS)
        hi = sp.sympify(hi, locals=NS)
        val = sp.integrate(expr, (x, lo, hi)).simplify()
        if sp.simplify(val - ans) != 0:
            raise AssertionError(f"{d['id']}: got {val}, expected {ans}")
    elif kind == "indefinite":
        if sp.simplify(sp.diff(ans, x) - expr) != 0:
            raise AssertionError(f"{d['id']}: d/dx({ans}) != {expr}")
    else:
        raise AssertionError(f"{d['id']}: unknown kind {kind}")


def known_good_spotchecks() -> None:
    x = NS["x"]
    assert sp.simplify(sp.integrate(1 / (1 + x**2), (x, 0, 1)) - sp.pi / 4) == 0
    assert sp.simplify(sp.integrate(2 * x / (x**2 + 1), (x, 0, 1)) - sp.log(2)) == 0
    assert sp.simplify(sp.integrate(sp.sin(x), (x, -sp.pi, sp.pi))) == 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--drills", type=Path, action="append", default=None)
    ap.add_argument(
        "--mutate-wrong",
        action="store_true",
        help="Mutation: corrupt one answer; must FAIL (exit 1).",
    )
    args = ap.parse_args()
    known_good_spotchecks()
    drills = load_all_drills(args.drills)
    if args.mutate_wrong:
        drills = [dict(d) for d in drills]
        drills[0]["answer_sympy"] = "0"  # wrong for first drill (U01-D01)
        # If somehow first is already 0, force a different wrong value
        if drills[0].get("id") == "U01-D01":
            drills[0]["answer_sympy"] = "0"
        else:
            drills[0]["answer_sympy"] = "999"
    try:
        for d in drills:
            check_drill(d)
    except AssertionError as e:
        print(f"FAIL math: {e}")
        return 1
    print(f"PASS check_math ({len(drills)} drills + spotchecks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
