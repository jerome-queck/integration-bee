"""Exact certificates for Yang rows the ordinary integrator does not close.

Example 3 is the shifted-parity integrand on [0, 6]. Example 1 is a polynomial
and uses pack_gate's ordinary definite integration. Section 2.4 item 12 is
sec(x)^6 exp(-tan x) on [0, pi/2]; the tangent substitution reduces it to a
Gamma integral. Every other shape returns None.
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


def definite_value(integrand, symbol, lo, hi):
    """Return a checked Yang value, or None on a shape miss."""
    sec_tan = _sec_tan_sixth(integrand, symbol, lo, hi)
    if sec_tan is not None:
        return sec_tan
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
