"""Source-faithful nonintegral answer contracts for Handoff F.

The question remains in the stored expression: two complete integrals for a
comparison, an integral equation for a function, the original finite sum or
product inside its limit, or a root count on its stated half-open interval.
These are not ordinary definite integrals with convenient scalar proxies.

The literal shapes below are the entire whitelist.  Positive root indices in
the comparison are explicit assumptions; the source's real-root notation is
read on that domain.  Function answers are C1 functions on the real line.
"""

from __future__ import annotations

import sympy as sp
from sympy.core.function import AppliedUndef


class RootCount(sp.Function):
    """Number of distinct zeros of args[0] in args[2], with variable args[1]."""

    nargs = 3


KINDS = frozenset({"comparison", "function", "expression", "root_count"})
EQUAL_VERDICT = sp.Symbol("I=J")


def _require(condition, label):
    if condition is not True and condition != sp.true:
        raise ArithmeticError("handoff-f-expressions: " + label)


def _zero(expr):
    return expr == 0 or sp.simplify(expr) == 0


def _comparison_form(expr, symbol):
    if not isinstance(expr, sp.Tuple) or len(expr) != 2:
        return None
    left, right = expr
    if not all(isinstance(item, sp.Integral) for item in expr):
        return None
    if left.limits != ((symbol, 0, 1),) or right.limits != ((symbol, 0, 1),):
        return None
    parameters = left.function.free_symbols - {symbol}
    if len(parameters) != 2:
        return None
    if any(not isinstance(p, sp.Symbol) or p.is_positive is not True
           or p.name == symbol.name for p in parameters):
        return None
    first, second = sorted(parameters, key=sp.default_sort_key)
    for a, b in ((first, second), (second, first)):
        expected_left = (1 - symbol**b)**(1 / a)
        expected_right = (1 - symbol**a)**(1 / b)
        if left.function == expected_left and right.function == expected_right:
            return a, b
    return None


def _function_form(expr, symbol):
    if not isinstance(expr, sp.Equality) or expr.rhs != 1:
        return None
    integrals = list(expr.lhs.atoms(sp.Integral))
    if len(integrals) != 1:
        return None
    inner = integrals[0]
    if len(inner.limits) != 1 or len(inner.limits[0]) != 3:
        return None
    dummy, lower, upper = inner.limits[0]
    if (not isinstance(dummy, sp.Symbol) or dummy.is_real is not True
            or dummy.name == symbol.name or (lower, upper) != (0, symbol)):
        return None
    term = inner.function
    if not isinstance(term, AppliedUndef) or term.args != (dummy,):
        return None
    if expr.lhs != term.func(symbol) - inner:
        return None
    return term.func, dummy


def _expression_form(expr, symbol):
    if not isinstance(expr, sp.Limit) or len(expr.args) != 4:
        return None
    body, n, destination, _direction = expr.args
    if (not isinstance(n, sp.Symbol) or n.is_positive is not True
            or n.is_integer is not True or n.name == symbol.name
            or destination != sp.oo or expr != sp.Limit(body, n, sp.oo)):
        return None
    for cls, name in ((sp.Sum, "harmonic"), (sp.Product, "product")):
        atoms = list(body.atoms(cls))
        if len(atoms) != 1:
            continue
        finite = atoms[0]
        if len(finite.limits) != 1 or len(finite.limits[0]) != 3:
            continue
        k, lower, upper = finite.limits[0]
        if (not isinstance(k, sp.Symbol) or k.is_integer is not True
                or k.is_positive is not True or k.name in {n.name, symbol.name}
                or (lower, upper) != (1, n)):
            continue
        if name == "harmonic":
            expected = sp.Sum(1 / (n + k), (k, 1, n))
        else:
            expected = sp.Product(n + k, (k, 1, n))**(1 / n) / n
        if body == expected:
            return name, n, k
    return None


def _root_form(expr, symbol):
    if not isinstance(expr, RootCount) or len(expr.args) != 3:
        return None
    primitive, variable, interval = expr.args
    if variable != symbol or interval != sp.Interval.Lopen(0, 2 * sp.pi):
        return None
    if not isinstance(primitive, sp.Integral) or len(primitive.limits) != 1:
        return None
    bound = primitive.limits[0]
    if len(bound) != 3:
        return None
    t, lower, upper = bound
    if (not isinstance(t, sp.Symbol) or t.is_real is not True
            or t.name == symbol.name or (lower, upper) != (0, symbol)
            or primitive.function != sp.sin(sp.sin(t))):
        return None
    return t


def open_expression(kind, expr, symbol):
    """Recognize only the full original questions, including their domains."""
    if symbol.is_real is not True:
        return False
    matchers = {
        "comparison": _comparison_form,
        "function": _function_form,
        "expression": _expression_form,
        "root_count": _root_form,
    }
    matcher = matchers.get(kind)
    return matcher is not None and matcher(expr, symbol) is not None


def _comparison_value(a, b):
    u = sp.Symbol("_f_u", positive=True)
    # With x=u**(1/b), dx=u**(1/b-1)/b du. Both beta arguments are
    # positive, so the beta integrals converge. The same substitution with
    # a and b exchanged handles J. No complex branches are used.
    mapping = u**(1 / b)
    _require(_zero(sp.diff(mapping, u) - u**(1 / b - 1) / b), "beta Jacobian")
    _require(sp.diff(mapping, u).is_positive is True, "beta orientation")
    _require(mapping.subs(u, 0) == 0 and mapping.subs(u, 1) == 1, "beta endpoints")
    _require(sp.powdenest(mapping**b) == u, "beta power substitution")
    _require((1 / b).is_positive is True and (1 + 1 / a).is_positive is True,
             "beta convergence")
    left = sp.beta(1 / b, 1 + 1 / a) / b
    right = sp.beta(1 / a, 1 + 1 / b) / a
    symmetric = sp.gamma(1 / a) * sp.gamma(1 / b) / (
        a * b * sp.gamma(1 + 1 / a + 1 / b)
    )
    _require(_zero(sp.expand_func(left.rewrite(sp.gamma)) - symmetric), "beta left")
    _require(_zero(sp.expand_func(right.rewrite(sp.gamma)) - symmetric), "beta right")
    return EQUAL_VERDICT


def _function_value(symbol):
    t = sp.Symbol("_f_t", real=True)
    f = sp.Function("_f")
    answer = sp.exp(symbol)
    _require(_zero(answer - sp.integrate(sp.exp(t), (t, 0, symbol)) - 1),
             "Volterra substitution")
    # In the C1 class the fundamental theorem gives f'=f, and setting x=0
    # gives f(0)=1. Multiplication by exp(-x) has zero derivative; hence it
    # is the constant 1 on R. This proves uniqueness, not only substitution.
    _require(_zero(sp.diff(sp.exp(-symbol) * f(symbol), symbol)
                   - sp.exp(-symbol) * (sp.diff(f(symbol), symbol) - f(symbol))),
             "Volterra integrating factor")
    _require(answer.subs(symbol, 0) == 1, "Volterra initial value")
    _require(_zero(sp.diff(answer, symbol) - answer), "Volterra ODE")
    return answer


def function_answer_ok(answer, symbol):
    """Check a candidate in the C1-on-R class, including its initial value."""
    if (not isinstance(answer, sp.Expr) or answer.free_symbols - {symbol}
            or answer.has(sp.Integral, sp.Sum, sp.Product, sp.Limit, sp.Derivative)
            or answer.atoms(AppliedUndef)):
        return False
    try:
        domain = sp.calculus.util.continuous_domain(answer, symbol, sp.S.Reals)
        derivative = sp.diff(answer, symbol)
        derivative_domain = sp.calculus.util.continuous_domain(derivative, symbol, sp.S.Reals)
        return (domain == derivative_domain == sp.S.Reals
                and _zero(derivative - answer)
                and _zero(answer.subs(symbol, 0) - 1))
    except (NotImplementedError, ValueError, TypeError):
        return False


def _harmonic_value(n, k):
    u = sp.Symbol("_f_u", nonnegative=True)
    finite_sum = sp.Sum(1 / (n + k), (k, 1, n))
    harmonic_difference = sp.harmonic(2 * n) - sp.harmonic(n)
    _require(finite_sum.change_index(k, k + n) == sp.Sum(1 / k, (k, n + 1, 2 * n)),
             "harmonic reindexing")
    _require(harmonic_difference.subs(n, 1) == sp.Rational(1, 2), "harmonic base")
    # Raising n by one drops the term 1/(n+1) and appends the terms
    # 1/(2n+1),1/(2n+2). The harmonic difference has the same increment.
    increment = 1 / (2 * n + 1) + 1 / (2 * n + 2) - 1 / (n + 1)
    _require(_zero(sp.expand_func(harmonic_difference.subs(n, n + 1)
                                 - harmonic_difference) - increment), "harmonic recurrence")
    # For decreasing h(u)=1/(n+u), each h(k) lies between its integrals
    # over [k,k+1] and [k-1,k]. Summing k=1..n bounds the ENTIRE stored
    # sum between these two integrals; these are bounds, not its definition.
    kernel = 1 / (n + u)
    _require(sp.diff(kernel, u).is_negative is True, "harmonic decreasing kernel")
    lower = sp.integrate(kernel, (u, 1, n + 1))
    upper = sp.integrate(kernel, (u, 0, n))
    lower_limit = sp.limit(lower, n, sp.oo)
    upper_limit = sp.limit(upper, n, sp.oo)
    _require(lower_limit == upper_limit == sp.log(2), "harmonic squeeze")
    return lower_limit


def _product_value(n, k):
    finite_product = sp.Product(n + k, (k, 1, n))
    gamma_ratio = sp.gamma(2 * n + 1) / sp.gamma(n + 1)
    _require((n + k).is_positive is True, "product positive factors")
    _require(_zero(finite_product.doit().rewrite(sp.gamma) / gamma_ratio - 1),
             "finite product gamma identity")
    # Every factor and n are positive, so the real nth root and logarithm
    # are single-valued. log Gamma is real on these positive arguments;
    # SymPy's exact asymptotic limit implements Stirling's formula. The
    # normalized logarithm is that of the COMPLETE original product limit.
    logarithm = (sp.loggamma(2 * n + 1) - sp.loggamma(n + 1)) / n - sp.log(n)
    logarithm_limit = sp.limit(logarithm, n, sp.oo)
    _require(_zero(logarithm_limit - (2 * sp.log(2) - 1)), "Stirling logarithm limit")
    _require(logarithm_limit.is_real is True and logarithm_limit.is_finite is True,
             "exponential continuity")
    return sp.simplify(sp.exp(logarithm_limit))


def _root_value(t):
    # sin is continuous, has no zero on (0,pi), and is 1 at pi/2; hence
    # it is strictly positive there. Its range on [0,pi] is [0,1].
    first_half = sp.Interval.open(0, sp.pi)
    _require(sp.solveset(sp.sin(t), t, domain=first_half) == sp.EmptySet,
             "inner sine zeros")
    _require(sp.sin(sp.pi / 2) == 1, "inner sine positive point")
    _require(sp.calculus.util.continuous_domain(sp.sin(t), t, sp.S.Reals) == sp.S.Reals,
             "sine continuity")
    _require(sp.calculus.util.function_range(sp.sin(t), t, sp.Interval(0, sp.pi))
             == sp.Interval(0, 1), "inner sine range")
    # sin has no zero on (0,1] and sin(1)>0. Therefore sin(sin(t))>0
    # on (0,pi). The exact half-period identity makes it strictly negative
    # on (pi,2pi), and cancels the two half-period integrals.
    _require(sp.solveset(sp.sin(t), t, domain=sp.Interval.Lopen(0, 1)) == sp.EmptySet,
             "outer sine zeros")
    _require(sp.sin(1).is_positive is True, "outer sine positive point")
    kernel = sp.sin(sp.sin(t))
    _require(sp.trigsimp(kernel.subs(t, t + sp.pi) + kernel) == 0,
             "root half-period cancellation")
    _require(kernel.is_real is True, "real continuous kernel")
    # Thus F(0)=F(2pi)=0, F strictly increases and then strictly decreases.
    # Its only roots on [0,2pi] are the endpoints; the stored domain excludes
    # 0 and includes 2pi. Changing either endpoint is rejected by _root_form.
    interval = sp.Interval.Lopen(0, 2 * sp.pi)
    _require(interval.contains(0) == sp.false and interval.contains(2 * sp.pi) == sp.true,
             "root interval endpoints")
    return sp.Integer(1)


def answer_value(kind, expr, symbol, limits):
    """Derive the answer for a typed original expression; None means no match."""
    if limits is not None or not open_expression(kind, expr, symbol):
        return None
    if kind == "comparison":
        return _comparison_value(*_comparison_form(expr, symbol))
    if kind == "function":
        return _function_value(symbol)
    if kind == "root_count":
        return _root_value(_root_form(expr, symbol))
    name, n, k = _expression_form(expr, symbol)
    return _harmonic_value(n, k) if name == "harmonic" else _product_value(n, k)


def transcripts():
    """id -> (kind, full SymPy question, limits, SymPy answer, variable name)."""
    x, t = sp.symbols("x t", real=True)
    a, b = sp.symbols("a b", positive=True)
    n, k = sp.symbols("n k", integer=True, positive=True)
    f = sp.Function("f")
    return {
        "R2-2022-Relay-Q01": (
            "comparison",
            sp.Tuple(sp.Integral((1 - x**b)**(1 / a), (x, 0, 1)),
                     sp.Integral((1 - x**a)**(1 / b), (x, 0, 1))),
            None, EQUAL_VERDICT, "x",
        ),
        "R2-2022-Relay-Q09": (
            "function", sp.Eq(f(x) - sp.Integral(f(t), (t, 0, x)), 1, evaluate=False),
            None, sp.exp(x), "x",
        ),
        "R2-2022-Relay-Q12": (
            "expression", sp.Limit(sp.Sum(1 / (n + k), (k, 1, n)), n, sp.oo),
            None, sp.log(2), "x",
        ),
        "R2-2022-Relay-Q13": (
            "root_count", RootCount(sp.Integral(sp.sin(sp.sin(t)), (t, 0, x)),
                                    x, sp.Interval.Lopen(0, 2 * sp.pi)),
            None, sp.Integer(1), "x",
        ),
        "R2-2023-Relay-Q11": (
            "expression", sp.Limit(sp.Product(n + k, (k, 1, n))**(1 / n) / n, n, sp.oo),
            None, 4 / sp.E, "x",
        ),
    }
