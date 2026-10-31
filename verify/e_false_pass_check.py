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


def test_exp_2pii() -> int:
    import sympy as sp

    import pack_gate

    if pack_gate._logs_equivalent(sp.Integer(0), 2 * sp.pi * sp.I):
        return fail("exp shortcut accepted a difference of 2*pi*I")
    x = sp.symbols("x", positive=True)
    if pack_gate._log_identity(sp.log(x), sp.log(x) + 2 * sp.pi * sp.I):
        return fail("exp shortcut accepted log(x) and log(x)+2*pi*I")
    if not pack_gate._logs_equivalent(sp.log(x) - sp.log(x + 1), sp.log(x / (x + 1))):
        return fail("exp shortcut rejected a real logarithm identity")
    return ok("exp shortcut 2*pi*I")


def test_symmetry_pv() -> int:
    import pack_gate

    x = pack_gate.namespace("x")["x"]
    values = pack_gate._reduced_integrals(1 / x, x, -1, 1)
    if any(value == 0 for value in values):
        return fail("symmetry reduction accepted the Cauchy principal value of 1/x on [-1, 1]")
    return ok("symmetry PV 1/x")


def test_floor_cell() -> int:
    import sympy as sp

    import pack_gate

    x = pack_gate.namespace("x")["x"]
    integrand = sp.sign(x - sp.floor(x) - sp.Rational(1, 2))
    got = pack_gate._floor_sum(integrand, x, 0, sp.oo)
    if got == 0:
        return fail("floor whole-cell sum accepted a non-convergent integral as 0")
    return ok("floor whole-cell sum")


def test_arctan_square() -> int:
    import sympy as sp

    import pack_gate

    z = sp.symbols("z")
    folded = pack_gate._fold_inverse_complements(sp.atan(z**2) + sp.atan(1 / z**2))
    if folded == sp.pi / 2 or sp.simplify(folded - sp.pi / 2) == 0:
        return fail("complex square was folded to +pi/2")
    real = sp.symbols("xr", real=True)
    kept = sp.simplify(pack_gate._fold_inverse_complements(sp.atan(real**2) + sp.atan(1 / real**2)))
    if kept != sp.pi / 2:
        return fail("real square lost the positive arctangent complement")
    return ok("complex-square arctan sign")


def test_display() -> int:
    import answer_plain_check as plain

    points = plain.POINTS
    vanish = f"(x-({points[0]}))*(x-({points[1]}))*(x-({points[2]}))"
    rows = {
        "blank": {"answer_plain": "   ", "answer_sympy": "1", "kind": "definite"},
        "1=2": {"answer_plain": "1=2", "answer_sympy": "1", "kind": "definite"},
        "a+b": {"answer_plain": "a + b", "answer_sympy": "2*a", "kind": "definite"},
        "sample-point": {
            "answer_plain": f"x + {vanish}",
            "answer_sympy": "x",
            "kind": "definite",
        },
    }
    for name, row in rows.items():
        if not plain.check_row(row):
            return fail(f"display checker accepted {name}")
    return ok("display checker")


def test_yang_sampler() -> int:
    import yang_worked_check as yang

    bad = yang.real_domain_failures(
        {"variable": "x", "sympy_expr": "log(-1-x**2)", "answer_sympy": "999"}
    )
    if not bad:
        return fail("Yang sampler accepted zero valid samples")
    return ok("Yang sampler zero valid samples")

CASES = {
    "primitive-abs": test_primitive_abs,
    "exp-2pii": test_exp_2pii,
    "symmetry-pv": test_symmetry_pv,
    "floor-cell": test_floor_cell,
    "arctan-square": test_arctan_square,
    "display": test_display,
    "yang-sampler": test_yang_sampler,
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
