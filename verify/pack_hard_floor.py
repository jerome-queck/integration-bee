"""Checked interval and series reductions for four source-read floor integrals.

IndexedMaximum keeps the printed infinite maximum as a mathematical operator.
It has no evaluator: only the exact binary-digit certificate below assigns a
value to its integral. All matchers return before doing algebra on a miss.
"""

from __future__ import annotations

import sympy as sp


class IndexedMaximum(sp.Function):
    """The maximum of a one-variable Lambda on the supplied index set.

    The Lambda binds the index, so it cannot become a free integration parameter.
    No maximum is evaluated by this representation. In this module only the
    explicit set Naturals0 and the printed binary-floor body are certified.
    """

    nargs = 2

    def _latex(self, printer):
        function, domain = self.args
        if isinstance(function, sp.Lambda) and len(function.variables) == 1:
            index = printer._print(function.variables[0])
            return r"\max_{%s\in %s}\left(%s\right)" % (
                index,
                printer._print(domain),
                printer._print(function.expr),
            )
        return printer._print_Function(self)


def _eq(expr) -> bool:
    return expr == 0 or sp.simplify(expr) == 0


def _positive_floor_series_shape(integrand, symbol) -> bool:
    if not isinstance(integrand, sp.Sum) or len(integrand.limits) != 1:
        return False
    if len(integrand.limits[0]) != 3:
        return False
    index, start, stop = integrand.limits[0]
    if not isinstance(index, sp.Symbol) or index == symbol or (start, stop) != (1, sp.oo):
        return False
    fractional = symbol - sp.floor(symbol)
    body = sp.floor((index + 1) / fractional)**(-sp.floor(symbol)) / (index + 1)
    return integrand.function == body


def _binary_maximum_shape(integrand, symbol) -> bool:
    if not isinstance(integrand, IndexedMaximum):
        return False
    function, domain = integrand.args
    if domain != sp.S.Naturals0 or not isinstance(function, sp.Lambda) or len(function.variables) != 1:
        return False
    index = function.variables[0]
    if not isinstance(index, sp.Symbol) or index == symbol:
        return False
    body = sp.floor(2**(index + 1) * symbol) / 2**index - sp.floor(2**index * symbol) / 2**(index - 1)
    return function.expr == body


def open_integrand(integrand, symbol) -> bool:
    """Allow canonical storage of just the two literal nonclosed readings."""
    return _positive_floor_series_shape(integrand, symbol) or _binary_maximum_shape(integrand, symbol)


def _reciprocal_floor(integrand, symbol, lo, hi):
    if (lo, hi) != (0, 1) or not integrand.has(sp.floor):
        return None
    target = 1 / symbol - sp.floor(1 / symbol) - 1 / (symbol**2 * sp.floor(1 / symbol)**2)
    if integrand != target:
        return None
    y = sp.Dummy("y", positive=True)
    n = sp.Dummy("n", integer=True, positive=True)
    upper = sp.Dummy("N", integer=True, positive=True)
    transformed = -target.subs(symbol, 1 / y) * sp.diff(1 / y, y)
    expected = 1 / y - sp.floor(y) / y**2 - 1 / sp.floor(y)**2
    if not _eq(transformed - expected):
        return None
    # On (n,n+1), floor(y)=n. The endpoint values have measure zero.
    if sp.floor(n + sp.Rational(1, 2)) != n:
        return None
    piece = expected.xreplace({sp.floor(y): n})
    primitive = sp.log(y) + n / y - y / n**2
    if not _eq(sp.diff(primitive, y) - piece):
        return None
    area = primitive.subs(y, n + 1) - primitive.subs(y, n)
    term = sp.log(n + 1) - sp.log(n) - 1 / (n + 1) - 1 / n**2
    if not _eq(area - term):
        return None
    harmonic_partial = sp.log(upper + 1) - sp.harmonic(upper + 1) + 1
    if harmonic_partial.subs(upper, 0) != 0:
        return None
    difference = harmonic_partial.subs(upper, n) - harmonic_partial.subs(upper, n - 1)
    if not _eq(sp.expand_func(difference) - (term + 1 / n**2)):
        return None
    first = sp.limit(harmonic_partial, upper, sp.oo)
    second = sp.summation(1 / n**2, (n, 1, sp.oo))
    if first != 1 - sp.EulerGamma or second != sp.pi**2 / 6:
        return None
    # Both sums converge. In the original variable the fractional part is
    # bounded by 1 and 1/(x*floor(1/x)) is at most 2, so the endpoint is integrable.
    return first - second


def _alternating_floor_ceiling(integrand, symbol, lo, hi):
    if (lo, hi) != (1, sp.oo) or not integrand.has(sp.floor, sp.ceiling):
        return None
    lower = sp.floor(symbol)
    upper = sp.ceiling(symbol)
    target = (-1)**upper / (sp.sqrt(lower * upper) * (sp.sqrt(upper) - sp.sqrt(lower)))
    if integrand != target:
        return None
    n = sp.Dummy("n", integer=True, positive=True)
    if sp.floor(n + sp.Rational(1, 2)) != n or sp.ceiling(n + sp.Rational(1, 2)) != n + 1:
        return None
    term = target.xreplace({lower: n, upper: n + 1})
    rationalised = (-1)**(n + 1) * (1 / sp.sqrt(n) + 1 / sp.sqrt(n + 1))
    if not _eq(term - rationalised):
        return None
    partial = 1 + (-1)**(n + 1) / sp.sqrt(n + 1)
    if partial.subs(n, 0) != 0:
        return None
    if not _eq(partial - partial.subs(n, n - 1) - rationalised):
        return None
    # The partial-sum remainder has modulus 1/sqrt(N+1). An arbitrary real
    # upper endpoint adds at most one interval, bounded by the unsigned term.
    remainder = sp.limit(1 / sp.sqrt(n + 1), n, sp.oo)
    last_interval = sp.limit(1 / sp.sqrt(n) + 1 / sp.sqrt(n + 1), n, sp.oo)
    if remainder != 0 or last_interval != 0:
        return None
    return sp.Integer(1)


def _positive_floor_series(integrand, symbol, lo, hi):
    if (lo, hi) != (1, sp.oo) or not _positive_floor_series_shape(integrand, symbol):
        return None
    index = integrand.limits[0][0]
    body = integrand.function
    n = sp.Dummy("n", integer=True, positive=True)
    t = sp.Dummy("t", real=True)
    m = sp.Dummy("M", integer=True, positive=True)
    j = sp.Dummy("j", integer=True, positive=True)
    p = sp.Dummy("p", integer=True, nonnegative=True)
    # For x=n+t, 0<t<1, floor(x)=n and {x}=t. All summands are nonnegative,
    # and floor((k+1)/t)>=k+1>=2, so Tonelli permits both rearrangements below.
    if not _eq(sp.floor(n + t) - n - sp.floor(t)):
        return None
    on_interval = body.xreplace({sp.floor(symbol): n}).subs(symbol, n + t)
    expected = sp.floor((index + 1) / t)**(-n) / (index + 1)
    if not _eq(on_interval - expected):
        return None
    level = p + 2
    geometric = sp.summation(level**(-n), (n, 1, sp.oo))
    if not _eq(geometric - 1 / (level - 1)):
        return None
    # M=k+1. floor(M/t)=j on (M/(j+1),M/j], for integers j>=M>=2.
    length = m / j - m / (j + 1)
    area = length / (m * (j - 1))
    if not _eq(area - 1 / ((j - 1) * j * (j + 1))):
        return None
    multiplicity = sp.summation(1, (m, 2, j))
    if multiplicity != j - 1:
        return None
    collapsed = sp.cancel(multiplicity * area)
    if not _eq(collapsed - (1 / j - 1 / (j + 1))):
        return None
    value = sp.summation(collapsed, (j, 2, sp.oo))
    return value if value == sp.Rational(1, 2) else None


def _binary_maximum(integrand, symbol, lo, hi):
    if (lo, hi) != (0, 1) or not _binary_maximum_shape(integrand, symbol):
        return None
    k = sp.Dummy("k", integer=True, nonnegative=True)
    m = sp.Dummy("m", integer=True, nonnegative=True)
    t = sp.Dummy("t", real=True)
    j = sp.Dummy("j", integer=True, positive=True)
    # Write 2^n*x=m+u, 0<=u<1. The floor-translation identity shows that
    # the expression is floor(2u)/2^n, hence either 0 or 2^(-n).
    if not _eq(sp.floor(2 * (m + t)) - 2 * m - sp.floor(2 * t)):
        return None
    for bit in (0, 1):
        digit = sp.floor(2 * m + bit) / 2**k - m / 2**(k - 1)
        if not _eq(digit - bit / 2**k):
            return None
    # On [2^(-k-1),2^(-k)), write x=(1+t)/2^(k+1), 0<=t<1.
    # For n<k both floors vanish; at n=k they are 1 and 0. Later binary
    # digits are bounded by 2^(-n), which decreases by the checked factor 1/2.
    point = (1 + t) / 2**(k + 1)
    if not _eq(2**(k + 1) * point - (1 + t)) or not _eq(2**k * point - (1 + t) / 2):
        return None
    if not _eq(2**(k - j + 1) * point - (1 + t) / 2**j):
        return None
    height = 2**(-k)
    if sp.simplify(height.subs(k, k + 1) / height) != sp.Rational(1, 2):
        return None
    length = 2**(-k) - 2**(-k - 1)
    if not _eq(height * length - 2**(-2 * k - 1)):
        return None
    # These disjoint dyadic intervals partition (0,1); the endpoints x=0,1
    # have zero measure. The integrand is nonnegative, so the areas add.
    value = sp.summation(height * length, (k, 0, sp.oo))
    return value if value == sp.Rational(2, 3) else None


def definite_value(integrand, symbol, lo, hi):
    """Return a checked definite value, or None for an unrecognised reading."""
    for builder in (
        _reciprocal_floor,
        _alternating_floor_ceiling,
        _positive_floor_series,
        _binary_maximum,
    ):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            return value
    return None
