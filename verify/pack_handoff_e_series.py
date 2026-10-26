"""Exact series certificates for the two Handoff E Round 1 integrals.

The 2020 answer is literally the convergent sum printed in its answer sheet.
Only that exact sum, with its original integral and bounds, bypasses the
ordinary closed-answer guard. The 2021 certificate uses finite floor pieces
and a finite product before taking any limit.
"""

from __future__ import annotations

import sympy as sp


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ValueError("handoff-e series certificate: " + label)


def _eq(expr):
    return expr == 0 or sp.simplify(expr) == 0


def open_answer_ok(integrand, answer, symbol, lo, hi):
    """Prove the literal sophomore's-dream sum, and no other open answer."""
    if integrand != symbol ** (-symbol) or (lo, hi) != (0, 1):
        return None
    if not isinstance(answer, sp.Sum) or len(answer.limits) != 1:
        return False
    index, start, stop = answer.limits[0]
    if (
        not isinstance(index, sp.Symbol)
        or index.name == symbol.name
        or index.is_integer is not True
        or index.is_positive is not True
        or (start, stop) != (1, sp.oo)
        or answer.function != index ** (-index)
    ):
        return False

    # On 0<x<=1, -x*log(x)>=0. Every term in the exponential series is
    # nonnegative, so monotone convergence permits termwise integration.
    n = sp.Symbol("_he_n", integer=True, nonnegative=True)
    z = sp.Symbol("_he_z", nonnegative=True)
    x, u, c = sp.symbols("_he_x _he_u _he_c", positive=True)
    _require(sp.summation(z**n / sp.factorial(n), (n, 0, sp.oo)) == sp.exp(z), "exp-series")
    _require(_eq(sp.exp(-x * sp.log(x)) - x ** (-x)), "power-rewrite")
    _require(sp.limit(sp.exp(-u), u, sp.oo) == 0, "lower-endpoint")
    _require(sp.exp(-u).subs(u, 0) == 1, "upper-endpoint")
    term = (-x * sp.log(x)) ** n / sp.factorial(n)
    transformed = term.subs(x, sp.exp(-u)) * sp.exp(-u)
    kernel = u**n * sp.exp(-(n + 1) * u) / sp.factorial(n)
    _require(_eq(transformed - kernel), "log-substitution")
    _require(kernel.is_nonnegative is True, "nonnegative-terms")
    moment = sp.integrate(u**n * sp.exp(-c * u), (u, 0, sp.oo)) / sp.factorial(n)
    moment = sp.simplify(moment.subs(c, n + 1))
    _require(_eq(moment - (n + 1) ** (-n - 1)), "gamma-moment")
    _require(_eq(moment.subs(n, index - 1) - answer.function), "reindex")

    # The resulting series is finite: k**(-k)<=2**(-k) for k>=2.
    # This bound is independent of any numerical estimate of the integral.
    count = sp.Symbol("_he_N", integer=True, positive=True)
    tail = sp.summation(2 ** (-index), (index, count + 1, sp.oo))
    _require(_eq(tail - 2 ** (-count)), "geometric-majorant")
    _require(sp.limit(tail, count, sp.oo) == 0, "majorant-tail")
    return True


def definite_value(integrand, symbol, lo, hi):
    """Fractional tangent: finite summation by parts, then a gamma product."""
    expected = sp.frac(sp.tan(symbol)) / sp.tan(symbol)
    if integrand != expected or (lo, hi) != (0, sp.pi / 2):
        return None
    u = sp.Symbol("_he_u", positive=True)
    k = sp.Symbol("_he_k", integer=True, positive=True)
    count = sp.Symbol("_he_N", integer=True, positive=True)
    changed = integrand.subs(symbol, sp.atan(u)) * sp.diff(sp.atan(u), u)
    _require(_eq(changed - sp.frac(u) / (u * (1 + u**2))), "tangent-substitution")
    _require(sp.atan(0) == 0 and sp.limit(sp.atan(u), u, sp.oo) == sp.pi / 2, "tangent-endpoints")
    # On [k,k+1), frac(u)=u-k. The k=0 interval is regular, and the
    # integer endpoints are a null set. First integrate only to N+1.
    _require(_eq((u - k) / (u * (1 + u**2)) - (1 / (1 + u**2) - k / (u * (1 + u**2)))), "floor-piece")
    primitive = sp.log(u) - sp.log(1 + u**2) / 2
    _require(_eq(sp.diff(primitive, u) - 1 / (u * (1 + u**2))), "piece-primitive")
    h = sp.log(1 + 1 / u**2)
    _require(_eq(primitive + h / 2), "positive-log-identity")
    piece = k * (primitive.subs(u, k + 1) - primitive.subs(u, k))
    _require(_eq(piece - k * (h.subs(u, k) - h.subs(u, k + 1)) / 2), "piece-endpoints")

    # Write L_N=sum_{k=1}^N h(k)=log(prod_{k=1}^N(1+1/k**2)).
    # All factors are positive, so this uses the real logarithm. Induction
    # gives sum k*(h(k)-h(k+1)) = L_N-N*h(N+1). Check its base and step.
    prior, current, following = sp.symbols("_he_L _he_h _he_next", real=True)
    finite = prior + current - count * following
    previous = prior - (count - 1) * current
    _require(sp.expand(finite - previous - count * (current - following)) == 0, "finite-sum-step")
    _require(sp.expand(finite.subs({prior: 0, count: 1}) - (current - following)) == 0, "finite-sum-base")
    product = sp.product(1 + 1 / k**2, (k, 1, count))
    _require(not product.has(sp.Product, sp.Sum), "finite-product")
    _require(_eq(product.subs(count, 1) - 2), "product-base")
    # SymPy takes the limit of the exact rising-factorial product and
    # simplifies Gamma(1+i)*Gamma(1-i) by reflection, not by quadrature.
    product_limit = sp.simplify(sp.limit(product, count, sp.oo))
    _require(_eq(product_limit - sp.sinh(sp.pi) / sp.pi), "product-limit")
    _require(product_limit.is_positive is True, "real-log-limit")
    boundary = count * sp.log(1 + 1 / (count + 1) ** 2)
    _require(sp.limit(boundary, count, sp.oo) == 0, "summation-boundary")
    base = sp.integrate(1 / (1 + u**2), (u, 0, count + 1))
    base_limit = sp.limit(base, count, sp.oo)
    _require(base_limit == sp.pi / 2, "cauchy-integral")
    # The improper integral exists: 0<=frac(u)/(u*(1+u**2))<=1/u**3
    # for u>=1. Thus the finite endpoints recover the original integral.
    tail_major = sp.integrate(u ** (-3), (u, count + 1, sp.oo))
    _require(sp.limit(tail_major, count, sp.oo) == 0, "improper-tail")
    return base_limit - sp.log(product_limit) / 2
