"""SymPy checks for the Round 2 notes added in the fourth 2026-10-26 wave.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

R2_WAVE4_PACK_IDS = (
    "R2-2023-Group-Q09",
    "R2-2023-Group-Q10",
    "R2-2023-Relay-Q04",
    "R2-2025-SG-Group-Q10",
    "R2-2025-SG-Group-Q13",
    "R2-2025-SG-Group-Q15",
    "R2-2025-SG-Relay-Q07",
    "R2-2025-SG-Relay-Q08",
    "R2-2025-SG-Relay-Q10",
    "R2-2025-SG-Relay-Q14",
    "R2-2025-SG-Relay-Q16",
    "R2-2025-SG-Relay-Q18",
    "R2-2025-SG-Relay-Q20",
    "R2-2025-SG-Relay-Q24",
    "R2-2025-UK-Group-Q10",
    "R2-2025-UK-Relay-Q09",
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


def check_r2_2023_group_q09() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    x = sp.symbols("x")
    _eq(sp.binomial(n, x), sp.binomial(n - 1, x) + sp.binomial(n - 1, x - 1))
    _eq(sp.binomial(n, x), sp.factorial(n) / (sp.gamma(x + 1) * sp.gamma(n - x + 1)))
    _eq(sp.gamma(n - x + 1), sp.rf(1 - x, n) * sp.gamma(1 - x))
    _eq(sp.gamma(x + 1), x * sp.gamma(x))
    z = sp.symbols("z")
    _eq(sp.gamma(z) * sp.gamma(1 - z) * sp.sin(sp.pi * z), sp.pi)
    formula = sp.factorial(n) * sp.sin(sp.pi * x) / (sp.pi * x * sp.rf(1 - x, n))
    gamma_form = sp.factorial(n) / (sp.gamma(x + 1) * sp.gamma(n - x + 1))
    factor = sp.sin(sp.pi * x) * sp.gamma(x) * sp.gamma(1 - x) - sp.pi
    gap = gamma_form - formula
    gap += factor * sp.factorial(n) / (sp.pi * sp.gamma(x + 1) * sp.gamma(n - x + 1))
    _eq(gap, 0)
    _eq(sp.binomial(0, x), sp.sin(sp.pi * x) / (sp.pi * x))
    _eq(sp.integrate(sp.sin(sp.pi * x) / (sp.pi * x), (x, -sp.oo, sp.oo)), 1)
    shifted = sp.sin(sp.pi * (1 - x)) / (sp.pi * (1 - x))
    _eq(sp.binomial(1, x), sp.sin(sp.pi * x) / (sp.pi * x) + shifted)
    _eq(sp.integrate(shifted, (x, -sp.oo, sp.oo)), 1)


def check_r2_2023_group_q10() -> None:
    x = sp.symbols("x", real=True)
    _eq(1 + sp.cos(x), 2 * sp.cos(x / 2) ** 2)
    phi = (1 + sp.sqrt(5)) / 2
    root = sp.sqrt(phi)
    _eq((root + sp.I / root) ** 2, 1 + 2 * sp.I)
    _eq((1 + 1 / root) / (1 + root), 1 / root)
    _eq(sp.tan(sp.acot(root)), 1 / root)
    b = 1 + sp.I
    c = sp.I
    _eq(b**2 - c**2, 1 + 2 * sp.I)
    _eq(sp.re(b + c * sp.cos(x)), 1)
    z = (b + root + sp.I / root) / 2
    _eq(sp.im(z) / sp.re(z), 1 / root)
    _eq(sp.im(sp.log(z)), sp.atan(sp.im(z) / sp.re(z)))
    t, gap, base = sp.symbols("t gap base", positive=True)
    cosine = (1 - t**2) / (1 + t**2)
    slope = gap + base
    _eq(
        (2 / (1 + t**2)) / (slope + base * cosine),
        2 / ((slope + base) + (slope - base) * t**2),
    )
    got = sp.integrate(2 / ((2 * base + gap) + gap * t**2), (t, 0, sp.oo))
    _eq(got, sp.pi / sp.sqrt((base + gap) ** 2 - base**2))
    bb, cc = sp.symbols("bb cc", positive=True)
    form = sp.pi * sp.log((bb + sp.sqrt(bb**2 - cc**2)) / 2)
    _eq(sp.diff(form, bb), sp.pi / sp.sqrt(bb**2 - cc**2))
    _eq(sp.limit(form - sp.pi * sp.log(bb), bb, sp.oo), 0)


def check_r2_2023_relay_q04() -> None:
    xx = sp.symbols("xx", positive=True)
    half = sp.Rational(1, 2) * (
        sp.log(sp.exp(xx / 2) - 1) - sp.log(sp.exp(xx / 2) + 1)
    )
    _eq(sp.diff(half, xx), sp.Rational(1, 2) * sp.exp(xx / 2) / (sp.exp(xx) - 1))
    _eq(
        sp.tanh(xx / 4).rewrite(sp.exp),
        (sp.exp(xx / 2) - 1) / (sp.exp(xx / 2) + 1),
    )
    u = sp.symbols("u", positive=True)
    _eq(sp.tanh(u).rewrite(sp.exp), (sp.exp(2 * u) - 1) / (sp.exp(2 * u) + 1))
    closed = sp.log(1 - sp.exp(-2 * u)) - sp.log(1 + sp.exp(-2 * u))
    _eq(sp.log((sp.exp(2 * u) - 1) / (sp.exp(2 * u) + 1)), closed)
    m = sp.symbols("m", integer=True, positive=True)
    _eq((-1) ** (2 * m), 1)
    _eq((-1) ** (2 * m - 1), -1)
    _eq((-1) ** (2 * m + 1), -1)
    a = sp.symbols("a", positive=True)
    _eq(
        sp.integrate(sp.exp(-a * u) * (1 - sp.exp(-2 * u)), (u, 0, sp.oo)),
        1 / a - 1 / (a + 2),
    )
    mm = sp.symbols("mm", integer=True, nonnegative=True)
    term = 1 / (2 * (2 * mm + 1) ** 2) - 1 / (4 * (2 * mm + 1) * (mm + 1))
    _eq(4 * term, 2 / (2 * mm + 1) ** 2 - 1 / ((2 * mm + 1) * (mm + 1)))
    _eq(1 / ((2 * mm + 1) * (mm + 1)), 2 / (2 * mm + 1) - 1 / (mm + 1))
    _eq(sp.summation(1 / (2 * mm + 1) ** 2, (mm, 0, sp.oo)), sp.pi**2 / 8)
    total = sp.symbols("N", integer=True, positive=True)

    def partial(index):
        return (
            2 * sp.harmonic(2 * index + 1)
            - sp.harmonic(index)
            - sp.harmonic(index + 1)
        )

    step = sp.simplify(sp.expand_func(partial(total) - partial(total - 1)))
    _eq(step, 2 / (2 * total + 1) - 1 / (total + 1))
    _eq(partial(0), 1)
    _eq(sp.limit(partial(total), total, sp.oo), 2 * sp.log(2))
    value = sp.pi**2 / 4 - 2 * sp.log(2)
    _eq(2 * (sp.pi**2 / 8) - 2 * sp.log(2), value)


def check_r2_2025_sg_group_q10() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.diff((x + 1) / x**3, x), -(2 * x + 3) / x**4)
    _eq(x**6 + x**2 + 2 * x + 1, x**6 + (x + 1) ** 2)
    u = sp.symbols("u", positive=True)
    expr = (
        x
        * (2 * x + 3)
        * (u ** sp.Rational(1, 3) * x)
        * (-(x**4) / (2 * x + 3))
        / (x**6 * (1 + u**2))
    )
    _eq(expr, -(u ** sp.Rational(1, 3)) / (1 + u**2))
    v = sp.symbols("v", positive=True)
    piece = v ** sp.Rational(1, 6) * sp.Rational(1, 2) * v ** sp.Rational(-1, 2)
    _eq(piece, sp.Rational(1, 2) * v ** (sp.Rational(2, 3) - 1))
    _eq(
        sp.integrate(v ** (sp.Rational(2, 3) - 1) / (1 + v), (v, 0, sp.oo)),
        sp.pi / sp.sin(2 * sp.pi / 3),
    )
    _eq(sp.pi / sp.sin(2 * sp.pi / 3) / 2, sp.pi / sp.sqrt(3))


def _check_ceiling() -> None:
    x = sp.symbols("x", positive=True)
    angle = sp.atan(x)
    raw = 1 / angle - (1 + x**2) / (1 + angle + x**2 * angle)
    reduced = 1 / (angle * (1 + angle * (1 + x**2)))
    _eq(raw, reduced)
    u, width = sp.symbols("u width", positive=True)
    aa, xx = sp.symbols("aa xx", positive=True)
    reduced_s = 1 / (aa * (1 + aa * (1 + xx**2)))
    substituted = reduced_s.subs({aa: u, xx**2: (1 - width) / width}) / width
    _eq(substituted, 1 / (u**2 + u * width))
    _eq(sp.together(1 / u**2 - 1 / (u**2 + u * width)), width / (u**2 * (u + width)))
    _eq(sp.integrate(1 / u**2, (u, sp.pi / 4, sp.pi / 2)), 2 / sp.pi)
    if not bool(sp.pi > 3):
        raise AssertionError("pi > 3")


def check_r2_2025_sg_group_q13() -> None:
    _check_ceiling()


def check_r2_2025_uk_group_q10() -> None:
    _check_ceiling()


def check_r2_2025_sg_group_q15() -> None:
    x = sp.symbols("x")
    antideriv = x * sp.asin(x) + sp.sqrt(1 - x**2)
    _eq(sp.diff(antideriv, x), sp.asin(x))
    _eq(antideriv.subs(x, 1) - antideriv.subs(x, 0), sp.pi / 2 - 1)
    n, t = sp.symbols("n t")
    _eq(sp.diff(sp.sin(t) ** (-n), t), -n * sp.cos(t) / sp.sin(t) ** (n + 1))
    for degree in range(1, 9):
        series_coeff = sp.series(sp.asin(x), x, 0, degree + 1).coeff(x, degree)
        height = (t / sp.sin(t)) ** degree
        coeff = sp.series(height, t, 0, degree).coeff(t, degree - 1) / degree
        _eq(series_coeff, coeff)


def check_r2_2025_sg_relay_q07() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    _eq(sp.factorial(n + 1), (n + 1) * sp.factorial(n))
    _eq(sp.factorial(2026), 2026 * sp.factorial(2025))
    phi = sp.symbols("phi", real=True)
    _eq(sp.Abs(1 - sp.exp(sp.I * phi)) ** 2, 4 * sp.sin(phi / 2) ** 2)
    left, right = sp.symbols("left right", real=True)
    _eq(
        sp.cos(left) * sp.cos(right),
        (sp.cos(left + right) + sp.cos(left - right)) / 2,
    )
    frequency = sp.symbols("frequency", integer=True, positive=True)
    theta = sp.symbols("theta", real=True)
    _eq(sp.integrate(sp.cos(2 * frequency * theta), (theta, 0, sp.pi / 2)), 0)
    _eq(sp.integrate(sp.cos(2 * frequency * theta) ** 2, (theta, 0, sp.pi / 2)), sp.pi / 4)
    _eq(sp.pi / 4 * (sp.pi**2 / 6) / 2026, sp.pi**3 / 48624)
    _eq(24 * 2026, 48624)
    z = sp.symbols("z")
    _eq(sp.expand_func(sp.polylog(1, z)), -sp.log(1 - z))
    _eq(sp.diff(-sp.log(1 - z), z), 1 / (1 - z))


def check_r2_2025_sg_relay_q08() -> None:
    x = sp.symbols("x", real=True)
    logder = sp.diff(sp.tan(x) * sp.log(sp.sin(x)), x)
    _eq(logder, sp.sec(x) ** 2 * sp.log(sp.sin(x)) + 1)
    _eq(sp.tan(x) ** 2 / sp.sin(x) ** 2, sp.sec(x) ** 2)
    ratio = sp.sin(x) ** (-2) * (sp.tan(x) ** 2 * sp.log(sp.sin(x)) + sp.sin(x) ** 2)
    _eq(ratio, logder)
    _eq(sp.sin(sp.pi / 4) ** sp.tan(sp.pi / 4), 1 / sp.sqrt(2))
    _eq(sp.limit(sp.tan(x) * sp.log(sp.sin(x)), x, sp.pi / 2, dir="-"), 0)


def check_r2_2025_sg_relay_q10() -> None:
    x = sp.symbols("x", real=True)
    power = sp.symbols("power", integer=True, nonnegative=True)
    _eq((-sp.sin(x)) ** (2 * power + 1) + sp.sin(x) ** (2 * power + 1), 0)
    _eq(sp.cos(2 * sp.pi - x), sp.cos(x))
    _eq(2026 - sp.cos(x) - (2025 + 1 - sp.cos(x)), 0)


def check_r2_2025_sg_relay_q14() -> None:
    ratio = sp.symbols("ratio")
    count = sp.symbols("count", integer=True, positive=True)
    last = sp.symbols("last", integer=True, positive=True)
    partial = sp.summation(ratio**count, (count, 1, last))
    _eq(partial * (1 - ratio) - ratio * (1 - ratio**last), 0)
    index = sp.symbols("index", integer=True, positive=True)
    _eq(sp.summation(1 / (index * (index + 1)), (index, 2, sp.oo)), sp.Rational(1, 2))
    _eq((index - 1) / (index * (index - 1) * (index + 1)), 1 / (index * (index + 1)))
    level = sp.symbols("level", integer=True, positive=True)
    _eq(level / index - level / (index + 1), level / (index * (index + 1)))


def _check_floor_log() -> None:
    mp.mp.dps = 40
    base = mp.mpf(2025)
    log_bound = mp.log(base) / mp.log(2)
    if not (10 < log_bound < 11):
        raise AssertionError(log_bound)
    powers = {k: mp.power(base, mp.mpf(1) / k) for k in range(1, 12)}
    if not (powers[11] < 2 < powers[10]):
        raise AssertionError((powers[11], powers[10]))
    total = (powers[10] - 2) / 10
    for k in range(2, 10):
        total += (powers[k] - powers[k + 1]) / k
    total += powers[1] - powers[2]
    if not (mp.mpf(1999) < total < mp.mpf(2000)):
        raise AssertionError(total)
    if int(mp.floor(total)) != 1999:
        raise AssertionError(total)
    _eq(sp.simplify(2 * sp.log(5) + 4 * sp.log(3) - sp.log(2025)), 0)


def check_r2_2025_sg_relay_q16() -> None:
    _check_floor_log()


def _check_cosh_sine() -> None:
    x = sp.symbols("x", real=True)
    left = sp.sin(x) / (sp.cosh(x) + sp.cos(x))
    right = 2 * sp.exp(-x) * sp.sin(x) / (
        1 + 2 * sp.exp(-x) * sp.cos(x) + sp.exp(-2 * x)
    )
    _eq(left, right)
    weight = sp.exp((-1 + sp.I) * x)
    _eq(sp.im(2 * weight / (1 + weight)), right)
    rate = sp.symbols("rate", positive=True)
    _eq(
        sp.integrate(sp.exp(-rate * x) * sp.sin(rate * x) / x, (x, 0, sp.oo)),
        sp.pi / 4,
    )
    ratio = sp.symbols("ratio")
    count = sp.symbols("count", integer=True, positive=True)
    last = sp.symbols("last", integer=True, positive=True)
    partial = sp.summation(((-1) ** (count - 1)) * ratio**count, (count, 1, last))
    _eq(partial * (1 + ratio) - ratio * (1 - (-ratio) ** last), 0)
    approach = sp.symbols("approach", positive=True)
    _eq(sp.limit(sp.pi / 2 * approach / (1 + approach), approach, 1), sp.pi / 4)


def check_r2_2025_sg_relay_q18() -> None:
    _check_cosh_sine()


def check_r2_2025_uk_relay_q09() -> None:
    _check_cosh_sine()


def check_r2_2025_sg_relay_q20() -> None:
    level = sp.symbols("level")
    _eq((2 + level / 2) / (4 + level), sp.Rational(1, 2))
    xx = sp.symbols("xx")
    _eq(sp.expand_func(sp.polylog(1, xx)), -sp.log(1 - xx))
    _eq(sp.expand_func(sp.polylog(1, -xx)), -sp.log(1 + xx))
    _eq(sp.expand_func(sp.polylog(1, xx**2)), -sp.log(1 - xx**2))
    total = sp.polylog(2, xx) + sp.polylog(2, -xx) - sp.polylog(2, xx**2) / 2
    numerator = -sp.log(1 - xx) - sp.log(1 + xx) + sp.log(1 - xx**2)
    _eq(sp.simplify(sp.expand_func(sp.diff(total, xx))), numerator / xx)
    _eq(sp.logcombine(numerator, force=True), 0)
    _eq(total.subs(xx, 0), 0)
    _eq(sp.polylog(2, 1), sp.pi**2 / 6)
    _eq(sp.polylog(2, 0), 0)


def check_r2_2025_sg_relay_q24() -> None:
    t = sp.symbols("t", real=True)
    raw = sp.exp(t) * (sp.exp(t) ** (sp.E / 2 - 1)) * (1 + t) / (sp.exp(t) ** sp.E + 1)
    _eq(raw, (1 + t) / (2 * sp.cosh(sp.E * t / 2)))
    odd = t / sp.cosh(sp.E * t / 2)
    _eq(odd.subs(t, -t) + odd, 0)
    u = sp.symbols("u", real=True)
    _eq(sp.diff(sp.atan(sp.sinh(u)), u), sp.sech(u))
    _eq(
        sp.limit(sp.atan(sp.sinh(u)), u, sp.oo)
        - sp.limit(sp.atan(sp.sinh(u)), u, -sp.oo),
        sp.pi,
    )
    _eq(sp.Rational(1, 2) * (2 / sp.E) * sp.pi, sp.pi / sp.E)


R2_WAVE4_CHECKS = (
    check_r2_2023_group_q09,
    check_r2_2023_group_q10,
    check_r2_2023_relay_q04,
    check_r2_2025_sg_group_q10,
    check_r2_2025_sg_group_q13,
    check_r2_2025_sg_group_q15,
    check_r2_2025_sg_relay_q07,
    check_r2_2025_sg_relay_q08,
    check_r2_2025_sg_relay_q10,
    check_r2_2025_sg_relay_q14,
    check_r2_2025_sg_relay_q16,
    check_r2_2025_sg_relay_q18,
    check_r2_2025_sg_relay_q20,
    check_r2_2025_sg_relay_q24,
    check_r2_2025_uk_group_q10,
    check_r2_2025_uk_relay_q09,
)


if __name__ == "__main__":
    for item in R2_WAVE4_CHECKS:
        item()
        print(f"PASS {item.__name__}", flush=True)
