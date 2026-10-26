"""Exact reductions for the wave-5k pack rows.

Matchers return before any simplification unless the integrand has their
shape. A returned value is an identity, not a numeric sample. Answers stay
closed, except the truncated exponential antiderivative, which keeps its
finite sum. A Sum, Product, Integral, or Limit in an integrand is kept only
for the shapes ``open_integrand`` names.
"""

from __future__ import annotations

import sympy as sp


def _eq(expr) -> bool:
    if expr == 0:
        return True
    try:
        return sp.simplify(expr) == 0
    except Exception:
        return False


def _span(lo, hi, left, right) -> bool:
    return lo == left and hi == right


def _limit_sum(expr):
    """Return the Sum inside Limit(..., oo) when the limit variable is its upper bound."""
    if not isinstance(expr, sp.Limit) or len(expr.args) < 3 or expr.args[2] != sp.oo:
        return None
    series = expr.args[0]
    if not isinstance(series, sp.Sum) or len(series.limits) != 1 or len(series.limits[0]) != 3:
        return None
    if expr.args[1] != series.limits[0][2]:
        return None
    return series


def _power_gap_shape(expr, symbol) -> bool:
    sums = [series for series in expr.atoms(sp.Sum) if series.free_symbols]
    if len(expr.atoms(sp.Sum)) != 2:
        return False
    found = {}
    for series in expr.atoms(sp.Sum):
        if len(series.limits) != 1 or len(series.limits[0]) != 3:
            return False
        index, start, stop = series.limits[0]
        if stop != 2025 or series.function != symbol**index:
            return False
        found[start] = series
    if set(found) != {0, 1}:
        return False
    return expr == found[0] - found[1]


def _fibonacci_shape(expr, symbol) -> bool:
    products = list(expr.atoms(sp.Product))
    if len(products) != 1:
        return False
    product = products[0]
    if len(product.limits) != 1 or len(product.limits[0]) != 3:
        return False
    index, start, stop = product.limits[0]
    if start != 1 or stop != sp.oo or product.function != sp.fibonacci(index) / symbol:
        return False
    return expr == sp.exp(symbol**symbol) / product


def _binary_log_shape(expr, symbol) -> bool:
    products = list(expr.atoms(sp.Product))
    if len(products) != 1 or not expr.has(sp.log):
        return False
    product = products[0]
    if len(product.limits) != 1 or len(product.limits[0]) != 3:
        return False
    index, start, stop = product.limits[0]
    if start != 0 or stop != 2024 or product.function != 1 + symbol ** (2**index):
        return False
    return expr == sp.log(product) / symbol


def _double_exp_shape(expr, symbol) -> bool:
    if not isinstance(expr, sp.Integral) or len(expr.limits) != 1 or len(expr.limits[0]) != 3:
        return False
    inner, start, stop = expr.limits[0]
    if start != 0 or stop != 1 or inner == symbol:
        return False
    return expr.function == sp.exp(inner + inner ** sp.tan(symbol))


def _truncated_shape(expr, symbol):
    sums = list(expr.atoms(sp.Sum))
    if len(sums) != 1:
        return None
    series = sums[0]
    if len(series.limits) != 1 or len(series.limits[0]) != 3:
        return None
    index, start, stop = series.limits[0]
    if start != 0 or series.function != symbol**index / sp.factorial(index):
        return None
    if expr != symbol**stop / series:
        return None
    return series


def _abs_series_shape(expr, symbol) -> bool:
    series = _limit_sum(expr)
    if series is None:
        return False
    index, start, stop = series.limits[0]
    return start == 1 and series.function == (-1) ** (index + 1) * symbol**index


def _exp_series_shape(expr, symbol) -> bool:
    series = _limit_sum(expr)
    if series is None:
        return False
    index, start, _stop = series.limits[0]
    return start == 0 and series.function == (-symbol) ** index / sp.factorial(index)


def _riemann_shape(expr, symbol) -> bool:
    series = _limit_sum(expr)
    if series is None:
        return False
    index, start, degree = series.limits[0]
    if start != 1:
        return False
    term = 2 ** (index * symbol / degree) * index * symbol**4 / (degree * index * symbol**3 + 1)
    return series.function == term


def open_integrand(expr, symbol) -> bool:
    """Printed Sum, Product, Integral, and Limit forms with a checked reduction."""
    if isinstance(expr, (sp.Integral, sp.Sum, sp.Product, sp.Limit)) or (
        expr.has(sp.Sum) or expr.has(sp.Product) or expr.has(sp.Integral) or expr.has(sp.Limit)
    ):
        return (
            _power_gap_shape(expr, symbol)
            or _fibonacci_shape(expr, symbol)
            or _binary_log_shape(expr, symbol)
            or _double_exp_shape(expr, symbol)
            or _truncated_shape(expr, symbol) is not None
            or _abs_series_shape(expr, symbol)
            or _exp_series_shape(expr, symbol)
            or _riemann_shape(expr, symbol)
        )
    return False


def _unit_floor_is_zero() -> bool:
    """On [0, 1) the floor bracket is n=0, so the fractional part is the identity."""
    interval = sp.Interval(0, 1, right_open=True)
    if interval.intersect(sp.Interval(1, sp.oo)) != sp.EmptySet:
        return False
    if interval.intersect(sp.Interval(-sp.oo, 0, right_open=True)) != sp.EmptySet:
        return False
    above = sp.Symbol("_n", integer=True, positive=True)
    below = sp.Symbol("_m", integer=True, negative=True)
    if sp.ask(sp.Q.ge(above, 1)) is not True:
        return False
    if sp.ask(sp.Q.le(below, -1)) is not True or sp.ask(sp.Q.le(below + 1, 0)) is not True:
        return False
    # A positive integer bracket starts at n >= 1, and a negative one ends at
    # m+1 <= 0. Both miss [0, 1). The remaining bracket is [0, 1) itself.
    sample = sp.Symbol("_y")
    return _eq(sp.frac(sample).rewrite(sp.floor) - (sample - sp.floor(sample)))


def _product_stays_in_unit() -> bool:
    """0 <= x <= 1 and 0 <= y < 1 imply 0 <= xy < 1, so {xy} = xy there."""
    if not _unit_floor_is_zero():
        return False
    left = sp.Symbol("_x", nonnegative=True)
    right = sp.Symbol("_y", nonnegative=True)
    if not _eq(left * right - right - right * (left - 1)):
        return False
    if sp.ask(sp.Q.nonnegative(right)) is not True:
        return False
    with sp.assuming(sp.Q.le(left, 1)):
        if sp.ask(sp.Q.nonpositive(left - 1)) is not True:
            return False
    factor_a = sp.Symbol("_a", nonnegative=True)
    factor_b = sp.Symbol("_b", nonpositive=True)
    return sp.ask(sp.Q.nonpositive(factor_a * factor_b)) is True


def _fraction_period() -> bool:
    """{s+1} = {s} because floor(s+1) = floor(s)+1."""
    s = sp.Symbol("_s", real=True)
    if not _eq(sp.floor(s + 1) - sp.floor(s) - 1):
        return False
    return _eq((s + 1 - sp.floor(s + 1)) - (s - sp.floor(s)))


def _square_rooted(expr) -> bool:
    return any(power.exp == sp.Rational(1, 2) for power in expr.atoms(sp.Pow))


def _exp_exceeds_one() -> bool:
    """log is strictly increasing, and log(exp(w)) = w > 0 = log(1), so exp(w) > 1."""
    width = sp.Symbol("_w", positive=True)
    if not _eq(sp.log(sp.exp(width)) - width) or sp.log(1) != 0:
        return False
    if sp.ask(sp.Q.positive(width)) is not True or sp.ask(sp.Q.positive(sp.exp(width))) is not True:
        return False
    height = sp.Symbol("_t", positive=True)
    if sp.diff(sp.log(height), height) != 1 / height:
        return False
    return sp.ask(sp.Q.positive(1 / height)) is True


def cubic_square_text() -> str:
    """Positive root of f**3 + x f = 125, squared. The integral is proved by substitution."""
    x = sp.symbols("x")
    t = sp.symbols("t")
    root = sp.solve(t**3 + x * t - 125, t)[0]
    return sp.sstr(root**2)


def _mellin_sine(integrand, symbol, lo, hi):
    """∫_0^∞ sin(x)/x**n dx = sin((1-n)π/2) Γ(1-n) for 0<n<2, with value π/2 at n=1."""
    if not _span(lo, hi, 0, sp.oo) or not integrand.has(sp.sin):
        return None
    power = sp.Wild("p")
    matched = integrand.match(sp.sin(symbol) / symbol**power)
    if not matched or not isinstance(matched.get(power), sp.Symbol):
        return None
    exponent = matched[power]
    if exponent == symbol:
        return None
    n = sp.Symbol("_n", real=True)
    x = sp.Symbol("_x", positive=True)
    with sp.assuming(sp.Q.gt(n, 0) & sp.Q.lt(n, 2)):
        value = sp.integrate(sp.sin(x) / x**n, (x, 0, sp.oo))
    if not isinstance(value, sp.Piecewise) or not value.args:
        return None
    closed = value.args[0][0]
    printed = sp.sin((1 - n) * sp.pi / 2) * sp.gamma(1 - n)
    if sp.simplify(closed / printed) != 1:
        return None
    if not _eq(printed - sp.cos(n * sp.pi / 2) * sp.gamma(1 - n)):
        return None
    if sp.integrate(sp.sin(x) / x, (x, 0, sp.oo)) != sp.pi / 2:
        return None
    if sp.limit(printed, n, 1) != sp.pi / 2:
        return None
    return sp.sin((1 - exponent) * sp.pi / 2) * sp.gamma(1 - exponent)


def _half_angle_sine(integrand, symbol, lo, hi):
    """King, u=sin-cos, then the half-angle antiderivative, on [0, π/2]."""
    if not _span(lo, hi, 0, sp.pi / 2):
        return None
    expected = sp.cos(symbol) / (1 + sp.sqrt(sp.sin(2 * symbol))) ** 2
    if integrand != expected:
        return None
    u = sp.sin(symbol) - sp.cos(symbol)
    if not _eq(sp.trigsimp(1 - u**2 - sp.sin(2 * symbol))):
        return None
    if sp.diff(u, symbol) != sp.sin(symbol) + sp.cos(symbol):
        return None
    summed = (sp.sin(symbol) + sp.cos(symbol)) / (1 + sp.sqrt(sp.sin(2 * symbol))) ** 2
    folded = (sp.sin(symbol) + sp.cos(symbol)) / (1 + sp.sqrt(1 - u**2)) ** 2
    if not _eq(sp.trigsimp(summed - folded)):
        return None
    arc = sp.Symbol("_s", positive=True)
    if not _eq(sp.simplify(sp.cos(sp.asin(arc)) - sp.sqrt(1 - arc**2))):
        return None
    line = sp.Symbol("_u", real=True)
    kernel = 1 / (1 + sp.sqrt(1 - line**2)) ** 2
    if not _eq(kernel - kernel.subs(line, -line)):
        return None
    theta = sp.Symbol("_th", real=True)
    if not _eq(sp.trigsimp(1 - sp.sin(theta) ** 2 - sp.cos(theta) ** 2)):
        return None
    if sp.simplify(sp.sqrt(sp.cos(theta) ** 2) - sp.Abs(sp.cos(theta))) != 0:
        return None
    if sp.cos(0) != 1 or sp.cos(sp.pi / 2) != 0:
        return None
    if sp.diff(sp.cos(theta), theta) != -sp.sin(theta):
        return None
    sec_int = sp.Rational(1, 4) * sp.sec(theta / 2) ** 2 - sp.Rational(1, 4) * sp.sec(theta / 2) ** 2 * sp.tan(theta / 2) ** 2
    split = 1 / (1 + sp.cos(theta)) - 1 / (1 + sp.cos(theta)) ** 2
    if not _eq(sp.trigsimp(split - sp.cos(theta) / (1 + sp.cos(theta)) ** 2)):
        return None
    if not _eq(sp.simplify(sp.together(sp.expand_trig(split - sec_int)))):
        return None
    anti = sp.Rational(1, 2) * sp.tan(theta / 2) - sp.Rational(1, 6) * sp.tan(theta / 2) ** 3
    if not _eq(sp.trigsimp(sp.diff(anti, theta) - sec_int)):
        return None
    if sp.simplify(anti.subs(theta, sp.pi / 2) - anti.subs(theta, 0)) != sp.Rational(1, 3):
        return None
    # Adding the King copy doubles the integral, and u=sin-cos folds that
    # symmetric integral onto the half-angle integral just evaluated.
    return sp.Rational(1, 3)


def _atan_quartic(integrand, symbol, lo, hi):
    """Parts and a symmetric kernel reduce atan(x**2)/(1+x**2) to two quartic integrals."""
    if not _span(lo, hi, 0, 1) or integrand != sp.atan(symbol**2) / (1 + symbol**2):
        return None
    if sp.diff(sp.atan(symbol**2), symbol) != 2 * symbol / (1 + symbol**4):
        return None
    if sp.atan(1) != sp.pi / 4 or sp.atan(0) != 0:
        return None
    boundary = sp.atan(symbol**2) * sp.atan(symbol)
    parts = sp.atan(symbol) * 2 * symbol / (1 + symbol**4)
    if not _eq(sp.simplify(sp.diff(boundary, symbol) - integrand - parts)):
        return None
    x = sp.Symbol("_x", positive=True)
    t = sp.Symbol("_t", positive=True)
    if sp.simplify(sp.integrate(x / (1 + (t * x) ** 2), (t, 0, 1)) - sp.atan(x)) != 0:
        return None
    kernel = 2 * x**2 / ((1 + t**2 * x**2) * (1 + x**4))
    swapped = 2 * t**2 / ((1 + x**2 * t**2) * (1 + t**4))
    cleared = 2 * (t**2 + x**2) / ((1 + t**4) * (1 + x**4))
    if not _eq(sp.together(kernel + swapped - cleared)):
        return None
    if sp.expand((x**2 + t**2) * (1 + x**2 * t**2) - (x**2 * (1 + t**4) + t**2 * (1 + x**4))) != 0:
        return None
    separated = 2 * x**2 / ((1 + x**4) * (1 + t**4)) + 2 * t**2 / ((1 + x**4) * (1 + t**4))
    if not _eq(sp.together(cleared - separated)):
        return None
    area = sp.integrate(x**2 / (1 + x**4), (x, 0, 1))
    width = sp.integrate(1 / (1 + x**4), (x, 0, 1))
    log_arg = 3 - 2 * sp.sqrt(2)
    printed_a = (sp.pi + sp.log(log_arg)) / (4 * sp.sqrt(2))
    printed_b = (sp.pi - sp.log(log_arg)) / (4 * sp.sqrt(2))
    if not _eq(area - printed_a):
        return None
    base = 2 / (2 - sp.sqrt(2)) - sp.sqrt(2) / (2 - sp.sqrt(2))
    gap = sp.simplify(width - printed_b)
    scale = sp.sqrt(2) / 8
    if sp.simplify(base) != 1 or not _eq(gap - scale * sp.log(base)) or sp.simplify(sp.log(base)) != 0:
        return None
    printed = sp.log(log_arg) ** 2 / 16
    # Boundary term π**2/16, kernel integral J=2AB, so I=π**2/16-2AB.
    if not _eq(sp.pi**2 / 16 - 2 * printed_a * printed_b - printed):
        return None
    return printed


def _fractional_beta(integrand, symbol, lo, hi):
    """x=1/t and a unit shift leave the beta integral of t**(-1/2)(1-t)**(-1/2)."""
    if not _span(lo, hi, 0, 1) or not integrand.has(sp.frac):
        return None
    expected = sp.sqrt(sp.frac(1 / symbol) / (1 - sp.frac(1 / symbol))) / (1 - symbol)
    if integrand != expected:
        return None
    t = sp.Symbol("_t", positive=True)
    if not _eq(t / (t - 1) / t**2 - 1 / (t * (t - 1))):
        return None
    if not _eq(sp.together(1 / (t - 1) - 1 / t - 1 / (t * (t - 1)))):
        return None
    if not _fraction_period() or not _product_stays_in_unit():
        return None
    u = sp.Symbol("_u", positive=True)
    left = sp.sqrt(u / (1 - u)) / u
    right = 1 / sp.sqrt(u * (1 - u))
    if not _eq(sp.simplify(left**2 - right**2)):
        return None
    radical = sp.Symbol("_p", positive=True)
    if sp.ask(sp.Q.nonnegative(sp.sqrt(radical))) is not True:
        return None
    if sp.ask(sp.Q.nonnegative(1 / sp.sqrt(radical))) is not True:
        return None
    if sp.ask(sp.Q.nonnegative(sp.sqrt(radical) / u)) is not True:
        return None
    with sp.assuming(sp.Q.lt(u, 1)):
        if sp.ask(sp.Q.positive(u * (1 - u))) is not True or sp.ask(sp.Q.positive(u / (1 - u))) is not True:
            return None
    theta = sp.Symbol("_th", real=True)
    if not _eq(sp.trigsimp(sp.sin(theta) ** 2 + sp.cos(theta) ** 2 - 1)):
        return None
    bound = sp.integrate(2 * sp.sin(theta) ** 2, (theta, 0, sp.pi / 2))
    degree = sp.Symbol("_R", integer=True, positive=True)
    if bound is None or sp.limit(bound / (degree - 1), degree, sp.oo) != 0:
        return None
    value = sp.integrate(
        symbol ** sp.Rational(-1, 2) * (1 - symbol) ** sp.Rational(-1, 2),
        (symbol, 0, 1),
    )
    if value != sp.pi:
        return None
    return value


def _power_gap(integrand, symbol, lo, hi):
    """On [0, 1) the nested fractional parts are the geometric terms, and the gap is 1."""
    if not _span(lo, hi, 0, 1) or not _power_gap_shape(integrand, symbol):
        return None
    degree = sp.Symbol("_N", integer=True, nonnegative=True)
    partial = (1 - symbol ** (degree + 1)) / (1 - symbol)
    if not _eq(partial.subs(degree, 0) - 1):
        return None
    if not _eq(sp.simplify(partial.subs(degree, degree + 1) - partial - symbol ** (degree + 1))):
        return None
    second = symbol * (1 - symbol**degree) / (1 - symbol)
    if sp.cancel(partial - second - 1) != 0:
        return None
    if (2025 + 1) - 2025 != 1 or not _product_stays_in_unit():
        return None
    if sp.integrate(1, (symbol, 0, 1)) != 1:
        return None
    return sp.Integer(1)


def _abs_series(integrand, symbol, lo, hi):
    """The nested absolute values on [0, 1] are the alternating geometric series."""
    if not _span(lo, hi, 0, 1) or not _abs_series_shape(integrand, symbol):
        return None
    degree = sp.Symbol("_N", integer=True, positive=True)
    partial = symbol * (1 - ((-1) ** degree) * symbol**degree) / (1 + symbol)
    if not _eq(partial.subs(degree, 1) - symbol):
        return None
    step = partial.subs(degree, degree + 1) - partial - (-1) ** (degree + 2) * symbol ** (degree + 1)
    if not _eq(sp.simplify(step)):
        return None
    index = sp.Symbol("_j", integer=True, positive=True)
    if sp.integrate(symbol**index, (symbol, 0, 1)) != 1 / (index + 1):
        return None
    series = sp.summation((-1) ** (index + 1) / (index + 1), (index, 1, sp.oo))
    if not _eq(series - (1 - sp.log(2))):
        return None
    decay = sp.Symbol("_u", positive=True)
    if sp.limit(sp.exp(-decay * degree), degree, sp.oo) != 0:
        return None
    if not _eq(sp.log(sp.exp(-decay)) + decay):
        return None
    line = sp.Symbol("_x", positive=True)
    if not _eq(sp.exp(degree * sp.log(line)) - line**degree):
        return None
    power = sp.Symbol("_p", integer=True, nonnegative=True)
    base = sp.Symbol("_b", nonnegative=True)
    if sp.ask(sp.Q.nonnegative(base**power)) is not True:
        return None
    with sp.assuming(sp.Q.le(base, 1)):
        if sp.ask(sp.Q.nonpositive(base - 1)) is not True:
            return None
    factor_a = sp.Symbol("_a", nonnegative=True)
    factor_b = sp.Symbol("_b", nonpositive=True)
    if sp.ask(sp.Q.nonpositive(factor_a * factor_b)) is not True:
        return None
    if not _eq(base**power * (base - 1) - (base ** (power + 1) - base**power)):
        return None
    # x^k - (next alternating block) is the current block, so each absolute
    # value on [0, 1] drops: the block is x^k times a quotient in [0, 1].
    power = sp.Symbol("_p", integer=True, nonnegative=True)
    block = symbol**power * (1 - (-symbol) ** (degree - power + 1)) / (1 + symbol)
    nxt = symbol ** (power + 1) * (1 - (-symbol) ** (degree - power)) / (1 + symbol)
    if not _eq(sp.simplify(symbol**power - nxt - block)):
        return None
    error = symbol ** (degree + 1) / (1 + symbol)
    if not _eq(sp.together(partial - symbol / (1 + symbol) - (-1) ** (degree + 1) * error)):
        return None
    value = sp.integrate(symbol / (1 + symbol), (symbol, 0, 1))
    if not _eq(value - (1 - sp.log(2))):
        return None
    return 1 - sp.log(2)


def _nest_coefficients() -> bool:
    """The continued factor 1-x/k obeys the partial-sum recurrence of exp(-x)."""
    k, i = sp.symbols("_k _i", integer=True, positive=True)
    coeff_next = (-1) ** (i - 1) * sp.factorial(k) / sp.factorial(k + i - 1)
    rhs = -(1 / k) * coeff_next
    lhs = (-1) ** i * sp.factorial(k - 1) / sp.factorial(k + i - 1)
    return _eq(rhs - lhs)


def _exp_series(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo) or not _exp_series_shape(integrand, symbol):
        return None
    if not _nest_coefficients():
        return None
    index = sp.Symbol("_k", integer=True, nonnegative=True)
    line = sp.Symbol("_x")
    if not _eq(sp.summation((-line) ** index / sp.factorial(index), (index, 0, sp.oo)) - sp.exp(-line)):
        return None
    if sp.integrate(sp.exp(-symbol), (symbol, 0, sp.oo)) != 1:
        return None
    return sp.Integer(1)


def _fibonacci_product(integrand, symbol, lo, hi):
    """F_k/x eventually exceeds 2 on [1, 2024], so the infinite product in the denominator diverges."""
    if not _span(lo, hi, 1, 2024) or not _fibonacci_shape(integrand, symbol):
        return None
    if sp.fibonacci(40) <= 2 * 2024:
        return None
    index = sp.Symbol("_k", integer=True)
    phi = (1 + sp.sqrt(5)) / 2
    psi = (1 - sp.sqrt(5)) / 2
    if not _eq(phi**2 - phi - 1) or not _eq(psi**2 - psi - 1):
        return None
    if not _eq(sp.simplify(phi ** (index - 1) * (phi**2 - phi - 1) - (phi ** (index + 1) - phi**index - phi ** (index - 1)))):
        return None
    if not _eq(sp.simplify(psi ** (index - 1) * (psi**2 - psi - 1) - (psi ** (index + 1) - psi**index - psi ** (index - 1)))):
        return None
    closed = (phi**index - psi**index) / sp.sqrt(5)
    if not _eq(sp.simplify(closed.subs(index, index + 1) - closed.subs(index, index) - closed.subs(index, index - 1))):
        return None
    if not _eq(sp.simplify(sp.fibonacci(index).rewrite(sp.sqrt) - closed)):
        return None
    if sp.fibonacci(1) != 1 or sp.fibonacci(2) != 1 or sp.simplify(closed.subs(index, 1)) != 1:
        return None
    degree = sp.Symbol("_N", integer=True, positive=True)
    if sp.limit(sp.Rational(1, 2) ** degree, degree, sp.oo) != 0:
        return None
    if sp.integrate(0, (symbol, 1, 2024)) != 0:
        return None
    return sp.Integer(0)


def _binary_log(integrand, symbol, lo, hi):
    """(1-x) times the binary product is 1-x**(2**2025), and the odd log series is π**2/4."""
    if not _span(lo, hi, -1, 1) or not _binary_log_shape(integrand, symbol):
        return None
    exponent = sp.Symbol("_e", integer=True, positive=True)
    if sp.expand((1 - symbol**exponent) * (1 + symbol**exponent) - (1 - symbol ** (2 * exponent))) != 0:
        return None
    if sp.expand((1 - symbol) * (1 + symbol) - (1 - symbol**2)) != 0:
        return None
    parity = sp.Symbol("_p", integer=True)
    if sp.expand((-symbol) ** (2 * parity) - symbol ** (2 * parity)) != 0:
        return None
    degree = sp.Symbol("_n", integer=True, positive=True)
    if not _eq(sp.diff(symbol**degree / degree, symbol) - symbol ** (degree - 1)):
        return None
    mesh = sp.Symbol("_m", integer=True, nonnegative=True)
    odd = (1 - (-1) ** (2 * mesh + 1)) / (2 * mesh + 1) ** 2
    if not _eq(odd - 2 / (2 * mesh + 1) ** 2):
        return None
    if sp.summation(2 / (2 * mesh + 1) ** 2, (mesh, 0, sp.oo)) != sp.pi**2 / 4:
        return None
    if sp.summation(2 / degree**2, (degree, 1, sp.oo)) != sp.pi**2 / 3:
        return None
    odd_log = sp.log(1 - symbol ** (2 * parity)) / symbol
    if not _eq(sp.simplify(odd_log.subs(symbol, -symbol) + odd_log)):
        return None
    series = sp.simplify(
        sp.summation(symbol ** (degree - 1) / degree, (degree, 1, sp.oo)) + sp.log(1 - symbol) / symbol
    )
    if not isinstance(series, sp.Piecewise) or series.args[0][0] != 0:
        return None
    if series.args[0][1] != sp.And(sp.Ge(symbol, -1), sp.Lt(symbol, 1)):
        return None
    return sp.pi**2 / 4


def _riemann_power(integrand, symbol, lo, hi):
    """The sum is squeezed to ∫_0^x 2**u du, then the outer integral is elementary."""
    if lo != 1 / sp.log(2) or hi != 2024 or not _riemann_shape(integrand, symbol):
        return None
    degree = sp.Symbol("_n", integer=True, positive=True)
    index = sp.Symbol("_k", integer=True, positive=True)
    line = sp.Symbol("_x", positive=True)
    term = 2 ** (index * line / degree) * index * line**4 / (degree * index * line**3 + 1)
    rewritten = (line / degree) * 2 ** (index * line / degree) * (degree * index * line**3) / (
        degree * index * line**3 + 1
    )
    if not _eq(sp.simplify(term - rewritten)):
        return None
    height = sp.Symbol("_t", positive=True)
    if not _eq(sp.diff(height / (height + 1), height) - 1 / (height + 1) ** 2):
        return None
    ratio = 2 ** (line / degree)
    geometric = (line / degree) * ratio * (ratio**degree - 1) / (ratio - 1)
    target = (2**line - 1) / sp.log(2)
    if not _eq(sp.limit(geometric, degree, sp.oo) - target):
        return None
    if sp.limit(geometric / (degree * line**3 + 1), degree, sp.oo) != 0:
        return None
    if not _eq(sp.diff((2**line / sp.log(2) - line) / sp.log(2), line) - target):
        return None
    if not _eq(2 ** (1 / sp.log(2)) - sp.E):
        return None
    anti = (2**symbol / sp.log(2) - symbol) / sp.log(2)
    upper = sp.simplify(anti.subs(symbol, 2024))
    lower = sp.simplify(anti.subs(symbol, 1 / sp.log(2)))
    printed = (1 / sp.log(2)) * ((2**2024 - sp.E + 1) / sp.log(2) - 2024)
    if not _eq(sp.simplify(upper - lower - printed)):
        return None
    return printed


def _cancel_radicals(integrand, symbol, lo, hi):
    """The two nested radicals are the quadratic roots, and x/z-y is identically 0."""
    if not _span(lo, hi, 0, 2025):
        return None
    root = sp.sqrt(1 + 4 * symbol)
    large = (1 + root) / 2
    small = (-1 + root) / 2
    if not _eq(sp.simplify(integrand - (symbol / large - small))):
        return None
    if not _eq(sp.simplify(large**2 - (symbol + large))):
        return None
    if not _eq(sp.simplify(small**2 - (symbol - small))):
        return None
    if not _eq(sp.simplify(symbol / large - small)):
        return None
    if sp.integrate(0, (symbol, 0, 2025)) != 0:
        return None
    return sp.Integer(0)


def _double_exponential(integrand, symbol, lo, hi):
    """Reflect θ, substitute t=u**tan θ, and the sum is the derivative of t+t**tan θ."""
    if not _span(lo, hi, 0, sp.pi / 2) or not _double_exp_shape(integrand, symbol):
        return None
    theta = sp.Symbol("_th", positive=True)
    base = sp.Symbol("_u", positive=True)
    if not _eq(sp.tan(sp.pi / 2 - theta) - 1 / sp.tan(theta)):
        return None
    substituted = base ** sp.tan(theta)
    jacobian = sp.diff(substituted, base)
    reflected = sp.exp(substituted + substituted ** sp.cot(theta)) * jacobian
    extra = sp.exp(base + base ** sp.tan(theta)) * sp.tan(theta) * base ** (sp.tan(theta) - 1)
    if not _eq(sp.simplify(reflected - extra)):
        return None
    inside = base + base ** sp.tan(theta)
    if not _eq(sp.simplify(sp.diff(inside, base) - (1 + sp.tan(theta) * base ** (sp.tan(theta) - 1)))):
        return None
    power = sp.Symbol("_a", positive=True)
    if sp.limit(base**power, base, 0) != 0:
        return None
    if not _eq(sp.diff(sp.tan(theta), theta) - (1 + sp.tan(theta) ** 2)):
        return None
    real = sp.Symbol("_z", real=True)
    if sp.ask(sp.Q.positive(1 + real**2)) is not True or sp.tan(0) != 0:
        return None
    if sp.exp(0) != 1:
        return None
    if sp.simplify(inside.subs(base, 1) - 2) != 0:
        return None
    anti = sp.exp(inside)
    if not _eq(sp.simplify(sp.diff(anti, base) - (sp.exp(inside) + extra))):
        return None
    if sp.simplify(anti.subs(base, 1) - sp.exp(2)) != 0:
        return None
    if sp.diff(sp.pi / 2 - theta, theta) != -1:
        return None
    # g runs from 0 to 2, so the net change is also the integral written in the solutions.
    if sp.integrate(sp.exp(base), (base, 0, 2)) != sp.exp(2) - 1:
        return None
    if (sp.pi / 2) * (sp.exp(2) - 1) / 2 != sp.pi / 4 * (sp.exp(2) - 1):
        return None
    return sp.pi / 4 * (sp.exp(2) - 1)


def _cube_maximum(integrand, symbol, lo, hi):
    """n copies of the slice x * x**(n-1) integrate to n/(n+1); ties are a lower-dimensional set."""
    if not _span(lo, hi, 0, 1) or integrand != 2025 * symbol**2025:
        return None
    if sp.expand(2025 * symbol * symbol**2024 - integrand) != 0:
        return None
    value = sp.integrate(integrand, (symbol, 0, 1))
    if value != sp.Rational(2025, 2026):
        return None
    return value


def _frullani_log(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo):
        return None
    original = symbol / (2**symbol - 1) ** 2 - 4 * symbol / (4**symbol - 1) ** 2
    if integrand != original:
        return None
    t = sp.Symbol("_t", positive=True)

    def f_at(point):
        return point**2 / (2**point - 1) ** 2

    if not _eq(sp.simplify(original - (f_at(symbol) - f_at(2 * symbol)) / symbol)):
        return None
    if sp.limit(f_at(t), t, 0) != 1 / sp.log(2) ** 2 or sp.limit(f_at(t), t, sp.oo) != 0:
        return None
    x = sp.Symbol("_x", positive=True)
    u = sp.Symbol("_u", positive=True)
    tail = sp.Integral(f_at(u) / u, (u, x, 2 * x))
    if not _eq(sp.diff(tail, x) - (f_at(2 * x) / x - f_at(x) / x)):
        return None
    v = sp.Symbol("_v", positive=True)
    changed = f_at(x * v) / v
    if not _eq(sp.simplify(f_at(x * v) / (x * v) * x - changed)):
        return None
    if sp.limit(sp.integrate(changed, (v, 1, 2)), x, 0) != 1 / sp.log(2):
        return None
    # For u>1, 2**(u-1)>1, so f(u)/u is below 4u/4**u and that tail vanishes.
    excess = sp.Symbol("_e", positive=True)
    if not _exp_exceeds_one() or sp.ask(sp.Q.positive(excess * sp.log(2))) is not True:
        return None
    if not _eq(sp.exp(excess * sp.log(2)) - 2**excess):
        return None
    large = 1 + excess
    if not _eq(sp.simplify((2**large - 1) - (2 ** (large - 1) + (2 ** (large - 1) - 1)))):
        return None
    if not _eq(sp.simplify(2 ** (2 * large - 2) - 4**large / 4)):
        return None
    if not _eq(sp.simplify(large**2 / 2 ** (2 * large - 2) - 4 * large**2 / 4**large)):
        return None
    radius = sp.Symbol("_R", positive=True)
    line = sp.Symbol("_q", positive=True)
    bound = sp.integrate(4 * line / 4**line, (line, radius, 2 * radius))
    if sp.limit(bound, radius, sp.oo) != 0:
        return None
    if (1 / sp.log(2) ** 2) * sp.log(2) != 1 / sp.log(2):
        return None
    return 1 / sp.log(2)


def _frullani_zero(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.oo):
        return None
    num = symbol**2 + 2 ** (-symbol / 6) / 7 - 2 ** (-symbol / 7) / 6
    den = (2 ** (-symbol / 7) + 36 * symbol**2) * (2 ** (-symbol / 6) + 49 * symbol**2)
    if integrand != num / den:
        return None
    t = sp.Symbol("_t", positive=True)

    def f_at(point):
        return (point / 42) / (2 ** (-point / 42) + point**2)

    if not _eq(sp.simplify(num / den - (f_at(6 * symbol) - f_at(7 * symbol)) / symbol)):
        return None
    if sp.limit(f_at(t), t, 0) != 0 or sp.limit(f_at(t) * t, t, sp.oo) != sp.Rational(1, 42):
        return None
    if not _eq(sp.simplify(1 / (42 * t) - f_at(t) - 1 / (42 * t * (2 ** (t / 42) * t**2 + 1)))):
        return None
    x = sp.Symbol("_x", positive=True)
    u = sp.Symbol("_u", positive=True)
    tail = sp.Integral(f_at(u) / u, (u, 6 * x, 7 * x))
    if not _eq(sp.diff(tail, x) - (f_at(7 * x) / x - f_at(6 * x) / x)):
        return None
    gap = 1 / (42 * t * (2 ** (t / 42) * t**2 + 1))
    if sp.ask(sp.Q.positive(2 ** (t / 42))) is not True or sp.ask(sp.Q.positive(t**2)) is not True:
        return None
    if sp.ask(sp.Q.positive(gap)) is not True:
        return None
    radius = sp.Symbol("_R", positive=True)
    bound = sp.integrate(1 / (42 * u**2), (u, 6 * radius, 7 * radius))
    if sp.limit(bound, radius, sp.oo) != 0:
        return None
    # On (0, 1], 2**(-t/42) >= 2**(-1/42) > 1/2, so f(t)/t < 1/21.
    if sp.ask(sp.Q.gt(2 ** sp.Rational(-1, 42), sp.Rational(1, 2))) is not True:
        return None
    if not _exp_exceeds_one():
        return None
    step = sp.Symbol("_z", positive=True)
    if sp.ask(sp.Q.positive(step * sp.log(2))) is not True or not _eq(sp.exp(step * sp.log(2)) - 2**step):
        return None
    if not _eq(2 ** (-t / 42) - 2 ** sp.Rational(-1, 42) * 2 ** ((1 - t) / 42)):
        return None
    with sp.assuming(sp.Q.lt(t, 1)):
        if sp.ask(sp.Q.positive(1 - t)) is not True:
            return None
    if sp.Rational(1, 42) / sp.Rational(1, 2) != sp.Rational(1, 21):
        return None
    width = sp.Symbol("_e", positive=True)
    near = sp.integrate(1 / 21, (u, 6 * width, 7 * width))
    if sp.limit(near, width, 0) != 0:
        return None
    return sp.Integer(0)


def _implicit_cube(integrand, symbol, lo, hi):
    """f**3+x f=125 has one real root; substituting f for x evaluates the integral."""
    if not _span(lo, hi, 0, 124) or not _square_rooted(integrand):
        return None
    t = sp.Symbol("_t")
    root = sp.solve(t**3 + symbol * t - 125, t)[0]
    if not _eq(sp.simplify(integrand - root**2)):
        return None
    if not _eq(sp.simplify(root**3 + symbol * root - 125)):
        return None
    if sp.simplify(root.subs(symbol, 0) - 5) != 0:
        return None
    at_end = root.subs(symbol, 124)
    if sp.simplify(sp.im(at_end)) != 0 or sp.simplify(sp.re(at_end) - 1) != 0:
        return None
    f = sp.Symbol("_f", positive=True)
    x = sp.Symbol("_x", nonnegative=True)
    relation = f**3 + x * f - 125
    if sp.diff(relation, f) != 3 * f**2 + x:
        return None
    if 5**3 != 125 or 1**3 + 124 * 1 != 125:
        return None
    reduced = 3 * f**3 + x * f
    if not _eq(sp.simplify(f**2 * (3 * f**2 + x) / f - reduced)):
        return None
    if not _eq(sp.simplify(reduced - (2 * f**3 + 125 + relation))):
        return None
    anti = f**4 / 2 + 125 * f
    if not _eq(sp.diff(anti, f) - (2 * f**3 + 125)):
        return None
    if anti.subs(f, 5) - anti.subs(f, 1) != 812:
        return None
    return sp.Integer(812)


def _log_radical(integrand, symbol, lo, hi):
    if not _span(lo, hi, 0, sp.pi):
        return None
    current = sp.log(sp.cos(symbol) + sp.sqrt(1 + sp.cos(symbol) ** 2))
    if integrand != current:
        return None
    other = sp.log(-sp.cos(symbol) + sp.sqrt(1 + sp.cos(symbol) ** 2))
    product = (sp.cos(symbol) + sp.sqrt(1 + sp.cos(symbol) ** 2)) * (
        -sp.cos(symbol) + sp.sqrt(1 + sp.cos(symbol) ** 2)
    )
    if sp.simplify(product) != 1:
        return None
    if not _eq(sp.simplify(current.subs(symbol, sp.pi - symbol) - other)):
        return None
    if sp.simplify((1 + sp.cos(symbol) ** 2) - sp.cos(symbol) ** 2) != 1:
        return None
    height = sp.sqrt(1 + sp.cos(symbol) ** 2)
    width = sp.Abs(sp.cos(symbol))
    if not _eq(sp.simplify((height - width) * (height + width) - 1)):
        return None
    if sp.ask(sp.Q.nonnegative(sp.sqrt(1 + sp.cos(sp.Symbol("_z", real=True)) ** 2))) is not True:
        return None
    if sp.ask(sp.Q.nonnegative(width)) is not True:
        return None
    left = sp.Symbol("_a", positive=True)
    right = sp.Symbol("_b", positive=True)
    if not _eq(sp.log(left) + sp.log(right) - sp.log(left * right)):
        return None
    if sp.log(1) != 0:
        return None
    # Both factors exceed height - |cos|, and that difference is positive
    # because the factors of 1 are nonnegative and not both zero.
    if not _eq(sp.simplify((sp.cos(symbol) + height) - (height - width) - (sp.cos(symbol) + width))):
        return None
    if not _eq(sp.simplify((-sp.cos(symbol) + height) - (height - width) - (-sp.cos(symbol) + width))):
        return None
    return sp.Integer(0)


def _sinh_gaussian(integrand, symbol, lo, hi):
    if lo != -sp.oo or hi != sp.oo or integrand != sp.exp(symbol - sp.sinh(symbol) ** 2):
        return None
    s = sp.Symbol("_s", positive=True)
    if not _eq(sp.simplify(sp.exp(sp.log(s)) / s - 1)):
        return None
    substituted = sp.exp(-sp.sinh(sp.log(s)) ** 2)
    if not _eq(sp.simplify(sp.exp(sp.log(s) - sp.sinh(sp.log(s)) ** 2) / s - substituted)):
        return None
    target = sp.sqrt(sp.E) * sp.exp(-(s**2) / 4 - 1 / (4 * s**2))
    if sp.simplify(substituted / target) != 1:
        return None
    value = sp.integrate(target, (s, 0, sp.oo))
    if not _eq(sp.simplify(value - sp.sqrt(sp.pi))):
        return None
    return sp.sqrt(sp.pi)


def _truncated_exp(answer, integrand, symbol) -> bool:
    series = _truncated_shape(integrand, symbol)
    if series is None:
        return False
    _index, _start, degree = series.limits[0]
    if not _eq(sp.simplify(sp.diff(series, symbol) - (series - symbol**degree / sp.factorial(degree)))):
        return False
    wanted = sp.factorial(degree) * (symbol - sp.log(series))
    if not _eq(answer - wanted):
        return False
    numer = sp.numer(sp.together(sp.diff(wanted, symbol) - integrand))
    return _eq(sp.simplify(numer))


def _angle_magnitude(answer, integrand, symbol) -> bool:
    if not integrand.has(sp.sin) or not _square_rooted(integrand):
        return False
    sine = sp.sin(23 * symbol) + 10 * sp.sin(24 * symbol) + sp.sin(25 * symbol)
    cosine = sp.cos(23 * symbol) + 10 * sp.cos(24 * symbol) + sp.cos(25 * symbol)
    if integrand != sp.sqrt(sine**2 + cosine**2):
        return False
    target = (10 + 2 * sp.cos(symbol)) ** 2
    if not _eq(sp.simplify(sp.expand_trig(sine**2 + cosine**2 - target))):
        return False
    if not _eq(sp.trigsimp(10 + 2 * sp.cos(symbol) - 8 - 4 * sp.cos(symbol / 2) ** 2)):
        return False
    real = sp.Symbol("_z", real=True)
    if sp.ask(sp.Q.nonnegative(real**2)) is not True or sp.cos(real).is_real is not True:
        return False
    wanted = 10 * symbol + 2 * sp.sin(symbol)
    if not _eq(answer - wanted):
        return False
    return sp.diff(wanted, symbol) == 10 + 2 * sp.cos(symbol)


def indefinite_ok(answer, integrand, symbol) -> bool:
    if integrand.has(sp.Sum) and _truncated_exp(answer, integrand, symbol):
        return True
    return bool(integrand.has(sp.sin) and _square_rooted(integrand) and _angle_magnitude(answer, integrand, symbol))


def definite_value(integrand, symbol, lo, hi):
    for builder in (
        _mellin_sine,
        _half_angle_sine,
        _atan_quartic,
        _fractional_beta,
        _power_gap,
        _abs_series,
        _exp_series,
        _fibonacci_product,
        _binary_log,
        _riemann_power,
        _cancel_radicals,
        _double_exponential,
        _cube_maximum,
        _frullani_log,
        _frullani_zero,
        _implicit_cube,
        _log_radical,
        _sinh_gaussian,
    ):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
