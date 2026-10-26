"""Exact certificates for nested sphere, tangent-ray and finite-grid integrals.

The accompanying solutions/pack notes supply the change-of-variables,
Cauchy-theorem and coefficient-comparison arguments. These certificates
check the symbolic identities and hypotheses used in those arguments.
They match mathematical expressions and never inspect a catalog id.
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


def _require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def matches_sphere_integral(integrand, symbol):
    """Admit only the printed inner integral; do not relax other inputs."""
    inners = list(integrand.atoms(sp.Integral))
    if len(inners) != 1:
        return False
    inner = inners[0]
    if len(inner.limits) != 1 or len(inner.limits[0]) != 3:
        return False
    angle, start, stop = inner.limits[0]
    if not isinstance(angle, sp.Symbol) or angle == symbol:
        return False
    if start != 0 or stop != 2 * sp.pi:
        return False
    exponent = sp.sin(symbol) * (sp.cos(angle) - sp.sin(angle))
    expected = sp.sin(symbol) * sp.Integral(sp.exp(exponent), (angle, 0, 2 * sp.pi))
    return integrand == expected


def sphere_integral_value(integrand, symbol, lo, hi):
    """Rotate the unit sphere, preserving the explicit inner integral."""
    if lo != 0 or hi != sp.pi or not matches_sphere_integral(integrand, symbol):
        return None
    inner = next(iter(integrand.atoms(sp.Integral)))
    angle = sp.Dummy("sphere_angle", real=True)
    exponent = inner.function.args[0].subs(inner.limits[0][0], angle)
    coefficients = sp.expand(exponent / sp.sin(symbol))
    a = coefficients.coeff(sp.cos(angle))
    b = coefficients.coeff(sp.sin(angle))
    _require(sp.simplify(coefficients - a * sp.cos(angle) - b * sp.sin(angle)) == 0,
             "sphere-coefficients")
    vector = sp.Matrix([a, b, 0])
    radius = sp.sqrt(vector.dot(vector))
    point = sp.Matrix([
        sp.sin(symbol) * sp.cos(angle),
        sp.sin(symbol) * sp.sin(angle),
        sp.cos(symbol),
    ])
    rotation = sp.Matrix([
        [-b / radius, 0, a / radius],
        [a / radius, 0, b / radius],
        [0, 1, 0],
    ])
    area_vector = point.diff(symbol).cross(point.diff(angle))
    _require(sp.trigsimp(point.dot(point) - 1) == 0, "sphere-surface")
    _require(sp.trigsimp(area_vector.dot(area_vector) - sp.sin(symbol) ** 2) == 0,
             "sphere-jacobian")
    _require(sp.simplify(vector.dot(point) - exponent) == 0, "sphere-exponent")
    _require(sp.simplify(rotation.T * rotation) == sp.eye(3), "sphere-orthogonality")
    _require(rotation.det() == 1, "sphere-orientation")
    _require(rotation.T * vector == sp.Matrix([0, 0, radius]), "sphere-axis")
    rotated = rotation * point
    _require(sp.simplify(vector.dot(rotated) - radius * sp.cos(symbol)) == 0,
             "sphere-rotated-exponent")
    rotated_area = rotated.diff(symbol).cross(rotated.diff(angle))
    _require(sp.trigsimp(rotated_area.dot(rotated_area) - sp.sin(symbol) ** 2) == 0,
             "sphere-rotated-jacobian")
    u = sp.Symbol("_sphere_u", real=True)
    _require(sp.diff(sp.cos(symbol), symbol) == -sp.sin(symbol), "sphere-substitution")
    _require(sp.cos(0) == 1 and sp.cos(sp.pi) == -1, "sphere-endpoints")
    value = 2 * sp.pi * sp.integrate(sp.exp(radius * u), (u, -1, 1))
    _require(not value.has(sp.Integral, sp.Sum, sp.Product, sp.Limit), "sphere-closed-value")
    return sp.simplify(value.rewrite(sp.sinh))


@lru_cache(maxsize=1)
def _tangent_ray_certificate():
    x = sp.Symbol("_x", real=True)
    y = sp.Symbol("_y", nonnegative=True)
    r = sp.Symbol("_r", nonnegative=True)
    c, s = sp.symbols("_c _s", real=True)
    z, q = sp.symbols("_z _q")
    fun = (1 + sp.I * q) / (z + 2 * sp.I + sp.I * z * q)
    boundary = fun.subs({z: x, q: sp.exp(sp.I * x)})
    target = sp.cos(x)**2 / (
        sp.cos(x)**2 + (x * sp.cos(x) + sp.sin(x) + 1)**2
    )
    _require(
        sp.trigsimp(sp.together(-sp.im(sp.expand_complex(boundary)) - target)) == 0,
        "real-boundary-integrand",
    )

    real_z = x + sp.I * y
    phase = r * (c + sp.I * s)
    gap = sp.expand(
        (real_z + 2 * sp.I) * sp.conjugate(real_z + 2 * sp.I)
        - sp.I * real_z * phase * sp.conjugate(sp.I * real_z * phase)
    )
    positive_gap = (x**2 + y**2) * (1 - r**2) + 4 * y + 4
    _require(
        sp.rem(gap - positive_gap, c**2 + s**2 - 1, c) == 0,
        "no-pole-norm-gap",
    )
    upper = sp.Symbol("_upper", nonnegative=True)
    _require(
        sp.factor(positive_gap.subs(r**2, 1 / (1 + upper))).is_positive is True,
        "no-pole-positive",
    )
    decay = sp.exp(-2 * y)
    _require(decay.subs(y, 0) == 1 and (-sp.diff(decay, y)).is_positive is True,
             "upper-half-plane-modulus")
    _require(
        sp.simplify(sp.exp(sp.I * real_z) * sp.conjugate(sp.exp(sp.I * real_z)) - decay) == 0,
        "exponential-modulus",
    )

    shift = 2 * sp.I / (1 + sp.I * q)
    _require(sp.cancel(fun - 1 / (z + shift)) == 0, "contour-rewrite")
    _require(
        sp.cancel(fun - 1 / z + shift / (z * (z + shift))) == 0,
        "contour-error-identity",
    )
    n = sp.Symbol("_n", integer=True, positive=True)
    _require(sp.exp(2 * sp.pi * sp.I * n) == 1, "vertical-phase")
    vertical_shift = shift.subs(q, r)
    squared_shift = sp.simplify(vertical_shift * sp.conjugate(vertical_shift))
    _require(sp.simplify(squared_shift - 4 / (1 + r**2)) == 0,
             "vertical-modulus")
    _require(sp.factor(4 - squared_shift).is_nonnegative is True,
             "vertical-bound")
    _require(sp.exp(-2 * sp.pi) < sp.Rational(1, 3), "top-decay")
    top_bound = 2 / (1 - sp.Rational(1, 3))
    _require(top_bound == 3 and 2 * sp.pi > top_bound, "top-bound")

    radius = sp.Symbol("_R", positive=True)
    error_bound = 4 * radius * top_bound / (radius * (radius - top_bound))
    _require(sp.limit(error_bound, radius, sp.oo) == 0, "contour-error-limit")
    t = sp.Symbol("_t", real=True)
    contour = (
        sp.integrate(sp.I / (1 + sp.I * t), (t, 0, 1))
        + sp.integrate(1 / (t + sp.I), (t, 1, -1))
        + sp.integrate(sp.I / (-1 + sp.I * t), (t, 1, 0))
    )
    _require(sp.simplify(contour + sp.conjugate(contour)) == 0,
             "imaginary-contour")
    return sp.simplify(sp.im(contour))


def tangent_ray_value(integrand, symbol, lo, hi):
    """Evaluate the original cosine-square ratio on the whole real line."""
    if lo != -sp.oo or hi != sp.oo:
        return None
    target = sp.cos(symbol)**2 / (
        sp.cos(symbol)**2 + (symbol * sp.cos(symbol) + sp.sin(symbol) + 1)**2
    )
    if integrand != target:
        return None
    return _tangent_ray_certificate()



def _grid_factor(expr, variable):
    if not isinstance(expr, sp.Sum) or len(expr.limits) != 1:
        return None
    step, start, stop = expr.limits[0]
    if not isinstance(step, sp.Symbol) or start != 0:
        return None
    if not isinstance(expr.function, sp.Pow):
        return None
    base, degree = expr.function.as_base_exp()
    if len(degree.free_symbols) != 1:
        return None
    index = next(iter(degree.free_symbols))
    if index in (variable, step) or step == variable or index.is_integer is not True or index.is_positive is not True:
        return None
    count = sp.expand(stop + 1)
    degree_shift = sp.expand(degree - index)
    count_shift = sp.expand(count - index)
    if not (degree_shift.is_Integer and count_shift.is_Integer):
        return None
    if degree.is_nonnegative is not True or (count - degree).is_positive is not True:
        return None
    expected = variable + sp.sqrt(variable**2 - 1) * sp.cos(2 * sp.pi * step / count)
    if base != expected:
        return None
    return index, degree_shift, count_shift


def _grid_product(expr, variable):
    if isinstance(expr, sp.Pow) and expr.exp == 2 and isinstance(expr.base, sp.Sum):
        factors = (expr.base, expr.base)
    elif isinstance(expr, sp.Mul) and len(expr.args) == 2:
        factors = expr.args
    else:
        return None
    parsed = [_grid_factor(factor, variable) for factor in factors]
    if any(item is None for item in parsed):
        return None
    first, second = parsed
    if first[1:] != second[1:]:
        return None
    return tuple(sorted(parsed, key=lambda item: sp.default_sort_key(item[0])))


def matches_legendre_grid(integrand, variable) -> bool:
    """Admit only two explicitly finite grids of non-aliased integer powers."""
    return _grid_product(integrand, variable) is not None


def _require_zero(expr):
    if sp.simplify(expr) != 0:
        raise ArithmeticError("Legendre grid certificate failed")


@lru_cache(maxsize=1)
def _legendre_grid_certificate() -> bool:
    """Check the algebraic identities in the all-degree proof, not sample degrees."""
    x, t, v = sp.symbols("_x _t _v", real=True)
    j, r = sp.symbols("_j _r", integer=True, nonnegative=True)
    d, size = sp.symbols("_d _size", integer=True, positive=True)
    mode = sp.Symbol("_mode", integer=True)

    # Nonconstant Fourier modes vanish by finite geometric summation. The
    # matcher proves degree < grid size, excluding nonzero aliased modes.
    root = sp.exp(2 * sp.pi * sp.I * mode / size)
    _require_zero(root**size - 1)
    q = sp.Symbol("_q", nonzero=True)
    _require_zero(q ** (j + 1) - q**j - (q - 1) * q**j)

    # Constant Laurent coefficients of cos(theta)^(2j) are central binomials.
    # Their recurrence uniquely identifies the analytic series near v = 0.
    coefficient = sp.factorial(2 * j) / (4**j * sp.factorial(j) ** 2)
    next_coefficient = coefficient.subs(j, j + 1)
    _require_zero((j + 1) * next_coefficient - (j + sp.Rational(1, 2)) * coefficient)
    _require_zero(coefficient.subs(j, 0) - 1)
    central_series = (1 - v) ** (-sp.Rational(1, 2))
    _require_zero((1 - v) * sp.diff(central_series, v) - central_series / 2)
    _require_zero(central_series.subs(v, 0) - 1)
    _require_zero(
        sp.binomial(d, 2 * j) * sp.binomial(2 * j, j) / 4**j
        - sp.factorial(d) / (4**j * sp.factorial(j) ** 2 * sp.factorial(d - 2 * j))
    )
    power_coefficient = sp.factorial(r + 2 * j) / (sp.factorial(r) * sp.factorial(2 * j))
    _require_zero(
        (r + 1) * power_coefficient.subs(r, r + 1) - (r + 2 * j + 1) * power_coefficient
    )
    _require_zero(power_coefficient.subs(r, 0) - 1)
    power_series = (1 - v) ** (-2 * j - 1)
    _require_zero((1 - v) * sp.diff(power_series, v) - (2 * j + 1) * power_series)
    _require_zero(power_series.subs(v, 0) - 1)
    series_argument = t**2 * (x**2 - 1) / (1 - x * t) ** 2
    _require_zero((1 - x * t) ** 2 * (1 - series_argument) - (1 - 2 * x * t + t**2))

    # The generated polynomials obey a self-adjoint differential equation and
    # three-term recurrence, which establish orthogonality and every norm.
    generating = (1 - 2 * x * t + t**2) ** (-sp.Rational(1, 2))
    _require_zero(generating.subs(t, 0) - 1)
    _require_zero(sp.diff(generating, t).subs(t, 0) - x)
    _require_zero(
        sp.diff((1 - x**2) * sp.diff(generating, x), x)
        + t**2 * sp.diff(generating, t, 2) + 2 * t * sp.diff(generating, t)
    )
    _require_zero(
        (1 - 2 * x * t + t**2) * sp.diff(generating, t) - (x - t) * generating
    )
    left, right = sp.Function("_left")(x), sp.Function("_right")(x)
    boundary = (1 - x**2) * (left * sp.diff(right, x) - right * sp.diff(left, x))
    _require_zero(
        left * sp.diff((1 - x**2) * sp.diff(right, x), x)
        - right * sp.diff((1 - x**2) * sp.diff(left, x), x)
        - sp.diff(boundary, x)
    )
    _require_zero((1 - x**2).subs(x, -1))
    _require_zero((1 - x**2).subs(x, 1))
    _require_zero(d * (d + 1) - r * (r + 1) - (d - r) * (d + r + 1))
    norm = 2 / (2 * d + 1)
    _require_zero(d * norm / (2 * d - 1) - d * norm.subs(d, d - 1) / (2 * d + 1))
    _require_zero(norm.subs(d, 0) - sp.integrate(sp.Integer(1), (x, -1, 1)))
    return True


def legendre_grid_value(integrand, variable, lo, hi):
    """Evaluate the original finite-sum product using the checked certificate."""
    if lo != -1 or hi != 1:
        return None
    grids = _grid_product(integrand, variable)
    if grids is None:
        return None
    _legendre_grid_certificate()
    (m, degree_shift, count_shift), (n, _, _) = grids
    diagonal = 2 * (n + count_shift) ** 2 / (2 * (n + degree_shift) + 1)
    return sp.Piecewise((diagonal, sp.Eq(m, n)), (0, True))
