#!/usr/bin/env python3
"""Re-check worked solutions under solutions/pack and solutions/yang.

The catalog in problems/records.jsonl is not read or written. Each check is an
identity SymPy can close, or a high-precision quadrature against the value
printed in the cited PDF. Run from the repository root:

    python3 solutions/self_check.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import mpmath as mp
import sympy as sp

from pack_checks import EXTRA_CHECKS, EXTRA_PACK_IDS

ROOT = Path(__file__).resolve().parent
PACK = ROOT / "pack"
YANG = ROOT / "yang"

# Answered pack rows whose worked PDF (or mark scheme, for the same final)
# is written up here. Yang ids are only examples whose guide prints a final.
PACK_IDS = (
    "R1-2020-Q06",
    "R1-2020-Q10",
    "R1-2020-Q11",
    "R1-2020-Q13",
    "R1-2020-Q15",
    "R1-2020-Q18",
    "R1-2020-Q19",
    "R1-2020-Q20",
    "R1-2020-Q21",
    "R1-2020-Q23",
    "R1-2020-Q24",
    "R1-2020-Q25",
    "R1-2020-Q27",
    "R1-2020-Q28",
    "R1-2020-Q31",
    "R1-2020-Q32",
    "R1-2020-Q34",
    "R1-2020-Q39",
    "R1-2020-Q40",
    "R1-2021-Q01",
    "R1-2021-Q11",
    "R1-2021-Q15",
    "R1-2021-Q18",
    "R1-2021-Q20",
    "R1-2021-Q31",
    "R1-2021-Q32",
    "R1-2021-Q37",
    "R1-2021-Q39",
    "R1-2021-Q40",
    "R1-2022-Q02",
    "R1-2022-Q04",
    "R1-2022-Q05",
    "R1-2022-Q15",
    "R1-2022-Q22",
    "R1-2024-Q01",
)
if set(PACK_IDS) & set(EXTRA_PACK_IDS):
    raise AssertionError("duplicate pack ids")
PACK_IDS = tuple(sorted(PACK_IDS + EXTRA_PACK_IDS))
YANG_IDS = (
    "YANG-1.3-Ex01",
    "YANG-1.3-Ex02",
    "YANG-1.3-Ex03",
)


def _eq(left, right) -> None:
    if sp.simplify(left - right) != 0:
        raise AssertionError(f"{left} != {right}")


def _quad(func, a, b) -> mp.mpf:
    val = mp.quad(func, [a, b])
    if isinstance(val, mp.mpc):
        if abs(val.imag) > mp.mpf("1e-15"):
            raise AssertionError(f"non-real quadrature {val}")
        val = val.real
    return mp.mpf(val)


def _near(got, target, tol) -> None:
    got_v, target_v = mp.mpf(got), mp.mpf(target)
    if not (mp.isfinite(got_v) and mp.isfinite(target_v)):
        raise AssertionError(f"non-finite comparison {got} vs {target}")
    err = abs(got_v - target_v)
    if err >= tol:
        raise AssertionError(f"{got} vs {target}, err {err}")


def check_files() -> None:
    missing = [name for name in PACK_IDS if not (PACK / f"{name}.md").is_file()]
    missing += [name for name in YANG_IDS if not (YANG / f"{name}.md").is_file()]
    if missing:
        raise AssertionError(f"missing write-ups: {missing}")
    if len(PACK_IDS) < 30:
        raise AssertionError("pack manual count")


def check_r1_2020_q06() -> None:
    a, u = sp.symbols("a u", positive=True)
    derived = sp.integrate(sp.Rational(1, 2) / (1 + (a - 1) * u), (u, 0, 1))
    _eq(derived, sp.log(a) / (2 * (a - 1)))
    n = sp.symbols("n", integer=True, nonnegative=True)
    series = sp.summation(sp.Rational(1, 2) / (n + 1) ** 2, (n, 0, sp.oo))
    _eq(series, sp.pi**2 / 12)
    _eq(series / 2, sp.pi**2 / 24)


def check_r1_2020_q10() -> None:
    x = sp.symbols("x", real=True)
    left = sp.sqrt(sp.log(9 - x))
    right = sp.sqrt(sp.log(x + 3))
    _eq(left / (left + right) + right / (left + right), 1)
    _eq(sp.integrate(1, (x, 2, 4)) / 2, 1)


def check_r1_2020_q11() -> None:
    x = sp.symbols("x", positive=True)
    integrand = (3 * x**10 + 2 * x**8 - 2) * (x**10 + x**8 + 1) ** sp.Rational(1, 4) / x**6
    antideriv = sp.Rational(2, 5) * (x**6 + x**4 + x ** (-4)) ** sp.Rational(5, 4)
    _eq(sp.diff(antideriv, x), integrand)
    y = sp.symbols("y", real=True, nonzero=True)
    real_integrand = (3 * y**10 + 2 * y**8 - 2) * (y**10 + y**8 + 1) ** sp.Rational(1, 4) / y**6
    stored = 2 * (y**10 + y**8 + 1) ** sp.Rational(5, 4) / (5 * y**5)
    _eq(sp.diff(stored, y), real_integrand)


def check_r1_2020_q13() -> None:
    x = sp.symbols("x", real=True)
    u = sp.sqrt(1 + sp.exp(x))
    antideriv = 2 * u + sp.log((u - 1) / (u + 1))
    _eq(sp.diff(antideriv, x), u)


def check_r1_2020_q15() -> None:
    x = sp.symbols("x", real=True)
    integrand = 1 / sp.sqrt(1 + sp.exp(2 * x))
    s = sp.sqrt(1 + sp.exp(2 * x))
    log_form = sp.Rational(1, 2) * sp.log((s - 1) / (s + 1))
    asinh_form = -sp.asinh(sp.exp(-x))
    _eq(sp.diff(log_form, x), integrand)
    _eq(sp.diff(asinh_form, x), integrand)
    elementary = x - sp.log(1 + s)
    _eq(sp.exp(2 * log_form) * (s + 1) ** 2, sp.exp(2 * x))
    _eq(asinh_form.rewrite(sp.log), elementary)
    # exp(2 log_form) = exp(2 elementary) and both expressions are real, so they agree.
    _eq(sp.exp(log_form - elementary), 1)
    if abs(complex(sp.N((log_form - elementary).subs(x, 0), 40))) > 1e-30:
        raise AssertionError("Q15 log and asinh forms differ at 0")


def check_r1_2020_q18() -> None:
    x = sp.symbols("x", real=True)
    t = sp.tan(x / 2)
    antideriv = sp.log((t + 1) / (t + 3))
    integrand = 1 / (2 + 2 * sp.sin(x) + sp.cos(x))
    _eq(sp.diff(antideriv, x), integrand)


def check_r1_2020_q19() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    c, u = sp.symbols("c u", positive=True)
    term = sp.integrate(sp.exp(-c * u) * u**n, (u, 0, sp.oo))
    _eq(term, sp.factorial(n) / c ** (n + 1))
    _eq(term.subs(c, n + 1) / sp.factorial(n), 1 / (n + 1) ** (n + 1))
    mp.mp.dps = 25
    partial = sum(mp.power(k, -k) for k in range(1, 40))

    def integrand(t):
        if t == 0:
            return mp.mpf(1)
        return mp.exp(-t * mp.log(t))

    _near(_quad(integrand, 0, 1), partial, mp.mpf("1e-12"))


def check_r1_2020_q20() -> None:
    mp.mp.dps = 25
    got = _quad(lambda u: mp.log(u) ** 2 / (1 + u * u), 0, mp.inf)
    _near(got, mp.pi**3 / 8, mp.mpf("1e-18"))


def check_r1_2020_q21() -> None:
    mp.mp.dps = 25
    log_sine = _quad(lambda t: mp.log(mp.sin(t)), 0, mp.pi / 2)
    _near(log_sine, -(mp.pi / 2) * mp.log(2), mp.mpf("1e-12"))
    # I(1) = pi*ln 4 + 4 * log_sine = 0 once log_sine is -pi/2 ln 2.
    log_sine_exact = -sp.pi / 2 * sp.log(2)
    i_one = sp.pi * sp.log(4) + 4 * log_sine_exact
    _eq(i_one, 0)
    _eq(2 * sp.pi * sp.log(sp.pi) - i_one, 2 * sp.pi * sp.log(sp.pi))
    got = _quad(lambda t: mp.log(1 - 2 * mp.pi * mp.cos(t) + mp.pi**2), 0, mp.pi)
    _near(got, 2 * mp.pi * mp.log(mp.pi), mp.mpf("1e-12"))


def check_r1_2020_q23() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    piece = 1 / (2 * (n + 1) ** 2)
    total = sp.summation(piece, (n, 1, sp.oo))
    _eq(total, sp.pi**2 / 12 - sp.Rational(1, 2))


def check_r1_2020_q24() -> None:
    x = sp.symbols("x", positive=True)
    closed = -sp.Rational(1, 2) + sp.Rational(1, 2) * sp.sqrt(4 * x - 3)
    _eq(closed**2, x - (1 + closed))
    antideriv = -x / 2 + sp.Rational(1, 12) * (4 * x - 3) ** sp.Rational(3, 2)
    _eq(sp.diff(antideriv, x), closed)


def check_r1_2020_q25() -> None:
    a, b = sp.symbols("a b", positive=True)
    log_form = sp.pi * sp.log((a + sp.sqrt(a**2 - b**2)) / 2)
    arcosh_form = sp.pi * sp.acosh(a / b) + sp.pi * sp.log(b / 2)
    _eq(sp.acosh(a / b).rewrite(sp.log), sp.log(a / b + sp.sqrt((a / b) ** 2 - 1)))
    _eq(arcosh_form.rewrite(sp.log), log_form)
    mp.mp.dps = 25
    aa, bb = mp.mpf(3), mp.mpf(1)
    got = _quad(lambda t: mp.log(aa + bb * mp.cos(t)), 0, mp.pi)
    target = mp.pi * mp.log((aa + mp.sqrt(aa**2 - bb**2)) / 2)
    _near(got, target, mp.mpf("1e-12"))


def check_r1_2020_q27() -> None:
    t = sp.symbols("t", positive=True)
    base = sp.integrate(1 / (sp.sqrt(t) * (1 + t)), (t, 0, sp.oo))
    _eq(base, sp.pi)
    _eq(sp.pi / 2 * base / 2, sp.pi**2 / 4)


def check_r1_2020_q28() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    x = sp.symbols("x", positive=True)
    moment = sp.integrate(-(sp.log(x)) * x**n, (x, 0, 1))
    _eq(moment, 1 / (n + 1) ** 2)
    total = sp.summation(1 / (n * (n + 1) ** 2), (n, 1, sp.oo))
    _eq(total, 2 - sp.pi**2 / 6)


def check_r1_2020_q31() -> None:
    x = sp.symbols("x", real=True)
    half = x / 4
    _eq(sp.expand_trig(sp.sqrt(2) * sp.sin(half + sp.pi / 4) - (sp.sin(half) + sp.cos(half))), 0)
    _eq((sp.sin(half) + sp.cos(half)) ** 2, 1 + sp.sin(x / 2))
    antideriv = 4 * (sp.sin(half) - sp.cos(half))
    _eq(sp.diff(antideriv, x), sp.sin(half) + sp.cos(half))


def check_r1_2020_q32() -> None:
    x = sp.symbols("x")
    _eq(sp.integrate(sp.log(x), (x, 0, 1)), -1)
    _eq(sp.integrate(sp.log(1 - x), (x, 0, 1)), -1)
    q28 = 2 - sp.pi**2 / 6
    expanded = sp.log(2) ** 2 + sp.log(2) * (-1) + sp.log(2) * (-1) + q28
    _eq(expanded, sp.log(2) ** 2 - 2 * sp.log(2) + 2 - sp.pi**2 / 6)
    mp.mp.dps = 25
    got = _quad(lambda t: mp.log(1 + t) * mp.log(1 - t), 0, 1)
    target = mp.log(2) ** 2 - 2 * mp.log(2) + 2 - mp.pi**2 / 6
    _near(got, target, mp.mpf("1e-12"))


def check_r1_2020_q34() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.diff(sp.exp(sp.exp(x)), x), sp.exp(x + sp.exp(x)))


def check_r1_2020_q39() -> None:
    a, u, k = sp.symbols("a u k", positive=True)
    antideriv = (2 / k) * sp.atan(u * k)
    integrand = 2 / ((1 - a**2) * u**2 + 1)
    _eq(sp.diff((2 / sp.sqrt(1 - a**2)) * sp.atan(u * sp.sqrt(1 - a**2)), u), integrand)
    _eq(sp.limit(antideriv, u, sp.oo), sp.pi / k)
    _eq(sp.integrate(sp.pi / sp.sqrt(1 - a**2), (a, 0, sp.Rational(1, 2))), sp.pi**2 / 6)


def check_r1_2020_q40() -> None:
    x = sp.symbols("x", real=True)
    reduced = sp.log(sp.tan(x) + 1)
    ratio = (sp.sec(x) ** 2 - 2) / (sp.tan(x) - 1)
    _eq(sp.simplify(ratio - (sp.tan(x) + 1)), 0)
    _eq(sp.sin(x) + sp.cos(x), sp.sqrt(2) * sp.cos(sp.pi / 4 - x))
    shifted = sp.log(sp.cos(sp.pi / 4 - x))
    _eq(shifted.subs(x, sp.pi / 4 - x), sp.log(sp.cos(x)))
    _eq(sp.integrate(sp.log(sp.sqrt(2)), (x, 0, sp.pi / 4)), sp.pi * sp.log(2) / 8)


def check_r1_2021_q01() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.diff(x ** (sp.E - 1) / (sp.E - 1), x), x ** (sp.E - 2))
    n = sp.symbols("n", integer=True)
    _eq(sp.summation(1 / sp.factorial(n), (n, 2, sp.oo)), sp.E - 2)


def check_r1_2021_q11() -> None:
    m, t = sp.symbols("m t", positive=True)
    n = m + 1
    _eq(sp.integrate(t**n * sp.exp(-(n - 1) * t), (t, 0, sp.oo)), sp.gamma(n + 1) / (n - 1) ** (n + 1))
    _eq(sp.factorial(2011) / 2010**2012, sp.gamma(2012) / 2010**2012)


def check_r1_2021_q15() -> None:
    x = sp.symbols("x", real=True)
    integrand = 1 / (sp.csc(x) + 1)
    worked = x + sp.sec(x) - sp.tan(x)
    scheme = x - 2 * sp.sin(x / 2) / (sp.sin(x / 2) + sp.cos(x / 2))
    _eq(sp.diff(worked, x), integrand)
    _eq(sp.diff(scheme, x), integrand)
    gap = (1 - sp.sin(x)) / sp.cos(x) - (1 - 2 * sp.sin(x / 2) / (sp.sin(x / 2) + sp.cos(x / 2)))
    _eq(gap, 0)


def check_r1_2021_q18() -> None:
    x = sp.symbols("x", positive=True)
    integrand = sp.sqrt(1 / x - 1)
    worked = sp.asin(sp.sqrt(x)) + sp.sqrt(x * (1 - x))
    scheme = sp.sqrt(x * (1 - x)) - sp.atan(sp.sqrt((1 - x) / x))
    _eq(sp.diff(worked, x), integrand)
    _eq(sp.diff(scheme, x), integrand)
    _eq(sp.diff(worked - scheme, x), 0)
    _eq((worked - scheme).subs(x, sp.Rational(1, 2)), sp.pi / 2)


def check_r1_2021_q20() -> None:
    x = sp.symbols("x", positive=True)
    integrand = sp.sqrt(x**2 - 1)
    antideriv = sp.Rational(1, 2) * x * sp.sqrt(x**2 - 1) - sp.Rational(1, 2) * sp.acosh(x)
    _eq(sp.diff(antideriv, x), integrand)


def check_r1_2021_q31() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    term = 1 / n - 1 / (n + 1) - 1 / (n + 1) ** 2
    _eq(sp.summation(term, (n, 1, sp.oo)), 2 - sp.pi**2 / 6)


def check_r1_2021_q32() -> None:
    u = sp.symbols("u", real=True)
    _eq(sp.integrate(sp.sin(u) / u, (u, 0, sp.oo)), sp.pi / 2)
    a, b = sp.symbols("a b", positive=True)
    _eq(sp.integrate(sp.pi / 2, (sp.symbols("t"), a, b)), sp.pi / 2 * (b - a))


def check_r1_2021_q37() -> None:
    x = sp.symbols("x", real=True)
    f = sp.sin(x) * sp.cos(x) * (sp.cos(x) - sp.sin(x))
    _eq(f + f.subs(x, sp.pi / 2 - x), 0)
    _eq(sp.integrate(f, (x, 0, sp.pi / 2)), 0)


def check_r1_2021_q39() -> None:
    x = sp.symbols("x", real=True)
    integrand = 1 / (sp.sin(x) ** 4 + sp.cos(x) ** 4)
    antideriv = sp.atan(sp.tan(2 * x) / sp.sqrt(2)) / sp.sqrt(2)
    _eq(sp.diff(antideriv, x), integrand)


def check_r1_2021_q40() -> None:
    x = sp.symbols("x", positive=True)
    value = sp.integrate(x**sp.I / (1 + x) ** 2, (x, 0, sp.oo))
    _eq(value, sp.pi / sp.sinh(sp.pi))
    _eq(sp.re(value), sp.pi / sp.sinh(sp.pi))


def check_r1_2022_q02() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    _eq(sp.summation(k * (k - 1), (k, 1, 100)), 333300)


def check_r1_2022_q04() -> None:
    x = sp.symbols("x", positive=True)
    y = sp.Rational(1, 2) + sp.sqrt(x + sp.Rational(1, 4))
    _eq(y**2, x + y)
    antideriv = sp.Rational(2, 3) * (x + sp.Rational(1, 4)) ** sp.Rational(3, 2) + x / 2
    _eq(sp.simplify(antideriv.subs(x, 1) - antideriv.subs(x, 0)), sp.Rational(5, 12) * (1 + sp.sqrt(5)))


def check_r1_2022_q05() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    partial = sp.log(n + 1) - (sp.harmonic(n + 1) - 1)
    _eq(sp.limit(partial, n, sp.oo), 1 - sp.EulerGamma)


def check_r1_2022_q15() -> None:
    x = sp.symbols("x", real=True)
    denom = (1 + sp.cos(x) + sp.sin(x)) ** 2
    split = 2 * (1 + sp.cos(x)) * (1 + sp.sin(x))
    _eq(denom, split)
    reduced = sp.Rational(1, 2) * (1 - sp.sin(x))
    _eq(sp.integrate(reduced, (x, 0, sp.pi / 2)), (sp.pi - 2) / 4)


def check_r1_2022_q22() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    alternating = sp.summation(((-1) ** (n + 1)) / n**2, (n, 1, sp.oo))
    basel = sp.summation(1 / n**2, (n, 1, sp.oo))
    _eq(alternating + basel, sp.pi**2 / 4)


def check_r1_2024_q01() -> None:
    n = sp.symbols("n", real=True)
    average = sp.simplify(sp.integrate(sp.exp(sp.I * n), (n, -1, 1)) / 2)
    if average != sp.sin(1):
        raise AssertionError(average)


def check_yang_1_3_ex01() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate((x + 1) * (x**2 + 1), (x, -1, 1)), sp.Rational(8, 3))
    _eq(2 * sp.integrate(x**2 + 1, (x, 0, 1)), sp.Rational(8, 3))


def check_yang_1_3_ex02() -> None:
    x = sp.symbols("x", real=True)
    odd = x * sp.asin(x) / sp.atan(x)
    _eq(odd.subs(x, -x) + odd, 0)
    full = odd + 1
    _eq(full + full.subs(x, -x), 2)
    _eq(sp.integrate(sp.Integer(1), (x, -1, 1)), 2)


def check_yang_1_3_ex03() -> None:
    u = sp.symbols("u", real=True)
    expr = (u * (u**2 - 1) + 1) / (u**2 + 1)
    odd_piece = u - 2 * u / (u**2 + 1)
    _eq(sp.simplify(expr - odd_piece - 1 / (u**2 + 1)), 0)
    _eq(odd_piece.subs(u, -u) + odd_piece, 0)
    _eq(sp.integrate(1 / (u**2 + 1), (u, -3, 3)), 2 * sp.atan(3))


CHECKS = (
    check_files,
    check_r1_2020_q06,
    check_r1_2020_q10,
    check_r1_2020_q11,
    check_r1_2020_q13,
    check_r1_2020_q15,
    check_r1_2020_q18,
    check_r1_2020_q19,
    check_r1_2020_q20,
    check_r1_2020_q21,
    check_r1_2020_q23,
    check_r1_2020_q24,
    check_r1_2020_q25,
    check_r1_2020_q27,
    check_r1_2020_q28,
    check_r1_2020_q31,
    check_r1_2020_q32,
    check_r1_2020_q34,
    check_r1_2020_q39,
    check_r1_2020_q40,
    check_r1_2021_q01,
    check_r1_2021_q11,
    check_r1_2021_q15,
    check_r1_2021_q18,
    check_r1_2021_q20,
    check_r1_2021_q31,
    check_r1_2021_q32,
    check_r1_2021_q37,
    check_r1_2021_q39,
    check_r1_2021_q40,
    check_r1_2022_q02,
    check_r1_2022_q04,
    check_r1_2022_q05,
    check_r1_2022_q15,
    check_r1_2022_q22,
    check_r1_2024_q01,
    *EXTRA_CHECKS,
    check_yang_1_3_ex01,
    check_yang_1_3_ex02,
    check_yang_1_3_ex03,
)


def main() -> int:
    for check in CHECKS:
        check()
        print(f"PASS {check.__name__}")
    print(f"PASS {len(PACK_IDS)} pack manuals, {len(YANG_IDS)} Yang examples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
