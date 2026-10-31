"""SymPy checks for the R1 pack notes added in the 2026-10-26 wave.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

WAVE_PACK_IDS = (
    "R1-2020-Q01",
    "R1-2020-Q02",
    "R1-2020-Q05",
    "R1-2020-Q07",
    "R1-2020-Q08",
    "R1-2020-Q26",
    "R1-2020-Q36",
    "R1-2020-Q37",
    "R1-2020-Q38",
    "R1-2021-Q04",
    "R1-2021-Q05",
    "R1-2021-Q19",
    "R1-2021-Q22",
    "R1-2021-Q24",
    "R1-2021-Q28",
    "R1-2021-Q29",
    "R1-2021-Q34",
    "R1-2022-Q01",
    "R1-2022-Q03",
    "R1-2022-Q06",
    "R1-2022-Q08",
    "R1-2022-Q12",
    "R1-2022-Q13",
    "R1-2022-Q14",
    "R1-2022-Q26",
    "R1-2022-Q29",
    "R1-2023-Q01",
    "R1-2023-Q02",
    "R1-2023-Q03",
    "R1-2023-Q06",
    "R1-2023-Q07",
    "R1-2023-Q10",
    "R1-2023-Q11",
    "R1-2023-Q12",
    "R1-2023-Q13",
    "R1-2023-Q15",
    "R1-2023-Q16",
    "R1-2023-Q18",
    "R1-2023-Q19",
    "R1-2023-Q22",
    "R1-2023-Q23",
    "R1-2023-Q24",
    "R1-2023-Q26",
    "R1-2023-Q27",
    "R1-2023-Q29",
    "R1-2024-Q02",
    "R1-2024-Q03",
    "R1-2024-Q05",
    "R1-2024-Q06",
    "R1-2024-Q08",
    "R1-2024-Q12",
    "R1-2024-Q14",
    "R1-2024-Q16",
    "R1-2024-Q18",
    "R1-2024-Q19",
    "R1-2024-Q23",
    "R1-2024-Q25",
    "R1-2025-Online-Q01",
    "R1-2025-Online-Q09",
    "R1-2025-Online-Q11",
    "R1-2025-Online-Q14",
    "R1-2025-Online-Q15",
    "R1-2025-Online-Q17",
)


def _eq(left, right) -> None:
    if sp.simplify(left - right) != 0:
        raise AssertionError(f"{left} != {right}")


def _near(got, target, tol) -> None:
    got_v, target_v = mp.mpf(got), mp.mpf(target)
    if not (mp.isfinite(got_v) and mp.isfinite(target_v)):
        raise AssertionError(f"non-finite comparison {got} vs {target}")
    err = abs(got_v - target_v)
    if err >= tol:
        raise AssertionError(f"{got} vs {target}, err {err}")


def check_r1_2020_q01() -> None:
    x = sp.symbols("x", real=True)
    f = sp.cos(x) / (1 + sp.exp(x))
    _eq(sp.simplify(f + f.subs(x, -x) - sp.cos(x)), 0)
    _eq(sp.integrate(sp.cos(x), (x, -sp.pi / 2, sp.pi / 2)), 2)


def check_r1_2020_q02() -> None:
    x = sp.symbols("x", positive=True)
    integrand = x**2 / (1 + x**2) ** 2
    split = 1 / (1 + x**2) - 1 / (1 + x**2) ** 2
    _eq(integrand, split)
    theta = sp.symbols("theta", real=True)
    _eq(sp.integrate(sp.sin(theta) ** 2, (theta, 0, sp.pi / 2)), sp.pi / 4)


def check_r1_2020_q05() -> None:
    x = sp.symbols("x", positive=True)
    t = sp.tan(x)
    root = sp.sqrt(2 * t)
    antideriv = (sp.sqrt(2) / 4) * (
        sp.log((t - root + 1) / (t + root + 1))
        + 2 * sp.atan(root - 1)
        + 2 * sp.atan(root + 1)
    )
    _eq(sp.diff(antideriv, x), sp.sqrt(t))


def check_r1_2020_q07() -> None:
    x = sp.symbols("x", positive=True)
    u = x ** sp.Rational(1, 6)
    antideriv = 6 * u - 6 * sp.atan(u)
    integrand = x ** sp.Rational(-1, 2) / (1 + x ** sp.Rational(1, 3))
    _eq(sp.diff(antideriv, x), integrand)


def check_r1_2020_q08() -> None:
    a = sp.symbols("a")
    deriv = -1 / (a + 1) ** 2
    _eq(sp.im(sp.simplify(deriv.subs(a, sp.I))), sp.Rational(1, 2))


def check_r1_2020_q26() -> None:
    x = sp.symbols("x", positive=True)
    antideriv = x * sp.cos(sp.log(x)) / 2 + x * sp.sin(sp.log(x)) / 2
    _eq(sp.diff(antideriv, x), sp.cos(sp.log(x)))


def check_r1_2020_q36() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.diff(sp.atan(x**2 / 2) / 4, x), x / (x**4 + 4))


def check_r1_2020_q37() -> None:
    x = sp.symbols("x", positive=True)
    s = sp.sqrt(x - 1)
    _eq(s + s**3, x * s)
    _eq(sp.diff(2 * sp.atan(s), x), 1 / (x * s))


def check_r1_2020_q38() -> None:
    x = sp.symbols("x", real=True)
    u = sp.sin(x) - sp.cos(x)
    _eq(sp.trigsimp(2 - sp.sin(2 * x) - (1 + u**2)), 0)
    s = sp.symbols("s", real=True)
    _eq(sp.integrate(1 / (1 + s**2), (s, -1, 1)), sp.pi / 2)


def check_r1_2021_q04() -> None:
    value = sp.log((1 + sp.I) / (1 - sp.I)) / (2 * sp.I)
    _eq(value, sp.pi / 4)


def check_r1_2021_q05() -> None:
    mp.mp.dps = 25
    log_sine = mp.quad(lambda t: mp.log(mp.sin(t)), [0, mp.pi / 2])
    _near(log_sine, -(mp.pi / 2) * mp.log(2), mp.mpf("1e-18"))
    closed = sp.pi * sp.log(4) + 4 * (-sp.pi / 2 * sp.log(2))
    _eq(closed, 0)


def check_r1_2021_q19() -> None:
    t = sp.symbols("t", real=True)
    n = sp.symbols("n", integer=True, positive=True)
    lhs = sp.exp(3 * sp.cos(t)) * sp.cos(3 * sp.sin(t))
    rhs = sp.re(sp.exp(3 * sp.exp(sp.I * t)))
    _eq(sp.expand_complex(lhs - rhs), 0)
    _eq(sp.integrate(1, (t, 0, 2 * sp.pi)), 2 * sp.pi)
    _eq(sp.integrate(sp.exp(sp.I * n * t), (t, 0, 2 * sp.pi)), 0)


def check_r1_2021_q22() -> None:
    theta = sp.symbols("theta", real=True)
    tan_shift = (1 - sp.tan(theta)) / (1 + sp.tan(theta))
    _eq(sp.simplify(sp.tan(sp.pi / 4 - theta) - tan_shift), 0)
    _eq(sp.simplify(1 + tan_shift - 2 / (1 + sp.tan(theta))), 0)
    _eq(sp.integrate(sp.log(2), (theta, 0, sp.pi / 4)) / 2, sp.pi * sp.log(2) / 8)


def check_r1_2021_q24() -> None:
    x = sp.symbols("x", real=True)
    antideriv = x - sp.sqrt(1 - x**2) * sp.asin(x)
    _eq(sp.diff(antideriv, x), x * sp.asin(x) / sp.sqrt(1 - x**2))


def check_r1_2021_q28() -> None:
    x = sp.symbols("x", positive=True)
    s = sp.sqrt(2)
    antideriv = sp.log(x ** (1 - s) + 1) / (1 - s)
    _eq(sp.diff(antideriv, x), 1 / (x + x**s))
    value = 0 - antideriv.subs(x, 1)
    _eq(sp.simplify(value), (1 + s) * sp.log(2))


def check_r1_2021_q29() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    term = n * (sp.exp(-n) - sp.exp(-(n + 1)))
    rewritten = n * sp.exp(-n) - (n + 1) * sp.exp(-(n + 1)) + sp.exp(-(n + 1))
    _eq(sp.expand(term - rewritten), 0)
    tail = sp.summation(sp.exp(-(n + 1)), (n, 1, sp.oo))
    _eq(sp.simplify(sp.exp(-1) + tail), 1 / (sp.E - 1))


def check_r1_2021_q34() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.diff(sp.tanh(x), x), 1 / sp.cosh(x) ** 2)
    _eq(sp.limit(sp.tanh(x), x, sp.oo) - sp.limit(sp.tanh(x), x, -sp.oo), 2)


def check_r1_2022_q01() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(1 / sp.sqrt(x - x**2), (x, 0, 1)), sp.pi)


def check_r1_2022_q03() -> None:
    x = sp.symbols("x", real=True)
    f = sp.cos(x + sp.cos(x))
    _eq(sp.trigsimp(f.subs(x, sp.pi - x) + f), 0)


def check_r1_2022_q06() -> None:
    x = sp.symbols("x", positive=True)
    pair = sp.atan(x) + sp.acot(x)
    _eq(sp.diff(pair, x), 0)
    _eq(pair.subs(x, 1), sp.pi / 2)
    _eq(sp.integrate((sp.pi / 2) / (x**2 + 1), (x, 0, 1)), sp.pi**2 / 8)


def check_r1_2022_q08() -> None:
    x = sp.symbols("x", real=True)
    cot_minus = sp.cot(x) - 1
    rewritten = (1 - sp.tan(x)) / sp.tan(x)
    _eq(sp.simplify(cot_minus - rewritten), 0)
    theta = sp.symbols("theta", real=True)
    tan_shift = (1 - sp.tan(theta)) / (1 + sp.tan(theta))
    _eq(sp.simplify(sp.tan(sp.pi / 4 - theta) - tan_shift), 0)
    _eq(sp.simplify(1 + tan_shift - 2 / (1 + sp.tan(theta))), 0)
    _eq(sp.integrate(sp.log(2), (theta, 0, sp.pi / 4)) / 2, sp.pi * sp.log(2) / 8)


def check_r1_2022_q12() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(sp.cos(x**2), (x, 0, sp.oo)), sp.sqrt(sp.pi / 8))
    _eq(sp.sqrt(sp.pi / 8), sp.sqrt(2) * sp.sqrt(sp.pi) / 4)


def check_r1_2022_q13() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    x = sp.symbols("x", positive=True)
    term = sp.integrate(sp.log(x) * x ** (2 * n), (x, 0, 1))
    _eq(term, -1 / (2 * n + 1) ** 2)
    _eq(2 * sp.summation(-1 / (2 * n + 1) ** 2, (n, 0, sp.oo)), -sp.pi**2 / 4)


def check_r1_2022_q14() -> None:
    _eq(sp.integrate(1, (sp.symbols("x"), 0, sp.pi / 2)), sp.pi / 2)
    x = sp.symbols("x", real=True)
    _eq(sp.trigsimp(sp.tan(x) * sp.cot(x) - 1), 0)


def check_r1_2022_q26() -> None:
    mp.mp.dps = 25
    product = mp.nprod(lambda n: (2 * n + 2) ** 2 / ((2 * n + 1) * (2 * n + 3)), [0, mp.inf])
    _near(product, mp.pi / 2, mp.mpf("1e-18"))
    _eq(sp.log(sp.pi / 2), sp.log(sp.pi) - sp.log(2))


def check_r1_2022_q29() -> None:
    theta = sp.symbols("theta", real=True)
    left = sp.cos(2 * theta) * (sp.sin(theta) + sp.cos(theta)) / (sp.cos(theta) - sp.sin(theta))
    _eq(sp.simplify(left - (1 + sp.sin(2 * theta))), 0)
    _eq(sp.limit(sp.cos(2 * theta) * sp.log(sp.cos(theta) - sp.sin(theta)), theta, 0), 0)
    _eq(
        sp.limit(sp.cos(2 * theta) * sp.log(sp.cos(theta) - sp.sin(theta)), theta, sp.pi / 4, dir="-"),
        0,
    )
    value = -sp.integrate((1 + sp.sin(2 * theta)) / 2, (theta, 0, sp.pi / 4))
    _eq(value, -(sp.pi + 2) / 8)


def check_r1_2023_q01() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(sp.sqrt(1 - x**2), (x, -1, 1)), sp.pi / 2)


def check_r1_2023_q02() -> None:
    x = sp.symbols("x", real=True)
    integrand = 1 / (1 - sp.sin(x)) + 1 / (1 + sp.sin(x))
    _eq(sp.trigsimp(integrand - 2 / sp.cos(x) ** 2), 0)
    _eq(sp.diff(2 * sp.tan(x), x), 2 / sp.cos(x) ** 2)


def check_r1_2023_q03() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    _eq(sp.summation(4 ** (-n), (n, 0, sp.oo)), sp.Rational(4, 3))


def check_r1_2023_q06() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(sp.exp(-(x**2) + 4 * x + 1) - sp.exp(-((x - 2) ** 2) + 5)), 0)
    _eq(sp.integrate(sp.exp(-((x - 2) ** 2)), (x, -sp.oo, sp.oo)) * sp.exp(5), sp.exp(5) * sp.sqrt(sp.pi))


def check_r1_2023_q07() -> None:
    x = sp.symbols("x", real=True)
    f = 1 / (3**x + 1)
    _eq(sp.simplify(f + f.subs(x, -x) - 1), 0)
    _eq(sp.integrate(1, (x, -1, 1)) / 2, 1)


def check_r1_2023_q10() -> None:
    a = sp.symbols("a", positive=True)
    u, t = sp.symbols("u t", real=True)
    _eq(sp.integrate(sp.exp(-u) * sp.cos(a * u), (u, 0, sp.oo)), 1 / (1 + a**2))
    _eq(sp.integrate(1 / (1 + t**2), (t, 0, a)), sp.atan(a))


def check_r1_2023_q11() -> None:
    left = sp.log(2 + sp.sqrt(3)) - sp.log(sp.sqrt(3))
    right = sp.log(1 + 2 * sp.sqrt(3) / 3)
    _eq(sp.exp(left - right), 1)


def check_r1_2023_q12() -> None:
    _eq(sp.Integer(1672 - 420) / 2, 626)


def check_r1_2023_q13() -> None:
    x = sp.symbols("x", real=True)
    integrand = 5 * (x**6 + x) ** 4
    antideriv = (x**5 + 1) ** 5 / 5
    _eq(sp.diff(antideriv, x), integrand)
    _eq(antideriv.subs(x, 0) - antideriv.subs(x, -1), sp.Rational(1, 5))


def check_r1_2023_q15() -> None:
    _eq(2 * (sp.pi / 2 - sp.pi / 3), sp.pi / 3)


def check_r1_2023_q16() -> None:
    x = sp.symbols("x", positive=True)
    antideriv = sp.log(x) - sp.log(x**22 + 1) / 22
    _eq(sp.diff(antideriv, x), 1 / (x**23 + x))


def check_r1_2023_q18() -> None:
    g, h = sp.symbols("g h", positive=True)
    c = g * h
    a = g**2 + c
    b = h**2 + c
    _eq((a + b) * c - a * b, 0)
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(sp.sin(sp.pi * x), (x, 0, 1)) / sp.pi / 2, 1 / sp.pi**2)


def check_r1_2023_q19() -> None:
    n = sp.symbols("n", positive=True)
    _eq(sp.gamma(n) * sp.gamma(1 - n) - sp.pi / sp.sin(sp.pi * n), 0)
    reflected = sp.pi / sp.sin(sp.pi / 4)
    _eq(sp.simplify(reflected / (8 * sp.sqrt(2)) - sp.pi / 8), 0)


def check_r1_2023_q22() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(x * sp.exp(-x / 2), (x, 0, sp.oo)), 4)
    _eq(sp.integrate(sp.sin(x) * sp.exp(-x / 2), (x, 0, sp.oo)), sp.Rational(4, 5))
    _eq(4 + sp.Rational(4, 5), sp.Rational(24, 5))


def check_r1_2023_q23() -> None:
    t = sp.symbols("t", positive=True)
    _eq(sp.integrate((1 - sp.cos(t)) / t**2, (t, 0, sp.oo)), sp.pi / 2)
    _eq(sp.Rational(1, 2) * (sp.Rational(4, 3) - sp.Rational(2, 3)) * sp.pi / 2, sp.pi / 6)


def check_r1_2023_q24() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(1 / (x**4 - x**2 + 1), (x, 0, sp.oo)), sp.pi / 2)


def check_r1_2023_q26() -> None:
    _eq(sp.Rational(3, 2) * sp.pi / sp.sin(sp.pi / 3), sp.sqrt(3) * sp.pi)
    x = sp.symbols("x", positive=True)
    _eq(sp.limit(sp.atan(x) / x ** sp.Rational(1, 3), x, sp.oo), 0)
    _eq(sp.limit(sp.atan(x) / x ** sp.Rational(1, 3), x, 0), 0)


def check_r1_2023_q27() -> None:
    x = sp.symbols("x", real=True)
    num = x**3 + x + 1
    reflected = num.subs(x, 1 - x)
    den = 3 * x**2 - 3 * x + 4
    _eq(sp.expand(num + reflected - den), 0)
    _eq(sp.integrate(1, (x, 0, 1)) / 2, sp.Rational(1, 2))


def check_r1_2023_q29() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    _eq(sp.summation((-1) ** (n - 1) / n**2, (n, 1, sp.oo)), sp.pi**2 / 12)
    _eq(sp.log(2) ** 2 / 4 + (sp.pi**2 / 12) / 4, sp.log(2) ** 2 / 4 + sp.pi**2 / 48)
    w = sp.symbols("w", positive=True)
    _eq(sp.integrate(sp.log(w) / w, (w, 1, 2)) / 2, sp.log(2) ** 2 / 4)


def check_r1_2024_q02() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.diff(x * sp.exp(x**2024), x), (2024 * x**2024 + 1) * sp.exp(x**2024))


def check_r1_2024_q03() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.diff(sp.atan(x**x), x), (sp.log(x) + 1) / (x**x + x ** (-x)))


def check_r1_2024_q05() -> None:
    x = sp.symbols("x", positive=True)
    pair = sp.atan(x) + sp.atan(1 / x)
    _eq(sp.diff(pair, x), 0)
    _eq(pair.subs(x, 1), sp.pi / 2)
    _eq(sp.integrate((sp.pi / 2) / x, (x, sp.Rational(1, 4), 4)) / 2, sp.pi * sp.log(2))


def check_r1_2024_q06() -> None:
    x = sp.symbols("x", real=True)
    f = sp.exp(-(x**2)) / (sp.exp(x) + 1)
    _eq(sp.simplify(f + f.subs(x, -x) - sp.exp(-(x**2))), 0)
    _eq(sp.integrate(sp.exp(-(x**2)), (x, -sp.oo, sp.oo)) / 2, sp.sqrt(sp.pi) / 2)


def check_r1_2024_q08() -> None:
    y = sp.symbols("y", real=True)
    _eq(sp.integrate(1 / (y**2 + 1), (y, -sp.oo, sp.oo)) / 2, sp.pi / 2)


def check_r1_2024_q12() -> None:
    u = sp.symbols("u", positive=True)
    _eq(sp.integrate(u / (u + 1) ** 4, (u, 0, sp.oo)), sp.Rational(1, 6))


def check_r1_2024_q14() -> None:
    k = sp.symbols("k", integer=True, nonnegative=True)
    n = sp.symbols("n", integer=True, positive=True)
    catalan = sp.summation((-1) ** k / (2 * k + 1) ** 2, (k, 0, sp.oo))
    _eq(catalan - sp.Catalan, 0)
    _eq(catalan / n, sp.Catalan / n)


def check_r1_2024_q16() -> None:
    t, p, q, x = sp.symbols("t p q x", positive=True)
    _eq(sp.integrate(sp.exp(-t * x**2), (x, 0, sp.oo)), sp.sqrt(sp.pi / t) / 2)
    _eq(sp.integrate(sp.sqrt(sp.pi / t) / 2, (t, p, q)), sp.sqrt(sp.pi) * (sp.sqrt(q) - sp.sqrt(p)))


def check_r1_2024_q18() -> None:
    mp.mp.dps = 25
    log_sine = mp.quad(lambda t: mp.log(mp.sin(t)), [0, mp.pi / 2])
    _near(log_sine, -(mp.pi / 2) * mp.log(2), mp.mpf("1e-18"))
    x = sp.symbols("x", real=True)
    _eq(sp.trigsimp(sp.log(sp.sin(x) * sp.cos(x)) - sp.log(sp.sin(2 * x) / 2)), 0)


def check_r1_2024_q19() -> None:
    x = sp.symbols("x", real=True)
    left = (1 + sp.tan(x)) / sp.sqrt(2)
    right = sp.cos(x - sp.pi / 4) / sp.cos(x)
    _eq(sp.simplify(left - right), 0)
    _eq(sp.integrate(sp.pi / 2, (x, 0, sp.pi / 4)) / 2, sp.pi**2 / 16)


def check_r1_2024_q23() -> None:
    a, x = sp.symbols("a x", positive=True)
    laplace = sp.integrate((sp.cos(3 * x) - sp.cos(x)) * sp.exp(-a * x), (x, 0, sp.oo))
    _eq(sp.simplify(laplace - (a / (a**2 + 9) - a / (a**2 + 1))), 0)
    antideriv = sp.log(a**2 + 9) / 2 - sp.log(a**2 + 1) / 2
    _eq(sp.diff(antideriv, a), a / (a**2 + 9) - a / (a**2 + 1))
    _eq(sp.limit(antideriv, a, sp.oo), 0)
    _eq(antideriv.subs(a, 0) / 2, sp.log(3) / 2)


def check_r1_2024_q25() -> None:
    mp.mp.dps = 25

    def integrand(t):
        if t == 0 or t == 1:
            return mp.mpf(0)
        return mp.log(mp.gamma(t)) * mp.sin(mp.pi * t)

    got = mp.quad(integrand, [0, 1])
    target = (mp.log(mp.pi) - mp.log(2) + 1) / mp.pi
    _near(got, target, mp.mpf("1e-12"))
    j = 2 * (sp.log(2) - 1) / sp.pi
    printed = (sp.log(sp.pi) - sp.log(2) + 1) / sp.pi
    _eq(2 * sp.log(sp.pi) / sp.pi - j, 2 * printed)


def check_r1_2025_online_q01() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(1 / (1 + x**2), (x, 0, sp.pi / 4)), sp.atan(sp.pi / 4))


def check_r1_2025_online_q09() -> None:
    x = sp.symbols("x", real=True)
    odd = (7 * x**7 - 5 * x**5 + 3 * x**3 - x) / sp.cos(x) ** 2
    _eq(sp.simplify(odd.subs(x, -x) + odd), 0)
    _eq(sp.integrate(sp.sec(x) ** 2, (x, -sp.pi / 4, sp.pi / 4)), 2)


def check_r1_2025_online_q11() -> None:
    x = sp.symbols("x", positive=True)
    antideriv = sp.log(sp.asin(sp.log(x)))
    integrand = 1 / (x * sp.asin(sp.log(x)) * sp.sqrt(1 - sp.log(x) ** 2))
    _eq(sp.diff(antideriv, x), integrand)


def check_r1_2025_online_q14() -> None:
    x = sp.symbols("x", real=True)
    f = sp.sin(sp.sin(x) + 2025 * x)
    reflected = sp.sin(sp.sin(2 * sp.pi - x) + 2025 * (2 * sp.pi - x))
    _eq(sp.trigsimp(sp.expand_trig(reflected + f)), 0)


def check_r1_2025_online_q15() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.trigsimp((sp.sin(x) + sp.cos(x)) ** 2 - (1 + sp.sin(2 * x))), 0)
    first = sp.integrate(sp.sin(x) + sp.cos(x), (x, 0, 3 * sp.pi / 4))
    second = sp.integrate(sp.sin(x) + sp.cos(x), (x, 3 * sp.pi / 4, sp.pi))
    _eq(first - second, 2 * sp.sqrt(2))


def check_r1_2025_online_q17() -> None:
    x = sp.symbols("x", positive=True)
    n = sp.symbols("n", real=True)
    antideriv = sp.log(x ** (1 - n) + n) / (1 - n)
    _eq(sp.simplify(sp.diff(antideriv, x) * (x + n * x**n) - 1), 0)
    # For n>1 the power x**(1-n) vanishes at infinity, so the value is the printed logarithm.
    printed = sp.log(n / (n + 1)) / (1 - n)
    at_inf = sp.log(n) / (1 - n)
    at_one = sp.log(n + 1) / (1 - n)
    _eq(sp.expand_log(sp.log(n / (n + 1)) - (sp.log(n) - sp.log(n + 1)), force=True), 0)
    _eq(sp.simplify(at_inf - at_one - (sp.log(n) - sp.log(n + 1)) / (1 - n)), 0)
    _eq(printed.subs(n, 2), sp.log(sp.Rational(2, 3)) / (1 - 2))


WAVE_CHECKS = (
    check_r1_2020_q01,
    check_r1_2020_q02,
    check_r1_2020_q05,
    check_r1_2020_q07,
    check_r1_2020_q08,
    check_r1_2020_q26,
    check_r1_2020_q36,
    check_r1_2020_q37,
    check_r1_2020_q38,
    check_r1_2021_q04,
    check_r1_2021_q05,
    check_r1_2021_q19,
    check_r1_2021_q22,
    check_r1_2021_q24,
    check_r1_2021_q28,
    check_r1_2021_q29,
    check_r1_2021_q34,
    check_r1_2022_q01,
    check_r1_2022_q03,
    check_r1_2022_q06,
    check_r1_2022_q08,
    check_r1_2022_q12,
    check_r1_2022_q13,
    check_r1_2022_q14,
    check_r1_2022_q26,
    check_r1_2022_q29,
    check_r1_2023_q01,
    check_r1_2023_q02,
    check_r1_2023_q03,
    check_r1_2023_q06,
    check_r1_2023_q07,
    check_r1_2023_q10,
    check_r1_2023_q11,
    check_r1_2023_q12,
    check_r1_2023_q13,
    check_r1_2023_q15,
    check_r1_2023_q16,
    check_r1_2023_q18,
    check_r1_2023_q19,
    check_r1_2023_q22,
    check_r1_2023_q23,
    check_r1_2023_q24,
    check_r1_2023_q26,
    check_r1_2023_q27,
    check_r1_2023_q29,
    check_r1_2024_q02,
    check_r1_2024_q03,
    check_r1_2024_q05,
    check_r1_2024_q06,
    check_r1_2024_q08,
    check_r1_2024_q12,
    check_r1_2024_q14,
    check_r1_2024_q16,
    check_r1_2024_q18,
    check_r1_2024_q19,
    check_r1_2024_q23,
    check_r1_2024_q25,
    check_r1_2025_online_q01,
    check_r1_2025_online_q09,
    check_r1_2025_online_q11,
    check_r1_2025_online_q14,
    check_r1_2025_online_q15,
    check_r1_2025_online_q17,
)
