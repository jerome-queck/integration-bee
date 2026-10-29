"""Exact certificates for answered Yang rows.

Example 3 stays a shifted-parity match on its printed integrand and [0, 6].
Lane L2 proves §1.4 item 3, (2^x + 3^x)/5^x on [0, ∞), by splitting it into
two exponential rays. Lane L5 adds shape-matched proofs for printed integrals
in §§1.12, 1.15, 1.17, 1.18, and 1.20. Lane L6 adds the tangent substitution
for §2.4 item 12. Lane L7 adds three §2.6 proofs: a nested radical under
sec(x)^2, an elliptic antiderivative of 1/sqrt(3 sin x + cos x), and
log(2 cos(x)^2 - 1) cos(x) on [0, π/4]. Each builder returns None before any
integration unless the integrand and endpoints match, because this function
runs for every definite row.
"""

from __future__ import annotations

import sympy as sp


def _zero(expr) -> bool:
    if expr == 0 or sp.simplify(expr) == 0:
        return True
    if expr.has(sp.sin, sp.cos, sp.tan, sp.exp, sp.log):
        try:
            if sp.trigsimp(expr) == 0 or sp.simplify(sp.trigsimp(expr)) == 0:
                return True
        except Exception:
            return False
    return False


def _closed(expr) -> bool:
    return expr is not None and not expr.has(sp.Integral, sp.Sum, sp.Product, sp.Limit)


def _affine_sign(expr, symbol, lo, hi):
    """1 when a degree-at-most-1 polynomial stays nonnegative, -1 when nonpositive."""
    expanded = sp.expand(expr)
    if not expanded.is_polynomial(symbol):
        return None
    polynomial = sp.Poly(expanded, symbol)
    if polynomial.degree() > 1:
        return None
    left = sp.simplify(expanded.subs(symbol, lo))
    right = sp.simplify(expanded.subs(symbol, hi))
    if left >= 0 and right >= 0:
        return 1
    if left <= 0 and right <= 0:
        return -1
    return None


def _abs_affine(expr, symbol, lo, hi):
    """Replace Abs of an affine expression by the sign it keeps on [lo, hi]."""
    if not isinstance(expr, sp.Abs) or len(expr.args) != 1:
        return None
    sign = _affine_sign(expr.args[0], symbol, lo, hi)
    if sign is None:
        return None
    return sp.simplify(sign * expr.args[0])


def _ftc(primitive, symbol, lo, hi, integrand):
    if not _zero(sp.diff(primitive, symbol) - integrand):
        return None
    value = sp.simplify(primitive.subs(symbol, hi) - primitive.subs(symbol, lo))
    if not _closed(value):
        return None
    return value


def _shifted_parity(integrand, symbol, lo, hi):
    """Yang 1.3 Example 3. Odd terms on [-3, 3] drop out, leaving atan."""
    if (lo, hi) != (0, 6) or symbol.is_real is not True:
        return None
    denominator = symbol**2 - 6 * symbol + 10
    target = ((symbol - 2) * (symbol - 3) * (symbol - 4) + 1) / denominator
    if integrand != target:
        return None

    u = sp.Dummy("u", real=True)
    substitution = u + 3
    lower, upper = lo - 3, hi - 3
    if (lower, upper) != (-3, 3) or sp.diff(substitution, u) != 1:
        return None
    shifted_denominator = sp.expand(denominator.subs(symbol, substitution))
    if shifted_denominator != u**2 + 1 or shifted_denominator.is_positive is not True:
        return None

    # The substitution maps [0, 6] to [-3, 3]. Its denominator is positive,
    # so all terms below are continuous and their ordinary integrals exist.
    shifted = integrand.subs(symbol, substitution)
    odd = u - 2 * u / (u**2 + 1)
    even = 1 / (u**2 + 1)
    if sp.cancel(shifted - odd - even) != 0:
        return None
    if sp.cancel(odd.subs(u, -u) + odd) != 0:
        return None
    # Reflecting u -> -u negates the odd part over the same interval, hence
    # its integral is zero. Only the explicitly checked even primitive remains.
    primitive = sp.atan(u)
    if sp.cancel(sp.diff(primitive, u) - even) != 0:
        return None
    return primitive.subs(u, upper) - primitive.subs(u, lower)


def _abs_exp_segment(integrand, symbol, lo, hi):
    """∫_{-1}^{1} |e^x - 1| dx. The exponential is below 1 on the left and above 1 on the right."""
    if (lo, hi) != (-1, 1) or integrand != sp.Abs(sp.exp(symbol) - 1):
        return None
    # ∫_0^h e^t dt = e^h - 1. The integrand is positive, so e^h - 1 >= 0 for h >= 0
    # and |e^x - 1| = e^x - 1 on [0, 1].
    step = sp.Dummy("s", real=True)
    height = sp.symbols("h", nonnegative=True)
    rise = sp.integrate(sp.exp(step), (step, 0, height))
    if not _zero(rise - (sp.exp(height) - 1)) or sp.exp(step).is_positive is not True:
        return None
    right = _ftc(sp.exp(symbol) - symbol, symbol, 0, 1, sp.exp(symbol) - 1)
    # The same integral with e^{-t} gives 1 - e^{-u} >= 0, so |e^{-u} - 1| = 1 - e^{-u}.
    decay = sp.integrate(sp.exp(-step), (step, 0, height))
    if not _zero(decay - (1 - sp.exp(-height))):
        return None
    line = sp.Dummy("u", real=True)
    if sp.diff(-line, line) != -1:
        return None
    left = _ftc(line + sp.exp(-line), line, 0, 1, 1 - sp.exp(-line))
    if left is None or right is None:
        return None
    total = sp.simplify(left + right)
    clean = sp.E + sp.exp(-1) - 2
    if not _zero(total - clean):
        return None
    return clean


def _abs_sine_periods(integrand, symbol, lo, hi):
    """∫_{-2π}^{2π} |sin x| dx by four shifts onto [0, π], where sin stays nonnegative.

    SymPy's direct integrator returns 4 on this interval. The value checked here is 8.
    """
    if integrand != sp.Abs(sp.sin(symbol)) or lo != -2 * sp.pi or hi != 2 * sp.pi:
        return None
    if sp.calculus.util.minimum(sp.sin(symbol), symbol, sp.Interval(0, sp.pi)) != 0:
        return None
    angle = sp.Dummy("t", real=True)
    total = 0
    for index in (-2, -1, 0, 1):
        # A Python power of -1 is a float for a negative exponent. Keep the sign exact.
        sign = sp.Integer(-1) ** index
        if not _zero(sp.sin(index * sp.pi + angle) - sign * sp.sin(angle)):
            return None
        if sp.cos(index * sp.pi) != sign or sp.cos((index + 1) * sp.pi) != -sign:
            return None
        # |sin(kπ + t)| = sin t on [0, π], and sign * sin(kπ + t) = sin t.
        signed = sign * sp.sin(symbol)
        piece = _ftc(-sign * sp.cos(symbol), symbol, index * sp.pi, (index + 1) * sp.pi, signed)
        if piece != 2:
            return None
        total += piece
    return total


def _abs_linear_quotient(integrand, symbol, lo, hi):
    """∫_0^4 |x-1| / (|x-2| + |x-3|) dx, split where each absolute value is affine."""
    target = sp.Abs(symbol - 1) / (sp.Abs(symbol - 2) + sp.Abs(symbol - 3))
    if (lo, hi) != (0, 4) or integrand != target:
        return None
    cuts = (0, 1, 2, 3, 4)
    total = 0
    for left, right in zip(cuts, cuts[1:]):
        numerator = _abs_affine(sp.Abs(symbol - 1), symbol, left, right)
        first = _abs_affine(sp.Abs(symbol - 2), symbol, left, right)
        second = _abs_affine(sp.Abs(symbol - 3), symbol, left, right)
        if numerator is None or first is None or second is None:
            return None
        denominator = sp.simplify(first + second)
        if _affine_sign(denominator, symbol, left, right) != 1:
            return None
        piece_integrand = sp.simplify(numerator / denominator)
        if not _zero(piece_integrand * denominator - numerator):
            return None
        value = sp.integrate(piece_integrand, (symbol, left, right))
        if not _closed(value):
            return None
        total += value
    clean = 2 + sp.Rational(9, 4) * sp.log(3) - sp.Rational(3, 4) * sp.log(5)
    if not _zero(total - clean):
        return None
    return clean


def _log_abs_clears(integrand, symbol, lo, hi):
    """∫_1^e (x+1) / (|x - ln x| + ln x) dx. On [1, e], x - ln x is at least 1."""
    target = (symbol + 1) / (sp.Abs(symbol - sp.log(symbol)) + sp.log(symbol))
    if (lo, hi) != (1, sp.E) or integrand != target:
        return None
    gap = symbol - sp.log(symbol)
    slope = sp.together(sp.diff(gap, symbol))
    if slope != (symbol - 1) / symbol:
        return None
    if _affine_sign(symbol - 1, symbol, 1, sp.E) != 1 or _affine_sign(symbol, symbol, 1, sp.E) != 1:
        return None
    # (x-1)/x >= 0 on [1, e], so x - ln x increases from 1 to e - 1 and stays at least 1.
    if gap.subs(symbol, 1) != 1 or sp.simplify(gap.subs(symbol, sp.E) - (sp.E - 1)) != 0:
        return None
    reduced = (symbol + 1) / symbol
    if not _zero(sp.together(target.subs(sp.Abs(gap), gap) - reduced)):
        return None
    return _ftc(symbol + sp.log(symbol), symbol, 1, sp.E, reduced)


def _sqrt_shift_abs(integrand, symbol, lo, hi):
    """∫_0^{16} |√x - 2| dx. Squaring compares √x with 2 on [0, 4] and [4, 16]."""
    if (lo, hi) != (0, 16) or integrand != sp.Abs(sp.sqrt(symbol) - 2):
        return None
    if sp.sqrt(4) != 2 or not _zero(sp.sqrt(symbol) ** 2 - symbol):
        return None
    base, height = sp.symbols("a b", nonnegative=True)
    if base.is_nonnegative is not True or height.is_nonnegative is not True:
        return None
    if (base + height).is_nonnegative is not True:
        return None
    if sp.expand(height**2 - base**2 - (height - base) * (height + base)) != 0:
        return None
    # a and b are nonnegative, so a + b is too, and a^2 <= b^2 exactly when a <= b.
    # Therefore √x <= 2 on an interval exactly when x <= 4.
    total = 0
    for left, right, expect_sign in ((0, 4, -1), (4, 16, 1)):
        if _affine_sign(symbol - 4, symbol, left, right) != expect_sign:
            return None
        signed = expect_sign * (sp.sqrt(symbol) - 2)
        primitive = expect_sign * (sp.Rational(2, 3) * symbol ** sp.Rational(3, 2) - 2 * symbol)
        value = _ftc(primitive, symbol, left, right, signed)
        if value is None:
            return None
        total += value
    return sp.simplify(total)


def _sec_radical_quarter(integrand, symbol, lo, hi):
    """∫_0^{π/6} √(1/(1-sin x) + 1/(1+sin x)) dx = √2 ∫ sec x dx."""
    target = sp.sqrt(1 / (1 - sp.sin(symbol)) + 1 / (1 + sp.sin(symbol)))
    if lo != 0 or hi != sp.pi / 6 or integrand != target:
        return None
    if not _zero(sp.together(target**2 - 2 / sp.cos(symbol) ** 2)):
        return None
    if sp.calculus.util.minimum(sp.cos(symbol), symbol, sp.Interval(0, sp.pi / 6)) != sp.sqrt(3) / 2:
        return None
    reduced = sp.sqrt(2) / sp.cos(symbol)
    if not _zero(reduced**2 - target**2):
        return None
    # Both sides are positive on [0, π/6]: cos stays at least √3/2, and the square root is nonnegative.
    primitive = sp.sqrt(2) * sp.log(sp.sec(symbol) + sp.tan(symbol))
    return _ftc(primitive, symbol, 0, sp.pi / 6, reduced)


def _inverse_log_pair(integrand, symbol, lo, hi):
    """∫_0^1 (ln(2)^2 2^{√x} + ln(1+x)^2) dx by splitting the first term."""
    target = sp.log(2) ** 2 * 2 ** sp.sqrt(symbol) + sp.log(1 + symbol) ** 2
    if (lo, hi) != (0, 1) or integrand != target:
        return None
    parameter = sp.Dummy("u", real=True)
    bound = sp.log(2) ** 2
    substitution = parameter / bound
    if sp.diff(substitution, parameter) != 1 / bound:
        return None
    pulled = sp.simplify(
        (sp.log(2) ** 2 * 2 ** sp.sqrt(symbol)).subs(symbol, substitution) * sp.diff(substitution, parameter)
    )
    if not _zero(pulled - sp.exp(sp.sqrt(parameter))):
        return None
    if substitution.subs(parameter, 0) != 0 or substitution.subs(parameter, bound) != 1:
        return None
    first = sp.integrate(sp.exp(sp.sqrt(parameter)), (parameter, 0, bound))
    second = sp.integrate(sp.log(1 + symbol) ** 2, (symbol, 0, 1))
    if not _closed(first) or not _closed(second):
        return None
    return sp.simplify(first + second)


def _king_log_half(integrand, symbol, lo, hi):
    """∫_0^1 ln(x+1) / ln(2 + x - x^2) dx. The reflected sum is 1, so the integral is 1/2."""
    target = sp.log(symbol + 1) / sp.log(2 + symbol - symbol**2)
    if (lo, hi) != (0, 1) or integrand != target:
        return None
    factors = (1 + symbol) * (2 - symbol)
    if sp.expand(factors - (2 + symbol - symbol**2)) != 0:
        return None
    if _affine_sign(1 + symbol, symbol, 0, 1) != 1 or _affine_sign(2 - symbol, symbol, 0, 1) != 1:
        return None
    split = sp.log(1 + symbol) + sp.log(2 - symbol)
    if not _zero(sp.exp(split - sp.log(factors)) - 1):
        return None
    # The factors are positive on [0, 1] and multiply to the quadratic, so the
    # denominator ln(2 + x - x^2) is the sum of logarithms above.
    reduced = sp.log(1 + symbol) / split
    reflected = sp.simplify(reduced.subs(symbol, 1 - symbol))
    if not _zero(reduced + reflected - 1):
        return None
    if sp.diff(1 - symbol, symbol) != -1:
        return None
    # u = 1 - x swaps the endpoints and preserves the integral, so twice the integral is ∫_0^1 1 dx.
    width = _ftc(symbol, symbol, 0, 1, sp.Integer(1))
    if width != 1:
        return None
    return sp.Rational(1, 2)


def _sqrt_log_ray(integrand, symbol, lo, hi):
    """∫_0^∞ ln(√x + 1) / (x √x) dx diverges. The substituted antiderivative tends to -∞ at 0."""
    target = sp.log(sp.sqrt(symbol) + 1) / (symbol * sp.sqrt(symbol))
    if lo != 0 or hi != sp.oo or integrand != target:
        return None
    parameter = sp.Dummy("t", positive=True)
    jacobian = sp.diff(parameter**2, parameter)
    if jacobian != 2 * parameter or _affine_sign(parameter, parameter, 0, 1) != 1:
        return None
    substituted = sp.simplify(target.subs(symbol, parameter**2) * jacobian)
    reduced = 2 * sp.log(1 + parameter) / parameter**2
    if not _zero(substituted - reduced):
        return None
    primitive = 2 * (-sp.log(1 + parameter) / parameter + sp.log(parameter) - sp.log(1 + parameter))
    if not _zero(sp.diff(primitive, parameter) - reduced):
        return None
    if sp.limit(primitive, parameter, sp.oo) != 0:
        return None
    if sp.limit(primitive, parameter, 0, dir="+") != -sp.oo:
        return None
    return sp.oo


def _gaussian_polynomial_tail(integrand, symbol, lo, hi):
    """∫_{-1}^∞ e^{-x^2} (5x^4 - 2x^6) dx is the tail of x^5 e^{-x^2}."""
    target = sp.exp(-(symbol**2)) * (5 * symbol**4 - 2 * symbol**6)
    if lo != -1 or hi != sp.oo or integrand != target:
        return None
    primitive = symbol**5 * sp.exp(-(symbol**2))
    if not _zero(sp.diff(primitive, symbol) - target):
        return None
    if sp.limit(primitive, symbol, sp.oo) != 0:
        return None
    lower = sp.simplify(primitive.subs(symbol, -1))
    if lower != -sp.exp(-1):
        return None
    return sp.simplify(0 - lower)


def _quartic_trig_period(integrand, symbol, lo, hi):
    """∫_0^{2π} dx / (sin^4 x + cos^4 x) reduces to four copies of ∫ dx / (3 + cos x)."""
    target = 1 / (sp.sin(symbol) ** 4 + sp.cos(symbol) ** 4)
    if lo != 0 or hi != 2 * sp.pi or integrand != target:
        return None
    if not _zero(sp.sin(symbol) ** 4 + sp.cos(symbol) ** 4 - (3 + sp.cos(4 * symbol)) / 4):
        return None
    reduced = 4 / (3 + sp.cos(4 * symbol))
    if not _zero(sp.together(target - reduced)):
        return None
    angle = sp.Dummy("u", real=True)
    if sp.diff(4 * symbol, symbol) != 4:
        return None
    stretched = sp.simplify(reduced.subs(symbol, angle / 4) * sp.diff(angle / 4, angle))
    if not _zero(stretched - 1 / (3 + sp.cos(angle))):
        return None
    period = sp.integrate(1 / (3 + sp.cos(angle)), (angle, 0, 2 * sp.pi))
    if not _closed(period):
        return None
    shift = sp.Dummy("s", real=True)
    for index in range(4):
        if not _zero(sp.cos(shift + 2 * sp.pi * index) - sp.cos(shift)):
            return None
    return sp.simplify(4 * period)


def _atan_log_line(integrand, symbol, lo, hi):
    """∫_0^∞ arctan(x) / (x (ln(x)^2 + 1)) dx = π^2/4 after x = e^t."""
    target = sp.atan(symbol) / (symbol * (sp.log(symbol) ** 2 + 1))
    if lo != 0 or hi != sp.oo or integrand != target:
        return None
    parameter = sp.Dummy("t", real=True)
    substituted = sp.simplify(target.subs(symbol, sp.exp(parameter)) * sp.exp(parameter))
    weight = sp.atan(sp.exp(parameter)) / (parameter**2 + 1)
    if not _zero(substituted - weight):
        return None
    pair = sp.atan(sp.exp(parameter)) + sp.atan(sp.exp(-parameter))
    if not _zero(sp.diff(pair, parameter)) or pair.subs(parameter, 0) != sp.pi / 2:
        return None
    # The derivative vanishes on the real line and the value at 0 is π/2, so the sum is π/2.
    reflected = weight.subs(parameter, -parameter)
    if not _zero(sp.together((weight + reflected) * (parameter**2 + 1) - pair)):
        return None
    if sp.diff(-parameter, parameter) != -1:
        return None
    line = sp.integrate(1 / (parameter**2 + 1), (parameter, -sp.oo, sp.oo))
    if line != sp.pi:
        return None
    return sp.simplify(line * sp.pi / 4)


def _log_cubic_unit(integrand, symbol, lo, hi):
    """∫_0^1 ln(1 + x + x^2) / x dx = ∫ (ln(1-x^3) - ln(1-x)) / x dx = π^2/9."""
    target = sp.log(1 + symbol + symbol**2) / symbol
    if (lo, hi) != (0, 1) or integrand != target:
        return None
    if sp.expand((1 - symbol**3) - (1 - symbol) * (1 + symbol + symbol**2)) != 0:
        return None
    difference = sp.log(1 - symbol**3) - sp.log(1 - symbol)
    if not _zero(sp.exp(difference - sp.log(1 + symbol + symbol**2)) - 1):
        return None
    first = sp.integrate(sp.log(1 - symbol**3) / symbol, (symbol, 0, 1))
    second = sp.integrate(sp.log(1 - symbol) / symbol, (symbol, 0, 1))
    if not _closed(first) or not _closed(second):
        return None
    return sp.simplify(first - second)


def _sec_tan_sixth(integrand, symbol, lo, hi):
    """Return ∫_0^{π/2} sec(x)^6 exp(-tan x) dx, or None on a shape miss.

    On [0, π/2), tan is a bijection onto [0, ∞) and its derivative is sec^2.
    sec^6 = (1+tan^2)^2 sec^2, so the integrand dx is (1+u^2)^2 e^{-u} du.
    """
    if symbol.is_real is not True or lo != 0 or hi != sp.pi / 2:
        return None
    target = sp.exp(-sp.tan(symbol)) * sp.sec(symbol) ** 6
    if integrand != target:
        return None
    sec2 = sp.sec(symbol) ** 2
    trig = 1 + sp.tan(symbol) ** 2
    if sp.simplify(sec2 - trig) != 0:
        return None
    if sp.simplify(sp.diff(sp.tan(symbol), symbol) - sec2) != 0:
        return None
    if sp.tan(symbol).subs(symbol, 0) != 0:
        return None
    if sp.limit(sp.tan(symbol), symbol, sp.pi / 2, dir="-") != sp.oo:
        return None
    # One factor of sec^2 is the measure du. The remaining power is (1+u^2)^2.
    if sp.simplify(sp.sec(symbol) ** 6 - trig ** 2 * sec2) != 0:
        return None
    parameter = sp.Dummy("u", positive=True)
    reduced = (1 + parameter ** 2) ** 2 * sp.exp(-parameter)
    polynomial = sp.expand((1 + parameter ** 2) ** 2)
    if polynomial != 1 + 2 * parameter ** 2 + parameter ** 4:
        return None
    if sp.expand(reduced) != sp.expand(polynomial * sp.exp(-parameter)):
        return None
    value = sp.integrate(reduced, (parameter, 0, sp.oo))
    if not getattr(value, "is_number", False) or value.has(sp.Integral):
        return None
    return value


def _two_five_power_ray(integrand, symbol, lo, hi):
    """Return ∫_0^∞ (2^x + 3^x)/5^x dx, or None on a shape miss.

    For a positive base, a^x = exp(x log a). The printed quotient is the sum
    of exp(-x log(5/2)) and exp(-x log(5/3)). Each coefficient is positive,
    so the antiderivative vanishes at infinity and equals 1/c at the origin.
    """
    if symbol.is_real is not True or lo != 0 or hi != sp.oo:
        return None
    target = (2**symbol + 3**symbol) / 5**symbol
    if integrand != target:
        return None
    rewritten = (sp.exp(symbol * sp.log(2)) + sp.exp(symbol * sp.log(3))) * sp.exp(-symbol * sp.log(5))
    if sp.simplify(integrand - rewritten) != 0:
        return None
    terms = (
        (sp.Rational(5, 2), sp.exp(-symbol * sp.log(sp.Rational(5, 2)))),
        (sp.Rational(5, 3), sp.exp(-symbol * sp.log(sp.Rational(5, 3)))),
    )
    if sp.simplify(rewritten - terms[0][1] - terms[1][1]) != 0:
        return None
    total = 0
    for base, term in terms:
        coefficient = sp.log(base)
        if coefficient.is_positive is not True:
            return None
        primitive = -sp.exp(-coefficient * symbol) / coefficient
        if sp.simplify(sp.diff(primitive, symbol) - term) != 0:
            return None
        if sp.limit(primitive, symbol, sp.oo) != 0:
            return None
        piece = -primitive.subs(symbol, 0)
        if sp.simplify(piece - 1 / coefficient) != 0:
            return None
        total += piece
    expected = 1 / sp.log(sp.Rational(5, 2)) + 1 / sp.log(sp.Rational(5, 3))
    if sp.simplify(total - expected) != 0:
        return None
    return expected

def _exact(expression) -> bool:
    return expression == 0 or sp.simplify(expression) == 0


def _matches(answer, wanted) -> bool:
    return answer == wanted or _exact(answer - wanted)


def indefinite_ok(answer, integrand, symbol):
    """Return True for a checked §2.6 antiderivative, False on a bad final, None on a miss."""
    for checker in (_nested_sec_square, _linear_trig_radical):
        verdict = checker(answer, integrand, symbol)
        if verdict is not None:
            return verdict
    return None


def _nested_sec_square(answer, integrand, symbol):
    """∫ sec(x)^2 sqrt(tan(x) sqrt(tan(x) sqrt(tan(x) sin(x)))) dx.

    The printed nest and tan(x)^(7/8) sin(x)^(1/8) have the same eighth power.
    For positive factors the principal nest equals that power. Where sine and
    cosine are positive, the derivative of (8/15) sec(x)^(15/8) and the
    denested integrand both reduce to sin/cos^(23/8).
    """
    if symbol.is_real is not True:
        return None
    nest = sp.sqrt(
        sp.tan(symbol) * sp.sqrt(sp.tan(symbol) * sp.sqrt(sp.tan(symbol) * sp.sin(symbol)))
    )
    if integrand != sp.sec(symbol)**2 * nest:
        return None
    wanted = sp.Rational(8, 15) * sp.sec(symbol)**sp.Rational(15, 8)
    if not _matches(answer, wanted):
        return False
    if not _exact(nest**8 - sp.tan(symbol)**7 * sp.sin(symbol)):
        return False
    factor_t, factor_s = sp.symbols("yang_t yang_s", positive=True)
    positive_power = factor_t**sp.Rational(7, 8) * factor_s**sp.Rational(1, 8)
    # Positive bases denest the printed association to the principal power.
    if nest.subs({sp.tan(symbol): factor_t, sp.sin(symbol): factor_s}) != positive_power:
        return False
    slope = sp.tan(symbol) * sp.sec(symbol)**sp.Rational(15, 8)
    if sp.diff(wanted, symbol) != slope:
        return False
    sine, cosine = sp.symbols("yang_sin yang_cos", positive=True)
    replaced_slope = slope.subs({sp.tan(symbol): sine / cosine, sp.sec(symbol): 1 / cosine})
    denested = (
        sp.sec(symbol)**2
        * sp.tan(symbol)**sp.Rational(7, 8)
        * sp.sin(symbol)**sp.Rational(1, 8)
    )
    replaced_denested = denested.subs({
        sp.tan(symbol): sine / cosine,
        sp.sec(symbol): 1 / cosine,
        sp.sin(symbol): sine,
    })
    if sp.expand_power_exp(replaced_slope) != sp.expand_power_exp(replaced_denested):
        return False
    return True


def _linear_trig_radical(answer, integrand, symbol):
    """∫ dx/sqrt(3 sin x + cos x), via a phase shift and the Weierstrass pullback.

    3 sin x + cos x = sqrt(10) sin(x + arctan(1/3)). t = tan(θ/2) and s = sqrt(t)
    pull 1/sqrt(sin θ) back to 2 sqrt(2) / sqrt(1+s^4). The s-derivative of
    sqrt(2) elliptic_f(2 atan(s), 1/2) is that pullback, and multiplying by
    10^(-1/4) restores the phase-shifted factor.
    """
    if symbol.is_real is not True:
        return None
    if integrand != 1 / sp.sqrt(3 * sp.sin(symbol) + sp.cos(symbol)):
        return None
    alpha = sp.atan(sp.Rational(1, 3))
    amplitude = sp.sqrt(10)
    hole = sp.symbols("s", positive=True)
    primitive = sp.sqrt(2) * sp.elliptic_f(2 * sp.atan(hole), sp.Rational(1, 2))
    wanted = amplitude**(-sp.Rational(1, 2)) * primitive.subs(
        hole, sp.sqrt(sp.tan((symbol + alpha) / 2))
    )
    if not _matches(answer, wanted):
        return False
    if not _exact(amplitude * sp.sin(symbol + alpha) - (3 * sp.sin(symbol) + sp.cos(symbol))):
        return False
    if not _exact(sp.cos(alpha) - 3 / amplitude) or not _exact(sp.sin(alpha) - 1 / amplitude):
        return False
    if not _exact(amplitude**(-sp.Rational(1, 2)) - sp.Integer(10)**(-sp.Rational(1, 4))):
        return False
    theta = sp.symbols("theta", real=True)
    tangent = sp.tan(theta / 2)
    if not _exact(sp.sin(theta) - 2 * tangent / (1 + tangent**2)):
        return False
    if not _exact(sp.diff(tangent, theta) - (1 + tangent**2) / 2):
        return False
    positive_t = sp.symbols("T", positive=True)
    jacobian = (2 / (1 + positive_t**2)) / sp.sqrt(2 * positive_t / (1 + positive_t**2))
    pulled = sp.sqrt(2) / (sp.sqrt(positive_t) * sp.sqrt(1 + positive_t**2))
    if not _exact(jacobian - pulled):
        return False
    if not _exact(pulled.subs(positive_t, hole**2) * (2 * hole) - 2 * sp.sqrt(2) / sp.sqrt(1 + hole**4)):
        return False
    ds_dtheta = ((1 + hole**4) / 2) / (2 * hole)
    sine_in_s = 2 * hole**2 / (1 + hole**4)
    if not _exact(sp.diff(primitive, hole) * ds_dtheta - 1 / sp.sqrt(sine_in_s)):
        return False
    scaled = amplitude**(-sp.Rational(1, 2)) * primitive
    if not _exact(
        sp.diff(scaled, hole) * ds_dtheta
        - amplitude**(-sp.Rational(1, 2)) / sp.sqrt(sine_in_s)
    ):
        return False
    if not _exact(
        1 / sp.sqrt(amplitude * sp.sin(theta))
        - amplitude**(-sp.Rational(1, 2)) / sp.sqrt(sp.sin(theta))
    ):
        return False
    return True


def _log_cosine_quarter(integrand, symbol, lo, hi):
    """∫_0^{π/4} log(2 cos(x)^2 - 1) cos(x) dx = sqrt(2) (log 2 - 1).

    2 cos(x)^2 - 1 = 1 - 2 sin(x)^2. F(u) = u log(1-2u^2) - 2u
    + log((1+sqrt(2) u)/(1-sqrt(2) u))/sqrt(2) differentiates to the
    substituted integrand, F(0) = 0, and the limit at x = π/4 from the
    left is the value.
    """
    if symbol.is_real is not True or lo != 0 or hi != sp.pi / 4:
        return None
    if integrand != sp.log(2 * sp.cos(symbol)**2 - 1) * sp.cos(symbol):
        return None
    u = sp.Dummy("u", real=True)
    antiderivative = (
        u * sp.log(1 - 2 * u**2)
        - 2 * u
        + sp.sqrt(2)**(-1) * sp.log((1 + sp.sqrt(2) * u) / (1 - sp.sqrt(2) * u))
    )
    composed = sp.diff(antiderivative.subs(u, sp.sin(symbol)), symbol)
    if not _exact(composed - integrand):
        return None
    if not _exact(antiderivative.subs(u, 0)):
        return None
    value = sp.sqrt(2) * (sp.log(2) - 1)
    limit = sp.limit(antiderivative.subs(u, sp.sin(symbol)), symbol, sp.pi / 4, dir="-")
    if not _exact(limit - value):
        return None
    return value

_DEFINITE = (
    _two_five_power_ray,
    _log_cosine_quarter,
    _sec_tan_sixth,
    _shifted_parity,
    _abs_exp_segment,
    _abs_sine_periods,
    _abs_linear_quotient,
    _log_abs_clears,
    _sqrt_shift_abs,
    _sec_radical_quarter,
    _inverse_log_pair,
    _king_log_half,
    _sqrt_log_ray,
    _gaussian_polynomial_tail,
    _quartic_trig_period,
    _atan_log_line,
    _log_cubic_unit,
)


def definite_value(integrand, symbol, lo, hi):
    """Return a checked Yang value, or None when no certificate matches."""
    for builder in _DEFINITE:
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
