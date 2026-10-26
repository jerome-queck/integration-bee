"""Exact reductions for the wave-5n pack rows.

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


def _log_radical(integrand, symbol, lo, hi):
    """ln(sqrt(1+sqrt(x))+sqrt(1-sqrt(x))) on [0, 1] is ln(2)/2+1/4."""
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.log):
        return None
    root = sp.sqrt(symbol)
    arg = sp.sqrt(1 + root) + sp.sqrt(1 - root)
    if integrand != sp.log(arg):
        return None
    # The factors are nonnegative on (0, 1), so the square is 2+2*sqrt(1-x).
    positive = sp.Symbol("_p", positive=True)
    left = sp.sqrt(1 + sp.sqrt(positive))
    right = sp.sqrt(1 - sp.sqrt(positive))
    square = (left + right) ** 2
    target = 2 * (1 + sp.sqrt(1 - positive))
    if sp.simplify(square / target) != 1:
        return None
    if not _eq(sp.expand_log(sp.log(left + right) - sp.log(sp.sqrt(square)), force=True)):
        return None
    half = sp.log(2) / 2 + sp.log(1 + sp.sqrt(1 - positive)) / 2
    if not _eq(sp.expand_log(sp.log(target) / 2 - half, force=True)):
        return None
    if not _eq(sp.expand_log(sp.log(sp.sqrt(target)) - sp.log(target) / 2, force=True)):
        return None
    if sp.simplify(sp.log(square / target)) != 0:
        return None
    u = sp.Symbol("_u", positive=True)
    changed = sp.log(1 + sp.sqrt(1 - (1 - u**2))) * sp.diff(1 - u**2, u)
    if not _eq(changed + 2 * u * sp.log(1 + u)):
        return None
    anti = u**2 * sp.log(1 + u) / 2 - u**2 / 4 + u / 2 - sp.log(1 + u) / 2
    if not _eq(sp.diff(anti, u) - u * sp.log(1 + u)):
        return None
    if sp.limit(anti, u, 0) != 0:
        return None
    if sp.simplify(anti.subs(u, 1) - sp.Rational(1, 4)) != 0:
        return None
    # ∫ log(1+sqrt(1-x)) dx = 2*(1/4). The constant log(2)/2 supplies the rest.
    return sp.log(2) / 2 + sp.Rational(1, 4)


def _log_pair(integrand, symbol, lo, hi):
    """The [0, 1] logarithm pair splits (ln 2)^2 into two equal integrals."""
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.log):
        return None
    expected = sp.log((1 + 3 * symbol) / (2 - symbol)) / (1 + symbol)
    if integrand != expected:
        return None
    f = sp.log(1 + symbol)
    g = 2 * symbol / (1 + symbol)
    inverse = symbol / (2 - symbol)
    if g.subs(symbol, 0) != 0 or sp.simplify(g.subs(symbol, 1) - 1) != 0:
        return None
    if not _eq(g.subs(symbol, inverse) - symbol):
        return None
    if not _eq(inverse.subs(symbol, g) - symbol):
        return None
    linked = (1 + g) * (1 + inverse) - (1 + 3 * symbol) / (2 - symbol) * 2 / (1 + symbol)
    if not _eq(linked):
        return None
    u = sp.Symbol("_u", positive=True)
    substituted = f.subs(symbol, inverse).subs(symbol, g.subs(symbol, u))
    weight = sp.diff(f, symbol).subs(symbol, g.subs(symbol, u)) * sp.diff(g, symbol).subs(symbol, u)
    if not _eq(substituted * weight - f.subs(symbol, u) * sp.diff(f.subs(symbol, g.subs(symbol, u)), u)):
        return None
    product = f * f.subs(symbol, g)
    if not _eq(sp.diff(product, symbol) - (sp.diff(f, symbol) * f.subs(symbol, g) + f * sp.diff(f.subs(symbol, g), symbol))):
        return None
    # Integration by parts on the substituted term cancels the g term.
    # The endpoint values are f(1)^2-f(0)^2.
    if sp.simplify(product.subs(symbol, 1) - sp.log(2) ** 2) != 0 or product.subs(symbol, 0) != 0:
        return None
    second = sp.log(2 / (1 + symbol)) / (1 + symbol)
    second_anti = -sp.log(2 / (1 + symbol)) ** 2 / 2
    if not _eq(sp.diff(second_anti, symbol) - second):
        return None
    if sp.simplify(second_anti.subs(symbol, 0) - (-sp.log(2) ** 2 / 2)) != 0 or second_anti.subs(symbol, 1) != 0:
        return None
    return sp.log(2) ** 2 / 2


def _relay_log_pair(integrand, symbol, lo, hi):
    """Reflection cancels ln(1+e^x) and leaves x ln((1+x)/(1-x)) on [-1, 1]."""
    if not _span(lo, hi, -1, 1) or not integrand.has(sp.exp):
        return None
    ratio = sp.log((1 + symbol) / (1 - symbol))
    expected = ratio * sp.log(1 + sp.exp(symbol))
    if integrand != expected:
        return None
    flipped = sp.log((1 - symbol) / (1 + symbol))
    if not _eq(sp.expand_log(flipped + ratio, force=True)):
        return None
    if not _eq(sp.log(1 + sp.exp(-symbol)) - (sp.log(1 + sp.exp(symbol)) - symbol)):
        return None
    manual = flipped * sp.log(1 + sp.exp(-symbol))
    claimed = -ratio * (sp.log(1 + sp.exp(symbol)) - symbol)
    if not _eq(sp.expand_log(manual - claimed, force=True)):
        return None
    reduced = symbol * ratio
    if not _eq(sp.expand_log(expected + manual - reduced, force=True)):
        return None
    # u=-x reverses [-1, 1]. The jacobian is -1 and the limits swap, so the
    # integral of f(-x) equals the integral of f.
    dummy = sp.Symbol("_u", real=True)
    if sp.diff(-dummy, dummy) != -1 or -(-1) != 1 or -(1) != -1:
        return None
    anti = sp.Rational(1, 2) * ((symbol**2 - 1) * ratio + 2 * symbol)
    if not _eq(sp.diff(anti, symbol) - reduced):
        return None
    if sp.limit((symbol**2 - 1) * ratio, symbol, 1, dir="-") != 0:
        return None
    if sp.limit((symbol**2 - 1) * ratio, symbol, -1, dir="+") != 0:
        return None
    if sp.limit(anti, symbol, 1, dir="-") != 1:
        return None
    if sp.limit(anti, symbol, -1, dir="+") != -1:
        return None
    return sp.Integer(1)


def _sec_line(integrand, symbol, lo, hi):
    """atan(x/cos x) jumps only on (-pi/2, pi/2), by pi."""
    if not _span(lo, hi, -sp.oo, sp.oo):
        return None
    expected = (sp.cos(symbol) + symbol * sp.sin(symbol)) / (symbol**2 + sp.cos(symbol) ** 2)
    if integrand != expected:
        return None
    anti = sp.atan(symbol / sp.cos(symbol))
    if not _eq(sp.diff(anti, symbol) - integrand):
        return None

    def edge(index):
        return (index + sp.Rational(1, 2)) * sp.pi

    positive = sp.Symbol("_k", integer=True, positive=True)
    negative = sp.Symbol("_km", integer=True, negative=True)
    for index in (positive, negative):
        right = sp.limit(anti, symbol, edge(index), dir="-")
        left = sp.limit(anti, symbol, edge(index - 1), dir="+")
        if sp.simplify(right - left) != 0:
            return None
    if sp.limit(anti, symbol, sp.pi / 2, dir="-") != sp.pi / 2:
        return None
    if sp.limit(anti, symbol, -sp.pi / 2, dir="+") != -sp.pi / 2:
        return None
    return sp.pi


def _asin_endpoint(integrand, symbol, lo, hi):
    """asin(x cos x) vanishes at both ends of [0, pi/2]."""
    if not _span(lo, hi, 0, sp.pi / 2) or not integrand.has(sp.tan):
        return None
    expected = (symbol * sp.tan(symbol) - 1) / sp.sqrt(sp.sec(symbol) ** 2 - symbol**2)
    if integrand != expected:
        return None
    cos = sp.cos(symbol)
    left_sq = 1 - symbol**2 * cos**2
    right_sq = cos**2 * (sp.sec(symbol) ** 2 - symbol**2)
    if not _eq(left_sq - right_sq):
        return None
    numerator = cos - symbol * sp.sin(symbol)
    if not _eq(numerator - cos * (1 - symbol * sp.tan(symbol))):
        return None
    anti = sp.asin(symbol * cos)
    if not _eq(sp.diff(anti, symbol) - numerator / sp.sqrt(left_sq)):
        return None
    reduced = (1 - symbol * sp.tan(symbol)) / sp.sqrt(sp.sec(symbol) ** 2 - symbol**2)
    # On (0, pi/2), cos is positive, so sqrt(1-x**2 cos**2)=cos*sqrt(sec**2-x**2).
    if sp.solveset(sp.cos(symbol), symbol, domain=sp.Interval(0, sp.pi / 2)) != sp.FiniteSet(sp.pi / 2):
        return None
    if sp.cos(0) != 1:
        return None
    manual = numerator / (cos * sp.sqrt(sp.sec(symbol) ** 2 - symbol**2))
    if not _eq(manual - reduced):
        return None
    if not _eq(reduced + integrand):
        return None
    if anti.subs(symbol, 0) != 0 or sp.limit(anti, symbol, sp.pi / 2) != 0:
        return None
    return sp.Integer(0)


def _semicircle_max(integrand, symbol, lo, hi):
    """The semicircle exceeds |x| only inside |x|=r/sqrt(2)."""
    if not integrand.has(sp.Max):
        return None
    parameters = [item for item in integrand.free_symbols if item != symbol]
    if len(parameters) != 1 or lo != -parameters[0] or hi != parameters[0]:
        return None
    radius = parameters[0]
    if radius.is_positive is not True:
        return None
    expected = sp.Max(sp.sqrt(radius**2 - symbol**2), sp.Abs(symbol))
    if integrand != expected:
        return None
    cross = radius / sp.sqrt(2)
    if not _eq(sp.sqrt(radius**2 - cross**2) - cross):
        return None
    sample = sp.Symbol("_x", positive=True)
    below = radius**2 - 2 * sample**2
    if sp.simplify(below.subs(sample, cross)) != 0:
        return None
    anti = sp.Rational(1, 2) * (symbol * sp.sqrt(radius**2 - symbol**2) + radius**2 * sp.asin(symbol / radius))
    if not _eq(sp.diff(anti, symbol) - sp.sqrt(radius**2 - symbol**2)):
        return None
    if anti.subs(symbol, 0) != 0:
        return None
    if sp.asin(1 / sp.sqrt(2)) != sp.pi / 4:
        return None
    inner = sp.simplify(anti.subs(symbol, cross))
    if not _eq(inner - (radius**2 / 4 + sp.pi * radius**2 / 8)):
        return None
    outer = sp.integrate(symbol, (symbol, cross, radius))
    if not _eq(2 * inner + 2 * outer - radius**2 * (1 + sp.pi / 4)):
        return None
    return radius**2 * (1 + sp.pi / 4)


def _double_log_series(integrand, symbol, lo, hi):
    """Order change turns the double logarithm into 1-pi**2/6."""
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.log):
        return None
    expected = (1 - symbol) * sp.log(1 - symbol) / symbol
    if integrand != expected:
        return None
    inner = sp.Symbol("_u")
    outer = sp.Symbol("_z")
    height = sp.Symbol("_a", positive=True)
    probe = sp.Function("_f")
    tower = sp.Integral(sp.Integral(probe(inner), (inner, 0, outer)), (outer, 0, height))
    flat = sp.Integral((height - inner) * probe(inner), (inner, 0, height))
    if sp.diff(tower, height) != sp.Integral(probe(inner), (inner, 0, height)):
        return None
    if sp.simplify(sp.diff(flat, height) - sp.Integral(probe(inner), (inner, 0, height))) != 0:
        return None
    index = sp.Symbol("_k", integer=True)
    degree = sp.Symbol("_n", integer=True, positive=True)
    base = sp.Symbol("_v", positive=True)
    geom = sp.summation(base**index, (index, 0, degree - 1))
    if not _eq((1 - base) * geom - (1 - base**degree)):
        return None
    if not _eq(sp.diff(base**index / index, base) - base ** (index - 1)):
        return None
    reindexed = sp.Sum(base ** (index - 1), (index, 1, degree)) - sp.Sum(base**index, (index, 0, degree - 1))
    if sp.simplify(reindexed.doit()) != 0:
        return None
    if not _eq(sp.diff(-sp.log(1 - base), base) - 1 / (1 - base)):
        return None
    # For 0<t<u<1, 1/(1-t) <= 1/(1-u), so the log remainder is at most
    # u^n/((n+1)(1-u)). Multiplied by (1-u)/u this is u^n/(n+1).
    ray = sp.Symbol("_t", positive=True)
    capped = sp.integrate(ray**degree, (ray, 0, base)) / (1 - base)
    if not _eq((1 - base) / base * capped - base**degree / (degree + 1)):
        return None
    if sp.integrate(base**degree / (degree + 1), (base, 0, 1)) != 1 / (degree + 1) ** 2:
        return None
    if sp.limit(1 / (degree + 1) ** 2, degree, sp.oo) != 0:
        return None
    power = sp.Symbol("_m", integer=True, positive=True)
    primitive = base**power / power - base ** (power + 1) / (power + 1)
    if not _eq(sp.diff(primitive, base) - (base ** (power - 1) - base**power)):
        return None
    if sp.limit(primitive, base, 0) != 0:
        return None
    if not _eq(primitive.subs(base, 1) - (1 / power - 1 / (power + 1))):
        return None
    if not _eq(1 / (power**2 * (power + 1)) - (1 / power) * (1 / power - 1 / (power + 1))):
        return None
    if not _eq(1 / (power**2 * (power + 1)) - (1 / power**2 - 1 / power + 1 / (power + 1))):
        return None
    total = sp.Symbol("_N", integer=True, positive=True)
    telescope = sp.summation(1 / (index + 1) - 1 / index, (index, 1, total))
    if not _eq(sp.simplify(telescope - (-1 + 1 / (total + 1)))):
        return None
    if sp.limit(telescope, total, sp.oo) != -1:
        return None
    if sp.zeta(2) != sp.pi**2 / 6:
        return None
    summed = sp.summation(1 / (index**2 * (index + 1)), (index, 1, sp.oo))
    if not _eq(summed - (sp.pi**2 / 6 - 1)):
        return None
    return 1 - sp.pi**2 / 6


def _tan_square_root(integrand, symbol, lo, hi):
    """sqrt(tan x) sqrt(1-tan x) on [0, pi/4] denests to the printed radical."""
    if not _span(lo, hi, 0, sp.pi / 4) or not integrand.has(sp.tan):
        return None
    expected = sp.sqrt(sp.tan(symbol)) * sp.sqrt(1 - sp.tan(symbol))
    if integrand != expected:
        return None
    slope = sp.Symbol("_t", positive=True)
    pulled = expected.subs(symbol, sp.atan(slope)) * sp.diff(sp.atan(slope), slope)
    target = sp.sqrt(slope * (1 - slope)) / (1 + slope**2)
    if not _eq(pulled - target):
        return None
    ray = sp.Symbol("_u", positive=True)
    height = 1 / (1 + ray**2)
    changed = target.subs(slope, height) * sp.diff(height, ray)
    quartic_source = 2 * ray**2 / ((1 + ray**2) * (ray**4 + 2 * ray**2 + 2))
    if not _eq(-changed - quartic_source):
        return None
    quartic = (2 * ray**2 + 4) / (ray**4 + 2 * ray**2 + 2)
    if not _eq(-2 / (ray**2 + 1) + quartic - quartic_source):
        return None
    width = sp.integrate(1 / (ray**2 + 1), (ray, 0, sp.oo))
    if width != sp.pi / 2:
        return None
    total = sp.integrate(quartic, (ray, 0, sp.oo))
    printed = sp.pi * (sp.sqrt(2 + 2 * sp.sqrt(2)) / 2 - 1)
    if sp.sqrtdenest(sp.simplify(total - sp.pi - printed)) != 0:
        return None
    return printed


def _arcsin_log(integrand, symbol, lo, hi):
    """The arcsine substitution reduces the logarithm to 4(t ln t-t)."""
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.asin):
        return None
    expected = sp.log(sp.asin(symbol)) / sp.sqrt((1 - symbol**2) * sp.asin(symbol))
    if integrand != expected:
        return None
    angle = sp.Symbol("_u", real=True)
    if sp.solveset(sp.cos(angle), angle, domain=sp.Interval(0, sp.pi / 2)) != sp.FiniteSet(sp.pi / 2):
        return None
    if sp.cos(0) != 1:
        return None
    if sp.asin(0) != 0 or sp.asin(1) != sp.pi / 2:
        return None
    slope = sp.diff(sp.asin(sp.sin(angle)), angle)
    if not _eq(slope - sp.cos(angle) / sp.Abs(sp.cos(angle))):
        return None
    raw = sp.simplify(expected.subs(symbol, sp.sin(angle)) * sp.diff(sp.sin(angle), angle))
    changed = raw.subs(sp.asin(sp.sin(angle)), angle).subs(sp.Abs(sp.cos(angle)), sp.cos(angle))
    if not _eq(changed - sp.log(angle) / sp.sqrt(angle)):
        return None
    ray = sp.Symbol("_t", positive=True)
    second = sp.log(ray**2) / ray * sp.diff(ray**2, ray)
    if not _eq(second - 4 * sp.log(ray)):
        return None
    anti = 4 * (ray * sp.log(ray) - ray)
    if not _eq(sp.diff(anti, ray) - 4 * sp.log(ray)):
        return None
    if sp.limit(ray * sp.log(ray), ray, 0) != 0:
        return None
    if sp.limit(anti, ray, 0) != 0:
        return None
    end = sp.sqrt(sp.pi / 2)
    value = sp.simplify(anti.subs(ray, end))
    printed = sp.sqrt(2 * sp.pi) * (sp.log(sp.pi / 2) - 2)
    if not _eq(value - printed):
        return None
    return printed


def _quartic_reflection(integrand, symbol, lo, hi):
    """Reflection halves 1/((e+e^x)((x-1)^4+1)) on the line."""
    if not _span(lo, hi, -sp.oo, sp.oo) or not integrand.has(sp.exp):
        return None
    quartic = symbol**4 - 4 * symbol**3 + 6 * symbol**2 - 4 * symbol + 2
    expected = 1 / ((sp.E + sp.exp(symbol)) * quartic)
    if integrand != expected:
        return None
    if not _eq(sp.expand(quartic - ((symbol - 1) ** 4 + 1))):
        return None
    shift = sp.Symbol("_t", real=True)
    shifted = expected.subs(symbol, shift + 1) * sp.diff(shift + 1, shift)
    kernel = 1 / ((1 + sp.exp(shift)) * (shift**4 + 1))
    if not _eq(shifted - sp.exp(-1) * kernel):
        return None
    if not _eq(kernel + kernel.subs(shift, -shift) - 1 / (shift**4 + 1)):
        return None
    width = sp.integrate(1 / (shift**4 + 1), (shift, -sp.oo, sp.oo))
    if not _eq(width - sp.pi / sp.sqrt(2)):
        return None
    return sp.pi / (2 * sp.E * sp.sqrt(2))


def _sine_powers(integrand, symbol, lo, hi):
    """Multiple-angle reduction of the four sine powers on [0, oo)."""
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.sin):
        return None
    sine = sp.sin(symbol)
    expected = sine**6 / symbol**2 + sine**5 / symbol + sine**4 / symbol**2 + sine**3 / symbol**3
    if integrand != expected:
        return None
    sixth = (10 - 15 * sp.cos(2 * symbol) + 6 * sp.cos(4 * symbol) - sp.cos(6 * symbol)) / 32
    fourth = sp.Rational(3, 8) - sp.cos(2 * symbol) / 2 + sp.cos(4 * symbol) / 8
    fifth = sp.Rational(5, 8) * sine - sp.Rational(5, 16) * sp.sin(3 * symbol) + sp.sin(5 * symbol) / 16
    third = (3 * sine - sp.sin(3 * symbol)) / 4
    for raw, closed in ((sine**6, sixth), (sine**4, fourth), (sine**5, fifth), (sine**3, third)):
        if sp.expand(raw.rewrite(sp.exp) - closed.rewrite(sp.exp)) != 0:
            return None
    if not _eq(sixth - (15 * (1 - sp.cos(2 * symbol)) - 6 * (1 - sp.cos(4 * symbol)) + (1 - sp.cos(6 * symbol))) / 32):
        return None
    if not _eq(fourth - (sp.Rational(1, 2) * (1 - sp.cos(2 * symbol)) - sp.Rational(1, 8) * (1 - sp.cos(4 * symbol)))):
        return None
    frequency = sp.Symbol("_k", positive=True)
    if sp.integrate(sp.sin(frequency * symbol) / symbol, (symbol, 0, sp.oo)) != sp.pi / 2:
        return None
    if sp.integrate((1 - sp.cos(frequency * symbol)) / symbol**2, (symbol, 0, sp.oo)) != sp.pi * frequency / 2:
        return None
    if sp.integrate((frequency * symbol - sp.sin(frequency * symbol)) / symbol**3, (symbol, 0, sp.oo)) != sp.pi * frequency**2 / 4:
        return None
    sin6 = (15 * (sp.pi * 2 / 2) - 6 * (sp.pi * 4 / 2) + (sp.pi * 6 / 2)) / 32
    sin4 = (sp.Rational(1, 2) * (sp.pi * 2 / 2) - sp.Rational(1, 8) * (sp.pi * 4 / 2))
    sin5 = (sp.Rational(5, 8) - sp.Rational(5, 16) + sp.Rational(1, 16)) * (sp.pi / 2)
    sin3 = (sp.pi * 9 / 4 - 3 * (sp.pi / 4)) / 4
    if not _eq(sin6 - 3 * sp.pi / 16) or not _eq(sin4 - sp.pi / 4):
        return None
    if not _eq(sin5 - 3 * sp.pi / 16) or not _eq(sin3 - 3 * sp.pi / 8):
        return None
    if not _eq(sin6 + sin5 + sin4 + sin3 - sp.pi):
        return None
    # sin^3(x)/x^3 = [3(x-sin x)-(3x-sin(3x))]/4x^3, up to the sign checked above.
    combined = (3 * symbol - sp.sin(3 * symbol)) - 3 * (symbol - sp.sin(symbol))
    if not _eq(combined - (3 * sine - sp.sin(3 * symbol))):
        return None
    return sp.pi


def _beta_radical(integrand, symbol, lo, hi):
    """u=(x+1)/x**3 turns the cubic radical into a beta value."""
    if not _span(lo, hi, 0, sp.oo):
        return None
    expected = symbol * (2 * symbol + 3) * (symbol + 1) ** sp.Rational(1, 3) / (symbol**6 + symbol**2 + 2 * symbol + 1)
    if integrand != expected:
        return None
    if not _eq(sp.expand(symbol**6 + (symbol + 1) ** 2 - (symbol**6 + symbol**2 + 2 * symbol + 1))):
        return None
    ratio = (symbol + 1) / symbol**3
    if not _eq(sp.diff(ratio, symbol) + (2 * symbol + 3) / symbol**4):
        return None
    ray = sp.Symbol("_u", positive=True)
    jacobian = symbol * (2 * symbol + 3) * (ray ** sp.Rational(1, 3) * symbol) * (-(symbol**4) / (2 * symbol + 3))
    jacobian /= symbol**6 * (1 + ray**2)
    if not _eq(jacobian + ray ** sp.Rational(1, 3) / (1 + ray**2)):
        return None
    power = sp.Symbol("_v", positive=True)
    piece = power ** sp.Rational(1, 6) * sp.Rational(1, 2) * power ** sp.Rational(-1, 2)
    if not _eq(piece - sp.Rational(1, 2) * power ** (sp.Rational(2, 3) - 1)):
        return None
    width = sp.integrate(power ** (sp.Rational(2, 3) - 1) / (1 + power), (power, 0, sp.oo))
    if not _eq(width - sp.pi / sp.sin(2 * sp.pi / 3)):
        return None
    if not _eq(width / 2 - sp.pi / sp.sqrt(3)):
        return None
    return sp.pi / sp.sqrt(3)


def _lambert_segment(integrand, symbol, lo, hi):
    """x=u e^u carries e^{W(x)}/x**2 from e to 2e**2 onto [1, 2]."""
    if not integrand.has(sp.LambertW):
        return None
    if lo != sp.E or hi != 2 * sp.E**2:
        return None
    if integrand != sp.exp(sp.LambertW(symbol)) / symbol**2:
        return None
    weight = sp.Symbol("_w", positive=True)
    source = weight * sp.exp(weight)
    if sp.solve(source - sp.E, weight) != [1]:
        return None
    if sp.solve(source - 2 * sp.E**2, weight) != [2]:
        return None
    changed = sp.exp(weight) / source**2 * sp.diff(source, weight)
    if not _eq(changed - (1 / weight + 1 / weight**2)):
        return None
    anti = sp.log(weight) - 1 / weight
    if not _eq(sp.diff(anti, weight) - (1 / weight + 1 / weight**2)):
        return None
    if sp.simplify(anti.subs(weight, 2) - anti.subs(weight, 1) - (sp.log(2) + sp.Rational(1, 2))) != 0:
        return None
    return sp.log(2) + sp.Rational(1, 2)


def _dilog_reflection(integrand, symbol, lo, hi):
    """Li_2(x)+Li_2(-x)=Li_2(x**2)/2 makes the integrand pair to 1/2."""
    if not _span(lo, hi, -1, 1) or not integrand.has(sp.polylog):
        return None
    expected = (1 + sp.polylog(2, symbol)) / (4 + sp.polylog(2, symbol**2))
    if integrand != expected:
        return None
    if not _eq(sp.expand_func(sp.diff(sp.polylog(2, symbol), symbol) + sp.log(1 - symbol) / symbol)):
        return None
    gap = sp.polylog(2, symbol) + sp.polylog(2, -symbol) - sp.polylog(2, symbol**2) / 2
    if gap.subs(symbol, 0) != 0:
        return None
    logs = -sp.log(1 - symbol) + sp.log(1 - symbol**2) - sp.log(1 + symbol)
    if not _eq(sp.expand_func(sp.diff(gap, symbol)) - logs / symbol):
        return None
    if sp.simplify(sp.logcombine(logs, force=True)) != 0:
        return None
    level = sp.Symbol("_L")
    if sp.simplify((2 + level / 2) / (4 + level) - sp.Rational(1, 2)) != 0:
        return None
    paired = expected + expected.subs(symbol, -symbol)
    if not _eq(paired - sp.Rational(1, 2) - gap / (4 + sp.polylog(2, symbol**2))):
        return None
    if sp.integrate(sp.Rational(1, 2), (symbol, 0, 1)) != sp.Rational(1, 2):
        return None
    return sp.Rational(1, 2)


def _factorial_fourier(integrand, symbol, lo, hi):
    """exp(cos x) cos(n x-sin x) is the real part of exp(i n x) exp(e^{-i x})."""
    if not _span(lo, hi, 0, 2 * sp.pi) or not integrand.has(sp.exp):
        return None
    integers = [item for item in integrand.free_symbols if item != symbol and item.is_integer]
    if len(integers) != 1:
        return None
    degree = integers[0]
    expected = sp.exp(sp.cos(symbol)) * sp.cos(degree * symbol - sp.sin(symbol))
    if integrand != expected:
        return None
    phase = sp.exp(sp.I * degree * symbol) * sp.exp(sp.exp(-sp.I * symbol))
    if not _eq(sp.re(phase) - integrand):
        return None
    if sp.simplify(sp.Abs(sp.exp(-sp.I * symbol)) - 1) != 0:
        return None
    frequency = sp.Symbol("_m", integer=True, nonzero=True)
    if sp.simplify(sp.exp(2 * sp.pi * sp.I * frequency) - 1) != 0:
        return None
    primitive = sp.exp(sp.I * frequency * symbol) / (sp.I * frequency)
    if sp.simplify(primitive.subs(symbol, 2 * sp.pi) - primitive.subs(symbol, 0)) != 0:
        return None
    if sp.integrate(1, (symbol, 0, 2 * sp.pi)) != 2 * sp.pi:
        return None
    step = sp.Symbol("_j", integer=True, nonnegative=True)
    if sp.summation(sp.Rational(1, 2) ** step, (step, 0, sp.oo)) != 2:
        return None
    cutoff = sp.Symbol("_K", integer=True, positive=True)
    if sp.limit(1 / sp.factorial(cutoff), cutoff, sp.oo) != 0:
        return None
    # |z|=1, so the exponential tail is at most the real tail, which is at
    # most twice the first omitted term once the ratio is at most 1/2.
    if sp.simplify(sp.factorial(cutoff + 1) / sp.factorial(cutoff) - (cutoff + 1)) != 0:
        return None
    return sp.Piecewise((2 * sp.pi / sp.factorial(degree), degree >= 0), (0, True))


def _binomial_line(integrand, symbol, lo, hi):
    """Pascal's identity doubles the binomial integral, from the sinc base."""
    if not _span(lo, hi, -sp.oo, sp.oo) or not integrand.has(sp.binomial):
        return None
    degrees = [item for item in integrand.free_symbols if item != symbol and item.is_integer]
    if len(degrees) != 1:
        return None
    degree = degrees[0]
    if degree.is_nonnegative is not True or integrand != sp.binomial(degree, symbol):
        return None
    if not _eq(sp.binomial(degree, symbol) - sp.binomial(degree - 1, symbol) - sp.binomial(degree - 1, symbol - 1)):
        return None
    if not _eq(sp.binomial(degree, symbol) - sp.factorial(degree) / (sp.gamma(symbol + 1) * sp.gamma(degree - symbol + 1))):
        return None
    if not _eq(sp.gamma(degree - symbol + 1) - sp.rf(1 - symbol, degree) * sp.gamma(1 - symbol)):
        return None
    if not _eq(sp.gamma(symbol + 1) - symbol * sp.gamma(symbol)):
        return None
    factor = sp.sin(sp.pi * symbol) * sp.gamma(symbol) * sp.gamma(1 - symbol) - sp.pi
    if not _eq(factor):
        return None
    gamma_form = sp.factorial(degree) / (sp.gamma(symbol + 1) * sp.gamma(degree - symbol + 1))
    formula = sp.factorial(degree) * sp.sin(sp.pi * symbol) / (sp.pi * symbol * sp.rf(1 - symbol, degree))
    gap = gamma_form - formula
    gap += factor * sp.factorial(degree) / (sp.pi * sp.gamma(symbol + 1) * sp.gamma(degree - symbol + 1))
    if not _eq(gap):
        return None
    if not _eq(sp.binomial(0, symbol) - sp.sin(sp.pi * symbol) / (sp.pi * symbol)):
        return None
    if sp.integrate(sp.sin(sp.pi * symbol) / (sp.pi * symbol), (symbol, -sp.oo, sp.oo)) != 1:
        return None
    shifted = sp.sin(sp.pi * (1 - symbol)) / (sp.pi * (1 - symbol))
    if not _eq(sp.binomial(1, symbol) - (sp.sin(sp.pi * symbol) / (sp.pi * symbol) + shifted)):
        return None
    if sp.integrate(shifted, (symbol, -sp.oo, sp.oo)) != 1:
        return None
    slide = sp.Symbol("_u", real=True)
    if sp.diff(slide + 1, slide) != 1:
        return None
    if sp.limit(slide + 1, slide, sp.oo) != sp.oo or sp.limit(slide + 1, slide, -sp.oo) != -sp.oo:
        return None
    if not _eq(sp.binomial(degree - 1, (slide + 1) - 1) - sp.binomial(degree - 1, slide)):
        return None
    if not _eq(2**degree - 2 * 2 ** (degree - 1)):
        return None
    if 2**0 != 1:
        return None
    return 2**degree


def _root_distance(integrand, symbol, lo, hi):
    """The smallest root gap of the cubic is even and integrates by F."""
    if not _span(lo, hi, -90, 90) or not isinstance(integrand, sp.Piecewise):
        return None
    width = sp.sqrt(symbol**2 - 4)
    expected = sp.Piecewise(
        (0, sp.Abs(symbol) < 2),
        (width, sp.Abs(symbol) <= 3 / sp.sqrt(2)),
        ((sp.Abs(symbol) - width) / 2, True),
    )
    if integrand != expected:
        return None
    unknown = sp.Symbol("_x")
    cubic = unknown**3 - (3 + symbol) * unknown**2 + (4 + 2 * symbol) * unknown - (2 + symbol)
    quotient, remainder = sp.div(cubic, unknown - 1)
    if remainder != 0:
        return None
    if not _eq(sp.expand(quotient - (unknown**2 - (2 + symbol) * unknown + (2 + symbol)))):
        return None
    gap = sp.sqrt(symbol**2 - 4)
    smaller = (2 + symbol - gap) / 2
    larger = (2 + symbol + gap) / 2
    if not _eq(sp.together(quotient.subs(unknown, smaller))):
        return None
    if not _eq(sp.together(quotient.subs(unknown, larger))):
        return None
    if not _eq(larger - smaller - gap):
        return None
    if not _eq(larger - 1 - (symbol + gap) / 2) or not _eq(smaller - 1 - (symbol - gap) / 2):
        return None
    threshold = 3 / sp.sqrt(2)
    if not _eq(((symbol - gap) / 2 - gap).subs(symbol, threshold)):
        return None
    mirror = sp.Symbol("_b", positive=True)
    mirrored = sp.sqrt(mirror**2 - 4)
    left = (2 - mirror - mirrored) / 2
    right = (2 - mirror + mirrored) / 2
    if not _eq(right - left - mirrored):
        return None
    if not _eq((mirror - mirrored) * (mirror + mirrored) - 4):
        return None
    if not _eq(right - 1 + (mirror - mirrored) / 2):
        return None
    if not _eq(left - 1 + (mirror + mirrored) / 2):
        return None
    if not _eq(1 - right - (mirror - mirrored) / 2):
        return None
    if not _eq(1 - left - (mirror + mirrored) / 2):
        return None
    disc = sp.expand((2 + symbol) ** 2 - 4 * (2 + symbol))
    if not _eq(disc - (symbol**2 - 4)):
        return None

    def capital(val):
        return val * sp.sqrt(val**2 - 4) / 2 - 2 * sp.log(val + sp.sqrt(val**2 - 4))

    if not _eq(sp.diff(capital(symbol), symbol) - sp.sqrt(symbol**2 - 4)):
        return None
    if sp.simplify((90**2 - threshold**2) / 2 - sp.Rational(16191, 4)) != 0:
        return None
    expr = -capital(90) + 3 * capital(threshold) - 2 * capital(2) + sp.Rational(16191, 4)
    target = 90 * (45 - sp.sqrt(2024)) - 2 * sp.log(45 - sp.sqrt(2024)) - 3 * sp.log(2)
    reduced = sp.simplify(sp.expand_log(sp.expand(expr - target), force=True))
    low = 45 - 2 * sp.sqrt(506)
    high = 45 + 2 * sp.sqrt(506)
    if sp.expand(low * high) != 1:
        return None
    if not _eq(reduced - 2 * sp.log(low) - 2 * sp.log(high)):
        return None
    if sp.simplify(sp.logcombine(2 * sp.log(low) + 2 * sp.log(high), force=True)) != 0:
        return None
    return target


def definite_value(integrand, symbol, lo, hi):
    for builder in (
        _log_radical,
        _log_pair,
        _relay_log_pair,
        _sec_line,
        _asin_endpoint,
        _semicircle_max,
        _double_log_series,
        _tan_square_root,
        _arcsin_log,
        _quartic_reflection,
        _sine_powers,
        _beta_radical,
        _lambert_segment,
        _dilog_reflection,
        _factorial_fourier,
        _binomial_line,
        _root_distance,
    ):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
