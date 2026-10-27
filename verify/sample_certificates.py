"""Exact reductions for the four formerly manual SAMPLE integrals.

The Bose integral carries its convergence domain in its parameter symbols:
s = 1 + sigma + I*tau, with sigma positive and tau real.  The radical
antiderivative is certified on its real open domain (-1, 1), on both sides
of zero.  Numeric agreement and forced power/logarithm rewrites are unused.
"""

from __future__ import annotations

import sympy as sp
from sympy.calculus.util import continuous_domain


def _require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def _eq(expression):
    return expression == 0 or sp.simplify(expression) == 0


def s_parameter(integrand, symbol, lo, hi):
    """Return the printed s only for the catalog's encoded half-plane."""
    sigma = sp.Symbol("sigma", positive=True)
    tau = sp.Symbol("tau", real=True)
    if symbol in {sigma, tau} or (lo, hi) != (0, sp.oo):
        return None
    expected = symbol**(sigma + sp.I * tau) / (sp.exp(symbol) - 1)
    if integrand != expected:
        return None
    return 1 + sigma + sp.I * tau


def _log_reflection(integrand, symbol, lo, hi):
    target = sp.log(symbol) / (symbol**2 - 2 * symbol + 2)
    if (lo, hi) != (1, 2) or integrand != target:
        return None
    t = sp.Dummy("sample_shift", positive=True)
    shifted = integrand.subs(symbol, 1 + t)
    weight = 1 / (1 + t**2)
    _require(_eq(shifted - sp.log(1 + t) * weight), "sample-log-shift")

    # This is tan(pi/4-theta) after t=tan(theta).  It reverses [0,1],
    # preserves the Cauchy weight, and is its own inverse.
    reflection = (1 - t) / (1 + t)
    _require(reflection.subs(t, 0) == 1 and reflection.subs(t, 1) == 0,
             "sample-log-reflected-endpoints")
    _require(_eq(reflection.subs(t, reflection) - t), "sample-log-involution")
    _require(sp.factor(sp.diff(reflection, t)).is_negative is True,
             "sample-log-orientation")
    reflected_weight = -sp.diff(reflection, t) / (1 + reflection**2)
    _require(_eq(reflected_weight - weight), "sample-log-reflected-weight")
    _require(_eq(1 + reflection - 2 / (1 + t)), "sample-log-reflected-argument")
    # Both logarithm arguments are positive.  expand_log uses those
    # assumptions, so this is a real logarithm identity without force=True.
    logarithms = sp.log(1 + t) + sp.log(2 / (1 + t))
    _require(sp.expand_log(logarithms) == sp.log(2), "sample-log-pair")
    mass = sp.integrate(weight, (t, 0, 1))
    _require(mass == sp.pi / 4, "sample-log-weight-integral")
    # The two continuous, reflected integrals have equal values. Adding
    # them replaces their logarithms by log(2).
    return sp.log(2) * mass / 2


def _gamma_zeta(integrand, symbol, lo, hi):
    if (lo, hi) != (0, sp.oo):
        return None
    power = integrand * (sp.exp(symbol) - 1)
    if power == 1:
        exponent = sp.S.Zero
    else:
        base, exponent = power.as_base_exp()
        if base != symbol:
            return None
    if integrand != symbol**exponent / (sp.exp(symbol) - 1):
        return None
    # A recognized Bose power with absent/invalid assumptions must fail
    # here, before the gate's general positive-parameter fallback can run.
    real_part = sp.re(exponent)
    _require(not exponent.has(symbol) and exponent.is_finite is True
             and real_part.is_positive is True, "sample-zeta-domain-Re-s-gt-one")
    s = 1 + exponent
    t = sp.Dummy("sample_bose_x", positive=True)
    n = sp.Dummy("sample_bose_n", integer=True, positive=True)
    q = sp.Dummy("sample_bose_q", positive=True)
    partial = q * (1 - q**n) / (1 - q)
    _require(_eq(partial.subs(n, 1) - q), "sample-zeta-geometric-base")
    _require(_eq(partial.subs(n, n + 1) - partial - q**(n + 1)),
             "sample-zeta-geometric-step")
    _require(sp.exp(-t).subs(t, 0) == 1
             and sp.diff(sp.exp(-t), t).is_negative is True,
             "sample-zeta-geometric-range")
    _require(sp.limit(sp.exp(-n * t), n, sp.oo) == 0,
             "sample-zeta-geometric-tail")
    kernel = (q / (1 - q)).subs(q, sp.exp(-t))
    _require(_eq(kernel - 1 / (sp.exp(t) - 1)), "sample-zeta-geometric-kernel")

    term = t**(s - 1) * sp.exp(-n * t)
    absolute_term = t**real_part * sp.exp(-n * t)
    _require(_eq(sp.Abs(term) - absolute_term), "sample-zeta-absolute-kernel")
    absolute_moment = sp.integrate(absolute_term, (t, 0, sp.oo))
    _require(_eq(absolute_moment - sp.gamma(1 + real_part) / n**(1 + real_part)),
             "sample-zeta-absolute-gamma-moment")
    absolute_sum = sp.gamma(1 + real_part) * sp.summation(
        n**(-1 - real_part), (n, 1, sp.oo)
    )
    _require(_eq(absolute_sum - sp.gamma(1 + real_part) * sp.zeta(1 + real_part))
             and absolute_sum.is_finite is True, "sample-zeta-absolute-summability")
    # Absolute summability licenses interchanging this complex series and
    # the integral.  Positive real t uses its real logarithm in t**(s-1).
    moment = sp.integrate(term, (t, 0, sp.oo))
    _require(_eq(moment - sp.gamma(s) / n**s), "sample-zeta-complex-gamma-moment")
    total = sp.summation(n**(-s), (n, 1, sp.oo))
    _require(total == sp.zeta(s), "sample-zeta-dirichlet-series")
    return sp.gamma(s) * total


def _fractional_part(integrand, symbol, lo, hi):
    target = (symbol - sp.floor(symbol)) / symbol**4
    if (lo, hi) != (1, sp.oo) or integrand != target:
        return None
    x = sp.Dummy("sample_floor_x", positive=True)
    n = sp.Dummy("sample_floor_n", integer=True, positive=True)
    t = sp.Dummy("sample_floor_t", real=True)
    _require(sp.floor(n + t) == n + sp.floor(t), "sample-floor-integer-shift")
    # For 0<=t<1, floor(t)=0 by definition.  Thus on [n,n+1) the
    # integrand is (x-n)/x**4; interval endpoints have measure zero.
    piece = (x - n) / x**4
    primitive = -1 / (2 * x**2) + n / (3 * x**3)
    _require(_eq(sp.diff(primitive, x) - piece), "sample-floor-piece-primitive")
    area = primitive.subs(x, n + 1) - primitive.subs(x, n)
    split = 1 / (6 * n**2) - 1 / (6 * (n + 1)**2) - 1 / (3 * (n + 1)**3)
    _require(_eq(area - split), "sample-floor-piece-value")
    # 0<={x}<1 gives an integrable 1/x**4 majorant. This proves both
    # the floor split and the vanishing remainder at a noninteger cutoff.
    _require(sp.integrate(x**(-4), (x, 1, sp.oo)) == sp.Rational(1, 3),
             "sample-floor-integrable-majorant")
    total = sp.summation(split, (n, 1, sp.oo))
    _require(_eq(total - (sp.Rational(1, 2) - sp.zeta(3) / 3)),
             "sample-floor-series")
    return total


def definite_value(integrand, symbol, lo, hi):
    """Return a checked value only for a supported integral and its bounds."""
    for builder in (_log_reflection, _gamma_zeta, _fractional_part):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None


def matches_radical(integrand, symbol):
    """Recognize the radical family that needs its real-domain proof."""
    target = symbol * sp.sqrt((1 - symbol**2) / (1 + symbol**2))
    return integrand == target and symbol.is_real is True


def indefinite_ok(answer, integrand, symbol):
    """Check SAMPLE Q19 symbolically throughout its real interior domain."""
    if not matches_radical(integrand, symbol):
        return None
    if answer.has(sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.Derivative,
                  sp.nan, sp.zoo, sp.oo, -sp.oo):
        return False
    domain = sp.Interval.open(-1, 1)
    try:
        if continuous_domain(answer, symbol, domain) != domain:
            return False
    except (NotImplementedError, ValueError):
        # Differentiating a Piecewise constant can erase an interior jump.
        # Without continuity, derivative equality on the pieces is not a
        # primitive on the whole interval claimed by this certificate.
        return False
    t = sp.Dummy("sample_radical_t", real=True)
    mapping = t / sp.sqrt(1 + t**2)
    # This smooth, strictly increasing map has image (-1,1), precisely
    # the interior of the integrand's real domain.  It covers negative x,
    # zero, and positive x without choosing a square-root sign by force.
    slope = sp.simplify(sp.diff(mapping, t))
    _require(slope == (1 + t**2)**(-sp.Rational(3, 2))
             and slope.is_positive is True, "sample-radical-domain-monotonicity")
    _require(sp.limit(mapping, t, -sp.oo) == -1
             and sp.limit(mapping, t, sp.oo) == 1, "sample-radical-domain-range")
    derivative = sp.simplify(sp.diff(answer, symbol).subs(symbol, mapping))
    mapped_integrand = sp.simplify(integrand.subs(symbol, mapping))
    return _eq(derivative - mapped_integrand)
