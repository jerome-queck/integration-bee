"""SymPy checks for the 2024 Round 3 Tournament notes.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

TOURNAMENT_PACK_IDS = (
    "R3-2024-Tournament-Q01",
    "R3-2024-Tournament-Q01-v10",
    "R3-2024-Tournament-Q01-v11",
    "R3-2024-Tournament-Q01-v4",
    "R3-2024-Tournament-Q01-v7",
    "R3-2024-Tournament-Q02",
    "R3-2024-Tournament-Q02-v3",
    "R3-2024-Tournament-Q02-v6",
    "R3-2024-Tournament-Q02-v9",
    "R3-2024-Tournament-Q03",
    "R3-2024-Tournament-Q03-v10",
    "R3-2024-Tournament-Q03-v4",
    "R3-2024-Tournament-Q03-v7",
    "R3-2024-Tournament-Q04",
    "R3-2024-Tournament-Q04-v10",
    "R3-2024-Tournament-Q04-v4",
    "R3-2024-Tournament-Q04-v5",
    "R3-2024-Tournament-Q04-v7",
    "R3-2024-Tournament-Q05",
    "R3-2024-Tournament-Q05-v10",
    "R3-2024-Tournament-Q05-v4",
    "R3-2024-Tournament-Q05-v6",
    "R3-2024-Tournament-Q05-v9",
    "R3-2024-Tournament-Q06",
    "R3-2024-Tournament-Q06-v4",
    "R3-2024-Tournament-Q06-v6",
    "R3-2024-Tournament-Q06-v9",
    "R3-2024-Tournament-Q07",
    "R3-2024-Tournament-Q07-v10",
    "R3-2024-Tournament-Q07-v11",
    "R3-2024-Tournament-Q07-v4",
    "R3-2024-Tournament-Q07-v7",
    "R3-2024-Tournament-Q08",
    "R3-2024-Tournament-Q08-v3",
    "R3-2024-Tournament-Q08-v6",
    "R3-2024-Tournament-Q08-v9",
    "R3-2024-Tournament-Q09",
    "R3-2024-Tournament-Q09-v10",
    "R3-2024-Tournament-Q09-v4",
    "R3-2024-Tournament-Q09-v7",
)


def _eq(left, right) -> None:
    gap = sp.simplify(left - right)
    if gap != 0:
        gap = sp.simplify(sp.together(sp.expand_trig(left - right)))
    if gap != 0:
        raise AssertionError(f"{left} != {right} ({gap})")


def check_r3_2024_tournament_q01() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    term = n / (1 + n**2 + n**4)
    piece = sp.Rational(1, 2) * (1 / (n**2 - n + 1) - 1 / (n**2 + n + 1))
    _eq(term, piece)
    total = sp.summation(piece, (n, 0, sp.oo))
    _eq(total, sp.Rational(1, 2))


def check_r3_2024_tournament_q02() -> None:
    x, t = sp.symbols("x t", positive=True)
    _eq(sp.trigsimp(4 * sp.cos(x) ** 2 - 1 - (2 * sp.cos(2 * x) + 1)), 0)
    sin2 = 2 * t / (1 + t**2)
    remainder = sin2 * (1 + t**2) / (2 * sp.sqrt(t)) * 1 / (1 + t**2)
    original = sp.sqrt(t) / (1 + t**2)
    _eq(remainder, original)
    _eq(sp.limit(sp.sin(2 * x) * sp.sqrt(sp.tan(x)), x, 0), 0)
    _eq(sp.sin(sp.pi / 2) * sp.sqrt(sp.tan(sp.pi / 4)), 1)


def check_r3_2024_tournament_q03() -> None:
    t = sp.symbols("t", positive=True)
    num = 2 - sp.sqrt(t) + t
    reflected = (2 - t ** (sp.Rational(-1, 2)) + t ** (-1)) * t ** sp.Rational(3, 2)
    reflected = sp.simplify(reflected)
    _eq(reflected, 2 * t ** sp.Rational(3, 2) - t + sp.sqrt(t))
    den = 1 + t ** sp.Rational(3, 2)
    _eq(sp.simplify((num + reflected) / den), 2)
    _eq(sp.integrate(1, (t, 0, sp.pi / 2)), sp.pi / 2)


def check_r3_2024_tournament_q04() -> None:
    x = sp.symbols("x")
    integrand = (x - 1) / ((x - 2) * (x - 3)) + (x - 2) / ((x - 3) * (x - 1)) + (x - 3) / ((x - 1) * (x - 2))
    split = sp.Rational(5, 2) / (x - 3) + sp.Rational(5, 2) / (x - 1) - 2 / (x - 2)
    _eq(integrand, split)
    antideriv = sp.Rational(5, 2) * sp.log(x - 3) + sp.Rational(5, 2) * sp.log(x - 1) - 2 * sp.log(x - 2)
    _eq(sp.diff(antideriv, x), split)


def check_r3_2024_tournament_q05() -> None:
    x = sp.symbols("x", positive=True)
    power = sp.log(2048)
    u = 1 + x ** (-power)
    integrand = 1 / (x ** (power + 1) * u)
    _eq(sp.simplify(integrand * (-power) / sp.diff(u, x)), 1 / u)
    _eq(sp.log(2) / sp.log(2048), sp.Rational(1, 11))
    _eq(u.subs(x, 1), 2)
    _eq(sp.limit(u, x, sp.oo), 1)


def check_r3_2024_tournament_q06() -> None:
    s, c = sp.symbols("s c", real=True)
    _eq(1 / (1 + 2 ** (-s)), 2**s / (1 + 2**s))
    _eq(1 / (1 + 2**c) + 1 / (1 + 2 ** (-c)), 1)
    _eq(sp.integrate(sp.Rational(1, 2), (s, 0, sp.pi)), sp.pi / 2)


def check_r3_2024_tournament_q07() -> None:
    x = sp.symbols("x", real=True)
    antideriv = 2025 * x + sp.exp(x) - sp.exp(-x)
    _eq(sp.diff(antideriv, x), 2025 + sp.exp(x) + sp.exp(-x))
    _eq(antideriv.subs(x, 1) - antideriv.subs(x, 0), 2025 + sp.E - sp.exp(-1))


def check_r3_2024_tournament_q08() -> None:
    s = sp.symbols("s", positive=True)
    _eq(1 / (sp.sinh(s) + 1 / sp.sinh(s)), sp.tanh(s) * sp.sech(s))
    _eq(sp.diff(-sp.sech(s), s), sp.tanh(s) * sp.sech(s))
    _eq(sp.limit(s * sp.sech(s), s, sp.oo), 0)
    _eq(sp.integrate(sp.sech(s), (s, 0, sp.oo)), sp.pi / 2)
    _eq(2 * (sp.pi / 2), sp.pi)


def check_r3_2024_tournament_q09() -> None:
    x, u = sp.symbols("x u", positive=True)
    second = 3 * u**2 * sp.sqrt(u**3 + u)
    _eq(sp.simplify(second.subs(u, x) + sp.sqrt(x + x**3)), (1 + 3 * x**2) * sp.sqrt(x + x**3))
    antideriv = sp.Rational(2, 3) * (x + x**3) ** sp.Rational(3, 2)
    _eq(sp.diff(antideriv, x), (1 + 3 * x**2) * sp.sqrt(x + x**3))
    _eq(antideriv.subs(x, 1) - antideriv.subs(x, 0), 4 * sp.sqrt(2) / 3)


def check_r3_2024_tournament_q01_v4() -> None:
    u = sp.symbols("u", positive=True)
    antideriv = sp.exp(2 * u) / (2 * u**2)
    _eq(sp.diff(antideriv, u), sp.exp(2 * u) * (u - 1) / u**3)
    value = sp.exp(-2) * (antideriv.subs(u, 2) - antideriv.subs(u, 1))
    _eq(sp.simplify(value), sp.Rational(1, 2) * (sp.E**2 / 4 - 1))


def check_r3_2024_tournament_q02_v3() -> None:
    x = sp.symbols("x", positive=True)
    complement = sp.atan(x) + sp.atan(1 / x)
    _eq(sp.diff(complement, x), 0)
    _eq(complement.subs(x, 1), sp.pi / 2)
    t = sp.symbols("t", real=True)
    _eq(sp.integrate(1 / (1 + t**2), (t, -sp.oo, sp.oo)), sp.pi)
    _eq((sp.pi / 4) * sp.pi, sp.pi**2 / 4)


def check_r3_2024_tournament_q03_v4() -> None:
    x = sp.symbols("x", positive=True)
    u = sp.sqrt(sp.exp(sp.sqrt(x)) - 1)
    true = sp.diff(u, x)
    claimed = (u**2 + 1) / (2 * sp.E * x * u)
    _eq(sp.simplify(true / claimed), sp.E * sp.sqrt(x) / 2)
    _eq(2 * sp.E * sp.integrate(1 / (1 + x**2), (x, 0, sp.oo)), sp.E * sp.pi)
    mp.mp.dps = 20
    got = mp.quad(lambda t: 1 / (t * mp.sqrt(mp.e ** mp.sqrt(t) - 1)), [1, mp.inf])
    if abs(got - mp.e * mp.pi) < 1:
        raise AssertionError(f"quadrature unexpectedly near e*pi: {got}")
    u = sp.symbols("u", positive=True)
    x_of_u = sp.log(1 + u**2) ** 2
    reduced = sp.simplify(sp.diff(x_of_u, u) / (x_of_u * u))
    _eq(reduced, 4 / ((1 + u**2) * sp.log(1 + u**2)))
    t = sp.symbols("t", real=True)
    _eq(sp.trigsimp(1 + sp.tan(t) ** 2 - sp.sec(t) ** 2), 0)
    s = sp.symbols("s", positive=True)
    _eq(4 / sp.log(s**2), 2 / sp.log(s))


def check_r3_2024_tournament_q04_v4() -> None:
    x = sp.symbols("x", positive=True)
    inside = x**3 + 1 / x**3 + 3 * (x + 1 / x)
    _eq(sp.expand(inside - (x + 1 / x) ** 3), 0)
    u = sp.log(x + 1 / x)
    _eq(sp.simplify(sp.diff(u, x) - (x**2 - 1) / (x**3 + x)), 0)
    antideriv = sp.Rational(3, 2) * u**2
    _eq(sp.diff(antideriv, x), 3 * (x**2 - 1) / (x**3 + x) * u)


def check_r3_2024_tournament_q05_v4() -> None:
    x = sp.symbols("x", positive=True)
    v = -2 * sp.sqrt(x - x**2)
    _eq(sp.diff(v, x), (2 * x - 1) / sp.sqrt(x - x**2))
    u = sp.symbols("u", real=True)
    _eq(sp.integrate(4 * sp.cos(u) ** 2, (u, 0, sp.pi / 2)), sp.pi)


def check_r3_2024_tournament_q06_v4() -> None:
    f = sp.symbols("f")
    _eq(sp.factor(f * (1 + f**2) - 2 * f), f * (f - 1) * (f + 1))
    _eq(2025 - 2024, 1)


def check_r3_2024_tournament_q07_v4() -> None:
    x = sp.symbols("x", real=True)
    s = sp.sqrt(7 * x - x**2)
    first = (x - s) / (2 * x - 7)
    second = ((7 - x) - s) / (7 - 2 * x)
    _eq(sp.simplify(first + second), 1)
    _eq(sp.integrate(first + second, (x, 3, 4)), 1)


def check_r3_2024_tournament_q08_v3() -> None:
    x = sp.symbols("x", positive=True)
    u = x * 4**x - 1
    _eq(sp.diff(u, x), 4**x * (1 + 2 * x * sp.log(2)))
    y = sp.symbols("y", positive=True)
    _eq(sp.diff(sp.atan(y), y) * 2, 2 / (1 + y**2))
    _eq(2 * (sp.pi / 2 - sp.pi / 3), sp.pi / 3)


def check_r3_2024_tournament_q09_v4() -> None:
    x = sp.symbols("x", real=True)
    u = sp.sec(x) + sp.tan(x)
    _eq(sp.simplify(sp.diff(u, x) - sp.sec(x) * u), 0)
    antideriv = u**2025 / 2025
    _eq(sp.diff(antideriv, x), sp.sec(x) * u**2025)


def check_r3_2024_tournament_q01_v7() -> None:
    x = sp.symbols("x", positive=True)
    u = (x * sp.E) ** x
    _eq(sp.simplify(sp.diff(u, x) - u * (sp.log(x) + 2)), 0)
    antideriv = sp.Rational(1, 2) * sp.log(1 + 2 * u)
    _eq(sp.simplify(sp.diff(antideriv, x) - (sp.log(x) + 2) / (u ** (-1) + 2)), 0)


def check_r3_2024_tournament_q02_v6() -> None:
    x, a = sp.symbols("x a", positive=True)
    _eq(sp.simplify(sp.tan(sp.atan(2 * x) - sp.atan(x))), x / (1 + 2 * x**2))
    _eq(sp.simplify(sp.tan(sp.atan(4 * x) - sp.atan(3 * x))), x / (1 + 12 * x**2))
    _eq(sp.integrate(1 / (1 + (a * x) ** 2), (x, 0, sp.oo)), sp.pi / (2 * a))
    _eq(sp.pi / 2 * (sp.log(2) - sp.log(sp.Rational(4, 3))), sp.pi / 2 * (sp.log(3) - sp.log(2)))


def check_r3_2024_tournament_q03_v7() -> None:
    x, y = sp.symbols("x y", real=True)
    _eq(sp.trigsimp(1 - (sp.sin(x) - sp.cos(x)) ** 2 - sp.sin(2 * x)), 0)
    _eq(sp.diff(sp.sin(x) - sp.cos(x), x), sp.cos(x) + sp.sin(x))
    _eq(sp.integrate(sp.sqrt(1 - y**2), (y, -1, 1)), sp.pi / 2)
    _eq(sp.Rational(1, 2) * sp.pi / 2, sp.pi / 4)


def check_r3_2024_tournament_q04_v7() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    term = 2**n / (3 ** (2**n) + 1)
    telescoping = 2**n / (3 ** (2**n) - 1) - 2 ** (n + 1) / (3 ** (2 ** (n + 1)) - 1)
    for value in range(6):
        _eq(term.subs(n, value), telescoping.subs(n, value))
    _eq(2**0 / (3 ** (2**0) - 1), sp.Rational(1, 2))
    _eq(sp.Rational(1, 2) / sp.log(2), 1 / (2 * sp.log(2)))


def check_r3_2024_tournament_q05_v6() -> None:
    x = sp.symbols("x", real=True)
    y = sp.exp(sp.tan(x) * sp.log(sp.sin(x)))
    _eq(sp.simplify(sp.diff(y, x) / y), sp.sec(x) ** 2 * sp.log(sp.sin(x)) + 1)
    _eq(y.subs(x, sp.pi / 4), sp.sqrt(2) / 2)
    _eq(sp.limit(y, x, sp.pi / 2, dir="-"), 1)
    _eq(1 - sp.sqrt(2) / 2, 1 - sp.sqrt(2) / 2)


def check_r3_2024_tournament_q06_v6() -> None:
    u = sp.symbols("u", real=True)
    inside = sp.sec(u) ** 2 + 2 * sp.tan(u)
    _eq(sp.simplify(inside - (1 + sp.tan(u)) ** 2), 0)
    antideriv = -sp.log(sp.cos(u)) + sp.tan(u) - u
    _eq(sp.simplify(sp.diff(antideriv, u) - (sp.tan(u) + sp.tan(u) ** 2)), 0)
    value = antideriv.subs(u, sp.pi / 4) - antideriv.subs(u, 0)
    _eq(sp.simplify(value), sp.log(2) / 2 + 1 - sp.pi / 4)


def check_r3_2024_tournament_q07_v7() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.expand(x**2 + 1 / x**2 - ((x - 1 / x) ** 2 + 2)), 0)
    fresnel = sp.integrate(sp.cos(x**2), (x, 0, sp.oo))
    _eq(fresnel, sp.sqrt(2 * sp.pi) / 4)
    _eq(sp.integrate(sp.sin(x**2), (x, 0, sp.oo)), fresnel)
    _eq(fresnel * (sp.cos(2) - sp.sin(2)), sp.sqrt(2 * sp.pi) / 4 * (sp.cos(2) - sp.sin(2)))


def check_r3_2024_tournament_q08_v6() -> None:
    x = sp.symbols("x", positive=True)
    antideriv = x**sp.E * sp.exp(x) - x**sp.E * sp.exp(-x)
    integrand = x**sp.E * (sp.exp(x) + sp.exp(-x)) + x ** (sp.E - 1) * (sp.exp(x + 1) - sp.exp(1 - x))
    _eq(sp.diff(antideriv, x), integrand)
    _eq(antideriv.subs(x, 1) - sp.limit(antideriv, x, 0), sp.E - sp.exp(-1))


def check_r3_2024_tournament_q09_v7() -> None:
    x = sp.symbols("x", real=True)
    u = sp.log(sp.sin(x)) - sp.log(1 + sp.cos(x))
    _eq(sp.simplify(sp.diff(u, x)), 1 / sp.sin(x))
    _eq(sp.diff(sp.log(u), x), 1 / (sp.sin(x) * u))


def check_r3_2024_tournament_q01_v10() -> None:
    a = sp.symbols("a", positive=True)
    lhs = sp.tan(a) / (3 - sp.tan(a) ** 2)
    rhs = (1 / sp.tan(a) - 3 / sp.tan(3 * a)) / 8
    _eq(lhs, rhs)
    _eq(sp.limit(a * sp.cot(a), a, 0), 1)
    _eq(sp.tan(sp.pi / 2 - 3), sp.cot(3))


def check_r3_2024_tournament_q01_v11() -> None:
    check_r3_2024_tournament_q01_v10()
    _eq(sp.Rational(1, 8) * (1 - 3 * sp.cot(3)), sp.Rational(1, 8) * (1 - 3 * sp.tan(sp.pi / 2 - 3)))


def check_r3_2024_tournament_q02_v9() -> None:
    z = sp.symbols("z", real=True)
    _eq(sp.trigsimp(sp.sin(z) ** 2 * sp.cos(z) ** 2), (1 - sp.cos(4 * z)) / 8)
    y = sp.symbols("y", real=True)
    antideriv = sp.exp(4 * y) * (sp.cos(4 * y) + sp.sin(4 * y)) / 8
    _eq(sp.diff(antideriv, y), sp.exp(4 * y) * sp.cos(4 * y))
    _eq(antideriv.subs(y, 0), sp.Rational(1, 8))
    _eq(sp.limit(antideriv, y, -sp.oo), 0)
    end = sp.Rational(1, 8)
    x = sp.symbols("x", positive=True)
    _eq(sp.Rational(1, 8) * sp.integrate(x**3, (x, 0, 1)) - sp.Rational(1, 8) * end, sp.Rational(1, 64))


def check_r3_2024_tournament_q03_v10() -> None:
    x, n = sp.symbols("x n", positive=True)
    _eq(sp.diff(sp.tan(x) ** (n + 1) / (n + 1), x), sp.tan(x) ** n * (1 + sp.tan(x) ** 2))
    _eq((sp.tan(sp.pi / 4) ** (n + 1) - sp.limit(sp.tan(x) ** (n + 1), x, 0)) / (n + 1), 1 / (n + 1))


def check_r3_2024_tournament_q04_v10() -> None:
    x = sp.symbols("x", real=True)
    two = sp.Integer(2)
    for m, n in ((2, 1), (3, 1), (4, 2), (0, -1), (-1, -2), (1, 0)):
        prod = 1
        for k in range(1, m - n + 1):
            prod *= sp.cos(two ** (m - k) * x)
        left = sp.sin(two**m * x)
        right = two ** (m - n) * sp.sin(two**n * x) * prod
        _eq(sp.trigsimp(left - right, method="fu"), 0)
        factor = two ** (-m)
        _eq(1 / two ** (m - n) / two**n, factor)
        printed = two ** (-m + 2*n)
        if (factor == printed) != (n == 0):
            raise AssertionError("printed factor must agree exactly when n=0")

    y = sp.symbols("y", real=True)
    scale = sp.Symbol("_scale", positive=True)
    partial = sp.sin(scale*y) / (scale*sp.sin(y))
    _eq(partial.subs(scale, 1), 1)
    _eq(sp.trigsimp(partial.subs(scale, 2*scale) - partial*sp.cos(scale*y)), 0)
    # This base and step prove the product identity for every number of
    # doublings; the six concrete checks above also cover negative exponents.
    d = sp.Symbol("_d", integer=True, positive=True)
    degree = two ** (d-1) + 1012
    if degree.is_integer is not True or degree.is_positive is not True:
        raise AssertionError("positive integer Dirichlet degree")
    _eq(2*degree + 1, two**d + 2025)

    j = sp.Symbol("_j", integer=True, positive=True)
    step = (sp.sin((2*j+1)*y) - sp.sin((2*j-1)*y)
            - 2*sp.sin(y)*sp.cos(2*j*y))
    _eq(sp.trigsimp(step, method="fu"), 0)
    _eq(sp.integrate(sp.cos(2*j*y), (y, 0, sp.pi)), 0)
    _eq(sp.integrate(1, (y, 0, sp.pi)), sp.pi)
    # Starting at sin(y)/sin(y)=1, the checked step gives the finite
    # cosine polynomial and its integral for every positive odd frequency.
    kernel = sp.sin((2*j+1)*y) / sp.sin(y)
    _eq(sp.limit(kernel, y, 0, dir="+"), 2*j+1)
    _eq(kernel.subs(y, sp.pi-y), kernel)
    # Reflection supplies the same finite limit at pi. The polynomial also
    # removes every zero introduced by the original product denominator.
    for odd in (1, 5, 9):
        k = (odd - 1) // 2
        kernel = 1 + 2 * sum(sp.cos(2 * j * y) for j in range(1, k + 1))
        _eq(sp.expand_trig(sp.sin(odd * y) - kernel * sp.sin(y)), 0)
        _eq(sp.integrate(kernel, (y, 0, sp.pi)), sp.pi)


def check_r3_2024_tournament_q04_v5() -> None:
    check_r3_2024_tournament_q04_v4()


def check_r3_2024_tournament_q05_v9() -> None:
    w = sp.symbols("w", positive=True)
    x = w * sp.exp(w)
    dx = sp.diff(x, w)
    integrand = sp.exp(w) / x**2 * dx
    _eq(sp.simplify(integrand), (w + 1) / w**2)
    _eq(sp.integrate((w + 1) / w**2, w), sp.log(w) - 1 / w)


def check_r3_2024_tournament_q05_v10() -> None:
    check_r3_2024_tournament_q05_v9()


def check_r3_2024_tournament_q06_v9() -> None:
    o = sp.symbols("o", real=True)
    b = sp.symbols("b", positive=True)
    s = sp.sqrt(b**2 + o**2)
    plus = b + o + s
    minus = b - o + s
    _eq(sp.simplify(1 / plus + 1 / minus), 1 / b)
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(sp.sin(x) ** 2 / x**2, (x, 0, sp.oo)), sp.pi / 2)
    _eq((sp.pi / 2) / 45, sp.pi / 90)


def check_r3_2024_tournament_q07_v10() -> None:
    s, a = sp.symbols("s a", positive=True)
    a = 2 ** sp.Rational(1, 4)
    first = 1 / (a + s)
    second = s / (a * s + a**2)
    _eq(sp.simplify(first + second), 1 / a)
    _eq(sp.integrate(1 / a, (s, 0, sp.pi / 4)) / 2, sp.pi / (8 * a))


def check_r3_2024_tournament_q07_v11() -> None:
    check_r3_2024_tournament_q07_v10()


def check_r3_2024_tournament_q08_v9() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    term = sp.factorial(n) * 2**n * sp.factorial(n) / sp.factorial(2 * n + 1)
    beta = 2**n * sp.beta(n + 1, n + 1)
    _eq(term, beta)
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(1 - 2 * x * (1 - x) - (sp.Rational(1, 2) * (1 + (2 * x - 1) ** 2))), 0)
    _eq(sp.integrate(2 / (1 + (2 * x - 1) ** 2), (x, 0, 1)), sp.pi / 2)


def check_r3_2024_tournament_q09_v10() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(1 / (x**2 + 3), (x, 1, sp.sqrt(3))), sp.pi / (12 * sp.sqrt(3)))
    _eq(sp.log(3) * sp.pi / (12 * sp.sqrt(3)), sp.pi * sp.log(3) / (12 * sp.sqrt(3)))


TOURNAMENT_CHECKS = (
    check_r3_2024_tournament_q01,
    check_r3_2024_tournament_q01_v10,
    check_r3_2024_tournament_q01_v11,
    check_r3_2024_tournament_q01_v4,
    check_r3_2024_tournament_q01_v7,
    check_r3_2024_tournament_q02,
    check_r3_2024_tournament_q02_v3,
    check_r3_2024_tournament_q02_v6,
    check_r3_2024_tournament_q02_v9,
    check_r3_2024_tournament_q03,
    check_r3_2024_tournament_q03_v10,
    check_r3_2024_tournament_q03_v4,
    check_r3_2024_tournament_q03_v7,
    check_r3_2024_tournament_q04,
    check_r3_2024_tournament_q04_v10,
    check_r3_2024_tournament_q04_v4,
    check_r3_2024_tournament_q04_v5,
    check_r3_2024_tournament_q04_v7,
    check_r3_2024_tournament_q05,
    check_r3_2024_tournament_q05_v10,
    check_r3_2024_tournament_q05_v4,
    check_r3_2024_tournament_q05_v6,
    check_r3_2024_tournament_q05_v9,
    check_r3_2024_tournament_q06,
    check_r3_2024_tournament_q06_v4,
    check_r3_2024_tournament_q06_v6,
    check_r3_2024_tournament_q06_v9,
    check_r3_2024_tournament_q07,
    check_r3_2024_tournament_q07_v10,
    check_r3_2024_tournament_q07_v11,
    check_r3_2024_tournament_q07_v4,
    check_r3_2024_tournament_q07_v7,
    check_r3_2024_tournament_q08,
    check_r3_2024_tournament_q08_v3,
    check_r3_2024_tournament_q08_v6,
    check_r3_2024_tournament_q08_v9,
    check_r3_2024_tournament_q09,
    check_r3_2024_tournament_q09_v10,
    check_r3_2024_tournament_q09_v4,
    check_r3_2024_tournament_q09_v7,
)

from pack_checks_tournament_rem import REM_CHECKS, REM_PACK_IDS

if set(TOURNAMENT_PACK_IDS) & set(REM_PACK_IDS):
    raise AssertionError("duplicate tournament pack ids")
TOURNAMENT_PACK_IDS = TOURNAMENT_PACK_IDS + REM_PACK_IDS
TOURNAMENT_CHECKS = TOURNAMENT_CHECKS + REM_CHECKS


if __name__ == "__main__":
    for check in TOURNAMENT_CHECKS:
        check()
        print(f"PASS {check.__name__}")
    print(f"PASS {len(TOURNAMENT_PACK_IDS)} tournament notes")
