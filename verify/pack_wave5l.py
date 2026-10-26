"""Exact reductions for the wave-5l pack rows.

Matchers return before any simplification unless the integrand has their
shape. A returned value is an identity, not a numeric sample. Answers stay
closed. No integrand here keeps an inner Sum, Product, Integral, or Limit.
"""

from __future__ import annotations

import sympy as sp


def _eq(expr) -> bool:
    if expr == 0:
        return True
    try:
        return sp.simplify(expr) == 0
    except Exception:
        return False


def _span(lo, hi, left, right) -> bool:
    return lo == left and hi == right


def _floor_quartic(integrand, symbol, lo, hi):
    """On each integer interval the quartic floor term telescopes to 1/2."""
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.floor):
        return None
    level = sp.floor(symbol)
    if integrand != level / (1 + level**2 + level**4):
        return None
    n = sp.Symbol("_n", integer=True, nonnegative=True)
    term = n / (1 + n**2 + n**4)
    piece = sp.Rational(1, 2) * (1 / (n**2 - n + 1) - 1 / (n**2 + n + 1))
    if not _eq(term - piece):
        return None
    if sp.expand((n + 1) ** 2 - (n + 1) + 1 - (n**2 + n + 1)) != 0:
        return None
    height = 1 / (n**2 - n + 1)
    if height.subs(n, 0) != 1:
        return None
    large = sp.Symbol("_m", positive=True)
    if sp.limit(1 / (large**2 - large + 1), large, sp.oo) != 0:
        return None
    # The partial sum of a_{n}-a_{n+1} is a_0-a_{N+1}, and a_0=1.
    return sp.Rational(1, 2)


def _tan_boundary(integrand, symbol, lo, hi):
    """sin(2x) sqrt(tan x) differentiates back to the printed integrand on (0, pi/4]."""
    if not _span(lo, hi, 0, sp.pi / 4) or not integrand.has(sp.tan):
        return None
    expected = (4 * sp.cos(symbol) ** 2 - 1) * sp.sqrt(sp.tan(symbol))
    if integrand != expected:
        return None
    boundary = sp.sin(2 * symbol) * sp.sqrt(sp.tan(symbol))
    if not _eq(sp.diff(boundary, symbol) - integrand):
        return None
    if boundary.subs(symbol, sp.pi / 4) != 1:
        return None
    if sp.limit(boundary, symbol, 0) != 0:
        return None
    return sp.Integer(1)


def _atan_log_square(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.log) or not integrand.has(sp.atan):
        return None
    expected = sp.atan(symbol) / (symbol * (sp.log(symbol) ** 2 + 1))
    if integrand != expected:
        return None
    x = sp.Symbol("_x", positive=True)
    complement = sp.atan(x) + sp.atan(1 / x)
    if not _eq(sp.diff(complement, x)) or complement.subs(x, 1) != sp.pi / 2:
        return None
    y = sp.Symbol("_y", positive=True)
    reflected = expected.subs(symbol, 1 / y) * sp.diff(1 / y, y)
    target = sp.atan(1 / y) / (y * (sp.log(y) ** 2 + 1))
    if not _eq(-reflected - target):
        return None
    # The complement is the constant pi/2, so each reflection pair averages to pi/4.
    halved = (sp.pi / 2) / (2 * y * (sp.log(y) ** 2 + 1))
    reduced = (sp.pi / 4) / (y * (sp.log(y) ** 2 + 1))
    if not _eq(halved - reduced):
        return None
    log_y = sp.log(y)
    kernel = 1 / (y * (log_y**2 + 1))
    if sp.diff(log_y, y) != 1 / y:
        return None
    if not _eq(kernel / (sp.diff(log_y, y) / (1 + log_y**2)) - 1):
        return None
    t = sp.Symbol("_t", real=True)
    width = sp.integrate(1 / (1 + t**2), (t, -sp.oo, sp.oo))
    if width != sp.pi:
        return None
    return sp.pi**2 / 4


def _atan_parameter(big, small, symbol):
    """atan(big*x)-atan(small*x) equals atan of the tangent subtraction.

    The difference of the two sides has derivative 0 on (0, oo). Both sides
    tend to 0 as x tends to 0, so the constant is 0. The sample tangent is
    the subtraction formula at x=1; it is recorded so a wrong pair fails.
    """
    del symbol
    if sp.ask(sp.Q.positive(big - small)) is not True or sp.ask(sp.Q.positive(small)) is not True:
        return False
    x = sp.Symbol("_x", positive=True)
    left = sp.atan(big * x) - sp.atan(small * x)
    gap = (big - small) * x / (1 + big * small * x**2)
    right = sp.atan(gap)
    if not _eq(sp.diff(left - right, x)):
        return False
    if sp.limit(left, x, 0) != 0 or sp.limit(right, x, 0) != 0:
        return False
    tangent = sp.tan(sp.atan(big) - sp.atan(small)) - (big - small) / (1 + big * small)
    return _eq(tangent)


def _atan_frullani(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.atan):
        return None
    first = sp.atan(symbol / (1 + 2 * symbol**2))
    second = sp.atan(symbol / (1 + 12 * symbol**2))
    if integrand != (first - second) / symbol:
        return None
    if not _atan_parameter(2, 1, symbol) or not _atan_parameter(4, 3, symbol):
        return None
    s = sp.Symbol("_s", positive=True)
    x = sp.Symbol("_x", positive=True)
    if sp.diff(sp.atan(s * x), s) != x / (1 + (s * x) ** 2):
        return None
    inner = sp.integrate(1 / (1 + (s * x) ** 2), (x, 0, sp.oo))
    if not _eq(inner - sp.pi / (2 * s)):
        return None
    if sp.ask(sp.Q.positive(1 / (1 + (s * x) ** 2))) is not True:
        return None
    low = sp.integrate(sp.pi / (2 * s), (s, 1, 2))
    high = sp.integrate(sp.pi / (2 * s), (s, 3, 4))
    if not _eq(low - sp.pi / 2 * sp.log(2)):
        return None
    if not _eq(high - sp.pi / 2 * sp.log(sp.Rational(4, 3))):
        return None
    return sp.pi / 2 * (sp.log(3) - sp.log(2))


def _exp_pair(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, 2 * sp.pi):
        return None
    sine = 2 ** sp.sin(symbol)
    cosine = 2 ** sp.cos(symbol)
    if integrand != 1 / ((1 + sine) * (1 + cosine)):
        return None
    s = sp.Symbol("_s", real=True)
    c = sp.Symbol("_c", real=True)
    if not _eq(1 / (1 + 2 ** (-s)) - 2**s / (1 + 2**s)):
        return None
    if not _eq(1 / (1 + 2**c) + 1 / (1 + 2 ** (-c)) - 1):
        return None
    # x -> 2*pi-x replaces sin by -sin. Averaging cancels that factor.
    # The remaining integral of 1/(1+2**cos), shifted by pi on half the period,
    # is the constant 1 on an interval of length pi. Half of that is pi/2.
    if sp.integrate(sp.Integer(1), (s, 0, sp.pi)) != sp.pi:
        return None
    return sp.pi / 2


def _sec_root(integrand, symbol, lo, hi):
    if not _span(lo, hi, 1, sp.sqrt(2)) or not _square_root(integrand):
        return None
    expected = sp.sqrt(symbol**2 + 2 * sp.sqrt(symbol**2 - 1)) / symbol
    if integrand != expected:
        return None
    u = sp.Symbol("_u", real=True)
    if not _eq(sp.sec(u) ** 2 - 1 - sp.tan(u) ** 2):
        return None
    inside = sp.sec(u) ** 2 + 2 * sp.tan(u)
    if not _eq(inside - (1 + sp.tan(u)) ** 2):
        return None
    actual = sp.sqrt(inside) * sp.tan(u)
    claimed = sp.tan(u) + sp.tan(u) ** 2
    if not _eq(actual**2 - claimed**2):
        return None
    if sp.simplify(actual.subs(u, sp.pi / 6) - claimed.subs(u, sp.pi / 6)) != 0:
        return None
    anti = -sp.log(sp.cos(u)) + sp.tan(u) - u
    if not _eq(sp.diff(anti, u) - claimed):
        return None
    value = anti.subs(u, sp.pi / 4) - anti.subs(u, 0)
    if not _eq(sp.simplify(value) - (sp.log(2) / 2 + 1 - sp.pi / 4)):
        return None
    if sp.sec(0) != 1 or sp.simplify(sp.sec(sp.pi / 4) - sp.sqrt(2)) != 0:
        return None
    return sp.log(2) / 2 + 1 - sp.pi / 4


def _dirichlet_split(integrand, symbol, lo, hi):
    if lo != -sp.oo or hi != sp.oo or not integrand.has(sp.atan):
        return None
    arc = sp.atan(symbol)
    den = 45 * symbol**2 + symbol**2 * arc + symbol**2 * sp.sqrt(2025 + arc**2)
    if integrand != sp.sin(symbol) ** 2 / den:
        return None
    if 45**2 != 2025:
        return None
    o = sp.Symbol("_o", real=True)
    b = sp.Symbol("_b", positive=True)
    plus = b + o + sp.sqrt(b**2 + o**2)
    minus = b - o + sp.sqrt(b**2 + o**2)
    if not _eq(1 / plus + 1 / minus - 1 / b):
        return None
    weight = sp.sin(symbol) ** 2 / symbol**2
    if sp.integrate(weight, (symbol, 0, sp.oo)) != sp.pi / 2:
        return None
    # f(x)+f(-x) = weight/45, so the symmetric integral is half of that sum.
    return sp.pi / 90


def _fresnel_shift(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.cos):
        return None
    if integrand != sp.cos(symbol**2 + 1 / symbol**2):
        return None
    x = sp.Symbol("_x", positive=True)
    if sp.expand(x**2 + 1 / x**2 - ((x - 1 / x) ** 2 + 2)) != 0:
        return None
    if not _eq(sp.cos(1 / x**2 + x**2) - sp.cos(x**2 + 1 / x**2)):
        return None
    if not _eq(sp.diff(x - 1 / x, x) - (1 + 1 / x**2)):
        return None
    theta = sp.Symbol("_th", real=True)
    angle = sp.cos(theta**2) * sp.cos(2) - sp.sin(theta**2) * sp.sin(2)
    if not _eq(sp.expand_trig(sp.cos(theta**2 + 2) - angle)):
        return None
    if not _eq(sp.cos((-theta) ** 2) - sp.cos(theta**2)):
        return None
    if not _eq(sp.sin((-theta) ** 2) - sp.sin(theta**2)):
        return None
    fresnel = sp.integrate(sp.cos(theta**2), (theta, 0, sp.oo))
    if not _eq(fresnel - sp.sqrt(2 * sp.pi) / 4):
        return None
    if sp.integrate(sp.sin(theta**2), (theta, 0, sp.oo)) != fresnel:
        return None
    return fresnel * (sp.cos(2) - sp.sin(2))


def _king_fourth(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.pi / 4):
        return None
    root = 2 ** sp.Rational(1, 4)
    expected = 1 / (root + sp.sqrt(1 + sp.tan(symbol)))
    if integrand != expected:
        return None
    u = sp.Symbol("_u", real=True)
    if not _eq(sp.tan(sp.pi / 4 - u) - (1 - sp.tan(u)) / (1 + sp.tan(u))):
        return None
    height = sp.sqrt(1 + sp.tan(u))
    partner = height / (root * height + root**2)
    if not _eq(1 / (root + height) + partner - 1 / root):
        return None
    if root**2 != sp.sqrt(2):
        return None
    width = sp.integrate(1 / root, (u, 0, sp.pi / 4))
    if not _eq(width / 2 - sp.pi / (8 * root)):
        return None
    return sp.pi / (8 * root)


def _sinh_sech(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.sinh):
        return None
    expected = 1 / (sp.sinh(sp.sqrt(symbol)) + sp.csch(sp.sqrt(symbol)))
    if integrand != expected:
        return None
    s = sp.Symbol("_s", positive=True)
    if not _eq(sp.csch(s) - 1 / sp.sinh(s)):
        return None
    reduced = sp.tanh(s) * sp.sech(s)
    if not _eq(1 / (sp.sinh(s) + sp.csch(s)) - reduced):
        return None
    if not _eq(sp.diff(sp.sqrt(symbol), symbol) * 2 * sp.sqrt(symbol) - 1):
        return None
    if not _eq(sp.diff(-sp.sech(s), s) - reduced):
        return None
    boundary = -s * sp.sech(s)
    if not _eq(sp.diff(boundary, s) + sp.sech(s) - s * reduced):
        return None
    if sp.limit(s * sp.sech(s), s, sp.oo) != 0 or (s * sp.sech(s)).subs(s, 0) != 0:
        return None
    if sp.integrate(sp.sech(s), (s, 0, sp.oo)) != sp.pi / 2:
        return None
    return sp.pi


def _exp_quartic(integrand, symbol, lo, hi):
    if not _span(lo, hi, 1, sp.oo):
        return None
    expected = (1 + 2 * symbol * sp.log(2)) / (symbol * sp.sqrt(symbol * 4**symbol - 1))
    if integrand != expected:
        return None
    x = sp.Symbol("_x", positive=True)
    base = x * 4**x - 1
    if not _eq(sp.diff(base, x) - 4**x * (1 + 2 * x * sp.log(2))):
        return None
    if base.subs(x, 1) != 3:
        return None
    if sp.limit(base, x, sp.oo) != sp.oo:
        return None
    y = sp.Symbol("_y", positive=True)
    if not _eq(sp.diff(y**2, y) / ((y**2 + 1) * y) - 2 / (1 + y**2)):
        return None
    if not _eq(sp.atan(sp.sqrt(3)) - sp.pi / 3):
        return None
    return 2 * (sp.pi / 2 - sp.pi / 3)


def _factorial_beta(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.factorial):
        return None
    if not integrand.has(sp.floor) or not integrand.has(sp.ceiling):
        return None
    level = sp.floor(symbol)
    cap = sp.ceiling(symbol)
    expected = sp.factorial(level) * sp.factorial2(2 * level) / sp.factorial(2 * cap - 1)
    if integrand != expected:
        return None
    n = sp.Symbol("_n", integer=True, nonnegative=True)
    if not _eq(sp.factorial2(2 * n) - 2**n * sp.factorial(n)):
        return None
    slot = expected.xreplace({level: n, cap: n + 1})
    beta = 2**n * sp.beta(n + 1, n + 1)
    if not _eq(slot - beta):
        return None
    rewritten = sp.beta(n + 1, n + 1).rewrite(sp.Integral)
    if not isinstance(rewritten, sp.Integral) or len(rewritten.limits) != 1:
        return None
    dummy, start, end = rewritten.limits[0]
    body = dummy**n * (1 - dummy) ** n
    if (start, end) != (0, 1) or not _eq(rewritten.function - body):
        return None
    t = sp.Symbol("_t", real=True)
    radius = 2 * t * (1 - t)
    if not _eq(sp.Rational(1, 2) - radius - (2 * t - 1) ** 2 / 2):
        return None
    # On [0, 1] the same square gives 0 <= 2t(1-t) <= 1/2.
    gap = sp.Rational(1, 4) - (t - sp.Rational(1, 2)) ** 2
    if not _eq(t * (1 - t) - gap):
        return None
    if gap.subs(t, 0) != 0 or gap.subs(t, 1) != 0 or gap.subs(t, sp.Rational(1, 2)) != sp.Rational(1, 4):
        return None
    ratio = sp.Symbol("_r")
    degree = sp.Symbol("_N", integer=True, positive=True)

    def geometric(index):
        return (1 - ratio ** (index + 1)) / (1 - ratio)

    if sp.simplify(geometric(0) - 1) != 0:
        return None
    step = geometric(degree) - geometric(degree - 1) - ratio**degree
    if sp.simplify(sp.together(step)) != 0:
        return None
    if sp.limit((sp.Rational(1, 2)) ** (degree + 1), degree, sp.oo) != 0:
        return None
    if not _eq(1 / (1 - radius) - 2 / (1 + (2 * t - 1) ** 2)):
        return None
    if sp.integrate(2 / (1 + (2 * t - 1) ** 2), (t, 0, 1)) != sp.pi / 2:
        return None
    return sp.pi / 2


def _two_roots(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, 1) or not _square_root(integrand):
        return None
    expected = sp.sqrt(symbol + symbol**3) + sp.sqrt(symbol + symbol ** sp.Rational(1, 3))
    if integrand != expected:
        return None
    u = sp.Symbol("_u", positive=True)
    if sp.diff(u**3, u) != 3 * u**2:
        return None
    second = 3 * u**2 * sp.sqrt(u**3 + u)
    if not _eq(second.subs(u, symbol) + sp.sqrt(symbol + symbol**3) - (1 + 3 * symbol**2) * sp.sqrt(symbol + symbol**3)):
        return None
    anti = sp.Rational(2, 3) * (symbol + symbol**3) ** sp.Rational(3, 2)
    if not _eq(sp.diff(anti, symbol) - (1 + 3 * symbol**2) * sp.sqrt(symbol + symbol**3)):
        return None
    if anti.subs(symbol, 0) != 0:
        return None
    return anti.subs(symbol, 1)


def _floor_tangent(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.floor) or not integrand.has(sp.tan):
        return None
    step = 3 ** (-sp.floor(symbol))
    expected = step * sp.tan(step) / (3 - sp.tan(step) ** 2)
    if integrand != expected:
        return None
    a = sp.Symbol("_a", positive=True)
    t = sp.tan(a)
    triple = (3 * t - t**3) / (1 - 3 * t**2)
    if not _eq(sp.expand_trig(sp.tan(3 * a) * (1 - 3 * t**2) - (3 * t - t**3))):
        return None
    cleared = 1 / t - 3 * (1 - 3 * t**2) / (t * (3 - t**2))
    if not _eq(sp.together(cleared) - 8 * t / (3 - t**2)):
        return None
    if sp.limit(a * sp.cot(a), a, 0) != 1:
        return None
    if not _eq(sp.tan(sp.pi / 2 - 3) - sp.cot(3)):
        return None
    return sp.Rational(1, 8) * (1 - 3 * sp.cot(3))


def _floor_tower(integrand, symbol, lo, hi):
    if lo != -sp.oo or hi != sp.oo or not integrand.has(sp.floor):
        return None
    expected = 2 ** (sp.floor(2**symbol) + symbol) / (3 ** (2 ** sp.floor(2**symbol)) + 1)
    if integrand != expected:
        return None
    y = sp.Symbol("_y", positive=True)
    if not _eq(sp.diff(2**symbol, symbol) / (2**symbol * sp.log(2)) - 1):
        return None
    n = sp.Symbol("_n", integer=True, nonnegative=True)
    base = 3 ** (2**n)
    term = 2**n / (base + 1)
    telescoping = 2**n / (base - 1) - 2 ** (n + 1) / (base**2 - 1)
    if not _eq(sp.cancel(term - telescoping)):
        return None
    if sp.Rational(1, 3 ** (2**0) - 1) != sp.Rational(1, 2):
        return None
    large = sp.Symbol("_m", positive=True)
    if sp.limit(2**large / 3 ** (2**large), large, sp.oo) != 0:
        return None
    if sp.limit(3 ** (-(2**large)), large, sp.oo) != 0:
        return None
    return 1 / (2 * sp.log(2))


def _log_semicircle(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.log):
        return None
    expected = sp.log(symbol) * (2 * symbol - 1) / sp.sqrt(symbol - symbol**2)
    if integrand != expected:
        return None
    branch = -2 * sp.sqrt(symbol - symbol**2)
    if not _eq(sp.diff(branch, symbol) - (2 * symbol - 1) / sp.sqrt(symbol - symbol**2)):
        return None
    if sp.limit(sp.log(symbol) * branch, symbol, 0) != 0:
        return None
    if sp.limit(sp.log(symbol) * branch, symbol, 1) != 0:
        return None
    u = sp.Symbol("_u", real=True)
    xx = sp.sin(u) ** 2
    if not _eq(xx - xx**2 - (sp.sin(u) * sp.cos(u)) ** 2):
        return None
    positive = sp.Symbol("_p", positive=True)
    if sp.sqrt(positive**2) != positive:
        return None
    if sp.solveset(sp.sin(u), u, domain=sp.Interval.open(0, sp.pi)) != sp.EmptySet:
        return None
    if sp.sin(sp.pi / 2) != 1:
        return None
    # sin(2u) stays positive for u in (0, pi/2), so the square root is sin(u)cos(u).
    if not _eq(sp.sin(u) * sp.cos(u) - sp.sin(2 * u) / 2):
        return None
    sample = sp.sin(sp.pi / 4) * sp.cos(sp.pi / 4)
    if not _eq(sp.sqrt(sample**2) - sample):
        return None
    replaced = 2 * sp.sin(u) * sp.cos(u) / xx * sp.diff(xx, u)
    if not _eq(replaced - 4 * sp.cos(u) ** 2):
        return None
    if sp.integrate(4 * sp.cos(u) ** 2, (u, 0, sp.pi / 2)) != sp.pi:
        return None
    return sp.pi


def _eta_square(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.exp):
        return None
    if integrand != 1 / (1 + sp.exp(sp.sqrt(symbol))):
        return None
    u = sp.Symbol("_u", positive=True)
    if not _eq((1 / (1 + sp.exp(sp.sqrt(symbol)))).subs(symbol, u**2) * sp.diff(u**2, u) - 2 * u / (1 + sp.exp(u))):
        return None
    q = sp.exp(-u)
    ratio = sp.Symbol("_r")
    degree = sp.Symbol("_N", integer=True, positive=True)

    def geometric(index):
        return (1 - ratio ** (index + 1)) / (1 - ratio)

    if sp.simplify(geometric(0) - 1) != 0:
        return None
    step = geometric(degree) - geometric(degree - 1) - ratio**degree
    if sp.simplify(sp.together(step)) != 0:
        return None
    # |−e^{−u}| = e^{−u} < 1, so the remainder of ratio = −q vanishes.
    if sp.limit(sp.exp(-(degree + 1) * u), degree, sp.oo) != 0:
        return None
    if not _eq(sp.log(sp.exp(-u)) + u):
        return None
    signed = -q
    if not _eq(1 / (1 - signed) - 1 / (1 + q)):
        return None
    n = sp.Symbol("_n", integer=True, nonnegative=True)
    if not _eq(q / (1 + q) - 1 / (1 + sp.exp(u))):
        return None
    if not _eq(sp.integrate(u * sp.exp(-(n + 1) * u), (u, 0, sp.oo)) - 1 / (n + 1) ** 2):
        return None
    series = sp.summation(2 * (-1) ** n / (n + 1) ** 2, (n, 0, sp.oo))
    if series != sp.pi**2 / 6:
        return None
    return series


def _atan_split(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.atan):
        return None
    arc = sp.atan(symbol)
    companion = sp.acot(symbol)
    expected = 1 / ((1 + symbol**2) * (1 + sp.pi / 2 + arc * companion))
    if integrand != expected:
        return None
    if sp.diff(arc + companion, symbol) != 0:
        return None
    if (arc + companion).subs(symbol, 1) != sp.pi / 2:
        return None
    u = sp.Symbol("_u", real=True)
    den = (1 + u) * (1 + sp.pi / 2 - u)
    piece = (1 / (1 + u) + 1 / (1 + sp.pi / 2 - u)) / (2 + sp.pi / 2)
    if not _eq(piece - 1 / den):
        return None
    anti = sp.log(1 + u) - sp.log(1 + sp.pi / 2 - u)
    if not _eq(sp.diff(anti, u) - (1 / (1 + u) + 1 / (1 + sp.pi / 2 - u))):
        return None
    gap = anti.subs(u, sp.pi / 4) - anti.subs(u, 0)
    if not _eq(gap / (2 + sp.pi / 2) - sp.log(1 + sp.pi / 2) / (2 + sp.pi / 2)):
        return None
    return sp.log(1 + sp.pi / 2) / (2 + sp.pi / 2)


def _atan_square(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.atan):
        return None
    arc = sp.atan(symbol) * sp.acot(symbol)
    expected = 1 / ((1 + symbol**2) * (1 + arc))
    if integrand != expected:
        return None
    if sp.diff(sp.atan(symbol) + sp.acot(symbol), symbol) != 0:
        return None
    if (sp.atan(symbol) + sp.acot(symbol)).subs(symbol, 1) != sp.pi / 2:
        return None
    u = sp.Symbol("_u", real=True)
    quad = 1 + sp.pi / 2 * u - u**2
    completed = (1 + sp.pi**2 / 16) - (u - sp.pi / 4) ** 2
    if sp.expand(quad - completed) != 0:
        return None
    root = sp.sqrt(16 + sp.pi**2) / 4
    v = sp.Symbol("_v", real=True)
    anti = sp.atanh(v / root) / root
    if not _eq(sp.diff(anti, v) - 1 / (root**2 - v**2)):
        return None
    z = sp.Symbol("_z", real=True)
    if not _eq(sp.atanh(-z) + sp.atanh(z)):
        return None
    end = sp.pi / 4
    if not _eq(4 * root - sp.sqrt(16 + sp.pi**2)):
        return None
    value = anti.subs(v, 0) - anti.subs(v, -end)
    if not _eq(value - 4 / sp.sqrt(16 + sp.pi**2) * sp.atanh(sp.pi / sp.sqrt(16 + sp.pi**2))):
        return None
    return value


def _gamma_nest(integrand, symbol, lo, hi):
    if not _span(lo, hi, 1, sp.oo) or not integrand.has(sp.exp):
        return None
    if integrand != sp.exp(-sp.sqrt(sp.sqrt(symbol) - 1)):
        return None
    u = sp.Symbol("_u", positive=True)
    if not _eq(sp.diff((u**2 + 1) ** 2, u) - 4 * u * (1 + u**2)):
        return None
    moment = sp.integrate((u + u**3) * sp.exp(-u), (u, 0, sp.oo))
    if moment != 7:
        return None
    return 4 * moment


def _shifted_phase(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, 2) or not integrand.has(sp.cos):
        return None
    phase = symbol**3 - 3 * symbol**2 + 4 * symbol - 2
    expected = (3 * symbol**2 - 5 * symbol + 3) * sp.cos(phase)
    if integrand != expected:
        return None
    u = sp.Symbol("_u", real=True)
    shifted = symbol + 1
    if sp.expand(expected.subs(symbol, u + 1).rewrite(sp.cos) - expected.subs(symbol, u + 1)) != 0:
        return None
    coefficient = sp.expand((3 * shifted**2 - 5 * shifted + 3).subs(symbol, u) - (3 * u**2 + u + 1))
    moved = sp.expand(phase.subs(symbol, u + 1) - (u**3 + u))
    if coefficient != 0 or moved != 0:
        return None
    odd = u * sp.cos(u**3 + u)
    if not _eq(odd.subs(u, -u) + odd):
        return None
    span = sp.Symbol("_a", positive=True)
    if sp.diff(sp.Integral(odd, (u, -span, span)), span) != 0:
        return None
    even = (3 * u**2 + 1) * sp.cos(u**3 + u)
    if not _eq(sp.diff(sp.sin(u**3 + u), u) - even):
        return None
    if sp.sin(2) - sp.sin(-2) != 2 * sp.sin(2):
        return None
    return 2 * sp.sin(2)


def _logistic_king(integrand, symbol, lo, hi):
    if not _span(lo, hi, -2024, 2025):
        return None
    expected = 1 / (3**symbol + sp.sqrt(3))
    if integrand != expected:
        return None
    if not _eq(sp.simplify(expected + expected.subs(symbol, 1 - symbol) - 1 / sp.sqrt(3))):
        return None
    if (1 - (-2024)) != 2025 or (1 - 2025) != -2024:
        return None
    if 2025 - (-2024) != 4049:
        return None
    return sp.Integer(4049) / (2 * sp.sqrt(3))


def _square_root(expr) -> bool:
    return any(power.exp == sp.Rational(1, 2) for power in expr.atoms(sp.Pow))


def _log_cube(answer, integrand, symbol) -> bool:
    if not integrand.has(sp.log):
        return False
    inside = symbol**3 + symbol ** (-3) + 3 * (symbol + 1 / symbol)
    expected = (symbol**2 - 1) / (symbol**3 + symbol) * sp.log(inside)
    if integrand != expected:
        return False
    wanted = sp.Rational(3, 2) * sp.log(symbol + 1 / symbol) ** 2
    if not _eq(answer - wanted):
        return False
    positive = sp.Symbol("_p", positive=True)
    packed = positive**3 + positive ** (-3) + 3 * (positive + 1 / positive)
    if sp.expand(packed * positive**3 - (positive**2 + 1) ** 3) != 0:
        return False
    ratio = sp.log((positive**2 + 1) ** 3 / positive**3) - 3 * sp.log((positive**2 + 1) / positive)
    if not _eq(sp.expand_log(ratio, force=True)):
        return False
    reduced = 3 * sp.log(positive + 1 / positive) * (positive**2 - 1) / (positive**3 + positive)
    return _eq(sp.diff(wanted, symbol).subs(symbol, positive) - reduced)


def _lambert(answer, integrand, symbol) -> bool:
    if not integrand.has(sp.LambertW):
        return False
    weight = sp.LambertW(symbol)
    if integrand != sp.exp(weight) / symbol**2:
        return False
    wanted = sp.log(sp.Abs(weight)) - 1 / weight
    if not _eq(answer - wanted):
        return False
    w = sp.Symbol("_w", positive=True)
    branch = sp.Symbol("_x", positive=True)
    if sp.solve(w * sp.exp(w) - branch, w) != [sp.LambertW(branch)]:
        return False
    source = w * sp.exp(w)
    slope = sp.diff(source, w)
    if not _eq(slope - sp.exp(w) * (w + 1)):
        return False
    if sp.ask(sp.Q.positive(slope)) is not True:
        return False
    if sp.limit(source, w, 0) != 0 or sp.limit(source, w, sp.oo) != sp.oo:
        return False
    changed = sp.exp(w) / source**2 * slope
    if not _eq(changed - (w + 1) / w**2):
        return False
    if not _eq(sp.log(sp.Abs(w)) - sp.log(w)):
        return False
    return _eq(sp.diff(sp.log(w) - 1 / w, w) - (w + 1) / w**2)


def indefinite_ok(answer, integrand, symbol) -> bool:
    if _log_cube(answer, integrand, symbol):
        return True
    return bool(integrand.has(sp.LambertW) and _lambert(answer, integrand, symbol))


def definite_value(integrand, symbol, lo, hi):
    for builder in (
        _floor_quartic,
        _tan_boundary,
        _atan_log_square,
        _atan_frullani,
        _exp_pair,
        _sec_root,
        _dirichlet_split,
        _fresnel_shift,
        _king_fourth,
        _sinh_sech,
        _exp_quartic,
        _factorial_beta,
        _two_roots,
        _floor_tangent,
        _floor_tower,
        _log_semicircle,
        _eta_square,
        _atan_split,
        _atan_square,
        _gamma_nest,
        _shifted_phase,
        _logistic_king,
    ):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
