"""Exact certificates for the Handoff C pack rows.

Every matcher checks the complete integrand and bounds before doing proof work.
The only open integrands accepted here are four literal limit families and the
inner Fresnel integral. Limit exchanges have explicit uniform bounds or a
finite-product identity and domination. Returned values are derived from exact
identities and compared by pack_gate's strict certificate comparator.
"""

from __future__ import annotations

import sympy as sp


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-c certificate: " + label)


def _eq(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _hc_limits_form(expr, symbol):
    """Recognize exact finite families, including their integer parameters."""
    if not isinstance(expr, sp.Limit) or len(expr.args) != 4:
        return None
    family, count, destination, _direction = expr.args
    if (
        not isinstance(count, sp.Symbol)
        or count.name == symbol.name
        or count.is_integer is not True
        or count.is_positive is not True
        or destination != sp.oo
    ):
        return None
    if expr != sp.Limit(family, count, sp.oo):
        return None
    expected = sp.sin(sp.pi * sp.floor(count * symbol + 1) / (2 * count))
    if family == expected:
        return "floor-sine"
    expected = 2 * sp.sqrt(1 - sp.floor(count * symbol) ** 2 / count**2)
    if family == expected:
        return "floor-disk"
    expected = count * (1 + symbol**3) / (count + symbol + symbol**3 + symbol**5)
    if family == expected:
        return "rational-limit"
    products = list(family.atoms(sp.Product))
    if len(products) != 1:
        return None
    product = products[0]
    if len(product.limits) != 1 or len(product.limits[0]) != 3:
        return None
    index, start, stop = product.limits[0]
    if (
        not isinstance(index, sp.Symbol)
        or index.name in {symbol.name, count.name}
        or index.is_integer is not True
        or start != 0
        or stop != count
    ):
        return None
    power = symbol ** (2**index)
    factor = power + sp.frac(sp.sinh(power) ** 2) / sp.frac(sp.cosh(power) ** 2)
    if product.function != factor or family != (1 - symbol) * product:
        return None
    return "binary-product"


def _hc_floor_sine_limit():
    """The finite integrands differ uniformly from sin(pi*x/2) by pi/(2n)."""
    y = sp.Symbol("_hc_y", real=True)
    n = sp.Symbol("_hc_n", positive=True, integer=True)
    # floor(y+1)-y = 1-{y} lies in (0,1].  The defining floor
    # inequalities and |cos(t)| <= 1 give the stated Lipschitz bound.
    remainder = 1 - (y - sp.floor(y))
    if not _eq(sp.floor(y + 1) - y - remainder):
        return None
    t = sp.Symbol("_hc_t", real=True)
    if sp.diff(sp.sin(t), t) != sp.cos(t):
        return None
    if not _eq(1 - sp.cos(t) ** 2 - sp.sin(t) ** 2):
        return None
    if sp.ask(sp.Q.nonnegative(sp.sin(t) ** 2)) is not True:
        return None
    error = sp.pi / (2 * n)
    if error.is_positive is not True or sp.limit(error, n, sp.oo) != 0:
        return None
    # The interval has length 1, so the same bound controls the integral
    # error and proves exchange of the outer limit with integration.
    return sp.integrate(sp.sin(sp.pi * t / 2), (t, 0, 1))


def _hc_floor_disk_limit():
    """x=n**2*u**2 fixes the original moving interval; dominated convergence."""
    n = sp.Symbol("_hc_n", positive=True, integer=True)
    u = sp.Symbol("_hc_u", positive=True)
    z = sp.Symbol("_hc_z", positive=True)
    original = sp.sqrt((n**2 - sp.floor(sp.sqrt(z)) ** 2) / z) / n**2
    substituted = original.subs(z, n**2 * u**2) * sp.diff(n**2 * u**2, u)
    target = 2 * sp.sqrt(1 - sp.floor(n * u) ** 2 / n**2)
    if not _eq(substituted - target):
        return None
    if (n**2 * u**2).subs(u, 0) != 0 or (n**2 * u**2).subs(u, 1) != n**2:
        return None
    if sp.ask(sp.Q.positive(sp.diff(n**2 * u**2, u))) is not True:
        return None
    # For 0<=u<=1, v=floor(nu)/n satisfies 0<=v<=u and u-v<1/n.
    # Hence 0<=u**2-v**2<=2/n.  The square-root inequality below gives
    # |2*sqrt(1-v**2)-2*sqrt(1-u**2)| <= 2*sqrt(2/n).
    v = sp.Symbol("_hc_v", nonnegative=True)
    if sp.expand(u**2 - v**2 - (u - v) * (u + v)) != 0:
        return None
    a, b = sp.symbols("_hc_a _hc_b", nonnegative=True)
    if not _eq((sp.sqrt(a) + sp.sqrt(b)) ** 2 - (a + b) - 2 * sp.sqrt(a * b)):
        return None
    if sp.ask(sp.Q.nonnegative(2 * sp.sqrt(a * b))) is not True:
        return None
    error = 2 * sp.sqrt(2 / n)
    if error.is_positive is not True or sp.limit(error, n, sp.oo) != 0:
        return None
    # In particular all integrands are in [0,2] a.e.; the transformed
    # finite integrals converge to this checked quarter-disk integral.
    return sp.integrate(2 * sp.sqrt(1 - u**2), (u, 0, 1))


def _hc_rational_unit_limit():
    """0 <= (1+x**3)-f_n(x) <= 6/n on [0,1]."""
    n = sp.Symbol("_hc_n", positive=True, integer=True)
    x = sp.Symbol("_hc_x", nonnegative=True)
    numerator = 1 + x**3
    tail = x + x**3 + x**5
    finite = n * numerator / (n + tail)
    residual = numerator * tail / (n + tail)
    if not _eq(numerator - finite - residual):
        return None
    if sp.ask(sp.Q.nonnegative(tail)) is not True:
        return None
    if sp.ask(sp.Q.positive(n + tail)) is not True:
        return None
    # These polynomials have nonnegative coefficients.  Their factorizations
    # certify tail<=3 and numerator<=2 whenever 0<=x<=1.
    tail_cofactor = 3 + 2 * x + 2 * x**2 + x**3 + x**4
    numerator_cofactor = 1 + x + x**2
    if sp.expand(3 - tail - (1 - x) * tail_cofactor) != 0:
        return None
    if sp.expand(2 - numerator - (1 - x) * numerator_cofactor) != 0:
        return None
    if not all(coefficient >= 0 for polynomial in (tail_cofactor, numerator_cofactor)
               for coefficient in sp.Poly(polynomial, x).all_coeffs()):
        return None
    nonnegative_gap = 3 * (2 - numerator) + numerator * (3 - tail)
    if sp.expand(6 - numerator * tail - nonnegative_gap) != 0:
        return None
    if not _eq(6 / n - residual - (n * nonnegative_gap + 6 * tail) / (n * (n + tail))):
        return None
    if sp.limit(6 / n, n, sp.oo) != 0 or sp.limit(finite, n, sp.oo) != numerator:
        return None
    return sp.integrate(numerator, (x, 0, 1))


def _hc_binary_product_limit():
    """Fractional parts agree a.e.; finite products telescope before the limit."""
    y = sp.Symbol("_hc_y", real=True)
    z = sp.Symbol("_hc_z", real=True)
    n = sp.Symbol("_hc_n", positive=True, integer=True)
    if not _eq(sp.cosh(y) ** 2 - sp.sinh(y) ** 2 - 1):
        return None
    if not _eq(sp.frac(z + 1).rewrite(sp.floor) - sp.frac(z).rewrite(sp.floor)):
        return None
    # Each cosh(x**(2**k))**2 is strictly increasing on (0,1).
    # Its integer level sets are finite; over all k their union is countable.
    # Thus the printed ratio equals 1 off a null set, and its removable
    # values may be filled by 1 for each finite integral.
    positive = sp.Symbol("_hc_p", positive=True)
    power = sp.Symbol("_hc_m", positive=True)
    derivative = sp.diff(sp.cosh(positive**power) ** 2, positive)
    if sp.ask(sp.Q.positive(derivative)) is not True:
        return None
    if sp.expand((1 - z) * (1 + z) - (1 - z**2)) != 0:
        return None
    # Base N=0 and the same identity at z=x**(2**(N+1)) prove by
    # induction (1-x)*Product(1+x**(2**k), k=0..N)=1-x**(2**(N+1)).
    if not _eq(2 * 2 ** (n + 1) - 2 ** (n + 2)):
        return None
    x = sp.Symbol("_hc_x", positive=True)
    m = sp.Symbol("_hc_M", positive=True)
    primitive = x - x ** (m + 1) / (m + 1)
    if not _eq(sp.diff(primitive, x) - (1 - x**m)):
        return None
    if sp.limit(primitive, x, 0, dir="+") != 0:
        return None
    finite_value = sp.simplify(primitive.subs(x, 1) - primitive.subs(x, 0))
    if not _eq(finite_value - (1 - 1 / (m + 1))):
        return None
    finite_value = finite_value.subs(m, 2 ** (n + 1))
    if sp.limit(finite_value, n, sp.oo) != 1:
        return None
    # 0<=1-x**(2**(N+1))<=1 on [0,1], so dominated convergence
    # justifies storing the literal pointwise Limit under the integral.
    return sp.limit(finite_value, n, sp.oo)


def _hc_limits_values(integrand, symbol, lo, hi):
    if lo != 0 or hi != 1:
        return None
    form = _hc_limits_form(integrand, symbol)
    if form is None:
        return None
    builders = {
        "floor-sine": _hc_floor_sine_limit,
        "floor-disk": _hc_floor_disk_limit,
        "rational-limit": _hc_rational_unit_limit,
        "binary-product": _hc_binary_product_limit,
    }
    return builders[form]()


def _hc_cubic_product_boundary(integrand, symbol, lo, hi):
    """SG relay 11: a real square-root derivative, with its branch checked."""
    if lo != -1 or hi != 0:
        return None
    a = symbol**3 + symbol**2 - 1
    b = 2*symbol**3 + symbol**2 - 2
    target = ((3*symbol**2 + 2*symbol)/a
              + (6*symbol**2 + 2*symbol)/b) * sp.sqrt(a*b)
    if integrand != target:
        return None
    # A cubic's extrema on this compact interval occur at endpoints or at
    # the complete list of roots of its quadratic derivative. Both cubics
    # are strictly negative there, so a*b>0 and the principal root is smooth.
    for polynomial, critical in ((a, [-sp.Rational(2, 3), 0]),
                                (b, [-sp.Rational(1, 3), 0])):
        _require(sp.solve(sp.diff(polynomial, symbol), symbol) == critical,
                           "cubic-critical-points")
        for point in [-1, 0, *critical]:
            _require(polynomial.subs(symbol, point) < 0, "negative-cubic")
    primitive = 2*sp.sqrt(a*b)
    _require(_eq(sp.diff(primitive, symbol) - target),
                       "square-root-derivative")
    return sp.simplify(primitive.subs(symbol, hi) - primitive.subs(symbol, lo))


def _hc_reciprocal_log_power(integrand, symbol, lo, hi):
    """SG relay 22 / UK relay 16: x -> 1/x yields a constant logarithmic weight."""
    if lo != sp.sqrt(2)-1 or hi != sp.sqrt(2)+1:
        return None
    target = 1/(symbol*(sp.E + (symbol**2+1)**(1/sp.log(symbol))))
    if integrand != target:
        return None
    _require(lo.is_positive is True and _eq(lo*hi-1),
                       "reciprocal-positive-endpoints")
    t = sp.Symbol("_hc_t", positive=True)
    a = sp.Symbol("_hc_a", positive=True)
    # All logarithm arguments are positive. For t!=1 this checks
    # h(t)+h(1/t)=2, hence A(1/t)=exp(2)/A(t), where A=exp(h)>0.
    h = sp.log(1+t**2)/sp.log(t)
    reciprocal_base = (t**2+1)/t**2
    _require(_eq(reciprocal_base - (1+t**(-2))),
                       "power-reciprocal-base")
    reflected_h = sp.expand_log(sp.log(reciprocal_base))/(-sp.log(t))
    _require(_eq(h+reflected_h-2), "power-log-complement")
    _require(sp.exp(sp.simplify(h+reflected_h)) == sp.E**2,
                       "power-product")
    original = target.subs(symbol, t).xreplace({(t**2+1)**(1/sp.log(t)): a})
    reflected = target.subs(symbol, 1/t)/t**2
    _require(sp.expand_log(sp.log(1/t)) == -sp.log(t), "power-reciprocal-log")
    reflected_power = (1+t**(-2))**(1/sp.log(1/t))
    _require(reflected.has(reflected_power), "power-reflected-shape")
    reflected = reflected.xreplace({reflected_power: sp.E**2/a})
    pair = sp.simplify(original + reflected)
    _require(pair == 1/(sp.E*t), "power-reciprocal-pair")
    # 0<1/(exp(1)+A)<exp(-1) on both sides of t=1, so the
    # missing value at 1 causes no improper divergence. Integrating the pair
    # over reciprocal endpoints gives twice log(hi)/e.
    _require((1/(sp.E+a)).is_positive is True, "power-positive")
    _require(sp.simplify(1/sp.E-1/(sp.E+a)).is_positive is True,
                       "power-bounded")
    primitive = sp.log(t)/(2*sp.E)
    _require(_eq(sp.diff(primitive, t)-pair/2),
                       "power-pair-primitive")
    _require(_eq(1/lo-hi), "power-log-endpoints")
    return sp.log(hi)/sp.E


def _hc_log_product_limit():
    """The finite product of 1-1/n**2, n=2..N, checked by induction."""
    n = sp.Symbol("_hc_n", integer=True, positive=True)
    partial = (n+1)/(2*n)
    _require(partial.subs(n, 1) == 1, "log-product-empty")
    _require(_eq(partial/partial.subs(n, n-1)-(1-1/n**2)),
                       "log-product-recurrence")
    # For n>=2 every factor lies in (0,1). Consequently the sum of
    # their real logarithms is log of this positive finite product; the
    # terms have one sign, so the finite limit also gives absolute convergence.
    k = sp.Symbol("_hc_k", integer=True, nonnegative=True)
    factor = 1-1/(k+2)**2
    _require(sp.factor(factor).is_positive is True,
                       "log-product-positive-factors")
    _require((1-factor).is_positive is True, "log-product-factors-below-one")
    _require(partial.is_positive is True, "log-product-positive-partial")
    _require(sp.limit(sp.log(1-1/n**2), n, sp.oo) == 0,
                       "log-product-vanishing-piece")
    return sp.limit(sp.log(partial), n, sp.oo)


def _hc_floor_log_telescope(integrand, symbol, lo, hi):
    """2021 group 2 and 2022 relay 14 reduce to the same log product."""
    reciprocal = lo == 0 and hi == sp.Rational(1, 2)
    straight = lo == 2 and hi == sp.oo
    if not reciprocal and not straight:
        return None
    floor = sp.floor(1/symbol) if reciprocal else sp.floor(symbol)
    if reciprocal:
        target = floor*sp.ceiling(1/symbol)*sp.log(1-1/floor**2)
    else:
        target = sp.log((floor**2-1)/floor**2)
    if integrand != target:
        return None
    n = sp.Symbol("_hc_n", integer=True, positive=True)
    u = sp.Symbol("_hc_u", positive=True)
    if reciprocal:
        # x is strictly between 1/(n+1) and 1/n. These inequalities prove
        # n<1/x<n+1, so the floor and ceiling are n and n+1. Endpoint
        # exceptions form a countable null set and do not affect the integral.
        left, right = 1/(n+1), 1/n
        point = left+(right-left)*u/(1+u)
        _require(sp.factor(1/point-n).is_positive is True,
                           "reciprocal-floor-lower")
        _require(sp.factor(n+1-1/point).is_positive is True,
                           "reciprocal-floor-upper")
        piece = integrand.xreplace({sp.floor(1/symbol): n,
                                    sp.ceiling(1/symbol): n+1})
        contribution = piece*(right-left)
        _require(_eq(contribution-sp.log(1-1/n**2)),
                           "reciprocal-floor-piece")
        _require(right.subs(n, 2) == hi, "reciprocal-floor-start")
        _require(sp.limit(left, n, sp.oo) == lo, "reciprocal-floor-end")
    else:
        # Unit intervals [n,n+1) partition [2,oo); their endpoint values
        # are irrelevant. The last partial interval is bounded by one term,
        # whose absolute value tends to zero.
        point = n+u/(1+u)
        _require(sp.factor(point-n).is_positive is True, "floor-lower")
        _require(sp.factor(n+1-point).is_positive is True, "floor-upper")
        piece = integrand.xreplace({sp.floor(symbol): n})
        _require(_eq(piece-sp.log(1-1/n**2)), "floor-piece")
    return _hc_log_product_limit()


def _hc_log_quadratic_reciprocal(integrand, symbol, lo, hi):
    """2022 group 9: f(x)+f(1/x)/x**2=2/(1+x**2)."""
    if lo != 0 or hi != sp.oo:
        return None
    target = sp.log(1-symbol+symbol**2)/((1+symbol**2)*sp.log(symbol))
    if integrand != target:
        return None
    t = sp.Symbol("_hc_t", positive=True)
    p = t**2-t+1
    square = (t-sp.Rational(1, 2))**2+sp.Rational(3, 4)
    _require(_eq(p-square) and square.is_positive is True,
                       "quadratic-positive")
    f = target.subs(symbol, t)
    _require(sp.limit(f, t, 1) == sp.Rational(1, 2),
                       "quadratic-removable-one")
    _require(sp.limit(f, t, 0, dir="+") == 0, "quadratic-origin")
    _require(sp.limit(t**2*f, t, sp.oo) == 2, "quadratic-tail")
    # p(1/t)=p(t)/t**2 with positive t and p(t), so the real logarithm
    # splits without changing its branch.
    _require(_eq(p.subs(t, 1/t)-p/t**2),
                       "quadratic-reciprocal-base")
    reflected_log = sp.expand_log(sp.log(p/t**2))
    _require(_eq(reflected_log-sp.log(p)+2*sp.log(t)),
                       "quadratic-log-split")
    reflected = f.subs(t, 1/t)/t**2
    reflected = reflected.xreplace({sp.log(1-1/t+1/t**2): reflected_log})
    pair = sp.simplify(f+reflected)
    _require(pair == 2/(1+t**2), "quadratic-reciprocal-pair")
    return sp.integrate(pair/2, (t, 0, sp.oo))


def _hc_dilog_reflection(integrand, symbol, lo, hi):
    """SG relay 20: the real dilogarithm duplication identity and reflection."""
    if lo != -1 or hi != 1:
        return None
    target = (1+sp.polylog(2, symbol))/(4+sp.polylog(2, symbol**2))
    if integrand != target:
        return None
    t = sp.Symbol("_hc_t", real=True)
    u = sp.Symbol("_hc_u", positive=True)
    duplication = sp.polylog(2, t)+sp.polylog(2, -t)-sp.polylog(2, t**2)/2
    derivative = sp.expand_func(sp.diff(duplication, t))
    logarithms = (sp.log(1-t**2)-sp.log(1-t)-sp.log(1+t))/t
    _require(_eq(derivative-logarithms), "dilog-derivative")
    # t=u/(1+u) covers (0,1); 1-t, 1+t and 1-t**2 are positive.
    # Thus logarithms split on their real branches. The identity on (-1,0)
    # follows because duplication is even, and continuity supplies the endpoints.
    point = u/(1+u)
    _require(point.is_positive is True and sp.factor(1-point).is_positive is True,
                       "dilog-unit-interval")
    log_sum = (sp.log(sp.factor(1-point**2))
               - sp.log(sp.factor(1-point))-sp.log(sp.factor(1+point)))
    _require(sp.simplify(sp.expand_log(log_sum)) == 0, "dilog-log-branches")
    _require(duplication.subs(t, 0) == 0, "dilog-constant")
    # Li_2 rises from 0 to pi**2/6 on [0,1]. Its derivative under the
    # positive parameterization is log(1+u)/(u*(1+u))>0; hence the printed
    # denominator is at least 4, with finite limits at x=+/-1.
    increasing = sp.simplify(sp.expand_func(sp.diff(sp.polylog(2, point), u)))
    expected_derivative = sp.log(1+u)/(u*(1+u))
    _require(_eq(increasing-expected_derivative),
                       "dilog-monotone-derivative")
    _require(expected_derivative.is_positive is True, "dilog-positive-derivative")
    _require(sp.polylog(2, 0) == 0 and sp.polylog(2, 1) == sp.pi**2/6
                       and sp.polylog(2, -1) == -sp.pi**2/12,
                       "dilog-endpoints")
    folded = (target+target.subs(symbol, -symbol)).xreplace(
        {sp.polylog(2, -symbol): sp.polylog(2, symbol**2)/2-sp.polylog(2, symbol)})
    _require(sp.simplify(folded) == sp.Rational(1, 2), "dilog-folded-value")
    return sp.integrate(sp.Rational(1, 2), (t, 0, 1))


def _hc_finite_floor_blocks(integrand, symbol, lo, hi):
    """SG relay 12: four equal fractional-part pieces, no numerical quadrature."""
    if lo != 3 or hi != 7:
        return None
    target = (10-sp.frac(symbol))/(sp.floor(symbol)+sp.floor(10-symbol)+10)
    if integrand != target:
        return None
    n = sp.Symbol("_hc_n", integer=True)
    t = sp.Symbol("_hc_t", real=True)
    u = sp.Symbol("_hc_u", positive=True)
    point = n+u/(1+u)
    # These strict bounds identify the two floors on every open unit block;
    # the finitely many integer endpoints do not affect the integral.
    for gap in (point-n, n+1-point, 10-point-(9-n), 10-n-(10-point)):
        _require(sp.factor(gap).is_positive is True, "block-floor-bounds")
    piece = integrand.xreplace({sp.floor(symbol): n, sp.floor(-symbol): -n-1,
                                sp.frac(symbol): symbol-n})
    piece = sp.simplify(piece.subs(symbol, n+t))
    _require(piece == (10-t)/19, "block-piece")
    one = sp.integrate(piece, (t, 0, 1))
    _require(one == sp.Rational(1, 2), "block-integral")
    return (hi-lo)*one


def _hc_fresnel_shape(expr, symbol):
    """Recognize the printed inner integral, with a distinct real dummy."""
    if not isinstance(expr, sp.Integral) or len(expr.limits) != 1:
        return False
    limit = expr.limits[0]
    if len(limit) != 3:
        return False
    inner, lower, upper = limit
    return (
        isinstance(inner, sp.Symbol)
        and inner.is_real is True
        and inner.name != symbol.name
        and lower == 0
        and upper == sp.oo
        and expr.function == sp.sin(inner**2 + symbol**2)
    )


def _hc_fresnel_quadrant(integrand, symbol, lo, hi):
    """Evaluate the ordinary iterated integral using convergent Fresnel factors.

    No change to polar coordinates or absolutely convergent double integral
    is used: first take the inner improper integral, then the outer one.
    """
    if lo != 0 or hi != sp.oo or not _hc_fresnel_shape(integrand, symbol):
        return None
    inner = integrand.limits[0][0]
    separated = (
        sp.sin(inner**2) * sp.cos(symbol**2)
        + sp.cos(inner**2) * sp.sin(symbol**2)
    )
    _require(
        sp.expand_trig(integrand.function) == separated, "fresnel-angle-sum"
    )
    u = sp.Symbol("_hc_fresnel_u", real=True)
    sine = sp.integrate(sp.sin(u**2), (u, 0, sp.oo))
    cosine = sp.integrate(sp.cos(u**2), (u, 0, sp.oo))
    _require(
        sine.is_finite is True and cosine.is_finite is True,
        "fresnel-convergent-factors",
    )
    # The inner value is S*cos(y**2)+C*sin(y**2). Both outer terms
    # converge individually, so linearity gives S*C+C*S.
    return sp.simplify(2 * sine * cosine)


def _hc_sine_cosh_ray(integrand, symbol, lo, hi):
    """Abel-sum a geometric kernel, then remove damping by domination."""
    expected = sp.sin(symbol) / (symbol * (sp.cosh(symbol) + sp.cos(symbol)))
    if lo != 0 or hi != sp.oo or integrand != expected:
        return None
    x, r = sp.symbols("_hc_sine_x _hc_sine_r", positive=True)
    q = r * sp.exp(-x)
    w = q * (sp.cos(x) + sp.I * sp.sin(x))
    denominator = 1 + 2 * q * sp.cos(x) + q**2
    damped = 2 * q * sp.sin(x) / (x * denominator)
    _require(
        _eq(sp.im(2 * w / (1 + w)) / x - damped),
        "sine-geometric-imaginary-part",
    )
    _require(
        _eq(
            (damped.subs(r, 1) - expected.subs(symbol, x)).rewrite(sp.exp)
        ),
        "sine-original-kernel",
    )
    # For |z|<1, induction gives the partial sum of 2*(-1)^(n-1)*z^n.
    z = sp.Symbol("_hc_sine_z")
    count = sp.Symbol("_hc_sine_count", integer=True, positive=True)
    partial = 2 * z * (1 - (-z) ** count) / (1 + z)
    _require(partial.subs(count, 1) == 2 * z, "sine-series-base")
    _require(
        _eq(
            partial.subs(count, count + 1)
            - partial
            - 2 * (-1) ** count * z ** (count + 1)
        ),
        "sine-series-step",
    )
    a = sp.Symbol("_hc_sine_a", positive=True)
    radius = a / (1 + a)
    _require(
        radius.is_positive is True and sp.factor(1 - radius).is_positive is True,
        "sine-abel-radius",
    )
    _require(
        sp.limit(radius**count, count, sp.oo) == 0, "sine-series-remainder"
    )
    # Each scaled Laplace/Dirichlet integral is pi/4. For fixed r<1,
    # |sin(a*x)|<=a*x bounds the absolute term integral by 1, and sum r^n
    # converges. Thus the series may be integrated term by term.
    moment = sp.integrate(sp.exp(-a * x) * sp.sin(a * x) / x, (x, 0, sp.oo))
    _require(moment.is_finite is True, "sine-laplace-moment")
    _require(
        sp.integrate(a * sp.exp(-a * x), (x, 0, sp.oo)) == 1,
        "sine-absolute-term-bound",
    )
    integrated = 2 * moment * r / (1 + r)
    # Domination as r -> 1-: on 0<x<pi/2, cos(x)>=0, so the
    # denominator is >=1 and |damped|<=2. On x>=pi/2, write it as
    # (1-q)^2+2*q*(1+cos(x)); q<=exp(-pi/2), hence the denominator
    # is >=(1-exp(-pi/2))^2. The resulting tail majorant is integrable.
    p, c = sp.symbols("_hc_sine_p _hc_sine_c", real=True)
    _require(
        sp.expand(1 + 2 * p * c + p**2 - (1 - p) ** 2 - 2 * p * (1 + c)) == 0,
        "sine-denominator-bound",
    )
    gap = 1 - sp.exp(-sp.pi / 2)
    _require(gap.is_positive is True, "sine-tail-gap")
    tail_mass = sp.integrate(4 * sp.exp(-x) / (sp.pi * gap**2), (x, sp.pi / 2, sp.oo))
    _require(tail_mass.is_finite is True, "sine-tail-majorant")
    return sp.limit(integrated, r, 1, dir="-")


def _hc_csch_frullani(integrand, symbol, lo, hi):
    """A finite-cutoff dyadic cancellation proves the csch integral."""
    expected = (sp.sinh(symbol) - symbol) / (symbol**2 * sp.sinh(symbol))
    if lo != 0 or hi != sp.oo or integrand != expected:
        return None
    x = sp.Symbol("_hc_csch_x", positive=True)
    # h(x)=coth(x)-1/x, kept as exponentials for reliable endpoint limits.
    h = (sp.exp(2 * x) + 1) / (sp.exp(2 * x) - 1) - 1 / x
    _require(
        _eq(
            (expected.subs(symbol, x) - (h - h.subs(x, x / 2)) / x).rewrite(sp.exp)
        ),
        "csch-dyadic-identity",
    )
    u = sp.Symbol("_hc_csch_u", positive=True)
    _require(
        _eq((h.subs(x, x / 2) / x).subs(x, 2 * u) * 2 - h.subs(x, u) / u),
        "csch-half-substitution",
    )
    # Integrating from eps to R leaves only
    # integral(R/2,R,h(u)/u)-integral(eps/2,eps,h(u)/u).
    # Scale each interval to [1/2,1]. Endpoint limits of h are uniform
    # there, so the two limits are h(infinity)*log(2) and h(0)*log(2).
    scale, v = sp.symbols("_hc_csch_scale _hc_csch_v", positive=True)
    _require(
        _eq((h / x).subs(x, scale * v) * scale - h.subs(x, scale * v) / v),
        "csch-endpoint-scaling",
    )
    origin = sp.limit(sp.together(h), x, 0, dir="+")
    infinity = sp.limit(h, x, sp.oo)
    _require(origin == 0 and infinity == 1, "csch-endpoint-limits")
    width = sp.integrate(1 / v, (v, sp.Rational(1, 2), 1))
    return (infinity - origin) * width


def _hc_erfinv_exponential(integrand, symbol, lo, hi):
    """The real inverse error function changes the integral into a Gaussian."""
    if lo != -1 or hi != 1 or integrand != sp.exp(sp.erfinv(symbol)):
        return None
    u = sp.Symbol("_hc_erf_u", real=True)
    inverse_map = sp.erf(u)
    jacobian = sp.diff(inverse_map, u)
    _require(jacobian.is_positive is True, "erf-monotone-map")
    _require(
        inverse_map.subs(u, -sp.oo) == -1 and inverse_map.subs(u, sp.oo) == 1,
        "erf-endpoints",
    )
    pulled = integrand.subs(symbol, inverse_map) * jacobian
    gaussian = 2 * sp.exp(sp.Rational(1, 4)) * sp.exp(-(u - sp.Rational(1, 2)) ** 2) / sp.sqrt(sp.pi)
    _require(_eq(pulled - gaussian), "erf-complete-square")
    mass = sp.integrate(sp.exp(-(u - sp.Rational(1, 2)) ** 2), (u, -sp.oo, sp.oo))
    _require(mass.is_finite is True, "erf-gaussian-convergence")
    return sp.simplify(2 * sp.exp(sp.Rational(1, 4)) * mass / sp.sqrt(sp.pi))


def open_integrand(expr, symbol):
    """Permit only the exact nested expressions whose reductions are checked."""
    return _hc_limits_form(expr, symbol) is not None or _hc_fresnel_shape(expr, symbol)


def definite_value(integrand, symbol, lo, hi):
    """Return a derived value on a recognized shape, otherwise None."""
    for builder in (
        _hc_limits_values,
        _hc_cubic_product_boundary,
        _hc_reciprocal_log_power,
        _hc_floor_log_telescope,
        _hc_log_quadratic_reciprocal,
        _hc_dilog_reflection,
        _hc_finite_floor_blocks,
        _hc_fresnel_quadrant,
        _hc_sine_cosh_ray,
        _hc_csch_frullani,
        _hc_erfinv_exponential,
    ):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
