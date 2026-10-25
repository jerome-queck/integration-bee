#!/usr/bin/env python3
"""SymPy-check official sample answers marked verify=sympy in answers_feed.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import sympy  # noqa: F401
except ImportError:
    sys.stderr.write("FAIL: sympy missing\n")
    sys.exit(2)

import pack_gate

ROOT = Path(__file__).resolve().parent.parent
FEED = ROOT / "past" / "samples" / "answers_feed.json"


def check_one(d: dict) -> None:
    kind = d["kind"]
    if kind == "definite":
        limits = (str(d["limits"][0]), str(d["limits"][1]))
    elif kind == "indefinite":
        limits = None
    else:
        raise AssertionError(f"{d['id']}: unknown kind {kind}")
    if not pack_gate.proven(kind, d["sympy_expr"], limits, d["answer_sympy"], "x"):
        raise AssertionError(f"{d['id']}: not proved")


def check_suspect(d: dict) -> None:
    needed = ("sympy_expr", "answer_sympy", "answer_pdf_sympy", "kind")
    missing = [key for key in needed if key not in d]
    if missing:
        raise AssertionError(f"{d['id']}: suspect row missing {', '.join(missing)}")
    if d["kind"] != "indefinite":
        raise AssertionError(f"{d['id']}: suspect row kind {d['kind']}")
    if not pack_gate.proven(d["kind"], d["sympy_expr"], None, d["answer_sympy"], "x"):
        raise AssertionError(f"{d['id']}: stated answer is not an antiderivative")
    if pack_gate.proven(d["kind"], d["sympy_expr"], None, d["answer_pdf_sympy"], "x"):
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
    if q17 is None or q17.get("pdf_answer_suspect") or q17.get("answer_sympy") != "E*x":
        print("FAIL SAMPLE-Q17 must grade e*x and is not a pdf-suspect row")
        return 1
    q15 = next((row for row in rows if row.get("id") == "SAMPLE-Q15"), None)
    if q15 is None or not q15.get("pdf_answer_suspect"):
        print("FAIL SAMPLE-Q15 must stay the printed-sign suspect")
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
