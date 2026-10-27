"""Certificates for the explicitly clarified Relay readings in Handoff M.

The stored full question is matched before any limit exchange.  In particular,
Relay 2023 Q19 uses the catalog's stated sqrt(n) upper-bound clarification;
the printed n-bound integral is deliberately outside this certificate.
"""

from __future__ import annotations

import sympy as sp

import pack_handoff_d_2021


class MinimalLogPassOn(sp.Function):
    """Pass (r+sqrt(r+s))/u from a value (r/s)*(log(t)-u).

    The parameters are positive integers, gcd(r,s)=1, and u is the smallest
    possible positive integer. This explicit normalization is the catalog's
    clarification of shuttle D3; the original PDF does not prescribe it.
    The single argument retains the complete integral whose form is extracted.
    """

    nargs = 1

    def _latex(self, printer):
        return (r"\operatorname{pass}_{\min u}\!\left("
                + printer._print(self.args[0]) + r"\right)")


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ArithmeticError("handoff-m: " + label)


def _cosine_limit_form(expr, symbol):
    if not isinstance(expr, sp.Limit) or len(expr.args) != 4:
        return None
    body, n, destination, _direction = expr.args
    if (not isinstance(n, sp.Symbol) or n.is_positive is not True
            or n.is_integer is not True or n.name == symbol.name
            or destination != sp.oo or expr != sp.Limit(body, n, sp.oo)):
        return None
    expected = sp.Integral(sp.cos(symbol / sp.sqrt(n))**n,
                           (symbol, 0, sp.sqrt(n)))
    return n if body == expected else None


def open_expression(kind, expr, symbol):
    """Recognize the complete clarified limit, including its integer index."""
    return (kind == "expression" and symbol.is_real is True
            and _cosine_limit_form(expr, symbol) is not None)


def _cosine_limit_value(n):
    u = sp.Symbol("_m_u", real=True)
    x = sp.Symbol("_m_x", positive=True)
    scaled = x / sp.sqrt(n)
    _require(scaled.subs(x, 0) == 0
             and scaled.subs(x, sp.sqrt(n)) == 1,
             "cosine scaling endpoints")
    _require(sp.diff(scaled, x).is_positive is True,
             "cosine scaling orientation")
    _require(1 < sp.pi / 2, "cosine positive arc")
    _require(sp.solveset(sp.cos(u), u, domain=sp.Interval(0, 1)) == sp.EmptySet
             and sp.cos(0) == 1, "cosine has no zero on the arc")

    # On [0,1], cos(u)>0, so tan and log(cos) are real and smooth.  The
    # checked derivative (tan(u)-u)'=tan(u)^2>=0 and value at 0 give
    # tan(u)>=u.  Thus log(cos(u))+u^2/2 has nonpositive derivative and
    # starts at 0.  This supplies the global bound needed below, rather
    # than merely a pointwise Gaussian approximation.
    tangent_gap = sp.tan(u) - u
    _require(tangent_gap.subs(u, 0) == 0, "tangent gap initial value")
    _require(sp.trigsimp(sp.diff(tangent_gap, u) - sp.tan(u)**2) == 0,
             "tangent gap derivative")
    _require((sp.tan(u)**2).is_extended_nonnegative is True,
             "tangent square sign")
    log_gap = sp.log(sp.cos(u)) + u**2 / 2
    _require(log_gap.subs(u, 0) == 0, "logarithm bound initial value")
    _require(sp.trigsimp(sp.diff(log_gap, u) + tangent_gap) == 0,
             "logarithm bound derivative")
    _require(sp.simplify(-n * scaled**2 / 2 + x**2 / 2) == 0,
             "Gaussian domination exponent")

    # Extend the finite-n integrand by zero for x>sqrt(n).  The matched
    # upper bound is essential: for 0<=x<=sqrt(n), u=x/sqrt(n) lies in
    # [0,1] and the inequalities just proved give
    #   0 <= cos(x/sqrt(n))^n <= exp(-x^2/2).
    # Every fixed x>0 eventually lies inside the interval.  The endpoint
    # x=0 is harmless (its value is 1 for every n).
    _require(sp.limit(sp.sqrt(n), n, sp.oo) == sp.oo,
             "Gaussian domains exhaust the ray")
    exponent = sp.limit(n * sp.log(sp.cos(scaled)), n, sp.oo)
    _require(exponent == -x**2 / 2, "pointwise Gaussian exponent")
    gaussian = sp.exp(exponent)
    _require(gaussian.is_positive is True, "positive Gaussian majorant")
    mass = sp.integrate(gaussian, (x, 0, sp.oo))
    _require(not mass.has(sp.Integral) and mass.is_finite is True,
             "integrable Gaussian majorant")
    # Dominated convergence now proves the limit of the complete integrals.
    return mass


def answer_value(kind, expr, symbol, limits):
    """Derive an answer only for the recognized full clarified question."""
    if limits is not None or not open_expression(kind, expr, symbol):
        return None
    return _cosine_limit_value(_cosine_limit_form(expr, symbol))


def _shuttle_form(symbol):
    return MinimalLogPassOn(sp.Integral((1 - symbol) / (2 * symbol + 1),
                                        (symbol, 0, 1)))


def open_integrand(expr, symbol):
    """Retain D3's complete integral and its explicitly normalized pass-on."""
    return symbol.is_real is True and expr == _shuttle_form(symbol)


def _shuttle_value():
    # Derive c through the already checked D1/D2 chain, rather than taking
    # it from the mark. The source integrand at this c must be the matched one.
    c = pack_handoff_d_2021._d21_d2()
    _require(c == 1, "D3 received parameter")
    x = sp.Symbol("_m_x", positive=True)
    original = (1 - x) / (x**c + (x**c + 1)**c)
    _require(sp.simplify(original - (1 - x) / (2 * x + 1)) == 0,
             "D3 source integrand")
    primitive = -x / 2 + 3 * sp.log(2 * x + 1) / 4
    _require(sp.simplify(sp.diff(primitive, x) - original) == 0,
             "D3 primitive")
    value = primitive.subs(x, 1) - primitive.subs(x, 0)

    # Uniqueness of the normalization uses the known transcendence of e.
    # If value=(r/s)(log(t)-u), then
    #   t**(4*r)/3**(3*s) = exp(4*r*u-2*s).
    # The left side is rational and the exponent is an integer, so it must
    # be zero. Thus s=2*r*u; coprimality forces r=1 and s=2*u. Unique prime
    # factorization then gives t=3**v and 2*v=3*u: u=2*k, t=27**k.
    # These theorem premises, not numerical coefficient matching, classify
    # ALL admissible tuples as (1,4*k,27**k,2*k), positive integer k.
    _require(sp.E.is_transcendental is True, "D3 transcendence premise")
    r, u, k = sp.symbols("_m_r _m_u _m_k", positive=True, integer=True)
    _require(sp.gcd(r, 2 * r * u) == r, "D3 reduced numerator")
    _require(sp.gcd(2, 3) == 1, "D3 prime-exponent parity")
    family = (sp.Integer(1), 4 * k, 27**k, 2 * k)
    fr, fs, ft, fu = family
    _require(sp.simplify(sp.expand_log(fr / fs * (sp.log(ft) - fu)) - value) == 0,
             "D3 entire normalized family")
    _require(k.is_integer is True and k.is_positive is True,
             "D3 positive integer family index")
    # k>=1, so the unique minimum of u=2*k is attained at k=1.
    r, s, t, u = (item.subs(k, 1) for item in family)
    _require((r, s, t, u) == (1, 4, 27, 2) and sp.gcd(r, s) == 1,
             "D3 minimum-u tuple")
    _require(sp.simplify(r / s * (sp.log(t) - u) - value) == 0,
             "D3 normalized integral")
    return (r + sp.sqrt(r + s)) / u


def _volterra_value(symbol):
    # The catalog explicitly requires real differentiable f with f(x)>0
    # for 0<|x|<=1. Hence 2*f*f'=x*f/(1+x**2) can be divided by f on
    # BOTH sides of zero. Continuity and f(0)=0 fix both constants, giving h.
    h = sp.log(1 + symbol**2) / 4
    square_primitive = sp.log(1 + symbol**2)**2 / 16
    primitive = (symbol * sp.log(1 + symbol**2) - 2 * symbol
                 + 2 * sp.atan(symbol)) / 4
    nonzero = sp.Symbol("_m_nonzero", real=True, nonzero=True)
    _require(h.subs(symbol, nonzero).is_positive is True,
             "Q20 positive branch on both sides")
    _require((1 + symbol**2).is_positive is True,
             "Q20 smooth real denominator")
    _require(h.subs(symbol, 0) == square_primitive.subs(symbol, 0) == 0,
             "Q20 zero initial data")
    _require(sp.simplify(sp.diff(h, symbol) - symbol / (2 * (1 + symbol**2))) == 0,
             "Q20 divided ODE")
    _require(sp.simplify(square_primitive - h**2) == 0,
             "Q20 square identity")
    _require(sp.simplify(sp.diff(square_primitive, symbol)
                         - symbol * h / (1 + symbol**2)) == 0,
             "Q20 integral-equation primitive")
    _require(sp.simplify(sp.diff(primitive, symbol) - h) == 0,
             "Q20 final integral primitive")
    return sp.simplify(primitive.subs(symbol, 1) - primitive.subs(symbol, -1))


def definite_value(expr, symbol, lo, hi):
    if symbol.is_real is not True:
        return None
    if (lo, hi) == (0, 1) and open_integrand(expr, symbol):
        return _shuttle_value()
    if (lo, hi) == (-1, 1) and expr == sp.log(1 + symbol**2) / 4:
        return _volterra_value(symbol)
    return None


def transcripts():
    """id -> (kind, full SymPy question, limits, SymPy answer, variable name)."""
    x = sp.Symbol("x", real=True)
    n = sp.Symbol("n", positive=True, integer=True)
    return {
        "R2-2021-Relay-D03": (
            "definite", _shuttle_form(x), (0, 1), (1 + sp.sqrt(5)) / 2, "x",
        ),
        "R2-2023-Relay-Q19": (
            "expression",
            sp.Limit(sp.Integral(sp.cos(x / sp.sqrt(n))**n,
                                 (x, 0, sp.sqrt(n))), n, sp.oo),
            None, sp.sqrt(sp.pi / 2), "x",
        ),
        "R2-2023-Relay-Q20": (
            "definite", sp.log(1 + x**2) / 4, (-1, 1),
            (sp.pi + sp.log(4) - 4) / 4, "x",
        ),
    }
