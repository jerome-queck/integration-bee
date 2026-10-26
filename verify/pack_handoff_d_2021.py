"""Source-preserving scalar pass-on certificates for the 2021 shuttle.

The source asks for operations on integral values: these are stored as whole
Integral expressions with the printed operation still outside the Integral.
The companion bound metadata must agree with the inner bounds.  Earlier
shuttle parameters are derived afresh, not asserted from the mark scheme.

Sources: sources/past/r2/2021/Shuttle_2021_R2_UK_University_Integration_Bee.pdf,
pages 2--5; Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf, page 4.
The non-scalar prime-factor answer D1 and underdetermined form-extraction D3
stay manual; D1 is nevertheless proved internally to obtain D2's parameters.
"""

from __future__ import annotations

import sympy as sp


def _d21_require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-d-2021 certificate: " + label)


def _d21_zero(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _d21_forms(x):
    """Exact full source operations, after certified preceding pass-ons."""
    value = sp.Symbol("shuttle_value")
    # floor(Integral(...)) may call numerical quadrature in its constructor.
    # Subs retains both the exact source integral and its pass-on operation.
    return {
        "A01": (sp.Subs(value**2, value, sp.Integral(sp.log(x)**2, (x, 0, 1))), 0, 1),
        "A02": (sp.Subs(sp.pi / value, value,
                        sp.Integral(sp.sin(x) / sp.sin(x + sp.pi / 4),
                                   (x, 0, sp.pi / 2))), 0, sp.pi / 2),
        "A03": (sp.Subs(4 * value, value,
                        sp.Integral(1 / (1 + sp.tan(x)**(2 * sp.sqrt(2))),
                                   (x, 0, sp.pi / 2))), 0, sp.pi / 2),
        "B02": (sp.Subs(sp.Mod(sp.floor(value), 10), value,
                        sp.Integral(sp.log(1 + 169 / x**2), (x, 0, sp.oo))), 0, sp.oo),
        "C01": (sp.Subs(value**2 - 2, value,
                        sp.Integral((sp.sin(sp.acot(x)) + sp.cos(sp.atan(x))) /
                                    (x**2 + 1), (x, -1, 1))), -1, 1),
        "C02": (sp.Subs(2 - value, value,
                        sp.Integral(x**3 * sp.exp(-x), (x, 0, 0))), 0, 0),
        "C03": (sp.Subs(sp.floor(sp.Abs(value)) + 1, value,
                        sp.Integral(sp.log(sp.sqrt(x)) /
                        (sp.sqrt(x) * (x + 1)**2), (x, 0, sp.oo))),
                0, sp.oo),
        "D02": (sp.Subs(sp.floor(value) + 1, value,
                        sp.Integral((x**3 - x**2) / sp.log(x), (x, 0, 1))), 0, 1),
    }


def _d21_pi_bounds():
    """Rational bounds from atan(1/2)+atan(1/3)=pi/4; no floats."""
    t = sp.Symbol("_d21_t", positive=True)
    lower, upper = 1 - t**2, 1 - t**2 + t**4
    _d21_require(_d21_zero(1 / (1 + t**2) - lower - t**4 / (1 + t**2)),
                 "atan-lower-remainder")
    _d21_require(_d21_zero(upper - 1 / (1 + t**2) - t**6 / (1 + t**2)),
                 "atan-upper-remainder")
    _d21_require((t**4 / (1 + t**2)).is_positive is True and
                 (t**6 / (1 + t**2)).is_positive is True, "atan-bound-signs")
    a, b = sp.Rational(1, 2), sp.Rational(1, 3)
    angle = sp.atan(a) + sp.atan(b)
    _d21_require(sp.expand_trig(sp.tan(angle)) == 1, "atan-addition")
    # Each positive argument is below 1, so both angles are in (0,pi/4).
    # Their sum is in (0,pi/2), where tan is injective: the sum is pi/4.
    _d21_require(0 < a < 1 and 0 < b < 1, "atan-principal-branch")
    low = 4 * sum(sp.integrate(lower, (t, 0, q)) for q in (a, b))
    high = 4 * sum(sp.integrate(upper, (t, 0, q)) for q in (a, b))
    _d21_require(2 < low < high < 4, "pi-enclosure")
    return low, high


def _d21_a1():
    x = sp.Symbol("_d21_x", positive=True)
    primitive = x * (sp.log(x)**2 - 2 * sp.log(x) + 2)
    _d21_require(_d21_zero(sp.diff(primitive, x) - sp.log(x)**2), "A1-primitive")
    start = sp.limit(primitive, x, 0, dir="+")
    _d21_require(start == 0, "A1-improper-endpoint")
    value = primitive.subs(x, 1) - start
    return value**2


def _d21_a2():
    a = _d21_a1()
    _d21_require(a == 4, "A2-received-parameter")
    x = sp.Symbol("_d21_x", real=True)
    f = sp.sin(x) / sp.sin(x + sp.pi / a)
    _d21_require(sp.trigsimp(f + f.subs(x, sp.pi / 2 - x) - sp.sqrt(2)) == 0,
                 "A2-reflection")
    # The denominator is positive on the entire interval: its argument is
    # between pi/4 and 3pi/4. Reflection therefore preserves this proper integral.
    value = sp.integrate(sp.sqrt(2), (x, 0, sp.pi / 2)) / 2
    _d21_require(value.is_positive is True, "A2-nonzero-integral")
    return sp.simplify(sp.pi / value)


def _d21_a3():
    b = _d21_a2()
    _d21_require(b == 2 * sp.sqrt(2) and b.is_positive is True,
                 "A3-received-parameter")
    x = sp.Symbol("_d21_x", real=True)
    t = sp.Symbol("_d21_t", positive=True)
    _d21_require(sp.trigsimp(sp.tan(sp.pi / 2 - x) - 1 / sp.tan(x)) == 0,
                 "A3-tangent-reflection")
    f = 1 / (1 + t**b)
    _d21_require(_d21_zero(f + f.subs(t, 1 / t) - 1), "A3-power-complement")
    # tan(x)>0 on the open interval; this licenses real powers and reciprocal
    # exponent rules. Each summand is in (0,1), so endpoint integrability holds.
    value = sp.integrate(sp.Integer(1), (x, 0, sp.pi / 2)) / 2
    return 4 * value


def _d21_b2():
    x = sp.Symbol("_d21_x", real=True)
    previous = sp.sin(sp.sin(x) - x)
    _d21_require(sp.trigsimp(previous + previous.subs(x, 2 * sp.pi - x)) == 0,
                 "B1-reflection-zero")
    # B1 is continuous and reflection-odd, so its passed-on value is a=0.
    u = sp.Symbol("_d21_u", positive=True)
    primitive = u * sp.log(1 + 169 / u**2) + 26 * sp.atan(u / 13)
    _d21_require(_d21_zero(sp.diff(primitive, u) - sp.log(1 + 169 / u**2)),
                 "B2-primitive")
    value = sp.limit(primitive, u, sp.oo) - sp.limit(primitive, u, 0, dir="+")
    _d21_require(value == 13 * sp.pi, "B2-improper-value")
    low, high = _d21_pi_bounds()
    low_digit, high_digit = sp.floor(13 * low), sp.floor(13 * high)
    _d21_require(low_digit == high_digit and 10 <= low_digit < 100,
                 "B2-two-digit-integer-part")
    # Both bounds have integer part 40.  For a two-digit positive number,
    # its second digit is the units digit of the integer part.
    return sp.Mod(low_digit, 10)


def _d21_c1():
    x = sp.Symbol("_d21_x", real=True)
    u = sp.Symbol("_d21_u", positive=True)
    f = (sp.sin(sp.acot(x)) + sp.cos(sp.atan(x))) / (x**2 + 1)
    positive_piece = 2 / (1 + u**2)**sp.Rational(3, 2)
    _d21_require(_d21_zero(f.subs(x, -u)), "C1-negative-branch")
    _d21_require(_d21_zero(f.subs(x, u) - positive_piece), "C1-positive-branch")
    # SymPy's signed principal acot branch agrees with the printed mark 0.
    # The paper does not state the branch: the continuous (0,pi) convention
    # would instead give pass-on 6. This qualification is in the source note.
    # Its value at 0 is immaterial to the integral; both one-sided pieces are bounded.
    primitive = 2 * u / sp.sqrt(1 + u**2)
    _d21_require(_d21_zero(sp.diff(primitive, u) - positive_piece), "C1-primitive")
    value = primitive.subs(u, 1) - primitive.subs(u, 0)
    return sp.simplify(value**2 - 2)


def _d21_c2():
    a = _d21_c1()
    _d21_require(a == 0, "C2-received-parameter")
    x = sp.Symbol("_d21_x", real=True)
    value = sp.integrate(x**3 * sp.exp(-x), (x, 0, a))
    return 2 - value


def _d21_c3():
    b = _d21_c2()
    _d21_require(b == 2, "C3-received-parameter")
    x, u, a = sp.symbols("_d21_x _d21_u _d21_a", positive=True)
    original = sp.log(x**(1 / b)) / (x**(1 / b) * (x + 1)**2)
    pulled = original.subs(x, u**2) * 2 * u
    target = 2 * sp.log(u) / (1 + u**2)**2
    _d21_require(_d21_zero(pulled - target), "C3-square-substitution")
    _d21_require((u**2).subs(u, 0) == 0 and sp.limit(u**2, u, sp.oo) == sp.oo,
                 "C3-substitution-endpoints")
    family = sp.log(x) / (a + x**2)
    scaled = family.subs(x, sp.sqrt(a) * u) * sp.sqrt(a)
    reduced = (sp.log(u) + sp.log(a) / 2) / (sp.sqrt(a) * (1 + u**2))
    _d21_require(_d21_zero(sp.expand_log(scaled) - reduced), "C3-parameter-scaling")
    odd = sp.log(u) / (1 + u**2)
    _d21_require(_d21_zero(odd + odd.subs(u, 1 / u) / u**2), "C3-reciprocal-zero")
    # The reciprocal logarithm is absolutely integrable: bound by -log u
    # on (0,1), and by log u/u^2 on (1,oo).
    for majorant, left, right in ((-sp.log(u), 0, 1), (sp.log(u) / u**2, 1, sp.oo)):
        bound = sp.integrate(majorant, (u, left, right))
        _d21_require(bound.is_finite is True, "C3-reciprocal-L1")
    base = sp.limit(sp.atan(u), u, sp.oo) - sp.atan(0)
    _d21_require(sp.diff(sp.atan(u), u) == 1 / (1 + u**2), "C3-Cauchy-primitive")
    formula = sp.log(a) * base / (2 * sp.sqrt(a))
    _d21_require(_d21_zero(sp.diff(family, a) + sp.log(x) / (a + x**2)**2),
                 "C3-differentiate-kernel")
    # For 1/2<=a<=3/2 the derivative is dominated by
    # 4|log x|/(1+x^2)^2, bounded by 4(-log x) below 1 and
    # 4log x/x^4 above 1. These integrable bounds license differentiation.
    for majorant, left, right in ((-4 * sp.log(u), 0, 1),
                                   (4 * sp.log(u) / u**4, 1, sp.oo)):
        bound = sp.integrate(majorant, (u, left, right))
        _d21_require(bound.is_finite is True, "C3-derivative-L1")
    value = sp.simplify(-2 * sp.diff(formula, a).subs(a, 1))
    _d21_require(value == -sp.pi / 2, "C3-derived-integral")
    low, high = _d21_pi_bounds()
    lower_floor, upper_floor = sp.floor(low / 2), sp.floor(high / 2)
    _d21_require(lower_floor == upper_floor, "C3-absolute-value-floor")
    return lower_floor + 1


def _d21_d1_parameters():
    """Squeeze the complete improper integrals, then factor the denominator."""
    x, u = sp.symbols("_d21_x _d21_u", positive=True)
    n = sp.Symbol("_d21_n", integer=True, positive=True)
    # On [5/6,1], 0<=1-exp(-x^n)<=x^n.  The exponential inequality
    # follows because u-1+exp(-u) starts at 0 and has positive derivative.
    gap = u - 1 + sp.exp(-u)
    _d21_require(gap.subs(u, 0) == 0 and sp.diff(gap, u).subs(u, 0) == 0 and
                 sp.diff(gap, u, 2).is_positive is True,
                 "D1-exponential-inequality")
    first_error = sp.integrate(x**n, (x, sp.Rational(5, 6), 1))
    _d21_require(sp.limit(first_error, n, sp.oo) == 0, "D1-bounded-piece-error")
    # For x=1+u>=1, Bernoulli's inequality follows by this induction:
    # P_{n+1}=(1+u)P_n+n*u^2, P_1=0. Hence e^-x^n <= e^(-1-nu).
    polynomial = (1 + u)**n - 1 - n * u
    _d21_require(polynomial.subs(n, 1) == 0, "D1-Bernoulli-base")
    _d21_require(sp.expand(polynomial.subs(n, n + 1) - (1 + u) * polynomial - n*u**2) == 0,
                 "D1-Bernoulli-induction")
    _d21_require((n * u**2).is_positive is True, "D1-Bernoulli-remainder")
    tail = sp.integrate(sp.exp(-1 - n * u), (u, 0, sp.oo))
    _d21_require(sp.limit(tail, n, sp.oo) == 0, "D1-improper-tail-error")
    value = sp.integrate(sp.Integer(1), (x, sp.Rational(5, 6), 1))
    numerator, denominator = value.as_numer_denom()
    _d21_require(sp.gcd(numerator, denominator) == 1, "D1-reduced-fraction")
    primes = sorted(sp.factorint(denominator), reverse=True)
    _d21_require(len(primes) == 2 and all(sp.isprime(p) for p in primes),
                 "D1-prime-factors")
    return tuple(primes)


def _d21_d2():
    a, b = _d21_d1_parameters()
    _d21_require(a == 3 and b == 2 and a > b, "D2-received-parameters")
    x = sp.Symbol("_d21_x", positive=True)
    s = sp.Symbol("_d21_s", positive=True)
    primitive = x**s / sp.log(x)
    _d21_require(sp.diff(primitive, s) == x**s, "D2-parameter-primitive")
    _d21_require(_d21_zero(primitive.subs(s, a) - primitive.subs(s, b)
                          - (x**a - x**b) / sp.log(x)), "D2-parameter-endpoints")
    # x^s>=0 on (0,1), so Tonelli exchanges the two integrals.
    inner = sp.integrate(x**s, (x, 0, 1))
    _d21_require(inner == 1 / (s + 1), "D2-power-integral")
    value = sp.integrate(inner, (s, b, a))
    _d21_require(_d21_zero(value - sp.log(sp.Rational(4, 3))), "D2-derived-integral")
    # Since 1/(a+1)<=1/(s+1)<=1/(b+1), the integral lies between
    # (a-b)/(a+1)=1/4 and (a-b)/(b+1)=1/3, strictly between 0 and 1.
    low, high = sp.Rational(a - b, a + 1), sp.Rational(a - b, b + 1)
    _d21_require(0 < low <= high < 1, "D2-strict-integer-interval")
    return sp.floor(low) + 1


def open_integrand(expr, symbol):
    if not isinstance(expr, sp.Subs):
        return False
    return any(expr == shape[0] for shape in _d21_forms(symbol).values())


def definite_value(integrand, symbol, lo, hi):
    if not isinstance(integrand, sp.Subs):
        return None
    builders = {"A01": _d21_a1, "A02": _d21_a2, "A03": _d21_a3,
                "B02": _d21_b2, "C01": _d21_c1, "C02": _d21_c2,
                "C03": _d21_c3, "D02": _d21_d2}
    for label, (shape, left, right) in _d21_forms(symbol).items():
        if integrand == shape and lo == left and hi == right:
            return builders[label]()
    return None
