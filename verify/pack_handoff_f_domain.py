"""A complete real-parameter answer for Relay 2022 Q15.

The question gives no domain for n.  Its printed finite answer is valid only
for n > 2.  This certificate retains the original integral and proves both
branches over the explicitly adopted real domain.  In particular, substituting
n = 2+a in the proof does not restrict or rename the catalog's parameter.
"""

from __future__ import annotations

import sympy as sp


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ArithmeticError("handoff-f-domain: " + label)


def _zero(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _parameter(expr, symbol, limits):
    if limits is None or tuple(limits) != (0, sp.oo):
        return None
    if not isinstance(expr, sp.Integral) or expr.limits != ((symbol, 0, sp.oo),):
        return None
    parameters = expr.free_symbols
    if len(parameters) != 1:
        return None
    n = next(iter(parameters))
    if (
        not isinstance(n, sp.Symbol)
        or n.name == symbol.name
        or n != sp.Symbol(n.name, real=True)
        or expr.function != sp.acot(symbol ** (n / 2))
    ):
        return None
    return n


def open_expression(expr, symbol):
    return _parameter(expr, symbol, (0, sp.oo)) is not None


def _value(n):
    x, z, v, a = sp.symbols("_fd_x _fd_z _fd_v _fd_a", positive=True)
    h, b, ell = sp.symbols("_fd_h _fd_b _fd_ell", nonnegative=True)

    # On positive arguments acot decreases strictly from pi/2 to zero.
    # Thus 0 < acot(z) < pi/2, so every real n is integrable near x=0.
    _require(sp.diff(sp.acot(z), z) == -1 / (1 + z**2), "acot-derivative")
    _require(sp.diff(sp.acot(z), z).is_negative is True, "acot-decreasing")
    _require(sp.limit(sp.acot(z), z, 0, dir="+") == sp.pi / 2, "acot-at-zero")
    _require(sp.limit(sp.acot(z), z, sp.oo) == 0, "acot-at-infinity")
    _require(sp.integrate(sp.pi / 2, (x, 0, 1)).is_finite is True, "origin-majorant")

    # 1/z-acot(z) decreases to zero, proving acot(z) <= 1/z for z>0.
    upper_gap = 1 / z - sp.acot(z)
    upper_derivative = -1 / (z**2 * (1 + z**2))
    _require(_zero(sp.diff(upper_gap, z) - upper_derivative), "upper-gap-derivative")
    _require(upper_derivative.is_negative is True, "upper-gap-decreasing")
    _require(sp.limit(upper_gap, z, sp.oo) == 0, "upper-gap-limit")

    # a>0 parametrizes exactly the convergent branch n>2.  The endpoint
    # bounds justify integration by parts on the whole improper integral.
    convergent_n = 2 + a
    p = convergent_n / 2
    f = sp.acot(x**p)
    tail_majorant = sp.integrate(x ** (-p), (x, 1, sp.oo))
    _require(tail_majorant == 2 / a and tail_majorant.is_finite is True, "finite-tail")
    _require(sp.limit(x * sp.pi / 2, x, 0, dir="+") == 0, "parts-origin")
    _require(_zero(1 - p + a / 2), "parts-tail-exponent")
    _require(sp.limit(x ** (-a / 2), x, sp.oo) == 0, "parts-tail")
    reduced = p * x**p / (1 + x**convergent_n)
    _require(_zero(sp.diff(x * f, x) - f + reduced), "parts-identity")

    # v=x^n takes (0,infinity) monotonically onto itself.  SymPy evaluates
    # the resulting convergent beta integral; the gamma reflection check
    # independently identifies its finite value with the printed formula.
    mapping = v ** (1 / convergent_n)
    jacobian = sp.diff(mapping, v)
    _require(jacobian.is_positive is True, "power-orientation")
    _require(sp.limit(mapping, v, 0, dir="+") == 0, "power-origin")
    _require(sp.limit(mapping, v, sp.oo) == sp.oo, "power-infinity")
    alpha = sp.Rational(1, 2) + 1 / convergent_n
    _require(alpha.is_positive is True, "beta-lower-domain")
    _require(sp.factor(1 - alpha).is_positive is True, "beta-upper-domain")
    beta_kernel = v ** (alpha - 1) / (1 + v)
    pulled = reduced.subs(x, mapping) * jacobian
    _require(_zero(pulled - beta_kernel / 2), "power-substitution")
    beta_value = sp.integrate(beta_kernel, (v, 0, sp.oo))
    reflected = sp.gammasimp(sp.gamma(alpha) * sp.gamma(1 - alpha))
    _require(_zero(beta_value - reflected), "beta-reflection")
    finite_value = beta_value / 2
    _require(
        _zero(finite_value - sp.pi / (2 * sp.cos(sp.pi / convergent_n))),
        "finite-branch",
    )

    # b>=0 parametrizes every remaining real n as n=2-b.  Writing x=exp(ell)
    # with ell>=0 covers x>=1, and x^(n/2)/x=exp(-b*ell/2)<=1.
    # Monotonicity therefore gives acot(x^(n/2)) >= acot(x) on that ray.
    _require(_zero((2 - b) / 2 - 1 + b / 2), "divergent-exponent")
    _require((-b * ell / 2).is_nonpositive is True, "divergent-power-order")

    # For z>=1, acot(z)-1/(2z) decreases to zero and is nonnegative.
    # Its derivative at z=1+h is explicitly nonpositive for all h>=0.
    lower_gap = sp.acot(z) - 1 / (2 * z)
    lower_derivative = -h * (h + 2) / (2 * (1 + h) ** 2 * (1 + (1 + h) ** 2))
    _require(
        _zero(sp.diff(lower_gap, z).subs(z, 1 + h) - lower_derivative),
        "lower-gap-derivative",
    )
    _require(lower_derivative.is_nonpositive is True, "lower-gap-decreasing")
    _require(sp.limit(lower_gap, z, sp.oo) == 0, "lower-gap-limit")
    tail_lower = sp.integrate(1 / (2 * x), (x, 1, z))
    _require(sp.limit(tail_lower, z, sp.oo) == sp.oo, "divergent-tail")

    return sp.Piecewise((sp.pi / (2 * sp.cos(sp.pi / n)), n > 2), (sp.oo, True))


def answer_value(kind, expr, symbol, limits):
    if kind != "domain":
        return None
    n = _parameter(expr, symbol, limits)
    return None if n is None else _value(n)


def transcripts():
    x, n = sp.symbols("x n", real=True)
    expr = sp.Integral(sp.acot(x ** (n / 2)), (x, 0, sp.oo))
    answer = sp.Piecewise((sp.pi / (2 * sp.cos(sp.pi / n)), n > 2), (sp.oo, True))
    return {
        "R2-2022-Relay-Q15": (
            "domain",
            sp.srepr(expr),
            ("0", "oo"),
            sp.srepr(answer),
            "x",
        )
    }
