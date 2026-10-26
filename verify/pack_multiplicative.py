"""Exact forward-quotient contract for the two 2025 discrete products.

This is separate from ordinary antiderivatives: their arbitrary constant is
additive. Here C denotes a nonzero multiplicative constant. Identities hold
on the common domain of the candidate and its unit shift; Gamma poles and
zeros of a submitted periodic factor are excluded. No uniqueness up to a
constant is claimed for functions of a real variable.
"""

from __future__ import annotations

import sympy as sp


KIND = "discrete_multiplicative"


def answer_ok(factor, candidate, symbol) -> bool:
    """Prove F(x+1)/F(x)=2025*x+2026, with F not identically zero.

    The literal factor restricts this certificate to UK Relay 10 and SG
    Relay 29. Both PDFs define this forward quotient explicitly. Keeping
    the quotient, rather than cross-multiplying an equation, rejects the
    identically-zero pseudo-solution. No additive constant is stripped.
    """
    if factor != 2025 * symbol + 2026 or not isinstance(candidate, sp.Expr):
        return False
    if candidate.has(sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.Derivative):
        return False
    if candidate.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
        return False
    constants = {}
    for parameter in candidate.free_symbols - {symbol}:
        if parameter.name != "C" or parameter.is_zero is True:
            return False
        # Only this answer kind gives the mark scheme's C its required
        # nonzero interpretation. Ordinary integral parsing is untouched.
        constants[parameter] = sp.Symbol("C", nonzero=True)
    candidate = candidate.xreplace(constants)
    if candidate.is_zero is True or candidate == 0:
        return False
    quotient = candidate.subs(symbol, symbol + 1) / candidate
    if quotient.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
        return False
    # expand_func applies Gamma(w+1)=w*Gamma(w) to the rational shifts
    # before cancellation. combsimp alone leaves this ratio unevaluated.
    quotient = sp.cancel(sp.expand_func(quotient))
    return sp.simplify(quotient - factor) == 0
