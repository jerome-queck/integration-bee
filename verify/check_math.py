#!/usr/bin/env python3
"""SymPy checker for unit drills (multi-unit harness).

Loads verify/drills_unit*.json (or --drills PATH).
Exit 0 iff every answer matches; exit 1 on mismatch.

Definite integrals: prefer symbolic simplify; fall back to numeric
comparison when SymPy leaves an Integral or simplify is flaky.
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
    "Rational": sp.Rational,
    "asinh": sp.asinh,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "Catalan": sp.Catalan,
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


def numeric_close(a, b, tol: float = 1e-7) -> bool:
    try:
        diff = complex(sp.N(sp.simplify(a - b)))
        return abs(diff) < tol
    except Exception:
        return False


def _integrate_worker(payload, q):
    try:
        expr, lo, hi = payload
        x = NS["x"]
        val = sp.integrate(expr, (x, lo, hi))
        q.put(("ok", val))
    except Exception as e:
        q.put(("err", str(e)))


def integrate_timeout(expr, lo, hi, timeout: float = 8.0):
    """Return integrate result or None on timeout/error."""
    import multiprocessing as mp
    q: mp.Queue = mp.Queue()
    p = mp.Process(target=_integrate_worker, args=((expr, lo, hi), q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join(1)
        return None
    if q.empty():
        return None
    status, val = q.get()
    return val if status == "ok" else None


def check_drill(d: dict) -> None:
    x = NS["x"]
    expr = sp.sympify(d["sympy_expr"], locals=NS)
    ans = sp.sympify(d["answer_sympy"], locals=NS)
    kind = d["kind"]
    if kind == "definite":
        lo, hi = d["limits"]
        lo = sp.sympify(lo, locals=NS)
        hi = sp.sympify(hi, locals=NS)
        use_numeric = d.get("verify_mode") == "numeric"
        if not use_numeric:
            val = integrate_timeout(expr, lo, hi, timeout=8.0)
            if val is not None and not val.has(sp.Integral):
                if sp.simplify(val - ans) == 0 or numeric_close(val, ans):
                    return
        try:
            nval = sp.N(sp.Integral(expr, (x, lo, hi)))
            nans = sp.N(ans)
            if abs(complex(nval - nans)) < 1e-6:
                return
        except Exception as e:
            raise AssertionError(f"{d['id']}: numeric fallback failed: {e}") from e
        raise AssertionError(f"{d['id']}: got (symbolic/numeric mismatch) expected {ans}")
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
    import multiprocessing as mp
    try:
        mp.set_start_method("spawn", force=True)
    except RuntimeError:
        pass
    sys.exit(main())
