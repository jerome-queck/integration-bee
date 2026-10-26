"""Exact, source-checked Handoff E tournament certificates.

The tangent limit uses u=tan(t)**(n+1) before taking its limit; the
original n*tan(t)**n family is not dominated and cannot be interchanged
with integration. Only this checked transformed limit is an open shape.
"""

from __future__ import annotations

import sympy as sp


def _eq(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-e tournament certificate: " + label)


def _log_trig_unit(integrand, symbol, lo, hi):
    if (lo, hi) != (0, 1):
        return None
    expected = symbol**3 * sp.sin(sp.log(symbol))**2 * sp.cos(sp.log(symbol))**2
    if integrand != expected:
        return None
    y = sp.Symbol("_he_log_y", real=True)
    phase = (1 - sp.cos(4*y)) / 8
    _require(_eq(sp.trigsimp(sp.sin(y)**2 * sp.cos(y)**2 - phase)),
             "double angle")
    changed = integrand.subs(symbol, sp.exp(y)) * sp.diff(sp.exp(y), y)
    reduced = sp.exp(4*y) * phase
    _require(_eq(sp.trigsimp(changed - reduced)), "logarithmic substitution")
    _require(sp.exp(y).subs(y, 0) == 1 and sp.limit(sp.exp(y), y, -sp.oo) == 0,
             "logarithmic endpoints")
    primitive = sp.exp(4*y) * (2 - sp.cos(4*y) - sp.sin(4*y)) / 64
    _require(_eq(sp.diff(primitive, y) - reduced), "damped cosine primitive")
    lower = sp.limit(primitive, y, -sp.oo)
    _require(lower == 0, "damped cosine tail")
    return sp.simplify(primitive.subs(y, 0) - lower)


def _eth_root_ray(integrand, symbol, lo, hi):
    """The radical index on slide 65 is e: sqrt(root(x,e)-1)."""
    if (lo, hi) != (1, sp.oo):
        return None
    if integrand != 1 / (symbol * sp.sqrt(symbol**(1/sp.E) - 1)):
        return None
    u = sp.Symbol("_he_root_u", positive=True)
    inverse = (1 + u**2)**sp.E
    _require(_eq(inverse**(1/sp.E) - (1 + u**2)), "positive real e-th root")
    _require(inverse.subs(u, 0) == 1 and sp.limit(inverse, u, sp.oo) == sp.oo,
             "root substitution endpoints")
    _require(sp.diff(inverse, u).is_positive is True, "root substitution orientation")
    changed = integrand.subs(symbol, inverse) * sp.diff(inverse, u)
    reduced = 2*sp.E / (1 + u**2)
    _require(_eq(changed - reduced), "root substitution Jacobian")
    primitive = 2*sp.E*sp.atan(u)
    _require(_eq(sp.diff(primitive, u) - reduced), "arctangent primitive")
    return sp.limit(primitive, u, sp.oo) - primitive.subs(u, 0)


def _tangent_limit_count(expr, symbol):
    if not isinstance(expr, sp.Limit) or len(expr.args) != 4:
        return None
    family, count, destination, direction = expr.args
    if (
        not isinstance(count, sp.Symbol)
        or count.name == symbol.name
        or count.is_positive is not True
        or count.is_integer is not True
        or destination != sp.oo
        or expr != sp.Limit(family, count, sp.oo)
    ):
        return None
    expected = count / ((count + 1) * (1 + symbol**(2 / (count + 1))))
    return count if family == expected else None


def _tangent_limit_unit(integrand, symbol, lo, hi):
    if (lo, hi) != (0, 1):
        return None
    n = _tangent_limit_count(integrand, symbol)
    if n is None:
        return None
    u = sp.Symbol("_he_tan_u", positive=True)
    t = sp.Symbol("_he_tan_t", real=True)
    forward = sp.tan(t)**(n + 1)
    inverse = sp.atan(u**(1 / (n + 1)))
    _require(forward.subs(t, 0) == 0 and forward.subs(t, sp.pi/4) == 1,
             "finite-n tangent endpoints")
    _require(_eq(forward.subs(t, inverse) - u), "finite-n tangent inverse")
    _require(sp.diff(inverse, u).is_positive is True, "finite-n tangent orientation")
    changed = n * sp.tan(inverse)**n * sp.diff(inverse, u)
    family = integrand.args[0].subs(symbol, u)
    _require(_eq(changed - family), "finite-n tangent Jacobian")
    # For u>0, u**(2/(n+1))>0, and 0<n/(n+1)<1, so 0<family<1.
    # Thus the constant 1 dominates every member on (0,1). The endpoint
    # u=0 has a different pointwise limit but has measure zero.
    power = u**(2 / (n + 1))
    _require(power.is_positive is True, "positive tangent denominator term")
    _require((n / (n + 1)).is_positive is True, "positive tangent coefficient")
    _require(_eq(1 - n/(n+1) - 1/(n+1)) and (1/(n+1)).is_positive is True,
             "tangent coefficient bounded by one")
    _require(sp.integrate(sp.Integer(1), (u, 0, 1)) == 1, "integrable domination")
    pointwise = sp.limit(family, n, sp.oo)
    _require(pointwise == sp.Rational(1, 2), "tangent pointwise limit")
    return sp.integrate(pointwise, (u, 0, 1))


def open_integrand(expr, symbol):
    return _tangent_limit_count(expr, symbol) is not None


def definite_value(integrand, symbol, lo, hi):
    for builder in (_log_trig_unit, _eth_root_ray, _tangent_limit_unit):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
