"""Exact certificates for the Handoff B pack rows.

Each builder matches an expression and its bounds before deriving a value.
Five outer limits retain the entire Limit(Integral(...), n, oo) expression;
the bounds stored beside them must match the inner integral. They are never
interpreted as an integral of a pointwise limit. The decimal indicator and
nested radical retain infinite products, and one antiderivative retains a
finite sum. All other inputs keep the ordinary closed-expression contract.
"""

from __future__ import annotations

import sympy as sp


def _eq(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def _b_chain_minimum(expr, symbol, lo, hi):
    if lo != 0 or hi != 2025 or not expr.has(sp.Min):
        return None
    fractional = sp.frac(symbol)
    circle = sp.sqrt(fractional - fractional**2)
    spike = sp.Abs(sp.sqrt(3) * sp.asin(sp.cos(sp.pi * symbol)) / sp.pi)
    if expr != sp.Min(circle, spike):
        return None
    u = sp.Symbol("_b_chain_u", real=True)
    theta = sp.Symbol("_b_chain_theta", real=True)
    z = sp.Symbol("_b_chain_z", real=True)
    _require(
        sp.frac(symbol + 1).rewrite(sp.floor) == fractional.rewrite(sp.floor), "fractional-period"
    )
    _require(
        sp.trigsimp(sp.cos(sp.pi * (symbol + 1)) + sp.cos(sp.pi * symbol)) == 0,
        "cosine-antiperiod",
    )
    _require(sp.Abs(sp.asin(-z)) == sp.Abs(sp.asin(z)), "spike-period")
    phase = sp.pi / 2 - sp.pi * u
    _require(sp.sin(phase) == sp.cos(sp.pi * u), "principal-arcsine")
    _require(phase.subs(u, 0) == sp.pi / 2 and phase.subs(u, 1) == -sp.pi / 2, "arcsine-range")
    circle_squared = u - u**2
    line = sp.sqrt(3) * (sp.Rational(1, 2) - u)
    gap = sp.factor(circle_squared - line**2)
    _require(_eq(gap + (4 * u - 3) * (4 * u - 1) / 4), "minimum-crossings")
    _require(_eq(circle_squared.subs(u, 1 - u) - circle_squared), "semicircle-reflection")
    _require(sp.Abs(line.subs(u, 1 - u)) == sp.Abs(line), "spike-reflection")
    # On [0,1/4] the squared gap is nonpositive; on [1/4,1/2] it is
    # nonnegative. Both heights are nonnegative, so the minimum switches once.
    mapping = (1 - sp.cos(theta)) / 2
    _require(
        _eq(circle_squared.subs(u, mapping) - sp.sin(theta) ** 2 / 4), "semicircle-substitution"
    )
    _require(
        mapping.subs(theta, 0) == 0 and mapping.subs(theta, sp.pi / 3) == sp.Rational(1, 4),
        "semicircle-endpoints",
    )
    sector_piece = sp.integrate(sp.sin(theta) / 2 * sp.diff(mapping, theta), (theta, 0, sp.pi / 3))
    line_piece = sp.integrate(line, (u, sp.Rational(1, 4), sp.Rational(1, 2)))
    return sp.simplify(2025 * 2 * (sector_piece + line_piece))


def _b_chain_log_power(expr, symbol, lo, hi):
    if lo != 0 or not expr.has(sp.log):
        return None
    tangent = sp.cos(2 * symbol) / (-sp.log(sp.tan(symbol)) * sp.cos(symbol) ** 4)
    sine = sp.cos(symbol) ** 3 * sp.sin(symbol) / sp.log(sp.sin(symbol))
    if hi == sp.pi / 4 and expr == tangent:
        mapping = sp.atan
        lower, upper, factor = sp.Integer(0), sp.Integer(2), sp.Integer(1)
    elif hi == sp.pi / 2 and expr == sine:
        mapping = sp.asin
        lower, upper, factor = sp.Integer(1), sp.Integer(3), sp.Integer(-1)
    else:
        return None
    t = sp.Symbol("_b_chain_t", positive=True)
    parameter = sp.Symbol("_b_chain_parameter", nonnegative=True)
    _require(mapping(0) == lo and mapping(1) == hi, "log-power-endpoints")
    moved = expr.subs(symbol, mapping(t)) * sp.diff(mapping(t), t)
    reduced = factor * (t**upper - t**lower) / sp.log(t)
    _require(_eq(moved - reduced), "log-power-substitution")
    primitive = t**parameter / sp.log(t)
    _require(sp.diff(primitive, parameter) == t**parameter, "power-parameter-derivative")
    _require(
        _eq(
            factor * (primitive.subs(parameter, upper) - primitive.subs(parameter, lower)) - reduced
        ),
        "power-parameter-endpoints",
    )
    # On 0<t<1 the power kernel is nonnegative, so Tonelli applies before
    # the overall sign is restored. Its t integral is 1/(parameter+1).
    inner = sp.integrate(t**parameter, (t, 0, 1))
    _require(inner == 1 / (parameter + 1), "power-unit-integral")
    return factor * sp.integrate(inner, (parameter, lower, upper))


def _b_chain_golden_arctangent(expr, symbol, lo, hi):
    if lo != 0 or hi != sp.oo or not expr.has(sp.atan):
        return None
    phi = (1 + sp.sqrt(5)) / 2
    expected = symbol**phi * sp.atan(symbol) / (1 + symbol ** (2 * phi**2))
    if expr != expected:
        return None
    u = sp.Symbol("_b_chain_u", positive=True)
    exponent = sp.simplify(phi**2)
    _require(_eq(exponent - phi - 1), "golden-exponent")
    weight = u**phi / (1 + u ** (2 * phi**2))
    reflected = weight.subs(u, 1 / u) / u**2
    _require(_eq(reflected - weight), "golden-reciprocal-weight")
    complement = sp.atan(u) + sp.atan(1 / u)
    _require(
        _eq(sp.diff(complement, u)) and complement.subs(u, 1) == sp.pi / 2, "arctangent-complement"
    )
    primitive = sp.atan(u**exponent) / exponent
    _require(_eq(sp.diff(primitive, u) - weight), "golden-primitive")
    start = sp.limit(primitive, u, 0, dir="+")
    stop = sp.limit(primitive, u, sp.oo)
    _require(start == 0 and stop == sp.pi / (2 * exponent), "golden-endpoints")
    return sp.pi * (stop - start) / 4


def _b_chain_dirichlet(expr, symbol, lo, hi):
    if lo != 0 or hi != sp.pi / 2:
        return None
    expected = sp.sec(symbol) * sp.csc(symbol) * sp.sin(sp.tan(symbol))
    if expr != expected:
        return None
    t = sp.Symbol("_b_chain_t", positive=True)
    mapping = sp.atan(t)
    reduced = expr.subs(symbol, mapping) * sp.diff(mapping, t)
    _require(_eq(reduced - sp.sin(t) / t), "dirichlet-substitution")
    _require(
        sp.limit(mapping, t, 0, dir="+") == 0 and sp.limit(mapping, t, sp.oo) == sp.pi / 2,
        "dirichlet-endpoints",
    )
    return sp.integrate(sp.sin(t) / t, (t, 0, sp.oo))


def _b_chain_log_cosine(expr, symbol, lo, hi):
    if lo != 0 or hi != sp.oo or expr != sp.log(1 + sp.exp(-symbol)) * sp.cos(symbol):
        return None
    n = sp.Symbol("_b_chain_n", integer=True, positive=True)
    u = sp.Symbol("_b_chain_u", positive=True)
    q = sp.Symbol("_b_chain_q", positive=True)
    _require(sp.diff(sp.log(1 + q), q) == 1 / (1 + q), "log-series-derivative")
    _require(sp.log(1 + q).subs(q, 0) == 0, "log-series-constant")
    geometric = (1 - (-q) ** n) / (1 + q)
    _require(_eq(geometric.subs(n, n + 1) - geometric - (-q) ** n), "log-geometric-recurrence")
    _require(geometric.subs(n, 1) == 1, "log-geometric-base")
    _require(sp.limit(sp.exp(-n * u), n, sp.oo) == 0, "log-geometric-remainder")
    # Integrating the geometric identity from 0 to q=e^-u gives the log
    # series. The sum of absolute L1 bounds is zeta(2), which licenses Fubini.
    absolute_term = sp.integrate(sp.exp(-n * u) / n, (u, 0, sp.oo))
    _require(absolute_term == 1 / n**2, "log-series-L1-term")
    bound = sp.summation(absolute_term, (n, 1, sp.oo))
    _require(bound.is_finite is True, "log-series-L1-sum")
    term = sp.integrate(sp.exp(-n * u) * sp.cos(u), (u, 0, sp.oo))
    _require(_eq(term - n / (n**2 + 1)), "damped-cosine-transform")
    return sp.summation((-1) ** (n - 1) * term / n, (n, 1, sp.oo))


def _b_chain_hyperbolic(expr, symbol, lo, hi):
    if lo != 0 or hi != sp.oo or expr != symbol * sp.cosh(symbol) / sp.sinh(sp.pi * symbol):
        return None
    u = sp.Symbol("_b_chain_u", positive=True)
    rate = sp.Symbol("_b_chain_rate", positive=True)
    n = sp.Symbol("_b_chain_n", integer=True, nonnegative=True)
    z = sp.Symbol("_b_chain_z", positive=True)
    alpha = (sp.pi - 1) / (2 * sp.pi)
    _require(
        alpha.is_positive is True and (1 - alpha).is_positive is True, "hyperbolic-positive-rates"
    )
    kernel = (
        u * (sp.exp(-(sp.pi - 1) * u) + sp.exp(-(sp.pi + 1) * u)) / (1 - sp.exp(-2 * sp.pi * u))
    )
    _require(_eq(expr.subs(symbol, u).rewrite(sp.exp) - kernel), "hyperbolic-geometric-kernel")
    _require(sp.limit(sp.exp(-2 * sp.pi * u * n), n, sp.oo) == 0, "hyperbolic-geometric-remainder")
    # The geometric terms are positive. Tonelli reduces the integral to the
    # two reciprocal-square series with shifts alpha and 1-alpha.
    term = sp.integrate(u * sp.exp(-rate * u), (u, 0, sp.oo))
    _require(term == 1 / rate**2, "hyperbolic-laplace-term")
    paired = 1 / ((2 * n + 1) * sp.pi - 1) ** 2 + 1 / ((2 * n + 1) * sp.pi + 1) ** 2
    scaled = (1 / (n + alpha) ** 2 + 1 / (n + 1 - alpha) ** 2) / (4 * sp.pi**2)
    _require(_eq(paired - scaled), "hyperbolic-series-scale")
    series = sp.expand_func(sp.summation(1 / (n + z) ** 2, (n, 0, sp.oo)))
    _require(series == sp.polygamma(1, z).rewrite(sp.zeta), "trigamma-series")
    _require(_eq(sp.gamma(z) * sp.gamma(1 - z) - sp.pi / sp.sin(sp.pi * z)), "gamma-reflection")
    # Twice differentiating the logarithm of the checked reflection identity
    # gives psi_1(z)+psi_1(1-z)=d²[-log(sin(pi*z))]/dz² for 0<z<1.
    logarithmic_left = sp.loggamma(z) + sp.loggamma(1 - z)
    _require(
        sp.diff(logarithmic_left, z, 2) == sp.polygamma(1, z) + sp.polygamma(1, 1 - z),
        "reflection-second-derivative",
    )
    reflected = sp.diff(-sp.log(sp.sin(sp.pi * z)), z, 2)
    return sp.trigsimp(reflected.subs(z, alpha) / (4 * sp.pi**2))


def _b_chain_real_cube_root(expr, symbol, lo, hi):
    if lo != 0 or hi != 1:
        return None
    expected = sp.sqrt(1 + sp.real_root(symbol - 1, 3))
    if expr != expected:
        return None
    u = sp.Symbol("_b_chain_u", positive=True)
    mapping = 1 - u**3
    _require(sp.real_root(-(u**3), 3) == -u, "real-cube-root-branch")
    reduced = -expr.subs(symbol, mapping) * sp.diff(mapping, u)
    _require(_eq(reduced - 3 * u**2 * sp.sqrt(1 - u)), "real-cube-root-substitution")
    _require(mapping.subs(u, 0) == 1 and mapping.subs(u, 1) == 0, "real-cube-root-endpoints")
    return sp.integrate(3 * u**2 * sp.sqrt(1 - u), (u, 0, 1))


def _b_chain_gamma(expr, symbol, lo, hi):
    if lo != 0 or hi != sp.oo or expr != sp.exp(-(symbol ** sp.Rational(1, 2025))):
        return None
    u = sp.Symbol("_b_chain_u", positive=True)
    mapping = u**2025
    _require(mapping ** sp.Rational(1, 2025) == u, "gamma-power-substitution")
    _require(
        mapping.subs(u, 0) == 0 and sp.limit(mapping, u, sp.oo) == sp.oo, "gamma-power-endpoints"
    )
    moved = expr.subs(symbol, mapping) * sp.diff(mapping, u)
    _require(moved == 2025 * u**2024 * sp.exp(-u), "gamma-jacobian")
    return sp.integrate(moved, (u, 0, sp.oo))


def _b_chain_polynomial_shape(expr, symbol):
    sums = list(expr.atoms(sp.Sum))
    if len(sums) != 2 or expr != sp.Mul(*sums):
        return None
    weighted = plain = None
    for series in sums:
        if len(series.limits) != 1 or len(series.limits[0]) != 3:
            return None
        index, start, stop = series.limits[0]
        if not isinstance(index, sp.Symbol) or index.name == symbol.name:
            return None
        if start == 1 and stop == 2025 and series.function == index * symbol**index:
            weighted = series
        elif start == 0 and stop == 2024 and series.function == symbol**index:
            plain = series
        else:
            return None
    return (weighted, plain) if weighted is not None and plain is not None else None


def indefinite_ok(answer, expr, symbol):
    if expr.has(sp.Sum):
        shape = _b_chain_polynomial_shape(expr, symbol)
        if shape is None:
            return None
        weighted, plain = shape
        index = weighted.limits[0][0]
        total = sp.Sum(symbol**index, (index, 1, 2025))
        constant, candidate = answer.as_independent(symbol, as_Add=True)
        if (
            constant.has(sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.nan, sp.zoo, sp.oo, -sp.oo)
            or constant.is_finite is False
        ):
            return False
        if candidate != total**2 / 2:
            return False
        derivative = sp.diff(total, symbol)
        _require(
            isinstance(derivative, sp.Sum) and derivative.limits == total.limits,
            "finite-polynomial-derivative-bounds",
        )
        _require(
            _eq(symbol * derivative.function - weighted.function),
            "finite-polynomial-derivative-terms",
        )
        j, start, stop = plain.limits[0]
        _require(start + 1 == 1 and stop + 1 == 2025, "finite-polynomial-reindex-bounds")
        _require(
            _eq(symbol * plain.function.subs(j, index - 1) - total.function),
            "finite-polynomial-reindex-terms",
        )
        _require(sp.diff(candidate, symbol) == total * derivative, "finite-polynomial-chain-rule")
        # The checked reindexing gives total=x*plain and weighted=x*total'.
        # Their product is total*total'; the polynomial identity includes x=0.
        return True
    expected = (sp.cos(symbol) + 1 - symbol**2) / (
        (symbol * sp.sin(symbol) + 1) * sp.sqrt(1 - symbol**2)
    )
    if expr != expected:
        return None
    y = (symbol + sp.sin(symbol)) / (symbol * sp.sin(symbol) + 1)
    constant, candidate = answer.as_independent(symbol, as_Add=True)
    if (
        constant.has(sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.nan, sp.zoo, sp.oo, -sp.oo)
        or constant.is_finite is False
    ):
        return False
    if candidate.has(sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.nan, sp.zoo, sp.oo, -sp.oo):
        return False
    if candidate.func != sp.asin or not _eq(candidate.args[0] - y):
        return False
    denominator = 1 + symbol * sp.sin(symbol)
    _require(
        _eq(
            sp.diff(y, symbol) - (sp.cos(symbol) + 1 - symbol**2) * sp.cos(symbol) / denominator**2
        ),
        "arcsine-ratio-derivative",
    )
    _require(
        _eq(denominator**2 * (1 - y**2) - sp.cos(symbol) ** 2 * (1 - symbol**2)), "arcsine-radicand"
    )
    _require(sp.pi / 2 > 1, "arcsine-real-domain")
    # The real integrand has -1<x<1. Hence cos(x)>0 and
    # 1+x*sin(x)>0 (|x*sin(x)|<1), fixing the square-root sign throughout.
    branch_derivative = sp.diff(y, symbol) * denominator / (sp.cos(symbol) * sp.sqrt(1 - symbol**2))
    return _eq(branch_derivative - expr)


def _b_limit_tower(x):
    return x ** (x**x) * sp.log(1 + x + x**x + x ** (x**x) + x ** (x ** (x**x)))


def _b_limit_full_form(expr, symbol):
    if not isinstance(expr, sp.Limit) or expr.args[2:] != (sp.oo, sp.Symbol("-")):
        return None
    body, n = expr.args[:2]
    if not isinstance(n, sp.Symbol) or n.is_integer is not True or n.is_positive is not True:
        return None
    inners = list(body.atoms(sp.Integral))
    if len(inners) != 1:
        return None
    inner = inners[0]
    if len(inner.limits) != 1 or len(inner.limits[0]) != 3:
        return None
    x, lo, hi = inner.limits[0]
    if x != symbol or n.name == x.name:
        return None
    if (lo, hi) == (0, 1):
        tower = x ** (x**x + n) * sp.log(1 + x + x**x + x ** (x**x) + x ** (x ** (x**x)))
        if body == (n + 1) * inner and inner.function == tower:
            return "tower", n, inner
        phase = sp.frac(n * x**2025)
        if body == inner and inner.function == 2025 * sp.sin(phase) * sp.cos(phase):
            return "fractional", n, inner
    if (lo, hi) == (0, sp.Rational(1, 2)):
        if body == inner and inner.function == (1 - (1 - 2 * x) ** (2**n)) / 2:
            return "iterate", n, inner
    if (lo, hi) == (1, n) and body == inner:
        if inner.function == sp.log(1 + sp.E / n + (n * x) ** (-1 / sp.E)):
            return "divergent-log", n, inner
        if inner.function == sp.log(1 + 2 / n + 1 / sp.sqrt(n * x)):
            return "finite-log", n, inner
    return None


def limits_full_limit_shape(expr, symbol):
    """Recognize a whole printed limit, never a pointwise limit of an integrand."""
    return _b_limit_full_form(expr, symbol) is not None


def _b_limit_decimal_form(expr, symbol):
    if not isinstance(expr, sp.Product) or len(expr.limits) != 1 or len(expr.limits[0]) != 3:
        return None
    k, lo, hi = expr.limits[0]
    if not isinstance(k, sp.Symbol) or k.name == symbol.name or k.is_integer is not True:
        return None
    expected = 1 - sp.KroneckerDelta(sp.Mod(sp.floor(10**k * symbol), 10), 9)
    return k if (lo, hi) == (1, sp.oo) and expr.function == expected else None


def _b_limit_nested_form(expr, symbol):
    if not isinstance(expr, sp.Product) or len(expr.limits) != 1 or len(expr.limits[0]) != 3:
        return None
    k, lo, hi = expr.limits[0]
    if not isinstance(k, sp.Symbol) or k.name == symbol.name or k.is_integer is not True:
        return None
    expected = symbol ** (2 ** (1 - k)) * 2 ** (-k * symbol / 4**k)
    return k if (lo, hi) == (1, sp.oo) and expr.function == expected else None


def limits_open_integrand(expr, symbol):
    return (
        limits_full_limit_shape(expr, symbol)
        or _b_limit_decimal_form(expr, symbol) is not None
        or _b_limit_nested_form(expr, symbol) is not None
    )


def _b_limit_tower_value(n, inner):
    x = sp.Symbol("_b_tower_x", positive=True)
    original = inner.function.subs(inner.limits[0][0], x)
    amplitude = _b_limit_tower(x)
    _require(_eq(original / x**n - amplitude), "tower-factorization")
    normalizer = (n + 1) * sp.integrate(x**n, (x, 0, 1))
    _require(normalizer == 1, "tower-unit-mass")
    d = sp.Symbol("_b_tower_d", positive=True)
    cutoff = 1 / (1 + d)
    tail = (n + 1) * sp.integrate(x**n, (x, 0, cutoff))
    _require(_eq(tail - cutoff ** (n + 1)), "tower-tail-mass")
    _require(sp.limit(tail, n, sp.oo) == 0, "tower-tail-vanishes")
    u, v = sp.symbols("_b_tower_u _b_tower_v", positive=True)
    power = sp.exp(-u * v)
    _require(
        power.is_positive is True and (-sp.diff(power, u)).is_positive is True,
        "tower-positive-decreasing-powers",
    )
    _require(power.subs(u, 0) == 1, "tower-power-upper-endpoint")
    # For x=exp(-u) every finite tower lies in (0,1]. Consequently the
    # amplitude lies in [0,log(5)] and is continuous at 1. The unit-mass
    # kernels put vanishing mass on [0,cutoff], giving the endpoint value.
    endpoint = sp.limit(amplitude, x, 1, dir="-")
    _require(endpoint == amplitude.subs(x, 1), "tower-continuous-endpoint")
    return endpoint


def _b_limit_fractional_value(n, inner):
    x, t, u = sp.symbols("_b_frac_x _b_frac_t _b_frac_u", positive=True)
    k = sp.Integer(2025)
    alpha = 1 / k
    original = inner.function.subs(inner.limits[0][0], x)
    _require(
        original == k * sp.sin(sp.frac(n * x**k)) * sp.cos(sp.frac(n * x**k)), "fractional-reading"
    )
    weight = alpha * t ** (alpha - 1)
    _require(_eq(sp.diff(t**alpha, t) - weight), "fractional-jacobian")
    _require(sp.powdenest((t**alpha) ** k) == t, "fractional-phase")
    _require(sp.integrate(weight, (t, 0, 1)) == 1, "fractional-weight-mass")
    cell = k * sp.sin(u) * sp.cos(u)
    mean = sp.integrate(cell, (u, 0, 1))
    primitive = k * sp.sin(u) ** 2 / 2 - mean * u
    _require(_eq(sp.diff(primitive, u) - cell + mean), "fractional-cell-primitive")
    _require(primitive.subs(u, 0) == 0 and primitive.subs(u, 1) == 0, "fractional-cell-endpoints")
    _require(_eq(sp.sin(u) ** 2 + sp.cos(u) ** 2 - 1), "fractional-bounded-cells")
    _require(
        weight.is_positive is True and (-sp.diff(weight, t)).is_positive is True,
        "fractional-decreasing-weight",
    )
    delta = sp.Symbol("_b_frac_delta", positive=True)
    head_mass = sp.integrate(weight, (t, 0, delta))
    _require(_eq(head_mass - delta**alpha), "fractional-head-mass")
    variation = sp.integrate(-sp.diff(weight, t), (t, delta, 1))
    _require(
        _eq(variation - weight.subs(t, delta) + weight.subs(t, 1)), "fractional-tail-variation"
    )
    # The periodic primitive H of cell-mean vanishes at integer endpoints
    # and |H| <= k. Integration by parts on [delta,1] bounds the error by
    # 2*k*w(delta)/n. The omitted head has error at most 2*k*delta**alpha.
    # With delta=1/n both bounds decay as n**(-1/k), despite the singular weight.
    error = (2 * k * head_mass + 2 * k * weight.subs(t, delta) / n).subs(delta, 1 / n)
    _require(_eq(error - 2 * (k + 1) / n**alpha), "fractional-error-bound")
    _require(sp.limit(error, n, sp.oo) == 0, "fractional-error-vanishes")
    return mean


def _b_limit_iterate_value(n, inner):
    x = inner.limits[0][0]
    first = 2 * x - 2 * x**2
    term = inner.function
    _require(_eq(term.subs(n, 1) - first), "iterate-base")
    _require(sp.expand(1 - 2 * first - (1 - 2 * x) ** 2) == 0, "iterate-conjugacy")
    z, m = sp.symbols("_b_iterate_z _b_iterate_m", positive=True)
    f = (1 - z**m) / 2
    _require(sp.expand(2 * f - 2 * f**2 - (1 - z ** (2 * m)) / 2) == 0, "iterate-step")
    _require(sp.simplify(2 ** (n + 1) - 2 * 2**n) == 0, "iterate-exponent-step")
    _require(sp.diff((1 - z) / 2, z) == -sp.Rational(1, 2), "iterate-jacobian")
    value = sp.integrate((1 - z**m) / 4, (z, 0, 1))
    _require(_eq(value - (sp.Rational(1, 4) - 1 / (4 * (m + 1)))), "iterate-finite-integral")
    return sp.limit(value.subs(m, 2**n), n, sp.oo)


def _b_limit_log_value(tag, n, inner):
    x = sp.Symbol("_b_log_x", positive=True)
    t = sp.Symbol("_b_log_t", nonnegative=True)
    upper_gap = t - sp.log(1 + t)
    lower_gap = sp.log(1 + t) - t + t**2 / 2
    _require(_eq(sp.diff(upper_gap, t) - t / (1 + t)), "log-upper-bound")
    _require(_eq(sp.diff(lower_gap, t) - t**2 / (1 + t)), "log-lower-bound")
    _require(upper_gap.subs(t, 0) == lower_gap.subs(t, 0) == 0, "log-bounds-anchor")
    if tag == "finite-log":
        perturbation = 2 / n + 1 / sp.sqrt(n * x)
        _require(
            inner.function.subs(inner.limits[0][0], x) == sp.log(1 + perturbation),
            "log-finite-reading",
        )
        main = sp.integrate(perturbation, (x, 1, n))
        error = sp.integrate(sp.expand(perturbation**2 / 2), (x, 1, n))
        _require(sp.limit(error, n, sp.oo) == 0, "log-quadratic-error")
        return sp.limit(main, n, sp.oo)
    # The integrand decreases in x, so (n-1) times its value at x=n bounds
    # the integral from below. log(1+t)>=t/(1+t) then proves divergence
    # without subtracting two infinite terms from an antiderivative.
    power = (n * x) ** (-1 / sp.E)
    _require((-sp.diff(power, x)).is_positive is True, "log-divergent-monotone")
    rational_gap = sp.log(1 + t) - t / (1 + t)
    _require(_eq(sp.diff(rational_gap, t) - t / (1 + t) ** 2), "log-rational-lower-bound")
    _require(rational_gap.subs(t, 0) == 0, "log-rational-anchor")
    _require((1 - 2 / sp.E).is_positive is True, "log-divergence-power")
    lower = (n - 1) * power.subs(x, n) / (1 + power.subs(x, n))
    return sp.limit(lower, n, sp.oo)


def _b_limit_decimal_value():
    digit = sp.Symbol("_b_digit", integer=True)
    indicator = 1 - sp.KroneckerDelta(digit, 9)
    children = sum(indicator.subs(digit, value) for value in range(10))
    _require(children == 9, "decimal-nine-children")
    n = sp.Symbol("_b_digits", integer=True, positive=True)
    width = sp.Integer(10) ** (-n)
    count = children**n
    _require(sp.simplify(width.subs(n, n + 1) / width) == sp.Rational(1, 10), "decimal-cell-width")
    _require(sp.simplify(count.subs(n, n + 1) / count) == children, "decimal-cell-count")
    # Each prefix has ten disjoint decimal subintervals, nine of which survive.
    # The indicator is nonnegative and supported on the 9**n surviving cells
    # of length 10**(-n), for every n. Decimal endpoint choices are countable.
    return sp.limit(count * width, n, sp.oo)


def _b_limit_nested_value(k):
    x = sp.Symbol("_b_nested_x", positive=True)
    _require(sp.simplify(2**k / 2 ** (2 * k - 1) - 2 ** (1 - k)) == 0, "nested-odd-depth")
    _require(sp.simplify(k / 2 ** (2 * k) - k / 4**k) == 0, "nested-even-depth")
    power = sp.summation(2 ** (1 - k), (k, 1, sp.oo))
    decay = sp.summation(k / 4**k, (k, 1, sp.oo))
    _require(power.is_finite is True and decay.is_positive is True, "nested-convergent-exponents")
    n = sp.Symbol("_b_depth", integer=True, positive=True)
    _require(sp.limit(2 ** (-n), n, sp.oo) == 0, "nested-odd-truncation-remainder")
    # Taking logarithms of each positive finite truncation gives exactly the
    # two sums above. Both even and odd truncations have the same limit.
    return sp.integrate(x**power * sp.exp(-decay * x * sp.log(2)), (x, 0, sp.oo))


def _b_limit_radical_pair(x):
    a = x**2 / 2 - x**3 / 27 + sp.sqrt(x**4 / 4 - x**5 / 27)
    u = a ** sp.Rational(1, 3)
    first = u + x**2 / (9 * u) - x / 3
    second = (x**2 + sp.sqrt(x**4 + 4 * x**3)) / 2
    return first, second


def _b_limit_radical_value(expr, symbol, lo, hi):
    if (lo, hi) != (0, sp.Rational(1, 2)):
        return None
    first, second = _b_limit_radical_pair(symbol)
    if expr != first + second:
        return None
    x, z = sp.symbols("_b_radical_x _b_radical_z", positive=True)
    f_map = x / sp.sqrt(x + z)
    g_map = sp.sqrt(x**3 + x**2 * z)
    for mapping, sign in ((f_map, -1), (g_map, 1)):
        elasticity = sp.simplify(z * sp.diff(mapping, z) / mapping)
        _require(_eq(elasticity - sign * z / (2 * (x + z))), "radical-log-contraction")
    _require((x / (2 * (x + z))).is_positive is True, "radical-contraction-gap")
    # In log coordinates both positive iteration maps have Lipschitz constant
    # at most 1/2. Thus their finite nested truncations converge to the unique
    # positive fixed points used in the transcription.
    a = x**2 / 2 - x**3 / 27 + sp.sqrt(x**4 / 4 - x**5 / 27)
    _require(_eq(a**2 + (2 * x**3 / 27 - x**2) * a + x**6 / 729), "radical-cardano-discriminant")
    u = sp.Symbol("_b_radical_u", positive=True)
    candidate = u + x**2 / (9 * u) - x / 3
    cubic = candidate**3 + x * candidate**2 - x**2
    _require(
        _eq(cubic - (u**3 - x**2 + 2 * x**3 / 27 + x**6 / (729 * u**3))), "radical-cardano-cubic"
    )
    s = sp.Symbol("_b_radical_s", positive=True)
    interval_x = s / (2 * (1 + s))
    _require(
        sp.factor((x**4 / 4 - x**5 / 27).subs(x, interval_x)).is_positive is True,
        "radical-real-discriminant",
    )
    _require(
        sp.factor((x**2 / 2 - 2 * x**3 / 27).subs(x, interval_x)).is_positive is True,
        "radical-positive-cubic-root",
    )
    _require(
        (x**4 / 4 - x**5 / 27).subs(x, hi).is_positive is True, "radical-endpoint-discriminant"
    )
    _require(
        (x**2 / 2 - 2 * x**3 / 27).subs(x, hi).is_positive is True, "radical-endpoint-positive-root"
    )
    _, second_pos = _b_limit_radical_pair(x)
    _require(_eq(second_pos**2 - x**2 * second_pos - x**3), "radical-positive-quadratic-root")
    _require(sp.diff(second_pos, x).is_positive is True, "radical-increasing-inverse")
    _require(sp.limit(second_pos, x, 0, dir="+") == 0, "radical-left-endpoint")
    _require(second_pos.subs(x, hi) == hi, "radical-right-endpoint")
    f_equation = z**3 + x * z**2 - x**2
    g_equation = z**2 - x**2 * z - x**3
    _require(
        sp.expand(f_equation + g_equation.xreplace({x: z, z: x})) == 0, "radical-inverse-equations"
    )
    _require(sp.diff(f_equation, z).is_positive is True, "radical-positive-root-unique")
    # These increasing continuous positive roots are inverses. Substitution
    # followed by integration by parts gives int(f)+int(g)=[x*g(x)]_0^hi.
    return hi * second_pos.subs(x, hi)


def _limits_value(expr, symbol, lo, hi):
    whole = _b_limit_full_form(expr, symbol)
    if whole is not None:
        tag, n, inner = whole
        if inner.limits[0][1:] != (lo, hi):
            return None
        if tag == "tower":
            return _b_limit_tower_value(n, inner)
        if tag == "fractional":
            return _b_limit_fractional_value(n, inner)
        if tag == "iterate":
            return _b_limit_iterate_value(n, inner)
        return _b_limit_log_value(tag, n, inner)
    digit_index = _b_limit_decimal_form(expr, symbol)
    if digit_index is not None and (lo, hi) == (0, 1):
        return _b_limit_decimal_value()
    nested_index = _b_limit_nested_form(expr, symbol)
    if nested_index is not None and (lo, hi) == (0, sp.oo):
        return _b_limit_nested_value(nested_index)
    return _b_limit_radical_value(expr, symbol, lo, hi)


def _b_dich_frullani(integrand, symbol, lo, hi):
    if lo != 0 or hi != sp.oo or not integrand.has(sp.Pow):
        return None
    expected = (
        ((1 + 3 / symbol) ** symbol) ** sp.Rational(1, 3) - sp.sqrt((1 + 2 / symbol) ** symbol)
    ) / symbol
    if integrand != expected:
        return None
    x, z, scale = sp.symbols("_b_dich_x _b_dich_z _b_dich_scale", positive=True)
    f = (1 + 1 / x) ** x
    if not _eq(expected.subs(symbol, x) - (f.subs(x, x / 3) - f.subs(x, x / 2)) / x):
        return None
    slope = sp.log(1 + z) - z / (1 + z)
    if not _eq(sp.diff(f, x) / f - slope.subs(z, 1 / x)):
        return None
    if not _eq(sp.diff(slope, z) - z / (1 + z) ** 2):
        return None
    if sp.limit(slope, z, 0) != 0 or (z / (1 + z) ** 2).is_positive is not True:
        return None
    first, last = sp.limit(f, x, 0, dir="+"), sp.limit(f, x, sp.oo)
    if first != 1 or last != sp.E:
        return None
    # f increases from 1 to e. Tonelli applies to f'(s*x) >= 0 on
    # s in [1/3,1/2], and the x integral is (f(infinity)-f(0))/s.
    if not _eq(sp.diff(f.subs(x, scale * x), scale) / x - sp.diff(f, x).subs(x, scale * x)):
        return None
    return (first - last) * sp.integrate(1 / scale, (scale, sp.Rational(1, 3), sp.Rational(1, 2)))


def _b_dich_fresnel(integrand, symbol, lo, hi):
    if lo != -sp.oo or hi != sp.oo:
        return None
    phase = symbol**2 + symbol * sp.sqrt(3 * sp.pi) + sp.pi
    if integrand != sp.sin(phase):
        return None
    y = sp.Symbol("_b_dich_y", real=True)
    shift = sp.sqrt(3 * sp.pi) / 2
    shifted_phase = sp.expand(phase.subs(symbol, y - shift))
    if shifted_phase != y**2 + sp.pi / 4:
        return None
    shifted = (sp.sin(y**2) + sp.cos(y**2)) / sp.sqrt(2)
    if not _eq(sp.expand_trig(sp.sin(shifted_phase)) - shifted):
        return None
    if shifted.subs(y, -y) != shifted:
        return None
    sine = sp.integrate(sp.sin(y**2), (y, 0, sp.oo))
    cosine = sp.integrate(sp.cos(y**2), (y, 0, sp.oo))
    if sine.has(sp.Integral) or cosine.has(sp.Integral):
        return None
    # Each one-sided Fresnel integral converges, so a finite translation of
    # the whole-line integral preserves its value without a principal value.
    return sp.simplify(sp.sqrt(2) * (sine + cosine))


def _b_dich_log_ratio(integrand, symbol, lo, hi):
    if lo != 0 or hi != 1 or not integrand.has(sp.log):
        return None
    expected = sp.sqrt(symbol / (1 - symbol)) * sp.log(symbol / (1 - symbol))
    if integrand != expected:
        return None
    t = sp.Symbol("_b_dich_t", positive=True)
    change = t**2 / (1 + t**2)
    if sp.limit(change, t, 0) != 0 or sp.limit(change, t, sp.oo) != 1:
        return None
    if sp.diff(change, t).factor().is_positive is not True:
        return None
    transformed = 4 * t**2 * sp.log(t) / (1 + t**2) ** 2
    if not _eq(expected.subs(symbol, change) * sp.diff(change, t) - transformed):
        return None
    reflected = transformed.subs(t, 1 / t) / t**2
    averaged = 2 * (t**2 - 1) * sp.log(t) / (1 + t**2) ** 2
    if not _eq((transformed + reflected) / 2 - averaged):
        return None
    boundary = -2 * t * sp.log(t) / (1 + t**2)
    remainder = 2 / (1 + t**2)
    if not _eq(averaged - sp.diff(boundary, t) - remainder):
        return None
    if sp.limit(boundary, t, 0, dir="+") != 0 or sp.limit(boundary, t, sp.oo) != 0:
        return None
    return sp.integrate(remainder, (t, 0, sp.oo))


def _b_dich_log_roots(integrand, symbol, lo, hi):
    if lo != 0 or hi != 1 or not integrand.has(sp.log):
        return None
    expected = sp.log(sp.sqrt(symbol) + sp.sqrt(1 - symbol)) / sp.sqrt(symbol)
    if integrand != expected:
        return None
    x = sp.Symbol("_b_dich_x", real=True)
    u = sp.Symbol("_b_dich_u", real=True)
    roots = sp.sqrt(x) + sp.sqrt(1 - x)
    change = sp.sqrt(x) - sp.sqrt(1 - x)
    f = expected.subs(symbol, x)
    if not _eq((f + f.subs(x, 1 - x)) / 2 - sp.log(roots) * sp.diff(change, x)):
        return None
    if sp.expand(roots**2 + change**2) != 2:
        return None
    if change.subs(x, 0) != -1 or change.subs(x, 1) != 1:
        return None
    positive = sp.Symbol("_b_dich_positive", positive=True)
    interior = positive / (1 + positive)
    if sp.simplify(roots.subs(x, interior)).is_positive is not True:
        return None
    if sp.simplify(sp.diff(change, x).subs(x, interior)).is_positive is not True:
        return None
    # On (0,1), both roots are positive and change'(x)>0. Thus the
    # reflected average is 1/2 integral[-1,1] log(2-u**2) du.
    kernel = sp.log(2 - u**2)
    if kernel.subs(u, -u) != kernel:
        return None
    root2 = sp.sqrt(2)
    primitive = u * kernel - 2 * u + root2 * (sp.log(root2 + u) - sp.log(root2 - u))
    if not _eq(sp.diff(primitive, u) - kernel):
        return None
    return sp.simplify(primitive.subs(u, 1) - primitive.subs(u, 0))


def _b_dich_gaussian(integrand, symbol, lo, hi):
    if lo != 0 or hi != sp.oo or not integrand.has(sp.exp):
        return None
    radicand = 1 + ((symbol**4 - 1) / (2 * symbol**2)) ** 2
    expected = sp.exp(-1 - sp.sqrt(radicand))
    if integrand != expected:
        return None
    x = sp.Symbol("_b_dich_x", positive=True)
    y = sp.Symbol("_b_dich_y", real=True)
    root = (x**4 + 1) / (2 * x**2)
    if root.is_positive is not True or not _eq(root**2 - radicand.subs(symbol, x)):
        return None
    change = x - 1 / x
    if not _eq(-1 - root - (-2 - change**2 / 2)):
        return None
    if not _eq(change.subs(x, 1 / x) + change):
        return None
    derivative = sp.diff(change, x)
    if derivative != 1 + 1 / x**2 or derivative.is_positive is not True:
        return None
    if sp.limit(change, x, 0, dir="+") != -sp.oo or sp.limit(change, x, sp.oo) != sp.oo:
        return None
    # Inversion leaves exp(-change**2/2) invariant. Averaging its dx and
    # dx/x**2 integrals supplies half the Jacobian of y=x-1/x.
    normal = sp.integrate(sp.exp(-(y**2) / 2), (y, -sp.oo, sp.oo))
    if normal.has(sp.Integral):
        return None
    return sp.simplify(sp.exp(-2) * normal / 2)


def _b_dich_reciprocal_root(integrand, symbol, lo, hi):
    if lo != 0 or hi != sp.oo:
        return None
    expected = 1 / ((symbol + sp.sqrt(symbol**2 + 1)) * (1 + symbol))
    if integrand != expected:
        return None
    t = sp.Symbol("_b_dich_t", positive=True)
    change = (1 - t**2) / (2 * t)
    root = (1 + t**2) / (2 * t)
    if root.is_positive is not True or not _eq(root**2 - change**2 - 1):
        return None
    if sp.limit(change, t, 0, dir="+") != sp.oo or change.subs(t, 1) != 0:
        return None
    if (-sp.diff(change, t)).factor().is_positive is not True:
        return None
    reduced = (1 + t**2) / (1 + 2 * t - t**2)
    if not _eq(-sp.diff(change, t) / ((change + root) * (1 + change)) - reduced):
        return None
    root2 = sp.sqrt(2)
    primitive = (
        -t - sp.log(1 + 2 * t - t**2) + root2 * (sp.log(root2 + t - 1) - sp.log(root2 - t + 1))
    )
    if not _eq(sp.diff(primitive, t) - reduced):
        return None
    return sp.simplify(primitive.subs(t, 1) - primitive.subs(t, 0))


def open_integrand(expr, symbol):
    return (
        expr.has(sp.Sum) and _b_chain_polynomial_shape(expr, symbol) is not None
    ) or limits_open_integrand(expr, symbol)


def definite_value(expr, symbol, lo, hi):
    for builder in (
        _b_chain_minimum,
        _b_chain_log_power,
        _b_chain_golden_arctangent,
        _b_chain_dirichlet,
        _b_chain_log_cosine,
        _b_chain_hyperbolic,
        _b_chain_real_cube_root,
        _b_chain_gamma,
        _limits_value,
        _b_dich_frullani,
        _b_dich_fresnel,
        _b_dich_log_ratio,
        _b_dich_log_roots,
        _b_dich_gaussian,
        _b_dich_reciprocal_root,
    ):
        value = builder(expr, symbol, lo, hi)
        if value is not None:
            return value
    return None
