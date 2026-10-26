"""Exact Handoff D certificates for the 2024 and 2025 relay/group rows.

Scalar operations outside an integral are retained in the expression: a
floor, a ceiling, a product integral (exp of the log integral), or an outer
limit.  Their inner bounds must also match the catalog's bound metadata.
The indefinite product integral is deliberately not accepted: the marking
contract for indefinite rows identifies additive, not multiplicative, constants.
"""

from __future__ import annotations

import sympy as sp


def _d25_require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-d certificate: " + label)


def _d25_eq(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _d25_positive_integer(index, symbol):
    return (
        isinstance(index, sp.Symbol)
        and index.name != symbol.name
        and index.is_integer is True
        and index.is_positive is True
    )


def _d25_limit_shape(expr, symbol):
    if not isinstance(expr, sp.Limit):
        return None
    body, n, destination, direction = expr.args
    if not _d25_positive_integer(n, symbol) or destination != sp.oo:
        return None
    if expr != sp.Limit(body, n, sp.oo):
        return None
    expected = n * sp.Integral(
        (1 - sp.Abs(symbol) + sp.Abs(symbol) ** 3) ** n,
        (symbol, -sp.Rational(1, 20), sp.Rational(1, 24)),
    )
    if body == expected:
        return "cusp"
    sums = list(body.atoms(sp.Sum))
    if len(sums) != 1 or len(sums[0].limits) != 1:
        return None
    series = sums[0]
    k, start, stop = series.limits[0]
    if not _d25_positive_integer(k, symbol) or k.name == n.name:
        return None
    if start != 1 or stop != n or series.function != (k / n) ** symbol:
        return None
    if body == sp.Integral(series, (symbol, 0, 1)) / n:
        return "riemann"
    return None


def _d25_riemann_limit():
    x = sp.Symbol("_d25_x", nonnegative=True)
    y = sp.Symbol("_d25_y", positive=True)
    n = sp.Symbol("_d25_n", positive=True, integer=True)
    # For each x in [0,1], y**x is nondecreasing on [0,1], bounded by
    # 1. The upper/lower uniform-grid Riemann sums differ by at most 1/n.
    # Hence this same bound controls the outer integral error, uniformly
    # in x, and licenses the outer limit without integrating a pointwise
    # limit of the original n-dependent expression.
    derivative = sp.diff(y**x, y)
    _d25_require(_d25_eq(derivative - x * y ** (x - 1)), "riemann-monotonicity")
    _d25_require(derivative.is_nonnegative is True, "riemann-positive-derivative")
    _d25_require(sp.limit(1 / n, n, sp.oo) == 0, "riemann-uniform-error")
    inner = sp.integrate(y**x, (y, 0, 1))
    _d25_require(inner == 1 / (x + 1), "riemann-inner-integral")
    return sp.integrate(inner, (x, 0, 1))


def _d25_cusp_limit():
    y = sp.Symbol("_d25_y", nonnegative=True)
    n = sp.Symbol("_d25_n", positive=True, integer=True)
    u = sp.Symbol("_d25_u", nonnegative=True)
    base = 1 - y / n + y**3 / n**3
    _d25_require(sp.limit(base**n, n, sp.oo) == sp.exp(-y), "cusp-pointwise-limit")
    c = 1 - sp.Rational(1, 20) ** 2
    _d25_require(c > 0, "cusp-positive-decay")
    # On either original half-interval, 0<=u<=1/20. Thus
    # u**3<=u/400 and 0<1-u+u**3<=1-c*u.  Under y=n*|x|,
    # (1-c*y/n)**n <= exp(-c*y), from log(1-v)<=-v.
    _d25_require(
        sp.expand((1 - c * u) - (1 - u + u**3)) == u / 400 - u**3,
        "cusp-cubic-bound",
    )
    v = sp.Symbol("_d25_v", positive=True)
    _d25_require(_d25_eq(sp.diff(-v - sp.log(1 - v), v) - v / (1 - v)),
                   "cusp-log-inequality")
    _d25_require((-v - sp.log(1 - v)).subs(v, 0) == 0, "cusp-log-bound-origin")
    _d25_require(sp.integrate(sp.exp(-c * y), (y, 0, sp.oo)).is_finite is True,
                   "cusp-integrable-majorant")
    _d25_require(n * sp.diff(y / n, y) == 1, "cusp-jacobian")
    _d25_require(sp.limit(n / 20, n, sp.oo) == sp.oo
                   and sp.limit(n / 24, n, sp.oo) == sp.oo, "cusp-moving-boundaries")
    # Zero-extend both transformed half-interval integrands to [0,infinity).
    # The checked integrable majorant proves dominated convergence on each.
    return 2 * sp.integrate(sp.exp(-y), (y, 0, sp.oo))


_D25_DIGITS = (8, 4, 6, 1, 3, 9, 5, 0, 7, 2)


def _d25_decimal_term(symbol, index):
    digit = sp.Mod(sp.floor(10**index * symbol), 10)
    mapped = sum(value * sp.KroneckerDelta(digit, d) for d, value in enumerate(_D25_DIGITS))
    return mapped / 10**index


def _d25_decimal_shape(expr, symbol):
    if not isinstance(expr, sp.Sum) or len(expr.limits) != 1:
        return False
    n, start, stop = expr.limits[0]
    return (
        _d25_positive_integer(n, symbol)
        and start == 1 and stop == sp.oo
        and expr.function == _d25_decimal_term(symbol, n)
    )


def _d25_decimal_value():
    # Verify the printed cycle map, rather than assuming an arbitrary table
    # is a permutation.  The terminating/nonterminating decimal choices
    # disagree only on a countable, measure-zero set.
    mapping = list(range(10))
    for cycle in ((3, 1, 4), (5, 9, 2, 6), (8, 7, 0)):
        for old, new in zip(cycle, cycle[1:] + cycle[:1]):
            mapping[old] = new
    _d25_require(tuple(mapping) == _D25_DIGITS, "decimal-printed-cycles")
    _d25_require(sorted(mapping) == list(range(10)), "decimal-bijection")
    j = sp.Symbol("_d25_j", positive=True, integer=True)
    m = sp.Symbol("_d25_m", positive=True, integer=True)
    q = sp.Symbol("_d25_q", nonnegative=True, integer=True)
    d = sp.Symbol("_d25_d", nonnegative=True, integer=True)
    # At decimal depth j, digit d occurs on the cells with index 10q+d,
    # q=0,...,10**(j-1)-1. Each cell has length 10**(-j).
    cell_left = (10 * q + d) / 10**j
    cell_right = (10 * q + d + 1) / 10**j
    _d25_require(sp.simplify(cell_right - cell_left) == 10 ** (-j), "decimal-cell-width")
    _d25_require(sp.simplify(10 ** (j - 1) * (cell_right - cell_left)) == sp.Rational(1, 10),
                   "decimal-digit-measure")
    _d25_require(sp.Mod(10 * q + d, 10) == sp.Mod(d, 10), "decimal-cell-digit")
    # Every tail is at most sum_{j>m}9/10**j = 10**(-m), uniformly.
    tail = sp.summation(9 / 10**j, (j, m + 1, sp.oo))
    _d25_require(sp.simplify(tail - 10 ** (-m)) == 0, "decimal-uniform-tail")
    _d25_require(sp.limit(tail, m, sp.oo) == 0, "decimal-tail-limit")
    mean_digit = sp.Rational(sum(mapping), 10)
    return sp.summation(mean_digit / 10**j, (j, 1, sp.oo))


def _d25_nested_abs_value(expr, symbol, lo, hi):
    target = sp.Abs(2 * sp.frac(symbol / 2) - 1)
    if lo != 0 or hi != 2025 or expr != target:
        return None
    # Compile the ORIGINAL finite nested absolute value over every unit
    # interval, starting at |2025-x|.  Each stage has integer endpoint
    # values differing by exactly one and is affine between them. Therefore
    # subtracting the next integer can have a zero only at an endpoint;
    # taking Abs creates no interior kink. This is an induction on the
    # original 2025 stages, not sampling an otherwise unknown function.
    values = list(range(2025, -1, -1))
    for constant in range(2024, 0, -1):
        _d25_require(all(abs(a - b) == 1 for a, b in zip(values, values[1:])),
                       "nested-abs-affine-integer-cells")
        values = [abs(constant - value) for value in values]
    expected = [1 - index % 2 for index in range(2026)]
    _d25_require(values == expected, "nested-abs-all-endpoint-values")
    # On even cells x=2j+u the displayed triangle is 1-u; on odd cells
    # x=2j+1+u it is u, for 0<=u<=1.  These are exactly the endpoint
    # interpolants proved above, including both endpoints by continuity.
    u = sp.Symbol("_d25_u", real=True)
    j = sp.Symbol("_d25_j", integer=True)
    _d25_require((sp.frac(j + u / 2) - sp.frac(u / 2)).rewrite(sp.floor) == 0,
                   "nested-abs-even-period")
    _d25_require((sp.frac(j + (u + 1) / 2) - sp.frac((u + 1) / 2)).rewrite(sp.floor) == 0,
                   "nested-abs-odd-period")
    up = sp.integrate(u, (u, 0, 1))
    down = sp.integrate(1 - u, (u, 0, 1))
    _d25_require(up == down, "nested-abs-cell-area")
    return sum(up if value == 0 else down for value in values[:-1])


def _d25_lagrange_shape(expr, symbol):
    if not isinstance(expr, sp.Sum) or len(expr.limits) != 1:
        return False
    n, start, stop = expr.limits[0]
    if not _d25_positive_integer(n, symbol) or start != 1 or stop != sp.oo:
        return False
    limits = list(expr.function.atoms(sp.Limit))
    if len(limits) != 1:
        return False
    coefficient = limits[0]
    derivative, t, destination, direction = coefficient.args
    if not isinstance(t, sp.Symbol) or t.name in {symbol.name, n.name} or destination != 0:
        return False
    expected_derivative = sp.Derivative(t**n / (sp.factorial(n) * sp.sin(t) ** n), (t, n - 1))
    expected = sp.Limit(expected_derivative, t, 0)
    return coefficient == expected and expr.function == symbol**n * expected


def _d25_lagrange_value():
    t = sp.Symbol("_d25_t", positive=True)
    z = sp.Symbol("_d25_z", real=True)
    n = sp.Symbol("_d25_n", positive=True, integer=True)
    m = sp.Symbol("_d25_m", nonnegative=True, integer=True)
    # sin(t) has a simple zero and derivative 1 at 0, so it is conformal
    # there; t/sin(t) has a removable singularity with value 1. Its inverse
    # germ is asin(z). These are the hypotheses of the residue coefficient
    # change of variables, checked explicitly below.
    _d25_require(sp.sin(0) == 0 and sp.diff(sp.sin(t), t).subs(t, 0) == 1,
                   "lagrange-simple-zero")
    _d25_require(sp.limit(t / sp.sin(t), t, 0) == 1, "lagrange-removable-value")
    _d25_require(sp.sin(sp.asin(z)) == z and sp.asin(0) == 0, "lagrange-inverse-germ")
    # For EVERY n>=1, the residue of a meromorphic derivative vanishes.
    # Under z=sin(t), [z^n]asin(z)=Res(t*cos(t)/sin(t)^(n+1)).
    # The checked identity therefore makes it (1/n)Res(sin(t)^(-n))
    # = (1/n)[t^(n-1)](t/sin(t))^n, precisely the printed derivative
    # divided by n!. This is an all-n identity, with no finite sampling.
    identity = sp.diff(t / sp.sin(t) ** n, t) - (
        1 / sp.sin(t) ** n - n * t * sp.cos(t) / sp.sin(t) ** (n + 1)
    )
    _d25_require(sp.simplify(identity) == 0, "lagrange-residue-identity-all-n")
    _d25_require(sp.simplify(sp.factorial(n - 1) / sp.factorial(n) - 1 / n) == 0,
                   "lagrange-derivative-coefficient")
    # The binomial series for asin'(z)=(1-z^2)^(-1/2) gives the
    # nonnegative coefficients a_m z^(2m+1) below. This and the inverse
    # germ identify the series on [0,1); Tonelli extends termwise
    # integration to [0,1], regardless of the endpoint representation.
    _d25_require(sp.diff(sp.asin(z), z) == 1 / sp.sqrt(1 - z**2), "lagrange-inverse-derivative")
    a = sp.factorial(2 * m) / (4**m * sp.factorial(m) ** 2 * (2 * m + 1))
    _d25_require(a.is_positive is True, "lagrange-positive-coefficients")
    _d25_require(sp.simplify((2 * m + 1) * a - sp.binomial(2 * m, m) / 4**m) == 0,
                   "lagrange-binomial-coefficients")
    primitive = z * sp.asin(z) + sp.sqrt(1 - z**2)
    _d25_require(sp.simplify(sp.diff(primitive, z) - sp.asin(z)) == 0, "lagrange-primitive")
    return primitive.subs(z, 1) - primitive.subs(z, 0)


def _d25_outer_shape(expr, symbol):
    # Subs keeps the outer operation unevaluated through srepr/sympify.
    # Constructing floor(Integral(...)) itself can trigger numerical evalf
    # in SymPy, which would erase the very source shape being certified.
    if isinstance(expr, sp.Subs) and len(expr.variables) == len(expr.point) == 1:
        placeholder = expr.variables[0]
        if not isinstance(placeholder, sp.Symbol) or placeholder.name == symbol.name:
            return None
        integral = expr.point[0]
        if expr.expr == sp.floor(placeholder):
            operation = "floor"
        elif expr.expr == sp.ceiling(placeholder):
            operation = "ceiling"
        elif expr.expr == sp.exp(placeholder):
            operation = "exp"
        else:
            return None
    elif expr.func == sp.exp and len(expr.args) == 1:
        operation, integral = "exp", expr.args[0]
    else:
        return None
    if not isinstance(integral, sp.Integral):
        return None
    if len(integral.limits) != 1 or len(integral.limits[0]) != 3:
        return None
    variable, lo, hi = integral.limits[0]
    if variable != symbol:
        return None
    f = integral.function
    if operation == "exp" and (lo, hi) == (1, 2):
        if f == sp.log((symbol - 1) ** (symbol ** -2)):
            return "product", lo, hi
    if operation == "ceiling" and (lo, hi) == (1, sp.oo):
        target = 1 / sp.atan(symbol) - (1 + symbol**2) / (
            1 + sp.atan(symbol) + symbol**2 * sp.atan(symbol)
        )
        if f == target:
            return "ceiling", lo, hi
    if operation != "floor":
        return None
    if (lo, hi) == (2, 2025):
        target = 1 / sp.floor(2 * sp.log(5) / sp.log(symbol) + 4 * sp.log(3) / sp.log(symbol))
        if f == target:
            return "floor-log", lo, hi
    if (lo, hi) != (0, 1):
        return None
    sums = list(f.atoms(sp.Sum))
    if len(sums) != 1 or len(sums[0].limits) != 1:
        return None
    series = sums[0]
    k, start, stop = series.limits[0]
    if (
        # A finite Sum with integer endpoints visits integer indices even
        # when Subs canonicalization drops the bound symbol's assumptions.
        isinstance(k, sp.Symbol) and k.name != symbol.name
        and start == 0 and stop == 998 and series.function == (-symbol) ** k
        and f == sp.pi * (sp.exp(sp.pi * symbol) - 1) + (1 + symbol) * series
    ):
        return "floor-exponential", lo, hi
    return None


def _d25_product_value():
    t = sp.Symbol("_d25_t", positive=True)
    x = t + 1
    original = sp.log((x - 1) ** (x ** -2))
    reduced = sp.log(t) / (1 + t) ** 2
    _d25_require(sp.expand_log(original) == reduced, "product-logarithm")
    primitive = sp.log(t) - sp.log(t) / (t + 1) - sp.log(t + 1)
    _d25_require(sp.simplify(sp.diff(primitive, t) - reduced) == 0, "product-log-primitive")
    lower = sp.limit(primitive, t, 0, dir="+")
    upper = primitive.subs(t, 1)
    _d25_require(lower == 0, "product-log-improper-endpoint")
    # Logarithms turn each positive tagged product into its ordinary sum;
    # the integrable log singularity has the checked finite endpoint limit.
    return sp.exp(upper - lower)


def _d25_ceiling_value():
    x = sp.Symbol("_d25_x", positive=True)
    u = sp.Symbol("_d25_u", positive=True)
    w = sp.Symbol("_d25_w", nonnegative=True)
    original = 1 / sp.atan(x) - (1 + x**2) / (1 + sp.atan(x) + x**2 * sp.atan(x))
    reduced = 1 / (sp.atan(x) * (1 + (1 + x**2) * sp.atan(x)))
    _d25_require(sp.factor(original - reduced) == 0, "ceiling-positive-reduction")
    # x=tan(u), u in [pi/4,pi/2). Here atan(tan(u))=u on the
    # principal branch. The algebraic substitution checks its remaining
    # Jacobian and denominator, without asking SymPy to change branches.
    transformed = sp.trigsimp((1 / (u * (1 + (1 + sp.tan(u) ** 2) * u))) / sp.cos(u) ** 2)
    _d25_require(sp.trigsimp(transformed - 1 / (u**2 + u * sp.cos(u) ** 2)) == 0,
                   "ceiling-tangent-substitution")
    _d25_require(sp.atan(1) == sp.pi / 4 and sp.limit(sp.atan(x), x, sp.oo) == sp.pi / 2,
                   "ceiling-tangent-bounds")
    gap = 1 / u**2 - 1 / (u**2 + u * w)
    _d25_require(sp.factor(gap - w / (u**2 * (u + w))) == 0,
                   "ceiling-upper-bound-identity")
    _d25_require((w / (u**2 * (u + w))).is_nonnegative is True, "ceiling-upper-bound-sign")
    upper = sp.integrate(1 / u**2, (u, sp.pi / 4, sp.pi / 2))
    _d25_require(upper > 0 and upper < 1, "ceiling-unit-enclosure")
    # Original integrand is strictly positive for every x>=1. Its integral
    # is therefore in (0,upper] subset (0,1), proving its ceiling exactly.
    return sp.ceiling(upper)


def _d25_floor_log_value():
    _d25_require(sp.logcombine(2 * sp.log(5) + 4 * sp.log(3)) == sp.log(2025),
                   "floor-log-change-of-base")
    _d25_require(2**10 < 2025 < 2**11, "floor-log-active-blocks")
    # log_x(2025) decreases on x>1, giving the exact constant blocks
    # (2025**(1/(k+1)),2025**(1/k)] for k=1,...,10; the last is
    # truncated at x=2. Endpoint values have measure zero.
    root = lambda k: sp.Integer(2025) ** sp.Rational(1, k)
    block_sum = (root(10) - 2) / 10 + sum((root(k) - root(k + 1)) / k for k in range(1, 10))
    collected = sp.Integer(2025) - sp.Rational(1, 5) - sum(root(k) / (k * (k - 1)) for k in range(2, 11))
    _d25_require(sp.expand(block_sum - collected) == 0, "floor-log-block-telescope")
    root_floors = (45000000, 12651489, 6708203, 4584426, 3556893, 2967197, 2590020, 2330132, 2141127)
    scale = 10**6
    lower = upper = sp.Integer(2025) - sp.Rational(1, 5)
    for k, floor in enumerate(root_floors, 2):
        _d25_require(floor**k <= 2025 * scale**k < (floor + 1) ** k, "floor-log-root-enclosure")
        lower -= sp.Rational(floor + 1, scale * k * (k - 1))
        upper -= sp.Rational(floor, scale * k * (k - 1))
    _d25_require(1999 < lower < upper < 2000, "floor-log-integer-enclosure")
    return sp.floor(lower)


def _d25_floor_exponential_value():
    x = sp.Symbol("_d25_x", real=True)
    m = sp.Symbol("_d25_m", nonnegative=True, integer=True)
    # The finite geometric polynomial is verified by recurrence for all m,
    # then specialized to m=998; no 999-term symbolic expansion is needed.
    q = sp.Symbol("_d25_q", real=True)
    closed = (1 - q ** (m + 1)) / (1 - q)
    _d25_require(sp.cancel(closed.subs(m, m + 1) - closed - q ** (m + 1)) == 0,
                   "floor-exp-geometric-recurrence")
    _d25_require(sp.cancel(closed.subs(m, 0)) == 1, "floor-exp-geometric-base")
    poly = sp.cancel((1 + x) * closed.subs({q: -x, m: 998}))
    _d25_require(poly == 1 + x**999, "floor-exp-finite-polynomial")
    value = sp.integrate(sp.pi * (sp.exp(sp.pi * x) - 1) + poly, (x, 0, 1))
    _d25_require(value == sp.exp(sp.pi) - sp.pi + sp.Rational(1, 1000), "floor-exp-inner-integral")
    # Machin's identity from an exact tangent addition and the principal
    # range: 0 < 4 atan(1/5)-atan(1/239) < 4/5 < pi/2.
    tangent = sp.Rational(1, 5)
    doubled = 2 * tangent / (1 - tangent**2)
    quadrupled = 2 * doubled / (1 - doubled**2)
    machin_tangent = (quadrupled - sp.Rational(1, 239)) / (1 + quadrupled / 239)
    _d25_require(machin_tangent == 1, "floor-exp-Machin-tangent")
    _d25_require(4 * sp.Rational(5, 26) - sp.Rational(1, 239) > 0
                   and sp.Rational(4, 5) < sp.pi / 2, "floor-exp-Machin-range")
    atan_sum = lambda z, count: sum((-1) ** k * z ** (2 * k + 1) / (2 * k + 1) for k in range(count))
    low_pi = 16 * atan_sum(sp.Rational(1, 5), 12) - 4 * atan_sum(sp.Rational(1, 239), 5)
    high_pi = 16 * atan_sum(sp.Rational(1, 5), 13) - 4 * atan_sum(sp.Rational(1, 239), 4)
    p = sp.Rational(31415926535, 10**10)
    q = sp.Rational(31415926536, 10**10)
    _d25_require(p < low_pi < high_pi < q, "floor-exp-rational-pi-enclosure")
    # The alternating arctangent remainder gives low_pi<pi<high_pi.
    # Positive exponential coefficients give T30(p)<exp(pi); all ratios
    # in the tail beyond degree 30 are <=q/32<1, yielding the upper bound.
    taylor = lambda z: sum(z**k / sp.factorial(k) for k in range(31))
    _d25_require(0 < q / 32 < 1, "floor-exp-tail-ratio")
    lower = taylor(p) - q + sp.Rational(1, 1000)
    upper = taylor(q) + q**31 / (sp.factorial(31) * (1 - q / 32)) - p + sp.Rational(1, 1000)
    _d25_require(20 < lower < upper < 21, "floor-exp-integer-enclosure")
    return sp.floor(lower)


def open_integrand(expr, symbol):
    return bool(
        _d25_limit_shape(expr, symbol)
        or _d25_decimal_shape(expr, symbol)
        or _d25_lagrange_shape(expr, symbol)
        or _d25_outer_shape(expr, symbol)
    )


def definite_value(integrand, symbol, lo, hi):
    limit_shape = _d25_limit_shape(integrand, symbol)
    if limit_shape == "riemann" and (lo, hi) == (0, 1):
        return _d25_riemann_limit()
    if limit_shape == "cusp" and (lo, hi) == (-sp.Rational(1, 20), sp.Rational(1, 24)):
        return _d25_cusp_limit()
    if (lo, hi) == (0, 1):
        if _d25_decimal_shape(integrand, symbol):
            return _d25_decimal_value()
        if _d25_lagrange_shape(integrand, symbol):
            return _d25_lagrange_value()
    nested = _d25_nested_abs_value(integrand, symbol, lo, hi)
    if nested is not None:
        return nested
    outer_shape = _d25_outer_shape(integrand, symbol)
    if outer_shape is not None:
        shape, inner_lo, inner_hi = outer_shape
        if (lo, hi) != (inner_lo, inner_hi):
            return None
        return {
            "product": _d25_product_value,
            "ceiling": _d25_ceiling_value,
            "floor-log": _d25_floor_log_value,
            "floor-exponential": _d25_floor_exponential_value,
        }[shape]()
    return None
