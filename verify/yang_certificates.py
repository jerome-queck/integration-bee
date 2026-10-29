"""Exact certificates for Yang rows the ordinary integrator does not close.

Example 3 is the shifted-parity integrand on [0, 6]. Example 1 is a polynomial
and uses pack_gate's ordinary definite integration. Section 1.4 item 3 is
(2^x + 3^x)/5^x on [0, ∞). Section 2.4 item 12 is sec(x)^6 exp(-tan x)
on [0, pi/2]; the tangent substitution reduces it to a Gamma integral.
Three §2.6 practice rows use the same module: a nested radical
under sec(x)^2, an elliptic antiderivative of 1/sqrt(3 sin x + cos x), and
the improper integral of log(2 cos(x)^2 - 1) cos(x) on [0, π/4]. Every other
shape returns None.
"""

from __future__ import annotations

import sympy as sp


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
    u = sp.Dummy("u", positive=True)
    reduced = (1 + u ** 2) ** 2 * sp.exp(-u)
    polynomial = sp.expand((1 + u ** 2) ** 2)
    if polynomial != 1 + 2 * u ** 2 + u ** 4:
        return None
    if sp.expand(reduced) != sp.expand(polynomial * sp.exp(-u)):
        return None
    value = sp.integrate(reduced, (u, 0, sp.oo))
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


def definite_value(integrand, symbol, lo, hi):
    """Return a checked Yang value, or None on a shape miss."""
    powers = _two_five_power_ray(integrand, symbol, lo, hi)
    if powers is not None:
        return powers
    sec_tan = _sec_tan_sixth(integrand, symbol, lo, hi)
    if sec_tan is not None:
        return sec_tan
    quarter = _log_cosine_quarter(integrand, symbol, lo, hi)
    if quarter is not None:
        return quarter
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

    # The substitution maps [0,6] to [-3,3]. Its denominator is positive,
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
