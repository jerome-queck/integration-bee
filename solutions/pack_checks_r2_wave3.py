"""SymPy checks for the third 2026-10-26 wave of Round 2 pack notes.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

from pack_checks_r2_rem import (
    check_r2_2025_uk_group_q03,
    check_r2_2025_uk_relay_q11,
    check_r2_2025_uk_relay_q15,
    check_r2_2025_uk_relay_q17,
    check_r2_2025_uk_relay_q18,
)

R2_WAVE3_PACK_IDS = (
    "R2-2021-Group-Q01",
    "R2-2021-Group-Q07",
    "R2-2021-Group-Q08",
    "R2-2021-Relay-B02",
    "R2-2021-Relay-B03",
    "R2-2021-Relay-B04",
    "R2-2021-Relay-C01",
    "R2-2021-Relay-C02",
    "R2-2021-Relay-C03",
    "R2-2021-Relay-C04",
    "R2-2021-Relay-D01",
    "R2-2021-Relay-D02",
    "R2-2021-Relay-D03",
    "R2-2021-Relay-D04",
    "R2-2022-Group-Q09",
    "R2-2022-Group-Q10",
    "R2-2022-Relay-Q01",
    "R2-2022-Relay-Q10",
    "R2-2022-Relay-Q14",
    "R2-2022-Relay-Q15",
    "R2-2022-Relay-Q20",
    "R2-2023-Group-Q03",
    "R2-2023-Group-Q06",
    "R2-2023-Group-Q07",
    "R2-2023-Relay-Q07",
    "R2-2023-Relay-Q10",
    "R2-2025-SG-Group-Q04",
    "R2-2025-SG-Group-Q05",
    "R2-2025-SG-Group-Q06",
    "R2-2025-SG-Group-Q08",
    "R2-2025-SG-Group-Q09",
    "R2-2025-SG-Group-Q12",
    "R2-2025-SG-Relay-Q05",
    "R2-2025-SG-Relay-Q11",
    "R2-2025-SG-Relay-Q17",
    "R2-2025-SG-Relay-Q21",
    "R2-2025-SG-Relay-Q22",
    "R2-2025-SG-Relay-Q25",
    "R2-2025-SG-Relay-Q26",
    "R2-2025-SG-Relay-Q27",
    "R2-2025-SG-Relay-Q28",
    "R2-2025-SG-Relay-Q29",
    "R2-2025-SG-Relay-Q30",
    "R2-2025-UK-Group-Q04",
    "R2-2025-UK-Group-Q05",
    "R2-2025-UK-Group-Q07",
    "R2-2025-UK-Group-Q08",
    "R2-2025-UK-Group-Q09",
    "R2-2025-UK-Relay-Q10",
    "R2-2025-UK-Relay-Q13",
    "R2-2025-UK-Relay-Q16",
)


def _eq(left, right) -> None:
    if left == right:
        return
    diff = left - right
    if diff == 0 or sp.simplify(diff) == 0:
        return
    if sp.simplify(sp.expand(diff)) == 0:
        return
    if sp.trigsimp(diff) == 0:
        return
    rewritten = getattr(diff, "rewrite", None)
    if rewritten is not None and sp.simplify(rewritten(sp.exp)) == 0:
        return
    raise AssertionError(f"{left} != {right}")


def _atan_pair(u) -> None:
    total = sp.atan(sp.exp(u)) + sp.atan(sp.exp(-u))
    _eq(sp.diff(total, u), 0)
    _eq(total.subs(u, 0), sp.pi / 2)


def _period(a) -> None:
    """∫_0^{2π} dθ/(a−cos θ) = 2π/√(a²−1) for a>1, via tan(θ/2) on each half."""
    tt = sp.symbols("tt", positive=True)
    anti_minus = (2 / sp.sqrt(a**2 - 1)) * sp.atan(tt * sp.sqrt(a + 1) / sp.sqrt(a - 1))
    denom_minus = (a - 1) + (a + 1) * tt**2
    _eq(sp.together(sp.diff(anti_minus, tt)) * denom_minus, 2)
    _eq(anti_minus.subs(tt, 0), 0)
    _eq(sp.atan(sp.oo), sp.pi / 2)
    half = sp.pi / sp.sqrt(a**2 - 1)
    _eq((2 / sp.sqrt(a**2 - 1)) * (sp.pi / 2), half)
    anti_plus = (2 / sp.sqrt(a**2 - 1)) * sp.atan(tt * sp.sqrt(a - 1) / sp.sqrt(a + 1))
    denom_plus = (a + 1) + (a - 1) * tt**2
    _eq(sp.together(sp.diff(anti_plus, tt)) * denom_plus, 2)
    left_minus = (1 / (a - (1 - tt**2) / (1 + tt**2))) * 2 / (1 + tt**2)
    _eq(left_minus, 2 / denom_minus)
    left_plus = (1 / (a + (1 - tt**2) / (1 + tt**2))) * 2 / (1 + tt**2)
    _eq(left_plus, 2 / denom_plus)
    _eq(2 * half, 2 * sp.pi / sp.sqrt(a**2 - 1))


def check_r2_2021_group_q01() -> None:
    th = sp.symbols("th", real=True)
    _eq(sp.diff(th**2 * sp.tan(th), th), 2 * th * sp.tan(th) + th**2 * sp.sec(th) ** 2)
    _eq(sp.diff(th * sp.log(sp.cos(th)), th), sp.log(sp.cos(th)) - th * sp.tan(th))
    _eq((sp.pi / 4) ** 2, sp.pi**2 / 16)
    phi = sp.symbols("phi", positive=True)
    r = sp.symbols("r", positive=True)
    kernel = r * sp.sin(phi) / (1 - 2 * r * sp.cos(phi) + r**2)
    _eq(sp.limit(kernel, r, 1), sp.sin(phi) / (2 - 2 * sp.cos(phi)))
    _eq(sp.sin(phi) / (2 - 2 * sp.cos(phi)), sp.cot(phi / 2) / 2)
    m = sp.symbols("m", integer=True, nonnegative=True)
    _eq(((-1) ** (2 * m + 2)) * sp.sin((2 * m + 1) * sp.pi / 2), (-1) ** m)
    _eq(sp.Rational(1, 2) * sp.summation((-1) ** m / (2 * m + 1) ** 2, (m, 0, sp.oo)), sp.Catalan / 2)
    eye = sp.pi**2 / 16 - 2 * (sp.Catalan / 2 - sp.pi * sp.log(2) / 8)
    _eq(eye, sp.pi**2 / 16 + sp.pi * sp.log(2) / 4 - sp.Catalan)


def check_r2_2021_group_q07() -> None:
    u = sp.symbols("u", real=True)
    _atan_pair(u)
    x = sp.exp(u)
    integrand = sp.atan(x) / x ** (sp.log(x) + 1) * sp.diff(x, u)
    _eq(integrand, sp.atan(sp.exp(u)) * sp.exp(-(u**2)))
    f = sp.atan(sp.exp(u)) * sp.exp(-(u**2))
    pair = sp.atan(sp.exp(u)) + sp.atan(sp.exp(-u))
    _eq((f + f.subs(u, -u)) / 2, pair / 2 * sp.exp(-(u**2)))
    _eq(sp.integrate(sp.exp(-(u**2)), (u, -sp.oo, sp.oo)), sp.sqrt(sp.pi))
    _eq(sp.pi / 4 * sp.sqrt(sp.pi), sp.pi ** sp.Rational(3, 2) / 4)


def check_r2_2021_group_q08() -> None:
    u = sp.symbols("u", positive=True)
    quartic = (2 * u**2 + 4) / (u**4 + 2 * u**2 + 2)
    expr = -2 / (u**2 + 1) + quartic
    _eq(expr, 2 * u**2 / ((1 + u**2) * (u**4 + 2 * u**2 + 2)))
    total = sp.integrate(quartic, (u, 0, sp.oo)) - sp.pi
    printed = sp.pi * (sp.sqrt(2 + 2 * sp.sqrt(2)) / 2 - 1)
    if sp.sqrtdenest(sp.simplify(total - printed)) != 0:
        raise AssertionError(total)


def check_r2_2021_relay_b02() -> None:
    x = sp.symbols("x", positive=True)
    anti = x * sp.log(1 + 169 / x**2) + 26 * sp.atan(x / 13)
    _eq(sp.diff(anti, x), sp.log(1 + 169 / x**2))
    _eq(sp.limit(x * sp.log(1 + 169 / x**2), x, sp.oo), 0)
    _eq(sp.limit(x * sp.log(1 + 169 / x**2), x, 0), 0)
    _eq(26 * (sp.pi / 2), 13 * sp.pi)
    digits = mp.floor(13 * mp.pi)
    if digits != 40:
        raise AssertionError(digits)


def check_r2_2021_relay_b03() -> None:
    x = sp.symbols("x", real=True)
    b = sp.symbols("b", positive=True)
    _eq(sp.integrate(1 / (x**2 + 1), (x, 0, 1)), sp.pi / 4)
    _eq(sp.limit(sp.log(b), b, 0), -sp.oo)


def check_r2_2021_relay_b04() -> None:
    u = sp.symbols("u", positive=True)
    x = sp.pi * u
    left = sp.log(x) / (x**2 + sp.pi**2) * sp.pi
    right = (sp.log(sp.pi) + sp.log(u)) / (sp.pi * (u**2 + 1))
    _eq(left, right)
    v = sp.symbols("v", positive=True)
    flipped = sp.log(1 / v) / (1 + 1 / v**2) * (1 / v**2)
    _eq(flipped, -sp.log(v) / (1 + v**2))
    _eq(sp.integrate(1 / (1 + u**2), (u, 0, sp.oo)), sp.pi / 2)
    _eq((1 / sp.pi) * sp.log(sp.pi) * (sp.pi / 2), sp.log(sp.pi) / 2)


def check_r2_2021_relay_c01() -> None:
    x = sp.symbols("x", positive=True)
    num = sp.sin(sp.acot(x)) + sp.cos(sp.atan(x))
    _eq(num, 2 / sp.sqrt(1 + x**2))
    _eq(sp.diff(x / sp.sqrt(1 + x**2), x), 1 / (1 + x**2) ** sp.Rational(3, 2))
    _eq(2 * (1 / sp.sqrt(2)), sp.sqrt(2))
    y = sp.symbols("y", negative=True)
    _eq(sp.sin(sp.acot(y)) + sp.cos(sp.atan(y)), 0)
    _eq(sp.sqrt(2) ** 2 - 2, 0)


def check_r2_2021_relay_c02() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(x**3 * sp.exp(-x), (x, 0, 0)), 0)
    _eq(2 - 0, 2)


def check_r2_2021_relay_c03() -> None:
    v = sp.symbols("v", positive=True)
    x = v**2
    integrand = sp.log(sp.sqrt(x)) / (sp.sqrt(x) * (x + 1) ** 2) * sp.diff(x, v)
    _eq(integrand, 2 * sp.log(v) / (v**2 + 1) ** 2)
    a = sp.symbols("a", positive=True)
    u = sp.symbols("u", positive=True)
    pulled = sp.log(sp.sqrt(a) * u) / (a + a * u**2) * sp.sqrt(a)
    _eq(pulled, (sp.log(a) / 2 + sp.log(u)) / (sp.sqrt(a) * (1 + u**2)))
    flipped = sp.log(1 / u) / (1 + 1 / u**2) * (1 / u**2)
    _eq(flipped, -sp.log(u) / (1 + u**2))
    capital = sp.pi * sp.log(a) / (4 * sp.sqrt(a))
    _eq(sp.diff(capital, a).subs(a, 1), sp.pi / 4)
    _eq(2 * (-sp.pi / 4), -sp.pi / 2)
    if not (sp.pi > 2 and sp.pi < 4):
        raise AssertionError("pi bounds")


def check_r2_2021_relay_c04() -> None:
    u = sp.symbols("u", real=True)
    integrand = sp.cos(u) / (2 - sp.sin(2 * u))
    shifted = sp.simplify(integrand.subs(u, sp.pi / 4 - u))
    even = sp.simplify((shifted + shifted.subs(u, -u)) / 2)
    _eq(even, sp.cos(u) / (sp.sqrt(2) * (2 - sp.cos(2 * u))))
    _eq(2 - sp.cos(2 * u), 1 + 2 * sp.sin(u) ** 2)
    w = sp.symbols("w", positive=True)
    _eq(sp.diff(sp.atan(w * sp.sqrt(2)) / sp.sqrt(2), w), 1 / (1 + 2 * w**2))
    _eq(sp.sqrt(2) * (1 / sp.sqrt(2)), 1)
    _eq(sp.atan(1), sp.pi / 4)


def check_r2_2021_relay_d01() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    _eq(sp.limit(sp.Rational(5, 6) ** n, n, sp.oo), 0)
    _eq(sp.limit(sp.exp(-(sp.Rational(7, 6)) ** n), n, sp.oo), 0)
    x = sp.symbols("x")
    _eq(sp.integrate(1, (x, sp.Rational(5, 6), 1)), sp.Rational(1, 6))
    if sp.factorint(6) != {2: 1, 3: 1}:
        raise AssertionError(sp.factorint(6))


def check_r2_2021_relay_d02() -> None:
    x = sp.symbols("x", positive=True)
    s = sp.symbols("s", positive=True)
    a = sp.Integer(3)
    b = sp.Integer(2)
    _eq(sp.diff(x**s / sp.log(x), s), x**s)
    _eq((x**a - x**b) / sp.log(x), x**a / sp.log(x) - x**b / sp.log(x))
    _eq(sp.integrate(x**s, (x, 0, 1)), 1 / (s + 1))
    _eq(sp.integrate(1 / (s + 1), (s, b, a)), sp.log(sp.Rational(4, 3)))
    if not (sp.E > sp.Rational(5, 2) > sp.Rational(4, 3) > 1):
        raise AssertionError("log bounds")


def check_r2_2021_relay_d03() -> None:
    x = sp.symbols("x", positive=True)
    value = sp.integrate((1 - x) / (2 * x + 1), (x, 0, 1))
    _eq(value, sp.Rational(3, 4) * sp.log(3) - sp.Rational(1, 2))
    _eq(value, (sp.log(27) - 2) / 4)
    _eq((1 + sp.sqrt(1 + 4)) / 2, (1 + sp.sqrt(5)) / 2)
    # The alternate printed representation has the same integral but a
    # different pass-on. Minimal u selects k=1 from the full family.
    _eq(value, (sp.log(729) - 4) / 8)
    _eq((1 + sp.sqrt(1 + 8)) / 4, 1)
    k = sp.symbols("k", positive=True, integer=True)
    _eq(sp.expand_log((sp.log(27**k) - 2*k) / (4*k)), value)


def check_r2_2021_relay_d04() -> None:
    th = sp.symbols("th", real=True)
    phi = (1 + sp.sqrt(5)) / 2
    _eq(phi - sp.cos(th) ** 2, (sp.sqrt(5) - sp.cos(2 * th)) / 2)
    aa = sp.symbols("aa", positive=True)
    _period(aa)
    _eq(2 * sp.pi / sp.sqrt(5 - 1), sp.pi)
    g = 1 / (phi - sp.cos(th) ** 2)
    _eq(g.subs(th, 2 * sp.pi - th), g)
    _eq(sp.pi * (2 * sp.pi), 2 * sp.pi**2)


def check_r2_2022_group_q09() -> None:
    t = sp.symbols("t", positive=True)
    xx = sp.symbols("xx", positive=True)
    f = sp.log(1 - xx + xx**2) / ((1 + xx**2) * sp.log(xx))
    pulled = f.subs(xx, 1 / t) * (1 / t**2)
    _eq(pulled, -f.subs(xx, t) + 2 / (1 + t**2))
    _eq(sp.integrate(2 / (1 + t**2), (t, 0, sp.oo)), sp.pi)


def check_r2_2022_group_q10() -> None:
    x = sp.symbols("x", real=True)
    g = sp.atan(sp.exp(x)) / sp.cosh(x) * sp.tanh(x / 2) / x
    target = (sp.pi / 2) * sp.tanh(x / 2) / (x * sp.cosh(x))
    pref = sp.tanh(x / 2) / (x * sp.cosh(x))
    rest = sp.simplify((g + g.subs(x, -x) - target) / pref)
    _eq(rest, sp.atan(sp.exp(x)) + sp.atan(sp.exp(-x)) - sp.pi / 2)
    _atan_pair(x)
    _eq(sp.tanh(x / 2) / sp.cosh(x), sp.tanh(x) - sp.tanh(x / 2))
    a = sp.symbols("a", positive=True)
    _eq(sp.diff(sp.tanh(a * x), a), x / sp.cosh(a * x) ** 2)
    _eq(sp.integrate(1 / a, (a, sp.Rational(1, 2), 1)), sp.log(2))


def check_r2_2022_relay_q01() -> None:
    a, b = sp.symbols("a b", positive=True)
    left = sp.gamma(1 / b) * sp.gamma(1 + 1 / a) / (sp.gamma(1 + 1 / a + 1 / b) * b)
    right = sp.gamma(1 / a) * sp.gamma(1 / b) / (a * b * sp.gamma(1 + 1 / a + 1 / b))
    _eq(sp.gamma(1 + 1 / a), sp.gamma(1 / a) / a)
    _eq(left, right)


def check_r2_2022_relay_q10() -> None:
    a, t = sp.symbols("a t", positive=True)
    _eq(sp.integrate(sp.exp(-(a + 1) * t), (t, 0, sp.oo)), 1 / (a + 1))
    _eq(sp.diff(sp.log(1 + a), a), 1 / (a + 1))
    _eq(sp.log(1), 0)


def check_r2_2022_relay_q14() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    capital = sp.symbols("N", integer=True, positive=True)
    _eq(1 - 1 / n**2, (n - 1) * (n + 1) / n**2)
    _eq(sp.product(1 - 1 / n**2, (n, 2, capital)), (capital + 1) / (2 * capital))
    _eq(sp.limit(sp.log((capital + 1) / (2 * capital)), capital, sp.oo), -sp.log(2))


def check_r2_2022_relay_q15() -> None:
    n = sp.symbols("n", positive=True)
    v = sp.symbols("v", positive=True)
    piece = (n / 2) * v ** (sp.Rational(1, 2)) / (1 + v) * (1 / n) * v ** (1 / n - 1)
    _eq(piece, sp.Rational(1, 2) * v ** (sp.Rational(1, 2) + 1 / n - 1) / (1 + v))
    bb = sp.symbols("bb", positive=True)
    _eq(sp.gamma(bb) * sp.gamma(1 - bb) * sp.sin(sp.pi * bb) / sp.pi, 1)
    _eq(sp.sin(sp.pi * (sp.Rational(1, 2) + 1 / n)), sp.cos(sp.pi / n))


def check_r2_2022_relay_q20() -> None:
    A = sp.symbols("A", positive=True)
    u = sp.symbols("u", positive=True)
    _eq(sp.limit((A - A ** sp.Rational(1, 4)) / A, A, sp.oo), 1)
    _eq(sp.limit(A ** (-sp.Rational(1, 4)), A, sp.oo), 0)
    _eq(sp.limit(sp.exp(sp.log(A) / A ** sp.Rational(1, 4)), A, sp.oo), 1)
    _eq(sp.together(u / (1 + u) - u / 2), u * (1 - u) / (2 * (1 + u)))
    L = sp.log(A)
    anti = -2 / L * sp.exp(-L * u / 2)
    _eq(sp.diff(anti, u), sp.exp(-L * u / 2))
    _eq(anti.subs(u, 1) - anti.subs(u, 0), (2 / L) * (1 - sp.exp(-L / 2)))


def check_r2_2023_group_q03() -> None:
    x = sp.symbols("x")
    for size in range(2, 6):
        matrix = sp.eye(size)
        matrix[0, size - 1] = x
        matrix[size - 1, 0] = x
        _eq(matrix.det(), 1 - x**2)
    _eq(sp.integrate(1 - x**2, (x, 0, 1)), sp.Rational(2, 3))


def check_r2_2023_group_q06() -> None:
    c, t = sp.symbols("c t", positive=True)
    y = t**2
    integrand = sp.exp(-c * (y + 1 / y)) / sp.sqrt(y) * sp.diff(y, t)
    _eq(integrand, 2 * sp.exp(-c * (t**2 + 1 / t**2)))
    _eq(sp.exp(-c * (t**2 + 1 / t**2)), sp.exp(-2 * c) * sp.exp(-c * (t - 1 / t) ** 2))
    closed = sp.integrate(sp.exp(-c * t**2 - c / t**2), (t, 0, sp.oo))
    _eq(2 * closed, sp.sqrt(sp.pi / c) * sp.exp(-2 * c))


def check_r2_2023_group_q07() -> None:
    n = sp.symbols("n", positive=True)
    m = sp.symbols("m", integer=True)
    bit = sp.symbols("bit")
    _eq((2 * m + bit) / 2**n - m / 2 ** (n - 1), bit / 2**n)
    k = sp.symbols("k", integer=True, positive=True)
    _eq(sp.summation(2 ** (1 - 2 * k), (k, 1, sp.oo)), sp.Rational(2, 3))


def check_r2_2023_relay_q07() -> None:
    m = sp.symbols("m", real=True)
    _eq(2 * (m + 1) - 2 * m, 2)
    u = sp.symbols("u", real=True)
    _eq(2 * sp.integrate(sp.sqrt(1 - u**2), (u, 0, 1)), sp.pi / 2)


def check_r2_2023_relay_q10() -> None:
    r, x = sp.symbols("r x", positive=True)
    anti = sp.Rational(1, 2) * (x * sp.sqrt(r**2 - x**2) + r**2 * sp.asin(x / r))
    _eq(sp.diff(anti, x), sp.sqrt(r**2 - x**2))
    _eq(sp.asin(1 / sp.sqrt(2)), sp.pi / 4)
    inner = anti.subs(x, r / sp.sqrt(2))
    _eq(inner, r**2 / 4 + sp.pi * r**2 / 8)
    outer = sp.integrate(x, (x, r / sp.sqrt(2), r))
    _eq(2 * inner + 2 * outer, r**2 * (1 + sp.pi / 4))


def check_r2_2025_uk_group_q04() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    upper = 2 / k
    lower = 2 / (k + 1)
    _eq(sp.Rational(1, 2) * (upper**2 - lower**2), 2 * (1 / k**2 - 1 / (k + 1) ** 2))
    _eq((1 / k) / (1 - 1 / k), 1 / (k - 1))
    term = 2 * (1 / (k - 1)) * (1 / k**2 - 1 / (k + 1) ** 2)
    _eq(sp.summation(term, (k, 2, sp.oo)), 2 - sp.pi**2 / 6)


def check_r2_2025_uk_group_q05() -> None:
    x = sp.symbols("x", real=True)
    product = sp.atan(sp.sin(x)) * (sp.sin(x) - sp.cos(x))
    weight = sp.cos(x) / (1 + sp.sin(x) ** 2)
    integrand = (sp.sin(x) + sp.cos(x)) * sp.atan(sp.sin(x))
    _eq(sp.diff(product, x), integrand + (sp.sin(x) - sp.cos(x)) * weight)
    _eq(sp.atan(1) * 1, sp.pi / 4)
    t = sp.symbols("t", positive=True)
    _eq(sp.integrate(t / (1 + t**2), (t, 0, 1)), sp.log(2) / 2)
    _eq(sp.cos(x) ** 2 / (1 + sp.sin(x) ** 2), 2 / (1 + sp.sin(x) ** 2) - 1)
    pulled = 1 / (1 + t**2 / (1 + t**2)) * 1 / (1 + t**2)
    _eq(pulled, 1 / (1 + 2 * t**2))
    _eq(sp.integrate(1 / (1 + 2 * t**2), (t, 0, sp.oo)), sp.pi / (2 * sp.sqrt(2)))
    second = 2 * (sp.pi / (2 * sp.sqrt(2))) - sp.pi / 2
    eye = sp.pi / 4 - (sp.log(2) / 2 - second)
    _eq(eye, sp.pi / sp.sqrt(2) - sp.pi / 4 - sp.log(2) / 2)


def check_r2_2025_uk_group_q07() -> None:
    x = sp.symbols("x")
    t = sp.symbols("t", real=True)
    _eq(sp.expand((x - 1) ** 4 + 1), x**4 - 4 * x**3 + 6 * x**2 - 4 * x + 2)
    _eq(1 / (sp.E + sp.exp(t + 1)), sp.exp(-1) / (1 + sp.exp(t)))
    f = 1 / ((1 + sp.exp(t)) * (t**4 + 1))
    _eq(f + f.subs(t, -t), 1 / (t**4 + 1))
    _eq(sp.integrate(1 / (t**4 + 1), (t, -sp.oo, sp.oo)), sp.pi / sp.sqrt(2))
    _eq(sp.exp(-1) * sp.Rational(1, 2) * sp.pi / sp.sqrt(2), sp.pi / (2 * sp.E * sp.sqrt(2)))


def check_r2_2025_uk_group_q08() -> None:
    th = sp.symbols("th")
    s5 = sp.Rational(5, 8) * sp.sin(th) - sp.Rational(5, 16) * sp.sin(3 * th) + sp.Rational(1, 16) * sp.sin(5 * th)
    s3 = (3 * sp.sin(th) - sp.sin(3 * th)) / 4
    s4 = sp.Rational(3, 8) - sp.Rational(1, 2) * sp.cos(2 * th) + sp.Rational(1, 8) * sp.cos(4 * th)
    s6 = (10 - 15 * sp.cos(2 * th) + 6 * sp.cos(4 * th) - sp.cos(6 * th)) / 32
    _eq(sp.sin(th) ** 5, s5)
    _eq(sp.sin(th) ** 3, s3)
    _eq(sp.sin(th) ** 4, s4)
    _eq(sp.sin(th) ** 6, s6)
    _eq((15 * (1 - sp.cos(2 * th)) - 6 * (1 - sp.cos(4 * th)) + (1 - sp.cos(6 * th))) / 32, s6)
    _eq(sp.Rational(1, 2) * (1 - sp.cos(2 * th)) - sp.Rational(1, 8) * (1 - sp.cos(4 * th)), s4)
    k = sp.symbols("k", positive=True)
    axis = sp.symbols("axis", positive=True)
    _eq(sp.integrate(sp.sin(k * axis) / axis, (axis, 0, sp.oo)), sp.pi / 2)
    _eq(sp.diff(sp.pi * k / 2, k), sp.pi / 2)
    b = sp.symbols("b", positive=True)
    _eq(sp.diff(sp.pi * b**2 / 4, b), sp.pi * b / 2)
    sin6 = (15 * 2 - 6 * 4 + 6) * (sp.pi / 2) / 32
    sin4 = (sp.Rational(1, 2) * 2 - sp.Rational(1, 8) * 4) * (sp.pi / 2)
    sin5 = (sp.Rational(5, 8) - sp.Rational(5, 16) + sp.Rational(1, 16)) * (sp.pi / 2)
    sin3 = (sp.pi * 9 / 4 - 3 * (sp.pi / 4)) / 4
    _eq(sin6, 3 * sp.pi / 16)
    _eq(sin4, sp.pi / 4)
    _eq(sin5, 3 * sp.pi / 16)
    _eq(sin3, 3 * sp.pi / 8)
    _eq(sin6 + sin5 + sin4 + sin3, sp.pi)


def check_r2_2025_uk_group_q09() -> None:
    n, s = sp.symbols("n s", positive=True)
    beta = sp.gamma(n) * sp.gamma(s) / sp.gamma(n + s)
    _eq(beta.subs(s, 1), 1 / n)
    _eq(sp.diff(beta, s) / beta, sp.digamma(s) - sp.digamma(n + s))
    _eq(sp.digamma(1), -sp.EulerGamma)
    ni = sp.symbols("ni", integer=True, positive=True)
    _eq(sp.harmonic(ni).rewrite(sp.digamma), sp.digamma(ni + 1) + sp.EulerGamma)
    _eq(sp.expand_func(sp.harmonic(ni + 1)), sp.harmonic(ni) + 1 / (ni + 1))
    _eq(sp.summation((-1) ** ni / (ni + 1), (ni, 1, sp.oo)), sp.log(2) - 1)


def check_r2_2025_uk_relay_q10() -> None:
    w = sp.symbols("w", positive=True)
    x = sp.symbols("x", positive=True)
    _eq(sp.gamma(w + 1) / sp.gamma(w), w)
    _eq(x + sp.Rational(1, 2025) + 1, x + sp.Rational(2026, 2025))
    _eq(2025 * (x + sp.Rational(2026, 2025)), 2025 * x + 2026)
    _eq(2025 * (x + 1 + sp.Rational(1, 2025)), 2025 * x + 2026)


def check_r2_2025_uk_relay_q13() -> None:
    s = sp.symbols("s", positive=True)
    _eq(sp.exp(sp.log(s)) / s, 1)
    _eq(
        sp.exp(-(sp.sinh(sp.log(s)) ** 2)),
        sp.exp(sp.Rational(1, 2)) * sp.exp(-(s**2) / 4 - 1 / (4 * s**2)),
    )
    closed = sp.integrate(sp.exp(-(s**2) / 4 - 1 / (4 * s**2)), (s, 0, sp.oo))
    _eq(sp.exp(sp.Rational(1, 2)) * closed, sp.sqrt(sp.pi))


def check_r2_2025_uk_relay_q16() -> None:
    t = sp.symbols("t", positive=True)
    capital = sp.exp(sp.log(sp.exp(2 * t) + 1) / t)
    reflected = sp.exp(sp.log(sp.exp(-2 * t) + 1) / (-t))
    _eq(reflected, sp.E**2 / capital)
    kernel = 1 / (sp.E + capital)
    _eq(kernel + 1 / (sp.E + sp.E**2 / capital), 1 / sp.E)
    _eq((sp.sqrt(2) - 1) * (sp.sqrt(2) + 1), 1)
    _eq(sp.log(sp.sqrt(2) + 1) + sp.log(sp.sqrt(2) - 1), 0)


def check_r2_2025_sg_group_q04() -> None:
    check_r2_2025_uk_group_q03()


def check_r2_2025_sg_group_q05() -> None:
    check_r2_2025_uk_group_q04()


def check_r2_2025_sg_group_q06() -> None:
    check_r2_2025_uk_group_q05()


def check_r2_2025_sg_group_q08() -> None:
    check_r2_2025_uk_group_q07()


def check_r2_2025_sg_group_q09() -> None:
    check_r2_2025_uk_group_q08()


def check_r2_2025_sg_group_q12() -> None:
    check_r2_2025_uk_group_q09()


def check_r2_2025_sg_relay_q05() -> None:
    check_r2_2025_uk_relay_q17()


def check_r2_2025_sg_relay_q11() -> None:
    x = sp.symbols("x", real=True)
    a = x**3 + x**2 - 1
    b = 2 * x**3 + x**2 - 2
    expr = (sp.diff(a, x) / a + sp.diff(b, x) / b) * sp.sqrt(a * b)
    _eq(expr, 2 * sp.diff(sp.sqrt(a * b), x))
    _eq(a.subs(x, 0) * b.subs(x, 0), 2)
    _eq(a.subs(x, -1) * b.subs(x, -1), 3)
    _eq(sp.sqrt(a.subs(x, 0) * b.subs(x, 0)) - sp.sqrt(a.subs(x, -1) * b.subs(x, -1)), sp.sqrt(2) - sp.sqrt(3))
    _eq(a.subs(x, -sp.Rational(2, 3)), -sp.Rational(23, 27))
    _eq(b.subs(x, -sp.Rational(1, 3)), -sp.Rational(53, 27))


def check_r2_2025_sg_relay_q17() -> None:
    x = sp.symbols("x", positive=True)
    y = x ** (x**2 / 2) * sp.exp(-(x**2) / 4)
    _eq(sp.diff(sp.log(y), x), x * sp.log(x))
    _eq(sp.integrate(x * sp.log(x), x), x**2 * sp.log(x) / 2 - x**2 / 4)


def check_r2_2025_sg_relay_q21() -> None:
    check_r2_2025_uk_relay_q13()


def check_r2_2025_sg_relay_q22() -> None:
    check_r2_2025_uk_relay_q16()


def check_r2_2025_sg_relay_q25() -> None:
    check_r2_2025_uk_relay_q15()


def check_r2_2025_sg_relay_q26() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.sin(x) ** 2 * sp.cos(x) ** 2, (1 - sp.cos(4 * x)) / 8)
    _eq(1 / (1 + sp.sin(x) ** 2 * sp.cos(x) ** 2), 8 / (9 - sp.cos(4 * x)))
    aa = sp.symbols("aa", positive=True)
    _period(aa)
    _eq(sp.sqrt(80), 4 * sp.sqrt(5))
    _eq(2 * (2 * sp.pi / sp.sqrt(80)), sp.pi / sp.sqrt(5))


def check_r2_2025_sg_relay_q27() -> None:
    u = sp.symbols("u", real=True)
    _eq(sp.exp(u - u**2), sp.exp(sp.Rational(1, 4)) * sp.exp(-((u - sp.Rational(1, 2)) ** 2)))
    _eq(sp.integrate(sp.exp(-((u - sp.Rational(1, 2)) ** 2)), (u, -sp.oo, sp.oo)), sp.sqrt(sp.pi))
    _eq((2 / sp.sqrt(sp.pi)) * sp.exp(sp.Rational(1, 4)) * sp.sqrt(sp.pi), 2 * sp.exp(sp.Rational(1, 4)))


def check_r2_2025_sg_relay_q28() -> None:
    check_r2_2025_uk_relay_q18()


def check_r2_2025_sg_relay_q29() -> None:
    check_r2_2025_uk_relay_q10()


def check_r2_2025_sg_relay_q30() -> None:
    check_r2_2025_uk_relay_q11()


R2_WAVE3_CHECKS = (
    check_r2_2021_group_q01,
    check_r2_2021_group_q07,
    check_r2_2021_group_q08,
    check_r2_2021_relay_b02,
    check_r2_2021_relay_b03,
    check_r2_2021_relay_b04,
    check_r2_2021_relay_c01,
    check_r2_2021_relay_c02,
    check_r2_2021_relay_c03,
    check_r2_2021_relay_c04,
    check_r2_2021_relay_d01,
    check_r2_2021_relay_d02,
    check_r2_2021_relay_d03,
    check_r2_2021_relay_d04,
    check_r2_2022_group_q09,
    check_r2_2022_group_q10,
    check_r2_2022_relay_q01,
    check_r2_2022_relay_q10,
    check_r2_2022_relay_q14,
    check_r2_2022_relay_q15,
    check_r2_2022_relay_q20,
    check_r2_2023_group_q03,
    check_r2_2023_group_q06,
    check_r2_2023_group_q07,
    check_r2_2023_relay_q07,
    check_r2_2023_relay_q10,
    check_r2_2025_sg_group_q04,
    check_r2_2025_sg_group_q05,
    check_r2_2025_sg_group_q06,
    check_r2_2025_sg_group_q08,
    check_r2_2025_sg_group_q09,
    check_r2_2025_sg_group_q12,
    check_r2_2025_sg_relay_q05,
    check_r2_2025_sg_relay_q11,
    check_r2_2025_sg_relay_q17,
    check_r2_2025_sg_relay_q21,
    check_r2_2025_sg_relay_q22,
    check_r2_2025_sg_relay_q25,
    check_r2_2025_sg_relay_q26,
    check_r2_2025_sg_relay_q27,
    check_r2_2025_sg_relay_q28,
    check_r2_2025_sg_relay_q29,
    check_r2_2025_sg_relay_q30,
    check_r2_2025_uk_group_q04,
    check_r2_2025_uk_group_q05,
    check_r2_2025_uk_group_q07,
    check_r2_2025_uk_group_q08,
    check_r2_2025_uk_group_q09,
    check_r2_2025_uk_relay_q10,
    check_r2_2025_uk_relay_q13,
    check_r2_2025_uk_relay_q16,
)
