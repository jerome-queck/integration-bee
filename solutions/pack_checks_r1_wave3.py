"""SymPy checks for the third 2026-10-26 wave of R1 pack notes.

Imported by solutions/pack_checks.py. The catalog is not read.
"""

from __future__ import annotations

import mpmath as mp
import sympy as sp

R1_WAVE3_PACK_IDS = (
    "R1-2020-Q04",
    "R1-2020-Q16",
    "R1-2021-Q10",
    "R1-2021-Q14",
    "R1-2021-Q27",
    "R1-2022-MIT-TB-Q01",
    "R1-2022-MIT-TB-Q02",
    "R1-2022-MIT-TB-Q07",
    "R1-2022-MIT-TB-Q09",
    "R1-2022-MIT-TB-Q11",
    "R1-2022-MIT-TB-Q13",
    "R1-2022-MIT-TB-Q14",
    "R1-2022-MIT-TB-Q15",
    "R1-2022-MIT-TB-Q16",
    "R1-2022-MIT-TB-Q17",
    "R1-2022-MIT-TB-Q18",
    "R1-2022-MIT-TB-Q20",
    "R1-2022-MIT-TB-Q21",
    "R1-2022-MIT-TB-Q22",
    "R1-2022-MIT-TB-Q23",
    "R1-2022-MIT-TB-Q27",
    "R1-2022-MIT-TB-Q29",
    "R1-2022-MIT-TB-Q30",
    "R1-2022-Oxford-Q01",
    "R1-2022-Oxford-Q02",
    "R1-2022-Oxford-Q03",
    "R1-2022-Oxford-Q04",
    "R1-2022-Oxford-Q05",
    "R1-2022-Oxford-Q06",
    "R1-2022-Oxford-Q07",
    "R1-2022-Oxford-Q08",
    "R1-2022-Oxford-Q09",
    "R1-2022-Oxford-Q10",
    "R1-2022-Oxford-Q11",
    "R1-2022-Oxford-Q12",
    "R1-2022-Oxford-Q13",
    "R1-2022-Oxford-Q14",
    "R1-2022-Oxford-Q15",
    "R1-2022-Oxford-Q16",
    "R1-2022-Oxford-Q17",
    "R1-2022-Oxford-Q18",
    "R1-2022-Oxford-Q19",
    "R1-2022-Oxford-Q20",
    "R1-2022-Oxford-Q21",
    "R1-2022-Oxford-Q22",
    "R1-2022-Oxford-Q23",
    "R1-2022-Oxford-Q24",
    "R1-2022-Oxford-Q25",
    "R1-2022-Oxford-Q26",
    "R1-2022-Oxford-Q27",
    "R1-2022-Oxford-Q28",
    "R1-2022-Oxford-Q29",
    "R1-2022-Oxford-Q30",
    "R1-2022-TB2022-Q01",
    "R1-2022-TB2022-Q02",
    "R1-2022-TB2022-Q03",
    "R1-2022-TB2022-Q04",
    "R1-2022-TB2022-Q05",
    "R1-2022-TB2022-Q06",
    "R1-2022-TB2022-Q07",
    "R1-2022-TB2022-Q08",
    "R1-2022-TB2022-Q09",
    "R1-2022-TB2022-Q10",
    "R1-2022-TB2022-Q11",
    "R1-2022-TB2022-Q12",
    "R1-2022-TB2022-Q13",
    "R1-2022-TB2022-Q14",
    "R1-2022-TB2022-Q15",
    "R1-2022-TB2022-Q16",
    "R1-2022-TB2022-Q17",
    "R1-2022-TB2022-Q18",
    "R1-2022-TB2022-Q19",
    "R1-2022-TB2022-Q20",
    "R1-2025-Online-Q07",
    "R1-2025-Online-Q08",
    "R1-2025-Online-Q10",
    "R1-2025-Online-Q12",
    "R1-2025-Online-Q13",
    "R1-2025-Online-Q19",
    "R1-2025-Online-Q22",
    "R1-2025-Online-Q23",
    "R1-2025-Online-Q24",
    "R1-2025-Online-Q25",
    "R1-2025-Online-Q27",
    "R1-2025-Online-Q28",
    "R1-2025-Online-Q29",
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


def _reflection_one() -> None:
    x = sp.symbols("x", real=True)
    f = sp.cos(x) / (1 + sp.exp(x))
    _eq(sp.simplify(f + f.subs(x, -x) - sp.cos(x)), 0)
    _eq(sp.integrate(sp.cos(x), (x, -sp.pi / 2, sp.pi / 2)), 2)
    if sp.simplify(sp.sin(1) - 1) == 0:
        raise AssertionError("sin(1) collapsed to 1")


def _nested_radical() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    tail = sp.summation(1 / sp.factorial(n), (n, 2, sp.oo))
    _eq(tail, sp.E - 2)
    x = sp.symbols("x", positive=True)
    _eq(sp.diff(x ** (sp.E - 1) / (sp.E - 1), x), x ** (sp.E - 2))


def _power_one_over_log() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(sp.exp(sp.log(x) / sp.log(x))), sp.E)
    _eq(sp.integrate(sp.E, (x, 0, 1)), sp.E)


def _exp_exp() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.diff(sp.exp(sp.exp(x)), x), sp.exp(x + sp.exp(x)))


def _log_ratio() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(sp.log((1 + x) / (1 - x)), (x, 0, 1)), sp.log(4))


def _logistic() -> None:
    a, x = sp.symbols("a x", positive=True)
    _eq(sp.integrate(1 / (1 + sp.exp(a * x)), (x, 0, sp.oo)), sp.log(2) / a)


def _quarter_after_exp() -> None:
    u = sp.symbols("u", positive=True)
    _eq(sp.integrate(sp.sqrt(1 - u**2), (u, 0, 1)), sp.pi / 4)


def _double_angle_product() -> None:
    x = sp.symbols("x", real=True)
    n = 6
    prod = sp.Integer(1)
    for i in range(1, n + 1):
        prod *= sp.cos(x / 2**i)
    _eq(sp.trigsimp(sp.expand(2**n * sp.sin(x / 2**n) * prod - sp.sin(x))), 0)
    _eq(sp.integrate(sp.sin(x), (x, 0, sp.pi / 2)), 1)


def _full_period_cancel() -> None:
    x, t = sp.symbols("x t", real=True)
    f = sp.sin(sp.sin(x) - x)
    _eq(sp.trigsimp(f.subs(x, sp.pi + t) + f.subs(x, sp.pi - t)), 0)


def _tan_any_power() -> None:
    x = sp.symbols("x", real=True)
    t = sp.symbols("t", positive=True)
    f = 1 / (t + 1)
    reflected = 1 / (1 / t + 1)
    _eq(sp.simplify(f + reflected - 1), 0)
    _eq(sp.simplify(sp.cot(x) - 1 / sp.tan(x)), 0)
    _eq(sp.integrate(sp.Rational(1, 2), (x, 0, sp.pi / 2)), sp.pi / 4)


def _sqrt_ratio() -> None:
    x = sp.symbols("x")
    _eq(sp.integrate(sp.sqrt((1 + x) / (1 - x)), (x, 0, 1)), 1 + sp.pi / 2)


def _arctan_over_sqrt() -> None:
    z = sp.symbols("z", positive=True)
    _eq(sp.diff(sp.atan(z) + sp.atan(1 / z), z), 0)
    _eq(sp.atan(1) + sp.atan(1), sp.pi / 2)
    th = sp.symbols("th", real=True)
    _eq(sp.simplify(sp.tan(sp.pi / 2 - th) ** 2 - 1 / sp.tan(th) ** 2), 0)
    _eq(2 * (sp.pi / 2) * (sp.pi / 2) / 2, sp.pi**2 / 4)


def _arctan_plus_arccot() -> None:
    x = sp.symbols("x", positive=True)
    pair = sp.atan(x) + sp.acot(x)
    _eq(sp.diff(pair, x), 0)
    _eq(pair.subs(x, 1), sp.pi / 2)
    _eq(sp.integrate((sp.pi / 2) / x, (x, 1, sp.sqrt(3))), sp.pi * sp.log(3) / 4)


def _ln_two_x() -> None:
    x = sp.symbols("x", positive=True)
    anti = sp.log(x) + sp.log(2) * sp.log(sp.log(x))
    _eq(sp.diff(anti, x), (sp.log(2) + sp.log(x)) / (x * sp.log(x)))
    _eq(sp.log(2 * x) - (sp.log(2) + sp.log(x)), 0)


def _gauss_moment() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    moment = sp.gamma(n + sp.Rational(1, 2)) / 2
    printed = sp.factorial(2 * n) * sp.sqrt(sp.pi) / (4**n * sp.factorial(n) * 2)
    _eq(moment, printed)


def _three_halves() -> None:
    left = sp.gamma(sp.Rational(7, 2)) * sp.gamma(sp.Rational(5, 2)) / sp.gamma(6) * 2
    _eq(left, 3 * sp.pi / 128)


def _sqrt_log() -> None:
    u = sp.symbols("u", positive=True)
    _eq(sp.integrate(sp.sqrt(u) * sp.exp(-u), (u, 0, sp.oo)), sp.sqrt(sp.pi) / 2)


def _dutis_atan() -> None:
    b, u = sp.symbols("b u", positive=True)
    deriv = sp.integrate(1 / ((b**2 + 1) * u**2 + 1), (u, 0, sp.oo))
    _eq(deriv, sp.pi / (2 * sp.sqrt(b**2 + 1)))
    _eq(sp.diff(sp.pi * sp.asinh(b) / 2, b), sp.pi / (2 * sp.sqrt(b**2 + 1)))
    x = sp.symbols("x", real=True)
    left = 1 / (1 + b**2 * sp.sin(x) ** 2)
    right = sp.sec(x) ** 2 / ((b**2 + 1) * sp.tan(x) ** 2 + 1)
    _eq(sp.simplify(left - right), 0)


def _alternating_basel() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    _eq(sp.summation((-1) ** (n - 1) / n**2, (n, 1, sp.oo)), sp.pi**2 / 12)


def _zeta_three() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    x = sp.symbols("x", positive=True)
    term = sp.integrate(x**2 * sp.exp(-k * x), (x, 0, sp.oo))
    _eq(term, 2 / k**3)
    _eq(sp.summation(2 / k**3, (k, 1, sp.oo)), 2 * sp.zeta(3))


def _log_over_quadratic() -> None:
    th = sp.symbols("th", real=True)
    expr = sp.log(1 + sp.tan(th) ** 2) + 2 * sp.log(sp.cos(th))
    _eq(sp.simplify(sp.logcombine(expr, force=True)), 0)
    mp.mp.dps = 20
    got = mp.quad(lambda t: mp.log(mp.sin(t)), [0, mp.pi / 2])
    _near(got, -(mp.pi / 2) * mp.log(2), mp.mpf("1e-10"))


def _rational_quartic() -> None:
    x = sp.symbols("x", positive=True)
    anti = sp.atan((x - 1 / x) / sp.sqrt(2)) / sp.sqrt(2)
    _eq(sp.diff(anti, x), (x**2 + 1) / (x**4 + 1))


def _dirichlet_exp() -> None:
    a, x = sp.symbols("a x", positive=True)
    laplace = sp.integrate(sp.exp(-x) * sp.cos(a * x), (x, 0, sp.oo))
    _eq(laplace, 1 / (1 + a**2))
    _eq(sp.diff(sp.atan(a), a), 1 / (1 + a**2))
    _eq(sp.atan(0), 0)


def _log_sin_log() -> None:
    u = sp.symbols("u", positive=True)
    _eq(sp.integrate(u * sp.exp(-u) * sp.sin(u), (u, 0, sp.oo)), sp.Rational(1, 2))


def _log_tan_square() -> None:
    mp.mp.dps = 20

    def integrand(t):
        if t == 0 or t == mp.pi / 2:
            return mp.mpf(0)
        return mp.log(mp.tan(t)) ** 2

    got = mp.quad(integrand, [0, mp.pi / 2])
    _near(got, mp.pi**3 / 8, mp.mpf("1e-8"))


def _cos_over_cosh() -> None:
    mp.mp.dps = 20
    got = mp.quad(lambda t: mp.cos(t) / mp.cosh(t), [-mp.inf, mp.inf])
    _near(got, mp.pi / mp.cosh(mp.pi / 2), mp.mpf("1e-10"))


def _cos_over_double() -> None:
    u = sp.symbols("u", real=True)
    _eq(sp.integrate(1 / (1 + u**2), (u, -1, 1)), sp.pi / 2)
    x = sp.symbols("x", real=True)
    u_expr = sp.sin(x) - sp.cos(x)
    _eq(sp.simplify(1 + u_expr**2 - (2 - sp.sin(2 * x))), 0)
    _eq(sp.diff(u_expr, x), sp.cos(x) + sp.sin(x))


def _sophomore_slice() -> None:
    x, s = sp.symbols("x s", positive=True)
    got = sp.integrate(x**s, (s, 0, 1))
    manual = (x - 1) / sp.log(x)
    _eq(got.args[0][0], manual)
    _eq(got.args[1][0], 1)
    _eq(sp.limit(manual, x, 1), 1)
    mp.mp.dps = 20

    def integrand(t):
        if t == 0 or t == 1:
            return mp.mpf(0)
        return (t - 1) / ((t + 1) * mp.log(t))

    got = mp.quad(integrand, [0, 1])
    _near(got, mp.log(mp.pi / 2), mp.mpf("1e-10"))


def _sec_log() -> None:
    a, t = sp.symbols("a t", positive=True)
    kernel = 2 / ((1 + a) + (1 - a) * t**2)
    anti = 2 / sp.sqrt(1 - a**2) * sp.atan(t * sp.sqrt((1 - a) / (1 + a)))
    _eq(sp.diff(anti, t), kernel)
    _eq(sp.limit(sp.atan(t), t, sp.oo), sp.pi / 2)
    _eq(2 / sp.sqrt(1 - a**2) * sp.pi / 2, sp.pi / sp.sqrt(1 - a**2))
    _eq(sp.diff(sp.pi * sp.asin(a), a), sp.pi / sp.sqrt(1 - a**2))
    _eq((sp.pi * sp.asin(a)).subs(a, sp.Rational(1, 3)), sp.pi * sp.asin(sp.Rational(1, 3)))


def _sin_minus_log() -> None:
    w = sp.symbols("w", positive=True)
    second = 1 / w**2 - 1 / (w**2 + 1)
    antideriv = -1 / w - sp.atan(w)
    _eq(sp.diff(antideriv, w), second)
    # J'(s) = pi/2 - 1/s - atan(s), and J(1) is the integral of -J' from 1 to infinity.
    capital = w * sp.atan(w) - sp.log(1 + w**2) / 2 - sp.pi * w / 2 + sp.log(w)
    value = sp.limit(capital, w, sp.oo) - capital.subs(w, 1)
    _eq(value, sp.log(2) / 2 + sp.pi / 4 - 1)


def _frullani_cosine() -> None:
    a, c, x = sp.symbols("a c x", positive=True)
    one = sp.integrate(sp.exp(-a * x) * sp.cos(c * x), (x, 0, sp.oo))
    _eq(one, a / (a**2 + c**2))
    antideriv = sp.log(a**2 + sp.E**2) / 2 - sp.log(a**2 + sp.pi**2) / 2
    _eq(sp.diff(antideriv, a), a / (a**2 + sp.E**2) - a / (a**2 + sp.pi**2))
    _eq(antideriv.subs(a, 0), sp.log(sp.E / sp.pi))
    _eq(sp.Rational(1, 2) * sp.log(sp.E**2 / sp.pi**2), sp.log(sp.E / sp.pi))


def _parameter_arcsine() -> None:
    k, t = sp.symbols("k t", positive=True)
    kernel = 2 / ((1 + k) + (1 - k) * t**2)
    anti = 2 / sp.sqrt(1 - k**2) * sp.atan(t * sp.sqrt((1 - k) / (1 + k)))
    _eq(sp.diff(anti, t), kernel)
    _eq(2 / sp.sqrt(1 - k**2) * sp.pi / 2, sp.pi / sp.sqrt(1 - k**2))
    _eq(sp.diff(sp.pi * sp.asin(k), k), sp.pi / sp.sqrt(1 - k**2))


def _catalan_series() -> None:
    n = sp.symbols("n", integer=True, nonnegative=True)
    _eq(sp.summation((-1) ** n / (2 * n + 1), (n, 0, sp.oo)), sp.pi / 4)
    _eq(sp.summation((-1) ** n / (2 * n + 1) ** 2, (n, 0, sp.oo)), sp.Catalan)
    _eq(sp.summation(1 / (2 * n + 1) ** 2, (n, 0, sp.oo)), sp.pi**2 / 8)
    piece = sp.pi * sp.I * sp.pi / 4 + 2 * sp.Catalan - 2 * sp.I * sp.pi**2 / 8
    _eq(sp.expand(piece), 2 * sp.Catalan)


def _log_quadratic_form() -> None:
    alpha, beta, x = sp.symbols("alpha beta x", positive=True)
    expanded = alpha * sp.sin(x) ** 2 + beta * sp.cos(x) ** 2
    rewritten = (alpha + beta) / 2 + (beta - alpha) / 2 * sp.cos(2 * x)
    _eq(sp.trigsimp(sp.expand(expanded - rewritten)), 0)
    p = (alpha + beta) / 2
    q = (beta - alpha) / 2
    disc = sp.simplify(p**2 - q**2)
    _eq(disc, alpha * beta)
    closed = (p + sp.sqrt(disc)) / 2
    _eq(sp.simplify(closed - (sp.sqrt(alpha) + sp.sqrt(beta)) ** 2 / 4), 0)
    mp.mp.dps = 20

    def integrand(t):
        return mp.log(7997 * mp.sin(t) ** 2 + 7945 * mp.cos(t) ** 2)

    got = mp.quad(integrand, [0, mp.pi / 2])
    target = mp.pi * mp.log((mp.sqrt(7997) + mp.sqrt(7945)) / 2)
    _near(got, target, mp.mpf("1e-10"))


def _fourier_cosine() -> None:
    a, b, x = sp.symbols("a b x", positive=True)
    got = sp.integrate(sp.cos(a * x) / (x**2 + b**2), (x, 0, sp.oo))
    _eq(got, sp.pi * sp.exp(-a * b) / (2 * b))


def _minus_basel() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    _eq(sp.summation(1 / n**2, (n, 1, sp.oo)), sp.pi**2 / 6)
    _eq(-sp.pi**2 / 6, -sp.pi**2 / 6)


def _three_to_cos() -> None:
    x = sp.symbols("x", real=True)
    z = sp.symbols("z", positive=True)
    _eq(sp.simplify(3 ** sp.cos(x) * 3 ** (-sp.cos(x))), 1)
    _eq(sp.diff(sp.atan(z) + sp.atan(1 / z), z), 0)
    _eq(sp.atan(1) + sp.atan(1), sp.pi / 2)
    _eq(sp.integrate(sp.pi / 2, (x, 0, sp.pi)) / 2, sp.pi**2 / 4)


def _half_angle_sqrt() -> None:
    x = sp.symbols("x", real=True)
    _eq(sp.trigsimp((sp.sin(x / 4) + sp.cos(x / 4)) ** 2 - (1 + sp.sin(x / 2))), 0)
    _eq(sp.diff(4 * (sp.sin(x / 4) - sp.cos(x / 4)), x), sp.sin(x / 4) + sp.cos(x / 4))


def _product_logs() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    x = sp.symbols("x", positive=True)
    _eq(sp.integrate(x**n * sp.log(x), (x, 0, 1)), -1 / (n + 1) ** 2)
    term = 1 / (n * (n + 1) ** 2)
    partial = 1 / n - 1 / (n + 1) - 1 / (n + 1) ** 2
    _eq(sp.together(term - partial), 0)
    _eq(sp.summation(partial, (n, 1, sp.oo)), 2 - sp.pi**2 / 6)


def _truncated_exp() -> None:
    n, k, x = sp.symbols("n k x", positive=True)
    u = sp.Sum(x**k / sp.factorial(k), (k, 0, n))
    # The derivative identity is checked on a concrete degree and the general term.
    degree = 4
    poly = sum(x**k / sp.factorial(k) for k in range(degree + 1))
    _eq(sp.diff(poly, x), poly - x**degree / sp.factorial(degree))
    anti = sp.factorial(degree) * x - sp.factorial(degree) * sp.log(poly)
    integrand = x**degree / poly
    _eq(sp.simplify(sp.diff(anti, x) - integrand), 0)


def _odd_semicircle() -> None:
    x = sp.symbols("x", real=True)
    odd = x**3 * sp.cos(x / 2) * sp.sqrt(4 - x**2)
    _eq(sp.simplify(odd.subs(x, -x) + odd), 0)
    _eq(sp.integrate(sp.sqrt(4 - x**2), (x, -2, 2)) / 2, sp.pi)


def _floor_geometric() -> None:
    n = sp.symbols("n", integer=True, positive=True)
    r = sp.exp(-1)
    _eq(sp.summation(n * r**n, (n, 1, sp.oo)) * (1 - r), 1 / (sp.E - 1))
    _eq(sp.summation(n * r**n, (n, 1, sp.oo)), r / (1 - r) ** 2)


def _x5_over_log() -> None:
    p = sp.symbols("p", positive=True)
    x = sp.symbols("x", positive=True)
    _eq(sp.diff(sp.integrate(x**p, (x, 0, 1)), p), sp.integrate(x**p * sp.log(x), (x, 0, 1)))
    _eq(sp.diff(sp.log(p + 1), p), 1 / (p + 1))
    _eq(sp.log(6), sp.log(6))
    # d/dp of the integral of (x^p-1)/log x equals 1/(p+1), and the value at 0 is 0.
    _eq(sp.integrate(x**5, (x, 0, 1)) - sp.integrate(1, (x, 0, 1)), sp.Rational(1, 6) - 1)


def _wallis_power() -> None:
    m = 1011
    wallis = sp.pi / 2 * sp.binomial(2 * m, m) / 4**m
    _eq(4 * wallis, sp.pi * sp.binomial(2022, 1011) / 2**2021)


def _constant_log() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(sp.log(x**2) - 2 * sp.log(2 * x)), -2 * sp.log(2))
    _eq(sp.diff(-2 * x * sp.log(2), x), -2 * sp.log(2))


def _log_log_square() -> None:
    x = sp.symbols("x", positive=True)
    anti = sp.log(sp.log(x)) ** 2 / 2
    _eq(sp.diff(anti, x), sp.log(sp.log(x)) / (x * sp.log(x)))


def _reciprocal_square() -> None:
    x = sp.symbols("x", positive=True)
    integrand = 1 / (x + 1 / x) ** 2
    split = x**2 / (x**2 + 1) ** 2
    _eq(sp.simplify(integrand - split), 0)
    _eq(sp.integrate(split, (x, 0, sp.oo)), sp.pi / 4)


def _quarter_circle() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(sp.sin(sp.acos(x)) - sp.sqrt(1 - x**2)), 0)
    _eq(sp.integrate(sp.sqrt(1 - x**2), (x, 0, 1)), sp.pi / 4)


def _nested_exp() -> None:
    x = sp.symbols("x")
    value = 1
    for k in range(6, 0, -1):
        value = 1 - (x / k) * value
    partial = sum(((-x) ** k) / sp.factorial(k) for k in range(7))
    _eq(sp.expand(value - partial), 0)
    t = sp.symbols("t", positive=True)
    _eq(sp.integrate(sp.exp(-t), (t, 0, sp.oo)), 1)


def _alternating_harmonic() -> None:
    x = sp.symbols("x", positive=True)
    _eq(sp.simplify(x**2 - (x**3 - x**4) - (x**2 - x**3 + x**4)), 0)
    _eq(sp.factor(x**2 - x**3 + x**4), x**2 * (1 - x + x**2))
    k = sp.symbols("k", integer=True, positive=True)
    series = sp.summation((-1) ** (k + 1) / (k + 1), (k, 1, sp.oo))
    _eq(series, 1 - sp.log(2))


def _octahedron() -> None:
    a, b, c = sp.symbols("a b c", nonnegative=True)
    _eq(sp.expand((a + b + c) ** 2 - (a**2 + b**2 + c**2)), 2 * (a * b + b * c + c * a))
    x, y, z = sp.symbols("x y z", nonnegative=True)
    octant = sp.integrate(1, (z, 0, 1 - x - y), (y, 0, 1 - x), (x, 0, 1))
    _eq(8 * octant, sp.Rational(4, 3))


def _cancel_radicals() -> None:
    x = sp.symbols("x", positive=True)
    s = sp.sqrt(1 + 4 * x)
    z = (1 + s) / 2
    y = (-1 + s) / 2
    _eq(sp.simplify(z**2 - (x + z)), 0)
    _eq(sp.simplify(y**2 - (x - y)), 0)
    _eq(sp.simplify(x / z - y), 0)


def _frullani_two() -> None:
    x = sp.symbols("x", positive=True)
    f = lambda t: t**2 / (2**t - 1) ** 2
    original = x / (2**x - 1) ** 2 - 4 * x / (4**x - 1) ** 2
    _eq(sp.simplify(original - (f(x) - f(2 * x)) / x), 0)
    _eq(sp.limit(f(x), x, 0), 1 / sp.log(2) ** 2)
    _eq(sp.limit(f(x), x, sp.oo), 0)
    _eq((1 / sp.log(2) ** 2) * sp.log(2), 1 / sp.log(2))


def _inverse_pair() -> None:
    x = sp.symbols("x", positive=True)
    f = sp.sqrt(sp.log(x))
    _eq(sp.simplify(sp.exp(f**2) - x), 0)
    upper = sp.symbols("b", positive=True)
    product = upper * sp.sqrt(sp.log(upper))
    second = sp.exp(sp.log(upper)) * sp.diff(sp.sqrt(sp.log(upper)), upper)
    _eq(sp.simplify(sp.diff(product, upper) - (sp.sqrt(sp.log(upper)) + second)), 0)
    e = sp.E
    y = (x - 1) / (e - 1)
    _eq(sp.simplify(sp.diff(y, x) * (e - 1) - 1), 0)
    _eq(e * 1 - 1 * 0, e)


def _frullani_zero() -> None:
    x = sp.symbols("x", positive=True)
    num = x**2 + 2 ** (-x / 6) / 7 - 2 ** (-x / 7) / 6
    den = (2 ** (-x / 7) + 36 * x**2) * (2 ** (-x / 6) + 49 * x**2)
    f = lambda t: (t / 42) / (2 ** (-t / 42) + t**2)
    split = (f(6 * x) - f(7 * x)) / x
    _eq(sp.simplify(num / den - split), 0)
    t = sp.symbols("t", positive=True)
    _eq(sp.limit(f(t), t, 0), 0)
    _eq(sp.limit(f(t) * t, t, sp.oo), sp.Rational(1, 42))


def _collapse_radical() -> None:
    x, n = sp.symbols("x n", real=True)
    _eq(sp.expand((x + n + 1) ** 2 - (1 + (x + n) * (x + n + 2))), 0)
    t = sp.symbols("t", real=True)
    _eq(sp.integrate(t + 1, (t, 0, 25)), sp.Rational(675, 2))


def _surd_antiderivative() -> None:
    u = sp.symbols("u", positive=True)
    piece = 1 / (u**2 * (u + 1))
    parts = -1 / u + 1 / u**2 + 1 / (u + 1)
    _eq(sp.together(piece - parts), 0)
    _eq(sp.simplify(sp.diff(sp.log(1 + 1 / u) - 1 / u, u) - parts), 0)
    r = (1 + sp.sqrt(3)) / 2
    _eq(sp.simplify(r**2 - (2 + sp.sqrt(3)) / 2), 0)
    _eq(sp.simplify(1 / r - (sp.sqrt(3) - 1)), 0)
    _eq(sp.simplify(sp.log(r) + sp.log(sp.sqrt(3) - 1)), 0)


def _root_distance() -> None:
    a, x = sp.symbols("a x")
    cubic = x**3 - (3 + a) * x**2 + (4 + 2 * a) * x - (2 + a)
    quot, rem = sp.div(cubic, x - 1, domain=sp.QQ.frac_field(a))
    _eq(rem, 0)
    s = sp.sqrt(a**2 - 4)
    smaller = (2 + a - s) / 2
    larger = (2 + a + s) / 2
    _eq(sp.simplify(sp.together(quot.subs(x, smaller))), 0)
    _eq(sp.simplify(smaller - 1 - (a - s) / 2), 0)
    _eq(sp.simplify(1 - larger.subs(a, -a) - (a - s) / 2), 0)
    threshold = 3 / sp.sqrt(2)
    _eq(sp.simplify(((a - s) / 2 - s).subs(a, threshold)), 0)

    def capital(val):
        return val * sp.sqrt(val**2 - 4) / 2 - 2 * sp.log(val + sp.sqrt(val**2 - 4))

    expr = -capital(90) + 3 * capital(threshold) - 2 * capital(2) + sp.Rational(16191, 4)
    target = 90 * (45 - sp.sqrt(2024)) - 2 * sp.log(45 - sp.sqrt(2024)) - 3 * sp.log(2)
    gap = sp.simplify(sp.expand_log(sp.expand(expr - target), force=True))
    low = 45 - 2 * sp.sqrt(506)
    high = 45 + 2 * sp.sqrt(506)
    _eq(sp.expand(low * high), 1)
    _eq(sp.simplify(gap - 2 * sp.log(low) - 2 * sp.log(high)), 0)
    _eq(sp.simplify(sp.logcombine(2 * sp.log(low) + 2 * sp.log(high), force=True)), 0)
    _eq((90**2 - threshold**2) / 2, sp.Rational(16191, 4))


def _implicit_cube() -> None:
    f, x = sp.symbols("f x", positive=True)
    _eq(sp.simplify((3 * f**3 + x * f) - (2 * f**3 + 125) - (f**3 + x * f - 125)), 0)
    _eq(5**3, 125)
    _eq(1**3 + 124 * 1, 125)
    anti = f**4 / 2 + 125 * f
    _eq(anti.subs(f, 5) - anti.subs(f, 1), 812)


def check_r1_2020_q04() -> None:
    _frullani_cosine()


def check_r1_2020_q16() -> None:
    _parameter_arcsine()


def check_r1_2021_q10() -> None:
    _catalan_series()


def check_r1_2021_q14() -> None:
    _log_quadratic_form()


def check_r1_2021_q27() -> None:
    _fourier_cosine()


def check_r1_2022_mit_tb_q01() -> None:
    _reflection_one()


def check_r1_2022_mit_tb_q02() -> None:
    _nested_radical()


def check_r1_2022_mit_tb_q07() -> None:
    _full_period_cancel()


def check_r1_2022_mit_tb_q09() -> None:
    _arctan_over_sqrt()


def check_r1_2022_mit_tb_q11() -> None:
    _ln_two_x()


def check_r1_2022_mit_tb_q13() -> None:
    _minus_basel()
    n = sp.symbols("n", integer=True, positive=True)
    _eq(sp.summation(-1 / n**2, (n, 1, sp.oo)), -sp.pi**2 / 6)


def check_r1_2022_mit_tb_q14() -> None:
    _three_to_cos()


def check_r1_2022_mit_tb_q15() -> None:
    _half_angle_sqrt()


def check_r1_2022_mit_tb_q16() -> None:
    _product_logs()


def check_r1_2022_mit_tb_q17() -> None:
    _truncated_exp()


def check_r1_2022_mit_tb_q18() -> None:
    _odd_semicircle()


def check_r1_2022_mit_tb_q20() -> None:
    _floor_geometric()


def check_r1_2022_mit_tb_q21() -> None:
    _x5_over_log()
    p = sp.symbols("p", positive=True)
    _eq(sp.integrate(sp.diff(sp.log(p + 1), p), (p, 0, 5)), sp.log(6))


def check_r1_2022_mit_tb_q22() -> None:
    _wallis_power()


def check_r1_2022_mit_tb_q23() -> None:
    _constant_log()


def check_r1_2022_mit_tb_q27() -> None:
    _log_log_square()


def check_r1_2022_mit_tb_q29() -> None:
    _reciprocal_square()


def check_r1_2022_mit_tb_q30() -> None:
    _quarter_circle()


def check_r1_2022_oxford_q01() -> None:
    _reflection_one()


def check_r1_2022_oxford_q02() -> None:
    _nested_radical()


def check_r1_2022_oxford_q03() -> None:
    _power_one_over_log()


def check_r1_2022_oxford_q04() -> None:
    _exp_exp()


def check_r1_2022_oxford_q05() -> None:
    _log_ratio()


def check_r1_2022_oxford_q06() -> None:
    _logistic()


def check_r1_2022_oxford_q07() -> None:
    _quarter_after_exp()


def check_r1_2022_oxford_q08() -> None:
    _double_angle_product()


def check_r1_2022_oxford_q09() -> None:
    _full_period_cancel()


def check_r1_2022_oxford_q10() -> None:
    _tan_any_power()


def check_r1_2022_oxford_q11() -> None:
    _sqrt_ratio()


def check_r1_2022_oxford_q12() -> None:
    _arctan_over_sqrt()


def check_r1_2022_oxford_q13() -> None:
    _arctan_plus_arccot()


def check_r1_2022_oxford_q14() -> None:
    _ln_two_x()


def check_r1_2022_oxford_q15() -> None:
    _gauss_moment()


def check_r1_2022_oxford_q16() -> None:
    _three_halves()


def check_r1_2022_oxford_q17() -> None:
    _sqrt_log()


def check_r1_2022_oxford_q18() -> None:
    _dutis_atan()


def check_r1_2022_oxford_q19() -> None:
    _alternating_basel()


def check_r1_2022_oxford_q20() -> None:
    _zeta_three()


def check_r1_2022_oxford_q21() -> None:
    _log_over_quadratic()


def check_r1_2022_oxford_q22() -> None:
    _rational_quartic()


def check_r1_2022_oxford_q23() -> None:
    _dirichlet_exp()


def check_r1_2022_oxford_q24() -> None:
    _log_sin_log()


def check_r1_2022_oxford_q25() -> None:
    _log_tan_square()


def check_r1_2022_oxford_q26() -> None:
    _cos_over_cosh()


def check_r1_2022_oxford_q27() -> None:
    _cos_over_double()


def check_r1_2022_oxford_q28() -> None:
    _sophomore_slice()


def check_r1_2022_oxford_q29() -> None:
    _sec_log()


def check_r1_2022_oxford_q30() -> None:
    _sin_minus_log()


def check_r1_2022_tb2022_q01() -> None:
    _reflection_one()


def check_r1_2022_tb2022_q02() -> None:
    _nested_radical()


def check_r1_2022_tb2022_q03() -> None:
    _power_one_over_log()


def check_r1_2022_tb2022_q04() -> None:
    _exp_exp()


def check_r1_2022_tb2022_q05() -> None:
    _log_ratio()


def check_r1_2022_tb2022_q06() -> None:
    _logistic()


def check_r1_2022_tb2022_q07() -> None:
    _full_period_cancel()


def check_r1_2022_tb2022_q08() -> None:
    _tan_any_power()


def check_r1_2022_tb2022_q09() -> None:
    _arctan_over_sqrt()


def check_r1_2022_tb2022_q10() -> None:
    _arctan_plus_arccot()


def check_r1_2022_tb2022_q11() -> None:
    _ln_two_x()


def check_r1_2022_tb2022_q12() -> None:
    _gauss_moment()


def check_r1_2022_tb2022_q13() -> None:
    _sqrt_log()


def check_r1_2022_tb2022_q14() -> None:
    _alternating_basel()


def check_r1_2022_tb2022_q15() -> None:
    _zeta_three()


def check_r1_2022_tb2022_q16() -> None:
    _log_over_quadratic()


def check_r1_2022_tb2022_q17() -> None:
    _dirichlet_exp()


def check_r1_2022_tb2022_q18() -> None:
    _log_sin_log()


def check_r1_2022_tb2022_q19() -> None:
    _log_tan_square()


def check_r1_2022_tb2022_q20() -> None:
    _cos_over_double()


def check_r1_2025_online_q07() -> None:
    x = sp.symbols("x")
    k = sp.symbols("k", integer=True)
    powers = sp.summation(x**k, (k, 0, 2025)) - sp.summation(x**k, (k, 1, 2025))
    _eq(sp.simplify(powers), 1)
    _eq(sp.integrate(1, (x, 0, 1)), 1)
    for n in range(1, 6):
        value = sp.Rational(1, 2) ** n
        _eq(sp.frac(value), value)


def check_r1_2025_online_q08() -> None:
    _nested_exp()


def check_r1_2025_online_q10() -> None:
    _dutis_atan()


def check_r1_2025_online_q12() -> None:
    _alternating_harmonic()


def check_r1_2025_online_q13() -> None:
    _octahedron()


def check_r1_2025_online_q19() -> None:
    _cancel_radicals()


def check_r1_2025_online_q22() -> None:
    _frullani_two()


def check_r1_2025_online_q23() -> None:
    _inverse_pair()


def check_r1_2025_online_q24() -> None:
    _frullani_zero()


def check_r1_2025_online_q25() -> None:
    _collapse_radical()


def check_r1_2025_online_q27() -> None:
    _surd_antiderivative()


def check_r1_2025_online_q28() -> None:
    _root_distance()


def check_r1_2025_online_q29() -> None:
    _implicit_cube()


R1_WAVE3_CHECKS = (
    check_r1_2020_q04,
    check_r1_2020_q16,
    check_r1_2021_q10,
    check_r1_2021_q14,
    check_r1_2021_q27,
    check_r1_2022_mit_tb_q01,
    check_r1_2022_mit_tb_q02,
    check_r1_2022_mit_tb_q07,
    check_r1_2022_mit_tb_q09,
    check_r1_2022_mit_tb_q11,
    check_r1_2022_mit_tb_q13,
    check_r1_2022_mit_tb_q14,
    check_r1_2022_mit_tb_q15,
    check_r1_2022_mit_tb_q16,
    check_r1_2022_mit_tb_q17,
    check_r1_2022_mit_tb_q18,
    check_r1_2022_mit_tb_q20,
    check_r1_2022_mit_tb_q21,
    check_r1_2022_mit_tb_q22,
    check_r1_2022_mit_tb_q23,
    check_r1_2022_mit_tb_q27,
    check_r1_2022_mit_tb_q29,
    check_r1_2022_mit_tb_q30,
    check_r1_2022_oxford_q01,
    check_r1_2022_oxford_q02,
    check_r1_2022_oxford_q03,
    check_r1_2022_oxford_q04,
    check_r1_2022_oxford_q05,
    check_r1_2022_oxford_q06,
    check_r1_2022_oxford_q07,
    check_r1_2022_oxford_q08,
    check_r1_2022_oxford_q09,
    check_r1_2022_oxford_q10,
    check_r1_2022_oxford_q11,
    check_r1_2022_oxford_q12,
    check_r1_2022_oxford_q13,
    check_r1_2022_oxford_q14,
    check_r1_2022_oxford_q15,
    check_r1_2022_oxford_q16,
    check_r1_2022_oxford_q17,
    check_r1_2022_oxford_q18,
    check_r1_2022_oxford_q19,
    check_r1_2022_oxford_q20,
    check_r1_2022_oxford_q21,
    check_r1_2022_oxford_q22,
    check_r1_2022_oxford_q23,
    check_r1_2022_oxford_q24,
    check_r1_2022_oxford_q25,
    check_r1_2022_oxford_q26,
    check_r1_2022_oxford_q27,
    check_r1_2022_oxford_q28,
    check_r1_2022_oxford_q29,
    check_r1_2022_oxford_q30,
    check_r1_2022_tb2022_q01,
    check_r1_2022_tb2022_q02,
    check_r1_2022_tb2022_q03,
    check_r1_2022_tb2022_q04,
    check_r1_2022_tb2022_q05,
    check_r1_2022_tb2022_q06,
    check_r1_2022_tb2022_q07,
    check_r1_2022_tb2022_q08,
    check_r1_2022_tb2022_q09,
    check_r1_2022_tb2022_q10,
    check_r1_2022_tb2022_q11,
    check_r1_2022_tb2022_q12,
    check_r1_2022_tb2022_q13,
    check_r1_2022_tb2022_q14,
    check_r1_2022_tb2022_q15,
    check_r1_2022_tb2022_q16,
    check_r1_2022_tb2022_q17,
    check_r1_2022_tb2022_q18,
    check_r1_2022_tb2022_q19,
    check_r1_2022_tb2022_q20,
    check_r1_2025_online_q07,
    check_r1_2025_online_q08,
    check_r1_2025_online_q10,
    check_r1_2025_online_q12,
    check_r1_2025_online_q13,
    check_r1_2025_online_q19,
    check_r1_2025_online_q22,
    check_r1_2025_online_q23,
    check_r1_2025_online_q24,
    check_r1_2025_online_q25,
    check_r1_2025_online_q27,
    check_r1_2025_online_q28,
    check_r1_2025_online_q29,
)


if __name__ == "__main__":
    for check in R1_WAVE3_CHECKS:
        check()
        print(f"PASS {check.__name__}", flush=True)
    print(f"PASS {len(R1_WAVE3_PACK_IDS)} wave-3 notes", flush=True)
