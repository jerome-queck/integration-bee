#!/usr/bin/env python3
"""Re-check the worked steps for Yang sections 2.7, 3.4, 3.8, 4.4, 4.6, 6.1, and 6.7.

Each function names the substitution or trick in the catalog writeup and checks
that step with SymPy. A definite value has to equal answer_sympy. An indefinite
antiderivative has to differentiate back to the integrand. Numeric agreement is
not used. Run from the repository root:

    python3 verify/yang_worked_steps.py
"""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp

import pack_gate

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"

# Section order, then problem order. This is the whole derived-writeup batch.
IDS = (
    "YANG-2.7-P01",
    "YANG-2.7-P02",
    "YANG-2.7-P03",
    "YANG-2.7-P04",
    "YANG-2.7-P05",
    "YANG-2.7-P06",
    "YANG-2.7-P07",
    "YANG-2.7-P08",
    "YANG-2.7-P09",
    "YANG-2.7-P10",
    "YANG-2.7-P11",
    "YANG-2.7-P12",
    "YANG-2.7-P13",
    "YANG-3.4-P06",
    "YANG-3.8-P01",
    "YANG-3.8-P02",
    "YANG-3.8-P03",
    "YANG-3.8-P04",
    "YANG-3.8-P05",
    "YANG-3.8-P06",
    "YANG-3.8-P07",
    "YANG-3.8-P08",
    "YANG-3.8-P09",
    "YANG-3.8-P10",
    "YANG-3.8-P11",
    "YANG-3.8-P12",
    "YANG-3.8-P13",
    "YANG-3.8-P14",
    "YANG-4.4-P01",
    "YANG-4.6-P04",
    "YANG-6.1-P04",
    "YANG-6.7-P03",
)


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def _is_zero(expr) -> bool:
    try:
        return sp.simplify(expr) == 0
    except Exception:
        return False


def same(left, right, label):
    require(_is_zero(left - right), label)


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


def integrand_of(row):
    return pack_gate._parse(row["sympy_expr"], "x")


def answer_of(row):
    return pack_gate._parse(row["answer_sympy"], "x")


def require_answer(value, row, label):
    answer = answer_of(row)
    if not _is_zero(sp.simplify(value) - answer) and not _is_zero(value - answer):
        raise AssertionError(f"{row['id']} derivation disagrees with stored answer: {value} vs {answer}")
    require(label, label)


def _abs_positive():
    positive = sp.Dummy("p", positive=True)
    same(sp.Abs(positive), positive, "absolute value of a positive quantity")


def check_2_7_p01(row, x):
    """Sine substitution for x/((1-x) sqrt(1-x**2))."""
    require(row["kind"] == "indefinite" and row["limits"] == [], row["id"] + " shape")
    integrand = integrand_of(row)
    th = sp.symbols("th", real=True)
    same(sp.sqrt(1 - sp.sin(th) ** 2), sp.Abs(sp.cos(th)), row["id"] + " square root")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 2), row["id"] + " cosine sign")
    _abs_positive()
    linked = sp.sin(th) / ((1 - sp.sin(th)) * sp.cos(th)) * sp.cos(th)
    same(sp.cancel(linked - sp.sin(th) / (1 - sp.sin(th))), 0, row["id"] + " jacobian")
    rewritten = -1 + sp.sec(th) ** 2 + sp.sec(th) * sp.tan(th)
    same(sp.together(sp.sin(th) / (1 - sp.sin(th)) - rewritten), 0, row["id"] + " rationalization")
    theta_form = -th + sp.tan(th) + sp.sec(th)
    same(sp.diff(theta_form, th), rewritten, row["id"] + " theta antiderivative")
    answer = answer_of(row)
    same(sp.diff(answer, x), integrand, row["id"] + " x antiderivative")
    same((1 + x) / sp.sqrt(1 - x**2), answer + sp.asin(x), row["id"] + " back substitution")


def check_2_7_p02(row, x):
    """Sine substitution for x**2/(1-x**2)**(3/2) on [0, 1/2]."""
    require(row["limits"] == ["0", "1/2"], row["id"] + " limits")
    integrand = integrand_of(row)
    th = sp.symbols("th", real=True)
    same(sp.sqrt(1 - sp.sin(th) ** 2), sp.Abs(sp.cos(th)), row["id"] + " square root")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 6), row["id"] + " cosine sign")
    manual = sp.sin(th) ** 2 / sp.cos(th) ** 2
    same(manual, sp.tan(th) ** 2, row["id"] + " tangent square")
    same(sp.tan(th) ** 2, sp.sec(th) ** 2 - 1, row["id"] + " pythagorean")
    antideriv = sp.tan(th) - th
    same(sp.diff(antideriv, th), sp.sec(th) ** 2 - 1, row["id"] + " antiderivative")
    value = sp.simplify(antideriv.subs(th, sp.pi / 6) - antideriv.subs(th, 0))
    same(value, sp.sqrt(3) / 3 - sp.pi / 6, row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")
    # The stored integrand, after x = sin(theta) and sqrt(1-sin**2) = cos(theta), is tan(theta)**2.
    replaced = integrand.subs(x, sp.sin(th)).subs(sp.sqrt(1 - sp.sin(th) ** 2), sp.cos(th))
    same(sp.simplify(replaced * sp.cos(th) - sp.tan(th) ** 2), 0, row["id"] + " substituted integrand")


def check_2_7_p03(row, x):
    """Cosine substitution for asin(sqrt(1-x**2)) on [-1, 1]."""
    require(row["limits"] == ["-1", "1"], row["id"] + " limits")
    th = sp.symbols("th", real=True)
    same(sp.sqrt(sp.sin(th) ** 2), sp.Abs(sp.sin(th)), row["id"] + " square root")
    require(_positive_on(sp.sin(th), th, 0, sp.pi), row["id"] + " sine sign")
    _abs_positive()
    branch = sp.asin(sp.sin(th))
    deriv = sp.simplify(sp.diff(branch, th))
    same(deriv, sp.cos(th) / sp.Abs(sp.cos(th)), row["id"] + " arcsine derivative")
    same(sp.sqrt(sp.cos(th) ** 2), sp.Abs(sp.cos(th)), row["id"] + " cosine root")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 2), row["id"] + " first cosine sign")
    same(deriv.subs(sp.Abs(sp.cos(th)), sp.cos(th)), 1, row["id"] + " derivative on the first half")
    require(branch.subs(th, 0) == 0, row["id"] + " arcsine at 0")
    require(_positive_on(-sp.cos(th), th, sp.pi / 2, sp.pi), row["id"] + " second cosine sign")
    same(deriv.subs(sp.Abs(sp.cos(th)), -sp.cos(th)), -1, row["id"] + " derivative on the second half")
    same(sp.diff(sp.pi - th, th), -1, row["id"] + " reflected angle")
    require(sp.simplify(branch.subs(th, sp.pi / 2) - sp.pi / 2) == 0, row["id"] + " arcsine at pi/2")
    piece = -th * sp.cos(th) + sp.sin(th)
    same(sp.diff(piece, th), th * sp.sin(th), row["id"] + " first antiderivative")
    first = sp.simplify(piece.subs(th, sp.pi / 2) - piece.subs(th, 0))
    require(first == 1, row["id"] + " first piece")
    other = -(sp.pi - th) * sp.cos(th) - sp.sin(th)
    same(sp.diff(other, th), (sp.pi - th) * sp.sin(th), row["id"] + " second antiderivative")
    second = sp.simplify(other.subs(th, sp.pi) - other.subs(th, sp.pi / 2))
    require(second == 1, row["id"] + " second piece")
    require_answer(first + second, row, row["id"] + " stored value")


def check_2_7_p04(row, x):
    """Sine substitution for atan(x/sqrt(1-x**2)) on [0, 1]."""
    require(row["limits"] == ["0", "1"], row["id"] + " limits")
    th = sp.symbols("th", real=True)
    same(sp.sqrt(1 - sp.sin(th) ** 2), sp.Abs(sp.cos(th)), row["id"] + " square root")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 2), row["id"] + " cosine sign")
    _abs_positive()
    branch = sp.atan(sp.tan(th))
    same(sp.diff(branch, th), 1, row["id"] + " arctangent derivative")
    require(branch.subs(th, 0) == 0, row["id"] + " arctangent at 0")
    antideriv = th * sp.sin(th) + sp.cos(th)
    same(sp.diff(antideriv, th), th * sp.cos(th), row["id"] + " antiderivative")
    value = sp.simplify(antideriv.subs(th, sp.pi / 2) - antideriv.subs(th, 0))
    same(value, sp.pi / 2 - 1, row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p05(row, x):
    """Tangent substitution for sqrt(1+sqrt(1+x**2))/(1+x**2) on [0, infinity)."""
    require(row["limits"] == ["0", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    th = sp.symbols("th", real=True)
    same(1 + sp.tan(th) ** 2, sp.sec(th) ** 2, row["id"] + " pythagorean")
    same(sp.diff(sp.tan(th), th), sp.sec(th) ** 2, row["id"] + " tangent derivative")
    same(sp.sqrt(sp.sec(th) ** 2), sp.Abs(sp.sec(th)), row["id"] + " secant root")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 2), row["id"] + " cosine sign")
    _abs_positive()
    pulled = integrand.subs(x, sp.tan(th)) * sp.sec(th) ** 2
    reduced = pulled.subs(sp.sqrt(1 + sp.tan(th) ** 2), sp.sec(th))
    same(reduced, sp.sqrt(1 + sp.sec(th)), row["id"] + " substituted integrand")
    same(1 + sp.sec(th), (1 + sp.cos(th)) / sp.cos(th), row["id"] + " secant sum")
    same(1 + sp.cos(th), 2 * sp.cos(th / 2) ** 2, row["id"] + " half-angle cosine")
    same(sp.cos(th), 1 - 2 * sp.sin(th / 2) ** 2, row["id"] + " half-angle sine")
    require(_positive_on(sp.cos(th / 2), th, 0, sp.pi / 2), row["id"] + " half-angle sign")
    u_expr = sp.sin(th / 2)
    same(sp.diff(u_expr, th), sp.cos(th / 2) / 2, row["id"] + " u derivative")
    factor = sp.sqrt(2) * sp.cos(th / 2) / sp.sqrt(1 - 2 * u_expr**2) * (2 / sp.cos(th / 2))
    same(factor, 2 * sp.sqrt(2) / sp.sqrt(1 - 2 * u_expr**2), row["id"] + " half-angle factor")
    phi = sp.symbols("phi", real=True)
    same(1 - 2 * (sp.sin(phi) / sp.sqrt(2)) ** 2, sp.cos(phi) ** 2, row["id"] + " phi identity")
    require(_positive_on(sp.cos(phi), phi, 0, sp.pi / 2), row["id"] + " phi cosine")
    same(sp.sqrt(sp.cos(phi) ** 2), sp.Abs(sp.cos(phi)), row["id"] + " phi root")
    collapsed = 2 * sp.sqrt(2) * (sp.cos(phi) / sp.sqrt(2)) / sp.cos(phi)
    same(collapsed, 2, row["id"] + " collapsed integrand")
    same(sp.sin(sp.pi / 4), sp.sqrt(2) / 2, row["id"] + " upper u")
    value = sp.integrate(2, (phi, 0, sp.pi / 2))
    require(value == sp.pi, row["id"] + " reduced integral")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p06(row, x):
    """Logarithmic antiderivative on [0, 1]."""
    require(row["limits"] == ["0", "1"], row["id"] + " limits")
    integrand = integrand_of(row)
    factored = sp.sqrt(1 - x**2) * (sp.asin(x) + sp.sqrt(1 - x**2))
    denominator = -x**2 + sp.sqrt(1 - x**2) * sp.asin(x) + 1
    same(denominator, factored, row["id"] + " factor")
    primitive = sp.log(sp.asin(x) + sp.sqrt(1 - x**2))
    same(sp.diff(primitive, x), integrand, row["id"] + " derivative")
    value = sp.simplify(primitive.subs(x, 1) - primitive.subs(x, 0))
    same(value, sp.log(sp.pi / 2), row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p07(row, x):
    """Secant substitution on [sqrt(2), infinity)."""
    require(row["limits"] == ["sqrt(2)", "oo"], row["id"] + " limits")
    th = sp.symbols("th", real=True)
    same(sp.sqrt(sp.sec(th) ** 2 - 1), sp.Abs(sp.tan(th)), row["id"] + " square root")
    require(_positive_on(sp.tan(th), th, sp.pi / 4, sp.pi / 2), row["id"] + " tangent sign")
    _abs_positive()
    manual = 1 / (sp.sec(th) ** 2 * sp.tan(th) ** 3) * (sp.sec(th) * sp.tan(th))
    target = sp.cos(th) ** 3 / sp.sin(th) ** 2
    same(sp.simplify(manual - target), 0, row["id"] + " substituted integrand")
    rewritten = sp.cos(th) / sp.sin(th) ** 2 - sp.cos(th)
    same(target, rewritten, row["id"] + " split")
    antideriv = -sp.csc(th) - sp.sin(th)
    same(sp.diff(antideriv, th), rewritten, row["id"] + " antiderivative")
    value = sp.simplify(antideriv.subs(th, sp.pi / 2) - antideriv.subs(th, sp.pi / 4))
    same(value, -2 + 3 * sp.sqrt(2) / 2, row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p08(row, x):
    """Hyperbolic substitution for the arctangent weight on [0, infinity)."""
    require(row["limits"] == ["0", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    u = sp.symbols("u", positive=True)
    same(sp.diff(sp.sinh(u), u), sp.cosh(u), row["id"] + " sinh derivative")
    same(sp.sqrt(1 + sp.sinh(u) ** 2), sp.cosh(u), row["id"] + " hyperbolic root")
    same(sp.cosh(u) + sp.sinh(u), sp.exp(u), row["id"] + " exponential sum")
    substituted = integrand.subs(x, sp.sinh(u)) * sp.cosh(u)
    reduced = sp.atan(sp.sinh(u)) * sp.exp(-u)
    same(substituted, reduced, row["id"] + " substituted integrand")
    boundary = -sp.exp(-u) * sp.atan(sp.sinh(u))
    remainder = sp.exp(-u) / sp.cosh(u)
    same(reduced, sp.diff(boundary, u) + remainder, row["id"] + " integration by parts")
    require(sp.limit(boundary, u, sp.oo) == 0, row["id"] + " upper boundary")
    require(sp.simplify(boundary.subs(u, 0)) == 0, row["id"] + " lower boundary")
    rational = 2 * sp.exp(-2 * u) / (1 + sp.exp(-2 * u))
    same(remainder.rewrite(sp.exp), rational, row["id"] + " exponential form")
    t = sp.symbols("t", positive=True)
    same(sp.diff(sp.exp(-2 * u), u), -2 * sp.exp(-2 * u), row["id"] + " t derivative")
    require(sp.simplify(sp.exp(-2 * u).subs(u, 0)) == 1, row["id"] + " t at 0")
    require(sp.limit(sp.exp(-2 * u), u, sp.oo) == 0, row["id"] + " t at infinity")
    value = sp.integrate(1 / (1 + t), (t, 0, 1))
    same(value, sp.log(2), row["id"] + " reduced integral")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p09(row, x):
    """Differentiate the exponential arcsecant antiderivative on [1, sqrt(2)]."""
    require(row["limits"] == ["1", "sqrt(2)"], row["id"] + " limits")
    integrand = integrand_of(row)
    positive = sp.symbols("p", positive=True)
    primitive = sp.exp(sp.asec(positive)) * positive * (sp.sqrt(positive**2 - 1) - 1) / 2
    same(sp.diff(primitive, positive), integrand.subs(x, positive), row["id"] + " derivative")
    require(sp.asec(1) == 0, row["id"] + " arcsecant of 1")
    same(sp.asec(sp.sqrt(2)), sp.pi / 4, row["id"] + " arcsecant of sqrt(2)")
    value = sp.simplify(primitive.subs(positive, sp.sqrt(2)) - primitive.subs(positive, 1))
    require(value == sp.Rational(1, 2), row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p10(row, x):
    """Sine substitution for asin(sqrt(x))/sqrt(1-x) on [0, 1]."""
    require(row["limits"] == ["0", "1"], row["id"] + " limits")
    th = sp.symbols("th", real=True)
    same(sp.diff(sp.sin(th) ** 2, th), 2 * sp.sin(th) * sp.cos(th), row["id"] + " jacobian")
    same(sp.sqrt(sp.sin(th) ** 2), sp.Abs(sp.sin(th)), row["id"] + " sine root")
    same(sp.sqrt(sp.cos(th) ** 2), sp.Abs(sp.cos(th)), row["id"] + " cosine root")
    require(_positive_on(sp.sin(th), th, 0, sp.pi / 2), row["id"] + " sine sign")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 2), row["id"] + " cosine sign")
    _abs_positive()
    antideriv = -2 * th * sp.cos(th) + 2 * sp.sin(th)
    same(sp.diff(antideriv, th), 2 * th * sp.sin(th), row["id"] + " antiderivative")
    value = sp.simplify(antideriv.subs(th, sp.pi / 2) - antideriv.subs(th, 0))
    require(value == 2, row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p11(row, x):
    """Differentiate 2(sqrt(x)-1)/sqrt(1-x) on [0, 1]."""
    require(row["limits"] == ["0", "1"], row["id"] + " limits")
    integrand = integrand_of(row)
    positive = sp.symbols("p", positive=True)
    primitive = 2 * (sp.sqrt(positive) - 1) / sp.sqrt(1 - positive)
    same(sp.diff(primitive, positive), integrand.subs(x, positive), row["id"] + " derivative")
    upper = sp.limit(primitive, positive, 1, dir="-")
    lower = sp.simplify(primitive.subs(positive, 0))
    require(upper == 0 and lower == -2, row["id"] + " endpoints")
    require_answer(sp.simplify(upper - lower), row, row["id"] + " stored value")


def check_2_7_p12(row, x):
    """Two square roots, then an arctangent antiderivative, on [1, 4]."""
    require(row["limits"] == ["1", "4"], row["id"] + " limits")
    integrand = integrand_of(row)
    t = sp.symbols("t", positive=True)
    u = sp.symbols("u", positive=True)
    same(sp.diff(t**2, t), 2 * t, row["id"] + " t jacobian")
    first = integrand.subs(x, t**2) * (2 * t)
    same(sp.simplify(first - 2 * t * sp.atan(sp.sqrt(t - 1))), 0, row["id"] + " t integrand")
    same(sp.diff(u**2 + 1, u), 2 * u, row["id"] + " u jacobian")
    second = first.subs(t, u**2 + 1) * (2 * u)
    piece = u * (u**2 + 1) * sp.atan(u)
    same(sp.simplify(second - 4 * piece), 0, row["id"] + " u integrand")
    antideriv = sp.atan(u) * (u**4 / 4 + u**2 / 2) - u**3 / 12 - u / 4 + sp.atan(u) / 4
    same(sp.diff(antideriv, u), (u**3 + u) * sp.atan(u), row["id"] + " antiderivative")
    value = sp.simplify(4 * (antideriv.subs(u, 1) - antideriv.subs(u, 0)))
    same(value, sp.pi - sp.Rational(4, 3), row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_2_7_p13(row, x):
    """Arctangent antiderivative on [0, 1], using the left-hand limit at 1."""
    require(row["limits"] == ["0", "1"], row["id"] + " limits")
    integrand = integrand_of(row)
    primitive = sp.atan(sp.sqrt(2) * x / sp.sqrt(1 - x**2)) / sp.sqrt(2)
    same(sp.diff(primitive, x), integrand, row["id"] + " derivative")
    require(sp.simplify(primitive.subs(x, 0)) == 0, row["id"] + " lower endpoint")
    upper = sp.limit(primitive, x, 1, dir="-")
    same(upper, sp.pi / (2 * sp.sqrt(2)), row["id"] + " upper limit")
    same(upper, sp.sqrt(2) * sp.pi / 4, row["id"] + " equivalent form")
    require_answer(upper, row, row["id"] + " stored value")


def check_3_4_p06(row, x):
    """Triple-angle split. The guide prints pi/sqrt(3) - log(8)."""
    require(row["limits"] == ["0", "sqrt(3)"], row["id"] + " limits")
    th = sp.symbols("th", real=True)
    same(sp.diff(sp.tan(th), th), sp.sec(th) ** 2, row["id"] + " tangent derivative")
    same(sp.tan(sp.pi / 3), sp.sqrt(3), row["id"] + " upper angle")
    argument = (3 * x - x**3) / (1 - 3 * x**2)
    same(sp.expand_trig(argument.subs(x, sp.tan(th)) - sp.tan(3 * th)), 0, row["id"] + " triple angle")
    y = sp.symbols("y", real=True)
    same(sp.diff(sp.atan(sp.tan(y)), y), 1, row["id"] + " arctangent derivative")
    require(sp.solveset(sp.cos(y), y, sp.Interval.Ropen(0, sp.pi / 2)) == sp.EmptySet, row["id"] + " first branch")
    same(sp.atan(sp.tan(sp.pi / 4)), sp.pi / 4, row["id"] + " first sample")
    require(sp.solveset(sp.cos(y), y, sp.Interval.Lopen(sp.pi / 2, sp.pi)) == sp.EmptySet, row["id"] + " second branch")
    same(sp.atan(sp.tan(3 * sp.pi / 4)), 3 * sp.pi / 4 - sp.pi, row["id"] + " second sample")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 3), row["id"] + " cosine sign")
    left = 3 * th * sp.tan(th) + 3 * sp.log(sp.cos(th))
    right = (3 * th - sp.pi) * sp.tan(th) + 3 * sp.log(sp.cos(th))
    same(sp.diff(left, th), 3 * th * sp.sec(th) ** 2, row["id"] + " first antiderivative")
    same(sp.diff(right, th), (3 * th - sp.pi) * sp.sec(th) ** 2, row["id"] + " second antiderivative")
    require(sp.simplify(left.subs(th, 0)) == 0, row["id"] + " lower endpoint")
    first = sp.simplify(left.subs(th, sp.pi / 6) - left.subs(th, 0))
    second = sp.simplify(right.subs(th, sp.pi / 3) - right.subs(th, sp.pi / 6))
    value = sp.simplify(first + second)
    same(value, sp.pi / sp.sqrt(3) - sp.log(8), row["id"] + " guide value")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p01(row, x):
    """Nested exponential speed integral on [0, (ln 4)**2]."""
    require(row["limits"] == ["0", "log(4)**2"], row["id"] + " limits")
    integrand = integrand_of(row)
    t = sp.symbols("t", positive=True)
    same(sp.diff(t**2, t), 2 * t, row["id"] + " t jacobian")
    same(sp.sqrt(sp.log(4) ** 2), sp.log(4), row["id"] + " upper t")
    substituted = integrand.subs(x, t**2) * (2 * t)
    reduced = 2 * sp.exp(t / 2) * sp.exp(sp.exp(t / 2) / 2)
    same(substituted, reduced, row["id"] + " t integrand")
    u = sp.symbols("u", positive=True)
    same(sp.diff(2 * sp.log(u), u), 2 / u, row["id"] + " u jacobian")
    same(sp.exp(sp.log(4) / 2), 2, row["id"] + " upper u")
    require(sp.exp(0) == 1, row["id"] + " lower u")
    changed = reduced.subs(t, 2 * sp.log(u)) * (2 / u)
    same(changed, 4 * sp.exp(u / 2), row["id"] + " u integrand")
    value = sp.integrate(4 * sp.exp(u / 2), (u, 1, 2))
    same(value, 8 * (sp.E - sp.sqrt(sp.E)), row["id"] + " reduced integral")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p02(row, x):
    """Real cube root on [-1, 1]."""
    require(row["limits"] == ["-1", "1"], row["id"] + " limits")
    integrand = integrand_of(row)
    positive = sp.symbols("p", positive=True)
    negative = -positive
    same(integrand.subs(x, positive**3), 15 * (positive + 1) ** 3, row["id"] + " positive root")
    same(integrand.subs(x, negative**3), 15 * (negative + 1) ** 3, row["id"] + " negative root")
    require(integrand.subs(x, 0) == 15, row["id"] + " at zero")
    same(sp.diff(positive**3, positive), 3 * positive**2, row["id"] + " jacobian")
    u = sp.symbols("u", real=True)
    value = sp.integrate(45 * u**2 * (1 + u) ** 3, (u, -1, 1))
    require(value == 84, row["id"] + " polynomial")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p03(row, x):
    """Expand the cubic and add four Gaussian moments on [0, infinity)."""
    require(row["limits"] == ["0", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    expanded = (x**3 + 3 * x**2 + 3 * x + 1) * sp.exp(-x**2)
    same(sp.expand(integrand - expanded), 0, row["id"] + " expansion")
    moments = (
        (sp.exp(-x**2), sp.sqrt(sp.pi) / 2),
        (x * sp.exp(-x**2), sp.Rational(1, 2)),
        (x**2 * sp.exp(-x**2), sp.sqrt(sp.pi) / 4),
        (x**3 * sp.exp(-x**2), sp.Rational(1, 2)),
    )
    weights = (1, 3, 3, 1)
    total = 0
    for weight, (term, expected) in zip(weights, moments):
        got = sp.integrate(term, (x, 0, sp.oo))
        same(got, expected, row["id"] + " moment")
        total += weight * got
    value = sp.simplify(total)
    same(value, 2 + 5 * sp.sqrt(sp.pi) / 4, row["id"] + " combination")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p04(row, x):
    """Logarithmic substitution for 1/(x (x**ln(4) + 1)) on [1, infinity)."""
    require(row["limits"] == ["1", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    u = sp.symbols("u", real=True)
    same(integrand * x, 1 / (x ** sp.log(4) + 1), row["id"] + " remove dx/x")
    same(sp.exp(u) ** sp.log(4), 4**u, row["id"] + " power")
    t = sp.symbols("t", positive=True)
    same(sp.diff(sp.exp(-u * sp.log(4)), u), -sp.log(4) * sp.exp(-u * sp.log(4)), row["id"] + " t derivative")
    # t = 4**(-u) runs from 1 down to 0, and du/(4**u+1) = -dt / (log(4) (1+t)).
    ratio = sp.together(
        (1 / (-sp.log(4) * t)) * (t / (1 + t)) + 1 / (sp.log(4) * (1 + t))
    )
    same(ratio, 0, row["id"] + " t integrand")
    value = sp.integrate(1 / (sp.log(4) * (1 + t)), (t, 0, 1))
    same(value, sp.log(2) / sp.log(4), row["id"] + " reduced integral")
    same(value, sp.Rational(1, 2), row["id"] + " logarithm quotient")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p05(row, x):
    """Complete the square on the whole line."""
    require(row["limits"] == ["-oo", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    completed = (x + sp.pi / 2) ** 2 + 3 * sp.pi**2 / 4
    same(sp.expand(x**2 + sp.pi * x + sp.pi**2 - completed), 0, row["id"] + " square")
    amplitude = sp.pi * sp.sqrt(3) / 2
    same(sp.sqrt(3 * sp.pi**2 / 4), amplitude, row["id"] + " amplitude")
    primitive = sp.atan((x + sp.pi / 2) / amplitude) / amplitude
    same(sp.diff(primitive, x), 1 / completed, row["id"] + " derivative")
    same(integrand, 1 / completed, row["id"] + " integrand")
    upper = sp.limit(primitive, x, sp.oo)
    lower = sp.limit(primitive, x, -sp.oo)
    value = sp.simplify(upper - lower)
    same(value, sp.pi / amplitude, row["id"] + " arctangent evaluation")
    same(value, 2 / sp.sqrt(3), row["id"] + " simplified quotient")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p06(row, x):
    """Square-root substitution and integration by parts on [0, infinity)."""
    require(row["limits"] == ["0", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    t = sp.symbols("t", positive=True)
    same(sp.diff(t**2, t), 2 * t, row["id"] + " jacobian")
    same(sp.log(sp.sqrt(t**2 + 1)), sp.log(1 + t**2) / 2, row["id"] + " logarithm")
    substituted = integrand.subs(x, t**2) * (2 * t)
    reduced = sp.log(1 + t**2) / t**2
    same(substituted, reduced, row["id"] + " substituted integrand")
    boundary = -sp.log(1 + t**2) / t
    same(sp.diff(boundary, t) + 2 / (1 + t**2), reduced, row["id"] + " parts")
    require(sp.limit(sp.log(1 + t**2) / t, t, sp.oo) == 0, row["id"] + " upper boundary")
    require(sp.limit(sp.log(1 + t**2) / t, t, 0) == 0, row["id"] + " lower boundary")
    value = sp.integrate(2 / (1 + t**2), (t, 0, sp.oo))
    require(value == sp.pi, row["id"] + " arctangent")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p07(row, x):
    """Odd terms drop on [-pi/2, pi/2]. The even term is a cosine cube."""
    require(row["limits"] == ["-pi/2", "pi/2"], row["id"] + " limits")
    integrand = integrand_of(row)
    rewritten = sp.sin(x) * sp.cos(x) ** 2 + sp.cos(x) ** 3 + sp.sin(x) * sp.cos(x)
    same(sp.simplify(integrand - rewritten), 0, row["id"] + " cosine factor")
    odd_square = -sp.cos(x) ** 3 / 3
    odd_product = -sp.cos(x) ** 2 / 2
    same(sp.diff(odd_square, x), sp.sin(x) * sp.cos(x) ** 2, row["id"] + " first odd term")
    same(sp.diff(odd_product, x), sp.sin(x) * sp.cos(x), row["id"] + " second odd term")
    for primitive in (odd_square, odd_product):
        require(sp.simplify(primitive.subs(x, sp.pi / 2) - primitive.subs(x, -sp.pi / 2)) == 0, row["id"] + " odd ends")
    same(sp.cos(x) ** 3, sp.cos(x) * (1 - sp.sin(x) ** 2), row["id"] + " cosine cube")
    same(sp.diff(sp.sin(x), x), sp.cos(x), row["id"] + " sine derivative")
    half = sp.integrate(1 - x**2, (x, 0, 1))
    require(half == sp.Rational(2, 3), row["id"] + " half integral")
    require_answer(2 * half, row, row["id"] + " stored value")


def check_3_8_p08(row, x):
    """Principal square roots of a complex conjugate pair on [-1, 1]."""
    require(row["limits"] == ["-1", "1"], row["id"] + " limits")
    integrand = integrand_of(row)
    th = sp.symbols("th", real=True)
    require(_positive_on(sp.sin(th), th, 0, sp.pi), row["id"] + " sine sign")
    require(_positive_on(sp.cos(th / 2), th, 0, sp.pi), row["id"] + " half cosine")
    same(sp.sqrt(-(sp.sin(th) ** 2)), sp.I * sp.Abs(sp.sin(th)), row["id"] + " inner root")
    _abs_positive()
    substituted = integrand.subs(x, sp.cos(th))
    with_abs = sp.sqrt(sp.cos(th) + sp.I * sp.Abs(sp.sin(th))) + sp.sqrt(sp.cos(th) - sp.I * sp.Abs(sp.sin(th)))
    same(substituted, with_abs, row["id"] + " absolute sine")
    plain = sp.sqrt(sp.exp(sp.I * th)) + sp.sqrt(sp.exp(-sp.I * th))
    same(with_abs.subs(sp.Abs(sp.sin(th)), sp.sin(th)), plain, row["id"] + " exponential radicands")
    same(sp.cos(th) + sp.I * sp.sin(th), sp.exp(sp.I * th), row["id"] + " positive euler")
    same(sp.cos(th) - sp.I * sp.sin(th), sp.exp(-sp.I * th), row["id"] + " negative euler")
    upper = sp.atan2(sp.sin(th), sp.cos(th))
    lower = sp.atan2(-sp.sin(th), sp.cos(th))
    same(sp.diff(upper, th), 1, row["id"] + " upper argument derivative")
    same(sp.diff(lower, th), -1, row["id"] + " lower argument derivative")
    same(upper.subs(th, sp.pi / 2), sp.pi / 2, row["id"] + " upper argument sample")
    same(lower.subs(th, sp.pi / 2), -sp.pi / 2, row["id"] + " lower argument sample")
    same(sp.re(sp.sqrt(sp.exp(sp.I * th))), sp.cos(upper / 2), row["id"] + " first real part")
    same(sp.im(sp.sqrt(sp.exp(sp.I * th))), sp.sin(upper / 2), row["id"] + " first imaginary part")
    same(sp.re(sp.sqrt(sp.exp(-sp.I * th))), sp.cos(lower / 2), row["id"] + " second real part")
    same(sp.im(sp.sqrt(sp.exp(-sp.I * th))), sp.sin(lower / 2), row["id"] + " second imaginary part")
    same(sp.cos(th / 2) + sp.cos((-th) / 2), 2 * sp.cos(th / 2), row["id"] + " real sum")
    same(sp.sin(th / 2) + sp.sin((-th) / 2), 0, row["id"] + " imaginary sum")
    same(sp.diff(sp.cos(th), th), -sp.sin(th), row["id"] + " cosine derivative")
    same(2 * sp.cos(th / 2) * sp.sin(th), 4 * sp.cos(th / 2) ** 2 * sp.sin(th / 2), row["id"] + " double angle")
    same(sp.diff(sp.cos(th / 2), th), -sp.sin(th / 2) / 2, row["id"] + " u derivative")
    u = sp.symbols("u", real=True)
    value = sp.integrate(8 * u**2, (u, 0, 1))
    require(value == sp.Rational(8, 3), row["id"] + " reduced integral")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p09(row, x):
    """Integration by parts after t = x**(1/4), on [1, 4]."""
    require(row["limits"] == ["1", "4"], row["id"] + " limits")
    t = sp.symbols("t", positive=True)
    same(sp.Integer(4) ** sp.Rational(1, 4), sp.sqrt(2), row["id"] + " upper t")
    same(sp.diff(t**4, t), 4 * t**3, row["id"] + " jacobian")
    parts = t**4 * sp.asec(t)
    extra = t**3 / sp.sqrt(t**2 - 1)
    same(sp.diff(parts, t), 4 * t**3 * sp.asec(t) + extra, row["id"] + " parts")
    boundary = sp.simplify(parts.subs(t, sp.sqrt(2)) - parts.subs(t, 1))
    require(boundary == sp.pi, row["id"] + " boundary")
    th = sp.symbols("th", real=True)
    require(_positive_on(sp.sin(th), th, 0, sp.pi / 4), row["id"] + " sine sign")
    require(_positive_on(sp.cos(th), th, 0, sp.pi / 4), row["id"] + " cosine sign")
    substituted = sp.simplify((extra * sp.diff(sp.sec(th), th)).subs(t, sp.sec(th)))
    same(substituted, sp.tan(th) * sp.sec(th) ** 4 / sp.Abs(sp.tan(th)), row["id"] + " secant form")
    _abs_positive()
    same(sp.sec(th) ** 4, sp.sec(th) ** 2 * (1 + sp.tan(th) ** 2), row["id"] + " secant power")
    same(sp.diff(sp.tan(th), th), sp.sec(th) ** 2, row["id"] + " tangent derivative")
    require(sp.tan(0) == 0, row["id"] + " lower w")
    same(sp.tan(sp.pi / 4), 1, row["id"] + " upper w")
    w = sp.symbols("w", real=True)
    remainder = sp.integrate(1 + w**2, (w, 0, 1))
    require(remainder == sp.Rational(4, 3), row["id"] + " remainder")
    require_answer(sp.simplify(boundary - remainder), row, row["id"] + " stored value")


def check_3_8_p10(row, x):
    """Polynomial division. The numerator of the remainder is the derivative of the denominator."""
    require(row["kind"] == "indefinite" and row["limits"] == [], row["id"] + " shape")
    integrand = integrand_of(row)
    quotient = 1 + (2 * x - 1) / (x**2 - x + 1)
    same(sp.together(integrand - quotient), 0, row["id"] + " division")
    same(sp.diff(x**2 - x + 1, x), 2 * x - 1, row["id"] + " denominator derivative")
    answer = answer_of(row)
    same(sp.diff(answer, x), integrand, row["id"] + " antiderivative")


def check_3_8_p11(row, x):
    """Arctangent antiderivative of 1/(e**x + e**(-(x+1))) on [0, infinity)."""
    require(row["limits"] == ["0", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    primitive = sp.sqrt(sp.E) * sp.atan(sp.exp(x) * sp.sqrt(sp.E))
    same(sp.diff(primitive, x), integrand, row["id"] + " derivative")
    upper = sp.limit(primitive, x, sp.oo)
    lower = primitive.subs(x, 0)
    value = sp.simplify(upper - lower)
    same(value, sp.sqrt(sp.E) * (sp.pi / 2 - sp.atan(sp.sqrt(sp.E))), row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p12(row, x):
    """Two substitutions for 1/sqrt(1+sqrt(e**x)) on [0, infinity)."""
    require(row["limits"] == ["0", "oo"], row["id"] + " limits")
    integrand = integrand_of(row)
    same(1 / sp.sqrt(1 + sp.sqrt(sp.exp(x))), integrand, row["id"] + " printed form")
    u = sp.symbols("u", positive=True)
    same(sp.diff(2 * sp.log(u), u), 2 / u, row["id"] + " u jacobian")
    after_u = integrand.subs(x, 2 * sp.log(u)) * (2 / u)
    same(after_u, 2 / (u * sp.sqrt(1 + u)), row["id"] + " u integrand")
    w = sp.symbols("w", positive=True)
    same(sp.diff(w**2 - 1, w), 2 * w, row["id"] + " w jacobian")
    after_w = after_u.subs(u, w**2 - 1) * (2 * w)
    same(sp.simplify(after_w - 4 / (w**2 - 1)), 0, row["id"] + " w integrand")
    primitive = 2 * sp.log((w - 1) / (w + 1))
    same(sp.diff(primitive, w), 4 / (w**2 - 1), row["id"] + " antiderivative")
    require(sp.limit(primitive, w, sp.oo) == 0, row["id"] + " upper limit")
    ratio = (sp.sqrt(2) - 1) / (sp.sqrt(2) + 1)
    lower = primitive.subs(w, sp.sqrt(2))
    same(lower, 2 * sp.log(ratio), row["id"] + " lower logarithm")
    require((sp.sqrt(2) - 1).is_positive and (sp.sqrt(2) + 1).is_positive, row["id"] + " positive factors")
    split = sp.log(sp.sqrt(2) - 1) - sp.log(sp.sqrt(2) + 1)
    same(sp.exp(split), ratio, row["id"] + " split exponential")
    value = -2 * split
    same(value, -2 * sp.log(sp.sqrt(2) - 1) + 2 * sp.log(sp.sqrt(2) + 1), row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p13(row, x):
    """Constant factor e, then two square-root substitutions, on [0, 9]."""
    require(row["limits"] == ["0", "9"], row["id"] + " limits")
    integrand = integrand_of(row)
    same(integrand, sp.E * sp.sqrt(1 + sp.sqrt(x)), row["id"] + " constant factor")
    u = sp.symbols("u", positive=True)
    same(sp.diff(u**2, u), 2 * u, row["id"] + " u jacobian")
    after_u = integrand.subs(x, u**2) * (2 * u)
    same(sp.simplify(after_u - 2 * sp.E * u * sp.sqrt(1 + u)), 0, row["id"] + " u integrand")
    w = sp.symbols("w", positive=True)
    same(sp.diff(w - 1, w), 1, row["id"] + " w jacobian")
    after_w = after_u.subs(u, w - 1)
    same(sp.simplify(after_w - 2 * sp.E * (w ** sp.Rational(3, 2) - w ** sp.Rational(1, 2))), 0, row["id"] + " w integrand")
    primitive = sp.Rational(2, 5) * w ** sp.Rational(5, 2) - sp.Rational(2, 3) * w ** sp.Rational(3, 2)
    same(sp.diff(primitive, w), w ** sp.Rational(3, 2) - w ** sp.Rational(1, 2), row["id"] + " antiderivative")
    span = sp.simplify(primitive.subs(w, 4) - primitive.subs(w, 1))
    value = sp.simplify(2 * sp.E * span)
    same(value, 232 * sp.E / 15, row["id"] + " endpoints")
    require_answer(value, row, row["id"] + " stored value")


def check_3_8_p14(row, x):
    """Tangent substitution. Differentiate the stored logarithm in u = tan(x)."""
    require(row["kind"] == "indefinite" and row["limits"] == [], row["id"] + " shape")
    integrand = integrand_of(row)
    u = sp.symbols("u", positive=True)
    same(sp.expand_trig(sp.tan(2 * x) - 2 * sp.tan(x) / (1 - sp.tan(x) ** 2)), 0, row["id"] + " double angle")
    rewritten = 2 / (u * (1 - u**2))
    same(sp.simplify((2 * u / (1 - u**2)) / u**2 - rewritten), 0, row["id"] + " rational integrand")
    same(sp.diff(sp.tan(x), x), 1 + sp.tan(x) ** 2, row["id"] + " tangent derivative")
    rational = rewritten / (1 + u**2)
    stored_u = -sp.log(u - 1) / 2 - sp.log(u + 1) / 2 - sp.log(u**2 + 1) / 2 + 2 * sp.log(u)
    same(sp.diff(stored_u, u), rational, row["id"] + " u antiderivative")
    answer = answer_of(row)
    same(answer, stored_u.subs(u, sp.tan(x)), row["id"] + " stored combination")
    chain = sp.diff(answer, x) - rewritten.subs(u, sp.tan(x))
    require(sp.simplify(sp.together(chain)) == 0, row["id"] + " chain rule")
    require(
        sp.simplify(sp.expand_trig(integrand - rewritten.subs(u, sp.tan(x)))) == 0,
        row["id"] + " back to the integrand",
    )


def check_4_4_p01(row, x):
    """King's rule for f(f(x)) on [1/4, 3/4]. The guide prints 1/4."""
    require(row["limits"] == ["1/4", "3/4"], row["id"] + " limits")
    integrand = integrand_of(row)

    def f(argument):
        return 4**argument / (2 + 4**argument)

    same(integrand, f(f(x)), row["id"] + " composition")
    z = sp.symbols("z", real=True)
    same(sp.cancel(sp.together(f(z) + f(1 - z) - 1)), 0, row["id"] + " complement")
    same(sp.cancel(sp.together(f(f(x)) + f(1 - f(x)) - 1)), 0, row["id"] + " composed complement")
    same(f(f(1 - x)), f(1 - f(x)), row["id"] + " swap")
    same(integrand + integrand.subs(x, 1 - x), 1, row["id"] + " reflected sum")
    same(sp.diff(1 - x, x), -1, row["id"] + " reflection derivative")
    lo, hi = sp.Rational(1, 4), sp.Rational(3, 4)
    same(1 - lo, hi, row["id"] + " swapped lower")
    same(1 - hi, lo, row["id"] + " swapped upper")
    length = sp.simplify(hi - lo)
    require(length == sp.Rational(1, 2), row["id"] + " length")
    require_answer(length / 2, row, row["id"] + " stored value")


def check_4_6_p04(row, x):
    """Reverse quotient rule. The guide takes f(x) = x and g(x) = 1 + ln(x)."""
    require(row["kind"] == "indefinite" and row["limits"] == [], row["id"] + " shape")
    integrand = integrand_of(row)
    quotient = ((1 + sp.log(x)) - 1) / (1 + sp.log(x)) ** 2
    same(sp.together(quotient - integrand), 0, row["id"] + " quotient")
    answer = answer_of(row)
    same(answer, x / (1 + sp.log(x)), row["id"] + " guide antiderivative")
    same(sp.diff(answer, x), integrand, row["id"] + " derivative")


def check_6_1_p04(row, x):
    """Inverse-function formula. The guide integrates csc(y)**2 and prints 1."""
    require(row["limits"] == ["1", "2"], row["id"] + " limits")
    same(sp.acsc(1), sp.pi / 2, row["id"] + " lower inverse")
    same(sp.acsc(sp.sqrt(2)), sp.pi / 4, row["id"] + " upper inverse")
    y = sp.symbols("y", real=True)
    positive = sp.symbols("p", positive=True)
    same(sp.csc(sp.acsc(sp.sqrt(positive))) ** 2, positive, row["id"] + " inverse")
    antideriv = -sp.cot(y)
    same(sp.diff(antideriv, y), sp.csc(y) ** 2, row["id"] + " cosecant antiderivative")
    moved = sp.simplify(antideriv.subs(y, sp.pi / 4) - antideriv.subs(y, sp.pi / 2))
    require(moved == -1, row["id"] + " moved integral")
    value = 2 * (sp.pi / 4) - 1 * (sp.pi / 2) - moved
    require(sp.simplify(value) == 1, row["id"] + " formula")
    require_answer(value, row, row["id"] + " stored value")


def check_6_7_p03(row, x):
    """Feynman trick. The guide prints ln(11)."""
    require(row["limits"] == ["0", "1"], row["id"] + " limits")
    integrand = integrand_of(row)
    n = sp.symbols("n", positive=True)
    family = (x**n - 1) / sp.log(x)
    same(family.subs(n, 10), integrand, row["id"] + " printed case")
    same(sp.diff(family, n), x**n, row["id"] + " parameter derivative")
    moment = sp.integrate(x**n, (x, 0, 1))
    same(moment, 1 / (n + 1), row["id"] + " power integral")
    same(sp.diff(sp.log(n + 1), n), 1 / (n + 1), row["id"] + " logarithm derivative")
    same((x**0 - 1) / sp.log(x), 0, row["id"] + " vanishing case")
    value = sp.log(11)
    require_answer(value, row, row["id"] + " stored value")


CHECKS = {
    "YANG-2.7-P01": check_2_7_p01,
    "YANG-2.7-P02": check_2_7_p02,
    "YANG-2.7-P03": check_2_7_p03,
    "YANG-2.7-P04": check_2_7_p04,
    "YANG-2.7-P05": check_2_7_p05,
    "YANG-2.7-P06": check_2_7_p06,
    "YANG-2.7-P07": check_2_7_p07,
    "YANG-2.7-P08": check_2_7_p08,
    "YANG-2.7-P09": check_2_7_p09,
    "YANG-2.7-P10": check_2_7_p10,
    "YANG-2.7-P11": check_2_7_p11,
    "YANG-2.7-P12": check_2_7_p12,
    "YANG-2.7-P13": check_2_7_p13,
    "YANG-3.4-P06": check_3_4_p06,
    "YANG-3.8-P01": check_3_8_p01,
    "YANG-3.8-P02": check_3_8_p02,
    "YANG-3.8-P03": check_3_8_p03,
    "YANG-3.8-P04": check_3_8_p04,
    "YANG-3.8-P05": check_3_8_p05,
    "YANG-3.8-P06": check_3_8_p06,
    "YANG-3.8-P07": check_3_8_p07,
    "YANG-3.8-P08": check_3_8_p08,
    "YANG-3.8-P09": check_3_8_p09,
    "YANG-3.8-P10": check_3_8_p10,
    "YANG-3.8-P11": check_3_8_p11,
    "YANG-3.8-P12": check_3_8_p12,
    "YANG-3.8-P13": check_3_8_p13,
    "YANG-3.8-P14": check_3_8_p14,
    "YANG-4.4-P01": check_4_4_p01,
    "YANG-4.6-P04": check_4_6_p04,
    "YANG-6.1-P04": check_6_1_p04,
    "YANG-6.7-P03": check_6_7_p03,
}


def load_rows():
    rows = {}
    for line in RECORDS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[row["id"]] = row
    return rows


SECTIONS = frozenset({"2.7", "3.4", "3.8", "4.4", "4.6", "6.1", "6.7"})


def check_steps(rows):
    require(tuple(CHECKS) == IDS, "check order")
    require(set(IDS) == set(CHECKS), "check ids")
    require({ident.split("-")[1] for ident in IDS} == set(SECTIONS), "section set")
    present = [
        row["id"]
        for row in rows.values()
        if row.get("source") == "yang_book" and row.get("section") in SECTIONS and row.get("kind") != "reference"
    ]
    require(set(present) == set(IDS), "catalog batch")
    x = sp.symbols("x", real=True)
    for ident in IDS:
        CHECKS[ident](rows[ident], x)


def check_text(rows):
    """The writeup states the stored answer and leaves the origin missing."""
    for ident in IDS:
        row = rows[ident]
        plain = row.get("worked_solution_plain")
        latex = row.get("worked_solution_latex")
        require(isinstance(plain, str) and plain.strip(), ident + " missing plain")
        require(isinstance(latex, str) and latex.strip(), ident + " missing latex")
        require(row.get("worked_solution_origin") == "missing", ident + " origin")
        require(plain.strip().endswith("The answer is " + row["answer_sympy"] + "."), ident + " plain answer")
        require(latex.strip().endswith("The answer is \\(" + row["answer_latex"] + "\\)."), ident + " latex answer")


def main():
    rows = load_rows()
    check_steps(rows)
    check_text(rows)
    print(f"PASS yang worked steps ({len(IDS)} rows)")


if __name__ == "__main__":
    main()
