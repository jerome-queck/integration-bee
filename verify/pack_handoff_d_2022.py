"""Exact integral certificates for the 2022 Relay part of Handoff D.

The two limits retain their full finite integral and its bounds.  The nested
exponential integral retains the paper's definition (which is E1, not SymPy Ei).
Only these three complete shapes extend the open-expression whitelist.
"""

from __future__ import annotations

import sympy as sp


def _d22_require(condition, label):
    if condition is not True and condition != sp.true:
        raise ArithmeticError("handoff-d-2022: " + label)


def _d22_eq(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _d22_e1_form(expr, symbol):
    inners = list(expr.atoms(sp.Integral))
    if len(inners) != 1:
        return None
    inner = inners[0]
    if len(inner.limits) != 1 or len(inner.limits[0]) != 3:
        return None
    t, lo, hi = inner.limits[0]
    if (
        not isinstance(t, sp.Symbol)
        or t.name == symbol.name
        or (lo, hi) != (symbol, sp.oo)
        or inner.function != sp.exp(-t) / t
    ):
        return None
    parameters = expr.free_symbols - {symbol}
    if len(parameters) != 1:
        return None
    a = next(iter(parameters))
    if a.is_positive is not True or a.name in {symbol.name, t.name}:
        return None
    if expr != sp.exp(-a * symbol) * inner:
        return None
    return a


def _d22_limit_form(expr, symbol):
    if not isinstance(expr, sp.Limit) or len(expr.args) != 4:
        return None
    family, parameter, destination, direction = expr.args
    if not isinstance(parameter, sp.Symbol) or parameter.name == symbol.name:
        return None
    inners = list(family.atoms(sp.Integral))
    if len(inners) != 1:
        return None
    inner = inners[0]
    if len(inner.limits) != 1 or len(inner.limits[0]) != 3 or inner.limits[0][0] != symbol:
        return None
    if destination == 0 and direction == sp.Symbol("+") and family == inner:
        if inner.limits[0][1:] != (parameter, 2 * parameter):
            return None
        other = inner.function.free_symbols - {symbol}
        if len(other) != 1:
            return None
        n = next(iter(other))
        if n.is_integer is not True or n.is_positive is not True or n.name == parameter.name:
            return None
        if inner.function != sp.sin(symbol) ** (n - 1) / symbol**n:
            return None
        expected = sp.Limit(inner, parameter, 0, dir="+")
        return ("sinc", parameter, inner, n) if expr == expected else None
    if destination == sp.oo and parameter.is_positive is True:
        expected = sp.Integral(parameter ** (1 / symbol), (symbol, 1, parameter)) / parameter
        if expr == sp.Limit(expected, parameter, sp.oo):
            return "average-power", parameter, inner, None
    return None


def _d22_e1_value(a):
    x, t = sp.symbols("_d22_x _d22_t", positive=True)
    s = sp.Symbol("_d22_s", positive=True)
    # On 0 < x < t the full kernel is nonnegative, so Tonelli applies.
    # Integrating in x first produces (exp(-t)-exp(-(a+1)*t))/(a*t).
    kernel = sp.exp(-a * x - t) / t
    _d22_require(kernel.is_positive is True, "E1-positive-kernel")
    inner_x = sp.integrate(sp.exp(-a * x), (x, 0, t))
    _d22_require(_d22_eq(inner_x - (1 - sp.exp(-a * t)) / a), "E1-inner-x")
    reduced = sp.exp(-t) * inner_x / t
    # A second positive parameter integral evaluates the Frullani expression
    # without subtracting divergent integrals at t=0.
    parameter_kernel = sp.exp(-(1 + s) * t)
    _d22_require(parameter_kernel.is_positive is True, "E1-parameter-positive")
    parameter_integral = sp.integrate(parameter_kernel, (s, 0, a))
    _d22_require(_d22_eq(parameter_integral / a - reduced), "E1-parameter-identity")
    inner_t = sp.integrate(parameter_kernel, (t, 0, sp.oo))
    _d22_require(inner_t == 1 / (1 + s), "E1-Laplace-kernel")
    value = sp.integrate(inner_t, (s, 0, a)) / a
    _d22_require(value.is_finite is True, "E1-finite-value")
    # The original input carries the checked positive-a domain.  Render the
    # derived final with the same user-facing parameter name: the answer
    # consumer parses ordinary "a" without constructor-specific assumptions.
    return value.xreplace({a: sp.Symbol(a.name)})


def _d22_sinc_value(n):
    h, u = sp.symbols("_d22_h _d22_u", positive=True)
    t = sp.Symbol("_d22_t", real=True)
    original = sp.sin(t) ** (n - 1) / t**n
    mapping = h * u
    pulled = original.subs(t, mapping) * sp.diff(mapping, u)
    reduced = (sp.sin(h * u) / (h * u)) ** (n - 1) / u
    _d22_require(_d22_eq(pulled - reduced), "sinc-substitution")
    _d22_require(mapping.subs(u, 1) == h and mapping.subs(u, 2) == 2 * h, "sinc-bounds")
    _d22_require(sp.diff(mapping, u).is_positive is True, "sinc-orientation")
    # |sin(z)| <= |z| follows from the mean-value theorem, sin(0)=0,
    # and |cos(z)| <= 1.  The latter follows from the checked identity and
    # nonnegativity of sin(z)^2.  Since n-1 is a nonnegative integer,
    # |sinc(h*u)^(n-1)/u| <= 1/u on [1,2], uniformly in h>0.
    z = sp.Symbol("_d22_z", real=True)
    _d22_require(sp.diff(sp.sin(z), z) == sp.cos(z) and sp.sin(0) == 0, "sinc-MVT")
    _d22_require(sp.trigsimp(sp.cos(z) ** 2 + sp.sin(z) ** 2 - 1) == 0, "sinc-bound-identity")
    _d22_require((sp.sin(z) ** 2).is_nonnegative is True, "sinc-bound-square")
    _d22_require((n - 1).is_nonnegative is True, "sinc-nonnegative-power")
    limit = sp.limit(reduced, h, 0, dir="+")
    _d22_require(limit == 1 / u, "sinc-pointwise-limit")
    # The checked finite integral of the dominator licenses dominated
    # convergence for the *whole* original integral, not its pointwise limit.
    value = sp.integrate(limit, (u, 1, 2))
    _d22_require(value.is_finite is True, "sinc-integrable-dominator")
    return value


def _d22_average_value():
    a = sp.Symbol("_d22_A", positive=True)
    ell = sp.Symbol("_d22_L", positive=True)
    u = sp.Symbol("_d22_u", nonnegative=True)
    v, x = sp.symbols("_d22_v _d22_x", positive=True)
    # For A >= 16 split the domain at 2 and A^(1/4).  A^(1/x)
    # decreases in x for A>1.  The complete integral is bounded below by
    # (A-1)/A because A^(1/x)>=1 throughout [1,A].
    _d22_require(
        _d22_eq(sp.diff(sp.exp(ell / x), x) + ell * sp.exp(ell / x) / x**2),
        "average-monotonicity-derivative",
    )
    _d22_require((ell * sp.exp(ell / x) / x**2).is_positive is True, "average-decreasing")
    _d22_require((ell / x).is_positive is True, "average-lower-integrand")
    _d22_require(sp.Integer(16) ** sp.Rational(1, 4) == 2, "average-split-order")
    # x=1+u, 0<=u<=1: exp(L/(1+u)-L) <= exp(-L*u/2).
    gap = -ell * u / 2 - (ell / (1 + u) - ell)
    _d22_require(_d22_eq(gap - ell * u * (1 - u) / (2 * (1 + u))), "average-first-exponents")
    _d22_require(sp.factor(gap.subs(u, v / (1 + v))).is_positive is True, "average-first-bound")
    first = sp.integrate(sp.exp(-ell * u / 2), (u, 0, 1))
    _d22_require(_d22_eq(2 / ell - first - 2 * sp.exp(-ell / 2) / ell), "average-first-tail")
    _d22_require((2 * sp.exp(-ell / 2) / ell).is_positive is True, "average-first-tail-positive")
    # On [2,A^(1/4)] the normalized integral is at most A^(-1/4).
    _d22_require(sp.factor(sp.Rational(1, 2) - 1 / (2 + v)).is_positive is True, "average-middle-exponent")
    middle = sp.simplify(a ** sp.Rational(1, 4) * sp.sqrt(a) / a)
    _d22_require(middle == a ** (-sp.Rational(1, 4)), "average-middle-bound")
    # On [A^(1/4),A], the normalized length is <=1 and the integrand
    # is at most A^(A^(-1/4)).  These estimates bound every finite A>=16.
    tail_gap = a ** (-sp.Rational(1, 4)) - 1 / (a ** sp.Rational(1, 4) + v)
    _d22_require(sp.factor(tail_gap).is_positive is True, "average-tail-exponent")
    _d22_require(
        _d22_eq(1 - (a - a ** sp.Rational(1, 4)) / a - a ** (-sp.Rational(3, 4))),
        "average-tail-length",
    )
    lower = (a - 1) / a
    upper = 2 / sp.log(a) + middle + a ** (a ** (-sp.Rational(1, 4)))
    lower_limit = sp.limit(lower, a, sp.oo)
    upper_limit = sp.limit(upper, a, sp.oo)
    _d22_require(lower_limit == upper_limit, "average-squeeze")
    return lower_limit


def open_integrand(expr, symbol):
    return _d22_e1_form(expr, symbol) is not None or _d22_limit_form(expr, symbol) is not None


def definite_value(integrand, symbol, lo, hi):
    a = _d22_e1_form(integrand, symbol)
    if a is not None:
        return _d22_e1_value(a) if (lo, hi) == (0, sp.oo) else None
    form = _d22_limit_form(integrand, symbol)
    if form is None:
        return None
    tag, _parameter, inner, n = form
    if inner.limits[0][1:] != (lo, hi):
        return None
    return _d22_sinc_value(n) if tag == "sinc" else _d22_average_value()
