"""Source-checked Catalan reductions, including a literal continued fraction.

Every builder checks its integrand and interval before deriving a value.  The
continued-fraction expression retains its coefficients; it has no evaluator
that silently substitutes a trigonometric function or a contest answer.
"""

from __future__ import annotations

import sympy as sp


class ContinuedFraction(sp.Function):
    r"""a / (b(m) + c(m)/(b(m+1) + c(m+1)/(...))).

    Arguments are a, Lambda(n, b(n)), Lambda(n, c(n)), and the starting
    integer m.  The value means the limit of finite convergents, whenever
    that limit exists.  Lambdas bind the coefficient index so it is not a
    free parameter.  This inert expression only stores the printed object.
    """

    nargs = 4

    def _latex(self, printer):
        first, denominators, numerators, start = self.args
        if (not isinstance(denominators, sp.Lambda) or not isinstance(numerators, sp.Lambda)
                or len(denominators.variables) != 1 or len(numerators.variables) != 1):
            return r"\operatorname{ContinuedFraction}\left(" + ", ".join(
                printer._print(arg) for arg in self.args
            ) + r"\right)"
        tail = printer._print(denominators(start + 2)) + r"+\ddots"
        for offset in (1, 0):
            tail = printer._print(denominators(start + offset)) + r"+\frac{" + printer._print(
                numerators(start + offset)
            ) + "}{" + tail + "}"
        return r"\frac{" + printer._print(first) + "}{" + tail + "}"


def _eq(expr) -> bool:
    return expr == 0 or sp.simplify(expr) == 0


def _atan_square(integrand, symbol, lo, hi):
    if (lo, hi) != (0, 1) or integrand != sp.atan(symbol) ** 2:
        return None
    import pack_gate

    theta = sp.Dummy("theta", real=True)
    substitution = sp.atan(symbol)
    if not _eq(sp.diff(substitution, symbol) - 1 / (1 + symbol**2)):
        return None
    if substitution.subs(symbol, 0) != 0 or substitution.subs(symbol, 1) != sp.pi / 4:
        return None
    first = symbol * integrand
    remainder = 2 * symbol * sp.atan(symbol) / (1 + symbol**2)
    if not _eq(sp.diff(first, symbol) - integrand - remainder):
        return None
    if not _eq(sp.tan(substitution) - symbol):
        return None
    second = theta * sp.log(sp.cos(theta))
    if not _eq(sp.diff(second, theta) - sp.log(sp.cos(theta)) + theta * sp.tan(theta)):
        return None
    if sp.limit(second, theta, 0) != 0:
        return None
    quarter = pack_gate._quarter_log_sums()
    if quarter is None:
        return None
    atan_boundary = first.subs(symbol, 1) - first.subs(symbol, 0)
    log_boundary = second.subs(theta, sp.pi / 4)
    return sp.simplify(atan_boundary + 2 * log_boundary - 2 * quarter["cos"])


def _log_sine_ratio(integrand, symbol, lo, hi):
    expected = sp.log((1 + sp.sin(symbol)) / (1 - sp.sin(symbol)))
    if (lo, hi) != (0, sp.pi / 2) or integrand != expected:
        return None
    import pack_gate

    theta = sp.Dummy("theta", real=True)
    reverse = sp.pi / 2 - 2 * theta
    argument = expected.args[0].subs(symbol, reverse)
    if not _eq(sp.trigsimp(sp.expand_trig(argument) - 1 / sp.tan(theta) ** 2)):
        return None
    if sp.diff(reverse, theta) != -2:
        return None
    if reverse.subs(theta, 0) != hi or reverse.subs(theta, sp.pi / 4) != lo:
        return None
    # On 0<theta<=pi/4 both tan(theta) and the printed ratio are positive.
    # Thus log(cot(theta)^2)=-2 log(tan(theta)), without a branch choice.
    quarter = pack_gate._catalan_tangent()
    return None if quarter is None else sp.simplify(-4 * quarter)


def _atan_reciprocal_square(integrand, symbol, lo, hi):
    if (lo, hi) != (1, sp.oo) or integrand != sp.atan(1 / symbol**2) / symbol:
        return None
    import pack_gate

    u = sp.Dummy("u", positive=True)
    line = 1 / u
    transformed = -integrand.subs(symbol, line) * sp.diff(line, u)
    expected = sp.atan(u**2) / u
    if not _eq(transformed - expected):
        return None
    if line.subs(u, 1) != 1 or sp.limit(line, u, 0, dir="+") != sp.oo:
        return None
    return pack_gate._atan_over_power(expected, u, 0, 1)


def open_integrand(integrand, symbol) -> bool:
    """Only the exact printed sine fraction may pass the open-expression gate."""
    if not isinstance(integrand, ContinuedFraction):
        return False
    first, denominators, numerators, start = integrand.args
    if first != symbol**2 or start != 1:
        return False
    if not isinstance(denominators, sp.Lambda) or not isinstance(numerators, sp.Lambda):
        return False
    if len(denominators.variables) != 1 or len(numerators.variables) != 1:
        return False
    n = sp.Dummy("n", integer=True, positive=True)
    d = 2 * n * (2 * n + 1)
    return (denominators(n) == d - symbol**2
            and numerators(n) == d * symbol**2
            and integrand.free_symbols == {symbol})


def _sine_continued_fraction(integrand, symbol, lo, hi):
    if (lo, hi) != (0, sp.pi / 2) or not open_integrand(integrand, symbol):
        return None
    first, denominators, numerators, _start = integrand.args
    n = sp.Dummy("n", integer=True, positive=True)
    d = 2 * n * (2 * n + 1)
    import pack_gate

    # If A_N/B_N is the Nth convergent and D_N=(2N+1)!, continuants
    # obey Y_N=(d_N-x^2)Y_(N-1)+d_(N-1)x^2 Y_(N-2).
    # After division by D_N this is
    # y_N=(1-x^2/d_N)y_(N-1)+(x^2/d_N)y_(N-2).
    # Its solutions with the initial convergent are B_N/D_N=S_N and
    # A_N/D_N=1-S_N, where S_N is the truncated sine series divided by x.
    factorial = sp.factorial(2 * n + 1)
    if not _eq(factorial - d * sp.factorial(2 * n - 1)):
        return None
    if not _eq(numerators(n - 1) * sp.factorial(2 * n - 3) / factorial - symbol**2 / d):
        return None
    term = (-1) ** n * symbol ** (2 * n) / factorial
    previous = term.subs(n, n - 1)
    if not _eq(term + symbol**2 * previous / d):
        return None
    partial = sp.Dummy("partial")
    recurrence = (1 - symbol**2 / d) * partial + symbol**2 / d * (partial - previous)
    if not _eq(recurrence - (partial + term)):
        return None
    complement = (1 - symbol**2 / d) * (1 - partial) + symbol**2 / d * (1 - partial + previous)
    if not _eq(complement - (1 - partial - term)):
        return None
    first_partial = 1 - symbol**2 / 6
    if not _eq(denominators(1) / sp.factorial(3) - first_partial):
        return None
    if not _eq(first / sp.factorial(3) - (1 - first_partial)):
        return None
    if term.subs(n, 0) != 1:
        return None

    # On [0,pi/2], alternating terms decrease and S_N >= 1-pi^2/24>0.
    # The factorial ratio tends to zero, proving absolute convergence.
    k = sp.Dummy("k", integer=True, nonnegative=True)
    next_denominator = (2 * k + 2) * (2 * k + 3)
    if sp.expand(next_denominator - 6).is_nonnegative is not True:
        return None
    if (1 - sp.pi**2 / 24).is_positive is not True:
        return None
    if sp.limit(sp.pi**2 / (4 * next_denominator), k, sp.oo) != 0:
        return None
    total = sp.summation(
        (-1) ** k * symbol ** (2 * k) / sp.factorial(2 * k + 1), (k, 0, sp.oo)
    )
    if not _eq(total - sp.sin(symbol) / symbol):
        return None
    reduced = symbol / sp.sin(symbol) - 1
    if not _eq((1 - total) / total - reduced):
        return None
    if sp.limit(reduced, symbol, 0) != 0:
        return None
    csc_value = pack_gate._csc_catalan(symbol / sp.sin(symbol), symbol, lo, hi)
    return None if csc_value is None else sp.simplify(csc_value - (hi - lo))


def definite_value(integrand, symbol, lo, hi):
    for builder in (_atan_square, _log_sine_ratio, _atan_reciprocal_square, _sine_continued_fraction):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
