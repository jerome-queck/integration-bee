"""Exact, source-checked certificates for the 2023 Handoff D integrals.

The PDF prints sin(2**n*x), not the linear-frequency OCR reading sin(2*n*x).
Its supremum is represented by an exact log-sum-exp limit, with the finite
maximum bounds proved below. Other outer limits retain the entire Integral
and its bounds. Only these three complete shapes extend the open whitelist.
"""

from __future__ import annotations

import sympy as sp


def _d23_require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-d-2023 certificate: " + label)


def _d23_form(expr, symbol):
    if not isinstance(expr, sp.Limit) or len(expr.args) != 4:
        return None
    family, parameter, destination, direction = expr.args
    if not isinstance(parameter, sp.Symbol) or parameter.name == symbol.name:
        return None
    if parameter.is_integer is True and parameter.is_positive is True:
        if destination != sp.oo or expr != sp.Limit(family, parameter, sp.oo):
            return None
        integral = sp.Integral((1 + symbol**4)**parameter, (symbol, 0, 2))
        if family == integral**(1 / parameter):
            return "maximum-root", parameter
        sums = list(family.atoms(sp.Sum))
        if len(sums) != 1 or len(sums[0].limits) != 1 or len(sums[0].limits[0]) != 3:
            return None
        index, start, stop = sums[0].limits[0]
        if (
            not isinstance(index, sp.Symbol)
            or index.name in {symbol.name, parameter.name}
            or index.is_integer is not True
            or index.is_positive is not True
            or start != 1 or stop != parameter
        ):
            return None
        expected = sp.log(sp.Sum(
            sp.exp(parameter * sp.sin(2**index * symbol)),
            (index, 1, parameter),
        )) / parameter
        if family == expected:
            return "doubling-supremum", parameter
        return None
    if destination != 0 or str(direction) != "+-" or parameter.is_real is not True:
        return None
    powers = [item for item in family.free_symbols if item != parameter]
    if len(powers) != 1:
        return None
    n = powers[0]
    if n.name in {symbol.name, parameter.name} or n.is_integer is not True or n.is_positive is not True:
        return None
    expected = sp.Integral(
        sp.tan(symbol)**(n - 1) / sp.sin(symbol)**n,
        (symbol, parameter, 2 * parameter),
    )
    if family == expected:
        return "shrinking-tangent", (parameter, n)
    return None


def _d23_maximum_root():
    """Squeeze an L^n norm between its maximum and a short terminal interval."""
    x = sp.Symbol("_d23_x", nonnegative=True)
    n = sp.Symbol("_d23_n", positive=True, integer=True)
    delta = sp.Symbol("_d23_delta", positive=True)
    f = 1 + x**4
    _d23_require(sp.diff(f, x).is_nonnegative is True, "maximum monotonicity")
    maximum = f.subs(x, 2)
    # For every 0<delta<1, monotonicity and positivity give
    # delta*f(2-delta)**n <= Integral(f**n,0,2) <= 2*f(2)**n.
    # Taking increasing positive nth roots then the two limits proves equality.
    lower = delta**(1 / n) * f.subs(x, 2 - delta)
    upper = 2**(1 / n) * maximum
    _d23_require(sp.limit(delta**(1 / n), n, sp.oo) == 1, "short interval root")
    _d23_require(sp.limit(upper, n, sp.oo) == maximum, "upper root limit")
    _d23_require(sp.limit(sp.limit(lower, n, sp.oo), delta, 0, dir="+") == maximum,
                 "lower root limit")
    return maximum


def _d23_doubling_supremum():
    """A binary-cylinder counting proof, valid almost everywhere, for sin(2^n x)."""
    n = sp.Symbol("_d23_n", positive=True, integer=True)
    k = sp.Symbol("_d23_k", positive=True, integer=True)
    r = sp.Symbol("_d23_r", nonnegative=True, integer=True)
    m = r + 2
    maximum = sp.Symbol("_d23_M", real=True)
    # For N real numbers a_j and M=max a_j, exp(N*M) <= sum exp(N*a_j)
    # <= N*exp(N*M). Monotonicity of log gives M <= L_N <= M+log(N)/N.
    # The running maxima increase to the supremum. This proves the transcript's
    # log-sum-exp limit is exactly the printed supremum at EVERY point.
    _d23_require(sp.simplify(sp.log(sp.exp(n * maximum)) / n - maximum) == 0,
                 "finite maximum lower bound")
    upper = sp.expand_log(sp.log(n * sp.exp(n * maximum))) / n
    _d23_require(sp.simplify(upper - maximum - sp.log(n) / n) == 0,
                 "finite maximum upper bound")
    _d23_require(sp.limit(sp.log(n) / n, n, sp.oo) == 0, "maximum error vanishes")

    y = sp.Symbol("_d23_y", real=True)
    j = sp.Symbol("_d23_j", integer=True, nonnegative=True)
    # x=pi*y, y in [0,1]. At n=j*m+1 the phase is 2*pi*2**(j*m)*y.
    _d23_require(sp.simplify(2**(j * m + 1) * sp.pi * y
                            - 2 * sp.pi * 2**(j * m) * y) == 0,
                 "doubling phase")
    # The m-bit word 01 followed by m-2 zeroes is the cylinder
    # [1/4,1/4+2**(-m)). Excluding it from each of k DISJOINT m-bit blocks
    # leaves (2**m-1)**k cylinders of length 2**(-m*k). Dyadic ambiguity
    # affects a countable null set only. The following all-m,k identity and
    # limit prove the set missing that word forever has measure zero.
    count = (2**m - 1)**k
    measure = count / 2**(m * k)
    miss = (1 - 2**(-m))**k
    _d23_require(sp.simplify(measure - miss) == 0, "binary cylinder measure")
    _d23_require((2**(-m)).is_positive is True, "positive cylinder width")
    width = 2**(-m)
    _d23_require(width.subs(r, 0) == sp.Rational(1, 4)
                 and sp.diff(width, r).is_negative is True,
                 "cylinder width at most one quarter")
    # The geometric limit follows from the all-k bound (1-p)**k<=1/(1+k*p).
    # Its induction step is the nonnegative rational difference below; the
    # base k=0 is equality. This avoids any undecided symbolic logarithm sign.
    p = sp.Symbol("_d23_p", positive=True)
    difference = 1 / (1 + (k + 1) * p) - (1 - p) / (1 + k * p)
    bound_gap = (k + 1) * p**2 / ((1 + k * p) * (1 + (k + 1) * p))
    _d23_require(sp.factor(difference - bound_gap) == 0 and bound_gap.is_positive is True,
                 "geometric domination induction")
    _d23_require(sp.limit(1 / (1 + k * 2**(-m)), k, sp.oo) == 0,
                 "missing cylinder null set")
    # Taking the countable intersection over m>=2 preserves full measure.
    # For such y the sine orbit enters every cylinder next to 1/4, hence has
    # values >=1-(2*pi*2**(-m))**2/2. The lower bound follows by convexity:
    # cos(z)-1+z**2/2 has value and slope zero at 0 and second derivative >=0.
    z = sp.Symbol("_d23_z", real=True)
    residual = sp.cos(z) - 1 + z**2 / 2
    _d23_require(residual.subs(z, 0) == 0 and sp.diff(residual, z).subs(z, 0) == 0,
                 "cosine initial data")
    _d23_require(sp.trigsimp(sp.diff(residual, z, 2) - 2 * sp.sin(z / 2)**2) == 0,
                 "cosine convexity")
    _d23_require((2 * sp.sin(z / 2)**2).is_nonnegative is True, "cosine bound sign")
    _d23_require(sp.trigsimp(sp.sin(sp.pi / 2 + z) - sp.cos(z)) == 0,
                 "cylinder sine phase")
    lower = 1 - (2 * sp.pi * 2**(-m))**2 / 2
    _d23_require(sp.limit(lower, r, sp.oo) == 1, "orbit reaches sine supremum")
    _d23_require(sp.trigsimp(1 - sp.sin(z)**2 - sp.cos(z)**2) == 0,
                 "sine upper bound")
    # The bounded supremum is continuous wherever it equals 1: one of its
    # continuous sine terms is arbitrarily close to 1 there, and it never
    # exceeds 1. Thus all discontinuities lie in the null exceptional set;
    # it is Riemann-integrable too. Either integral equals the value below.
    return sp.integrate(sp.Integer(1), (y, 0, sp.pi))


def _d23_shrinking_tangent(n):
    """Fix n, rescale t=h*u, and use continuity at zero on the compact u interval."""
    h = sp.Symbol("_d23_h", real=True)
    u = sp.Symbol("_d23_u", positive=True)
    t = sp.Symbol("_d23_t", real=True)
    f = sp.tan(t)**(n - 1) / sp.sin(t)**n
    pulled = h * f.subs(t, h * u)
    reduced = h * sp.cos(h * u)**(1 - n) / sp.sin(h * u)
    _d23_require(sp.trigsimp(sp.expand_power_base((pulled / reduced).rewrite(sp.cos))) == 1,
                 "tangent substitution")
    _d23_require((h * u).subs(u, 1) == h and (h * u).subs(u, 2) == 2 * h,
                 "moving endpoints")
    _d23_require(sp.diff(h * u, u) == h, "oriented Jacobian")
    _d23_require(sp.simplify(reduced.subs(h, -h) - reduced) == 0, "two sided limit")
    # g(t)=t/(sin(t)*cos(t)**(n-1)) extends continuously to g(0)=1.
    # For each FIXED positive integer n, g(h*u)->1 uniformly for 1<=u<=2:
    # |h*u|<=2|h|. For sufficiently small h the sine quotient and cosine
    # are nonzero, and this continuity gives |g|<=2 and domination by 2/u.
    # Thus the integral converges to Integral(1/u,1,2) from either side.
    _d23_require(sp.limit(t / sp.sin(t), t, 0, dir="+-") == 1, "sine quotient")
    _d23_require(sp.limit(sp.cos(t), t, 0, dir="+-") == 1, "cosine limit")
    _d23_require(sp.limit(reduced, h, 0, dir="+-") == 1 / u, "rescaled kernel limit")
    _d23_require(sp.integrate(2 / u, (u, 1, 2)).is_finite is True, "integrable domination")
    return sp.integrate(1 / u, (u, 1, 2))


def open_integrand(expr, symbol):
    return _d23_form(expr, symbol) is not None


def definite_value(integrand, symbol, lo, hi):
    form = _d23_form(integrand, symbol)
    if form is None:
        return None
    name, parameters = form
    if name == "maximum-root" and (lo, hi) == (0, 2):
        return _d23_maximum_root()
    if name == "doubling-supremum" and (lo, hi) == (0, sp.pi):
        return _d23_doubling_supremum()
    if name == "shrinking-tangent":
        endpoint, n = parameters
        if (lo, hi) == (endpoint, 2 * endpoint):
            return _d23_shrinking_tangent(n)
    return None
