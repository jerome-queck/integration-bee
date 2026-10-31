#!/usr/bin/env python3
"""Continuous primitives whose smooth pieces are separated by jumps.

The ordinary derivative check differentiates a floor. SymPy leaves
``Derivative(floor)`` in that result, so a floor correction cannot pass it.
This module does not change that test. A floor or Piecewise formula is an
antiderivative only when both of the following hold:

- on each piece the floor index is an integer constant, and the ordinary
  derivative equals the integrand;
- the left and right limits agree at every join.

A jumping formula fails the second test. ``must_fail`` is that sample.
Numeric checks use mpmath at 80 decimal places and require an absolute error below 10**(-30).
"""

from __future__ import annotations

import sympy as sp
from sympy import Q, ask

_DPS = 80


def _zero(expr) -> bool:
    if expr == 0:
        return True
    try:
        if sp.simplify(expr) == 0:
            return True
    except Exception:
        return False
    try:
        if sp.trigsimp(sp.expand(expr)) == 0:
            return True
    except Exception:
        return False
    return False


def _match(left, right) -> bool:
    return _zero(sp.expand(left - right))


def _same(left, right) -> bool:
    """Structural equality after expand.

    A miss must not call simplify. indefinite_ok runs this screen on every
    indefinite row, and simplify of a high power such as x**2024*exp(x**2024)
    blows the ordinary proof timeout.
    """
    try:
        return sp.expand(left) == sp.expand(right)
    except Exception:
        return False


def _generic_zero(expr) -> bool:
    """The unchanged pack-gate zero test, used on a smooth piece."""
    import pack_gate

    return pack_gate._zero(expr)


def _cos_nonnegative_on_half_turn() -> bool:
    """cos t >= 0 for every real t in [-pi/2, pi/2].

    sin(t)**2 is nonnegative and sin(t)**2 + cos(t)**2 = 1, so |cos t| <= 1.
    Lagrange's remainder after the degree-4 Taylor polynomial is then at most
    t**6/720 in absolute value, and
    cos t >= 1 - t**2/2 + t**4/24 - t**6/720.
    That lower bound is decreasing on [0, pi/4] and still positive at pi/4,
    because pi < 22/7 and the bound is positive at 11/14. Thus cos t > 0
    on [-pi/4, pi/4], so tan is strictly increasing there (its derivative is
    sec(t)**2 > 0). tan(pi/4) = 1, hence |tan u| < 1 for |u| < pi/4. The
    double-angle formula then gives cos t > 0 for |t| < pi/2, and the
    endpoints are 0.
    """
    t = sp.Symbol("_t", real=True)
    if ask(Q.nonnegative(sp.sin(t) ** 2)) is not True:
        return False
    if not _zero(sp.sin(t) ** 2 + sp.cos(t) ** 2 - 1):
        return False
    if ask(Q.le(1 - sp.sin(t) ** 2, 1)) is not True:
        return False
    lower = 1 - t**2 / 2 + t**4 / 24 - t**6 / 720
    # Derivative -t*(t**4 - 20*t**2 + 120)/120. The quartic factor stays positive.
    quartic = t**4 - 20 * t**2 + 120
    if sp.minimum(quartic, t, sp.Interval(0, 2)) <= 0:
        return False
    if not _zero(sp.diff(lower, t) + t * quartic / 120):
        return False
    # pi < 22/7 because x**4*(1-x)**4/(1+x**2) is nonnegative and not identically zero.
    height = sp.Symbol("_x", real=True)
    positive_integrand = height**4 * (1 - height) ** 4 / (1 + height**2)
    gap = sp.integrate(positive_integrand, (height, 0, 1))
    if gap != sp.Rational(22, 7) - sp.pi:
        return False
    if positive_integrand.subs(height, sp.Rational(1, 2)) <= 0:
        return False
    if not _zero(sp.together(positive_integrand * (1 + height**2) - (height * (1 - height)) ** 4)):
        return False
    # On [1/4, 1/2], x(1-x) is at least (1/4)*(3/4) and 1+x**2 is at most 5/4.
    quarter_low = sp.Rational(1, 4) * sp.Rational(3, 4)
    quarter_high = 1 + sp.Rational(1, 2) ** 2
    if quarter_low != sp.Rational(3, 16) or quarter_high != sp.Rational(5, 4):
        return False
    lower_integral = (sp.Rational(3, 16) ** 4) * sp.Rational(4, 5) * sp.Rational(1, 4)
    if lower_integral <= 0:
        return False
    # pi/4 < 11/14 because pi < 22/7, and lower decreases on [0, 11/14].
    bound = lower.subs(t, sp.Rational(11, 14))
    if not isinstance(sp.simplify(bound), sp.Rational) or sp.simplify(bound) <= 0:
        return False
    u = sp.Symbol("_u", real=True)
    if not _zero(sp.cos(2 * u) - (1 - sp.tan(u) ** 2) / (1 + sp.tan(u) ** 2)):
        return False
    if not _zero(sp.diff(sp.tan(u), u) - 1 / sp.cos(u) ** 2):
        return False
    if sp.tan(0) != 0 or sp.tan(sp.pi / 4) != 1:
        return False
    if sp.cos(sp.pi / 2) != 0 or sp.cos(-sp.pi / 2) != 0:
        return False
    ratio = (1 - u**2) / (1 + u**2)
    if ask(Q.positive(ratio), Q.lt(u**2, 1)) is not True:
        return False
    return True


def _sqrt_cos_integrand(integrand, symbol) -> bool:
    return _same(integrand, sp.sqrt(1 + sp.cos(symbol)))


def _sqrt_piece_slope(symbol, index):
    return sp.sqrt(2) * ((-1) ** index) * sp.cos(symbol / 2)


def _sqrt_piece_identity(symbol, index) -> bool:
    """With the floor frozen, the signed half-angle derivative is the integrand."""
    if not _cos_nonnegative_on_half_turn():
        return False
    if not _zero(1 + sp.cos(symbol) - 2 * sp.cos(symbol / 2) ** 2):
        return False
    if not _zero(sp.sqrt(2 * sp.cos(symbol / 2) ** 2) - sp.sqrt(2) * sp.Abs(sp.cos(symbol / 2))):
        return False
    t = sp.Symbol("_t", real=True)
    phase = 2 * (t + index * sp.pi)
    slope = _sqrt_piece_slope(symbol, index).subs(symbol, phase)
    if not _zero(slope - sp.sqrt(2) * sp.cos(t)):
        return False
    shifted = sp.sqrt(1 + sp.cos(phase))
    if not _zero(shifted - sp.sqrt(2) * sp.Abs(sp.cos(t))):
        return False
    # t = x/2 - k*pi lies in [-pi/2, pi/2) on that piece, so cos t = |cos t|.
    return True


def _sqrt_floor_holds(answer, symbol) -> bool:
    argument = symbol / (2 * sp.pi) + sp.Rational(1, 2)
    floors = answer.atoms(sp.floor)
    if floors != {sp.floor(argument)}:
        return False
    index = sp.Symbol("_k", integer=True)
    local = answer.xreplace({sp.floor(argument): index})
    if local.has(sp.floor):
        return False
    if not _zero(sp.diff(local, symbol) - _sqrt_piece_slope(symbol, index)):
        return False
    if not _sqrt_piece_identity(symbol, index):
        return False
    slot = sp.Symbol("_m", integer=True)
    join = (2 * slot - 1) * sp.pi
    left = sp.simplify(local.subs(index, slot - 1).subs(symbol, join))
    right = sp.simplify(local.subs(index, slot).subs(symbol, join))
    return _zero(left - right)


def _linear_floor_holds(answer, symbol, smooth, jump, argument, pole, period_shift) -> bool:
    """smooth + jump*floor(argument). The smooth piece uses the ordinary derivative test.

    ``period_shift`` is the point one period to the right, written in ``symbol``.
    ``pole`` is one join. The one-sided limits of ``smooth`` repeat at every join
    because ``smooth`` itself repeats under that shift.
    """
    floors = answer.atoms(sp.floor)
    if floors != {sp.floor(argument)}:
        return False
    index = sp.Symbol("_k", integer=True)
    local = answer.xreplace({sp.floor(argument): index})
    if local.has(sp.floor):
        return False
    coefficient = sp.diff(local, index)
    if coefficient.free_symbols & {symbol} or not _match(coefficient, jump):
        return False
    if not _match(local - coefficient * index, smooth):
        return False
    if not _zero(argument.subs(symbol, period_shift) - argument - 1):
        return False
    if not _zero(smooth.subs(symbol, period_shift) - smooth):
        return False
    left_value = sp.limit(smooth, symbol, pole, dir="-")
    right_value = sp.limit(smooth, symbol, pole, dir="+")
    if not getattr(left_value, "is_number", False) or not getattr(right_value, "is_number", False):
        return False
    slot = sp.Symbol("_m", integer=True)
    # The piece to the left of this pole has index m-1; the next piece has m.
    left = left_value + jump * (slot - 1)
    right = right_value + jump * slot
    return _zero(left - right)


def _exp_piecewise_holds(answer, symbol) -> bool:
    if not isinstance(answer, sp.Piecewise) or len(answer.args) != 2:
        return False
    right_piece, right_cond = answer.args[0]
    left_piece, left_cond = answer.args[1]
    if right_cond != (symbol >= -3) or left_cond is not sp.true:
        return False
    integrand_right = sp.exp(symbol / 2) * (symbol + 3)
    integrand_left = -sp.exp(symbol / 2) * (symbol + 3)
    if not _generic_zero(sp.diff(right_piece, symbol) - integrand_right):
        return False
    if not _generic_zero(sp.diff(left_piece, symbol) - integrand_left):
        return False
    height = sp.Symbol("_y", nonnegative=True)
    depth = sp.Symbol("_z", negative=True)
    if sp.Abs(height) != height or not _zero(sp.Abs(depth) + depth):
        return False
    if not _zero(sp.sqrt((symbol + 3) ** 2) - sp.Abs(symbol + 3)):
        return False
    join = -3
    return _match(right_piece.subs(symbol, join), left_piece.subs(symbol, join))


def _limits_differ(answer, symbol, point) -> bool | None:
    if answer.has(sp.floor, sp.Piecewise):
        return None
    left = sp.limit(answer, symbol, point, dir="-")
    right = sp.limit(answer, symbol, point, dir="+")
    if not getattr(left, "is_number", False) or not getattr(right, "is_number", False):
        return None
    return not _zero(left - right)


def holds(answer, integrand, symbol) -> bool | None:
    """True if ``answer`` is a proved continuous primitive, False if it jumps.

    None means this module does not claim the formula, so the ordinary
    derivative check still decides.
    """
    if _sqrt_cos_integrand(integrand, symbol):
        if answer.has(sp.floor):
            return _sqrt_floor_holds(answer, symbol)
        jumped = _limits_differ(answer, symbol, sp.pi)
        if jumped is True:
            return False
        return None
    atan_integrand = 1 / (1 + 8 * sp.cos(symbol) ** 2)
    if _same(integrand, atan_integrand):
        smooth = sp.atan(sp.tan(symbol) / 3) / 3
        if not _generic_zero(sp.diff(smooth, symbol) - atan_integrand):
            return False
        if answer.has(sp.floor):
            return _linear_floor_holds(
                answer,
                symbol,
                smooth,
                sp.pi / 3,
                symbol / sp.pi + sp.Rational(1, 2),
                sp.pi / 2,
                symbol + sp.pi,
            )
        jumped = _limits_differ(answer, symbol, sp.pi / 2)
        if jumped is True:
            return False
        return None
    sample_log = 1 / (symbol * (1 + sp.sin(sp.log(symbol)) ** 2))
    if _same(integrand, sample_log):
        smooth = sp.sqrt(2) * sp.atan(sp.sqrt(2) * sp.tan(sp.log(symbol))) / 2
        if not _generic_zero(sp.diff(smooth, symbol) - sample_log):
            return False
        if answer.has(sp.floor):
            return _linear_floor_holds(
                answer,
                symbol,
                smooth,
                sp.sqrt(2) * sp.pi / 2,
                sp.log(symbol) / sp.pi + sp.Rational(1, 2),
                sp.exp(sp.pi / 2),
                symbol * sp.exp(sp.pi),
            )
        jumped = _limits_differ(answer, symbol, sp.exp(sp.pi / 2))
        if jumped is True:
            return False
        return None
    sample_sine = 1 / (2 + sp.sin(symbol))
    if _same(integrand, sample_sine):
        smooth = 2 * sp.sqrt(3) * sp.atan(2 * sp.sqrt(3) * sp.tan(symbol / 2) / 3 + sp.sqrt(3) / 3) / 3
        if not _generic_zero(sp.diff(smooth, symbol) - sample_sine):
            return False
        if answer.has(sp.floor):
            return _linear_floor_holds(
                answer,
                symbol,
                smooth,
                2 * sp.sqrt(3) * sp.pi / 3,
                symbol / (2 * sp.pi) + sp.Rational(1, 2),
                sp.pi,
                symbol + 2 * sp.pi,
            )
        jumped = _limits_differ(answer, symbol, sp.pi)
        if jumped is True:
            return False
        return None
    radical = sp.sqrt(symbol**2 + 6 * symbol + 9) * sp.exp(symbol / 2)
    if _same(integrand, radical):
        if isinstance(answer, sp.Piecewise):
            return _exp_piecewise_holds(answer, symbol)
        jumped = _limits_differ(answer, symbol, -3)
        if jumped is True:
            return False
        return None
    return None


def catalog_verdict(answer, integrand, symbol):
    """True only for a proved continuous primitive. Anything else is a miss.

    A miss leaves the ordinary derivative check in place. A jumping formula
    is still a miss here: ``must_fail`` rejects it, and the ordinary check is
    not taught to reject or accept floors.
    """
    if holds(answer, integrand, symbol) is True:
        return True
    return None


def _sqrt_wanted(symbol):
    argument = symbol / (2 * sp.pi) + sp.Rational(1, 2)
    return 2 * ((-1) ** sp.floor(argument)) * sp.sqrt(2) * sp.sin(symbol / 2) + 4 * sp.sqrt(2) * sp.floor(argument)


def _exp_wanted(symbol):
    right = (2 * symbol + 2) * sp.exp(symbol / 2)
    left = (-2 * symbol - 2) * sp.exp(symbol / 2) - 8 * sp.exp(-sp.Rational(3, 2))
    return sp.Piecewise((right, symbol >= -3), (left, True))


def _atan_wanted(symbol):
    return sp.atan(sp.tan(symbol) / 3) / 3 + sp.pi * sp.floor(symbol / sp.pi + sp.Rational(1, 2)) / 3


def _log_wanted(symbol):
    argument = sp.log(symbol) / sp.pi + sp.Rational(1, 2)
    smooth = sp.sqrt(2) * sp.atan(sp.sqrt(2) * sp.tan(sp.log(symbol))) / 2
    return smooth + sp.sqrt(2) * sp.pi * sp.floor(argument) / 2


def _sine_wanted(symbol):
    smooth = 2 * sp.sqrt(3) * sp.atan(2 * sp.sqrt(3) * sp.tan(symbol / 2) / 3 + sp.sqrt(3) / 3) / 3
    return smooth + 2 * sp.sqrt(3) * sp.pi * sp.floor(symbol / (2 * sp.pi) + sp.Rational(1, 2)) / 3


def must_fail() -> None:
    """Reject a jumping antiderivative, and do not weaken the ordinary derivative test."""
    import pack_gate

    symbol = sp.Symbol("x", real=True)
    integrand = sp.sqrt(1 + sp.cos(symbol))
    jumping = 2 * sp.sin(symbol) / sp.sqrt(1 + sp.cos(symbol))
    if holds(jumping, integrand, symbol) is not False:
        raise AssertionError("jumping sqrt antiderivative was accepted")
    bare = 2 * ((-1) ** sp.floor(symbol / (2 * sp.pi) + sp.Rational(1, 2))) * sp.sqrt(2) * sp.sin(symbol / 2)
    if holds(bare, integrand, symbol) is not False:
        raise AssertionError("floor sign without the step was accepted")
    good = _sqrt_wanted(symbol)
    if holds(good, integrand, symbol) is not True:
        raise AssertionError("continuous sqrt primitive was rejected")
    if not pack_gate._zero(sp.diff(jumping, symbol) - integrand):
        raise AssertionError("ordinary derivative check no longer accepts the local formula")
    if pack_gate._zero(sp.diff(good, symbol) - integrand):
        raise AssertionError("ordinary derivative check was weakened to accept a floor correction")
    if catalog_verdict(jumping, integrand, symbol) is not None:
        raise AssertionError("jumping formula short-circuited the ordinary derivative check")

    quotient = 2 * (symbol**2 + 4 * symbol + 3) * sp.exp(symbol / 2) / sp.sqrt(symbol**2 + 6 * symbol + 9)
    radical = sp.exp(symbol / 2) * sp.sqrt(symbol**2 + 6 * symbol + 9)
    if holds(quotient, radical, symbol) is not False:
        raise AssertionError("jumping exponential quotient was accepted")
    broken = sp.Piecewise(
        ((2 * symbol + 2) * sp.exp(symbol / 2), symbol >= -3),
        ((-2 * symbol - 2) * sp.exp(symbol / 2), True),
    )
    if holds(broken, radical, symbol) is not False:
        raise AssertionError("piecewise exponential with a jump was accepted")
    if holds(_exp_wanted(symbol), radical, symbol) is not True:
        raise AssertionError("continuous exponential primitive was rejected")

    atan_integrand = 1 / (1 + 8 * sp.cos(symbol) ** 2)
    atan_jump = sp.atan(sp.tan(symbol) / 3) / 3
    if holds(atan_jump, atan_integrand, symbol) is not False:
        raise AssertionError("jumping arctangent was accepted")
    if holds(_atan_wanted(symbol), atan_integrand, symbol) is not True:
        raise AssertionError("continuous arctangent primitive was rejected")
    if not pack_gate._zero(sp.diff(atan_jump, symbol) - atan_integrand):
        raise AssertionError("ordinary derivative check no longer accepts atan(tan(x)/3)/3")
    if pack_gate._zero(sp.diff(_atan_wanted(symbol), symbol) - atan_integrand):
        raise AssertionError("ordinary derivative check was weakened to accept the floor step")


def _mp_diff(function, point, step):
    import mpmath as mp

    return (function(point + step) - function(point - step)) / (2 * step)


def _require_close(error, tolerance, label: str) -> None:
    if error >= tolerance:
        raise AssertionError(f"{label} error {error}")


def numeric_evidence() -> dict[str, str]:
    """Finite-difference and join errors at 40 decimals. Keys are catalog ids."""
    import mpmath as mp

    mp.mp.dps = _DPS
    tolerance = mp.mpf("1e-30")
    step = mp.mpf("1e-20")
    gap = mp.mpf("1e-40")
    report: dict[str, mp.mpf] = {}

    def record(ident: str, error) -> None:
        error = mp.mpf(error)
        report[ident] = max(report.get(ident, mp.mpf(0)), error)
        _require_close(error, tolerance, ident)

    def sqrt_f(value):
        index = mp.floor(value / (2 * mp.pi) + mp.mpf("0.5"))
        return 2 * ((-1) ** index) * mp.sqrt(2) * mp.sin(value / 2) + 4 * mp.sqrt(2) * index

    def sqrt_integrand(value):
        return mp.sqrt(1 + mp.cos(value))

    for text in ("-7.3", "-4", "-1", "0.4", "2", "5", "8"):
        point = mp.mpf(text)
        error = abs(_mp_diff(sqrt_f, point, step) - sqrt_integrand(point))
        record("YANG-1.15-P08", error)
        record("YANG-2.6-P01", error)
    for slot in range(-2, 4):
        join = (2 * slot - 1) * mp.pi

        def piece(index, value):
            return 2 * ((-1) ** index) * mp.sqrt(2) * mp.sin(value / 2) + 4 * mp.sqrt(2) * index

        closed = abs(piece(slot - 1, join) - piece(slot, join))
        approached = abs(sqrt_f(join - gap) - sqrt_f(join + gap))
        record("YANG-1.15-P08", closed)
        record("YANG-1.15-P08", approached)
        record("YANG-2.6-P01", closed)
        record("YANG-2.6-P01", approached)

    def exp_f(value):
        if value >= -3:
            return (2 * value + 2) * mp.e ** (value / 2)
        return (-2 * value - 2) * mp.e ** (value / 2) - 8 * mp.e ** (-mp.mpf("1.5"))

    def exp_integrand(value):
        return mp.e ** (value / 2) * mp.fabs(value + 3)

    for text in ("-7.3", "-4", "-3.2", "-2.5", "0.4", "2"):
        point = mp.mpf(text)
        record("YANG-1.6-P19", abs(_mp_diff(exp_f, point, step) - exp_integrand(point)))
    left_join = (-2 * (-3) - 2) * mp.e ** (mp.mpf("-1.5")) - 8 * mp.e ** (mp.mpf("-1.5"))
    right_join = (2 * (-3) + 2) * mp.e ** (mp.mpf("-1.5"))
    record("YANG-1.6-P19", abs(left_join - right_join))
    record("YANG-1.6-P19", abs(exp_f(mp.mpf("-3") - gap) - exp_f(mp.mpf("-3") + gap)))

    def atan_f(value):
        index = mp.floor(value / mp.pi + mp.mpf("0.5"))
        return mp.atan(mp.tan(value) / 3) / 3 + mp.pi * index / 3

    def atan_integrand(value):
        return 1 / (1 + 8 * mp.cos(value) ** 2)

    for text in ("-7.3", "-4", "-1", "0.4", "2", "5"):
        point = mp.mpf(text)
        record("YANG-2.6-P09", abs(_mp_diff(atan_f, point, step) - atan_integrand(point)))
    for slot in range(-2, 4):
        join = (2 * slot - 1) * mp.pi / 2
        target = mp.pi / 6 + mp.pi * (slot - 1) / 3
        record("YANG-2.6-P09", abs(atan_f(join - gap) - target))
        record("YANG-2.6-P09", abs(atan_f(join + gap) - target))

    def log_f(value):
        phase = mp.log(value)
        index = mp.floor(phase / mp.pi + mp.mpf("0.5"))
        return mp.sqrt(2) * mp.atan(mp.sqrt(2) * mp.tan(phase)) / 2 + mp.sqrt(2) * mp.pi * index / 2

    def log_integrand(value):
        return 1 / (value * (1 + mp.sin(mp.log(value)) ** 2))

    for text in ("0.2", "0.5", "1", "2", "5"):
        point = mp.mpf(text)
        record("SAMPLE-Q14", abs(_mp_diff(log_f, point, step) - log_integrand(point)))
    for slot in range(-1, 3):
        phase = (2 * slot - 1) * mp.pi / 2
        join = mp.e**phase
        target = mp.pi / (2 * mp.sqrt(2)) + (mp.pi / mp.sqrt(2)) * (slot - 1)
        record("SAMPLE-Q14", abs(log_f(join * mp.e ** (-gap)) - target))
        record("SAMPLE-Q14", abs(log_f(join * mp.e**gap) - target))

    def sine_f(value):
        index = mp.floor(value / (2 * mp.pi) + mp.mpf("0.5"))
        inside = 2 * mp.sqrt(3) * mp.tan(value / 2) / 3 + mp.sqrt(3) / 3
        return 2 * mp.sqrt(3) * mp.atan(inside) / 3 + 2 * mp.sqrt(3) * mp.pi * index / 3

    def sine_integrand(value):
        return 1 / (2 + mp.sin(value))

    for text in ("-4", "-1", "0.4", "2", "5"):
        point = mp.mpf(text)
        record("SAMPLE-Q16", abs(_mp_diff(sine_f, point, step) - sine_integrand(point)))
    for slot in range(-1, 3):
        join = (2 * slot - 1) * mp.pi
        target = mp.pi / mp.sqrt(3) + (2 * mp.pi / mp.sqrt(3)) * (slot - 1)
        record("SAMPLE-Q16", abs(sine_f(join - gap) - target))
        record("SAMPLE-Q16", abs(sine_f(join + gap) - target))

    return {ident: mp.nstr(report[ident], 6) for ident in sorted(report)}


def main() -> int:
    must_fail()
    evidence = numeric_evidence()
    print("PASS piecewise primitives (" + ", ".join(f"{ident} {evidence[ident]}" for ident in evidence) + ")")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
