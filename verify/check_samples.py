#!/usr/bin/env python3
"""SymPy-check official sample answers marked verify=sympy in answers_feed.json.

manual rows are skipped. A pdf_answer_suspect row must still prove its stated
antiderivative and must reject the PDF answer.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import sympy as sp
except ImportError:
    sys.stderr.write("FAIL: sympy missing\n")
    sys.exit(2)

import check_math

ROOT = Path(__file__).resolve().parent.parent
FEED = ROOT / "past" / "samples" / "answers_feed.json"

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
    "sqrt": sp.sqrt,
    "oo": sp.oo,
}


def check_one(d: dict) -> None:
    x = NS["x"]
    expr = sp.sympify(d["sympy_expr"], locals=NS)
    ans = sp.sympify(d["answer_sympy"], locals=NS)
    kind = d["kind"]
    if kind == "definite":
        lo = sp.sympify(d["limits"][0], locals=NS)
        hi = sp.sympify(d["limits"][1], locals=NS)
        partner = sp.simplify(expr + expr.subs(x, lo + hi - x))
        if partner == 1 and sp.simplify(ans - (hi - lo) / 2) == 0:
            return
        val = sp.integrate(expr, (x, lo, hi)).simplify()
        if sp.simplify(val - ans) != 0:
            raise AssertionError(f"{d['id']}: got {val}, expected {ans}")
    elif kind == "indefinite":
        if not check_math.is_antiderivative(ans, expr):
            raise AssertionError(f"{d['id']}: d/dx({ans}) != {expr}")
    else:
        raise AssertionError(f"{d['id']}: unknown kind {kind}")


def check_suspect(d: dict) -> None:
    needed = ("sympy_expr", "answer_sympy", "answer_pdf_sympy", "kind")
    missing = [key for key in needed if key not in d]
    if missing:
        raise AssertionError(f"{d['id']}: suspect row missing {', '.join(missing)}")
    if d["kind"] != "indefinite":
        raise AssertionError(f"{d['id']}: suspect row kind {d['kind']}")
    expr = sp.sympify(d["sympy_expr"], locals=check_math.NS)
    ans = sp.sympify(d["answer_sympy"], locals=check_math.NS)
    pdf = sp.sympify(d["answer_pdf_sympy"], locals=check_math.NS)
    if not check_math.is_antiderivative(ans, expr):
        raise AssertionError(f"{d['id']}: stated answer is not an antiderivative")
    if check_math.is_antiderivative(pdf, expr):
        raise AssertionError(f"{d['id']}: PDF answer matches the integrand")


def main() -> int:
    if not FEED.exists():
        print(f"FAIL missing {FEED}")
        return 1
    rows = json.loads(FEED.read_text())
    if len(rows) < 20:
        print(f"FAIL expected ≥20 sample rows, got {len(rows)}")
        return 1
    ids = {r["id"] for r in rows}
    for i in range(1, 21):
        sid = f"SAMPLE-Q{i:02d}"
        if sid not in ids:
            print(f"FAIL missing {sid}")
            return 1
    checked = 0
    suspects = 0
    for d in rows:
        if d.get("pdf_answer_suspect"):
            check_suspect(d)
            suspects += 1
        if d.get("verify") != "sympy":
            continue
        check_one(d)
        checked += 1
    q17 = next((row for row in rows if row.get("id") == "SAMPLE-Q17"), None)
    if q17 is None or not q17.get("pdf_answer_suspect"):
        print("FAIL SAMPLE-Q17 must stay a checked pdf-suspect row")
        return 1
    if suspects < 1:
        print("FAIL no pdf-suspect sample was checked")
        return 1
    if checked < 1:
        print("FAIL no sympy-verifiable samples")
        return 1
    skipped = sum(
        1
        for row in rows
        if row.get("verify") != "sympy" and not row.get("pdf_answer_suspect")
    )
    print(f"PASS check_samples ({checked} sympy, {suspects} pdf-suspect, {skipped} manual/skipped)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
