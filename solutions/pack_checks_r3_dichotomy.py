"""SymPy checks for the 2024 Round 3 Dichotomy and tiebreaker notes.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

DICHOTOMY_PACK_IDS = (
    "R3-2024-Dichotomy-S1-Q01a",
    "R3-2024-Dichotomy-S1-Q01b",
    "R3-2024-Dichotomy-S1-Q02a",
    "R3-2024-Dichotomy-S1-Q02b",
    "R3-2024-Dichotomy-S1-Q03a",
    "R3-2024-Dichotomy-S1-Q03b",
    "R3-2024-Dichotomy-S1-Q04a",
    "R3-2024-Dichotomy-S1-Q04b",
    "R3-2024-Dichotomy-S1-Q05a",
    "R3-2024-Dichotomy-S1-Q05b",
    "R3-2024-Dichotomy-S1-Q06a",
    "R3-2024-Dichotomy-S1-Q06b",
    "R3-2024-Dichotomy-S1-Q07a",
    "R3-2024-Dichotomy-S1-Q07b",
    "R3-2024-Dichotomy-S2-Q01a",
    "R3-2024-Dichotomy-S2-Q01b",
    "R3-2024-Dichotomy-S2-Q02a",
    "R3-2024-Dichotomy-S2-Q02b",
    "R3-2024-Dichotomy-S2-Q03a",
    "R3-2024-Dichotomy-S2-Q03b",
    "R3-2024-Dichotomy-S2-Q04a",
    "R3-2024-Dichotomy-S2-Q04b",
    "R3-2024-Dichotomy-S2-Q05a",
    "R3-2024-Dichotomy-S2-Q05b",
    "R3-2024-Dichotomy-S2-Q06a",
    "R3-2024-Dichotomy-S2-Q06b",
    "R3-2024-Dichotomy-S2-Q07a",
    "R3-2024-Dichotomy-S2-Q07b",
    "R3-2024-Dichotomy-S3-Q01a",
    "R3-2024-Dichotomy-S3-Q01b",
    "R3-2024-Dichotomy-S3-Q02a",
    "R3-2024-Dichotomy-S3-Q02b",
    "R3-2024-Dichotomy-S3-Q03a",
    "R3-2024-Dichotomy-S3-Q03b",
    "R3-2024-Dichotomy-S3-Q04a",
    "R3-2024-Dichotomy-S3-Q04b",
    "R3-2024-Dichotomy-S3-Q05a",
    "R3-2024-Dichotomy-S3-Q05b",
    "R3-2024-Dichotomy-S3-Q06a",
    "R3-2024-Dichotomy-S3-Q06b",
    "R3-2024-Dichotomy-S3-Q07a",
    "R3-2024-Dichotomy-S3-Q07b",
    "R3-2024-TB1-Q01",
    "R3-2024-TB2-Q01",
    "R3-2024-TB3-Q01",
    "R3-2024-TB4-Q01",
)


def _eq(left, right) -> None:
    if sp.simplify(left - right) != 0:
        raise AssertionError(f"{left} != {right}")


def _near(got, target, tol) -> None:
    err = abs(mp.mpf(got) - mp.mpf(target))
    if err >= tol:
        raise AssertionError(f"{got} vs {target}, err {err}")


def check_r3_2024_dichotomy_s1_q01a() -> None:
    x = sp.symbols("x")
    _eq(sp.integrate(sp.sqrt(4 - x**2), (x, 0, 2)), sp.pi)


def check_r3_2024_dichotomy_s1_q01b() -> None:
    a = sp.sqrt(2)
    area = 2 * sp.asin(a / 2) + a * sp.sqrt(4 - a**2) / 2
    _eq(area, sp.pi / 2 + 1)


def check_r3_2024_dichotomy_s1_q02a() -> None:
    x = sp.symbols("x", real=True)
    u = sp.symbols("u", positive=True)
    anti_u = sp.Rational(1, 2) * (sp.log(1 + u) - sp.log(1 - u)) + sp.atan(u)
    _eq(sp.diff(anti_u, u) * (1 + u**2), 2 / (1 - u**2))
    f1 = sp.Rational(1, 2) * (sp.log(1 + sp.tan(x)) - sp.log(1 - sp.tan(x))) + x
    f2 = x - sp.Rational(1, 2) * (
        sp.log(sp.cos(x) - sp.sin(x)) - sp.log(sp.cos(x) + sp.sin(x))
    )
    f3 = sp.atanh(sp.tan(x)) + x
    _eq(sp.diff(f1 - f2, x), 0)
    _eq(sp.diff(f1 - f3, x), 0)
    _eq((f1 - f2).subs(x, 0), 0)
    _eq(sp.simplify(f3.rewrite(sp.log) - f1), 0)


def check_r3_2024_dichotomy_s1_q02b() -> None:
    x = sp.symbols("x", real=True)
    ratio = sp.tan(x) / sp.tan(2 * x)
    reduced = (1 - sp.tan(x) ** 2) / 2
    _eq(sp.expand_trig(sp.tan(2 * x) * (1 - sp.tan(x) ** 2) - 2 * sp.tan(x)), 0)
    _eq(sp.diff(x - sp.tan(x) / 2, x), reduced)
    _eq(sp.simplify(sp.expand_trig(ratio - reduced)), 0)


def check_r3_2024_dichotomy_s1_q03a() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    series = sp.summation((-1) ** n / (n + 1) ** 2, (n, 0, sp.oo))
    _eq(2 * series, sp.pi**2 / 6)


def check_r3_2024_dichotomy_s1_q03b() -> None:
    y = sp.symbols("y", positive=True)
    e = sp.E
    u = y ** (1 / e)
    du = sp.diff(u, y)
    changed = sp.simplify(2 * u / (1 + u**e) * du)
    _eq(changed, (2 / e) * y ** (2 / e - 1) / (1 + y))
    z = sp.symbols("z", positive=True)
    _eq(sp.gamma(z) * sp.gamma(1 - z), sp.pi / sp.sin(sp.pi * z))
    b = 2 / e
    _eq((2 / e) * sp.pi / sp.sin(sp.pi * b), (2 * sp.pi / e) * sp.csc(2 * sp.pi / e))


def check_r3_2024_dichotomy_s1_q04a() -> None:
    m = sp.symbols("m", integer=True, positive=True)
    _eq(sp.summation(m / 4**m, (m, 1, sp.oo)), sp.Rational(4, 9))
    x = sp.symbols("x", positive=True)
    value = sp.integrate(x**2 * 2 ** (-sp.Rational(4, 9) * x), (x, 0, sp.oo))
    _eq(value, 729 / (32 * sp.log(2) ** 3))


def check_r3_2024_dichotomy_s1_q04b() -> None:
    x, f = sp.symbols("x f", positive=True)
    _eq(sp.expand(f**2 * (x + f) - x**2 - (f**3 + f**2 * x - x**2)), 0)
    g = sp.symbols("g", positive=True)
    _eq(sp.expand(g**2 - x**3 - x**2 * g - (g**2 - x**2 * g - x**3)), 0)
    y = sp.symbols("y", positive=True)
    inverse_eq = x**2 - y**2 * x - y**3
    forward_eq = y**3 + y**2 * x - x**2
    _eq(sp.expand(inverse_eq + forward_eq), 0)
    half = sp.Rational(1, 2)
    _eq(half**2 - (half**3 + half**2 * half), 0)
    _eq(half * half, sp.Rational(1, 4))


def check_r3_2024_dichotomy_s1_q05a() -> None:
    t = sp.symbols("t", positive=True)
    anti = t / sp.log(sp.log(t))
    num = sp.expand_log(sp.log(t ** (sp.log(sp.log(t)) ** 2) / sp.log(t)), force=True)
    den = sp.log(sp.log(t)) ** 3 * sp.log(t)
    _eq(sp.diff(anti, t), num / den)
    upper = sp.exp(sp.E)
    lower = sp.exp(2)
    _eq(anti.subs(t, upper) - anti.subs(t, lower), upper - lower / sp.log(2))


def check_r3_2024_dichotomy_s1_q05b() -> None:
    def integrand(xv):
        xv = mp.mpf(xv)
        lx = mp.log(xv)
        return (mp.log(1 - lx) + 1 - lx) * lx

    with mp.workdps(25):
        _near(mp.quad(integrand, [0, 1]), -4, mp.mpf("1e-12"))


def check_r3_2024_dichotomy_s1_q06a() -> None:
    a, b = sp.symbols("a b", real=True)
    added = (sp.tan(a) + sp.tan(b)) / (1 - sp.tan(a) * sp.tan(b))
    _eq(sp.simplify(added - sp.tan(a + b)), 0)
    _eq(sp.integrate(sp.tan(1), (a, 0, sp.pi / 2)) / 2, sp.pi / 4 * sp.tan(1))


def check_r3_2024_dichotomy_s1_q06b() -> None:
    x = sp.symbols("x", real=True)
    left = (sp.cos(x) + sp.sin(x)) / (sp.sqrt(2) * sp.sin(x))
    right = sp.cos(sp.pi / 4 - x) / sp.sin(x)
    _eq(sp.simplify(left - right), 0)
    _eq(sp.simplify(sp.tan(x) * sp.cot(x) - 1), 0)
    _eq(sp.integrate(sp.log(1), (x, 0, sp.pi / 4)), 0)


def check_r3_2024_dichotomy_s1_q07a() -> None:
    x = sp.symbols("x", positive=True)
    a = sp.atan(x)
    c = sp.acot(x)
    _eq(sp.diff(a + c, x), 0)
    _eq((a + c).subs(x, 1), sp.pi / 2)
    _eq(sp.expand((1 + a) * (1 + c) - (1 + (a + c) + a * c)), 0)
    u = sp.symbols("u", real=True)
    anti = sp.log(1 + u) - sp.log(1 + sp.pi / 2 - u)
    piece = anti.subs(u, sp.pi / 4) - anti.subs(u, 0)
    _eq(piece / (2 + sp.pi / 2), sp.log(1 + sp.pi / 2) / (2 + sp.pi / 2))


def check_r3_2024_dichotomy_s1_q07b() -> None:
    u = sp.symbols("u", real=True)
    quad = 1 + sp.pi / 2 * u - u**2
    completed = (1 + sp.pi**2 / 16) - (u - sp.pi / 4) ** 2
    _eq(sp.expand(quad - completed), 0)
    root = sp.sqrt(16 + sp.pi**2)
    z = sp.pi / root
    w = sp.symbols("w", positive=True)
    gap = sp.atanh(w).rewrite(sp.log) - sp.log((1 + w) / (1 - w)) / 2
    _eq(sp.exp(2 * gap), 1)
    _eq(sp.expand((1 + z) * (root - sp.pi) - (1 - z) * (root + sp.pi)), 0)


def check_r3_2024_dichotomy_s2_q01a() -> None:
    x = sp.symbols("x", positive=True)
    anti = -sp.log(x**4 + 1) / (2 * x**2)
    _eq(sp.diff(anti, x), sp.log(x**4 + 1) / x**3 - 2 * x / (x**4 + 1))
    _eq(sp.integrate(2 * x / (x**4 + 1), (x, 0, 1)), sp.pi / 4)
    _eq(-sp.log(2) / 2 + sp.pi / 4, sp.pi / 4 - sp.log(2) / 2)


def check_r3_2024_dichotomy_s2_q01b() -> None:
    x = sp.symbols("x", real=True)
    f = sp.log(x**4 + 1) / x**3
    _eq(sp.simplify(f + f.subs(x, -x)), 0)


def check_r3_2024_dichotomy_s2_q02a() -> None:
    y = sp.symbols("y", positive=True)
    changed = sp.simplify(2 * y / ((y**2 + 1) * y + 2 * y**2))
    _eq(changed, 2 / (y + 1) ** 2)
    _eq(sp.diff(-2 / (y + 1), y), changed)


def check_r3_2024_dichotomy_s2_q02b() -> None:
    y = sp.symbols("y", positive=True)
    changed = sp.simplify(2 * y / ((y + 1) * y**2 + 2 * y))
    anti = 4 / sp.sqrt(7) * sp.atan((2 * y + 1) / sp.sqrt(7))
    _eq(sp.diff(anti, y), changed)


def check_r3_2024_dichotomy_s2_q03a() -> None:
    x = sp.symbols("x", positive=True)
    integrand = (5 * x**2 + 3 * x - 2) / (x**3 + 2 * x**2)
    part = 3 / (x + 2) + 2 / x - 1 / x**2
    _eq(sp.together(integrand - part), 0)
    anti = 3 * sp.log(x + 2) + 2 * sp.log(x) + 1 / x
    _eq(sp.diff(anti, x), integrand)


def check_r3_2024_dichotomy_s2_q03b() -> None:
    x = sp.symbols("x", positive=True)
    integrand = (x + 1) ** 2 / ((x + 2) * (x**2 + x + 1))
    anti = sp.Rational(1, 3) * (sp.log(x**2 + x + 1) + sp.log(x + 2))
    other = sp.Rational(1, 3) * sp.log(1 + (x + 1) ** 3)
    _eq(sp.diff(anti, x), integrand)
    _eq(sp.diff(other, x), integrand)
    _eq(sp.expand((x + 2) * (x**2 + x + 1) - (1 + (x + 1) ** 3)), 0)


def check_r3_2024_dichotomy_s2_q04a() -> None:
    x = sp.symbols("x", positive=True)
    raw = 1 / ((x + sp.sqrt(x**2 + 1)) * (1 + x**2))
    rational = (sp.sqrt(x**2 + 1) - x) / (1 + x**2)
    _eq(sp.simplify(raw - rational), 0)
    anti = sp.asinh(x) - sp.Rational(1, 2) * sp.log(x**2 + 1)
    _eq(sp.diff(anti, x), rational)
    end = sp.log((x + sp.sqrt(x**2 + 1)) / sp.sqrt(x**2 + 1))
    _eq(sp.limit(end, x, sp.oo) - end.subs(x, 0), sp.log(2))


def check_r3_2024_dichotomy_s2_q04b() -> None:
    s2 = sp.sqrt(2)
    first = -1 - sp.log(2) - (s2 + 1) * sp.log(s2 - 1) + (s2 - 1) * sp.log(s2 + 1)
    second = -1 - sp.log(2) + 2 * s2 * sp.log(1 + s2)
    third = -1 - sp.log(2) + 2 * s2 * sp.asinh(1)
    fourth = -1 - sp.log(2) + 2 * s2 * sp.atanh(1 / s2)
    _eq(sp.simplify(first - second), 0)
    _eq(third - second, 0)
    _eq(sp.simplify(fourth.rewrite(sp.log) - second), 0)

    def integrand(t):
        t = mp.mpf(t)
        return (mp.sqrt(t * t + 1) - t) / (t + 1)

    with mp.workdps(25):
        _near(mp.quad(integrand, [0, mp.inf]), second.evalf(25), mp.mpf("1e-12"))


def check_r3_2024_dichotomy_s2_q05a() -> None:
    x = sp.symbols("x", positive=True)
    squared = 1 + ((x**4 - 1) / (2 * x**2)) ** 2
    _eq(sp.factor(sp.together(squared - ((x**4 + 1) / (2 * x**2)) ** 2)), 0)
    inside = 1 + (x**4 + 1) / (2 * x**2)
    half = sp.Rational(1, 2) * (x + 1 / x) ** 2
    _eq(sp.simplify(inside - half), 0)
    logged = sp.integrate(sp.log(x + 1 / x), (x, 0, 1))
    _eq(logged, -1 + sp.log(2) + sp.pi / 2)
    _eq(-sp.log(2) + 2 * logged, sp.log(2) + sp.pi - 2)


def check_r3_2024_dichotomy_s2_q05b() -> None:
    x = sp.symbols("x", positive=True)
    squared = 1 + ((x**4 - 1) / (2 * x**2)) ** 2
    _eq(sp.factor(sp.together(squared - ((x**4 + 1) / (2 * x**2)) ** 2)), 0)
    inside = -1 - (x**4 + 1) / (2 * x**2)
    target = -sp.Rational(1, 2) * (x + 1 / x) ** 2
    _eq(sp.simplify(inside - target), 0)
    _eq(sp.expand((x + 1 / x) ** 2 - ((x - 1 / x) ** 2 + 4)), 0)
    gauss = sp.integrate(sp.exp(-sp.Rational(1, 2) * x**2), (x, -sp.oo, sp.oo))
    printed = sp.sqrt(2 * sp.pi) / (2 * sp.E**2)
    _eq(sp.exp(-2) * gauss / 2, printed)

    def integrand(t):
        t = mp.mpf(t)
        return mp.e ** (-mp.mpf("0.5") * (t + 1 / t) ** 2)

    with mp.workdps(25):
        _near(mp.quad(integrand, [0, mp.inf]), printed.evalf(25), mp.mpf("1e-12"))


def check_r3_2024_dichotomy_s2_q06a() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(sp.sin(x) ** 2 / x**2, (x, 0, sp.oo)), sp.pi / 2)
    _eq(-sp.log(2) * sp.pi / 2, -sp.pi * sp.log(2) / 2)


def check_r3_2024_dichotomy_s2_q06b() -> None:
    u = sp.symbols("u", positive=True)
    direct = sp.sin(u) ** 2 / u**2
    shifted = 2 * sp.sin(u / 2) ** 2 / u**2
    changed = sp.simplify(shifted.subs(u, 2 * u) * 2)
    _eq(changed, direct)


def check_r3_2024_dichotomy_s2_q07a() -> None:
    n = sp.symbols("n", positive=True)
    term = n * sp.log(1 + sp.E / n + n ** (-2 / sp.E))
    if sp.limit(term, n, sp.oo) != sp.oo:
        raise AssertionError(term)


def check_r3_2024_dichotomy_s2_q07b() -> None:
    n = sp.symbols("n", positive=True)
    _eq(sp.limit(n * sp.log(1 + 3 / n), n, sp.oo), 3)
    _eq(sp.limit(1 / (1 + 2 / n), n, sp.oo), 1)
    _eq(3 + 1, 4)


def check_r3_2024_dichotomy_s3_q01a() -> None:
    x = sp.symbols("x", positive=True)
    anti = sp.atan(x) + sp.atan(x**3) / 3
    _eq(sp.diff(anti, x), (x**4 + 1) / (x**6 + 1))
    _eq(anti.subs(x, 1) - anti.subs(x, 0), sp.pi / 3)


def check_r3_2024_dichotomy_s3_q01b() -> None:
    x = sp.symbols("x", positive=True)
    anti = sp.Rational(1, 3) * (
        2 * sp.log(x + 1)
        + sp.Rational(1, 2) * sp.log(x**2 - x + 1)
        + sp.sqrt(3) * sp.atan((2 * x - 1) / sp.sqrt(3))
    )
    _eq(sp.diff(anti, x), (x**2 + 1) / (x**3 + 1))
    value = sp.simplify(anti.subs(x, 1) - anti.subs(x, 0))
    _eq(value, sp.Rational(1, 3) * (2 * sp.log(2) + sp.sqrt(3) * sp.pi / 3))


def check_r3_2024_dichotomy_s3_q02a() -> None:
    x = sp.symbols("x", real=True)
    u = sp.sqrt(1 + sp.sqrt(sp.exp(x)))
    _eq(sp.simplify(sp.diff(u, x) - (u**2 - 1) / (4 * u)), 0)
    s2 = sp.sqrt(2)
    _eq(sp.expand((s2 - 1) * (s2 + 1) - 1), 0)
    closed = 2 * (sp.log(s2 + 1) - sp.log(s2 - 1))
    replaced = closed.subs(sp.log(s2 - 1), -sp.log(s2 + 1))
    _eq(sp.simplify(replaced), 4 * sp.log(1 + s2))
    _eq(sp.simplify(sp.asinh(1).rewrite(sp.log) - sp.log(1 + s2)), 0)
    z = 1 / s2
    _eq(sp.expand((1 + z) * (s2 - 1) * s2 - (s2 + 1) * s2 * (1 - z)), 0)
    _eq(sp.expand((s2 + 1) ** 2 * (s2 - 1) - (s2 + 1)), 0)


def check_r3_2024_dichotomy_s3_q02b() -> None:
    u = sp.symbols("u", positive=True)
    _eq(sp.diff((u**2 + 1) ** 2, u), 4 * u * (1 + u**2))
    value = 4 * (
        sp.integrate(u * sp.exp(-u), (u, 0, sp.oo))
        + sp.integrate(u**3 * sp.exp(-u), (u, 0, sp.oo))
    )
    _eq(value, 28)


def check_r3_2024_dichotomy_s3_q03a() -> None:
    _eq(sp.csc(4 * sp.pi / 9), sp.sec(sp.pi / 18))
    _eq(sp.pi / 3 * sp.csc(4 * sp.pi / 9), sp.pi / 3 * sp.sec(sp.pi / 18))


def check_r3_2024_dichotomy_s3_q03b() -> None:
    b = 4
    a = sp.Rational(1, 3)
    formula = sp.pi / b * sp.csc((a + 1) / b * sp.pi)
    _eq(sp.simplify(formula), sp.pi / (2 * sp.sqrt(3)))


def check_r3_2024_dichotomy_s3_q04a() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    x = sp.symbols("x", positive=True)
    term = sp.integrate(x ** (-(4 * n + 3)), (x, 1, sp.oo))
    _eq(term, 1 / (4 * n + 2))
    _eq(sp.simplify(1 / ((2 * n + 1) * (4 * n + 2))), 1 / (2 * (2 * n + 1) ** 2))
    _eq(sp.summation((-1) ** n / (2 * n + 1) ** 2, (n, 0, sp.oo)), sp.Catalan)


def check_r3_2024_dichotomy_s3_q04b() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(sp.atan(1 / x) / x**2, (x, 1, sp.oo)), sp.pi / 4 - sp.log(2) / 2)


def check_r3_2024_dichotomy_s3_q05a() -> None:
    x = sp.symbols("x", positive=True)
    cube = ((1 + 3 / x) ** x) ** sp.Rational(1, 3)
    square = ((1 + 2 / x) ** x) ** sp.Rational(1, 2)
    _eq(sp.simplify(cube - (1 + 1 / (x / 3)) ** (x / 3)), 0)
    _eq(sp.simplify(square - (1 + 1 / (x / 2)) ** (x / 2)), 0)
    t = sp.symbols("t", positive=True)
    f = (1 + 1 / t) ** t
    _eq(sp.limit(f, t, 0), 1)
    _eq(sp.limit(f, t, sp.oo), sp.E)
    _eq((1 - sp.E) * sp.log(sp.Rational(3, 2)), (sp.E - 1) * sp.log(sp.Rational(2, 3)))


def check_r3_2024_dichotomy_s3_q05b() -> None:
    x = sp.symbols("x", real=True)
    completed = (x + sp.sqrt(3 * sp.pi) / 2) ** 2 + sp.pi / 4
    _eq(sp.expand(completed - (x**2 + x * sp.sqrt(3 * sp.pi) + sp.pi)), 0)
    fresnel = sp.integrate(sp.sin(x**2), (x, 0, sp.oo))
    _eq(fresnel, sp.sqrt(sp.pi / 8))
    _eq(sp.sqrt(2) * 2 * fresnel, sp.sqrt(sp.pi))


def check_r3_2024_dichotomy_s3_q06a() -> None:
    x = sp.symbols("x", real=True)
    factored = (sp.cos(x) ** 4 + sp.sin(x) ** 4) * (sp.cos(x) ** 2 - sp.sin(x) ** 2)
    _eq(sp.simplify(factored - (sp.cos(x) ** 8 - sp.sin(x) ** 8)), 0)
    reduced = sp.cos(2 * x) * (1 - sp.sin(2 * x) ** 2 / 2)
    _eq(sp.trigsimp(factored - reduced), 0)
    anti = sp.sin(2 * x) / 2 - sp.sin(2 * x) ** 3 / 12
    _eq(anti.subs(x, sp.pi / 4) - anti.subs(x, 0), sp.Rational(5, 12))


def check_r3_2024_dichotomy_s3_q06b() -> None:
    x = sp.symbols("x", real=True)
    reduced = sp.cos(2 * x) * (1 - sp.sin(2 * x) ** 2 / 4)
    _eq(sp.simplify(sp.cos(x) ** 6 - sp.sin(x) ** 6 - reduced), 0)
    anti = sp.sin(2 * x) / 2 - sp.sin(2 * x) ** 3 / 24
    _eq(anti.subs(x, sp.pi / 4) - anti.subs(x, 0), sp.Rational(11, 24))


def check_r3_2024_dichotomy_s3_q07a() -> None:
    u = sp.symbols("u", real=True)
    piece = sp.sin(2 * u) / 2 * sp.log(sp.tan(u)) - u
    _eq(sp.simplify(sp.diff(piece, u) - sp.cos(2 * u) * sp.log(sp.tan(u))), 0)
    _eq(sp.limit(sp.sin(2 * u) * sp.log(sp.tan(u)), u, 0), 0)
    _eq(sp.limit(sp.sin(2 * u) * sp.log(sp.tan(u)), u, sp.pi / 2), 0)
    _eq(-2 * (-sp.pi / 2), sp.pi)


def check_r3_2024_dichotomy_s3_q07b() -> None:
    u = sp.symbols("u", real=True)
    y = sp.symbols("y", positive=True)
    parts = sp.sin(u) * sp.log(sp.cos(u))
    _eq(
        sp.simplify(sp.diff(parts, u) - (sp.cos(u) * sp.log(sp.cos(u)) - sp.sin(u) ** 2 / sp.cos(u))),
        0,
    )
    rational = sp.integrate(y**2 / (1 - y**2), (y, 0, 1 / sp.sqrt(2)))
    one_side = -sp.sqrt(2) * sp.log(2) / 2 + 2 * rational
    target = -sp.sqrt(2) * sp.log(2) / 2 - sp.sqrt(2) + 2 * sp.log(1 + sp.sqrt(2))
    _eq(sp.simplify(one_side - target), 0)
    full = sp.log(2) + sp.sqrt(2) * target
    _eq(sp.simplify(full), 2 * sp.sqrt(2) * sp.log(1 + sp.sqrt(2)) - 2)


def check_r3_2024_tb1_q01() -> None:
    x = sp.symbols("x")
    _eq(sp.integrate(sp.sin(4 * x) / sp.sin(x), (x, 0, sp.pi / 2)), sp.Rational(4, 3))


def check_r3_2024_tb2_q01() -> None:
    x = sp.symbols("x", real=True)
    anti = sp.log(sp.exp(sp.exp(x)) + sp.exp(x))
    integrand = (sp.exp(sp.exp(x)) + 1) / (sp.exp(sp.exp(x) - x) + 1)
    _eq(sp.diff(anti, x), integrand)


def check_r3_2024_tb3_q01() -> None:
    x = sp.symbols("x", positive=True)
    integrand = 1 / ((x + 2) * sp.sqrt((x + 1) * (x + 3)))
    _eq(sp.diff(sp.asec(x + 2), x), integrand)
    atan = 2 * sp.atan(sp.sqrt((x + 1) / (x + 3)))
    _eq(sp.simplify(sp.diff(atan, x) / integrand), 1)


def check_r3_2024_tb4_q01() -> None:
    x = sp.symbols("x", real=True)
    f = 1 / (3**x + sp.sqrt(3))
    paired = sp.together(f + f.subs(x, 1 - x))
    _eq(sp.simplify(paired * sp.sqrt(3) - 1), 0)
    _eq(sp.Integer(2025 - (-2024)) / (2 * sp.sqrt(3)), 4049 / (2 * sp.sqrt(3)))


DICHOTOMY_CHECKS = (
    check_r3_2024_dichotomy_s1_q01a,
    check_r3_2024_dichotomy_s1_q01b,
    check_r3_2024_dichotomy_s1_q02a,
    check_r3_2024_dichotomy_s1_q02b,
    check_r3_2024_dichotomy_s1_q03a,
    check_r3_2024_dichotomy_s1_q03b,
    check_r3_2024_dichotomy_s1_q04a,
    check_r3_2024_dichotomy_s1_q04b,
    check_r3_2024_dichotomy_s1_q05a,
    check_r3_2024_dichotomy_s1_q05b,
    check_r3_2024_dichotomy_s1_q06a,
    check_r3_2024_dichotomy_s1_q06b,
    check_r3_2024_dichotomy_s1_q07a,
    check_r3_2024_dichotomy_s1_q07b,
    check_r3_2024_dichotomy_s2_q01a,
    check_r3_2024_dichotomy_s2_q01b,
    check_r3_2024_dichotomy_s2_q02a,
    check_r3_2024_dichotomy_s2_q02b,
    check_r3_2024_dichotomy_s2_q03a,
    check_r3_2024_dichotomy_s2_q03b,
    check_r3_2024_dichotomy_s2_q04a,
    check_r3_2024_dichotomy_s2_q04b,
    check_r3_2024_dichotomy_s2_q05a,
    check_r3_2024_dichotomy_s2_q05b,
    check_r3_2024_dichotomy_s2_q06a,
    check_r3_2024_dichotomy_s2_q06b,
    check_r3_2024_dichotomy_s2_q07a,
    check_r3_2024_dichotomy_s2_q07b,
    check_r3_2024_dichotomy_s3_q01a,
    check_r3_2024_dichotomy_s3_q01b,
    check_r3_2024_dichotomy_s3_q02a,
    check_r3_2024_dichotomy_s3_q02b,
    check_r3_2024_dichotomy_s3_q03a,
    check_r3_2024_dichotomy_s3_q03b,
    check_r3_2024_dichotomy_s3_q04a,
    check_r3_2024_dichotomy_s3_q04b,
    check_r3_2024_dichotomy_s3_q05a,
    check_r3_2024_dichotomy_s3_q05b,
    check_r3_2024_dichotomy_s3_q06a,
    check_r3_2024_dichotomy_s3_q06b,
    check_r3_2024_dichotomy_s3_q07a,
    check_r3_2024_dichotomy_s3_q07b,
    check_r3_2024_tb1_q01,
    check_r3_2024_tb2_q01,
    check_r3_2024_tb3_q01,
    check_r3_2024_tb4_q01,
)
