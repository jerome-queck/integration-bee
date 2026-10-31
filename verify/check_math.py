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
    sys.stderr.write("FAIL: sympy missing. python3 -m pip install sympy\n")
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


# The quadrature fallback must not be looser than numeric_close, or it
# accepts an answer the symbolic comparison already refused. 5e-8 sits
# between the previous 1e-7 bound and this one. Real drills match far inside it.
NUMERIC_FALLBACK_TOL = 1e-8


def numeric_close(a, b, tol: float = 1e-8) -> bool:
    try:
        diff = complex(sp.N(sp.simplify(a - b)))
        return abs(diff) < tol
    except Exception:
        return False


def _without_abs_sign(expr):
    """Rewrite the derivative of log|u| without deleting every absolute value.

    sign(u)/Abs(u) becomes 1/u, including inside a larger product. For a real
    factor, sign(v)**2 is 1 and log(v/sign(v)) is log(v) on the positive
    branch where log|log v| is defined. A bare Abs, as in x - Abs(x), stays.
    """

    def walk(node):
        if not isinstance(node, sp.Basic) or not node.args:
            return node
        node = node.func(*[walk(arg) for arg in node.args])
        if (
            isinstance(node, sp.Pow)
            and node.exp == 2
            and getattr(node.base, "func", None) == sp.sign
            and getattr(node.base.args[0], "is_real", None) is True
        ):
            return sp.Integer(1)
        if isinstance(node, sp.log):
            factors = list(sp.Mul.make_args(node.args[0]))
            if len(factors) == 2:
                left, right = factors

                def over_sign(num, den) -> bool:
                    return bool(
                        den.func == sp.Pow
                        and den.exp == -1
                        and den.base.func == sp.sign
                        and den.base.args[0] == num
                        and getattr(num, "is_real", None) is True
                    )

                if over_sign(left, right):
                    return sp.log(left)
                if over_sign(right, left):
                    return sp.log(right)
        if not isinstance(node, sp.Mul):
            return node
        args = list(node.args)
        used: set[int] = set()
        extra = []
        for i, arg in enumerate(args):
            if getattr(arg, "func", None) != sp.sign or i in used:
                continue
            base = arg.args[0]
            inverse = sp.Pow(sp.Abs(base), -1)
            for j, other in enumerate(args):
                if j == i or j in used:
                    continue
                if other == inverse:
                    used.add(i)
                    used.add(j)
                    extra.append(1 / base)
                    break
                if isinstance(other, sp.Pow) and other.base == sp.Abs(base):
                    used.add(i)
                    used.add(j)
                    extra.append(base * sp.Abs(base) ** (other.exp - 1))
                    break
        if not used:
            return node
        kept = [arg for i, arg in enumerate(args) if i not in used]
        return sp.Mul(*kept, *extra)

    return walk(expr)


def is_antiderivative(candidate, integrand) -> bool:
    """log|u| and log(u) share a derivative where both are defined. SymPy's
    derivative of log(Abs(u)) keeps sign(u)/Abs(u), so that quotient is
    rewritten to 1/u only after differentiation.
    """
    x = NS["x"]
    delta = sp.diff(candidate, x) - integrand
    if sp.simplify(delta) == 0:
        return True
    return sp.simplify(_without_abs_sign(delta)) == 0


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
            if abs(complex(nval - nans)) < NUMERIC_FALLBACK_TOL:
                return
        except Exception as e:
            raise AssertionError(f"{d['id']}: numeric fallback failed: {e}") from e
        raise AssertionError(f"{d['id']}: got (symbolic/numeric mismatch) expected {ans}")
    elif kind == "indefinite":
        if not is_antiderivative(ans, expr):
            raise AssertionError(f"{d['id']}: d/dx({ans}) != {expr}")
    else:
        raise AssertionError(f"{d['id']}: unknown kind {kind}")


def known_good_spotchecks() -> None:
    x = NS["x"]
    assert sp.simplify(sp.integrate(1 / (1 + x**2), (x, 0, 1)) - sp.pi / 4) == 0
    assert sp.simplify(sp.integrate(2 * x / (x**2 + 1), (x, 0, 1)) - sp.log(2)) == 0
    assert sp.simplify(sp.integrate(sp.sin(x), (x, -sp.pi, sp.pi))) == 0
    u01 = (2 * x + 3) / (x**2 + 3 * x + 2)
    assert is_antiderivative(sp.log(sp.Abs(x**2 + 3 * x + 2)), u01)
    assert is_antiderivative(sp.log(sp.Abs(x**2 + 3 * x + 2)) + sp.symbols("C"), u01)
    assert not is_antiderivative(sp.log(sp.Abs(x**2 + 3 * x + 2)) + x, u01)
    assert is_antiderivative(sp.log(sp.Abs(sp.log(x))), 1 / (x * sp.log(x)))
    assert not is_antiderivative(sp.exp(x), 1 / (x * sp.log(x)))
    assert not is_antiderivative(sp.log(sp.Abs(x)) * sp.sign(x), 1 / x)
    assert not is_antiderivative(3 * sp.log(sp.Abs(x)), 1 / x)
    assert not is_antiderivative(x**2 / 2, sp.Abs(x))
    assert is_antiderivative(x * sp.Abs(x) / 2, sp.Abs(x))
    pf = 1 / (x**2 - 1)
    assert is_antiderivative(sp.log(x - 1) / 2 - sp.log(x + 1) / 2, pf)
    assert is_antiderivative(sp.Rational(1, 2) * sp.log(sp.Abs((x - 1) / (x + 1))), pf)


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
