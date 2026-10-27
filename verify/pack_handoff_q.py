"""Exact finite-product certificate for Tournament 2024, Battle 4 Fight 2.

The printed condition m,n in Z with m>n is encoded bijectively as an
arbitrary integer m and a positive integer d=m-n, so n=m-d. The literal
product, numerator and both integration bounds remain in the input. The
derived answer is pi/2**m; the PDFs' pi/2**(m-2*n) has the wrong Jacobian.
No catalog id or submitted answer participates in recognizing the integral.
"""

from __future__ import annotations

from functools import lru_cache

import sympy as sp


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ArithmeticError("handoff-q certificate: " + label)


def _parameters(integrand, symbol):
    products = list(integrand.atoms(sp.Product))
    if len(products) != 1 or symbol.is_real is not True:
        return None
    product = products[0]
    if len(product.limits) != 1 or len(product.limits[0]) != 3:
        return None
    index, start, gap = product.limits[0]
    if (
        not isinstance(index, sp.Symbol)
        or index.is_integer is not True
        or start != 1
        or not isinstance(gap, (sp.Symbol, sp.Integer))
        or gap.is_integer is not True
        or gap.is_positive is not True
        or product.function.func != sp.cos
    ):
        return None
    # The product's frequency determines m independently of the numerator.
    # Rational powers of two also admit exact, concrete (m,n) regressions.
    frequency = sp.simplify(product.function.args[0] * 2**index / symbol)
    if frequency.is_Pow and frequency.base == 2:
        power = frequency.exp
    elif frequency.is_Rational and frequency.is_positive:
        power = sp.log(frequency, 2)
    else:
        return None
    if not isinstance(power, (sp.Symbol, sp.Integer)) or power.is_integer is not True:
        return None
    symbols = {symbol, index} | power.free_symbols | gap.free_symbols
    if len(symbols) != 2 + len(power.free_symbols) + len(gap.free_symbols):
        return None
    if len({item.name for item in symbols}) != len(symbols):
        return None
    expected = (
        sp.sin((2**power + 2025 * 2**(power-gap)) * symbol)
        / sp.sin(2**power * symbol)
        * sp.Product(sp.cos(2**(power-index) * symbol), (index, 1, gap))
    )
    if integrand != expected:
        return None
    return power, gap, product


def open_integrand(integrand, symbol) -> bool:
    """Admit only the source's finite product with its parameter assumptions."""
    return _parameters(integrand, symbol) is not None


@lru_cache(maxsize=1)
def _finite_identities():
    """Prove both identities by induction, without sampling the parameters."""
    y = sp.Dummy("y", real=True)
    scale = sp.Dummy("scale", positive=True)
    step = sp.Dummy("step", integer=True, nonnegative=True)
    mode = sp.Dummy("mode", integer=True, positive=True)

    # P_d(y)=prod(j=0..d-1, cos(2**j*y)). P_0=1, and adjoining
    # cos(2**d*y) doubles the frequency in sin(2**d*y)/(2**d*sin(y)).
    product_form = sp.sin(scale*y) / (scale*sp.sin(y))
    _require(product_form.subs(scale, 1) == 1, "empty product")
    recurrence = product_form.subs(scale, 2*scale) - product_form*sp.cos(scale*y)
    _require(sp.trigsimp(recurrence) == 0, "double-angle induction")
    _require(sp.simplify(2**(step+1) - 2*2**step) == 0, "binary frequency step")

    # D_L=sin((2L+1)y)/sin(y)=1+2*sum(j=1..L, cos(2jy)).
    # The cross-multiplied recurrence avoids all removable zeros of sin(y).
    _require(sp.sin((2*step+1)*y).subs(step, 0) == sp.sin(y), "kernel base")
    recurrence = (
        sp.sin((2*mode+1)*y) - sp.sin((2*mode-1)*y)
        - 2*sp.sin(y)*sp.cos(2*mode*y)
    )
    _require(sp.trigsimp(recurrence, method="fu") == 0, "kernel induction")
    _require(sp.integrate(sp.cos(2*mode*y), (y, 0, sp.pi)) == 0,
             "every nonconstant Fourier mode")
    # Each sum is finite, hence continuous and integrable on [0,pi]. It
    # supplies the removable extension at both endpoints; no infinite sum
    # or limit is interchanged with integration.
    return sp.integrate(sp.Integer(1), (y, 0, sp.pi))


def doubled_sine_product_value(integrand, symbol, lo, hi):
    """Return the derived value only after checking the full source family."""
    parameters = _parameters(integrand, symbol)
    if parameters is None:
        return None
    power, gap, product = parameters
    lower_power = power - gap
    if lo != 0 or hi != sp.pi / 2**lower_power:
        return None

    y = sp.Dummy("y", real=True)
    index = product.limits[0][0]
    inverse = y / 2**lower_power
    jacobian = sp.diff(inverse, y)
    _require(jacobian.is_positive is True, "positive substitution Jacobian")
    _require(inverse.subs(y, 0) == lo and inverse.subs(y, sp.pi) == hi,
             "substitution endpoints")
    _require(sp.simplify(2**lower_power * inverse - y) == 0, "inverse substitution")
    changed_factor = product.function.subs(symbol, inverse)
    _require(sp.simplify(changed_factor - sp.cos(2**(gap-index)*y)) == 0,
             "every product frequency")
    # j=d-k maps k=1..d bijectively to j=d-1..0 in P_d above.
    reverse_index = gap-index
    _require(reverse_index.subs(index, 1) == gap-1
             and reverse_index.subs(index, gap) == 0, "finite product reindexing")

    kernel_integral = _finite_identities()
    product_form = sp.sin(2**power * symbol) / (2**gap * sp.sin(2**lower_power * symbol))
    reduced = integrand.xreplace({product: product_form})
    frequency = 2**gap + 2025
    kernel = sp.sin(frequency*y) / sp.sin(y)
    _require(sp.simplify(reduced.subs(symbol, inverse)*jacobian - kernel/2**power) == 0,
             "product cancellation and Jacobian")

    degree = 2**(gap-1) + 1012
    _require(degree.is_integer is True and degree.is_positive is True,
             "finite positive kernel degree")
    _require(sp.simplify(frequency - (2*degree+1)) == 0, "odd kernel frequency")
    # For each finite d, the original denominator has only finitely many
    # zeros. The checked identities give a continuous cosine-polynomial
    # extension at all of them, so cancellation preserves the integral.
    return sp.simplify(jacobian * kernel_integral / 2**gap)


def definite_answer_ok(integrand, symbol, lo, hi, answer):
    """Compare in the admitted input's parameter domain, retaining signs.

    A learner's bare ``m`` denotes the input's integer m. Bind only bare
    names to the explicitly assumed input symbols, leaving unrelated or
    differently assumed symbols untouched. This lets the catalog store the
    ordinary answer text pi/2**m without changing other grading contracts.
    """
    value = doubled_sine_product_value(integrand, symbol, lo, hi)
    if value is None:
        return None
    if not isinstance(answer, sp.Expr) or answer.has(
        sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.Derivative,
        sp.nan, sp.zoo, sp.oo, -sp.oo,
    ):
        return False
    parameters = integrand.free_symbols - {symbol}
    contextual = answer.xreplace({sp.Symbol(item.name): item for item in parameters})
    return sp.simplify(value - contextual) == 0
