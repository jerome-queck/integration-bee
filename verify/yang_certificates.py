"""Exact shifted-parity certificate for the answered Yang symmetry example.

The matcher is restricted to Example 3's printed integrand and endpoints.
Example 1 is a polynomial and uses pack_gate's ordinary definite integration.
"""

from __future__ import annotations

import sympy as sp


def definite_value(integrand, symbol, lo, hi):
    """Return Yang 1.3 Example 3's checked value, or None on a shape miss."""
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
