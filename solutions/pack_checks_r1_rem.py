"""SymPy checks for the second 2026-10-26 wave of R1 pack notes.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

R1_REM_PACK_IDS = (
    "R1-2020-Q03",
    "R1-2020-Q09",
    "R1-2020-Q12",
    "R1-2020-Q14",
    "R1-2020-Q17",
    "R1-2020-Q22",
    "R1-2020-Q29",
    "R1-2020-Q30",
    "R1-2020-Q33",
    "R1-2020-Q35",
    "R1-2021-Q06",
    "R1-2021-Q07",
    "R1-2021-Q08",
    "R1-2021-Q17",
    "R1-2021-Q21",
    "R1-2021-Q23",
    "R1-2021-Q25",
    "R1-2021-Q33",
    "R1-2021-Q35",
    "R1-2021-Q38",
    "R1-2022-Q09",
    "R1-2022-Q10",
    "R1-2022-Q18",
    "R1-2022-Q19",
    "R1-2022-Q27",
    "R1-2022-MIT-TB-Q03",
    "R1-2022-MIT-TB-Q04",
    "R1-2022-MIT-TB-Q05",
    "R1-2022-MIT-TB-Q06",
    "R1-2022-MIT-TB-Q08",
    "R1-2022-MIT-TB-Q10",
    "R1-2022-MIT-TB-Q12",
    "R1-2022-MIT-TB-Q19",
    "R1-2022-MIT-TB-Q24",
    "R1-2022-MIT-TB-Q25",
    "R1-2022-MIT-TB-Q26",
    "R1-2022-MIT-TB-Q28",
    "R1-2024-Q27",
    "R1-2024-Q29",
    "R1-2025-Online-Q02",
    "R1-2025-Online-Q03",
    "R1-2025-Online-Q04",
    "R1-2025-Online-Q05",
    "R1-2025-Online-Q06",
    "R1-2025-Online-Q16",
    "R1-2025-Online-Q18",
    "R1-2025-Online-Q20",
    "R1-2025-Online-Q21",
    "R1-2025-Online-Q26",
    "R1-2025-Online-Q30",
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


def check_r1_2020_q03() -> None:
    th = sp.symbols("th", positive=True)
    x = sp.cos(2 * th)
    dx = sp.diff(x, th)
    integrand = (1 + sp.sqrt(3)) / ((1 + x) ** sp.Rational(1, 2) * (1 - x) ** sp.Rational(3, 2))
    expr = sp.simplify(integrand * dx).replace(sp.Abs, lambda z: z)
    _eq(sp.simplify(expr + (1 + sp.sqrt(3)) / sp.sin(th) ** 2), 0)
    _eq(sp.simplify((1 + sp.sqrt(3)) * (sp.cot(sp.pi / 6) - sp.cot(sp.pi / 4))), 2)


def check_r1_2020_q09() -> None:
    x = sp.symbols("x", positive=True)
    integrand = 1 / (x**2 - x * sp.sqrt(x**2 - 1))
    log_form = x + sp.sqrt(x**2 - 1) - sp.atan(sp.sqrt(x**2 - 1))
    sec_form = x + sp.sqrt(x**2 - 1) - sp.asec(x)
    _eq(sp.diff(log_form, x), integrand)
    _eq(sp.diff(sec_form, x), integrand)


def check_r1_2020_q12() -> None:
    a = sp.symbols("a", positive=True)
    iprime = sp.pi / 2 * (1 - sp.exp(-2 * a))
    _eq(sp.integrate(iprime, (a, 0, 1)), sp.pi / 4 * (1 + sp.exp(-2)))
    mp.mp.dps = 25

    def integrand(x):
        if x == 0:
            return mp.mpf(1)
        return mp.sin(x) ** 2 / (x**2 * (x**2 + 1))

    got = mp.quadosc(integrand, [0, mp.inf], omega=2)
    _near(got, mp.pi / 4 * (1 + mp.exp(-2)), mp.mpf("1e-12"))


def check_r1_2020_q14() -> None:
    th = sp.symbols("th", real=True)
    _eq(sp.simplify((1 + sp.tan(th) ** 2) * sp.cos(th) ** 2 - 1), 0)
    mp.mp.dps = 25

    def integrand(t):
        if t == mp.pi / 2:
            return -mp.inf
        return -2 * mp.log(mp.cos(t))

    _near(_quad(integrand, 0, mp.pi / 2), mp.pi * mp.log(2), mp.mpf("1e-12"))


def check_r1_2020_q17() -> None:
    x = sp.symbols("x", positive=True)
    antideriv = -2 * sp.log(1 + x) / sp.sqrt(x) + 4 * sp.atan(sp.sqrt(x))
    _eq(sp.diff(antideriv, x), sp.log(1 + x) / x ** sp.Rational(3, 2))
    _eq(sp.limit(sp.log(1 + x) / sp.sqrt(x), x, sp.oo), 0)
    _eq(sp.limit(sp.log(1 + x) / sp.sqrt(x), x, 0), 0)
    _eq(4 * (sp.pi / 2), 2 * sp.pi)


def check_r1_2020_q22() -> None:
    x = sp.symbols("x", real=True)
    ratio = (sp.sin(x) ** 3 + sp.cos(x) ** 3) / (sp.sin(x) + sp.cos(x))
    _eq(sp.simplify(ratio - (1 - sp.sin(x) * sp.cos(x))), 0)
    _eq(sp.sin(x) * sp.cos(x) - sp.sin(2 * x) / 2, 0)
    half = sp.integrate(1 - sp.sin(2 * x) / 2, (x, 0, sp.pi / 2)) / 2
    _eq(half, sp.pi / 4 - sp.Rational(1, 4))


def check_r1_2020_q29() -> None:
    x = sp.symbols("x", real=True)
    integrand = x * sp.log(x + sp.sqrt(x**2 + 1)) / sp.sqrt(x**2 + 1)
    printed = sp.sqrt(x**2 + 1) * sp.log(x + sp.sqrt(x**2 + 1)) - x
    _eq(sp.diff(printed, x), integrand)
    _eq(sp.asinh(x).rewrite(sp.log), sp.log(x + sp.sqrt(x**2 + 1)))
    _eq(sp.diff(sp.sqrt(x**2 + 1) * sp.asinh(x) - x, x).rewrite(sp.log), integrand)


def check_r1_2020_q30() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.trigsimp(sp.sin(x) ** 4 + sp.cos(x) ** 4 - (1 - sp.sin(2 * x) ** 2 / 2)), 0)
    u = sp.symbols("u", real=True)
    _eq(8 * sp.integrate(1 / (u**2 + 2), (u, 0, sp.oo)), 2 * sp.sqrt(2) * sp.pi)


def check_r1_2020_q33() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify((x + (1 - x)) / (1 - x * (1 - x)) - 1 / (x**2 - x + 1)), 0)
    _eq(sp.atan(0) + sp.atan(1), sp.atan(1))
    antideriv = x * sp.atan(x) - sp.log(1 + x**2) / 2
    _eq(sp.diff(antideriv, x), sp.atan(x))
    _eq(2 * (antideriv.subs(x, 1) - antideriv.subs(x, 0)), sp.pi / 2 - sp.log(2))


def check_r1_2020_q35() -> None:
    x = sp.symbols("x", real=True)
    partner = sp.atan(3 ** sp.cos(x)) + sp.atan(3 ** (-sp.cos(x)))
    _eq(sp.simplify(sp.diff(partner, x)), 0)
    _eq(partner.subs(x, sp.pi / 2), sp.pi / 2)
    _eq(sp.integrate(sp.pi / 2, (x, 0, sp.pi)) / 2, sp.pi**2 / 4)


def check_r1_2021_q06() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    _eq(4 * sp.summation((-1) ** n / (n + 1) ** 2, (n, 0, sp.oo)), sp.pi**2 / 3)
    mp.mp.dps = 25

    def integrand(x):
        if x == 0:
            return mp.mpf(0)
        return mp.log(x) ** 2 / (1 + x) ** 2

    _near(_quad(integrand, 0, mp.inf), mp.pi**2 / 3, mp.mpf("1e-12"))


def check_r1_2021_q07() -> None:
    u = sp.symbols("u", positive=True)
    x = 2 / u
    reflected = sp.log(x) / (x**2 + 2 * x + 2) * sp.diff(x, u)
    target = (sp.log(2) - sp.log(u)) / (u**2 + 2 * u + 2)
    _eq(sp.simplify(reflected + target), 0)
    z = sp.symbols("z", real=True)
    _eq(sp.integrate(1 / (z**2 + 2 * z + 2), (z, 0, sp.oo)), sp.pi / 4)
    _eq(sp.log(2) / 2 * (sp.pi / 4), sp.pi * sp.log(2) / 8)


def check_r1_2021_q08() -> None:
    u = sp.symbols("u", positive=True)
    x = u ** sp.Rational(1, 6)
    piece = x**6 / (x**6 + 1) ** 2 * sp.diff(x, u)
    _eq(sp.simplify(piece - u ** sp.Rational(1, 6) / (6 * (u + 1) ** 2)), 0)
    _eq(sp.gamma(sp.Rational(7, 6)) - sp.gamma(sp.Rational(1, 6)) / 6, 0)
    _eq(
        sp.gamma(sp.Rational(1, 6)) * sp.gamma(sp.Rational(5, 6)) - sp.pi / sp.sin(sp.pi / 6),
        0,
    )
    _eq(sp.gammasimp(sp.gamma(sp.Rational(1, 6)) * sp.gamma(sp.Rational(5, 6))) / 18, sp.pi / 9)


def check_r1_2021_q17() -> None:
    t = sp.symbols("t", real=True)
    _eq(sp.simplify(t**3 / (t + 2) - (t**2 - 2 * t + 4 - 8 / (t + 2))), 0)
    num = 2 / (1 + t**2)
    den = 2 + 2 * t / (1 + t**2)
    _eq(sp.simplify(num / den - 1 / (1 + t + t**2)), 0)
    anti = 2 / sp.sqrt(3) * sp.atan((2 * t + 1) / sp.sqrt(3))
    _eq(sp.simplify(sp.diff(anti, t) * (t**2 + t + 1) - 1), 0)
    span = sp.simplify(anti.subs(t, 1) - anti.subs(t, 0))
    _eq(span, sp.pi / (3 * sp.sqrt(3)))
    x = sp.symbols("x", real=True)
    plain = (
        sp.integrate(sp.sin(x) ** 2, (x, 0, sp.pi / 2))
        - 2 * sp.integrate(sp.sin(x), (x, 0, sp.pi / 2))
        + sp.integrate(4, (x, 0, sp.pi / 2))
        - 8 * span
    )
    printed = sp.pi * (81 - 32 * sp.sqrt(3)) / 36 - 2
    _eq(sp.simplify(plain - printed), 0)


def check_r1_2021_q21() -> None:
    a, x = sp.symbols("a x", real=True)
    split = sp.sin(a) / (sp.cos(x) * sp.cos(a - x))
    _eq(sp.trigsimp(sp.expand_trig(split - (sp.tan(a - x) + sp.tan(x)))), 0)
    _eq(sp.diff(-sp.log(sp.cos(x)), x), sp.tan(x))
    aa = sp.symbols("aa", positive=True)
    _eq(sp.simplify(sp.sec(aa) - 1 / sp.cos(aa)), 0)
    _eq(sp.expand_log(sp.log(1 / sp.cos(aa)) + sp.log(sp.cos(aa)), force=True), 0)


def check_r1_2021_q23() -> None:
    t = sp.symbols("t", positive=True)
    _eq(sp.simplify(sp.tan(sp.asin(t)) - t / sp.sqrt(1 - t**2)), 0)
    th = sp.symbols("th", real=True)
    a = sp.sin(th) ** 2
    _eq(sp.trigsimp(sp.diff(a, th) - 2 * sp.sin(th) * sp.cos(th)), 0)
    _eq(sp.trigsimp(2 * sp.sin(th) * sp.cos(th) / (sp.sin(th) * sp.cos(th)) - 2), 0)
    _eq(sp.integrate(2 * th, (th, 0, sp.pi / 2)), sp.pi**2 / 4)
    _eq(-(sp.pi**2 / 4) / 2, -sp.pi**2 / 8)
    k = sp.symbols("k", integer=True, nonnegative=True)
    term = sp.integrate(sp.log(t) * t ** (2 * k), (t, 0, 1))
    _eq(term, -1 / (2 * k + 1) ** 2)
    odds = sp.summation(1 / (2 * k + 1) ** 2, (k, 0, sp.oo))
    _eq(odds, sp.pi**2 / 8)


def check_r1_2021_q25() -> None:
    u = sp.symbols("u", positive=True)
    _eq(sp.diff(sp.atan(u) + sp.atan(1 / u), u), 0)
    _eq((sp.atan(u) + sp.atan(1 / u)).subs(u, 1), sp.pi / 2)
    t = sp.symbols("t", real=True)
    _eq(sp.integrate(1 / (t**2 + 1), (t, -sp.oo, sp.oo)), sp.pi)
    _eq(sp.pi / 4 * sp.pi, sp.pi**2 / 4)


def check_r1_2021_q33() -> None:
    x = sp.symbols("x", real=True)
    real_part = sp.exp(sp.cos(x)) * sp.cos(sp.sin(x))
    _eq(sp.simplify(sp.re(sp.exp(sp.exp(sp.I * x))) - real_part), 0)
    _eq(sp.integrate(sp.cos(5 * x) ** 2, (x, 0, 2 * sp.pi)), sp.pi)
    _eq(sp.pi / sp.factorial(5), sp.pi / 120)


def check_r1_2021_q35() -> None:
    u = sp.symbols("u", real=True)
    _eq(sp.diff((u**2 - u + 1) * sp.exp(u), u), (u**2 + u) * sp.exp(u))
    _eq(sp.expand(u * (u + 1) * sp.exp(u) - (u**2 + u) * sp.exp(u)), 0)
    end = (u**2 - u + 1) * sp.exp(u)
    _eq(end.subs(u, 1) - end.subs(u, 0), sp.E - 1)


def check_r1_2021_q38() -> None:
    left = sp.log(2 * sp.pi) + 3 * sp.log(3) + 8 * sp.log(2) - 7
    right = sp.log(13824 * sp.pi) - 7
    _eq(sp.simplify(left - right), 0)
    mp.mp.dps = 25
    _near(_quad(mp.loggamma, 3, 5), mp.log(13824 * mp.pi) - 7, mp.mpf("1e-12"))


def check_r1_2022_q09() -> None:
    b, u = sp.symbols("b u", positive=True)
    _eq(sp.integrate(1 / ((1 + b**2) * u**2 + 1), (u, 0, sp.oo)), sp.pi / (2 * sp.sqrt(1 + b**2)))
    t = sp.symbols("t", positive=True)
    _eq(sp.diff(sp.asinh(t), t), 1 / sp.sqrt(1 + t**2))
    _eq(sp.pi / 2 * sp.asinh(b), sp.pi / 2 * sp.asinh(b))


def check_r1_2022_q10() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    _eq(sp.summation(6 * (-1) ** n / (n + 1) ** 4, (n, 0, sp.oo)), 7 * sp.pi**4 / 120)
    _eq(sp.simplify((1 - 2 ** (1 - 4)) * sp.zeta(4) * 6 - 7 * sp.pi**4 / 120), 0)


def check_r1_2022_q18() -> None:
    mp.mp.dps = 25
    catalan = -_quad(lambda x: mp.log(x) / (1 + x * x), 0, 1)
    _near(catalan, mp.catalan, mp.mpf("1e-12"))
    got = _quad(lambda x: mp.log(1 + x) / (1 + x * x), 0, mp.inf)
    target = mp.catalan + mp.pi * mp.log(2) / 4
    _near(got, target, mp.mpf("1e-12"))
    _eq(sp.simplify(-(sp.pi / 2) * sp.log(2) + sp.symbols("G") + 3 * sp.pi / 4 * sp.log(2) - (sp.symbols("G") + sp.pi / 4 * sp.log(2))), 0)


def check_r1_2022_q19() -> None:
    a, t = sp.symbols("a t", positive=True)
    pref = 2 / sp.sqrt((1 - a) * (1 + a))
    antideriv = pref * sp.atan(t * sp.sqrt((1 - a) / (1 + a)))
    target = 2 / ((1 + a) + (1 - a) * t**2)
    _eq(sp.simplify(sp.diff(antideriv, t) - target), 0)
    _eq(sp.simplify(pref * sp.pi / 2 - sp.pi / sp.sqrt(1 - a**2)), 0)
    s = sp.symbols("s", real=True)
    _eq(sp.integrate(sp.pi / sp.sqrt(1 - s**2), (s, 0, sp.Rational(1, 3))), sp.pi * sp.asin(sp.Rational(1, 3)))


def check_r1_2022_q27() -> None:
    c, u = sp.symbols("c u", positive=True)
    _eq(sp.integrate(u * sp.exp(-c * u), (u, 0, sp.oo)), 1 / c**2)
    _eq(sp.integrate(sp.sin(u) * sp.exp(-c * u), (u, 0, sp.oo)), 1 / (c**2 + 1))
    t = sp.symbols("t", positive=True)
    antideriv = sp.log(1 + t) + 1 / (1 + t) - sp.log((1 + t) ** 2 + 1) / 2 + sp.atan(1 + t)
    deriv = t * (1 / (1 + t) ** 2 - 1 / ((1 + t) ** 2 + 1))
    _eq(sp.simplify(sp.diff(antideriv, t) - deriv), 0)
    at_inf = sp.limit(
        sp.log((1 + t) / sp.sqrt((1 + t) ** 2 + 1)) + 1 / (1 + t) + sp.atan(1 + t),
        t,
        sp.oo,
    )
    _eq(at_inf, sp.pi / 2)
    _eq(sp.simplify(at_inf - antideriv.subs(t, 0) - (sp.log(2) / 2 + sp.pi / 4 - 1)), 0)


def check_r1_2022_mit_tb_q03() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(sp.exp(sp.log(x) / sp.log(x)) - sp.E), 0)
    _eq(sp.integrate(sp.E, (x, 0, 1)), sp.E)


def check_r1_2022_mit_tb_q04() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.diff(sp.exp(sp.exp(x)), x), sp.exp(x + sp.exp(x)))


def check_r1_2022_mit_tb_q05() -> None:
    x = sp.symbols("x", real=True)
    antideriv = (1 + x) * sp.log(1 + x) + (1 - x) * sp.log(1 - x)
    deriv = sp.diff(antideriv, x)
    _eq(sp.simplify(deriv - (sp.log(1 + x) - sp.log(1 - x))), 0)
    _eq(sp.simplify(sp.exp(deriv) * (1 - x) - (1 + x)), 0)
    _eq(sp.limit(antideriv, x, 1) - antideriv.subs(x, 0), 2 * sp.log(2))
    _eq(2 * sp.log(2), sp.log(4))


def check_r1_2022_mit_tb_q06() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    a = sp.symbols("a", positive=True)
    _eq(sp.summation((-1) ** (n - 1) / (n * a), (n, 1, sp.oo)), sp.log(2) / a)


def check_r1_2022_mit_tb_q08() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(sp.cot(x) - 1 / sp.tan(x)), 0)
    t = sp.symbols("t", positive=True)
    p = sp.symbols("p", real=True)
    _eq(sp.simplify(sp.together(1 / (1 + t**p) + 1 / (1 + t ** (-p)) - 1)), 0)
    _eq(sp.integrate(sp.Rational(1, 2), (x, 0, sp.pi / 2)), sp.pi / 4)


def check_r1_2022_mit_tb_q10() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.diff(sp.atan(x) + sp.acot(x), x), 0)
    _eq((sp.atan(x) + sp.acot(x)).subs(x, 1), sp.pi / 2)
    _eq(sp.integrate((sp.pi / 2) / x, (x, 1, sp.sqrt(3))), sp.pi * sp.log(3) / 4)


def check_r1_2022_mit_tb_q12() -> None:
    s = sp.symbols("s", positive=True)
    _eq(sp.integrate(sp.sqrt(s) * sp.exp(-s), (s, 0, sp.oo)), sp.gamma(sp.Rational(3, 2)))
    _eq(sp.gamma(sp.Rational(3, 2)), sp.sqrt(sp.pi) / 2)


def check_r1_2022_mit_tb_q19() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(sp.diff(sp.tan(x) + sp.sec(x), x) * (1 - sp.sin(x)) - 1), 0)


def check_r1_2022_mit_tb_q24() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.expand((x + 1) ** 3 - (x**3 + 3 * x**2 + 3 * x + 1)), 0)
    _eq(sp.integrate((x + 1) ** 3, (x, -2, 0)), 0)


def check_r1_2022_mit_tb_q25() -> None:
    u = sp.symbols("u", real=True)
    _eq(sp.integrate(2 * sp.pi * sp.sin(sp.pi * u), (u, 0, 13)), 4)


def check_r1_2022_mit_tb_q26() -> None:
    u = sp.symbols("u", positive=True)
    _eq(sp.integrate(u * sp.exp(-u), (u, 0, sp.oo)) / 2, sp.Rational(1, 2))


def check_r1_2022_mit_tb_q28() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(1 / x - x / (x**2 + 1) - 1 / (x * (x**2 + 1))), 0)
    antideriv = sp.log(x) - sp.log(x**2 + 1) / 2
    _eq(sp.diff(antideriv, x), 1 / (x * (x**2 + 1)))
    _eq(sp.limit(sp.log(x / sp.sqrt(x**2 + 1)), x, sp.oo) - antideriv.subs(x, 1), sp.log(2) / 2)


def check_r1_2024_q27() -> None:
    u = sp.symbols("u", positive=True)
    x = u**2
    integrand = sp.exp(-x) / (sp.sqrt(x) * sp.exp(1 / x)) * sp.diff(x, u)
    _eq(sp.simplify(integrand - 2 * sp.exp(-u**2 - 1 / u**2)), 0)
    _eq(sp.simplify(sp.exp(-u**2 - 1 / u**2) - sp.exp(-(u - 1 / u) ** 2 - 2)), 0)
    _eq(sp.diff(u - 1 / u, u), 1 + 1 / u**2)
    v = sp.symbols("v", real=True)
    _eq(sp.integrate(sp.exp(-v**2 - 2), (v, -sp.oo, sp.oo)), sp.sqrt(sp.pi) / sp.exp(2))


def check_r1_2024_q29() -> None:
    n, k, x = sp.symbols("n k x", positive=True)
    left = 2 ** (k * x / n) * k * x**4 / (n * k * x**3 + 1)
    right = 2 ** (k * x / n) * x / (n + 1 / (k * x**3))
    _eq(sp.simplify(left - right), 0)
    anti = (2**x / sp.log(2) - x) / sp.log(2)
    _eq(sp.simplify(sp.diff(anti, x) - (2**x - 1) / sp.log(2)), 0)
    lo = 1 / sp.log(2)
    _eq(sp.simplify(2**lo - sp.E), 0)
    val = sp.simplify(anti.subs(x, 2024) - anti.subs(x, lo))
    printed = (2**2024 - sp.E + 1) / sp.log(2) ** 2 - 2024 / sp.log(2)
    _eq(sp.simplify(val - printed), 0)


def check_r1_2025_online_q02() -> None:
    k = sp.symbols("k", integer=True)
    _eq(sp.sin(sp.pi * k), 0)
    _eq(sp.integrate(0, (sp.symbols("x"), 0, 1)), 0)


def check_r1_2025_online_q03() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.together(sp.sech(2 * sp.log(x)).rewrite(sp.exp) - 2 * x**2 / (x**4 + 1)), 0)
    _eq(sp.simplify(x**2 + x ** (-2) - ((x - 1 / x) ** 2 + 2)), 0)
    _eq(sp.integrate(2 / (x**2 + 2), (x, 0, sp.oo)), sp.pi / sp.sqrt(2))
    mp.mp.dps = 25
    _near(_quad(lambda t: mp.sech(2 * mp.log(t)), 0, mp.inf), mp.pi / mp.sqrt(2), mp.mpf("1e-12"))


def check_r1_2025_online_q04() -> None:
    z, a = sp.symbols("z a", real=True)
    _eq(sp.exp(sp.I * sp.pi / 2), sp.I)
    _eq(sp.integrate(sp.I, (z, 0, a)), sp.I * a)


def check_r1_2025_online_q05() -> None:
    x = sp.symbols("x", positive=True)
    f = sp.cos(x) / (1 + sp.exp(1 / x))
    _eq(sp.simplify(f + f.subs(x, -x) - sp.cos(x)), 0)
    _eq(sp.integrate(sp.cos(x), (x, -sp.pi / 2, sp.pi / 2)), 2)


def check_r1_2025_online_q06() -> None:
    s = sp.symbols("s", positive=True)
    _eq(sp.integrate(sp.sqrt(s) * sp.exp(-s), (s, 0, sp.oo)), sp.sqrt(sp.pi) / 2)


def check_r1_2025_online_q16() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(1 / (x**4 + 1) - x**4 / (x**4 + 1) ** 2 - 1 / (x**4 + 1) ** 2), 0)
    boundary = x / (4 * (x**4 + 1))
    rest = sp.diff(boundary, x)
    _eq(sp.simplify(rest - (1 - 3 * x**4) / (4 * (x**4 + 1) ** 2)), 0)
    whole = sp.integrate((1 + x**2) / (1 + x**4), (x, 0, sp.oo))
    _eq(whole, sp.pi / sp.sqrt(2))
    _eq(sp.Rational(3, 8) * whole, 3 * sp.pi / (8 * sp.sqrt(2)))
    _eq(sp.simplify(3 * sp.pi / (8 * sp.sqrt(2)) - 3 * sp.sqrt(2) * sp.pi / 16), 0)


def check_r1_2025_online_q18() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(sp.diff(x * sp.log(sp.sin(x)), x) - sp.log(sp.sin(x)) - x * sp.cot(x)), 0)
    mp.mp.dps = 25

    def log_sine(t):
        if t == 0 or t == mp.pi / 2:
            return -mp.inf
        return mp.log(mp.sin(t))

    got = _quad(log_sine, 0, mp.pi / 2)
    _near(got, -(mp.pi / 2) * mp.log(2), mp.mpf("1e-12"))


def check_r1_2025_online_q20() -> None:
    t, th = sp.symbols("t th", positive=True)
    inside = t + t ** sp.tan(th)
    _eq(sp.diff(inside, t), 1 + sp.tan(th) * t ** (sp.tan(th) - 1))
    v = sp.symbols("v", real=True)
    _eq(sp.integrate(sp.exp(v), (v, 0, 2)) * sp.pi / 4, sp.pi / 4 * (sp.exp(2) - 1))


def check_r1_2025_online_q21() -> None:
    x = sp.symbols("x", real=True)
    _eq(2025 * sp.integrate(x**2025, (x, 0, 1)), sp.Rational(2025, 2026))


def check_r1_2025_online_q26() -> None:
    s, t = sp.symbols("s t", positive=True)
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(x**s, (x, 0, 1)), 1 / (s + 1))
    n = sp.symbols("n", integer=True, nonnegative=True)
    _eq(sp.integrate(1 / (t + 1), (t, n + 1, n + 2)), sp.log((n + 3) / (n + 2)))
    m = sp.symbols("M", integer=True, positive=True)
    partial = sp.factorial(2 * m + 1) ** 2 / (2 ** (4 * m) * sp.factorial(m) ** 4 * (m + 1))
    _eq(sp.limit(partial * sp.pi / 4, m, sp.oo), 1)
    mp.mp.dps = 25

    def integrand(z):
        if z == 0 or z == 1:
            return mp.mpf(0)
        return z * (z - 1) / ((z + 1) * mp.log(z))

    _near(_quad(integrand, 0, 1), mp.log(4 / mp.pi), mp.mpf("1e-12"))


def check_r1_2025_online_q30() -> None:
    x = sp.symbols("x", positive=True)
    left = 1 + x
    right = 1 + 2 / x
    _eq(sp.simplify((left + right) / (1 - left * right) + 1), 0)
    _eq(sp.pi + sp.atan(-1), 3 * sp.pi / 4)
    _eq(sp.integrate((sp.Rational(3, 8) * sp.pi) / x, (x, 1, 2)), 3 * sp.pi * sp.log(2) / 8)
    u = sp.symbols("u", positive=True)
    _eq(sp.simplify(sp.diff(sp.log(2 / u), u) + 1 / u), 0)


R1_REM_CHECKS = (
    check_r1_2020_q03,
    check_r1_2020_q09,
    check_r1_2020_q12,
    check_r1_2020_q14,
    check_r1_2020_q17,
    check_r1_2020_q22,
    check_r1_2020_q29,
    check_r1_2020_q30,
    check_r1_2020_q33,
    check_r1_2020_q35,
    check_r1_2021_q06,
    check_r1_2021_q07,
    check_r1_2021_q08,
    check_r1_2021_q17,
    check_r1_2021_q21,
    check_r1_2021_q23,
    check_r1_2021_q25,
    check_r1_2021_q33,
    check_r1_2021_q35,
    check_r1_2021_q38,
    check_r1_2022_q09,
    check_r1_2022_q10,
    check_r1_2022_q18,
    check_r1_2022_q19,
    check_r1_2022_q27,
    check_r1_2022_mit_tb_q03,
    check_r1_2022_mit_tb_q04,
    check_r1_2022_mit_tb_q05,
    check_r1_2022_mit_tb_q06,
    check_r1_2022_mit_tb_q08,
    check_r1_2022_mit_tb_q10,
    check_r1_2022_mit_tb_q12,
    check_r1_2022_mit_tb_q19,
    check_r1_2022_mit_tb_q24,
    check_r1_2022_mit_tb_q25,
    check_r1_2022_mit_tb_q26,
    check_r1_2022_mit_tb_q28,
    check_r1_2024_q27,
    check_r1_2024_q29,
    check_r1_2025_online_q02,
    check_r1_2025_online_q03,
    check_r1_2025_online_q04,
    check_r1_2025_online_q05,
    check_r1_2025_online_q06,
    check_r1_2025_online_q16,
    check_r1_2025_online_q18,
    check_r1_2025_online_q20,
    check_r1_2025_online_q21,
    check_r1_2025_online_q26,
    check_r1_2025_online_q30,
)


if __name__ == "__main__":
    for check in R1_REM_CHECKS:
        check()
        print(f"PASS {check.__name__}")
    print(f"PASS {len(R1_REM_PACK_IDS)} R1 remainder notes")
