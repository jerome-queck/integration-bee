"""Exact certificates for lane L8 of the Yang guide.

Each checker matches one printed integrand and its endpoints, then returns a
value only after SymPy has checked the identities in the reduction. A shape
miss returns None before any of that work. Numeric agreement is not used.
"""

from __future__ import annotations

import sympy as sp


def definite_value(integrand, symbol, lo, hi):
    """Return a checked L8 value, or None when the shape is not one of these."""
    if getattr(symbol, "name", None) != "x" or symbol.is_real is not True:
        return None
    for checker in (
        _nested_radical_line,
        _arcsin_log_segment,
        _hyperbolic_arctangent,
        _exponential_arcsecant,
        _sqrt_linear_fraction,
        _arctangent_complement,
        _fourth_root_arcsecant,
        _exponential_arctangent,
        _triple_angle_arctangent,
        _composed_exponential_fraction,
    ):
        value = checker(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None


def _is_zero(expr) -> bool:
    try:
        return sp.simplify(expr) == 0
    except Exception:
        return False


def _no_zero(expr, var, lo, hi) -> bool:
    try:
        return sp.solveset(expr, var, sp.Interval.open(lo, hi)) == sp.EmptySet
    except Exception:
        return False


def _positive_on(expr, var, lo, hi) -> bool:
    if not _no_zero(expr, var, lo, hi):
        return False
    value = sp.simplify(expr.subs(var, (lo + hi) / 2))
    return value.is_positive is True


def _nested_radical_line(integrand, x, lo, hi):
    """∫_0^∞ sqrt(1+sqrt(1+x**2))/(1+x**2) dx = pi.

    x = tan θ carries the integral to ∫_0^{π/2} sqrt(1+sec θ) dθ. The
    half-angle substitution then reduces that to ∫_0^{π/2} 2 dφ.
    """
    target = sp.sqrt(1 + sp.sqrt(1 + x**2)) / (1 + x**2)
    if integrand != target or lo != 0 or hi != sp.oo:
        return None
    th = sp.Dummy("th", real=True)
    if not _positive_on(sp.cos(th), th, 0, sp.pi / 2):
        return None
    if not _positive_on(sp.cos(th / 2), th, 0, sp.pi / 2):
        return None
    den = 1 + sp.tan(th) ** 2
    if not _is_zero(den - sp.sec(th) ** 2):
        return None
    if not _is_zero(sp.diff(sp.tan(th), th) - sp.sec(th) ** 2):
        return None
    num = sp.sqrt(1 + sp.sqrt(den))
    pulled = num / den * sp.sec(th) ** 2
    if not _is_zero(pulled - num):
        return None
    if not _is_zero(sp.sqrt(den) - sp.sqrt(sp.sec(th) ** 2)):
        return None
    if not _is_zero(sp.sqrt(sp.sec(th) ** 2) - sp.Abs(sp.sec(th))):
        return None
    # sec θ > 0 on (0, π/2), so sqrt(1+tan**2 θ) = sec θ and the
    # substituted integrand is sqrt(1+sec θ).
    if not _is_zero(1 + sp.sec(th) - (1 + sp.cos(th)) / sp.cos(th)):
        return None
    adjacent = 1 + sp.cos(th)
    cosine = sp.cos(th)
    root = sp.sqrt(adjacent) / sp.sqrt(cosine)
    if not _is_zero(root**2 - adjacent / cosine):
        return None
    if not _is_zero(adjacent - 2 * sp.cos(th / 2) ** 2):
        return None
    if not _is_zero(sp.sqrt(2 * sp.cos(th / 2) ** 2) - sp.sqrt(2) * sp.Abs(sp.cos(th / 2))):
        return None
    if not _is_zero(cosine - (1 - 2 * sp.sin(th / 2) ** 2)):
        return None
    # u = sin(θ/2) runs from 0 to sin(π/4) = √2/2, and
    # sqrt(1+sec θ) dθ = 2√2 du / sqrt(1-2u**2).
    if not _is_zero(sp.sin(sp.pi / 4) - sp.sqrt(2) / 2):
        return None
    if not _is_zero(sp.diff(sp.sin(th / 2), th) - sp.cos(th / 2) / 2):
        return None
    phi = sp.Dummy("phi", real=True)
    if not _positive_on(sp.cos(phi), phi, 0, sp.pi / 2):
        return None
    if not _is_zero(1 - 2 * (sp.sin(phi) / sp.sqrt(2)) ** 2 - sp.cos(phi) ** 2):
        return None
    if not _is_zero(sp.sqrt(sp.cos(phi) ** 2) - sp.Abs(sp.cos(phi))):
        return None
    if not _is_zero(sp.diff(sp.sin(phi) / sp.sqrt(2), phi) - sp.cos(phi) / sp.sqrt(2)):
        return None
    if not _is_zero(2 * sp.sqrt(2) / sp.sqrt(2) - 2):
        return None
    if sp.sin(0) != 0 or not _is_zero(sp.sin(sp.pi / 2) - 1):
        return None
    reduced = sp.integrate(2, (phi, 0, sp.pi / 2))
    if reduced != sp.pi:
        return None
    return reduced


def _arcsin_log_segment(integrand, x, lo, hi):
    """∫_0^1 (1-x)/(asin(x)sqrt(1-x**2)+1-x**2) dx = log(pi/2)."""
    target = (1 - x) / (sp.asin(x) * sp.sqrt(1 - x**2) + 1 - x**2)
    if integrand != target or lo != 0 or hi != 1:
        return None
    primitive = sp.log(sp.asin(x) + sp.sqrt(1 - x**2))
    if not _is_zero(sp.diff(primitive, x) - integrand):
        return None
    value = sp.simplify(primitive.subs(x, 1) - primitive.subs(x, 0))
    if not _is_zero(value - sp.log(sp.pi / 2)):
        return None
    return value


def _hyperbolic_arctangent(integrand, x, lo, hi):
    """∫_0^∞ atan(x)/((sqrt(1+x**2)+x)sqrt(1+x**2)) dx = log(2).

    x = sinh u turns the integrand into e^{-u} atan(sinh u). Integration by
    parts leaves ∫ e^{-u}/cosh(u) du, and t = e^{-2u} turns that into
    ∫_0^1 dt/(1+t).
    """
    target = sp.atan(x) / ((sp.sqrt(1 + x**2) + x) * sp.sqrt(1 + x**2))
    if integrand != target or lo != 0 or hi != sp.oo:
        return None
    u = sp.Dummy("u", positive=True)
    if not _is_zero(sp.diff(sp.sinh(u), u) - sp.cosh(u)):
        return None
    if not _is_zero(sp.sqrt(1 + sp.sinh(u) ** 2) - sp.cosh(u)):
        return None
    if not _is_zero(sp.cosh(u) + sp.sinh(u) - sp.exp(u)):
        return None
    substituted = integrand.subs(x, sp.sinh(u)) * sp.cosh(u)
    reduced = sp.atan(sp.sinh(u)) * sp.exp(-u)
    if not _is_zero(substituted - reduced):
        return None
    boundary = -sp.exp(-u) * sp.atan(sp.sinh(u))
    remainder = sp.exp(-u) / sp.cosh(u)
    if not _is_zero(reduced - (sp.diff(boundary, u) + remainder)):
        return None
    if sp.limit(boundary, u, sp.oo) != 0 or sp.simplify(boundary.subs(u, 0)) != 0:
        return None
    rational = 2 * sp.exp(-2 * u) / (1 + sp.exp(-2 * u))
    if not _is_zero(remainder.rewrite(sp.exp) - rational):
        return None
    t = sp.Dummy("t", positive=True)
    if not _is_zero(sp.diff(sp.exp(-2 * u), u) + 2 * sp.exp(-2 * u)):
        return None
    # t = e^{-2u} runs from 1 down to 0, and the minus sign from dt reverses it.
    if sp.simplify(sp.exp(-2 * u).subs(u, 0)) != 1:
        return None
    if sp.limit(sp.exp(-2 * u), u, sp.oo) != 0:
        return None
    value = sp.integrate(1 / (1 + t), (t, 0, 1))
    if not _is_zero(value - sp.log(2)):
        return None
    return value


def _exponential_arcsecant(integrand, x, lo, hi):
    """∫_1^{√2} exp(asec(x)) sqrt(x**2-1) dx = 1/2."""
    target = sp.exp(sp.asec(x)) * sp.sqrt(x**2 - 1)
    if integrand != target or lo != 1 or hi != sp.sqrt(2):
        return None
    positive = sp.Dummy("p", positive=True)
    primitive = sp.exp(sp.asec(positive)) * positive * (sp.sqrt(positive**2 - 1) - 1) / 2
    if not _is_zero(sp.diff(primitive, positive) - target.subs(x, positive)):
        return None
    value = sp.simplify(primitive.subs(positive, sp.sqrt(2)) - primitive.subs(positive, 1))
    if value != sp.Rational(1, 2):
        return None
    return value


def _sqrt_linear_fraction(integrand, x, lo, hi):
    """∫_0^1 dx/((1+sqrt(x))sqrt(x-x**2)) = 2."""
    target = 1 / ((1 + sp.sqrt(x)) * sp.sqrt(x - x**2))
    if integrand != target or lo != 0 or hi != 1:
        return None
    positive = sp.Dummy("p", positive=True)
    primitive = 2 * (sp.sqrt(positive) - 1) / sp.sqrt(1 - positive)
    if not _is_zero(sp.diff(primitive, positive) - target.subs(x, positive)):
        return None
    upper = sp.limit(primitive, positive, 1, dir="-")
    lower = sp.simplify(primitive.subs(positive, 0))
    if upper != 0 or lower != -2:
        return None
    return sp.simplify(upper - lower)


def _arctangent_complement(integrand, x, lo, hi):
    """∫_0^1 dx/((1+x**2)sqrt(1-x**2)) = pi/(2*sqrt(2)).

    The antiderivative's two-sided limit at 1 is the negative of the left-hand
    limit, so the evaluation uses dir='-'.
    """
    target = 1 / ((1 + x**2) * sp.sqrt(1 - x**2))
    if integrand != target or lo != 0 or hi != 1:
        return None
    primitive = sp.atan(sp.sqrt(2) * x / sp.sqrt(1 - x**2)) / sp.sqrt(2)
    if not _is_zero(sp.diff(primitive, x) - integrand):
        return None
    upper = sp.limit(primitive, x, 1, dir="-")
    lower = sp.simplify(primitive.subs(x, 0))
    if lower != 0:
        return None
    value = sp.simplify(upper - lower)
    if not _is_zero(value - sp.pi / (2 * sp.sqrt(2))):
        return None
    return value


def _fourth_root_arcsecant(integrand, x, lo, hi):
    """∫_1^4 asec(x**(1/4)) dx = pi - 4/3.

    t = x**(1/4) and integration by parts leave ∫_1^{√2} t**3/sqrt(t**2-1) dt.
    t = sec θ on (0, π/4), where tan θ > 0, turns that into ∫_0^1 (1+w**2) dw.
    """
    target = sp.asec(x ** sp.Rational(1, 4))
    if integrand != target or lo != 1 or hi != 4:
        return None
    if sp.simplify(sp.Integer(4) ** sp.Rational(1, 4)) != sp.sqrt(2):
        return None
    t = sp.Dummy("t", positive=True)
    if not _is_zero(sp.diff(t**4, t) - 4 * t**3):
        return None
    parts = t**4 * sp.asec(t)
    extra = t**3 / sp.sqrt(t**2 - 1)
    if not _is_zero(sp.diff(parts, t) - (4 * t**3 * sp.asec(t) + extra)):
        return None
    boundary = sp.simplify(parts.subs(t, sp.sqrt(2)) - parts.subs(t, 1))
    if boundary != sp.pi:
        return None
    th = sp.Dummy("th", real=True)
    if not _positive_on(sp.sin(th), th, 0, sp.pi / 4):
        return None
    if not _positive_on(sp.cos(th), th, 0, sp.pi / 4):
        return None
    substituted = sp.simplify((extra * sp.diff(sp.sec(th), th)).subs(t, sp.sec(th)))
    if not _is_zero(substituted - sp.tan(th) * sp.sec(th) ** 4 / sp.Abs(sp.tan(th))):
        return None
    if not _is_zero(sp.sec(th) ** 4 - sp.sec(th) ** 2 * (1 + sp.tan(th) ** 2)):
        return None
    if not _is_zero(sp.diff(sp.tan(th), th) - sp.sec(th) ** 2):
        return None
    if sp.tan(0) != 0 or not _is_zero(sp.tan(sp.pi / 4) - 1):
        return None
    w = sp.Dummy("w", real=True)
    remainder = sp.integrate(1 + w**2, (w, 0, 1))
    if remainder != sp.Rational(4, 3):
        return None
    return sp.simplify(boundary - remainder)


def _exponential_arctangent(integrand, x, lo, hi):
    """∫_0^∞ dx/(e**x + e**(-(x+1))) = sqrt(E)*(pi/2 - atan(sqrt(E)))."""
    target = 1 / (sp.exp(x) + sp.exp(-(x + 1)))
    if integrand != target or lo != 0 or hi != sp.oo:
        return None
    primitive = sp.sqrt(sp.E) * sp.atan(sp.exp(x) * sp.sqrt(sp.E))
    if not _is_zero(sp.diff(primitive, x) - integrand):
        return None
    upper = sp.limit(primitive, x, sp.oo)
    lower = primitive.subs(x, 0)
    value = sp.simplify(upper - lower)
    if not _is_zero(value - sp.sqrt(sp.E) * (sp.pi / 2 - sp.atan(sp.sqrt(sp.E)))):
        return None
    return value


def _triple_angle_arctangent(integrand, x, lo, hi):
    """∫_0^{√3} atan((3x-x**3)/(1-3x**2)) dx = pi/sqrt(3) - log(8).

    x = tan θ. atan(tan(3θ)) equals 3θ on [0, π/6) and 3θ-π on (π/6, π/3].
    Direct integration of the original integrand drops the jump.
    """
    target = sp.atan((3 * x - x**3) / (1 - 3 * x**2))
    if integrand != target or lo != 0 or hi != sp.sqrt(3):
        return None
    th = sp.Dummy("th", real=True)
    if not _is_zero(sp.diff(sp.tan(th), th) - sp.sec(th) ** 2):
        return None
    if not _is_zero(sp.tan(sp.pi / 3) - sp.sqrt(3)):
        return None
    argument = ((3 * x - x**3) / (1 - 3 * x**2)).subs(x, sp.tan(th))
    if not _is_zero(sp.expand_trig(argument - sp.tan(3 * th))):
        return None
    y = sp.Dummy("y", real=True)
    if not _is_zero(sp.diff(sp.atan(sp.tan(y)), y) - 1):
        return None
    if sp.solveset(sp.cos(y), y, sp.Interval.Ropen(0, sp.pi / 2)) != sp.EmptySet:
        return None
    if not _is_zero(sp.atan(sp.tan(sp.pi / 4)) - sp.pi / 4):
        return None
    if sp.solveset(sp.cos(y), y, sp.Interval.Lopen(sp.pi / 2, sp.pi)) != sp.EmptySet:
        return None
    if not _is_zero(sp.atan(sp.tan(3 * sp.pi / 4)) - (3 * sp.pi / 4 - sp.pi)):
        return None
    if not _positive_on(sp.cos(th), th, 0, sp.pi / 3):
        return None
    left = 3 * th * sp.tan(th) + 3 * sp.log(sp.cos(th))
    right = (3 * th - sp.pi) * sp.tan(th) + 3 * sp.log(sp.cos(th))
    if not _is_zero(sp.diff(left, th) - 3 * th * sp.sec(th) ** 2):
        return None
    if not _is_zero(sp.diff(right, th) - (3 * th - sp.pi) * sp.sec(th) ** 2):
        return None
    if sp.simplify(left.subs(th, 0)) != 0:
        return None
    first = sp.simplify(left.subs(th, sp.pi / 6) - left.subs(th, 0))
    second = sp.simplify(right.subs(th, sp.pi / 3) - right.subs(th, sp.pi / 6))
    value = sp.simplify(first + second)
    if not _is_zero(value - (sp.pi / sp.sqrt(3) - sp.log(8))):
        return None
    return value


def _composed_exponential_fraction(integrand, x, lo, hi):
    """∫_{1/4}^{3/4} f(f(x)) dx = 1/4 for f(t) = 4**t/(2+4**t).

    f(z)+f(1-z) is identically 1, so f(f(x))+f(f(1-x)) is identically 1.
    The interval is symmetric under x -> 1-x, and the two copies of the
    integral are equal.
    """
    if lo != sp.Rational(1, 4) or hi != sp.Rational(3, 4):
        return None

    def f(argument):
        return 4**argument / (2 + 4**argument)

    if integrand != f(f(x)):
        return None
    z = sp.Dummy("z", real=True)
    if sp.cancel(sp.together(f(z) + f(1 - z) - 1)) != 0:
        return None
    if sp.cancel(sp.together(1 - f(x) - f(1 - x))) != 0:
        return None
    piece = f(f(x)) + f(1 - f(x)) - 1
    if sp.cancel(sp.together(piece)) != 0:
        return None
    if not _is_zero(f(f(1 - x)) - f(1 - f(x))):
        return None
    if not _is_zero(integrand.subs(x, 1 - x) - f(f(1 - x))):
        return None
    if sp.diff(1 - x, x) != -1:
        return None
    if not _is_zero((1 - lo) - hi) or not _is_zero((1 - hi) - lo):
        return None
    length = sp.simplify(hi - lo)
    if length != sp.Rational(1, 2):
        return None
    return length / 2
