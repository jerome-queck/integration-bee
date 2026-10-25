"""SymPy checks for the pack notes added after the first 35.

Imported by solutions/self_check.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

EXTRA_PACK_IDS = (
    "R1-2021-Q02",
    "R1-2021-Q03",
    "R1-2021-Q09",
    "R1-2021-Q12",
    "R1-2021-Q13",
    "R1-2021-Q16",
    "R1-2021-Q26",
    "R1-2021-Q30",
    "R1-2021-Q36",
    "R1-2022-Q07",
    "R1-2022-Q11",
    "R1-2022-Q16",
    "R1-2022-Q17",
    "R1-2022-Q20",
    "R1-2022-Q21",
    "R1-2022-Q23",
    "R1-2022-Q24",
    "R1-2022-Q25",
    "R1-2022-Q28",
    "R1-2022-Q30",
    "R1-2023-Q04",
    "R1-2023-Q05",
    "R1-2023-Q08",
    "R1-2023-Q09",
    "R1-2023-Q14",
    "R1-2023-Q17",
    "R1-2023-Q20",
    "R1-2023-Q21",
    "R1-2023-Q25",
    "R1-2023-Q28",
    "R1-2023-Q30",
    "R1-2024-Q04",
    "R1-2024-Q07",
    "R1-2024-Q09",
    "R1-2024-Q10",
    "R1-2024-Q11",
    "R1-2024-Q13",
    "R1-2024-Q15",
    "R1-2024-Q17",
    "R1-2024-Q20",
    "R1-2024-Q21",
    "R1-2024-Q22",
    "R1-2024-Q24",
    "R1-2024-Q26",
    "R1-2024-Q28",
    "R1-2024-Q30",
)


def _eq(left, right) -> None:
    if sp.simplify(left - right) != 0:
        raise AssertionError(f"{left} != {right}")


def _near(got, target, tol) -> None:
    err = abs(mp.mpf(got) - mp.mpf(target))
    if err >= tol:
        raise AssertionError(f"{got} vs {target}, err {err}")


def check_r1_2021_q02() -> None:
    t = sp.symbols("t", real=True)
    wallis = 4 * sp.integrate(sp.cos(t) ** 420, (t, 0, sp.pi / 2))
    target = sp.pi * sp.binomial(420, 210) / 2**419
    _eq(wallis, target)
    duplicated = (
        sp.Integer(2)
        * sp.Pow(2, 1 - 420)
        * sp.pi
        * sp.factorial(419)
        / (sp.factorial(210) * sp.factorial(209))
    )
    _eq(duplicated, target)


def check_r1_2021_q03() -> None:
    u = sp.symbols("u", positive=True)
    value = sp.integrate(2 * ((1 + u) ** (-4) - (1 + u) ** (-5)), (u, 0, sp.oo))
    _eq(value, sp.Rational(1, 6))


def check_r1_2021_q09() -> None:
    x = sp.symbols("x", positive=True)
    integrand = (x - 1) / ((x + 1) * sp.sqrt(x**3 + x**2 + x))
    arcsec = 2 * sp.asec(sp.sqrt(x) + 1 / sp.sqrt(x))
    arctan = 2 * sp.atan(sp.sqrt((x**2 + x + 1) / x))
    _eq(sp.diff(arcsec, x), integrand)
    _eq(sp.diff(arctan, x), integrand)
    _eq((arcsec - arctan).subs(x, 1), 0)


def check_r1_2021_q12() -> None:
    n = sp.symbols("n", positive=True)
    first = sp.sin((1 - n) * sp.pi / 2) * sp.gamma(1 - n)
    second = sp.cos(n * sp.pi / 2) * sp.gamma(1 - n)
    third = sp.pi / (sp.sin(n * sp.pi / 2) * 2 * sp.gamma(n))
    _eq(first - second, 0)
    _eq(sp.gamma(n) * sp.gamma(1 - n) - sp.pi / sp.sin(sp.pi * n), 0)
    _eq(2 * sp.sin(n * sp.pi / 2) * sp.cos(n * sp.pi / 2) - sp.sin(n * sp.pi), 0)
    cleared = sp.sin(n * sp.pi) * sp.gamma(n) * sp.gamma(1 - n) - sp.pi
    _eq(cleared.subs(sp.gamma(n) * sp.gamma(1 - n), sp.pi / sp.sin(sp.pi * n)), 0)
    raw = (
        2
        * sp.sin(n * sp.pi / 2)
        * sp.cos(n * sp.pi / 2)
        * sp.gamma(n)
        * sp.gamma(1 - n)
        - sp.pi
    )
    _eq(
        raw.subs(2 * sp.sin(n * sp.pi / 2) * sp.cos(n * sp.pi / 2), sp.sin(n * sp.pi))
        - cleared,
        0,
    )
    half = sp.Rational(1, 2)
    formula = sp.sin((1 - half) * sp.pi / 2) * sp.gamma(1 - half)
    got = sp.integrate(sp.sin(sp.symbols("x")) / sp.symbols("x") ** half, (sp.symbols("x"), 0, sp.oo))
    _eq(got, formula)


def check_r1_2021_q13() -> None:
    x = sp.symbols("x", real=True)
    u = sp.sin(x) - sp.cos(x)
    _eq(sp.trigsimp(1 - u**2 - sp.sin(2 * x)), 0)
    sec_int = sp.Rational(1, 4) * sp.sec(x / 2) ** 2 - sp.Rational(1, 4) * sp.sec(x / 2) ** 2 * sp.tan(x / 2) ** 2
    split = 1 / (1 + sp.cos(x)) - 1 / (1 + sp.cos(x)) ** 2
    _eq(sp.trigsimp(split - sp.cos(x) / (1 + sp.cos(x)) ** 2), 0)
    _eq(sp.simplify(sp.together(sp.expand_trig(split - sec_int))), 0)
    antideriv = sp.Rational(1, 2) * sp.tan(x / 2) - sp.Rational(1, 6) * sp.tan(x / 2) ** 3
    _eq(sp.trigsimp(sp.diff(antideriv, x) - sec_int), 0)
    _eq(antideriv.subs(x, sp.pi / 2) - antideriv.subs(x, 0), sp.Rational(1, 3))


def check_r1_2021_q16() -> None:
    mark = sp.Rational(1, 2) * (sp.pi - sp.log(sp.sinh(sp.pi) / sp.pi))
    previous = (
        sp.pi / 2
        - sp.log(2) / 2
        - sp.Rational(1, 2) * sp.log(sp.sinh(sp.pi) / (2 * sp.pi))
    )
    last = sp.pi / 2 - sp.Rational(1, 2) * sp.log(sp.sinh(sp.pi) / (2 * sp.pi))
    _eq(previous, mark)
    _eq(last - mark, sp.log(2) / 2)
    mp.mp.dps = 25

    def term(n):
        n = mp.mpf(n)
        return n * (
            2 * mp.log(n + 1)
            - mp.log(1 + (n + 1) ** 2)
            - 2 * mp.log(n)
            + mp.log(1 + n * n)
        )

    n_cut = 300
    partial = sum(term(n) for n in range(1, n_cut + 1))
    # n**2 * a(n) increases to 2, so a(n) < 2/n**2 and the tail is < 2/n_cut.
    if term(n_cut) * n_cut**2 >= 2:
        raise AssertionError("Q16 tail bound")
    got = mp.pi / 2 - partial / 2
    target = (mp.pi - mp.log(mp.sinh(mp.pi) / mp.pi)) / 2
    gap = got - target
    if gap <= 0 or gap >= mp.mpf(1) / n_cut:
        raise AssertionError(f"Q16 series gap {gap}")


def check_r1_2021_q26() -> None:
    x = sp.symbols("x", positive=True)
    integrand = (x - x * sp.log(x) + 1) / (x * (x + 1) ** 2 + x * sp.log(x) ** 2)
    antideriv = sp.atan(sp.log(x) / (1 + x))
    _eq(sp.diff(antideriv, x), integrand)
    value = antideriv.subs(x, sp.E) - antideriv.subs(x, 1)
    _eq(value.rewrite(sp.acot), sp.acot(1 + sp.E))


def check_r1_2021_q30() -> None:
    x = sp.symbols("x", positive=True)
    a = sp.integrate(x**2 / (1 + x**4), (x, 0, 1))
    b = sp.integrate(1 / (1 + x**4), (x, 0, 1))
    log_arg = 3 - 2 * sp.sqrt(2)
    printed_a = (sp.pi + sp.log(log_arg)) / (4 * sp.sqrt(2))
    printed_b = (sp.pi - sp.log(log_arg)) / (4 * sp.sqrt(2))
    _eq(a, printed_a)
    _eq(sp.exp(8 / sp.sqrt(2) * (b - printed_b)), 1)
    _eq(sp.pi**2 / 16 - 2 * printed_a * printed_b, sp.log(log_arg) ** 2 / 16)


def check_r1_2021_q36() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    catalan = sp.summation(((-1) ** (k - 1)) / (2 * k - 1) ** 2, (k, 1, sp.oo))
    odd = sp.summation(1 / (2 * k - 1) ** 3, (k, 1, sp.oo))
    _eq(catalan, sp.Catalan)
    _eq(odd.rewrite(sp.zeta), sp.Rational(7, 8) * sp.zeta(3))
    mp.mp.dps = 25

    def integrand(t):
        if t == 0:
            return mp.mpf(0)
        return mp.atan(t) ** 2 / t

    target = mp.pi * mp.catalan / 2 - mp.mpf(7) / 8 * mp.zeta(3)
    got = mp.quad(integrand, [0, 1])
    _near(got, target, mp.mpf("1e-18"))


def check_r1_2022_q07() -> None:
    x = sp.symbols("x", positive=True)
    product = 1
    n = 6
    for i in range(1, n + 1):
        product *= sp.cos(x / 2**i)
    _eq((2**n) * sp.sin(x / 2**n) * product, sp.sin(x))
    _eq(sp.integrate(sp.sin(x), (x, 0, sp.pi / 2)), 1)


def check_r1_2022_q11() -> None:
    x = sp.symbols("x")
    series = sp.series((1 - 4 * x) ** (sp.Rational(-1, 2)), x, 0, 8).removeO()
    for n in range(8):
        coeff = series.coeff(x, n)
        _eq(coeff, sp.binomial(2 * n, n))
    value = sp.integrate((1 - 4 * x) ** (sp.Rational(-1, 2)), (x, 0, sp.Rational(1, 4)))
    _eq(value, sp.Rational(1, 2))


def check_r1_2022_q16() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    partial = sp.log(n + 1) - (sp.harmonic(n + 1) - 1)
    _eq(sp.limit(partial, n, sp.oo), 1 - sp.EulerGamma)


def check_r1_2022_q17() -> None:
    t, c = sp.symbols("t c", positive=True)
    _eq(sp.integrate(sp.exp(-c * t) * sp.cos(t), (t, 0, sp.oo)), c / (c**2 + 1))
    mp.mp.dps = 25
    got = mp.quad(lambda u: mp.cos(u) / mp.cosh(u), [-mp.inf, mp.inf])
    _near(got, mp.pi / mp.cosh(mp.pi / 2), mp.mpf("1e-18"))


def check_r1_2022_q20() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    total = sp.summation(1 / n**2 - 1 / (3 * n**2), (n, 1, sp.oo))
    _eq(total, sp.pi**2 / 9)


def check_r1_2022_q21() -> None:
    u = sp.symbols("u", positive=True)
    value = sp.E * sp.integrate(sp.sqrt(u) * sp.exp(-u), (u, 0, sp.oo))
    _eq(value, sp.E * sp.sqrt(sp.pi) / 2)


def check_r1_2022_q23() -> None:
    x = sp.symbols("x")
    integral = sp.integrate(
        x ** (sp.Rational(3, 4) - 1) * (1 - x) ** (sp.Rational(5, 4) - 1),
        (x, 0, 1),
    )
    beta = sp.beta(sp.Rational(3, 4), sp.Rational(5, 4))
    _eq(integral, beta)
    _eq(sp.gamma(sp.Rational(5, 4)), sp.gamma(sp.Rational(1, 4)) / 4)
    _eq(
        sp.gamma(sp.Rational(1, 4)) * sp.gamma(sp.Rational(3, 4)),
        sp.pi / sp.sin(sp.pi / 4),
    )
    _eq(sp.pi / sp.sin(sp.pi / 4), sp.pi * sp.sqrt(2))
    _eq(sp.Rational(1, 4) * sp.pi * sp.sqrt(2), sp.pi / (2 * sp.sqrt(2)))


def check_r1_2022_q24() -> None:
    x = sp.symbols("x", real=True)
    for n in range(0, 4):
        for k in range(0, 4):
            piece = sp.integrate(sp.exp(sp.I * (n - k) * x), (x, 0, 2 * sp.pi))
            _eq(sp.simplify(piece), 2 * sp.pi if n == k else 0)
    mp.mp.dps = 20

    def integrand(n):
        def f(u):
            return mp.exp(mp.cos(u)) * mp.cos(n * u - mp.sin(u))

        return f

    _near(mp.quad(integrand(2), [0, 2 * mp.pi]), 2 * mp.pi / 2, mp.mpf("1e-12"))
    _near(mp.quad(integrand(-1), [0, 2 * mp.pi]), 0, mp.mpf("1e-12"))


def check_r1_2022_q25() -> None:
    t = sp.symbols("t", positive=True)
    _eq(sp.integrate(sp.log(t) * sp.exp(-t), (t, 0, sp.oo)), -sp.EulerGamma)
    mp.mp.dps = 25

    def integrand(u):
        return mp.log(u) * mp.sin(u) / u

    head = mp.quad(integrand, [mp.mpf("1e-30"), 1])
    tail = mp.quadosc(integrand, [1, mp.inf], omega=1)
    _near(head + tail, -mp.euler * mp.pi / 2, mp.mpf("1e-18"))


def check_r1_2022_q28() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    series = sp.summation(4 * ((-1) ** n) / (2 * n + 1) ** 2, (n, 0, sp.oo))
    _eq(series, 4 * sp.Catalan)
    mp.mp.dps = 25

    def integrand(theta):
        root = mp.sqrt(1 + mp.cos(theta))
        return mp.log((root + 1) / (root - 1))

    got = mp.quad(integrand, [0, mp.pi / 2])
    _near(got.real, 4 * mp.catalan, mp.mpf("1e-18"))


def check_r1_2022_q30() -> None:
    z = sp.symbols("z")
    a = sp.symbols("a", positive=True)
    den = z * (z**2 + a**2)
    upper = sp.residue(sp.log(1 - sp.I * z) ** 2 / den, z, sp.I * a)
    lower = sp.residue(sp.log(1 + sp.I * z) ** 2 / den, z, -sp.I * a)
    target_res = sp.log(1 + a) ** 2 / (-2 * a**2)
    _eq(upper, target_res)
    _eq(lower, target_res)
    first = 2 * sp.pi * sp.I * (sp.I / 4) * upper
    second = -2 * sp.pi * sp.I * (-sp.I / 4) * lower
    _eq(sp.simplify(first + second), sp.pi * sp.log(1 + a) ** 2 / (2 * a**2))
    mp.mp.dps = 25

    def integrand(u):
        return mp.atan(u) * mp.log(1 + u * u) / (u * (1 + u * u))

    got = mp.quad(integrand, [0, mp.inf])
    _near(got, mp.pi * mp.log(2) ** 2 / 2, mp.mpf("1e-18"))


def check_r1_2023_q04() -> None:
    x, capital = sp.symbols("x X")
    _eq(sp.diff(2 * x * capital, capital), 2 * x)


def check_r1_2023_q05() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(sp.cos(sp.pi * x), (x, 0, 1)), 0)


def check_r1_2023_q08() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    _eq(sp.summation(n / 2**n, (n, 1, sp.oo)), 2)
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(4**x, (x, 0, 1)), 3 / (2 * sp.log(2)))


def check_r1_2023_q09() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    _eq(sp.summation(((-1) ** n) / (n + 1), (n, 0, sp.oo)), sp.log(2))


def check_r1_2023_q14() -> None:
    x = sp.symbols("x", positive=True)
    base = sp.log(sp.log(x))
    exponent = base / sp.log(base)
    _eq(sp.simplify(sp.log(base) * exponent - base), 0)
    _eq(sp.simplify(sp.exp(base) - sp.log(x)), 0)
    _eq(sp.integrate(sp.log(x), (x, 0, 1)), -1)


def check_r1_2023_q17() -> None:
    u = sp.symbols("u", real=True)
    antideriv = sp.exp(u) * (sp.sin(u) - sp.cos(u))
    _eq(sp.diff(antideriv, u), 2 * sp.exp(u) * sp.sin(u))
    _eq(antideriv.subs(u, sp.pi / 2) - antideriv.subs(u, 0), sp.exp(sp.pi / 2) + 1)


def check_r1_2023_q20() -> None:
    x = sp.symbols("x", real=True)
    f = 4**x / (2 + 4**x)
    _eq(sp.simplify(f.subs(x, 1 - x) - (1 - f)), 0)
    _eq(sp.integrate(1, (x, sp.Rational(1, 4), sp.Rational(3, 4))), sp.Rational(1, 2))


def check_r1_2023_q21() -> None:
    x = sp.symbols("x", real=True)
    ratio = sp.Integer(2023) / 2024
    integrand = 2023**x / (2023**x + 2024**x)
    first = sp.log(1 + ratio**x) / sp.log(ratio)
    second = x - sp.log(1 + (1 / ratio) ** x) / sp.log(1 / ratio)
    _eq(sp.diff(first, x), integrand)
    _eq(sp.diff(second, x), integrand)
    _eq(sp.diff(first - second, x), 0)


def check_r1_2023_q25() -> None:
    _eq(sp.LambertW(sp.exp(1 + sp.E)), sp.E)
    _eq(sp.LambertW(sp.E), 1)
    v = sp.symbols("v", real=True)
    integrand = 1 + v + v * sp.exp(v) + v**2 * sp.exp(v)
    antideriv = (
        v
        + v**2 / 2
        + (v - 1) * sp.exp(v)
        + (v**2 - 2 * v + 2) * sp.exp(v)
    )
    _eq(sp.diff(antideriv, v), integrand)
    _eq(sp.simplify(antideriv.subs(v, 1) - antideriv.subs(v, 0)), sp.E + sp.Rational(1, 2))


def check_r1_2023_q28() -> None:
    a, b = sp.symbols("a b", positive=True)
    _eq(sp.expand((a - b) ** 3 - (a**3 - b**3) + 3 * a * b * (a - b)), 0)
    x = sp.symbols("x", positive=True)
    root = sp.sqrt(x**2 + 1)
    _eq(sp.simplify((root + x) * (root - x) - 1), 0)
    y = sp.symbols("y", real=True)
    _eq(sp.diff((y**3 + 3 * y) / 2, y), sp.Rational(3, 2) * (y**2 + 1))
    _eq(sp.Rational(2**3 + 3 * 2, 2), 7)
    _eq(sp.Rational(3, 2) * sp.integrate(y * (y**2 + 1), (y, 0, 2)), 9)


def check_r1_2023_q30() -> None:
    t = sp.symbols("t", positive=True)
    _eq(sp.apart(1 / (t * (t - 1)), t), 1 / (t - 1) - 1 / t)
    x = sp.symbols("x")
    _eq(sp.integrate(x ** (sp.Rational(-1, 2)) * (1 - x) ** (sp.Rational(-1, 2)), (x, 0, 1)), sp.pi)


def check_r1_2024_q04() -> None:
    s, inn, cos_sym = sp.symbols("s inn cos")
    antideriv = s**2 * inn**2 / 2 + cos_sym**3 / 3
    _eq(sp.diff(antideriv, s), s * inn**2)
    _eq(sp.diff(antideriv, cos_sym), cos_sym**2)


def check_r1_2024_q07() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    term = n * (1 / n**4 - 1 / (n + 1) ** 4)
    total = sp.summation(term, (n, 1, sp.oo))
    _eq(total.rewrite(sp.zeta), sp.zeta(4))
    _eq(sp.Rational(3, 4) * sp.zeta(4), sp.pi**4 / 120)


def check_r1_2024_q09() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.trigsimp(1 + sp.cos(x) - 2 * sp.cos(x / 2) ** 2), 0)
    value = 4 * sp.integrate(sp.Rational(1, 2) * sp.sec(x / 2) ** 2, (x, 0, sp.pi / 2))
    _eq(value, 4)


def check_r1_2024_q10() -> None:
    t = sp.symbols("t", real=True)
    _eq(sp.integrate(sp.exp(-(t**2)), (t, 0, sp.oo)), sp.sqrt(sp.pi) / 2)
    x = sp.symbols("x", real=True)
    closed = sp.sqrt(sp.pi) / 2 * sp.exp(-(x**2))
    _eq(sp.diff(closed, x), -2 * x * closed)
    mp.mp.dps = 25
    got = mp.quad(lambda u: mp.exp(-(u**2)) * mp.cos(2 * u), [0, mp.inf])
    _near(got, mp.sqrt(mp.pi) / 2 * mp.exp(-1), mp.mpf("1e-18"))


def check_r1_2024_q11() -> None:
    t = sp.symbols("t", real=True)
    _eq(sp.integrate(sp.sin(t) / t, (t, 0, sp.oo)), sp.pi / 2)
    _eq(sp.Rational(1, 2) * (sp.pi / 2) ** 2, sp.pi**2 / 8)


def check_r1_2024_q13() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(1 / (1 + x**2) + x**2 / (1 + x**2) - 1), 0)
    _eq(sp.integrate(sp.sin(x) / x, (x, 0, sp.oo)), sp.pi / 2)


def check_r1_2024_q15() -> None:
    z = sp.symbols("z", positive=True)
    left = sp.sin(sp.I * z) / (sp.sinh(sp.I * z) + sp.sin(sp.I * z))
    right = sp.sinh(z) / (sp.sinh(z) + sp.sin(z))
    _eq(left, right)
    _eq(sp.simplify(right + sp.sin(z) / (sp.sinh(z) + sp.sin(z))), 1)


def check_r1_2024_q17() -> None:
    y = sp.symbols("y", real=True)
    value = sp.integrate(y * (1 + 1 / (1 + y**2)), (y, 0, 1))
    _eq(sp.simplify(value), (1 + sp.log(2)) / 2)


def check_r1_2024_q20() -> None:
    n = sp.symbols("n", positive=True)
    t = sp.symbols("t", positive=True)
    power = (n + t) ** t
    integrand = (n + t) ** (t - 1) * ((n + t) * sp.log(n + t) + t)
    _eq(sp.diff(power, t), integrand)
    k = sp.symbols("k", integer=True)
    _eq(sp.summation(k, (k, 0, 99)), 4950)


def check_r1_2024_q21() -> None:
    # F_1 = F_2 = 1, and F_{k+1} = F_k + F_{k-1} is unbounded.
    a, b = 1, 1
    for _ in range(40):
        a, b = b, a + b
    if b < 10**6:
        raise AssertionError("Fibonacci bound")
    x = sp.symbols("x")
    _eq(sp.integrate(0, (x, 1, 2024)), 0)


def check_r1_2024_q22() -> None:
    u = sp.symbols("u", positive=True)
    pair = sp.atan(u) + sp.atan(1 / u)
    _eq(sp.diff(pair, u), 0)
    _eq(pair.subs(u, 1), sp.pi / 2)
    a, b = sp.symbols("a b", positive=True)
    _eq(sp.integrate(sp.pi / sp.symbols("x"), (sp.symbols("x"), a, b)), sp.pi * sp.log(b / a))


def check_r1_2024_q24() -> None:
    x = sp.symbols("x")
    product = 1
    for k in range(0, 6):
        product *= 1 + x ** (2**k)
    _eq(sp.expand((1 - x) * product - (1 - x ** (2**6))), 0)
    m = sp.symbols("m", integer=True, nonnegative=True)
    total = sp.summation(2 / (2 * m + 1) ** 2, (m, 0, sp.oo))
    _eq(total, sp.pi**2 / 4)


def check_r1_2024_q26() -> None:
    t = sp.symbols("t", positive=True)
    _eq(sp.diff(sp.asin(t) - sp.acos(sp.sqrt(1 - t**2)), t), 0)
    _eq((sp.asin(t) - sp.acos(sp.sqrt(1 - t**2))).subs(t, sp.Rational(1, 2)), 0)
    _eq(sp.integrate(sp.pi / 2, (t, 0, sp.Rational(1, 2))), sp.pi / 4)


def check_r1_2024_q28() -> None:
    u = sp.symbols("u", positive=True)
    product = sp.asin(u) * sp.asin(u**2)
    target = 2 * u * sp.asin(u) / sp.sqrt(1 - u**4) + sp.asin(u**2) / sp.sqrt(1 - u**2)
    _eq(sp.diff(product, u), target)
    _eq(product.subs(u, 1) - product.subs(u, 0), sp.pi**2 / 4)


def check_r1_2024_q30() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.trigsimp(sp.sin(x) + sp.cos(x) - sp.sqrt(2) * sp.cos(x - sp.pi / 4)), 0)
    t, u = sp.symbols("t u", positive=True)
    span = sp.sqrt(t**2 - 1)
    antideriv = sp.asin(u / span)
    left = sp.diff(antideriv, u)
    right = 1 / sp.sqrt(span**2 - u**2)
    _eq(1 / left**2, 1 / right**2)
    _eq(antideriv.subs(u, span) - antideriv.subs(u, 0), sp.pi / 2)
    _eq(sp.integrate(sp.pi / (2 * t), (t, 1, sp.sqrt(2))), sp.pi / 2 * sp.log(sp.sqrt(2)))
    _eq(2 * (sp.pi / 2 * sp.log(sp.sqrt(2))), sp.pi / 2 * sp.log(2))


EXTRA_CHECKS = (
    check_r1_2021_q02,
    check_r1_2021_q03,
    check_r1_2021_q09,
    check_r1_2021_q12,
    check_r1_2021_q13,
    check_r1_2021_q16,
    check_r1_2021_q26,
    check_r1_2021_q30,
    check_r1_2021_q36,
    check_r1_2022_q07,
    check_r1_2022_q11,
    check_r1_2022_q16,
    check_r1_2022_q17,
    check_r1_2022_q20,
    check_r1_2022_q21,
    check_r1_2022_q23,
    check_r1_2022_q24,
    check_r1_2022_q25,
    check_r1_2022_q28,
    check_r1_2022_q30,
    check_r1_2023_q04,
    check_r1_2023_q05,
    check_r1_2023_q08,
    check_r1_2023_q09,
    check_r1_2023_q14,
    check_r1_2023_q17,
    check_r1_2023_q20,
    check_r1_2023_q21,
    check_r1_2023_q25,
    check_r1_2023_q28,
    check_r1_2023_q30,
    check_r1_2024_q04,
    check_r1_2024_q07,
    check_r1_2024_q09,
    check_r1_2024_q10,
    check_r1_2024_q11,
    check_r1_2024_q13,
    check_r1_2024_q15,
    check_r1_2024_q17,
    check_r1_2024_q20,
    check_r1_2024_q21,
    check_r1_2024_q22,
    check_r1_2024_q24,
    check_r1_2024_q26,
    check_r1_2024_q28,
    check_r1_2024_q30,
)
