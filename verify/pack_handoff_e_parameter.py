"""Source-checked contour certificate for R1-2022-Q30, with a > 0."""

from __future__ import annotations

import sympy as sp


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-e parameter certificate: " + label)


def _sinc_power(integrand, symbol, lo, hi):
    """∫_0^∞ sin(x)/x^n dx = π / (2 Γ(n) sin(π n/2)) for 0<n<2.

    The form cos(π n/2) Γ(1-n) is an indeterminate 0·∞ at n=1. The gamma
    reflection rewrites it as this quotient, which equals π/2 at n=1, the
    value of the sine integral.
    """
    if lo != 0 or hi != sp.oo:
        return None
    degree = sp.Symbol("n")
    if integrand.free_symbols != {symbol, degree}:
        return None
    if integrand != sp.sin(symbol) / symbol**degree:
        return None
    height = 1 - degree
    reflection = sp.gamma(height) * sp.gamma(degree) - sp.pi / sp.sin(sp.pi * height)
    _require(sp.simplify(reflection) == 0, "gamma-reflection")
    _require(sp.simplify(sp.sin(sp.pi - sp.pi * degree) - sp.sin(sp.pi * degree)) == 0, "sine-supplement")
    _require(
        sp.trigsimp(sp.sin(sp.pi * degree) - 2 * sp.sin(sp.pi * degree / 2) * sp.cos(sp.pi * degree / 2)) == 0,
        "double-angle",
    )
    # Γ(1-n) = π / (sin(π n) Γ(n)), so cos(π n/2) Γ(1-n) cancels to the quotient.
    rewritten = sp.cos(sp.pi * degree / 2) * sp.pi / (sp.sin(sp.pi * degree) * sp.gamma(degree))
    value = sp.pi / (2 * sp.sin(sp.pi * degree / 2) * sp.gamma(degree))
    _require(sp.simplify(rewritten - value) == 0, "cancelled-quotient")
    piece = (
        2
        * 4 ** (-degree / 2 - sp.Rational(1, 2))
        * sp.sqrt(sp.pi)
        * sp.gamma(1 - degree / 2)
        / sp.gamma(degree / 2 + sp.Rational(1, 2))
    )
    _require(sp.simplify(sp.gammasimp(piece / value)) == 1, "sympy-gamma-ratio")
    _require(sp.limit(value, degree, 1) == sp.pi / 2, "removable-n-equals-one")
    _require(sp.integrate(sp.sin(symbol) / symbol, (symbol, 0, sp.oo)) == sp.pi / 2, "sine-integral")
    return value


def definite_value(integrand, symbol, lo, hi):
    """Evaluate the two branch-safe logarithm contours in worked solution p.31.

    The matcher retains the stated positive parameter domain. The original
    problem and mark are on p.3 of their respective 2022 Round 1 PDFs.
    The sine-power row is the 0<n<2 form that stays finite at n=1.
    """
    sinc = _sinc_power(integrand, symbol, lo, hi)
    if sinc is not None:
        return sinc
    a = sp.Symbol("a", positive=True)
    if symbol == a or lo != 0 or hi != sp.oo:
        return None
    expected = sp.atan(symbol) * sp.log(1 + symbol**2) / (symbol * (a**2 + symbol**2))
    if integrand != expected:
        return None

    x = sp.Dummy("x", real=True)
    z = sp.Dummy("z")
    height = sp.Dummy("height", nonnegative=True)
    radius = sp.Dummy("radius", positive=True)
    angle = sp.Dummy("angle", real=True)
    denominator = z * (z**2 + a**2)

    # On the whole real axis, 1 +/- i*x lies in Re(w)=1. Thus its principal
    # logarithm is smooth there; derivative equality and the value at x=0
    # prove both logarithm identities without any forced branch rewrite.
    lower_log = sp.log(1 + x**2) / 2 - sp.I * sp.atan(x)
    upper_log = sp.log(1 + x**2) / 2 + sp.I * sp.atan(x)
    for sign, split in ((-1, lower_log), (1, upper_log)):
        difference = sp.log(1 + sign * sp.I * x) - split
        _require(sp.simplify(sp.diff(difference, x)) == 0, "real-log-derivative")
        _require(difference.subs(x, 0) == 0, "real-log-basepoint")
    real_integrand = expected.subs(symbol, x)
    _require(real_integrand.subs(x, -x) == real_integrand, "even-integrand")
    logarithm_pair = sp.I * (lower_log**2 - upper_log**2) / (2 * denominator.subs(z, x))
    _require(sp.expand(logarithm_pair - real_integrand) == 0, "real-contour-bridge")

    # For the minus log close upwards; for the plus log close downwards.
    # In either half-plane Re(1 +/- i*z)=1+height >= 1, so there is no
    # logarithm cut or zero. The rational denominator has just z=0,+/-i*a;
    # z=0 is removable and a>0 puts exactly one other pole in each contour.
    _require(sp.expand(z * (z - sp.I * a) * (z + sp.I * a) - denominator) == 0, "poles")
    _require(a.is_positive is True, "positive-pole-height")
    residues = []
    for sign in (-1, 1):
        log_argument = 1 + sign * sp.I * z
        half_plane = log_argument.subs(z, x - sign * sp.I * height)
        _require(sp.re(half_plane) == 1 + height, "branch-half-plane")
        _require(sp.re(half_plane).is_positive is True, "branch-positive-real-part")
        kernel = sp.log(log_argument) ** 2 / denominator
        _require(sp.limit(kernel, z, 0) == 0, "removable-origin")
        pole = -sign * sp.I * a
        _require(log_argument.subs(z, pole) == 1 + a, "pole-log-argument")
        residues.append(sp.residue(kernel, z, pole))

    # On |z|=R>a, |z^2+a^2| >= R^2-a^2 by the reverse triangle
    # inequality (the exact squared gap below is nonnegative). The branch
    # geometry above gives 1 <= |1 +/- i*z| <= 1+R and |arg| <= pi/2.
    # Hence |log(1 +/- i*z)| <= log(1+R)+pi/2 and the arc integral is
    # bounded by pi*(log(1+R)+pi/2)^2/(R^2-a^2), which tends to zero.
    circle = radius * (sp.cos(angle) + sp.I * sp.sin(angle))
    modulus_squared = sp.expand_complex((circle**2 + a**2) * (sp.conjugate(circle)**2 + a**2))
    squared_gap = 4 * radius**2 * a**2 * sp.cos(angle)**2
    _require(sp.trigsimp(modulus_squared - (radius**2 - a**2)**2 - squared_gap) == 0, "arc-denominator-gap")
    _require(squared_gap.is_nonnegative is True, "arc-denominator-bound")
    arc_bound = sp.pi * (sp.log(1 + radius) + sp.pi / 2)**2 / (radius**2 - a**2)
    _require(sp.limit(arc_bound, radius, sp.oo) == 0, "vanishing-arcs")

    # The first contour is counterclockwise, the second clockwise. Evenness
    # supplies the additional 1/2 in i/4*(integral_minus-integral_plus).
    minus_line = 2 * sp.pi * sp.I * residues[0]
    plus_line = -2 * sp.pi * sp.I * residues[1]
    return sp.simplify(sp.I * (minus_line - plus_line) / 4)
