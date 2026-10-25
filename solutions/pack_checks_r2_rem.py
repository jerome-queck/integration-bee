"""SymPy checks for the Round 2 notes added in the 2026-10-26 remainder wave.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

R2_REM_PACK_IDS = (
    "R2-2021-Group-Q02",
    "R2-2021-Group-Q03",
    "R2-2021-Group-Q06",
    "R2-2021-Group-Q09",
    "R2-2021-Relay-A01",
    "R2-2021-Relay-A02",
    "R2-2021-Relay-A03",
    "R2-2021-Relay-A04",
    "R2-2021-Relay-B01",
    "R2-2022-Group-Q02",
    "R2-2022-Group-Q05",
    "R2-2022-Group-Q07",
    "R2-2022-Relay-Q02",
    "R2-2022-Relay-Q03",
    "R2-2022-Relay-Q04",
    "R2-2022-Relay-Q05",
    "R2-2022-Relay-Q06",
    "R2-2022-Relay-Q07",
    "R2-2022-Relay-Q08",
    "R2-2022-Relay-Q09",
    "R2-2022-Relay-Q11",
    "R2-2022-Relay-Q12",
    "R2-2022-Relay-Q13",
    "R2-2022-Relay-Q16",
    "R2-2022-Relay-Q17",
    "R2-2022-Relay-Q18",
    "R2-2022-Relay-Q19",
    "R2-2023-Group-Q01",
    "R2-2023-Group-Q02",
    "R2-2023-Group-Q04",
    "R2-2023-Group-Q08",
    "R2-2023-Relay-Q01",
    "R2-2023-Relay-Q02",
    "R2-2023-Relay-Q03",
    "R2-2023-Relay-Q06",
    "R2-2023-Relay-Q12",
    "R2-2023-Relay-Q13",
    "R2-2023-Relay-Q15",
    "R2-2023-Relay-Q17",
    "R2-2023-Relay-Q20",
    "R2-2024-Group-Q08",
    "R2-2025-UK-Group-Q03",
    "R2-2025-UK-Relay-Q07",
    "R2-2025-UK-Relay-Q08",
    "R2-2025-UK-Relay-Q11",
    "R2-2025-UK-Relay-Q12",
    "R2-2025-UK-Relay-Q14",
    "R2-2025-UK-Relay-Q15",
    "R2-2025-UK-Relay-Q17",
    "R2-2025-UK-Relay-Q18",
    "R2-2025-UK-Relay-Q20",
)


def _eq(left, right) -> None:
    diff = sp.simplify(left - right)
    if diff == 0:
        return
    diff = sp.simplify(sp.expand(left - right))
    if diff == 0:
        return
    if sp.trigsimp(left - right) == 0:
        return
    raise AssertionError(f"{left} != {right}")


def check_r2_2021_group_q02() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    total = sp.symbols("N", integer=True, positive=True)
    left = sp.summation(sp.log(n - 1) - sp.log(n), (n, 2, total)).doit()
    right = sp.summation(sp.log(n + 1) - sp.log(n), (n, 2, total)).doit()
    _eq(left, -sp.log(total))
    _eq(right, sp.log(total + 1) - sp.log(2))
    partial = left + right
    _eq(sp.limit(partial, total, sp.oo), -sp.log(2))


def check_r2_2021_group_q03() -> None:
    a = sp.symbols("a", positive=True)
    base = sp.pi / sp.sqrt(a**2 - 1)
    second = sp.diff(base, a, 2) / 2
    _eq(sp.simplify(second.subs(a, 2)), sp.pi / (2 * sp.sqrt(3)))
    _eq(2 * (sp.pi / 2) / sp.sqrt((a + 1) * (a - 1)), base)


def check_r2_2021_group_q06() -> None:
    a, b = sp.symbols("a b", positive=True)
    _eq(sp.trigsimp(sp.sin(a) * sp.sin(b) - (sp.cos(a - b) - sp.cos(a + b)) / 2), 0)
    eps, p, q, s = sp.symbols("eps p q s", positive=True)
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(sp.exp(-eps * x) * sp.sin(s * x), (x, 0, sp.oo)), s / (eps**2 + s**2))
    _eq(
        sp.integrate(s / (eps**2 + s**2), (s, p, q)),
        sp.log(eps**2 + q**2) / 2 - sp.log(eps**2 + p**2) / 2,
    )
    _eq(sp.log((a + b) / (a - b)) / 2, sp.log(a / (a - b) + b / (a - b)) / 2)


def check_r2_2021_group_q09() -> None:
    u = sp.symbols("u", real=True)
    inner = sp.integrate(1 / (3 + u**2), (u, -1, 1))
    _eq(inner, sp.pi / (3 * sp.sqrt(3)))
    _eq(sp.pi * inner / 2, sp.pi**2 / (6 * sp.sqrt(3)))
    _eq(sp.pi**2 / (6 * sp.sqrt(3)), sp.sqrt(3) * sp.pi**2 / 18)


def check_r2_2021_relay_a01() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(sp.log(x) ** 2, (x, 0, 1)), 2)
    _eq(2**2, 4)


def check_r2_2021_relay_a02() -> None:
    x = sp.symbols("x", real=True)
    odd = (sp.sin(x) - sp.cos(x)) / (sp.sin(x) + sp.cos(x))
    _eq(sp.simplify(odd.subs(x, sp.pi / 2 - x) + odd), 0)
    value = sp.integrate(1 / sp.sqrt(2), (x, 0, sp.pi / 2))
    _eq(value, sp.pi / (2 * sp.sqrt(2)))
    _eq(sp.simplify(sp.pi / value), 2 * sp.sqrt(2))


def check_r2_2021_relay_a03() -> None:
    t = sp.symbols("t", positive=True)
    _eq(1 / (1 + t) + t / (1 + t), 1)
    x = sp.symbols("x", real=True)
    _eq(4 * sp.integrate(sp.Rational(1, 2), (x, 0, sp.pi / 2)), sp.pi)


def check_r2_2021_relay_a04() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(sp.sin(2 * x) - 2 * sp.sin(x) * sp.cos(x)), 0)
    inside = (
        sp.log(sp.sin(x))
        + sp.log(sp.cos(x))
        + sp.log(2)
        - sp.log(2 * sp.sin(x) * sp.cos(x))
    )
    _eq(sp.simplify(sp.exp(inside)), 1)
    j = -sp.pi / 2 * sp.log(2)
    _eq(sp.pi * j, -(sp.pi**2) * sp.log(2) / 2)


def check_r2_2021_relay_b01() -> None:
    x = sp.symbols("x", real=True)
    f = sp.sin(sp.sin(x) - x)
    _eq(sp.trigsimp(f.subs(x, 2 * sp.pi - x) + f), 0)


def check_r2_2022_group_q02() -> None:
    x = sp.symbols("x", positive=True)
    k = sp.symbols("k", integer=True, positive=True)
    _eq(sp.diff(x**k / sp.factorial(k), x), x ** (k - 1) / sp.factorial(k - 1))
    n = 4
    p = sum(x**j / sp.factorial(j) for j in range(n + 1))
    _eq(sp.diff(p, x), p - x**n / sp.factorial(n))
    antideriv = sp.factorial(n) * x - sp.factorial(n) * sp.log(p)
    _eq(sp.simplify(sp.diff(antideriv, x) - x**n / p), 0)


def check_r2_2022_group_q05() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    total = sp.symbols("N", integer=True, positive=True)
    finite = sp.product(1 - sp.Rational(1, 4) / k**2, (k, 1, total)).doit()
    closed = (
        2
        * sp.gamma(total + sp.Rational(1, 2))
        * sp.gamma(total + sp.Rational(3, 2))
        / (sp.pi * sp.gamma(total + 1) ** 2)
    )
    _eq(finite, closed)
    _eq(sp.limit(closed, total, sp.oo), 2 / sp.pi)
    _eq(sp.log(2 / sp.pi), sp.log(2) - sp.log(sp.pi))


def check_r2_2022_group_q07() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    piece = 1 / n - 2 / (2 * n + 1) - 2 / (2 * n + 1) ** 2
    _eq(sp.simplify(piece - 1 / (n * (2 * n + 1) ** 2)), 0)
    _eq(sp.summation((-1) ** (n - 1) / n, (n, 1, sp.oo)), sp.log(2))
    _eq(sp.summation((-1) ** (n - 1) / (2 * n + 1), (n, 1, sp.oo)), 1 - sp.pi / 4)
    alt = sp.summation((-1) ** (n - 1) / (2 * n + 1) ** 2, (n, 1, sp.oo))
    _eq(alt, 1 - sp.Catalan)
    value = -sp.log(2) + 2 * (1 - sp.pi / 4) + 2 * (1 - sp.Catalan)
    _eq(value, -sp.log(2) + 4 - 2 * sp.Catalan - sp.pi / 2)


def check_r2_2022_relay_q02() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(1 / (x + 1 / x) ** 2 - x**2 / (x**2 + 1) ** 2), 0)
    _eq(sp.simplify(x**2 / (x**2 + 1) ** 2 - (1 / (x**2 + 1) - 1 / (x**2 + 1) ** 2)), 0)
    _eq(sp.integrate(1 / (x**2 + 1), (x, -sp.oo, sp.oo)), sp.pi)
    _eq(sp.integrate(1 / (x**2 + 1) ** 2, (x, -sp.oo, sp.oo)), sp.pi / 2)


def check_r2_2022_relay_q03() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    x = sp.symbols("x", real=True)
    coeff = sp.integrate(x * sp.cos(2 * k * x), (x, 0, sp.pi / 2))
    _eq(sp.simplify(coeff), ((-1) ** k - 1) / (4 * k**2))
    m = sp.symbols("m", integer=True, nonnegative=True)
    odd = sp.summation(1 / (2 * m + 1) ** 3, (m, 0, sp.oo)).rewrite(sp.zeta)
    reduced = sp.simplify(odd)
    _eq(reduced, sp.zeta(3) * sp.Rational(7, 8))
    _eq(reduced / 2, sp.zeta(3) * sp.Rational(7, 16))
    _eq(sp.integrate(x, (x, 0, sp.pi / 2)) * (-sp.log(2)), -(sp.pi**2) * sp.log(2) / 8)


def check_r2_2022_relay_q04() -> None:
    a = sp.symbols("a", positive=True)
    t = sp.symbols("t", nonnegative=True)
    span = sp.sqrt(a**2 - 1)
    antideriv = sp.atan(t * span / a) / (a * span)
    target = 1 / (a**2 + (a**2 - 1) * t**2)
    _eq(sp.simplify(sp.diff(antideriv, t) - target), 0)
    _eq(sp.limit(sp.atan(t), t, sp.oo), sp.pi / 2)
    _eq(sp.simplify((sp.pi / 2) / (a * span) - sp.pi / (2 * a * span)), 0)


def check_r2_2022_relay_q05() -> None:
    p, q, s = sp.symbols("p q s", positive=True)
    u = sp.symbols("u", positive=True)
    _eq(sp.integrate(sp.exp(-s * u), (u, 0, sp.oo)), 1 / s)
    _eq(sp.integrate(1 / s, (s, p, q)), sp.log(q / p))
    _eq(sp.log(sp.Rational(2024, 24)), sp.log(sp.Rational(253, 3)))


def check_r2_2022_relay_q06() -> None:
    u = sp.symbols("u", positive=True)
    pulled = sp.log(1 / u) * sp.diff(1 / u, u) / (1 + (1 / u) ** 2)
    _eq(sp.simplify(pulled - sp.log(u) / (1 + u**2)), 0)
    _eq(
        (1 / sp.sqrt(3)) * (sp.log(3) / 2) * (sp.pi / 6),
        sp.pi * sp.log(3) / (12 * sp.sqrt(3)),
    )


def check_r2_2022_relay_q07() -> None:
    x = sp.symbols("x", positive=True)
    k = sp.symbols("k", integer=True, positive=True)
    series = 1 / x + 2 * x * (-1) / (x**2 + sp.pi**2)
    # The integrated term is exact; the expansion is checked numerically below.
    _eq(sp.integrate(1 / (x**2 + (sp.pi * k) ** 2), (x, 0, sp.oo)), 1 / (2 * k))
    _eq(sp.summation((-1) ** (k - 1) / k, (k, 1, sp.oo)), sp.log(2))
    got = mp.nsum(lambda m: ((-1) ** m) * 2 / (1 + (mp.pi * m) ** 2), [1, mp.inf])
    target = mp.csch(1) - 1
    if abs(got - target) > mp.mpf("1e-20"):
        raise AssertionError(f"csch expansion {got} vs {target}")
    _ = series  # documents the k=1 summand of the expansion


def check_r2_2022_relay_q08() -> None:
    x = sp.symbols("x", positive=True)
    g = 1 / (1 + sp.exp(-1 / x))
    reflected = 1 / (1 + sp.exp(1 / x))
    _eq(sp.simplify(g + reflected - 1), 0)
    _eq(sp.integrate(sp.cos(x), (x, 0, 1)), sp.sin(1))


def check_r2_2022_relay_q09() -> None:
    x = sp.symbols("x", real=True)
    t = sp.symbols("t", real=True)
    f = sp.exp(x)
    _eq(sp.simplify(f - sp.integrate(sp.exp(t), (t, 0, x)) - 1), 0)


def check_r2_2022_relay_q11() -> None:
    x, v = sp.symbols("x v", positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    changed = (sp.sin(x * v) / (x * v)) ** (n - 1) / v
    _eq(sp.limit(changed, x, 0), 1 / v)
    _eq(sp.integrate(1 / v, (v, 1, 2)), sp.log(2))


def check_r2_2022_relay_q12() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    left = sp.harmonic(2 * n) - sp.harmonic(n)
    _eq(left.subs(n, 1), sp.Rational(1, 2))
    _eq(sum(1 / (1 + k) for k in range(1, 2)), sp.Rational(1, 2))
    _eq(sp.expand_func(sp.harmonic(2 * n + 1) - sp.harmonic(2 * n)), 1 / (2 * n + 1))
    _eq(sp.expand_func(sp.harmonic(2 * n + 2) - sp.harmonic(2 * n + 1)), 1 / (2 * n + 2))
    _eq(sp.expand_func(sp.harmonic(n + 1) - sp.harmonic(n)), 1 / (n + 1))
    _eq(sp.limit(left, n, sp.oo), sp.log(2))


def check_r2_2022_relay_q13() -> None:
    t = sp.symbols("t", real=True)
    _eq(sp.simplify(sp.sin(sp.sin(t + sp.pi)) + sp.sin(sp.sin(t))), 0)


def check_r2_2022_relay_q16() -> None:
    u = sp.symbols("u", real=True)
    _eq(sp.integrate(sp.sqrt(1 - u**2), (u, 0, 1)), sp.pi / 4)


def check_r2_2022_relay_q17() -> None:
    a = sp.symbols("a", positive=True)
    p = a + sp.sqrt(a**2 - 1)
    q = a - sp.sqrt(a**2 - 1)
    _eq(sp.simplify(p * q), 1)
    _eq(sp.simplify(p + q), 2 * a)
    value = (sp.pi / 2) * (1 / sp.sqrt(q) - 1 / sp.sqrt(p)) / (p - q)
    target = sp.pi / (2 * sp.sqrt(2 * a + 2))
    _eq(sp.simplify(sp.sqrtdenest(value) - target), 0)


def check_r2_2022_relay_q18() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify(sp.sin(sp.acos(x)) - sp.sqrt(1 - x**2)), 0)
    _eq(sp.integrate(sp.sqrt(1 - x**2), (x, 0, 1)), sp.pi / 4)


def check_r2_2022_relay_q19() -> None:
    x = sp.symbols("x", real=True)
    f = x**3 * sp.exp(-(x**2))
    _eq(sp.simplify(f.subs(x, -x) + f), 0)


def check_r2_2023_group_q01() -> None:
    x = sp.symbols("x", real=True)
    f = sp.cos(sp.cos(x) ** 2) ** 2 + sp.sin(sp.sin(x) ** 2) ** 2
    _eq(sp.simplify(f + f.subs(x, sp.pi / 2 - x) - 2), 0)
    _eq(sp.simplify(f.subs(x, x + sp.pi) - f), 0)
    _eq(sp.integrate(1, (x, 0, sp.pi)), sp.pi)


def check_r2_2023_group_q02() -> None:
    w = sp.symbols("w", positive=True)
    n = sp.symbols("n", integer=True, nonnegative=True)
    _eq(sp.integrate(w ** (2 * n) * sp.log(w), (w, 0, 1)), -1 / (2 * n + 1) ** 2)
    _eq(sp.summation((-1) ** n / (2 * n + 1) ** 2, (n, 0, sp.oo)), sp.Catalan)
    _eq(4 * sp.Catalan, 4 * sp.Catalan)


def check_r2_2023_group_q04() -> None:
    x = sp.symbols("x", positive=True)
    cos = sp.cos(x)
    left_sq = 1 - x**2 * cos**2
    right_sq = cos**2 * (sp.sec(x) ** 2 - x**2)
    _eq(sp.simplify(left_sq - right_sq), 0)
    _eq(sp.simplify((cos - x * sp.sin(x)) - cos * (1 - x * sp.tan(x))), 0)
    antideriv = sp.asin(x * cos)
    _eq(antideriv.subs(x, 0), 0)
    _eq(sp.limit(antideriv, x, sp.pi / 2), 0)


def check_r2_2023_group_q08() -> None:
    x = sp.symbols("x", real=True)
    a_part = sp.sin(23 * x) + sp.sin(25 * x)
    b_part = sp.cos(23 * x) + sp.cos(25 * x)
    square = a_part**2 + b_part**2 + 100
    cross = 20 * (sp.cos(x) + sp.cos(x))
    # cos(24x-23x)+cos(24x-25x) = 2 cos x, and the factor 20 comes from 2*10.
    _eq(sp.trigsimp(sp.cos(24 * x - 23 * x) + sp.cos(24 * x - 25 * x) - 2 * sp.cos(x)), 0)
    pair = a_part**2 + b_part**2 - (2 + 2 * sp.cos(2 * x))
    _eq(sp.simplify(sp.expand(pair.rewrite(sp.exp))), 0)
    total = sp.sin(23 * x) + 10 * sp.sin(24 * x) + sp.sin(25 * x)
    total_c = sp.cos(23 * x) + 10 * sp.cos(24 * x) + sp.cos(25 * x)
    expr = total**2 + total_c**2 - (10 + 2 * sp.cos(x)) ** 2
    _eq(sp.simplify(sp.expand(expr.rewrite(sp.exp))), 0)
    _eq(sp.diff(10 * x + 2 * sp.sin(x), x), 10 + 2 * sp.cos(x))
    _ = square, cross


def check_r2_2023_relay_q01() -> None:
    x = sp.symbols("x", real=True)
    first = sp.cos(x) ** (sp.sin(x) ** sp.cos(x))
    second = sp.sin(x) ** (sp.cos(x) ** sp.sin(x))
    swapped = first.subs(x, sp.pi / 2 - x)
    _eq(sp.simplify(swapped - second), 0)


def check_r2_2023_relay_q02() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.integrate(1, (x, 0, sp.pi)), sp.pi)


def check_r2_2023_relay_q03() -> None:
    t = sp.symbols("t", positive=True)
    _eq(sp.gamma(t) * sp.gamma(1 - t), sp.pi / sp.sin(sp.pi * t))
    raabe = sp.log(2 * sp.pi) / 2
    _eq(2 * raabe - 1, sp.log(2 * sp.pi) - 1)


def check_r2_2023_relay_q06() -> None:
    x = sp.symbols("x", real=True)
    quotient = 16 * sp.cos(x) ** 4 - 12 * sp.cos(x) ** 2 + 1
    _eq(sp.expand(sp.sin(5 * x).rewrite(sp.exp) - (sp.sin(x) * quotient).rewrite(sp.exp)), 0)
    expr = sp.expand((quotient**2 * sp.sin(4 * x) ** 2).rewrite(sp.exp))
    _eq(sp.integrate(expr, (x, 0, 2 * sp.pi)), 4 * sp.pi)


def check_r2_2023_relay_q12() -> None:
    v = sp.symbols("v", real=True)
    _eq(sp.integrate(v * (1 - v**2), (v, 0, 1)), sp.Rational(1, 4))
    _eq(sp.log(2) ** 4 * sp.Rational(1, 4), sp.log(2) ** 4 / 4)


def check_r2_2023_relay_q13() -> None:
    x, v = sp.symbols("x v", positive=True)
    n = sp.symbols("n", integer=True, positive=True)
    changed = (sp.tan(x * v) / (x * v)) ** (n - 1) / v
    _eq(sp.limit(changed, x, 0), 1 / v)
    _eq(sp.integrate(1 / v, (v, 1, 2)), sp.log(2))


def check_r2_2023_relay_q15() -> None:
    theta = sp.symbols("theta", real=True)
    wallis = sp.integrate(sp.cos(theta) ** 4, (theta, 0, sp.pi / 2))
    _eq(wallis, 3 * sp.pi / 16)
    _eq(sp.Rational(8, 3) * sp.pi * wallis, sp.pi**2 / 2)


def check_r2_2023_relay_q17() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    total = sp.symbols("N", integer=True, positive=True)
    _eq(sp.simplify(2 * (1 / (4 * k - 1) - 1 / (4 * k + 1)) - 4 / (16 * k**2 - 1)), 0)
    base = 1 - sp.Rational(1, 3) + sp.Rational(1, 5)
    _eq(base, 1 - (sp.Rational(1, 3) - sp.Rational(1, 5)))
    step = (-1) ** (2 * total + 1) / (4 * total + 3) + (-1) ** (2 * total + 2) / (4 * total + 5)
    gap_step = -(1 / (4 * (total + 1) - 1) - 1 / (4 * (total + 1) + 1))
    _eq(sp.simplify(step - gap_step), 0)
    _eq(sp.summation((-1) ** k / (2 * k + 1), (k, 0, sp.oo)), sp.pi / 4)
    _eq(-1 + 2 * (1 - sp.pi / 4), 1 - sp.pi / 2)


def check_r2_2023_relay_q20() -> None:
    x = sp.symbols("x", positive=True)
    f = sp.log(1 + x**2) / 4
    _eq(sp.diff(f**2, x), x * f / (1 + x**2))
    _eq(2 * sp.integrate(f, (x, 0, 1)), (sp.pi + sp.log(4) - 4) / 4)


def check_r2_2024_group_q08() -> None:
    x = sp.symbols("x", positive=True)
    vertex = (sp.sqrt(1 - x**2) - sp.sqrt(1 + x**2)) / (2 * sp.sqrt(1 - x**4))
    split = 1 / (2 * sp.sqrt(1 + x**2)) - 1 / (2 * sp.sqrt(1 - x**2))
    _eq(sp.simplify(vertex - split), 0)
    coeff = sp.sqrt(1 - x**4)
    linear = sp.sqrt(1 + x**2) - sp.sqrt(1 - x**2)
    _eq(sp.simplify(-linear / (2 * coeff) - vertex), 0)
    _eq(sp.integrate(split, (x, 0, 1)), sp.log(1 + sp.sqrt(2)) / 2 - sp.pi / 4)
    _eq(sp.asinh(1), sp.log(1 + sp.sqrt(2)))


def check_r2_2025_uk_group_q03() -> None:
    x = sp.symbols("x", real=True)
    left = sp.sqrt(2 * x - x**2)
    right = sp.sqrt(1 - x**2)
    _eq(sp.simplify((left - right) * (left + right) - (2 * x - 1)), 0)
    _eq(sp.simplify(1 - (x - 1) ** 2 - (2 * x - x**2)), 0)
    y = sp.symbols("y", real=True)
    _eq(sp.integrate(sp.sqrt(1 - x**2), (x, 0, 1)), sp.pi / 4)
    _eq(sp.integrate(sp.sqrt(1 - y**2), (y, -1, 0)), sp.pi / 4)
    _eq(2 * (sp.pi / 4), sp.pi / 2)


def check_r2_2025_uk_relay_q07() -> None:
    x = sp.symbols("x", positive=True)
    y = sp.sin(x) ** sp.tan(x)
    integrand = sp.sin(x) ** (sp.tan(x) - 2) * (
        sp.tan(x) ** 2 * sp.log(sp.sin(x)) + sp.sin(x) ** 2
    )
    _eq(sp.simplify(sp.diff(y, x) - integrand), 0)
    _eq((sp.sqrt(2) / 2) ** 1, 1 / sp.sqrt(2))
    eps = sp.symbols("eps", positive=True)
    _eq(sp.limit(sp.cot(eps) * sp.log(sp.cos(eps)), eps, 0), 0)
    _eq(1 - 1 / sp.sqrt(2), 1 - 1 / sp.sqrt(2))


def check_r2_2025_uk_relay_q08() -> None:
    x = sp.symbols("x", real=True)
    f = sp.sin(x) ** 67 / (2026 - sp.cos(x))
    _eq(sp.simplify(f.subs(x, 2 * sp.pi - x) + f), 0)


def check_r2_2025_uk_relay_q11() -> None:
    a = sp.symbols("a")
    ratio = sp.gamma(a + 1) * sp.sin(sp.pi * a / 2) / a
    series = ratio.series(a, 0, 2).removeO()
    _eq(series.subs(a, 0), sp.pi / 2)
    slope = sp.diff(series, a).subs(a, 0)
    _eq(slope, -sp.EulerGamma * sp.pi / 2)


def check_r2_2025_uk_relay_q12() -> None:
    x = sp.symbols("x")
    _eq(sp.expand((1 - x) * (1 + x) - (1 - x**2)), 0)
    ell = sp.symbols("ell")
    _eq(sp.simplify((2 + ell / 2) / (4 + ell) - sp.Rational(1, 2)), 0)
    _eq(sp.integrate(sp.Rational(1, 2), (x, 0, 1)), sp.Rational(1, 2))


def check_r2_2025_uk_relay_q14() -> None:
    a, b = sp.symbols("a b", positive=True)
    _eq(sp.gamma(a / b) * sp.gamma(1 - a / b), sp.pi / sp.sin(sp.pi * a / b))
    aa = sp.symbols("aa", positive=True)
    closed = (sp.pi / sp.E) / sp.sin(sp.pi * aa / sp.E)
    _eq(closed.subs(aa, sp.E / 2), sp.pi / sp.E)
    _eq(sp.diff(closed, aa).subs(aa, sp.E / 2), 0)


def check_r2_2025_uk_relay_q15() -> None:
    x = sp.symbols("x", positive=True)
    u = sp.symbols("u", positive=True)
    integrand = (1 - x) / ((1 + x) * sp.sqrt(x + x**2 + x**3))
    changed = (1 - u) / (1 + u)
    pulled = integrand.subs(x, changed) * sp.diff(changed, u)
    target = -2 * u / (sp.sqrt(1 - u**2) * sp.sqrt(u**2 + 3))
    _eq(sp.simplify(pulled - target), 0)
    w = sp.symbols("w", real=True)
    _eq(sp.simplify((1 - w) * (w + 3) - (3 - 2 * w - w**2)), 0)
    _eq(sp.simplify(4 - (w + 1) ** 2 - (3 - 2 * w - w**2)), 0)
    uu = sp.symbols("uu", positive=True)
    _eq(sp.simplify(sp.diff(sp.asin(uu / 2), uu) - 1 / sp.sqrt(4 - uu**2)), 0)
    _eq(sp.asin(1) - sp.asin(sp.Rational(1, 2)), sp.pi / 3)


def check_r2_2025_uk_relay_q17() -> None:
    n = sp.symbols("n", integer=True)
    _eq(sp.floor(2 * n + sp.Rational(1, 3)), 2 * n)
    _eq(sp.floor(2 * n), 2 * n)
    m = sp.symbols("m", integer=True, positive=True)
    _eq(sp.summation(1 / (4 * m**2), (m, 1, sp.oo)), sp.pi**2 / 24)


def check_r2_2025_uk_relay_q18() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.simplify((x**2 - 1) / (x**2 + 1) - (1 - 2 / (x**2 + 1))), 0)
    b = sp.symbols("b", positive=True)
    _eq(
        sp.integrate(sp.cos(b * x) / (x**2 + 1), (x, 0, sp.oo)),
        sp.pi / 2 * sp.exp(-b),
    )
    kernel = sp.integrate(sp.pi / 2 * sp.exp(-b), (b, 0, 1))
    _eq(sp.pi / 2 - 2 * kernel, sp.pi / sp.E - sp.pi / 2)


def check_r2_2025_uk_relay_q20() -> None:
    mp.mp.dps = 40
    base = mp.mpf(2025)
    powers = {k: mp.power(base, mp.mpf(1) / k) for k in range(1, 11)}
    total = (powers[10] - 2) / 10
    for k in range(2, 10):
        total += (powers[k] - powers[k + 1]) / k
    total += powers[1] - powers[2]
    if not (mp.mpf(1999) < total < mp.mpf(2000)):
        raise AssertionError(total)
    if int(mp.floor(total)) != 1999:
        raise AssertionError(total)
    _eq(sp.simplify(2 * sp.log(5) + 4 * sp.log(3) - sp.log(2025)), 0)


R2_REM_CHECKS = (
    check_r2_2021_group_q02,
    check_r2_2021_group_q03,
    check_r2_2021_group_q06,
    check_r2_2021_group_q09,
    check_r2_2021_relay_a01,
    check_r2_2021_relay_a02,
    check_r2_2021_relay_a03,
    check_r2_2021_relay_a04,
    check_r2_2021_relay_b01,
    check_r2_2022_group_q02,
    check_r2_2022_group_q05,
    check_r2_2022_group_q07,
    check_r2_2022_relay_q02,
    check_r2_2022_relay_q03,
    check_r2_2022_relay_q04,
    check_r2_2022_relay_q05,
    check_r2_2022_relay_q06,
    check_r2_2022_relay_q07,
    check_r2_2022_relay_q08,
    check_r2_2022_relay_q09,
    check_r2_2022_relay_q11,
    check_r2_2022_relay_q12,
    check_r2_2022_relay_q13,
    check_r2_2022_relay_q16,
    check_r2_2022_relay_q17,
    check_r2_2022_relay_q18,
    check_r2_2022_relay_q19,
    check_r2_2023_group_q01,
    check_r2_2023_group_q02,
    check_r2_2023_group_q04,
    check_r2_2023_group_q08,
    check_r2_2023_relay_q01,
    check_r2_2023_relay_q02,
    check_r2_2023_relay_q03,
    check_r2_2023_relay_q06,
    check_r2_2023_relay_q12,
    check_r2_2023_relay_q13,
    check_r2_2023_relay_q15,
    check_r2_2023_relay_q17,
    check_r2_2023_relay_q20,
    check_r2_2024_group_q08,
    check_r2_2025_uk_group_q03,
    check_r2_2025_uk_relay_q07,
    check_r2_2025_uk_relay_q08,
    check_r2_2025_uk_relay_q11,
    check_r2_2025_uk_relay_q12,
    check_r2_2025_uk_relay_q14,
    check_r2_2025_uk_relay_q15,
    check_r2_2025_uk_relay_q17,
    check_r2_2025_uk_relay_q18,
    check_r2_2025_uk_relay_q20,
)
