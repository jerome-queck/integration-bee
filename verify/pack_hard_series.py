"""Checked Laplace and logarithmic-series reductions for three pack rows.

The logarithmic Sum keeps the printed summands.  Its passage through the
integral is justified by an absolutely summable remainder, not by assuming
that an arbitrary conditionally convergent series can be integrated.
"""

from __future__ import annotations

import sympy as sp


def _require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def _eq(expression):
    return expression == 0 or sp.simplify(expression) == 0


def matches_root_log_sum(integrand, symbol):
    """Recognize only the original alternating root-logarithm series."""
    if not isinstance(integrand, sp.Sum) or len(integrand.limits) != 1:
        return False
    index, first, last = integrand.limits[0]
    if not isinstance(index, sp.Symbol) or index == symbol or first != 1 or last != sp.oo:
        return False
    expected = (-1)**index * sp.log(
        (1 - symbol**(1 / index)) / (1 - symbol**(1 / (index + 1)))
    )
    return integrand.function == expected


def open_integrand(integrand, symbol):
    """Permit the exact printed Sum during transcript canonicalization."""
    return matches_root_log_sum(integrand, symbol)


def _sine_bose(integrand, symbol, lo, hi):
    if lo != 0 or hi != sp.oo or integrand != sp.sin(symbol) / (sp.exp(symbol) - 1):
        return None
    t = sp.Dummy("laplace_t", positive=True)
    n = sp.Dummy("laplace_n", integer=True, positive=True)
    q = sp.Dummy("laplace_q", positive=True)
    partial = q * (1 - q**n) / (1 - q)
    _require(_eq(partial.subs(n, 1) - q), "geometric-first")
    _require(_eq(partial.subs(n, n + 1) - partial - q**(n + 1)), "geometric-step")
    # q=e^-t lies in (0,1) for t>0.  Check the vanishing tail and the exact kernel.
    _require(sp.diff(sp.exp(-t), t).is_negative is True, "geometric-decrease")
    _require(sp.exp(-t).subs(t, 0) == 1, "geometric-origin")
    _require(sp.limit(sp.exp(-n * t), n, sp.oo) == 0, "geometric-tail")
    total = q / (1 - q)
    _require(_eq(total.subs(q, sp.exp(-t)) - 1 / (sp.exp(t) - 1)),
             "geometric-kernel")

    # |sin(t)|<=t follows from (t +/- sin(t))' = 1 +/- cos(t)>=0.
    # Thus sum_n int |e^-nt sin(t)| dt <= sum_n 1/n^2 < infinity.
    for sign, square in ((1, 2 * sp.cos(t / 2)**2), (-1, 2 * sp.sin(t / 2)**2)):
        _require(sp.trigsimp(sp.diff(t + sign * sp.sin(t), t) - square) == 0,
                 "laplace-majorant-derivative")
        _require(square.is_nonnegative is True, "laplace-majorant-sign")
    majorant = sp.integrate(t * sp.exp(-n * t), (t, 0, sp.oo))
    _require(majorant == 1 / n**2, "laplace-majorant-integral")
    _require(sp.summation(majorant, (n, 1, sp.oo)) == sp.pi**2 / 6,
             "laplace-absolute-summability")
    term = sp.integrate(sp.exp(-n * t) * sp.sin(t), (t, 0, sp.oo))
    _require(_eq(term - 1 / (n**2 + 1)), "laplace-term")
    value = sp.summation(term, (n, 1, sp.oo))
    final = sp.pi * sp.coth(sp.pi) / 2 - sp.Rational(1, 2)
    _require(_eq(value - final), "laplace-series-value")
    return final


def _root_log_sum(integrand, symbol, lo, hi):
    if lo != 0 or hi != 1 or not matches_root_log_sum(integrand, symbol):
        return None
    n = sp.Dummy("root_n", integer=True, positive=True)
    a, t, v, s = sp.symbols("_root_a _root_t _root_v _root_s", positive=True)

    # x=v^n turns int log(1-x^(1/n)) dx into the s-derivative of
    # n B(n,s) at s=1.  The beta integral and differentiation under it apply
    # for n>0 and s in a compact positive neighborhood of 1.
    power = v**n
    _require(_eq(power**(1 / n) - v), "root-substitution")
    _require(_eq(sp.diff(power, v) - n * v**(n - 1)), "root-jacobian")
    _require(power.subs(v, 0) == 0 and power.subs(v, 1) == 1, "root-endpoints")
    beta_kernel = v**(n - 1) * (1 - v)**(s - 1)
    _require(_eq(sp.diff(beta_kernel, s).subs(s, 1) - v**(n - 1) * sp.log(1 - v)),
             "beta-differentiation")
    beta = sp.gamma(n) * sp.gamma(s) / sp.gamma(n + s)
    _require(_eq(n * beta.subs(s, 1) - 1), "beta-normalization")
    moment = sp.simplify(n * sp.diff(beta, s).subs(s, 1))
    _require(_eq(moment + sp.harmonic(n).rewrite(sp.polygamma)), "beta-log-moment")
    gap = sp.expand_func(moment - moment.subs(n, n + 1))
    _require(_eq(gap - 1 / (n + 1)), "root-log-gap")

    # Let t=-log x, b_n=log((1-exp(-t/n))/(1-exp(-t/(n+1)))) and
    # c_n=log((n+1)/n).  If g(z)=log((1-e^-z)/z), then
    # c_n-b_n=g(t/(n+1))-g(t/n)>=0.  Indeed g'<0 follows from
    # e^z>1+z; the latter follows twice from differentiation and the value
    # at zero.  These are identities on positive real arguments only.
    _require(sp.diff(sp.exp(t), t).is_positive is True, "exp-monotone")
    excess = sp.exp(t) - 1 - t
    _require(excess.subs(t, 0) == 0 and sp.diff(excess, t).subs(t, 0) == 0,
             "exp-excess-origin")
    _require(sp.diff(excess, t, 2).is_positive is True, "exp-excess-convex")
    g = sp.log((1 - sp.exp(-t)) / t)
    _require(_eq(sp.diff(g, t) + excess / (t * (sp.exp(t) - 1))), "log-ratio-monotone")
    _require(sp.factor(t / n - t / (n + 1)).is_positive is True, "root-ordered-arguments")
    ratio = (1 - sp.exp(-t / n)) / (1 - sp.exp(-t / (n + 1)))
    scaled = ((n + 1) / n) * (
        (1 - sp.exp(-t / n)) / (t / n)
    ) / ((1 - sp.exp(-t / (n + 1))) / (t / (n + 1)))
    _require(_eq(ratio - scaled), "root-log-factorization")
    _require(sp.diff(1 - sp.exp(-t / a), a).is_negative is True, "root-log-positive")
    _require(_eq(sp.exp(-t)**(1 / n) - sp.exp(-t / n)), "root-exponential-parameter")

    c = sp.log((a + 1) / a)
    _require(_eq(sp.diff(c, a) + 1 / (a * (a + 1))), "constant-series-decrease")
    _require(sp.limit(c, a, sp.oo) == 0, "constant-series-tail")
    # The alternating constants converge.  The remaining functions have
    # summable L1 norms, since int(c_n-b_n)=c_n-1/(n+1) and the partial
    # sums below tend to 1-EulerGamma.  This proves the required exchange.
    mass = sp.log(n + 1) - sp.harmonic(n + 1) + 1
    _require(mass.subs(n, 0) == 0, "root-remainder-base")
    step = mass - mass.subs(n, n - 1) - c.subs(a, n) + 1 / (n + 1)
    _require(_eq(sp.expand_func(sp.expand_log(step))), "root-remainder-step")
    _require(sp.limit(mass, n, sp.oo) == 1 - sp.EulerGamma, "root-remainder-total")

    value = sp.summation((-1)**n * gap, (n, 1, sp.oo))
    _require(_eq(value - (sp.log(2) - 1)), "root-log-final-series")
    return value


def definite_value(integrand, symbol, lo, hi):
    """Return a checked value only after matching an exact source expression."""
    for builder in (_sine_bose, _root_log_sum):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
