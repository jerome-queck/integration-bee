"""Typed integral certificates for the four Handoff F integral contracts.

The full limit remains the problem expression for the shuttle and Dichotomy
rows.  D1's answer is the unordered prime-factor pair, not its integral value.
The product-indefinite kind denotes the printed multiplicative integral and
uses a positive logarithmic derivative, never the ordinary derivative test.

Sources: the 2021 shuttle, pp. 3 and 5, and mark scheme, p. 4; Singapore 2025
relay, p. 5; 2024 Dichotomy Segment 2, p. 4, answers, p. 5, and solutions,
p. 12.  The B3 paper passes b=0, without writing a limit.  Its printed -oo
answer is interpreted explicitly as the positive-parameter limit b -> 0+.
"""

from __future__ import annotations

import sympy as sp

import pack_handoff_b
import pack_handoff_d_2021


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-f-integrals certificate: " + label)


def _zero(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _limit_shape(expr, symbol):
    """Match the complete original integral, parameter, endpoint and side."""
    if not isinstance(expr, sp.Limit):
        return None
    inner, parameter, endpoint, direction = expr.args
    if not isinstance(parameter, sp.Symbol) or parameter.name == symbol.name:
        return None
    if not isinstance(inner, sp.Integral) or len(inner.limits) != 1:
        return None
    bounds = inner.limits[0]
    if len(bounds) != 3 or bounds[0] != symbol:
        return None
    _, lo, hi = bounds
    if (lo, hi) == (0, 1) and endpoint == 0 and direction == sp.Symbol("+"):
        # The adopted b -> 0+ interpretation uses a continuous positive
        # parameter.  In particular, positive integers cannot approach 0.
        if parameter != sp.Symbol(parameter.name, positive=True):
            return None
        expected = sp.log(parameter * (symbol + 1)) / (symbol**2 + 1)
        if inner.function == expected:
            return "shuttle-negative-infinity", parameter, inner
    if parameter.is_integer is not True or parameter.is_positive is not True:
        return None
    if endpoint != sp.oo or direction != sp.Symbol("-"):
        return None
    if (lo, hi) == (sp.Rational(5, 6), sp.oo):
        if inner.function == sp.exp(-symbol**parameter):
            return "shuttle-prime-factors", parameter, inner
    if (lo, hi) == (1, parameter):
        expected = sp.log(1 + sp.E / parameter + (parameter * symbol)**(-1 / sp.E))
        if inner.function == expected:
            return "dichotomy-positive-infinity", parameter, inner
    return None


def _shuttle_negative_infinity():
    # Re-derive B1=0, B2=13*pi and its second digit.  This is the same
    # checked pass-on chain used by the existing B2 catalog certificate.
    received = pack_handoff_d_2021._d21_b2()
    _require(received == 0, "B3-received-parameter")
    x, b = sp.symbols("_f_b3_x _f_b3_b", positive=True)
    original = sp.log(b * (x + 1)) / (1 + x**2)
    split = sp.log(b) / (1 + x**2) + sp.log(x + 1) / (1 + x**2)
    _require(_zero(sp.expand_log(original) - split), "B3-log-splitting")
    primitive = sp.atan(x)
    _require(sp.diff(primitive, x) == 1 / (1 + x**2), "B3-Cauchy-primitive")
    weight = primitive.subs(x, 1) - primitive.subs(x, 0)
    _require(weight == sp.pi / 4 and weight.is_positive is True, "B3-positive-mass")
    # On [0,1], 0 <= log(1+x) <= log 2.  The denominator is >=1,
    # so the remainder is continuous and its integral lies in [0,log(2)].
    _require(sp.diff(sp.log(1 + x), x).is_positive is True, "B3-log-monotonicity")
    _require(sp.log(1 + x).subs(x, 0) == 0, "B3-remainder-left")
    bound = sp.integrate(sp.log(2), (x, 0, 1))
    _require(bound.is_finite is True and bound.is_positive is True, "B3-remainder-bound")
    lower = sp.limit(weight * sp.log(b), b, 0, dir="+")
    upper = sp.limit(weight * sp.log(b) + bound, b, 0, dir="+")
    _require(lower == upper == -sp.oo, "B3-squeeze-negative-infinity")
    return upper


def _shuttle_prime_factors():
    # The existing certificate controls the entire improper integral: on
    # [5/6,1] its error is bounded by integral x**n; above 1 Bernoulli gives
    # e**(-x**n) <= e**(-1-n*(x-1)).  Both error integrals tend to zero.
    # It then reduces the resulting 1/6 and factors its denominator.
    factors = pack_handoff_d_2021._d21_d1_parameters()
    _require(len(factors) == 2 and all(sp.isprime(p) for p in factors), "D1-prime-pair")
    _require(sp.prod(factors) == 6, "D1-denominator-product")
    return sp.Tuple(*sorted(factors))


def _product_primitive(symbol):
    x = sp.Symbol("_f_product_x", positive=True)
    logarithm = x**2 * sp.log(x) / 2 - x**2 / 4
    _require(_zero(sp.diff(logarithm, x) - x * sp.log(x)), "product-IBP")
    _require(sp.expand_log(sp.log(x**x)) == x * sp.log(x), "product-log-integrand")
    primitive = x**(x**2 / 2) * sp.exp(-x**2 / 4)
    _require(primitive.is_positive is True, "product-positive-primitive")
    _require(_zero(sp.diff(primitive, x) / primitive - sp.diff(logarithm, x)),
             "product-log-derivative")
    return primitive.subs(x, symbol)


def answer_value(kind, expr, symbol, limits):
    """Return the proved mathematical answer; None means unsupported shape.

    ``limits`` contains parsed SymPy endpoints, matching the bounds inside
    the complete limit.  The product kind has empty bounds.  Its returned
    primitive is one representative; use ``product_answer_ok`` to compare
    candidates modulo a positive multiplicative constant.
    """
    if kind == "product_indefinite":
        if limits not in (None, [], ()) or expr != symbol**symbol:
            return None
        return _product_primitive(symbol)
    shape = _limit_shape(expr, symbol)
    if shape is None or limits is None or len(limits) != 2:
        return None
    tag, _parameter, inner = shape
    if tuple(limits) != tuple(inner.limits[0][1:]):
        return None
    if kind == "prime_factors" and tag == "shuttle-prime-factors":
        return _shuttle_prime_factors()
    if kind != "definite":
        return None
    if tag == "shuttle-negative-infinity":
        return _shuttle_negative_infinity()
    if tag == "dichotomy-positive-infinity":
        # The existing exact lower bound is (n-1)/(1+n**(2/E)).
        # It tends to oo because 1-2/E>0; this preserves the whole limit
        # and rejects changed bounds, changed root powers and wrong sides.
        value = pack_handoff_b.definite_value(expr, symbol, *limits)
        _require(value == sp.oo, "dichotomy-divergent-lower-bound")
        return value
    return None


def definite_value(expr, symbol, lo, hi):
    return answer_value("definite", expr, symbol, (lo, hi))


def open_integrand(expr, symbol):
    return _limit_shape(expr, symbol) is not None


def product_answer_ok(expr, answer, symbol):
    """Check the positive product primitive on x>0, with C>0 if present.

    The caller must parse C with the positive assumption for this kind.
    An explicitly nonpositive C is rejected, as are zero, negative
    primitives, additive shifts, and expressions with unevaluated calculus.
    No convention for an ordinary additive antiderivative is changed here.
    """
    if expr != symbol**symbol or not isinstance(answer, sp.Expr):
        return False
    if answer.has(sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.Derivative,
                  sp.Piecewise, sp.nan, sp.zoo, sp.oo, -sp.oo):
        return False
    constants = answer.free_symbols - {symbol}
    if any(c.name != "C" or c.is_positive is not True for c in constants):
        return False
    if len(constants) > 1:
        return False
    x = sp.Symbol("_f_product_x", positive=True)
    candidate = answer.xreplace({symbol: x})
    if candidate.is_positive is not True:
        return False
    # A formally zero logarithmic derivative can hide jumps: for example
    # exp(atan(tan(x))-x) has different constant values between poles.
    # A product primitive uses one constant on the entire positive ray.
    ray = sp.Interval.open(0, sp.oo)
    try:
        derivative = sp.diff(candidate, x)
        if (sp.calculus.util.continuous_domain(candidate, x, ray) != ray
                or sp.calculus.util.continuous_domain(derivative, x, ray) != ray):
            return False
    except (NotImplementedError, ValueError, TypeError):
        return False
    _product_primitive(symbol)
    return _zero(derivative / candidate - x * sp.log(x))


def transcripts():
    """Typed source readings: id -> (kind, expression, limits, answer, var)."""
    b = "Symbol('b', positive=True)"
    n = "Symbol('n', positive=True, integer=True)"
    return {
        "R2-2021-Relay-B03": (
            "definite",
            f"Limit(Integral(log({b}*(x+1))/(x**2+1),(x,0,1)),{b},0,dir='+')",
            ("0", "1"), "-oo", "x",
        ),
        "R2-2021-Relay-D01": (
            "prime_factors",
            f"Limit(Integral(exp(-x**{n}),(x,Rational(5,6),oo)),{n},oo)",
            ("5/6", "oo"), "Tuple(2,3)", "x",
        ),
        "R2-2025-SG-Relay-Q17": (
            "product_indefinite", "x**x", (),
            "Symbol('C', positive=True)*x**(x**2/2)*exp(-x**2/4)", "x",
        ),
        "R3-2024-Dichotomy-S2-Q07a": (
            "definite",
            f"Limit(Integral(log(1+E/{n}+({n}*x)**(-1/E)),(x,1,{n})),{n},oo)",
            ("1", n), "oo", "x",
        ),
    }
