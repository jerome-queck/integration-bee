"""Prove a layout reading against a mark-scheme reading.

A row is gated only when SymPy differentiates an indefinite answer back to the
integrand, or evaluates a definite integral to the printed answer. When the
direct value stays an unevaluated Integral, SymPy may still prove the printed
answer by an algebraic identity: the even part on symmetric limits, King's
reflection on a finite interval starting at 0, a constant sum f(x)+f(b-x) on
[0, b], the reciprocal substitution on (0, oo), a floor sum from 0 to
infinity, an integral with the other symbols taken positive, or the
substitution x = exp(-u) on [0, 1] when the integrand contains a logarithm.
A reduced integrand has to be simpler, and its evaluated value has to match.
Further checked reductions are an inverse-trig complement on a positive
argument (including an even power of a real expression), a reciprocal
substitution on an interval [a, 1/a], a logarithm on (0, oo) turned into an
even integral, an exponential rewrite of a hyperbolic function to a rational
function, a multiple-angle form of a rational function of sine and cosine, and
a square-root of 1 ± sin or 1 ± cos rewritten as an absolute value. A checked
functional equation also evaluates log(sin) on [0, pi/2], and that value is
reused for the tangent substitution of log(1+x**2)/(1+x**2) and for
integration by parts of x cot(x). Other checked forms are a reflection whose
log factors multiply to a constant, a square-root substitution that leaves an
inverse-tangent complement, a power of tangent that averages to 1/2, a
parameter derivative reduced by the tangent substitution, a split of
log(x+1/x)/(x+1/x), the Taylor series of log(1-x) with absolutely convergent
term integrals, integration by parts down to a beta integral, an explicit
arcsine antiderivative, and the Fourier series of the real part of exp(c e^{ix}).
A single letter of integration other than x is stored as x when x is not
already a parameter. The letter i in a layout reading is the imaginary unit.
The letter G in a mark scheme is Catalan's constant. Further checked forms
are the Catalan series for log(tan) on [0, π/4], the semicircle substitution
for log(x)/sqrt(4x-x^2), the shift x = tan θ - 1 for log(x)/(x^2+2x+2),
integration by parts of log(1-x)log(1+x), Fubini for x csc(x), the odd-zeta
series for log((e^x+1)/(e^x-1)), atan(x^n)/x, log(1+x)/(1+x^2), a symmetric
cosine product, a power substitution for 1/(n x^n+x), the gamma reflection
on [0, 1], a finite ceiling-floor sum, a quadratic log of sine and cosine,
and a square-root branch fixed by one interior point. Further checked
forms are ∫(x**p-x**q)/log(x) on [0, 1], log(x)/(x**2+3) on [1, 3],
1/(a**2-sin**2 x) on [0, π/2] for a>1, 1/(x**4+2 a x**2+1) on [0, ∞),
(1-x)/((1+x) sqrt(x+x**2+x**3)) on [0, 1], and a constant on each
integer interval of a power of floor.
Further checked forms are a constant sum of reciprocal square roots of
logarithms on a finite interval, the beta evaluation of a power of tangent,
a cosine modulus through the half-angle
substitution, geometric series for x**n/(exp(x)±1), a shift of log gamma, a
sine weight on log gamma, a product of sines, cot(x) log(sec x), the
derivative of a polylog in x**x, log(1+tan x) on [0, π/4], odd-zeta series,
a damped (t-sin t)/t**2 integral, a sine-square substitution, the Wallis
product, an artanh series reduced to the Wallis integral, and a Chebyshev
reduction. A reciprocal power that clears to a rational function is integrated
directly. (cos(a x)-cos(b x))/x**2 on [0, ∞) reduces by parts to the Dirichlet
integral, for positive a and b. A logarithm of an absolute value differentiates as the logarithm
of its argument. An indefinite answer is also accepted when its derivative
matches the integrand for a positive variable. Further checked forms are a
complement of two square-root logarithms on [2, 4], a fifth power of a
cosine-sine mean on [0, π/2], a root-exponential reflection on [-π/2, π/2],
1/(1+|cos x|) on [0, 2π], a shifted square-root logarithm reduced to a gamma
value, an arcsec substitution on [1, ∞), and an even power of cosine on a full
period reduced by the Wallis recurrence. Those seven patterns are checked before
the general reductions. Further checked forms are acosh(sin+cos) on [0, π/2],
atan(log(x)/(1+x)) on [1, e], a logistic composition on [1/4, 3/4],
(atan(x/a)+atan(x/b))/x between positive endpoints, floor pieces of
x**({x}-1)*(log(x**x)+{x}) on [0, 100], floor(1/x) on (0, 1], an alternating
power of a fractional part, a cube-root floor on (0, 1], the two integrals
equal to 1-γ, and x**2*cos(x)/(1+e**x) on [-π/2, π/2]. A positive integer
power of sec+tan differentiates from the symbolic exponent. Further checked
forms are log(1+x+x**2)/x on [0, 1], (log x/x)**n on [1, ∞), x{1/x}floor(1/x)
on [0, 1], a double Lambert W, reciprocal cube roots on [0, 7], an arcsine
product on [0, 1], cos(log x)/(1+x)**2, an inverse pair on [1, e], sin(π floor x),
the central binomial series on [0, 1/4], and a factorial-exponent power. When x
is already a parameter, the printed letter of integration stays. Numeric agreement
is not a proof.
"""

from __future__ import annotations

import multiprocessing as mp

import sympy as sp

import check_math

PROOF_TIMEOUT = 20.0


def namespace(variable: str) -> dict:
    ns = dict(check_math.NS)
    ns["ln"] = ns["log"]
    ns["Abs"] = sp.Abs
    ns["LambertW"] = sp.LambertW
    ns["acot"] = sp.acot
    ns["asec"] = sp.asec
    ns["acsc"] = sp.acsc
    ns["acosh"] = sp.acosh
    ns["atanh"] = sp.atanh
    ns["asech"] = sp.asech
    ns["acsch"] = sp.acsch
    ns["acoth"] = sp.acoth
    ns["sech"] = sp.sech
    ns["csch"] = sp.csch
    ns["coth"] = sp.coth
    ns["zeta"] = sp.zeta
    ns["gamma"] = sp.gamma
    ns["binomial"] = sp.binomial
    ns["G"] = sp.Catalan
    ns["EulerGamma"] = sp.EulerGamma
    ns["i"] = sp.I
    ns[variable] = sp.symbols(variable, real=True)
    ns["C"] = sp.Symbol("C")
    return ns


def _parse(text: str, variable: str):
    # A mark scheme can print a chain of equal values. Evaluating that chain
    # collapses a true link to True and the next link to False.
    if "Eq(" in text:
        with sp.evaluate(False):
            return sp.sympify(text, locals=namespace(variable))
    return sp.sympify(text, locals=namespace(variable))


def _unwrap_equality(expr):
    """Keep the right-hand side of a chain only when every link is an identity."""
    steps = 0
    while isinstance(expr, sp.Equality):
        steps += 1
        if steps > 4:
            return None
        left = _unwrap_equality(expr.lhs) if isinstance(expr.lhs, sp.Equality) else expr.lhs
        right = _unwrap_equality(expr.rhs) if isinstance(expr.rhs, sp.Equality) else expr.rhs
        if left is None or right is None or not _zero(left - right):
            return None
        expr = right
    return expr


def _answer_expr(text: str, variable: str):
    expr = _parse(text, variable)
    if isinstance(expr, sp.Equality):
        expr = _unwrap_equality(expr)
        if expr is None:
            return None
    constant = sp.Symbol("C")
    if not expr.has(constant):
        # Expanding (sec+tan)^n for a large printed n is not a proof, and it
        # hides the compact antiderivative the derivative check needs.
        if _large_integer_power(expr):
            return expr
        return sp.expand(expr).subs(constant, 0)
    expanded = sp.expand(expr)
    cleaned = expanded.subs(constant, 0)
    delta = sp.simplify(expanded - cleaned)
    symbol = namespace(variable)[variable]
    if delta.has(symbol) or not _closed(delta) or cleaned.has(constant):
        return None
    return cleaned


def _closed(expr) -> bool:
    if expr is None:
        return False
    if isinstance(expr, (int, float)):
        return True
    has = getattr(expr, "has", None)
    if has is None:
        return False
    if has(sp.Integral) or has(sp.Sum) or has(sp.Product):
        return False
    return True


def _zero(expr) -> bool:
    if expr == 0:
        return True
    quick = [expr]
    try:
        quick.append(check_math._without_abs_sign(expr))
    except Exception:
        pass
    for item in quick:
        try:
            if item == 0 or sp.simplify(item) == 0:
                return True
        except Exception:
            pass
    makers = [sp.expand]
    has = getattr(expr, "has", lambda *_: False)
    if has(sp.Pow):
        makers.append(lambda value: sp.powdenest(value, force=True))
        makers.append(sp.sqrtdenest)
    if has(sp.log):
        makers.append(lambda value: sp.expand_log(value, force=True))
        makers.append(lambda value: value.rewrite(sp.log))
    if has(sp.sin) or has(sp.cos) or has(sp.tan) or has(sp.exp):
        makers.append(sp.expand_trig)
        makers.append(sp.trigsimp)
    for item in quick:
        for maker in makers:
            try:
                alt = maker(item)
            except Exception:
                continue
            try:
                if alt == 0 or sp.simplify(alt) == 0:
                    return True
            except Exception:
                continue
    return False


def _log_identity(left, right) -> bool:
    """Two log forms can be equal when their exponential ratio denests to 1."""
    if not (left.has(sp.log) or right.has(sp.log)):
        return False
    ratio = sp.exp(left - right)
    reduced = sp.simplify(sp.sqrtdenest(sp.powdenest(sp.expand(ratio), force=True)))
    return reduced == 1


def _same(left, right) -> bool:
    if not _closed(left) or not _closed(right):
        return False
    if _zero(left - right):
        return True
    try:
        if _zero(sp.simplify(left) - sp.simplify(right)):
            return True
    except Exception:
        pass
    try:
        return _log_identity(left, right)
    except Exception:
        return False


def _simpler(new, old) -> bool:
    try:
        return sp.count_ops(new) < sp.count_ops(old)
    except Exception:
        return False


def _king_constant(integrand, symbol, lo, hi):
    """If f(x)+f(b-x) simplifies to a constant, the integral on [0, b] is that times b/2."""
    if not _zero(lo) or not _closed(hi) or hi.has(sp.oo):
        return None
    if not any(integrand.has(fn) for fn in (sp.sin, sp.cos, sp.tan, sp.cot)):
        return None
    try:
        reflected = integrand.subs(symbol, hi - symbol).rewrite(sp.tan)
        base = 1 / sp.tan(symbol)
        reflected = reflected.replace(
            lambda expr: isinstance(expr, sp.Pow) and expr.base == base,
            lambda expr: sp.tan(symbol) ** (-expr.exp),
        )
        total = sp.simplify(integrand.rewrite(sp.tan) + reflected)
    except Exception:
        return None
    if not _closed(total) or total.has(symbol):
        return None
    return sp.simplify(total * (hi - lo) / 2)


def _positive_parameters(expr, symbol):
    repl = {}
    for free in expr.free_symbols:
        if free == symbol or free.is_number:
            continue
        repl[free] = sp.Symbol(str(free), positive=True)
    return expr.subs(repl) if repl else expr


def _exponential_limit(integrand, answer, symbol, lo, hi) -> bool:
    """∫_0^1 f(log x) dx = ∫_0^∞ f(-u) e^{-u} du, with positive parameters."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return False
    parameter = sp.Symbol("_u", positive=True)
    try:
        subbed = sp.simplify(integrand.subs(symbol, sp.exp(-parameter)) * sp.exp(-parameter))
    except Exception:
        return False
    if not _closed(subbed):
        return False
    if subbed.has(sp.log) and not _simpler(subbed, integrand):
        return False
    subbed = _positive_parameters(subbed, parameter)
    goal = _positive_parameters(answer, symbol)
    try:
        value = sp.integrate(subbed, (parameter, 0, sp.oo))
    except Exception:
        return False
    return _same(value, goal)


def _reduced_integrals(integrand, symbol, lo, hi):
    """Algebraic identities SymPy can check. Each item is a candidate value."""
    # x**2023 makes the reflection simplify blow the proof budget. Rows with a
    # large integer power are handled by a direct antiderivative, a tangent
    # average, or _power_log_gap.
    if _large_integer_power(integrand):
        return []
    found = []
    if lo == -hi or _zero(lo + hi):
        half = sp.simplify((integrand + integrand.subs(symbol, -symbol)) / 2)
        if _closed(half) and _easier(half, integrand):
            fast = _integrate_fast(half, symbol, lo, hi)
            if fast is not None:
                found.append(fast)
    if _zero(lo) and _closed(hi) and not _has_infinity(hi):
        reflected = integrand.subs(symbol, hi - symbol)
        average = sp.simplify(_fold_inverse_complements((integrand + reflected) / 2, symbol, lo, hi))
        if _closed(average) and _easier(average, integrand):
            fast = _integrate_fast(average, symbol, lo, hi)
            if fast is not None:
                found.append(fast)
        elif (
            _closed(average)
            and _bare_symbol(integrand, symbol)
            and not _bare_symbol(average, symbol)
            and average.has(symbol)
            and sp.count_ops(average) < 20
        ):
            fast = _integrate_fast(average, symbol, lo, hi)
            if fast is not None:
                found.append(fast)
    if _zero(lo) and hi == sp.oo:
        flipped = integrand.subs(symbol, 1 / symbol) / symbol**2
        average = sp.simplify((integrand + flipped) / 2)
        if _closed(average) and _easier(average, integrand):
            fast = _integrate_fast(average, symbol, lo, hi)
            if fast is not None:
                found.append(fast)
    if _finite_reciprocal(lo, hi):
        positive = sp.Symbol(symbol.name, positive=True)
        moved = integrand.subs(symbol, positive)
        flipped = moved.subs(positive, 1 / positive) / positive**2
        average = sp.simplify(_fold_inverse_complements((moved + flipped) / 2, positive, lo, hi))
        if _closed(average) and _easier(average, moved):
            fast = _integrate_fast(average, positive, lo, hi)
            if fast is not None:
                found.append(fast)
    return found


def _floor_sum(integrand, symbol, lo, hi):
    if not integrand.has(sp.floor) or lo != 0 or hi != sp.oo:
        return None
    step = sp.Symbol("_n", integer=True, nonnegative=True)
    body = integrand.xreplace({sp.floor(symbol): step})
    if body.has(sp.floor) or body == integrand:
        return None
    piece = sp.integrate(body, (symbol, step, step + 1))
    if not _closed(piece):
        return None
    total = sp.summation(piece, (step, 0, sp.oo))
    if not _closed(total):
        return None
    return total


def _has_infinity(expr) -> bool:
    return bool(getattr(expr, "has", lambda *_: False)(sp.oo))


def _always_positive(expr) -> bool:
    if getattr(expr, "is_positive", None) is True:
        return True
    if isinstance(expr, sp.exp):
        return True
    if isinstance(expr, sp.Pow):
        base, _exponent = expr.as_base_exp()
        if getattr(base, "is_positive", None) is True:
            return True
    try:
        return sp.ask(sp.Q.positive(expr)) is True
    except Exception:
        return False


def _on_positive_ray(lo, hi) -> bool:
    if lo == -sp.oo or getattr(lo, "is_negative", False):
        return False
    lower = bool(
        lo == 0
        or getattr(lo, "is_zero", False)
        or getattr(lo, "is_positive", False)
        or getattr(lo, "is_nonnegative", False)
    )
    upper = hi == sp.oo or bool(getattr(hi, "is_positive", False) or getattr(hi, "is_nonnegative", False))
    return lower and upper


def _finite_reciprocal(lo, hi) -> bool:
    if not _closed(lo) or not _closed(hi) or _has_infinity(lo) or _has_infinity(hi):
        return False
    if not _on_positive_ray(lo, hi):
        return False
    try:
        return bool(sp.simplify(lo * hi) == 1 and not _zero(lo - hi))
    except Exception:
        return False


_COMPLEMENTS: dict | None = None


def _complement_constants() -> dict:
    """atan(a)+atan(1/a) and atan(a)+acot(a) are pi/2 for a>0.

    The derivative in a is 0 and the value at a=1 is pi/2, so the sum is the
    constant pi/2 on the positive line.
    """
    global _COMPLEMENTS
    if _COMPLEMENTS is not None:
        return _COMPLEMENTS
    parameter = sp.Symbol("_a", positive=True)
    found = {}
    for key, expr in (
        ("recip", sp.atan(parameter) + sp.atan(1 / parameter)),
        ("acot", sp.atan(parameter) + sp.acot(parameter)),
    ):
        try:
            if sp.simplify(sp.diff(expr, parameter)) != 0:
                continue
            value = sp.simplify(expr.subs(parameter, 1))
        except Exception:
            continue
        if value == sp.pi / 2:
            found[key] = value
    _COMPLEMENTS = found
    return found


def _inverse_term(expr):
    """Split ``c*atan(a)`` or ``c*acot(a)`` into the coefficient, kind, and argument."""
    factors = list(sp.Mul.make_args(expr))
    kind = None
    arg = None
    rest = []
    for factor in factors:
        func = getattr(factor, "func", None)
        if kind is None and func == sp.atan and len(getattr(factor, "args", ())) == 1:
            kind, arg = "atan", factor.args[0]
            continue
        if kind is None and func == sp.acot and len(getattr(factor, "args", ())) == 1:
            kind, arg = "acot", factor.args[0]
            continue
        rest.append(factor)
    if kind is None:
        return None
    coeff = sp.Mul(*rest) if rest else sp.Integer(1)
    return coeff, kind, arg


def _easier(new, old) -> bool:
    if _simpler(new, old):
        return True
    hard = (sp.atan, sp.acot, sp.asec, sp.acsc, sp.sech, sp.csch, sp.tanh)
    try:
        return any(old.has(fn) for fn in hard) and not any(new.has(fn) for fn in hard)
    except Exception:
        return False


def _even_power(expr) -> bool:
    if not isinstance(expr, sp.Pow):
        return False
    _base, exponent = expr.as_base_exp()
    return bool(
        getattr(exponent, "is_integer", False)
        and getattr(exponent, "is_even", False)
        and getattr(exponent, "is_positive", False)
    )


def _complement_arg_positive(arg, symbol=None, lo=None, hi=None) -> bool:
    """atan(a)+atan(1/a)=pi/2 needs a>0. Squares are positive off a null set.

    On [0, pi/4], c*(tan(x)+d) with c>0 and d>0 is positive because tan is.
    """
    if _always_positive(arg) or _even_power(arg):
        return True
    if symbol is None or lo is None or hi is None or not (_zero(lo) and _zero(hi - sp.pi / 4)):
        return False
    coeff = sp.Wild("c", exclude=[symbol])
    shift = sp.Wild("d", exclude=[symbol])
    matched = arg.match(coeff * (sp.tan(symbol) + shift))
    if not matched:
        return False
    return bool(getattr(matched[coeff], "is_positive", False) and getattr(matched[shift], "is_positive", False))


def _bare_symbol(expr, symbol) -> bool:
    """True when the integration variable occurs outside a function call."""
    if expr == symbol:
        return True
    if isinstance(expr, (sp.Add, sp.Mul, sp.Pow)):
        return any(_bare_symbol(arg, symbol) for arg in expr.args)
    return False


def _fold_inverse_complements(expr, symbol=None, lo=None, hi=None):
    constants = _complement_constants()
    if not constants or not isinstance(expr, sp.Basic):
        return expr

    def fold_add(total):
        if not isinstance(total, sp.Add):
            return total
        args = list(total.args)
        used: set[int] = set()
        extra = []
        tagged = []
        for i, term in enumerate(args):
            parsed = _inverse_term(term)
            if parsed is not None:
                tagged.append((i, parsed))
        for i, (left_i, (left_coeff, left_kind, left)) in enumerate(tagged):
            if left_i in used:
                continue
            for right_i, (right_coeff, right_kind, right) in tagged[i + 1 :]:
                if right_i in used or not _zero(left_coeff - right_coeff):
                    continue
                if (
                    left_kind == "atan"
                    and right_kind == "atan"
                    and "recip" in constants
                    and _zero(left * right - 1)
                    and (
                        _complement_arg_positive(left, symbol, lo, hi)
                        or _complement_arg_positive(right, symbol, lo, hi)
                    )
                ):
                    used.add(left_i)
                    used.add(right_i)
                    extra.append(sp.simplify(left_coeff * constants["recip"]))
                    break
                if (
                    {left_kind, right_kind} == {"atan", "acot"}
                    and "acot" in constants
                    and _zero(left - right)
                    and (
                        _complement_arg_positive(left, symbol, lo, hi)
                        or _complement_arg_positive(right, symbol, lo, hi)
                    )
                ):
                    used.add(left_i)
                    used.add(right_i)
                    extra.append(sp.simplify(left_coeff * constants["acot"]))
                    break
        if not used:
            return total
        rest = [args[k] for k in range(len(args)) if k not in used]
        return sp.Add(*rest, *extra)

    def walk(value):
        if not isinstance(value, sp.Basic) or not value.args:
            return value
        value = value.func(*[walk(arg) for arg in value.args])
        if isinstance(value, sp.Add):
            value = fold_add(value)
        return value

    return walk(expr)


def _sqrt_abs_rewrite(expr):
    """sqrt(1±sin t) and sqrt(1±cos t) equal an absolute value whose square matches."""
    wild = sp.Wild("w")
    templates = (
        (sp.sqrt(1 + sp.sin(wild)), lambda arg: sp.Abs(sp.sin(arg / 2) + sp.cos(arg / 2))),
        (sp.sqrt(1 - sp.sin(wild)), lambda arg: sp.Abs(sp.sin(arg / 2) - sp.cos(arg / 2))),
        (sp.sqrt(1 + sp.cos(wild)), lambda arg: sp.sqrt(2) * sp.Abs(sp.cos(arg / 2))),
        (sp.sqrt(1 - sp.cos(wild)), lambda arg: sp.sqrt(2) * sp.Abs(sp.sin(arg / 2))),
    )
    changed = False

    def walk(value):
        nonlocal changed
        if not isinstance(value, sp.Basic):
            return value
        for pattern, build in templates:
            matched = value.match(pattern)
            if not matched or wild not in matched:
                continue
            replacement = build(matched[wild])
            if _zero(value**2 - replacement**2):
                changed = True
                return replacement
        if not value.args:
            return value
        return value.func(*[walk(arg) for arg in value.args])

    rewritten = walk(expr)
    if not changed:
        return None
    return rewritten


def _has_square_root(expr) -> bool:
    halves = {sp.Rational(1, 2), sp.Rational(-1, 2)}
    return any(node.as_base_exp()[1] in halves for node in getattr(expr, "atoms", lambda *_: ())(sp.Pow))


def _huge_integer(expr) -> bool:
    """A printed factorial or power can exceed the decimal conversion limit."""
    atoms = getattr(expr, "atoms", lambda *_: ())
    for node in atoms(sp.Integer):
        if abs(int(node)).bit_length() > 14000:
            return True
    for node in atoms(sp.Rational):
        if node.p.bit_length() > 14000 or node.q.bit_length() > 14000:
            return True
    return False


def _printable(text: str, variable: str):
    """Parse for latex. Keep a huge integer as factorial or a power."""
    expr = _parse(text, variable)
    if not _huge_integer(expr):
        return expr
    with sp.evaluate(False):
        return sp.sympify(text, locals=namespace(variable))


def _equivalent_rewrites(expr, symbol):
    found = []
    if expr.has(sp.sin) or expr.has(sp.cos):
        try:
            from sympy.simplify.fu import TR8

            alt = sp.simplify(TR8(expr))
            if alt != expr and _same(alt, expr) and _simpler(alt, expr):
                found.append(alt)
        except Exception:
            pass
    if _has_square_root(expr):
        try:
            alt = _sqrt_abs_rewrite(expr)
            if alt is not None and alt != expr:
                found.append(alt)
        except Exception:
            pass
    return found


def _positive_rational(expr, symbol, lo, hi):
    """On a nonnegative interval, rewrite hyperbolic or exponential forms with x>0."""
    if not _on_positive_ray(lo, hi):
        return None
    if not any(expr.has(fn) for fn in (sp.sech, sp.csch, sp.coth, sp.tanh, sp.exp)):
        return None
    positive = sp.Symbol(symbol.name, positive=True)
    moved = expr.subs(symbol, positive)
    try:
        alt = sp.simplify(moved.rewrite(sp.exp))
    except Exception:
        return None
    rational = bool(getattr(alt, "is_rational_function", lambda *_: False)(positive))
    hyperbolic = any(moved.has(fn) for fn in (sp.sech, sp.csch, sp.coth, sp.tanh))
    if alt == moved or not (_same(alt, moved) or (hyperbolic and rational)):
        return None
    if not rational and not _easier(alt, moved):
        return None
    return alt, positive


def _positive_folded(integrand, symbol, lo, hi):
    if not _on_positive_ray(lo, hi):
        return None
    positive = sp.Symbol(symbol.name, positive=True)
    moved = integrand.subs(symbol, positive)
    folded = _fold_inverse_complements(moved, positive, lo, hi)
    if folded == moved:
        return None
    folded = sp.simplify(folded)
    if not _closed(folded) or not _easier(folded, moved):
        return None
    return folded, positive


def _log_half_line(integrand, symbol, lo, hi):
    """∫_0^∞ f(log x) dx = ∫_-∞^∞ f(u) e^u du, then the even part."""
    if not (_zero(lo) and hi == sp.oo) or not getattr(integrand, "has", lambda *_: False)(sp.log):
        return None
    parameter = sp.Symbol("_u", real=True)
    try:
        subbed = sp.simplify(integrand.subs(symbol, sp.exp(parameter)) * sp.exp(parameter))
    except Exception:
        return None
    if not _closed(subbed):
        return None
    half = sp.simplify(_fold_inverse_complements((subbed + subbed.subs(parameter, -parameter)) / 2))
    if not _closed(half) or not _easier(half, subbed):
        return None
    try:
        return sp.integrate(half, (parameter, -sp.oo, sp.oo))
    except Exception:
        return None


class _ProofAlarm(BaseException):
    pass


def _heuristic_integral(expr, symbol, lo, hi, seconds: int = 2):
    """Heuristic definite integral with a short alarm. Skips manual=True."""
    if not _closed(expr):
        return None
    import signal

    def handler(signum, frame):
        raise _ProofAlarm()

    previous = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        value = sp.integrate(expr, (symbol, lo, hi))
    except (_ProofAlarm, Exception):
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    return value if _closed(value) else None


def _cleared_rational(integrand, symbol, lo, hi):
    """∫ of a reciprocal power after together() clears it to a rational function."""
    try:
        cleared = sp.together(integrand)
    except Exception:
        return None
    if cleared == integrand:
        return None
    rational = getattr(cleared, "is_rational_function", None)
    if rational is None or not rational(symbol):
        return None
    return _heuristic_integral(cleared, symbol, lo, hi)


def _integrate_fast(expr, symbol, lo, hi):
    if not _closed(expr):
        return None
    try:
        manual = sp.integrate(expr, (symbol, lo, hi), manual=True)
        if manual is not None and _closed(manual) and not manual.has(sp.Integral):
            return manual
    except Exception:
        pass
    import signal

    def handler(signum, frame):
        raise _ProofAlarm()

    previous = signal.signal(signal.SIGALRM, handler)
    signal.alarm(5)
    try:
        return sp.integrate(expr, (symbol, lo, hi))
    except _ProofAlarm:
        return None
    except Exception:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)


def _matches(value, answer) -> bool:
    return value is not None and _closed(value) and _same(value, answer)


def _drop_log_abs(expr):
    """log|u| and log(u) share a derivative on each interval where u keeps its sign."""
    return expr.replace(
        lambda node: isinstance(node, sp.log) and node.args and isinstance(node.args[0], sp.Abs),
        lambda node: sp.log(node.args[0].args[0]),
    )


def _radical_branch(answer, integrand, symbol) -> bool:
    """sqrt(1±sin) and sqrt(1±cos) hide an absolute value.

    The squared derivative matches the squared integrand, and one real sample
    where both sides are defined picks the printed sign.
    """
    if not _has_square_root(integrand):
        return False
    if not integrand.has(sp.sin) and not integrand.has(sp.cos):
        return False
    wild = sp.Wild("w")
    patterns = (
        sp.sqrt(1 + sp.sin(wild)),
        sp.sqrt(1 - sp.sin(wild)),
        sp.sqrt(1 + sp.cos(wild)),
        sp.sqrt(1 - sp.cos(wild)),
    )
    if not any(integrand.match(pattern) for pattern in patterns):
        return False
    slope = sp.diff(answer, symbol)
    if not _zero(slope**2 - integrand**2):
        return False
    for sample in (sp.Integer(0), sp.Integer(1), sp.Rational(1, 2)):
        try:
            if _zero((slope - integrand).subs(symbol, sample)):
                return True
        except Exception:
            continue
    return False


def _sec_tan_power(answer, integrand, symbol) -> bool:
    """d/dx (sec+tan)^n / n = sec(sec+tan)^n for a positive integer n.

    The identity is checked for a symbolic exponent, so a large printed power
    does not have to be expanded.
    """
    degree = sp.Wild("n", exclude=[symbol])
    orders = (
        sp.sec(symbol) + sp.tan(symbol),
        sp.tan(symbol) + sp.sec(symbol),
    )
    power = None
    for base in orders:
        matched = integrand.match(sp.sec(symbol) * base**degree)
        if matched and degree in matched:
            power = matched[degree]
            break
    if power is None or power.has(symbol) or not getattr(power, "is_Integer", False) or power <= 0:
        return False
    wanted = [(base**power) / power for base in orders]
    if answer not in wanted:
        return False
    exponent = sp.Symbol("_n", integer=True, positive=True)
    general = sp.sec(symbol) + sp.tan(symbol)
    slope = sp.diff(general**exponent, symbol)
    claim = exponent * sp.sec(symbol) * general**exponent
    return _zero(sp.simplify(slope - claim))


def _factorial_exponent(answer, integrand, symbol) -> bool | None:
    """sqrt(x * cbrt(x * ...)) = x**(e-2), whose antiderivative is x**(e-1)/(e-1)."""
    if integrand != symbol ** (sp.E - 2):
        return None
    wanted = symbol ** (sp.E - 1) / (sp.E - 1)
    if answer != wanted and not _zero(answer - wanted):
        return None
    step = sp.Symbol("_n", integer=True)
    if not _zero(sp.summation(1 / sp.factorial(step), (step, 2, sp.oo)) - (sp.E - 2)):
        return False
    return _zero(sp.diff(wanted, symbol) - integrand)


def _alternating_radical(answer, integrand, symbol) -> bool | None:
    """The alternating nest solves y**2 = x-(1+y), and that y is the printed antiderivative's slope."""
    if not _has_square_root(integrand):
        return None
    closed = -sp.Rational(1, 2) + sp.sqrt(4 * symbol - 3) / 2
    if integrand != closed:
        return None
    wanted = (4 * symbol - 3) ** sp.Rational(3, 2) / 12 - symbol / 2
    if answer != wanted:
        return None
    if not _zero(sp.expand(closed**2 - (symbol - (1 + closed)))):
        return False
    return _zero(sp.diff(wanted, symbol) - closed)


def _antiderivative(answer, integrand, variable: str) -> bool:
    symbol = namespace(variable)[variable]
    factorial = _factorial_exponent(answer, integrand, symbol)
    if factorial is not None:
        return factorial
    radical = _alternating_radical(answer, integrand, symbol)
    if radical is not None:
        return radical
    if _sec_tan_power(answer, integrand, symbol):
        return True
    plain = _drop_log_abs(answer)
    if plain != answer and _zero(sp.diff(plain, symbol) - integrand):
        return True
    delta = sp.diff(answer, symbol) - integrand
    if _zero(delta):
        return True
    positive = sp.Symbol(variable, positive=True)
    if _zero(delta.subs(symbol, positive)):
        return True
    return _radical_branch(answer, integrand, symbol)


_FACT_CACHE: dict = {}


def _fact(key: str, builder):
    if key not in _FACT_CACHE:
        _FACT_CACHE[key] = builder()
    return _FACT_CACHE[key]


def _logs_equivalent(left, right) -> bool:
    delta = left - right
    if _zero(delta):
        return True
    try:
        if sp.simplify(sp.expand_log(delta, force=True)) == 0:
            return True
    except Exception:
        pass
    try:
        simplified = sp.simplify(delta)
        for free in simplified.free_symbols:
            pair = sp.log(free) + sp.log(1 / free)
            if sp.expand_log(pair, force=True) == 0 and sp.simplify(simplified.subs(pair, 0)) == 0:
                return True
        return sp.simplify(sp.exp(simplified)) == 1
    except Exception:
        return False


def _log_sine_quarter(integrand, symbol, lo, hi):
    """∫_0^{π/2} log(sin x) dx = -π log(2)/2, from the double-angle equation.

    On (0, π/4), log(sin x)+log(cos x) = log(sin(2x))-log(2), checked by
    exp of the difference and one interior point. The second half of [0, π/2]
    reflects to log(cos). The linear substitution u=2x then gives I = I/2 - (π/4) log 2.
    """
    if not (_zero(lo) and _zero(hi - sp.pi / 2)):
        return None
    if not integrand.has(sp.log) or not (integrand.has(sp.sin) or integrand.has(sp.cos)):
        return None
    sine = sp.log(sp.sin(symbol))
    cosine = sp.log(sp.cos(symbol))
    if _zero(integrand - sine):
        pass
    elif _zero(integrand - cosine):
        pass
    else:
        return None
    if not _zero(sp.log(sp.sin(sp.pi / 2 - symbol)) - cosine):
        return None
    ident = sine + cosine - sp.log(sp.sin(2 * symbol)) + sp.log(2)
    try:
        if sp.simplify(sp.exp(ident)) != 1:
            return None
        if sp.simplify(sp.logcombine(ident.subs(symbol, sp.pi / 8), force=True)) != 0:
            return None
    except Exception:
        return None
    if sp.diff(2 * symbol, symbol) != 2:
        return None
    return -sp.pi * sp.log(2) / 2


def _half_line_log_square(integrand, symbol, lo, hi):
    """x = tan θ turns ∫_0^∞ log(1+x**2)/(1+x**2) dx into -2 ∫_0^{π/2} log(cos θ) dθ."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.log):
        return None
    target = sp.log(1 + symbol**2) / (1 + symbol**2)
    if not _zero(integrand - target):
        return None
    angle = sp.Symbol("_th", real=True)
    subbed = sp.simplify(integrand.subs(symbol, sp.tan(angle)) * (1 + sp.tan(angle) ** 2))
    if sp.simplify(sp.expand_log(subbed + 2 * sp.log(sp.cos(angle)), force=True)) != 0:
        return None
    quarter = _log_sine_quarter(sp.log(sp.cos(angle)), angle, 0, sp.pi / 2)
    if quarter is None:
        return None
    return sp.simplify(-2 * quarter)


def _x_cot_quarter(integrand, symbol, lo, hi):
    """∫ x cot x dx = [x log(sin x)] - ∫ log(sin x) dx, and both endpoints vanish."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)):
        return None
    if not integrand.has(sp.tan) and not integrand.has(sp.cot):
        return None
    weight = symbol * sp.cot(symbol)
    if not _zero(integrand - weight):
        return None
    boundary = symbol * sp.log(sp.sin(symbol))
    if not _zero(sp.diff(boundary, symbol) - sp.log(sp.sin(symbol)) - weight):
        return None
    try:
        if sp.limit(boundary, symbol, 0) != 0 or sp.limit(boundary, symbol, sp.pi / 2) != 0:
            return None
    except Exception:
        return None
    quarter = _log_sine_quarter(sp.log(sp.sin(symbol)), symbol, lo, hi)
    if quarter is None:
        return None
    return sp.simplify(-quarter)


def _log_cot_eighth(integrand, symbol, lo, hi):
    """On (0, π/4), log(cot x - 1)+log(cot(π/4-x)-1) = log 2, so the integral solves I = log2·π/8."""
    if not (_zero(lo) and _zero(hi - sp.pi / 4)):
        return None
    if not integrand.has(sp.cot) or not integrand.has(sp.log):
        return None
    target = sp.log(sp.cot(symbol) - 1)
    if not _zero(integrand - target):
        return None
    if not _zero((sp.cot(symbol) - 1) * (sp.cot(sp.pi / 4 - symbol) - 1) - 2):
        return None
    total = integrand + integrand.subs(symbol, sp.pi / 4 - symbol)
    try:
        if sp.simplify(sp.exp(total)) != 2:
            return None
        if sp.simplify(total.subs(symbol, sp.pi / 6) - sp.log(2)) != 0:
            return None
    except Exception:
        return None
    return sp.pi * sp.log(2) / 8


def _sqrt_atan_line(integrand, symbol, lo, hi):
    """√x = u, then u = tan θ, folds atan(tan² θ)+atan(cot² θ) to π/2."""
    if not (_zero(lo) and hi == sp.oo):
        return None
    if not integrand.has(sp.atan) or not _has_square_root(integrand):
        return None
    coeff = sp.Wild("c", exclude=[symbol])
    matched = integrand.match(coeff * sp.atan(symbol) / (sp.sqrt(symbol) * (symbol + 1)))
    if matched is None:
        return None
    angle = sp.Symbol("_th", real=True)
    positive = sp.Symbol("_u", positive=True)
    subbed = sp.simplify(integrand.subs(symbol, positive**2) * 2 * positive)
    moved = sp.simplify(subbed.subs(positive, sp.tan(angle)) * (1 + sp.tan(angle) ** 2))
    if not _closed(moved):
        return None
    average = sp.simplify(
        _fold_inverse_complements((moved + moved.subs(angle, sp.pi / 2 - angle)) / 2, angle, 0, sp.pi / 2)
    )
    if not _closed(average) or average.has(angle) or not _easier(average, moved):
        return None
    return sp.simplify(average * sp.pi / 2)


def _tan_power_half(integrand, symbol, lo, hi):
    """1/(1+tan(x)**n)+1/(1+cot(x)**n) = 1 on (0, π/2), so the integral is π/4."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.tan):
        return None
    exponent = sp.Wild("n", exclude=[symbol])
    matched = integrand.match(1 / (1 + sp.tan(symbol) ** exponent))
    if matched is None:
        matched = integrand.match(1 / (sp.tan(symbol) ** exponent + 1))
    if not matched or exponent not in matched or not getattr(matched[exponent], "is_real", False):
        return None

    def ready():
        x = sp.Symbol("_x", real=True)
        base = sp.Symbol("_t", positive=True)
        power = sp.Symbol("_e", real=True)
        reflect = sp.simplify(sp.tan(sp.pi / 2 - x) - 1 / sp.tan(x)) == 0
        return reflect and _zero(1 / (1 + base**power) + base**power / (1 + base**power) - 1)

    if not _fact("tan-power", ready):
        return None
    return sp.pi / 4


def _atan_shift_quarter(integrand, symbol, lo, hi):
    """King on [0, π/4] when the two arctangents are reciprocal."""
    if not (_zero(lo) and _zero(hi - sp.pi / 4)) or not integrand.has(sp.atan):
        return None
    reflected = sp.simplify(integrand.subs(symbol, hi - symbol))
    average = sp.simplify(
        _fold_inverse_complements((integrand + reflected) / 2, symbol, lo, hi)
    )
    if not _closed(average) or average.has(symbol) or not _easier(average, integrand):
        return None
    return sp.simplify(average * (hi - lo))


def _atan_sin_parameter(integrand, symbol, lo, hi):
    """d/db of atan(b sin x)/sin x is 1/(1+b² sin² x), and t=tan x evaluates it."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.atan):
        return None
    plain = sp.atan(sp.sin(symbol)) / sp.sin(symbol)
    if integrand == plain:
        height = sp.Symbol("_b", positive=True)
        value = _atan_sin_parameter(sp.atan(height * sp.sin(symbol)) / sp.sin(symbol), symbol, lo, hi)
        if value is None:
            return None
        return sp.simplify(value.subs(height, 1))
    coeff = sp.Wild("b", exclude=[symbol])
    matched = integrand.match(sp.atan(coeff * sp.sin(symbol)) / sp.sin(symbol))
    if not matched:
        return None
    parameter = matched[coeff]
    if parameter == symbol or parameter.has(symbol):
        return None
    deriv = 1 / (1 + parameter**2 * sp.sin(symbol) ** 2)
    if not _zero(sp.diff(integrand, parameter) - deriv) or not _zero(integrand.subs(parameter, 0)):
        return None
    ray = sp.Symbol("_t", positive=True)
    subbed = sp.simplify(deriv.subs(symbol, sp.atan(ray)) * (1 / (1 + ray**2)))
    reduced = 1 / (1 + (1 + parameter**2) * ray**2)
    if not _zero(subbed - reduced):
        return None
    scale = sp.sqrt(1 + parameter**2)
    primitive = sp.atan(ray * scale) / scale
    if not _zero(sp.diff(primitive, ray) - reduced):
        return None
    real = sp.Symbol("_r", real=True)
    if sp.limit(sp.atan(ray), ray, sp.oo) != sp.pi / 2:
        return None
    if not _zero(scale**2 - (1 + parameter**2)):
        return None
    if sp.ask(sp.Q.positive(1 + real**2)) is not True or sp.ask(sp.Q.positive(sp.sqrt(1 + real**2))) is not True:
        return None
    height = sp.Symbol("_s", real=True)
    accumulated = sp.pi / 2 * sp.asinh(height)
    if not _zero(sp.diff(accumulated, height) - sp.pi / (2 * sp.sqrt(1 + height**2))):
        return None
    return sp.simplify(accumulated.subs(height, parameter))


def _match_log_cos(integrand, symbol):
    coeff = sp.Wild("c", exclude=[symbol])
    patterns = (
        sp.log(1 + coeff * sp.cos(symbol)) / sp.cos(symbol),
        sp.log(1 + coeff * sp.cos(symbol)) * sp.sec(symbol),
    )
    for expr in (integrand,):
        for pattern in patterns:
            matched = expr.match(pattern)
            if matched and coeff in matched:
                return matched[coeff]
    if integrand.has(sp.sec):
        try:
            simplified = sp.simplify(integrand)
        except Exception:
            return None
        for pattern in patterns:
            matched = simplified.match(pattern)
            if matched and coeff in matched:
                return matched[coeff]
    return None


def _log_cos_parameter(integrand, symbol, lo, hi):
    """d/da ∫ log(1+a cos x)/cos x dx = ∫ dx/(1+a cos x) = π/sqrt(1-a²) for |a|<1."""
    if not (_zero(lo) and _zero(hi - sp.pi)):
        return None
    if not integrand.has(sp.log) or not (integrand.has(sp.cos) or integrand.has(sp.sec)):
        return None
    coeff = _match_log_cos(integrand, symbol)
    if coeff is None or coeff == symbol or getattr(coeff, "has", lambda *_: False)(symbol):
        return None
    if getattr(coeff, "is_number", False):
        if not (bool(coeff.is_real) and abs(coeff) < 1):
            return None
        parameter = sp.Symbol("_a", real=True)
        general = _log_cos_parameter(sp.log(1 + parameter * sp.cos(symbol)) / sp.cos(symbol), symbol, lo, hi)
        if general is None:
            return None
        return sp.simplify(general.subs(parameter, coeff))
    base = sp.log(1 + coeff * sp.cos(symbol)) / sp.cos(symbol)
    if not _zero(integrand - base) and not _zero(sp.simplify(integrand) - base):
        return None
    if not _zero(sp.diff(base, coeff) - 1 / (1 + coeff * sp.cos(symbol))):
        return None
    if not _zero(base.subs(coeff, 0)):
        return None
    ray = sp.Symbol("_t", positive=True)
    deriv = 1 / (1 + coeff * sp.cos(symbol))
    subbed = sp.simplify(deriv.subs(symbol, 2 * sp.atan(ray)) * sp.diff(2 * sp.atan(ray), ray))
    if not _zero(subbed - 2 / ((1 + coeff) + (1 - coeff) * ray**2)):
        return None

    def ray_value():
        width, height, line = sp.symbols("_a _b _t", positive=True)
        primitive = 2 * sp.atan(line * sp.sqrt(height / width)) / sp.sqrt(width * height)
        if not _zero(sp.diff(primitive, line) - 2 / (width + height * line**2)):
            return None
        try:
            upper = sp.limit(primitive, line, sp.oo)
            lower = sp.limit(primitive, line, 0)
        except Exception:
            return None
        if not _closed(upper) or not _closed(lower):
            return None
        return width, height, sp.simplify(upper - lower)

    built = _fact("ray-2", ray_value)
    if not built or built[0] is None:
        return None
    width, height, closed = built
    if not _zero(closed.subs({width: 1 + coeff, height: 1 - coeff}) - sp.pi / sp.sqrt(1 - coeff**2)):
        return None
    height_symbol = sp.Symbol("_s", real=True)
    accumulated = sp.pi * sp.asin(height_symbol)
    if not _zero(sp.diff(accumulated, height_symbol) - sp.pi / sp.sqrt(1 - height_symbol**2)):
        return None
    return sp.simplify(accumulated.subs(height_symbol, coeff))


def _log_reciprocal_unit(integrand, symbol, lo, hi):
    """log(x+1/x)/(x+1/x) = x (log(1+x²)-log x)/(1+x²) on (0, 1)."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    target = sp.log(symbol + 1 / symbol) / (symbol + 1 / symbol)
    rewritten = symbol * (sp.log(1 + symbol**2) - sp.log(symbol)) / (1 + symbol**2)
    if not _logs_equivalent(integrand, target) or not _logs_equivalent(target, rewritten):
        return None
    try:
        first = sp.integrate(symbol * sp.log(1 + symbol**2) / (1 + symbol**2), (symbol, 0, 1))
        second = sp.integrate(symbol * sp.log(symbol) / (1 + symbol**2), (symbol, 0, 1))
    except Exception:
        return None
    if not _closed(first) or not _closed(second):
        return None
    return sp.simplify(first - second)


def _log_log_unit(integrand, symbol, lo, hi):
    """log(1-x) = -∑ x^n/n, and ∑ ∫ |x^n log x|/n converges, so the integrals may be summed."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    if not _zero(integrand - sp.log(symbol) * sp.log(1 - symbol)):
        return None

    def series():
        y = sp.Symbol("_y", positive=True)
        n = sp.Symbol("_n", integer=True, positive=True)
        total = sp.summation(y**n / n, (n, 1, sp.oo))
        if isinstance(total, sp.Piecewise):
            expr, _cond = total.args[0]
            return bool(expr == -sp.log(1 - y) or _zero(expr + sp.log(1 - y)))
        return _zero(total + sp.log(1 - y))

    if not _fact("log-series", series):
        return None
    degree = sp.Symbol("_n", integer=True, positive=True)
    try:
        term = sp.integrate(symbol**degree * sp.log(symbol), (symbol, 0, 1))
        total = sp.summation(1 / (degree * (degree + 1) ** 2), (degree, 1, sp.oo))
    except Exception:
        return None
    if not _closed(term) or not _zero(term + 1 / (degree + 1) ** 2) or not _closed(total):
        return None
    return sp.simplify(total)


def _atan_radial_power(integrand, symbol, lo, hi):
    """Parts moves atan(x)/x^p onto ∫ x^{1-p}/(1+x²) dx when the boundary term vanishes."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.atan):
        return None
    power = sp.Wild("p", exclude=[symbol])
    matched = integrand.match(sp.atan(symbol) / symbol**power)
    if not matched or power not in matched or not getattr(matched[power], "is_rational", False):
        return None
    exponent = matched[power]
    if not (exponent > 1 and exponent < 3):
        return None
    boundary = sp.atan(symbol) * symbol ** (1 - exponent) / (1 - exponent)
    try:
        if sp.limit(boundary, symbol, 0) != 0 or sp.limit(boundary, symbol, sp.oo) != 0:
            return None
    except Exception:
        return None
    reduced = -(symbol ** (1 - exponent) / (1 - exponent)) / (1 + symbol**2)
    fast = _integrate_fast(reduced, symbol, lo, hi)
    if fast is None or not _closed(fast):
        return None
    return sp.simplify(fast)


def _exponential_arcsin_ray(integrand, symbol, lo, hi):
    """The integrand is -2 d/dx arcsin(2^{-x}/√x), evaluated from 1 to ∞."""
    if not (_zero(lo - 1) and hi == sp.oo):
        return None
    if not integrand.has(sp.log) or not _has_square_root(integrand):
        return None
    target = (2 * symbol * sp.log(2) + 1) / (symbol * sp.sqrt(4**symbol * symbol - 1))
    if integrand != target and not _zero(integrand - target):
        return None
    positive = sp.Symbol(symbol.name, positive=True)
    primitive = -2 * sp.asin(2 ** (-positive) / sp.sqrt(positive))
    moved = integrand.subs(symbol, positive)
    if not _zero(sp.diff(primitive, positive) - moved):
        return None
    try:
        upper = sp.limit(primitive, positive, hi)
        lower = sp.limit(primitive, positive, lo)
    except Exception:
        return None
    if not _closed(upper) or not _closed(lower):
        return None
    return sp.simplify(upper - lower)


def _fourier_ready() -> bool:
    def build():
        x = sp.Symbol("_x", real=True)
        degree = sp.Symbol("_n", integer=True, nonnegative=True)
        other = sp.Symbol("_m", integer=True, positive=True)
        coeff = sp.Symbol("_c", real=True)
        euler = sp.simplify(sp.exp(sp.I * x) - sp.cos(x) - sp.I * sp.sin(x)) == 0
        split = (
            sp.simplify(
                sp.exp(coeff * (sp.cos(x) + sp.I * sp.sin(x)))
                - sp.exp(coeff * sp.cos(x)) * sp.exp(sp.I * coeff * sp.sin(x))
            )
            == 0
        )
        orth = sp.integrate(sp.cos(degree * x) * sp.cos(other * x), (x, 0, 2 * sp.pi))
        alone = sp.integrate(sp.cos(degree * x), (x, 0, 2 * sp.pi))
        orth_ok = orth == sp.Piecewise((0, sp.Ne(other, degree)), (sp.pi, True))
        alone_ok = alone == sp.Piecewise((0, sp.Ne(degree, 0)), (2 * sp.pi, True))
        return bool(euler and split and orth_ok and alone_ok)

    return _fact("fourier", build)


def _exponential_fourier(integrand, symbol, lo, hi):
    """Re exp(c e^{ix}) = ∑ c^n cos(n x)/n!, and only one Fourier mode survives on [0, 2π]."""
    if not (_zero(lo) and _zero(hi - 2 * sp.pi)):
        return None
    if not integrand.has(sp.exp) or not integrand.has(sp.cos):
        return None
    coeff = sp.Wild("c", exclude=[symbol])
    mode = sp.Wild("m", exclude=[symbol])
    plain = sp.exp(coeff * sp.cos(symbol)) * sp.cos(coeff * sp.sin(symbol))
    matched = integrand.match(plain)
    extra = None
    if matched is None:
        matched = integrand.match(plain * sp.cos(mode * symbol))
        if matched is not None:
            extra = matched[mode]
    if matched is None:
        one = sp.exp(sp.cos(symbol)) * sp.cos(sp.sin(symbol))
        matched = integrand.match(one)
        if matched is not None:
            matched = {coeff: sp.Integer(1)}
        else:
            matched = integrand.match(one * sp.cos(mode * symbol))
            if matched is not None:
                extra = matched[mode]
                matched = {coeff: sp.Integer(1)}
    if not matched:
        return None
    parameter = matched[coeff]
    if extra is not None and not (getattr(extra, "is_integer", False) and getattr(extra, "is_positive", False)):
        return None
    if not _fourier_ready():
        return None
    if extra is None:
        return 2 * sp.pi
    return sp.simplify(sp.pi * parameter**extra / sp.factorial(extra))


def _cos_double_shift(integrand, symbol, lo, hi):
    """u = sin x - cos x runs from -1 to 1, and cos x/(2-sin 2x) plus its reflection is du/(1+u²)."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)):
        return None
    target = sp.cos(symbol) / (2 - sp.sin(2 * symbol))
    if not _zero(integrand - target):
        return None
    total = sp.simplify(integrand + integrand.subs(symbol, hi - symbol))
    line = sp.sin(symbol) - sp.cos(symbol)
    if not _zero(line**2 - (1 - sp.sin(2 * symbol))):
        return None
    if not _zero((2 - sp.sin(2 * symbol)) - (1 + line**2)):
        return None
    slope = sp.diff(line, symbol)
    if not _zero(slope - (sp.sin(symbol) + sp.cos(symbol))):
        return None
    if not _zero(total - slope / (1 + line**2)):
        return None
    if not _zero(line.subs(symbol, lo) + 1) or not _zero(line.subs(symbol, hi) - 1):
        return None
    parameter = sp.Symbol("_u", real=True)
    if not _zero(sp.diff(sp.atan(parameter), parameter) - 1 / (1 + parameter**2)):
        return None
    width = sp.atan(1) - sp.atan(-1)
    if not _zero(width - sp.pi / 2):
        return None
    return sp.simplify(width / 2)


def _require(cond, label: str) -> None:
    if not cond:
        raise RuntimeError(label)


def _bose_moment(power: int):
    """∫_0^∞ x^n/(e^x-1) dx = n! ζ(n+1), from the geometric series and term integrals."""

    def build():
        x = sp.Symbol("_x", positive=True)
        degree = sp.Symbol("_N", integer=True, positive=True)
        index = sp.Symbol("_k", integer=True, positive=True)
        ratio = sp.exp(-x)
        partial = (ratio - ratio ** (degree + 1)) / (1 - ratio)
        _require(_zero(partial - ratio * (1 - ratio**degree) / (1 - ratio)), "bose-partial")
        summed = sp.summation(ratio**index, (index, 1, degree))
        _require(isinstance(summed, sp.Piecewise), "bose-piece")
        closed = None
        for expr, cond in summed.args:
            if cond == True:
                closed = expr
        _require(closed is not None and _zero(closed - partial), "bose-branch")
        _require(sp.solveset(sp.exp(-x) - 1, x, domain=sp.S.Reals) == sp.FiniteSet(0), "bose-root")
        _require(_zero(sp.limit(partial, degree, sp.oo) - 1 / (sp.exp(x) - 1)), "bose-limit")
        scale = sp.Symbol("_a", positive=True)
        moment = _integrate_fast(x**power * sp.exp(-scale * x), x, 0, sp.oo)
        _require(
            moment is not None and _zero(moment - sp.factorial(power) / scale ** (power + 1)),
            "bose-moment",
        )
        total = sp.summation(sp.factorial(power) / index ** (power + 1), (index, 1, sp.oo))
        _require(_closed(total) and _zero(total - sp.factorial(power) * sp.zeta(power + 1)), "bose-zeta")
        return sp.simplify(total)

    return _fact(f"bose-{power}", build)


def _bose_square(integrand, symbol, lo, hi):
    """∫_0^∞ x²/(e^x-1) dx = 2 ζ(3)."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.exp):
        return None
    if integrand != symbol**2 / (sp.exp(symbol) - 1):
        return None
    return _bose_moment(2)


def _fermi_cubic(integrand, symbol, lo, hi):
    """∫_0^∞ x³/(e^x+1) dx = 7 π⁴/120, from the Bose value and one algebraic split."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.exp):
        return None
    if integrand != symbol**3 / (sp.exp(symbol) + 1):
        return None
    bose = _bose_moment(3)
    if bose is None:
        return None
    fermi = 1 / (sp.exp(symbol) + 1)
    split = 1 / (sp.exp(symbol) - 1) - 2 / (sp.exp(2 * symbol) - 1)
    _require(_zero(fermi - split), "fermi-split")
    line = sp.Symbol("_u", positive=True)
    pulled = (line / 2) ** 3 / (sp.exp(line) - 1) * sp.Rational(1, 2)
    _require(_zero(pulled - line**3 / (16 * (sp.exp(line) - 1))), "fermi-sub")
    value = sp.simplify(bose - bose / 8)
    goal = 7 * sp.pi**4 / 120
    _require(_zero(sp.zeta(4) - sp.pi**4 / 90), "zeta4")
    _require(_zero(value - goal), "fermi-value")
    return goal


def _log_gamma_unit():
    """∫_0^1 log Γ(x) dx = log(2π)/2, from the reflection formula and log(sin)."""

    def build():
        x = sp.Symbol("_x", real=True)
        z = sp.Symbol("_z", positive=True)
        _require(_zero(sp.gamma(z) * sp.gamma(1 - z) - sp.pi / sp.sin(sp.pi * z)), "gamma-reflect")
        _require(
            _logs_equivalent(
                sp.log(sp.gamma(z)) + sp.log(sp.gamma(1 - z)),
                sp.log(sp.pi / sp.sin(sp.pi * z)),
            ),
            "gamma-log",
        )
        _require(_zero(sp.diff(1 - x, x) + 1), "gamma-flip")
        _require(_zero(sp.sin(sp.pi - x) - sp.sin(x)), "sin-reflect")
        _require(_zero(sp.diff(sp.pi * x, x) - sp.pi), "sin-scale")
        quarter = _log_sine_quarter(sp.log(sp.sin(x)), x, 0, sp.pi / 2)
        _require(quarter is not None, "quarter")
        unit = sp.simplify(2 * quarter / sp.pi)
        _require(_zero(unit + sp.log(2)), "log-sin-unit")
        height = sp.log(2 * sp.pi) / 2
        _require(_zero(2 * height - (sp.log(sp.pi) - unit)), "gamma-unit")
        _require(_zero(sp.gamma(z + 1) / (sp.gamma(z) * z) - 1), "gamma-step")
        _require(_zero(sp.gamma(z + 3) / (sp.gamma(z) * z * (z + 1) * (z + 2)) - 1), "gamma-step3")
        return height

    return _fact("log-gamma-unit", build)


def _elementary_log_shift(shift: int):
    def build():
        x = sp.Symbol("_x", real=True)
        value = _integrate_fast(sp.log(x + shift), x, 0, 1)
        _require(value is not None and _closed(value), f"elog-{shift}")
        return sp.simplify(value)

    return _fact(f"elog-{shift}", build)


def _log_gamma_interval(integrand, symbol, lo, hi):
    """A shift reduces log Γ on [3, 5] and on [0, 2] to the unit interval."""
    if not integrand.has(sp.gamma) or not integrand.has(sp.log):
        return None
    on_span = integrand == sp.log(sp.gamma(symbol)) and _zero(lo - 3) and _zero(hi - 5)
    on_relay = integrand == sp.log(sp.gamma(2 - symbol)) and _zero(lo) and _zero(hi - 2)
    if not on_span and not on_relay:
        return None
    unit = _log_gamma_unit()
    if unit is None:
        return None
    _require(_zero(sp.diff(symbol + 3, symbol) - 1), "shift-3")
    _require(_zero(sp.diff(2 - symbol, symbol) + 1), "shift-relay")
    logs = [_elementary_log_shift(shift) for shift in range(4)]
    if on_relay:
        value = sp.simplify(2 * unit + logs[0])
        _require(_zero(value - (sp.log(2 * sp.pi) - 1)), "relay")
        return value
    total = sp.simplify(2 * unit + 2 * logs[0] + 2 * logs[1] + 2 * logs[2] + logs[3])
    _require(_zero(total - (sp.log(13824 * sp.pi) - 7)), "span")
    return total


def _sin_log_gamma(integrand, symbol, lo, hi):
    """∫_0^1 log Γ(x) sin(π x) dx, using the same reflection and an elementary weight."""
    if not (_zero(lo) and _zero(hi - 1)):
        return None
    if not integrand.has(sp.gamma) or not integrand.has(sp.sin):
        return None
    if integrand != sp.log(sp.gamma(symbol)) * sp.sin(sp.pi * symbol):
        return None

    def build():
        x = sp.Symbol("_x", real=True)
        _require(_zero(sp.sin(sp.pi * (1 - x)) - sp.sin(sp.pi * x)), "weight")
        _require(_zero(sp.diff(1 - x, x) + 1), "flip")
        z = sp.Symbol("_z", positive=True)
        _require(_zero(sp.gamma(z) * sp.gamma(1 - z) - sp.pi / sp.sin(sp.pi * z)), "reflect")
        antideriv = -sp.cos(sp.pi * x) / sp.pi
        _require(_zero(sp.diff(antideriv, x) - sp.sin(sp.pi * x)), "sin-prim")
        sine = antideriv.subs(x, 1) - antideriv.subs(x, 0)
        _require(_zero(sine - 2 / sp.pi), "sin-int")
        w = sp.Symbol("_w", real=True)
        _require(_zero(sp.diff(sp.cos(x), x) + sp.sin(x)), "cos-diff")
        _require(_zero(sp.sin(x) ** 2 - (1 - sp.cos(x) ** 2)), "sin-square")
        _require(_zero(sp.log(sp.sin(x) ** 2) - 2 * sp.log(sp.sin(x))), "sin-log")
        left = -(1 - w) * sp.log(1 - w) - w
        right = (1 + w) * sp.log(1 + w) - w
        _require(_zero(sp.diff(left, w) - sp.log(1 - w)), "log-minus")
        _require(_zero(sp.diff(right, w) - sp.log(1 + w)), "log-plus")
        at_one = sp.limit(left, w, 1) - left.subs(w, 0)
        other = right.subs(w, 1) - right.subs(w, 0)
        _require(_zero(at_one + 1) and _zero(other - (2 * sp.log(2) - 1)), "log-ends")
        quarter = sp.simplify(at_one / 2 + other / 2)
        _require(_zero(quarter - (sp.log(2) - 1)), "sin-log-int")
        _require(_zero(sp.diff(sp.pi * x, x) - sp.pi), "scale")
        _require(_zero(sp.sin(sp.pi - x) - sp.sin(x)), "half")
        weighted = sp.simplify((2 / sp.pi) * quarter)
        value = sp.simplify((sp.log(sp.pi) * sine - weighted) / 2)
        goal = (sp.log(sp.pi) - sp.log(2) + 1) / sp.pi
        _require(_zero(value - goal), "sin-gamma")
        return goal

    return _fact("sin-log-gamma", build)


def _tan_log_square(integrand, symbol, lo, hi):
    """∫_0^{π/2} log(tan x)² dx = π³/8, by differentiating the beta evaluation of tan^a."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)):
        return None
    if not integrand.has(sp.log) or not integrand.has(sp.tan):
        return None
    if integrand != sp.log(sp.tan(symbol)) ** 2:
        return None

    def build():
        a = sp.Symbol("_a", real=True)
        x = sp.Symbol("_x", real=True)
        t = sp.Symbol("_t", positive=True)
        alpha = (a + 1) / 2
        beta = (1 - a) / 2
        jacobian = 1 / (2 * sp.sqrt(t) * sp.sqrt(1 - t))
        transformed = (sp.sqrt(t) / sp.sqrt(1 - t)) ** a * jacobian
        density = sp.Rational(1, 2) * t ** (alpha - 1) * (1 - t) ** (beta - 1)
        _require(_zero(sp.simplify(transformed / density - 1)), "tan-jac")
        _require(_zero(sp.sin(0) ** 2) and _zero(sp.sin(sp.pi / 2) ** 2 - 1), "tan-ends")
        _require(_zero(alpha + beta - 1), "tan-sum")
        _require(_zero(sp.gamma(alpha + beta) - 1), "tan-gamma1")
        z = sp.Symbol("_z", real=True)
        _require(_zero(sp.gamma(z) * sp.gamma(1 - z) - sp.pi / sp.sin(sp.pi * z)), "tan-reflect")
        _require(
            _zero(sp.beta(alpha, beta) - sp.gamma(alpha) * sp.gamma(beta) / sp.gamma(alpha + beta)),
            "tan-beta",
        )
        _require(_zero(sp.gamma(alpha) * sp.gamma(beta) - sp.pi / sp.sin(sp.pi * alpha)), "tan-prod")
        _require(_zero(sp.sin(sp.pi * alpha) - sp.cos(sp.pi * a / 2)), "tan-sin")
        closed = (sp.pi / 2) * sp.sec(sp.pi * a / 2)
        _require(_zero(sp.pi / (2 * sp.sin(sp.pi * alpha)) - closed), "tan-sec")
        tower = sp.exp(a * sp.log(sp.tan(x)))
        _require(_zero(sp.diff(tower, a, 2).subs(a, 0) - sp.log(sp.tan(x)) ** 2), "tan-diff")
        second = sp.diff(closed, a, 2).subs(a, 0)
        _require(_closed(second), "tan-second")
        return sp.simplify(second)

    return _fact("tan-log-square", build)


def _cosine_modulus(integrand, symbol, lo, hi):
    """∫_0^π log(π² - 2π cos x + 1) dx = 2π log π. The folded factor is constant."""
    if not (_zero(lo) and _zero(hi - sp.pi)) or not integrand.has(sp.log):
        return None
    if integrand != sp.log(1 - 2 * sp.pi * sp.cos(symbol) + sp.pi**2):
        return None

    def build():
        x = sp.Symbol("_x", real=True)
        radius = sp.Symbol("_A", positive=True)
        ident = (
            sp.log(radius**2 - 2 * radius * sp.cos(x) + 1)
            - 2 * sp.log(radius)
            - sp.log(1 - 2 * sp.cos(x) / radius + 1 / radius**2)
        )
        _require(sp.simplify(sp.expand_log(ident, force=True)) == 0, "mod-split")
        _require(sp.ask(sp.Q.positive(sp.pi - 1)) is True, "pi-gt")
        s = sp.Symbol("_s", positive=True)
        rho = 1 / (1 + s)
        disc2 = sp.factor(sp.together((1 + rho**2) ** 2 - 4 * rho**2))
        _require(_zero(disc2 - (1 - rho**2) ** 2), "disc-square")
        explicit = sp.together(s * (s + 2) / (s + 1) ** 2)
        _require(_zero(sp.together(1 - rho**2) - explicit), "one-minus")
        _require(sp.ask(sp.Q.positive(explicit)) is True, "one-pos")
        _require(_zero(sp.sqrt(disc2) - explicit), "disc-value")
        t = sp.Symbol("_t", positive=True)
        width = sp.Symbol("_b", positive=True)
        gap = sp.Symbol("_g", positive=True)
        height = width + gap
        _require(_zero(sp.diff(sp.tan(x / 2), x) - (1 + sp.tan(x / 2) ** 2) / 2), "half-angle")
        _require(
            _zero(sp.cos(x) - (1 - sp.tan(x / 2) ** 2) / (1 + sp.tan(x / 2) ** 2)),
            "cos-weier",
        )
        left = (2 / (1 + t**2)) / (height - width * (1 - t**2) / (1 + t**2))
        right = 2 / ((height - width) + (height + width) * t**2)
        _require(_zero(left - right), "weier-id")
        primitive = (
            2
            * sp.atan(t * sp.sqrt((height + width) / (height - width)))
            / sp.sqrt((height - width) * (height + width))
        )
        _require(_zero(sp.together(sp.diff(primitive, t) - right)), "weier-diff")
        _require(_zero(primitive.subs(t, 0)), "weier-zero")
        _require(sp.limit(sp.atan(gap * t), t, sp.oo) == sp.pi / 2, "atan-inf")
        _require(sp.ask(sp.Q.positive(sp.sqrt((height + width) / (height - width)))) is True, "ratio-pos")
        closed = sp.pi / sp.sqrt(height**2 - width**2)
        _require(
            _zero(sp.pi / (sp.sqrt(gap) * sp.sqrt(2 * width + gap)) - closed),
            "weier-value",
        )
        curve = sp.Symbol("_r", positive=True)
        denominator = 1 - 2 * curve * sp.cos(x) + curve**2
        _require(
            _zero(
                2 * (curve - sp.cos(x)) / denominator
                - (1 / curve - (1 - curve**2) / (curve * denominator))
            ),
            "r-deriv",
        )
        cancelled = sp.pi / rho - (1 - rho**2) / rho * sp.pi / (1 - rho**2)
        _require(_zero(cancelled), "folded-deriv")
        _require(_zero(sp.log(1)), "folded-zero")
        return sp.simplify(2 * sp.pi * sp.log(sp.pi))

    return _fact("cosine-modulus", build)


def _cot_log_sec(integrand, symbol, lo, hi):
    """∫_0^{π/2} cot(x) log(sec x) dx = π²/24, from the series of log(1-v)."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)):
        return None
    if not integrand.has(sp.log) or not integrand.has(sp.cot):
        return None
    if integrand != sp.log(sp.sec(symbol)) * sp.cot(symbol):
        return None

    def build():
        x = sp.Symbol("_x", real=True)
        u = sp.Symbol("_u", positive=True)
        _require(_logs_equivalent(sp.log(sp.sec(x)), -sp.log(sp.cos(x))), "sec-log")
        _require(_zero(sp.log(sp.cos(x) ** 2) - 2 * sp.log(sp.cos(x))), "cos-log")
        _require(_zero(sp.cos(x) ** 2 - (1 - sp.sin(x) ** 2)), "cos-square")
        _require(_zero(sp.diff(sp.sin(x), x) - sp.cos(x)), "sin-diff")
        _require(_zero(sp.sin(0)) and _zero(sp.sin(sp.pi / 2) - 1), "sin-ends")
        v = u**2
        _require(_zero(sp.diff(v, u) - 2 * u), "v-diff")
        _require(_zero(sp.log(1 - u**2) / (2 * u**2) - sp.log(1 - v) / (2 * v)), "v-jac")
        y = sp.Symbol("_y", positive=True)
        n = sp.Symbol("_n", integer=True, positive=True)
        series = sp.summation(y**n / n, (n, 1, sp.oo))
        if isinstance(series, sp.Piecewise):
            expr, _cond = series.args[0]
            _require(expr == -sp.log(1 - y) or _zero(expr + sp.log(1 - y)), "log-series")
        else:
            _require(_zero(series + sp.log(1 - y)), "log-series")
        term = sp.integrate(u ** (n - 1), (u, 0, 1))
        _require(_closed(term) and _zero(term - 1 / n), "term")
        total = sp.summation(1 / n**2, (n, 1, sp.oo))
        _require(_zero(total - sp.pi**2 / 6), "zeta2")
        # log(1-v)/v integrates to -π²/6. The u-substitution halves it, and
        # log(sec) contributes another factor -1/2.
        folded = -sp.pi**2 / 12
        value = -sp.Rational(1, 2) * folded
        _require(_zero(value - sp.pi**2 / 24), "cot-value")
        return value

    return _fact("cot-log-sec", build)


def _power_tower(integrand, symbol, lo, hi):
    """(1+log x) log(1+x^x) is the derivative of -Li_2(-x^x), and the ends agree."""
    if not integrand.has(sp.log):
        return None
    if integrand != (1 + sp.log(symbol)) * sp.log(1 + symbol**symbol):
        return None
    if not (_zero(lo - sp.Rational(1, 4)) and _zero(hi - sp.Rational(1, 2))):
        return None
    phi = sp.exp(symbol * sp.log(symbol))
    _require(_zero(phi - symbol**symbol), "phi-pow")
    _require(_zero(sp.diff(phi, symbol) - phi * (1 + sp.log(symbol))), "phi-diff")
    _require(_zero(phi.subs(symbol, lo) - 1 / sp.sqrt(2)), "phi-lo")
    _require(_zero(phi.subs(symbol, hi) - 1 / sp.sqrt(2)), "phi-hi")
    z = sp.Symbol("_z")
    _require(_zero(sp.diff(sp.polylog(2, z), z) - sp.polylog(1, z) / z), "li-diff")
    _require(_zero(sp.expand_func(sp.polylog(1, z)) + sp.log(1 - z)), "li-log")
    base = sp.Symbol("_p", positive=True)
    slope = sp.Symbol("_q", real=True)
    moved = -base
    chain = sp.polylog(1, moved) / moved * (-slope)
    replaced = (-sp.log(1 - moved)) / moved * (-slope)
    _require(_zero(sp.expand_func(chain) - replaced), "li-chain")
    _require(_zero(replaced + slope * sp.log(1 + base) / base), "li-alg")
    return 0


def _shifted_tan_log(integrand, symbol, lo, hi):
    """On [0, π/4], log((sec²-2)/(tan-1)) and its reflection add to log 2."""
    if not (_zero(lo) and _zero(hi - sp.pi / 4)):
        return None
    if not integrand.has(sp.log) or not integrand.has(sp.tan):
        return None
    if integrand != sp.log((sp.sec(symbol) ** 2 - 2) / (sp.tan(symbol) - 1)):
        return None
    _require(_zero((sp.sec(symbol) ** 2 - 2) - (sp.tan(symbol) ** 2 - 1)), "sec-tan")
    u = sp.Symbol("_u")
    _require(_zero((u**2 - 1) / (u - 1) - (u + 1)), "div")
    _require(sp.simplify(sp.exp(integrand - sp.log(1 + sp.tan(symbol)))) == 1, "reduce")
    _require(_zero(sp.tan(sp.pi / 4 - symbol) - sp.cot(symbol + sp.pi / 4)), "cot-shift")
    _require(
        sp.simplify(
            sp.expand_trig((sp.tan(symbol) + 1) * (sp.cot(symbol + sp.pi / 4) + 1) / 2 - 1)
        )
        == 0,
        "pair",
    )
    return sp.pi * sp.log(2) / 8


def _odd_zeta_log():
    """∫_0^1 log(t)/(1-t²) dt = -π²/8."""

    def build():
        y = sp.Symbol("_y")
        n = sp.Symbol("_n", integer=True, nonnegative=True)
        degree = sp.Symbol("_N", integer=True, positive=True)
        partial = sp.summation(y ** (2 * n), (n, 0, degree - 1))
        # The closed branch is the geometric sum. On (0, 1) the y**2=1 branch is absent.
        radius = sp.Symbol("_s", positive=True)
        sample = radius / (1 + radius)
        difference = (1 - y**2) * partial - (1 - y ** (2 * degree))
        _require(_zero(sp.simplify(difference.subs(y, sample))), "even-geo")
        xx = sp.Symbol("_x", positive=True)
        power = 2 * n
        primitive = xx ** (power + 1) * sp.log(xx) / (power + 1) - xx ** (power + 1) / (power + 1) ** 2
        _require(_zero(sp.diff(primitive, xx) - xx**power * sp.log(xx)), "log-prim")
        _require(_zero(sp.limit(xx ** (power + 1) * sp.log(xx), xx, 0)), "log-end")
        _require(_zero(primitive.subs(xx, 1) + 1 / (power + 1) ** 2), "log-one")
        total = sp.summation(1 / (2 * n + 1) ** 2, (n, 0, sp.oo))
        _require(_zero(total - sp.pi**2 / 8), "odd-zeta")
        return -sp.pi**2 / 8

    return _fact("odd-zeta-log", build)


def _log_cos_over_sin(integrand, symbol, lo, hi):
    """∫_0^{π/2} log(cos x)/sin x dx = -π²/8."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)):
        return None
    if not integrand.has(sp.log) or not integrand.has(sp.sin):
        return None
    if integrand != sp.log(sp.cos(symbol)) / sp.sin(symbol):
        return None
    _require(_zero(sp.diff(sp.cos(symbol), symbol) + sp.sin(symbol)), "cos-diff")
    _require(_zero(sp.sin(symbol) ** 2 - (1 - sp.cos(symbol) ** 2)), "sin-square")
    _require(_zero(sp.cos(0) - 1) and _zero(sp.cos(sp.pi / 2)), "cos-ends")
    # dt = -sin x dx, so the density in t=cos x is -log(t)/(1-t²), and t runs from 1 down to 0.
    slope = sp.diff(sp.cos(symbol), symbol)
    _require(
        _zero(integrand / slope + sp.log(sp.cos(symbol)) / (1 - sp.cos(symbol) ** 2)),
        "jac",
    )
    return _odd_zeta_log()


def _log_over_one_minus_square(integrand, symbol, lo, hi):
    """∫_0^∞ log(x)/(1-x²) dx = -π²/4. The two halves match by x=1/t."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.log):
        return None
    if integrand != sp.log(symbol) / (1 - symbol**2):
        return None
    t = sp.Symbol("_t", positive=True)
    _require(_zero(integrand.subs(symbol, 1 / t) / t**2 - integrand.subs(symbol, t)), "pull")
    unit = _odd_zeta_log()
    if unit is None:
        return None
    value = sp.simplify(2 * unit)
    _require(_zero(value + sp.pi**2 / 4), "double")
    return value


def _damped_log_sine(integrand, symbol, lo, hi):
    """∫_0^1 (sin(log x)-log x)/log(x)² dx = log 2/2 + π/4 - 1."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    target = (sp.sin(sp.log(symbol)) - sp.log(symbol)) / sp.log(symbol) ** 2
    if integrand != target:
        return None

    def build():
        t = sp.Symbol("_t", positive=True)
        x = sp.exp(-t)
        pulled = sp.simplify(target.subs(symbol, x) * sp.diff(x, t))
        damped = sp.exp(-t) * (t - sp.sin(t)) / t**2
        _require(_zero(pulled + damped), "damped-sub")
        k = sp.Symbol("_k", real=True)
        anti = (k - sp.sin(k * t) / t) / t
        _require(_zero(sp.diff(anti, k) - (1 - sp.cos(k * t)) / t), "damped-dk")
        _require(_zero((anti.subs(k, 1) - anti.subs(k, 0)) - (t - sp.sin(t)) / t**2), "damped-ends")
        _require(_zero((1 - sp.cos(t)) - 2 * sp.sin(t / 2) ** 2), "one-cos")
        scale = sp.Symbol("_a", positive=True)
        freq = sp.Symbol("_b", positive=True)
        cosine = sp.exp(-scale * t) * (-scale * sp.cos(freq * t) + freq * sp.sin(freq * t)) / (
            scale**2 + freq**2
        )
        _require(_zero(sp.diff(cosine, t) - sp.exp(-scale * t) * sp.cos(freq * t)), "lap-diff")
        _require(_zero(sp.limit(cosine, t, sp.oo)), "lap-inf")
        _require(_zero(-cosine.subs(t, 0) - scale / (scale**2 + freq**2)), "lap-zero")
        plain = _integrate_fast(sp.exp(-scale * t), t, 0, sp.oo)
        _require(plain is not None and _zero(plain - 1 / scale), "lap-one")
        difference = 1 / scale - scale / (scale**2 + freq**2)
        _require(_zero(difference - freq**2 / (scale * (scale**2 + freq**2))), "lap-gap")
        closed = sp.Rational(1, 2) * sp.log(1 + freq**2 / scale**2)
        _require(_zero(sp.diff(closed, scale) + freq**2 / (scale * (scale**2 + freq**2))), "lap-param")
        _require(_zero(sp.limit(closed, scale, sp.oo)), "lap-far")
        primitive = k * sp.log(1 + k**2) - 2 * k + 2 * sp.atan(k)
        _require(_zero(sp.diff(primitive, k) - sp.log(1 + k**2)), "log-prim")
        value = sp.simplify((primitive.subs(k, 1) - primitive.subs(k, 0)) / 2)
        goal = -1 + sp.log(2) / 2 + sp.pi / 4
        _require(_zero(value - goal), "damped-value")
        return goal

    return _fact("damped-log-sine", build)


def _wallis_plain():
    """∫_0^1 (x-1)/((x+1) log x) dx = log(π/2), by the Wallis product."""

    def build():
        x = sp.Symbol("_x", positive=True)
        t = sp.Symbol("_t", real=True)
        _require(_zero(sp.diff(x**t, t) - x**t * sp.log(x)), "xt-diff")
        _require(_zero(x**1 - x**0 - (x - 1)), "xt-ends")
        n = sp.Symbol("_n", integer=True, nonnegative=True)
        degree = sp.Symbol("_N", integer=True, positive=True)
        ratio = sp.Symbol("_r")
        partial = sp.summation(((-1) ** n) * ratio**n, (n, 0, degree - 1))
        claim = (1 - (-ratio) ** degree) / (1 + ratio)
        _require(_zero(partial - claim), "alt-sum")
        _require(_zero((1 + x) * claim.subs(ratio, x) - (1 - (-x) ** degree)), "alt-rem")
        _require(_zero(sp.integrate(x ** (n + t), (x, 0, 1)) - 1 / (n + t + 1)), "term")
        _require(
            _zero(sp.integrate(1 / (n + t + 1), (t, 0, 1)) - sp.log((n + 2) / (n + 1))),
            "log-term",
        )
        major = sp.integrate(1 / (degree + t + 1), (t, 0, 1))
        _require(_closed(major) and _zero(major - sp.log((degree + 2) / (degree + 1))), "major")
        _require(sp.limit(major, degree, sp.oo) == 0, "major-lim")
        step = sp.Symbol("_j", integer=True, nonnegative=True)
        even = (2 * step + 2) / (2 * step + 1)
        odd = (2 * step + 2) / (2 * step + 3)
        wallis = (2 * (step + 1)) ** 2 / ((2 * (step + 1) - 1) * (2 * (step + 1) + 1))
        _require(_zero(even * odd - wallis), "pair")
        _require(
            sp.simplify(sp.expand_log(sp.log(even) - sp.log((2 * step + 3) / (2 * step + 2)) - sp.log(wallis), force=True))
            == 0,
            "pair-log",
        )
        count = sp.Symbol("_M", integer=True, positive=True)
        index = sp.Symbol("_m", integer=True, positive=True)
        product = sp.simplify(
            sp.product((2 * index) ** 2 / ((2 * index - 1) * (2 * index + 1)), (index, 1, count))
        )
        _require(_closed(product), "product")
        limit = sp.limit(sp.log(product), count, sp.oo)
        goal = sp.log(sp.pi / 2)
        _require(_zero(limit - goal), "wallis-lim")
        _require(sp.ask(sp.Q.positive(sp.pi / 2)) is True, "pi-pos")
        return goal

    return _fact("wallis-log", build)


def _wallis_log(integrand, symbol, lo, hi):
    """The Wallis integral and its weighted sibling x times that integrand."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    plain = (symbol - 1) / ((symbol + 1) * sp.log(symbol))
    weighted = symbol * (symbol - 1) / ((symbol + 1) * sp.log(symbol))
    if integrand == plain:
        return _wallis_plain()
    if integrand != weighted:
        return None
    value = _wallis_plain()
    if value is None:
        return None
    x = sp.Symbol("_x", positive=True)
    t = sp.Symbol("_t", positive=True)
    _require(_zero(weighted.subs(symbol, x) - ((x - 1) / sp.log(x) - plain.subs(symbol, x))), "split")
    _require(_zero(sp.integrate(x**t, (x, 0, 1)) - 1 / (t + 1)), "inner")
    width = sp.integrate(1 / (t + 1), (t, 0, 1))
    _require(width is not None and _zero(width - sp.log(2)), "log2")
    total = sp.simplify(width - value)
    goal = -sp.log(sp.pi) + 2 * sp.log(2)
    _require(_zero(total - goal), "weighted")
    return total


def _artanh_wallis(integrand, symbol, lo, hi):
    """∫_0^1 log((2+x)/(2-x))/(x sqrt(1-x²)) dx = π²/6."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    target = sp.log((symbol + 2) / (2 - symbol)) / (symbol * sp.sqrt(1 - symbol**2))
    if integrand != target:
        return None

    def build():
        x = sp.Symbol("_x", real=True)
        _require(
            _zero(sp.diff(sp.log((2 + x) / (2 - x)) - 2 * sp.atanh(x / 2), x)),
            "atanh-diff",
        )
        _require(_zero((sp.log((2 + x) / (2 - x)) - 2 * sp.atanh(x / 2)).subs(x, 0)), "atanh-zero")
        u = sp.Symbol("_u")
        n = sp.Symbol("_n", integer=True, nonnegative=True)
        series = sp.summation(u ** (2 * n + 1) / (2 * n + 1), (n, 0, sp.oo))
        gap = sp.simplify(series - sp.atanh(u))
        s = sp.Symbol("_s", positive=True)
        sample = s / (2 * (1 + s))
        _require(_zero(sp.simplify(gap.subs(u, sample))), "atanh-series")
        _require(sp.ask(sp.Q.positive(sample)) is True and sp.ask(sp.Q.positive(1 - sample)) is True, "sample")
        term = 2 * (x / 2) ** (2 * n + 1) / (2 * n + 1) / x
        claim = x ** (2 * n) / ((2 * n + 1) * 4**n)
        _require(_zero(term - claim), "coeff")
        t = sp.Symbol("_t", positive=True)
        jacob = claim.subs(x, sp.sqrt(t)) / sp.sqrt(1 - t) * (1 / (2 * sp.sqrt(t)))
        density = (
            sp.Rational(1, 2)
            * t ** (n - sp.Rational(1, 2))
            * (1 - t) ** (-sp.Rational(1, 2))
            / ((2 * n + 1) * 4**n)
        )
        _require(_zero(jacob - density), "beta-jac")
        _require(
            _zero(
                sp.Rational(1, 2) * sp.beta(n + sp.Rational(1, 2), sp.Rational(1, 2))
                - (sp.pi / 2) * sp.binomial(2 * n, n) / 4**n
            ),
            "beta-wallis",
        )
        total = sp.summation(sp.binomial(2 * n, n) / ((2 * n + 1) * 16**n), (n, 0, sp.oo))
        _require(_zero(total - sp.pi / 3), "central")
        value = sp.simplify(sp.pi / 2 * total)
        _require(_zero(value - sp.pi**2 / 6), "artanh-value")
        return sp.simplify(value)

    return _fact("artanh-wallis", build)


def _chebyshev_ratio(integrand, symbol, lo, hi):
    """The quotient is a polynomial in cos x, and that polynomial integrates to 4π."""
    if not (_zero(lo) and _zero(hi - 2 * sp.pi)) or not integrand.has(sp.sin):
        return None
    if integrand != sp.sin(4 * symbol) ** 2 * sp.sin(5 * symbol) ** 2 / sp.sin(symbol) ** 2:
        return None
    cosine = sp.cos(symbol)
    alternate = (
        sp.sin(symbol) ** 2
        * (8 * cosine**3 - 4 * cosine) ** 2
        * (16 * cosine**4 - 12 * cosine**2 + 1) ** 2
    )
    _require(sp.simplify(sp.expand_trig(integrand - alternate)) == 0, "cheb-id")
    # manual=True spends far longer than the heuristic on this polynomial.
    fast = sp.integrate(sp.expand(alternate), (symbol, lo, hi))
    _require(_closed(fast), "cheb-int")
    return sp.simplify(fast)


def _sine_square_log(integrand, symbol, lo, hi):
    """x = sin² θ turns the log into an elementary integral on [0, π/4]."""
    if not (_zero(lo) and _zero(hi - sp.Rational(1, 2))) or not integrand.has(sp.log):
        return None
    if integrand != sp.log(-sp.sqrt(symbol) + sp.sqrt(1 - symbol)):
        return None

    def build():
        import sympy.calculus.util as util

        theta = sp.Symbol("_th", real=True)
        interval = sp.Interval(0, sp.pi / 4)
        _require(_zero(util.minimum(sp.cos(theta), theta, interval) - sp.sqrt(2) / 2), "min-cos")
        _require(_zero(util.minimum(sp.sin(theta), theta, interval)), "min-sin")
        _require(_zero(util.minimum(sp.cos(theta) - sp.sin(theta), theta, interval)), "min-diff")
        _require(_zero(sp.sin(sp.pi / 4) ** 2 - sp.Rational(1, 2)), "end")
        _require(_zero(sp.diff(sp.sin(theta) ** 2, theta) - 2 * sp.sin(theta) * sp.cos(theta)), "jac")
        x = sp.sin(theta) ** 2
        _require(
            _zero((sp.sqrt(1 - x) - sp.sqrt(x)) ** 2 - (1 - 2 * sp.sqrt(x * (1 - x)))),
            "left-square",
        )
        _require(_zero((sp.cos(theta) - sp.sin(theta)) ** 2 - (1 - sp.sin(2 * theta))), "right-square")
        _require(_zero(sp.sin(2 * theta) - 2 * sp.sin(theta) * sp.cos(theta)), "double")
        nonnegative = sp.Symbol("_y", nonnegative=True)
        _require(sp.refine(sp.Abs(nonnegative)) == nonnegative, "abs")
        substituted = 2 * sp.sin(theta) * sp.cos(theta) * sp.log(sp.cos(theta) - sp.sin(theta))
        fast = _integrate_fast(substituted, theta, 0, sp.pi / 4)
        _require(fast is not None and _closed(fast), "sub-int")
        goal = -sp.pi / 8 - sp.Rational(1, 4)
        _require(_zero(fast - goal), "sub-value")
        return sp.simplify(fast)

    return _fact("sine-square-log", build)


def _constant_log_span(integrand, symbol, lo, hi):
    """sqrt(log(A-x)) / (sqrt(log(A-x))+sqrt(log(x-B))) averages to 1/2."""
    if _has_infinity(lo) or _has_infinity(hi):
        return None
    if not integrand.has(sp.log) or not _has_square_root(integrand):
        return None
    if sp.count_ops(integrand) > 25:
        return None
    left = sp.Wild("A", exclude=[symbol])
    right = sp.Wild("B", exclude=[symbol])
    numerator = sp.sqrt(sp.log(left - symbol))
    matched = integrand.match(numerator / (numerator + sp.sqrt(sp.log(symbol - right))))
    if not matched:
        return None
    _require(_zero(lo + hi - (matched[left] + matched[right])), "span")
    total = sp.simplify(integrand + integrand.subs(symbol, lo + hi - symbol))
    _require(_closed(total) and not total.has(symbol) and _zero(total - 1), "sum")
    return sp.simplify((hi - lo) * sp.Rational(1, 2))


def _cosine_over_square(integrand, symbol, lo, hi):
    """∫_0^∞ (cos(a x)-cos(b x))/x**2 dx = π(b-a)/2 for a>0 and b>0.

    Parts moves the integral to ∫ (b sin(b x)-a sin(a x))/x dx. Each term is
    the Dirichlet integral after x → c x. The Laplace transform of sin identifies
    ∫_0^∞ sin(t)/t dt with π/2: its s-derivative is -1/(s²+1), and the value
    vanishes as s→∞ because |sin t|≤t.
    """
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.cos):
        return None
    coeff_a = sp.Wild("A", exclude=[symbol])
    coeff_b = sp.Wild("B", exclude=[symbol])
    matched = integrand.match((sp.cos(coeff_a * symbol) - sp.cos(coeff_b * symbol)) / symbol**2)
    if not matched:
        return None
    first = matched[coeff_a]
    second = matched[coeff_b]
    if first.has(symbol) or second.has(symbol):
        return None

    def build():
        a = sp.Symbol("_a", positive=True)
        b = sp.Symbol("_b", positive=True)
        x = sp.Symbol("_x", positive=True)
        height = sp.cos(a * x) - sp.cos(b * x)
        slope = -a * sp.sin(a * x) + b * sp.sin(b * x)
        _require(_zero(sp.diff(height, x) - slope), "parts-diff")
        _require(_zero(sp.diff(-1 / x, x) - x ** (-2)), "parts-measure")
        _require(_zero(sp.limit(height / x, x, 0)), "parts-zero")
        _require(_zero(sp.limit(height / x, x, sp.oo)), "parts-inf")
        _require(_dirichlet_half() is True, "dirichlet")
        old = sp.Symbol("_u", positive=True)
        scale = sp.Symbol("_c", positive=True)
        _require(
            _zero(sp.sin(scale * (old / scale)) / (old / scale) * (1 / scale) - sp.sin(old) / old),
            "scale",
        )
        return True

    if _fact("cosine-over-square", build) is not True:
        return None
    return sp.simplify(sp.pi * (second - first) / 2)


def _dirichlet_half():
    """∫_0^∞ sin(t)/t dt = π/2, from the Laplace transform of sin."""

    def build():
        decay = sp.Symbol("_s", positive=True)
        line = sp.Symbol("_t", positive=True)
        anti = sp.exp(-decay * line) * (-decay * sp.sin(line) - sp.cos(line)) / (decay**2 + 1)
        _require(_zero(sp.diff(anti, line) - sp.exp(-decay * line) * sp.sin(line)), "laplace-anti")
        _require(_zero(sp.limit(anti, line, sp.oo)), "laplace-inf")
        _require(_zero(-anti.subs(line, 0) - 1 / (decay**2 + 1)), "laplace-zero")
        angle = sp.Symbol("_theta", real=True)
        _require(_zero((1 - sp.cos(angle)) - 2 * sp.sin(angle / 2) ** 2), "one-minus-cos")
        _require(_zero((1 + sp.cos(angle)) - 2 * sp.cos(angle / 2) ** 2), "one-plus-cos")
        above = angle - sp.sin(angle)
        below = angle + sp.sin(angle)
        _require(_zero(sp.diff(above, angle) - 2 * sp.sin(angle / 2) ** 2), "sin-upper")
        _require(_zero(sp.diff(below, angle) - 2 * sp.cos(angle / 2) ** 2), "sin-lower")
        _require(_zero(above.subs(angle, 0)) and _zero(below.subs(angle, 0)), "sin-origin")
        real = sp.Symbol("_z", real=True)
        _require(sp.ask(sp.Q.nonnegative(real**2)) is True, "square")
        _require(_zero(sp.integrate(sp.exp(-decay * line), (line, 0, sp.oo)) - 1 / decay), "exp-tail")
        _require(_zero(sp.limit(1 / decay, decay, sp.oo)), "tail-inf")
        closed = sp.pi / 2 - sp.atan(decay)
        _require(_zero(sp.diff(closed, decay) + 1 / (decay**2 + 1)), "dirichlet-diff")
        _require(_zero(sp.limit(closed, decay, sp.oo)), "dirichlet-inf")
        _require(_zero(closed.subs(decay, 0) - sp.pi / 2), "dirichlet-zero")
        return True

    return _fact("dirichlet-half", build)


def _sin_product(integrand, symbol, lo, hi):
    """∫_0^∞ sin(a x) sin(b x)/x dx = log((a+b)/(a-b))/2 for a>b>0."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.sin):
        return None
    left = sp.Wild("A", exclude=[symbol])
    right = sp.Wild("B", exclude=[symbol])
    matched = integrand.match(sp.sin(left * symbol) * sp.sin(right * symbol) / symbol)
    if not matched:
        return None
    coeff_a = matched[left]
    coeff_b = matched[right]

    def build():
        a = sp.Symbol("_A", real=True)
        b = sp.Symbol("_B", real=True)
        _require(
            _zero(
                sp.expand_trig(
                    sp.sin(a) * sp.sin(b) - (sp.cos(a - b) - sp.cos(a + b)) / 2
                )
            ),
            "product",
        )
        p = sp.Symbol("_p", positive=True)
        q = sp.Symbol("_q", positive=True)
        x = sp.Symbol("_x", positive=True)
        s = sp.Symbol("_s", positive=True)
        c = sp.Symbol("_c", positive=True)
        anti = sp.exp(-s * x) * (-s * sp.cos(c * x) + c * sp.sin(c * x)) / (s**2 + c**2)
        _require(_zero(sp.diff(anti, x) - sp.exp(-s * x) * sp.cos(c * x)), "cos-anti")
        _require(_zero(sp.limit(anti, x, sp.oo)), "cos-inf")
        _require(_zero(-anti.subs(x, 0) - s / (s**2 + c**2)), "cos-lap")
        line = sp.Symbol("_u", positive=True)
        primitive = sp.Rational(1, 2) * sp.log((line**2 + p**2) / (line**2 + q**2))
        integrand_s = line / (line**2 + p**2) - line / (line**2 + q**2)
        _require(_zero(sp.diff(primitive, line) - integrand_s), "frullani")
        _require(_zero(sp.limit(primitive, line, sp.oo)), "frullani-inf")
        # ∫_s^∞ of that derivative is -primitive(s), and the s→0 value is log(q/p).
        at_zero = sp.limit(-primitive, line, 0)
        _require(_zero(at_zero - sp.log(q / p)), "frullani-zero")
        return True

    if _fact("sin-product", build) is not True:
        return None
    return sp.simplify(sp.log((coeff_a + coeff_b) / (coeff_a - coeff_b)) / 2)

def _catalan_tangent():
    """∫_0^{π/4} log(tan θ) dθ = -G, from the geometric series of 1/(1+u^2)."""

    def build():
        u = sp.Symbol("_u")
        index = sp.Symbol("_k", integer=True, nonnegative=True)
        series = sp.summation((-1) ** index * u ** (2 * index), (index, 0, sp.oo))
        piece = sp.simplify(series)
        branch = None
        if isinstance(piece, sp.Piecewise):
            for expr, cond in piece.args:
                if cond == True or expr.has(sp.Sum):
                    continue
                branch = expr
                break
        else:
            branch = piece
        _require(branch is not None and _zero(branch - 1 / (1 + u**2)), "geo")
        term = sp.integrate(((-1) ** index) * u ** (2 * index) * sp.log(u), (u, 0, 1))
        _require(_closed(term) and _zero(term + (-1) ** index / (2 * index + 1) ** 2), "term")
        total = sp.summation(term, (index, 0, sp.oo))
        _require(_closed(total) and _zero(total + sp.Catalan), "sum")
        _require(_zero(sp.diff(sp.atan(u), u) * (1 + u**2) - 1), "jac")
        _require(_zero(sp.simplify(sp.tan(sp.atan(u)) - u)), "tan")
        _require(_zero(sp.tan(sp.pi / 4) - 1) and _zero(sp.tan(0)), "ends")
        return -sp.Catalan

    return _fact("catalan-tangent", build)


def _quarter_log_sums():
    """∫_0^{π/4} log(sin) and ∫_0^{π/4} log(cos), from the half-period value and Catalan."""

    def build():
        theta = sp.Symbol("_th", real=True)
        sine = sp.log(sp.sin(theta))
        cosine = sp.log(sp.cos(theta))
        full = _log_sine_quarter(sine, theta, 0, sp.pi / 2)
        _require(full is not None and _zero(full + sp.pi * sp.log(2) / 2), "full")
        ident = sine + cosine - sp.log(sp.sin(2 * theta)) + sp.log(2)
        _require(sp.simplify(sp.exp(ident)) == 1, "exp")
        _require(sp.simplify(sp.logcombine(ident.subs(theta, sp.pi / 8), force=True)) == 0, "point")
        _require(_zero(sp.diff(2 * theta, theta) - 2), "jac")
        summed = sp.simplify(full / 2 - sp.pi * sp.log(2) / 4)
        _require(_zero(summed + sp.pi * sp.log(2) / 2), "pair")
        difference = _catalan_tangent()
        _require(difference is not None and _zero(difference + sp.Catalan), "diff")
        sine_quarter = sp.simplify((summed + difference) / 2)
        cosine_quarter = sp.simplify((summed - difference) / 2)
        return {"sum": summed, "sin": sine_quarter, "cos": cosine_quarter, "full": full}

    return _fact("quarter-log-sums", build)


def _semicircle_log(integrand, symbol, lo, hi):
    """x = 2+2 cos θ turns ∫_0^4 log(x)/sqrt(4x-x^2) dx into a cosine quarter that cancels."""
    if not (_zero(lo) and _zero(hi - 4)) or not integrand.has(sp.log):
        return None
    target = sp.log(symbol) / sp.sqrt(4 * symbol - symbol**2)
    if not _zero(integrand - target):
        return None
    theta = sp.Symbol("_th", real=True)
    line = 2 + 2 * sp.cos(theta)
    _require(_zero(sp.diff(line, theta) + 2 * sp.sin(theta)), "dx")
    _require(_zero(sp.simplify(4 * line - line**2 - 4 * sp.sin(theta) ** 2)), "rad")
    _require(_zero(1 + sp.cos(theta) - 2 * sp.cos(theta / 2) ** 2), "half")
    logged = sp.log(2 * (1 + sp.cos(theta))) - (2 * sp.log(2) + 2 * sp.log(sp.cos(theta / 2)))
    _require(sp.simplify(sp.exp(logged.subs(theta, sp.pi / 2))) == 1, "log-point")
    _require(sp.simplify(sp.exp(logged)) == 1, "log-exp")
    quarter = _log_sine_quarter(sp.log(sp.cos(theta)), theta, 0, sp.pi / 2)
    _require(quarter is not None, "quarter")
    _require(_zero(sp.diff(theta / 2, theta) - sp.Rational(1, 2)), "sub")
    total = sp.simplify(2 * sp.pi * sp.log(2) + 4 * quarter)
    _require(_zero(total), "cancel")
    return sp.Integer(0)


def _shifted_log_quadratic(integrand, symbol, lo, hi):
    """x = tan θ - 1 turns ∫_0^∞ log(x)/(x^2+2x+2) dx into π log 2 / 8."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.log):
        return None
    target = sp.log(symbol) / (symbol**2 + 2 * symbol + 2)
    if not _zero(integrand - target):
        return None
    theta = sp.Symbol("_th", real=True)
    line = sp.tan(theta) - 1
    measure = sp.diff(line, theta) / (line**2 + 2 * line + 2)
    _require(_zero(sp.simplify(measure - 1)), "dx")
    _require(_zero(sp.tan(sp.pi / 4) - 1), "lo")
    shift = theta - sp.pi / 4
    sine_diff = sp.sin(theta) - sp.cos(theta) - sp.sqrt(2) * sp.sin(shift)
    _require(_zero(sp.expand_trig(sine_diff)), "shift")
    _require(
        _zero(sp.expand_trig(sp.cos(shift + sp.pi / 4) - (sp.cos(shift) - sp.sin(shift)) / sp.sqrt(2))),
        "cos",
    )
    values = _quarter_log_sums()
    _require(values is not None, "quarters")
    # ∫_{π/4}^{π/2} log(tan θ-1) dθ = ∫_0^{π/4} [log 2 / 2 + log sin φ - log cos(φ+π/4)] dφ
    # and ∫_0^{π/4} log cos(φ+π/4) dφ = ∫_0^{π/2} log cos - ∫_0^{π/4} log cos.
    total = sp.simplify(sp.pi * sp.log(2) / 8 + values["sum"] - values["full"])
    _require(_zero(total - sp.pi * sp.log(2) / 8), "value")
    return sp.pi * sp.log(2) / 8


def _log_product_unit(integrand, symbol, lo, hi):
    """∫_0^1 log(1-x)log(1+x) dx by parts, down to ∫ log(1-x)/(1+x) dx."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    target = sp.log(1 - symbol) * sp.log(1 + symbol)
    if not _zero(integrand - target):
        return None

    def build():
        x = sp.Symbol("_x", real=True)
        primitive = (x - 1) * sp.log(1 - x) - x
        _require(_zero(sp.diff(primitive, x) - sp.log(1 - x)), "parts")
        _require(_zero(sp.limit(sp.log(1 + x) * primitive, x, 0)), "edge0")
        _require(_zero(sp.limit(sp.log(1 + x) * primitive, x, 1) + sp.log(2)), "edge1")
        _require(_zero((x - 1) / (x + 1) - (1 - 2 / (x + 1))), "split")
        plain = sp.integrate(sp.log(1 - x), (x, 0, 1))
        weight = sp.integrate(x / (1 + x), (x, 0, 1))
        folded = sp.integrate(sp.log(1 - x) / (1 + x), (x, 0, 1))
        _require(all(_closed(item) for item in (plain, weight, folded)), "pieces")
        _require(_zero(plain + 1), "plain")
        _require(_zero(weight - (1 - sp.log(2))), "weight")
        reduced = -sp.log(2) - (plain - 2 * folded) + weight
        return sp.simplify(reduced)

    return _fact("log-product-unit", build)


def _csc_catalan(integrand, symbol, lo, hi):
    """∫_0^{π/2} x csc x dx = 2G, by writing x as an inner integral."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.sin):
        return None
    if not _zero(integrand - symbol / sp.sin(symbol)):
        return None

    def build():
        x = sp.Symbol("_x", real=True)
        height = sp.log(sp.tan(x / 2))
        _require(_zero(sp.simplify(sp.diff(height, x) - 1 / sp.sin(x))), "anti")
        _require(_zero(sp.limit(height, x, sp.pi / 2)), "upper")
        bound = sp.Symbol("_b", positive=True)
        accumulated = sp.Integral(height.subs(x, bound) - height, (x, 0, bound))
        direct = bound / sp.sin(bound)
        _require(_zero(sp.simplify(sp.diff(accumulated, bound) - direct)), "leibniz")
        _require(_zero(sp.simplify(accumulated.subs(bound, 0))), "origin")
        width = sp.Symbol("_u", real=True)
        _require(_zero(sp.diff(2 * width, width) - 2), "half")
        catalan = _catalan_tangent()
        _require(catalan is not None, "catalan")
        value = sp.simplify(-2 * catalan)
        _require(_zero(value - 2 * sp.Catalan), "value")
        return True

    if _fact("csc-catalan", build) is not True:
        return None
    return 2 * sp.Catalan


def _coth_log_line(integrand, symbol, lo, hi):
    """∫_0^∞ log((e^x+1)/(e^x-1)) dx = π^2/4, from the odd-reciprocal squares."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.log) or not integrand.has(sp.exp):
        return None
    target = sp.log((sp.exp(symbol) + 1) / (sp.exp(symbol) - 1))
    if not _zero(integrand - target):
        return None

    def build():
        y = sp.Symbol("_y", positive=True)
        index = sp.Symbol("_m", integer=True, nonnegative=True)
        pulled = sp.log((1 + y) / (1 - y))
        _require(sp.simplify(sp.exp(pulled - target.subs(symbol, -sp.log(y)))) == 1, "sub")
        series = sp.summation(2 * y ** (2 * index + 1) / (2 * index + 1), (index, 0, sp.oo))
        piece = sp.simplify(series)
        branch = None
        if isinstance(piece, sp.Piecewise):
            for expr, cond in piece.args:
                if cond == True or expr.has(sp.Sum):
                    continue
                branch = expr
                break
        else:
            branch = piece
        _require(branch is not None, "series")
        rewritten = sp.simplify(branch.rewrite(sp.log) - pulled)
        _require(_zero(rewritten) or sp.simplify(sp.exp(rewritten)) == 1, "series-log")
        term = sp.integrate(2 * y ** (2 * index) / (2 * index + 1), (y, 0, 1))
        _require(_closed(term) and _zero(term - 2 / (2 * index + 1) ** 2), "term")
        total = sp.summation(1 / (2 * index + 1) ** 2, (index, 0, sp.oo))
        _require(_closed(total) and _zero(total - sp.pi**2 / 8), "odds")
        return sp.simplify(2 * total)

    return _fact("coth-log-line", build)


def _atan_over_power(integrand, symbol, lo, hi):
    """∫_0^1 atan(x^n)/x dx = G/n for n>0."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.atan):
        return None
    degree = sp.Wild("n", exclude=[symbol])
    matched = integrand.match(sp.atan(symbol**degree) / symbol)
    if not matched:
        return None
    power = matched[degree]
    if power.has(symbol) or power == 0 or getattr(power, "is_nonpositive", False):
        return None

    def build():
        x = sp.Symbol("_x", positive=True)
        n = sp.Symbol("_n", positive=True)
        u = sp.Symbol("_u", positive=True)
        _require(_zero(sp.diff(x**n, x) / (n * x**n) - 1 / x), "jac")
        index = sp.Symbol("_k", integer=True, nonnegative=True)
        series = sp.summation((-1) ** index * u ** (2 * index + 1) / (2 * index + 1), (index, 0, sp.oo))
        piece = sp.simplify(series)
        branch = None
        if isinstance(piece, sp.Piecewise):
            for expr, cond in piece.args:
                if cond == True or getattr(expr, "has", lambda *_: False)(sp.Sum):
                    continue
                branch = expr
                break
        else:
            branch = piece
        _require(branch is not None and _zero(sp.simplify(branch - sp.atan(u))), "atan")
        term = sp.integrate((-1) ** index * u ** (2 * index) / (2 * index + 1), (u, 0, 1))
        _require(_closed(term) and _zero(term - (-1) ** index / (2 * index + 1) ** 2), "term")
        total = sp.summation(term, (index, 0, sp.oo))
        _require(_closed(total) and _zero(total - sp.Catalan), "sum")
        return True

    if _fact("atan-over-power", build) is not True:
        return None
    return sp.simplify(sp.Catalan / power)


def _half_line_log_linear(integrand, symbol, lo, hi):
    """x = tan θ turns ∫_0^∞ log(1+x)/(1+x^2) dx into G + π log 2 / 4."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.log):
        return None
    target = sp.log(1 + symbol) / (1 + symbol**2)
    if not _zero(integrand - target):
        return None
    theta = sp.Symbol("_th", real=True)
    subbed = sp.simplify(integrand.subs(symbol, sp.tan(theta)) * (1 + sp.tan(theta) ** 2))
    _require(_logs_equivalent(subbed, sp.log(1 + sp.tan(theta))), "sub")
    combination = sp.sin(theta) + sp.cos(theta)
    _require(_zero(sp.expand_trig(combination - sp.sqrt(2) * sp.sin(theta + sp.pi / 4))), "amp")
    ident = sp.log(1 + sp.tan(theta)) - (sp.log(combination) - sp.log(sp.cos(theta)))
    _require(_zero(sp.exp(ident.subs(theta, sp.pi / 6)) - 1), "log-point")
    _require(_zero(sp.exp(ident) - 1), "log-exp")
    values = _quarter_log_sums()
    _require(values is not None, "quarters")
    # ∫_0^{π/2} log sin(θ+π/4) dθ = 2 (∫_0^{π/2} log sin - ∫_0^{π/4} log sin)
    shifted = sp.simplify(2 * (values["full"] - values["sin"]))
    total = sp.simplify(sp.pi * sp.log(2) / 4 + shifted - values["full"])
    goal = sp.Catalan + sp.pi * sp.log(2) / 4
    _require(_zero(total - goal), "value")
    return sp.simplify(goal)


def _cos_shift_segment(integrand, symbol, lo, hi):
    """∫_0^a x/(cos x cos(a-x)) dx = a log(sec a)/sin a.

    Symmetry makes the weight a/2. The product identity and u = 2x-a fold the
    integral onto 1/(cos a + cos u). The half-angle substitution turns that
    antiderivative into a rational identity, so the check never simplifies an
    absolute-value derivative.
    """
    if not _zero(lo) or not integrand.has(sp.cos):
        return None
    angle = sp.Wild("w")
    matched = integrand.match(symbol * sp.cos(symbol) ** -1 * sp.cos(angle) ** -1)
    if not matched:
        matched = integrand.match(symbol / (sp.cos(symbol) * sp.cos(angle)))
    if not matched:
        return None
    if not _zero(matched[angle] - (hi - symbol)) or _zero(hi):
        return None
    parameter = hi

    def build():
        a = sp.Symbol("_a", positive=True)
        x = sp.Symbol("_x", real=True)
        u = sp.Symbol("_u", real=True)
        density = 1 / (sp.cos(x) * sp.cos(a - x))
        _require(_zero(density - density.subs(x, a - x)), "sym")
        weight = sp.Symbol("_f")
        _require(_zero(x * weight + (a - x) * weight - a * weight), "king")
        _require(
            _zero(sp.expand_trig(sp.cos(x) * sp.cos(a - x) - (sp.cos(a) + sp.cos(2 * x - a)) / 2)),
            "prod",
        )
        _require(_zero(sp.diff(2 * x - a, x) - 2), "jac")
        reduced = 2 / (sp.cos(a) + sp.cos(2 * x - a))
        goal = 1 / (sp.cos(a) + sp.cos(u))
        folded = reduced.subs(x, (u + a) / 2) * sp.Rational(1, 2)
        _require(_zero(folded - goal), "sub")
        _require(_zero(goal - goal.subs(u, -u)), "even")
        tangent = sp.tan(u / 2)
        cotangent = 1 / sp.tan(a / 2)
        anti = (sp.log(cotangent + tangent) - sp.log(cotangent - tangent)) / sp.sin(a)
        slope = sp.diff(anti, u)
        height, half = sp.symbols("_T _C", positive=True)
        replaced = (slope - goal).subs(
            {
                sp.tan(u / 2): height,
                sp.tan(a / 2): 1 / half,
                sp.sin(a): 2 * half / (half**2 + 1),
                sp.cos(a): (half**2 - 1) / (half**2 + 1),
                sp.cos(u): (1 - height**2) / (1 + height**2),
            }
        )
        _require(sp.cancel(replaced) == 0, "anti")
        _require(_zero(sp.diff(sp.tan(u / 2), u) - (1 + sp.tan(u / 2) ** 2) / 2), "dt")
        _require(_zero(sp.sin(a) - 2 * cotangent / (1 + cotangent**2)), "sin")
        _require(_zero(sp.cos(a) - (cotangent**2 - 1) / (cotangent**2 + 1)), "cos-a")
        _require(_zero(sp.cos(u) - (1 - tangent**2) / (1 + tangent**2)), "cos-u")
        _require(_zero(anti.subs(u, 0)), "zero")
        num = sp.tan(a / 2) + cotangent
        den = cotangent - sp.tan(a / 2)
        _require(_zero(sp.log(num / den) - sp.log(sp.sec(a))), "end")
        _require(
            _zero(a * sp.log(sp.sec(a)) / sp.sin(a) - a * (sp.log(num / den) / sp.sin(a))),
            "value",
        )
        return True

    if _fact("cos-shift-segment", build) is not True:
        return None
    return sp.simplify(parameter * sp.log(sp.sec(parameter)) / sp.sin(parameter))


def _reciprocal_power_ray(integrand, symbol, lo, hi):
    """∫_1^∞ dx/(n x^n + x) = log(n/(n+1))/(1-n) for n>1."""
    if not (_zero(lo - 1) and hi == sp.oo):
        return None
    degree = sp.Wild("n", exclude=[symbol])
    matched = integrand.match(1 / (degree * symbol**degree + symbol))
    if not matched:
        return None
    power = matched[degree]
    if power.has(symbol):
        return None

    def build():
        x = sp.Symbol("_x", positive=True)
        shift = sp.Symbol("_m", positive=True)
        n = shift + 1
        w = x ** (n - 1)
        _require(_zero(sp.diff(sp.log(w), x) - (n - 1) / x), "dlog")
        anti = sp.log(w / (1 + n * w)) / (n - 1)
        stable = sp.log(1 / (x ** (1 - n) + n)) / (n - 1)
        _require(_zero(sp.simplify(anti - stable)), "stable")
        slope = 1 / (x * (1 + n * x ** (n - 1)))
        _require(_zero(sp.simplify(sp.diff(anti, x) - slope)), "anti")
        _require(_zero(sp.limit(stable, x, sp.oo) - sp.log(1 / n) / (n - 1)), "inf")
        _require(_zero(anti.subs(x, 1) - sp.log(1 / (1 + n)) / (n - 1)), "one")
        gap = sp.simplify(sp.limit(stable, x, sp.oo) - anti.subs(x, 1))
        goal = sp.log(n / (n + 1)) / (1 - n)
        _require(_zero(gap - goal), "gap")
        return True

    if _fact("reciprocal-power-ray", build) is not True:
        return None
    return sp.simplify(sp.log(power / (power + 1)) / (1 - power))


def _gamma_reflection_unit(integrand, symbol, lo, hi):
    """∫_0^1 dx/(π csc(πx)+Γ(x)^2) = 1/π^2, by reflection."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.gamma):
        return None
    target = 1 / (sp.pi * sp.csc(sp.pi * symbol) + sp.gamma(symbol) ** 2)
    if not _zero(integrand - target):
        return None

    def build():
        x = sp.Symbol("_x", real=True)
        _require(_zero(sp.simplify(sp.gamma(x) * sp.gamma(1 - x) * sp.sin(sp.pi * x) - sp.pi)), "reflect")
        scale = sp.pi * sp.csc(sp.pi * x)
        weight = sp.gamma(x) ** 2
        _require(_zero(sp.simplify(sp.gamma(1 - x) * sp.gamma(x) / scale - 1)), "ratio")
        left = 1 / (scale + weight)
        other = weight / (scale * (scale + weight))
        partner, mass = sp.symbols("_s _g", positive=True)
        _require(_zero(sp.simplify(1 / (partner + partner**2 / mass) - mass / (partner * (partner + mass)))), "flip")
        _require(_zero(sp.simplify(1 / (partner + mass) + mass / (partner * (partner + mass)) - 1 / partner)), "sum")
        _require(_zero(sp.simplify(1 / scale - sp.sin(sp.pi * x) / sp.pi)), "sine")
        primitive = -sp.cos(sp.pi * x) / sp.pi**2
        _require(_zero(sp.diff(primitive, x) - sp.sin(sp.pi * x) / sp.pi), "anti")
        _require(_zero(primitive.subs(x, 1) - primitive.subs(x, 0) - 2 / sp.pi**2), "ends")
        _require(_zero(sp.diff(1 - x, x) + 1), "swap")
        return sp.Integer(1) / sp.pi**2

    return _fact("gamma-reflection-unit", build)


def _log_sine_quadratic(integrand, symbol, lo, hi):
    """∫_0^{π/2} log(A sin^2+B cos^2) dθ = π log((√A+√B)/2) for A>0, B>0."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.log):
        return None
    left = sp.Wild("A", exclude=[symbol])
    right = sp.Wild("B", exclude=[symbol])
    matched = integrand.match(sp.log(left * sp.sin(symbol) ** 2 + right * sp.cos(symbol) ** 2))
    if not matched:
        return None
    coeff_a = matched[left]
    coeff_b = matched[right]
    if coeff_a.has(symbol) or coeff_b.has(symbol):
        return None
    if coeff_a == coeff_b:
        value = sp.pi * sp.log(coeff_a) / 2
        _require(_zero(sp.simplify(coeff_a * sp.sin(symbol) ** 2 + coeff_a * sp.cos(symbol) ** 2 - coeff_a)), "equal")
        return sp.simplify(value)

    def build():
        a = sp.Symbol("_a", positive=True)
        b = sp.Symbol("_b", positive=True)
        theta = sp.Symbol("_th", real=True)
        slope = 2 * a * sp.sin(theta) ** 2 / (a**2 * sp.sin(theta) ** 2 + b**2 * sp.cos(theta) ** 2)
        derived = sp.integrate(slope, (theta, 0, sp.pi / 2))
        _require(_closed(derived), "derived")
        gap = sp.simplify(derived - sp.pi / (a + b))
        if isinstance(gap, sp.Piecewise):
            for expr, cond in gap.args:
                if cond == True:
                    _require(_zero(sp.simplify(expr.subs(b, a))), "slope-eq")
                else:
                    _require(_zero(expr), "slope-ne")
        else:
            _require(_zero(gap), "slope")
        base = sp.pi * sp.log(b)
        _require(_zero(base - sp.pi * sp.log((b + b) / 2)), "base")
        return True

    if _fact("log-sine-quadratic", build) is not True:
        return None
    return sp.simplify(sp.pi * sp.log((sp.sqrt(coeff_a) + sp.sqrt(coeff_b)) / 2))


def _atan_over_linear(integrand, symbol, lo, hi):
    """∫_0^1 atan(x)/(1+x) dx = π log 2 / 8.

    atan(x) = ∫_0^x dy/(1+y^2). The iterated integral is
    ∫_0^1 (log 2 - log(1+y))/(1+y^2) dy, and y = tan θ folds the second term
    into log(1+tan) on [0, π/4], whose reflection is log 2 minus itself.
    """
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.atan):
        return None
    target = sp.atan(symbol) / (1 + symbol)
    if not _zero(integrand - target):
        return None

    def build():
        x = sp.Symbol("_x", positive=True)
        y = sp.Symbol("_y", positive=True)
        bound = sp.Symbol("_b", positive=True)
        height = sp.atan(x)
        _require(_zero(sp.diff(height, x) - 1 / (1 + x**2)), "atan")
        accumulated = sp.Integral((sp.log(1 + bound) - sp.log(1 + y)) / (1 + y**2), (y, 0, bound))
        _require(_zero(sp.simplify(sp.diff(accumulated, bound) - height.subs(x, bound) / (1 + bound))), "leibniz")
        _require(_zero(sp.simplify(accumulated.subs(bound, 0))), "origin")
        theta = sp.Symbol("_th", real=True)
        measure = sp.diff(sp.tan(theta), theta) / (1 + sp.tan(theta) ** 2)
        _require(_zero(sp.simplify(measure - 1)), "tan")
        pair = sp.log(1 + sp.tan(theta)) + sp.log(1 + sp.tan(sp.pi / 4 - theta))
        _require(_zero(sp.simplify(sp.exp(pair - sp.log(2)) - 1)), "reflect")
        _require(_zero(sp.tan(sp.pi / 4) - 1) and _zero(sp.tan(0)), "ends")
        total = sp.pi * sp.log(2) / 4 - sp.pi * sp.log(2) / 8
        _require(_zero(total - sp.pi * sp.log(2) / 8), "value")
        return sp.pi * sp.log(2) / 8

    return _fact("atan-over-linear", build)


def _power_log_gap(integrand, symbol, lo, hi):
    """∫_0^1 (x**p - x**q)/log(x) dx = log((p+1)/(q+1)) for p, q > -1."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    left = sp.Wild("p", exclude=[symbol])
    right = sp.Wild("q", exclude=[symbol])
    matched = integrand.match((symbol**left - symbol**right) / sp.log(symbol))
    if not matched:
        return None
    power_p = matched[left]
    power_q = matched[right]
    if power_p.has(symbol) or power_q.has(symbol):
        return None
    if (power_p + 1).is_positive is not True or (power_q + 1).is_positive is not True:
        return None

    def build():
        degree_a = sp.Symbol("_a", positive=True)
        degree_b = sp.Symbol("_b", positive=True)
        line = sp.Symbol("_x", positive=True)
        value = sp.integrate((line**degree_a - line**degree_b) / sp.log(line), (line, 0, 1))
        goal = sp.log(degree_a + 1) - sp.log(degree_b + 1)
        _require(_closed(value) and _zero(value - goal), "gap")
        return True

    if _fact("power-log-gap", build) is not True:
        return None
    return sp.log((power_p + 1) / (power_q + 1))


def _log_over_three(integrand, symbol, lo, hi):
    """∫_1^3 log(x)/(x**2+3) dx, by scaling onto a reciprocal interval."""
    if not (_zero(lo - 1) and _zero(hi - 3)) or not integrand.has(sp.log):
        return None
    if not _zero(integrand - sp.log(symbol) / (symbol**2 + 3)):
        return None

    def build():
        width = sp.Symbol("_u", positive=True)
        line = sp.sqrt(3) * width
        measure = sp.log(line) / (line**2 + 3) * sp.diff(line, width)
        reduced = (sp.log(width) + sp.log(3) / 2) / (sp.sqrt(3) * (width**2 + 1))
        _require(_zero(sp.simplify(measure - reduced)), "scale")
        _require(_zero(line.subs(width, 1 / sp.sqrt(3)) - 1), "lo")
        _require(_zero(line.subs(width, sp.sqrt(3)) - 3), "hi")
        mirror = sp.Symbol("_v", positive=True)
        flipped = sp.log(1 / mirror) / ((1 / mirror) ** 2 + 1) * sp.diff(1 / mirror, mirror)
        direct = sp.log(mirror) / (mirror**2 + 1)
        # u = 1/v reverses [1/√3, √3], and the log piece comes back as itself,
        # so that piece equals its negative.
        _require(_zero(sp.simplify(flipped - direct)), "odd")
        _require(_zero(sp.diff(sp.atan(width), width) * (1 + width**2) - 1), "atan")
        _require(_zero(sp.tan(sp.pi / 3) - sp.sqrt(3)), "tan-hi")
        _require(_zero(sp.tan(sp.pi / 6) - 1 / sp.sqrt(3)), "tan-lo")
        span = sp.pi / 3 - sp.pi / 6
        _require(_zero(span - sp.pi / 6), "span")
        total = sp.log(3) / (2 * sp.sqrt(3)) * span
        _require(_zero(sp.simplify(total - sp.pi * sp.log(3) / (12 * sp.sqrt(3)))), "value")
        return True

    if _fact("log-over-three", build) is not True:
        return None
    return sp.pi * sp.log(3) / (12 * sp.sqrt(3))


def _secant_square_quarter(integrand, symbol, lo, hi):
    """∫_0^{π/2} dx/(a**2-sin**2 x) = π/(2 a sqrt(a**2-1)) for a>1."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.sin):
        return None
    parameter = sp.Wild("A", exclude=[symbol])
    matched = integrand.match(1 / (parameter**2 - sp.sin(symbol) ** 2))
    if not matched:
        return None
    coeff = matched[parameter]
    if coeff.has(symbol) or coeff == 0:
        return None

    def build():
        height = sp.Symbol("_a", positive=True)
        slope = sp.Symbol("_t", positive=True)
        angle = sp.atan(slope)
        original = 1 / (height**2 - sp.sin(angle) ** 2)
        changed = sp.simplify(original * sp.diff(angle, slope))
        target = 1 / (height**2 + (height**2 - 1) * slope**2)
        _require(_zero(changed - target), "tan")
        primitive = sp.atan(slope * sp.sqrt(height**2 - 1) / height) / (
            height * sp.sqrt(height**2 - 1)
        )
        _require(_zero(sp.simplify(sp.diff(primitive, slope) - target)), "anti")
        _require(_zero(primitive.subs(slope, 0)), "zero")
        # Every a>1 is sqrt(1+b**2) for some b>0, and then atan's argument
        # tends to +∞, so the upper limit is π/2.
        breadth = sp.Symbol("_b", positive=True)
        placed = sp.simplify(primitive.subs(height, sp.sqrt(1 + breadth**2)))
        _require(
            _zero(sp.limit(placed, slope, sp.oo) - sp.pi / (2 * breadth * sp.sqrt(breadth**2 + 1))),
            "upper",
        )
        formula = sp.pi / (2 * height * sp.sqrt(height**2 - 1))
        _require(
            _zero(sp.simplify(formula.subs(height, sp.sqrt(1 + breadth**2)) - sp.limit(placed, slope, sp.oo))),
            "formula",
        )
        return True

    if _fact("secant-square-quarter", build) is not True:
        return None
    return sp.pi / (2 * coeff * sp.sqrt(coeff**2 - 1))


def _biquadratic_ray(integrand, symbol, lo, hi):
    """∫_0^∞ dx/(x**4 + 2 a x**2 + 1) = π/(2 sqrt(2 a+2)) for a>-1."""
    if not (_zero(lo) and hi == sp.oo):
        return None
    base, exponent = integrand.as_base_exp()
    if exponent != -1 or not base.has(symbol):
        return None
    free = [item for item in integrand.free_symbols if item != symbol]
    if len(free) != 1:
        return None
    coeff = free[0]
    quartic = symbol**4 + 2 * coeff * symbol**2 + 1
    if not _zero(base - quartic):
        return None

    def build():
        line = sp.Symbol("_x", positive=True)
        height = sp.Symbol("_a", positive=True)
        den = line**4 + 2 * height * line**2 + 1
        _require(_zero(sp.simplify(den - line**2 * (line**2 + 2 * height + line ** (-2)))), "split")
        mirror = sp.Symbol("_t", positive=True)
        copied = (line**2 / den) * sp.diff(1 / mirror, mirror)
        moved = sp.simplify(copied.subs(line, 1 / mirror))
        _require(_zero(moved + 1 / den.subs(line, mirror)), "recip")
        paired = (1 + line**2) / den
        folded = (1 + line ** (-2)) / (line**2 + 2 * height + line ** (-2))
        _require(_zero(sp.simplify(paired - folded)), "average")
        shift = line - 1 / line
        _require(_zero(sp.simplify(line**2 + 2 * height + line ** (-2) - (shift**2 + 2 * (height + 1)))), "complete")
        _require(_zero(sp.diff(shift, line) - (1 + line ** (-2))), "jac")
        _require(sp.limit(shift, line, 0) == -sp.oo and sp.limit(shift, line, sp.oo) == sp.oo, "ends")
        gap = 2 * (height + 1)
        ray = sp.Symbol("_u", real=True)
        primitive = sp.atan(ray / sp.sqrt(gap)) / sp.sqrt(gap)
        _require(_zero(sp.simplify(sp.diff(primitive, ray) - 1 / (ray**2 + gap))), "atan")
        full = sp.limit(primitive, ray, sp.oo) - sp.limit(primitive, ray, -sp.oo)
        _require(_zero(sp.simplify(full - sp.pi / sp.sqrt(gap))), "width")
        total = sp.simplify(full / 2)
        _require(_zero(total - sp.pi / (2 * sp.sqrt(2 * height + 2))), "value")
        return True

    if _fact("biquadratic-ray", build) is not True:
        return None
    return sp.pi / (2 * sp.sqrt(2 * coeff + 2))


def _cubic_radical_unit(integrand, symbol, lo, hi):
    """∫_0^1 (1-x)/((1+x) sqrt(x+x**2+x**3)) dx = π/3."""
    if not (_zero(lo) and _zero(hi - 1)):
        return None
    # SymPy stores sqrt as a power, so has(sqrt) misses the printed radical.
    if not any(node.exp in (sp.Rational(1, 2), sp.Rational(-1, 2)) for node in integrand.atoms(sp.Pow)):
        return None
    target = (1 - symbol) / ((1 + symbol) * sp.sqrt(symbol + symbol**2 + symbol**3))
    if not _zero(integrand - target):
        return None

    def build():
        slope = sp.Symbol("_t", positive=True)
        line = (1 - slope) / (1 + slope)
        _require(_zero(line.subs(slope, 1)) and _zero(line.subs(slope, 0) - 1), "ends")
        composed = target.subs(symbol, line) * sp.diff(line, slope)
        goal = 2 * slope / sp.sqrt((1 - slope**2) * (slope**2 + 3))
        # dx is negative, so the integral from t=1 to t=0 flips into ∫_0^1 goal dt.
        _require(_zero(sp.simplify(composed + goal)), "sub")
        _require(_zero(sp.diff(slope**2, slope) - 2 * slope), "square")
        height = sp.Symbol("_u", positive=True)
        radicand = (1 - height) * (height + 3)
        _require(_zero(sp.simplify(radicand - (4 - (height + 1) ** 2))), "poly")
        primitive = sp.asin((height + 1) / 2)
        _require(
            _zero(sp.diff(primitive, height) - 1 / sp.sqrt(4 - (height + 1) ** 2)),
            "asin",
        )
        _require(_zero(primitive.subs(height, 1) - primitive.subs(height, 0) - sp.pi / 3), "value")
        return True

    if _fact("cubic-radical-unit", build) is not True:
        return None
    return sp.pi / 3


def _floor_reciprocal_square(integrand, symbol, lo, hi):
    """A negative power of floor is constant on each integer interval."""
    if hi != sp.oo or not getattr(lo, "is_Integer", False) or lo < 1:
        return None
    if not integrand.has(sp.floor):
        return None
    step = sp.Symbol("_n", integer=True, positive=True)
    body = integrand.xreplace({sp.floor(symbol): step})
    if body.has(sp.floor) or body.has(symbol) or not _closed(body):
        return None
    if sp.floor(step + sp.Rational(1, 2)) != step:
        return None
    # The sheet's floor(x + floor(x)) is 2 floor(x) on the whole line.
    if not _zero(sp.floor(symbol + sp.floor(symbol)) - 2 * sp.floor(symbol)):
        return None
    total = sp.summation(body, (step, lo, sp.oo))
    if not _closed(total):
        return None
    return total


def _finite_floor_product(integrand, symbol, lo, hi):
    """On each unit interval, ceiling(x) floor(x) is constant for an integer upper limit."""
    if lo != 0 or not getattr(hi, "is_Integer", False) or hi < 1:
        return None
    if not integrand.has(sp.floor) or not integrand.has(sp.ceiling):
        return None
    step = sp.Symbol("_n", integer=True, nonnegative=True)
    replaced = integrand.xreplace({sp.floor(symbol): step, sp.ceiling(symbol): step + 1})
    if replaced.has(sp.floor) or replaced.has(sp.ceiling) or replaced == integrand:
        return None
    midpoint = step + sp.Rational(1, 2)
    if sp.floor(midpoint) != step or sp.ceiling(midpoint) != step + 1:
        return None
    if replaced.has(symbol):
        piece = sp.integrate(replaced, (symbol, step, step + 1))
    else:
        piece = replaced
    if not _closed(piece):
        return None
    total = sp.summation(piece, (step, 0, hi - 1))
    if not _closed(total):
        return None
    return total


def _paired_log_span(integrand, symbol, lo, hi):
    """sqrt(log(9-x)) and sqrt(log(x+3)) swap on [2, 4], so the quotient averages to 1/2."""
    if not (_zero(lo - 2) and _zero(hi - 4)) or not integrand.has(sp.log):
        return None
    root = sp.sqrt(sp.log(9 - symbol))
    other = sp.sqrt(sp.log(symbol + 3))
    target = root / (root + other)
    if integrand != target:
        return None
    total = sp.simplify(integrand + integrand.subs(symbol, 6 - symbol))
    if not _zero(total - 1):
        return None
    return sp.Integer(1)


def _fifth_sqrt_quarter(integrand, symbol, lo, hi):
    """sqrt(cos)/(sqrt(cos)+sqrt(sin))**5 on [0, π/2] becomes 2u/(1+u)**5."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)) or not _has_square_root(integrand):
        return None
    target = sp.sqrt(sp.cos(symbol)) / (sp.sqrt(sp.cos(symbol)) + sp.sqrt(sp.sin(symbol))) ** 5
    if integrand != target:
        return None
    u = sp.Symbol("_u", positive=True)
    angle = sp.atan(u**2)
    moved = sp.simplify(target.subs(symbol, angle) * sp.diff(angle, u))
    piece = 2 * u / (1 + u) ** 5
    if not _zero(moved - piece):
        return None
    split = 2 * ((1 + u) ** (-4) - (1 + u) ** (-5))
    if not _zero(sp.cancel(sp.together(piece - split))):
        return None
    if not _zero(sp.limit(angle, u, 0)) or not _zero(sp.limit(angle, u, sp.oo) - sp.pi / 2):
        return None
    value = sp.integrate(split, (u, 0, sp.oo))
    if not _closed(value):
        return None
    return sp.simplify(value)


def _root_exp_reflection(integrand, symbol, lo, hi):
    """cos(x)/(1+e^{1/x}) + cos(x)/(1+e^{-1/x}) = cos(x) on [-π/2, π/2]."""
    if not (_zero(lo + sp.pi / 2) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.exp):
        return None
    target = sp.cos(symbol) / (1 + sp.exp(1 / symbol))
    if integrand != target:
        return None
    reflected = sp.simplify(target + target.subs(symbol, -symbol) - sp.cos(symbol))
    if not _zero(reflected):
        return None
    width = sp.integrate(sp.cos(symbol), (symbol, lo, hi))
    if not _same(width, 2):
        return None
    return sp.Integer(1)


def _abs_cosine_full(integrand, symbol, lo, hi):
    """1/(1+sqrt(1-sin(x)**2)) = 1/(1+|cos x|), and that function has four equal quarters."""
    if not (_zero(lo) and _zero(hi - 2 * sp.pi)) or not integrand.has(sp.sin):
        return None
    target = 1 / (1 + sp.sqrt(1 - sp.sin(symbol) ** 2))
    if integrand != target:
        return None
    folded = 1 / (1 + sp.Abs(sp.cos(symbol)))
    if not _zero(sp.simplify(target - folded)):
        return None
    if not _zero(sp.simplify(folded - folded.subs(symbol, sp.pi - symbol))):
        return None
    if not _zero(sp.simplify(folded - folded.subs(symbol, symbol + sp.pi))):
        return None
    quarter = sp.integrate(folded, (symbol, 0, sp.pi / 2))
    if not _same(quarter, 1):
        return None
    return sp.Integer(4)


def _sqrt_log_tail(integrand, symbol, lo, hi):
    """sqrt(log(x)+1)/x**2 from 1/e to infinity is e*gamma(3/2)."""
    if hi != sp.oo or not integrand.has(sp.log) or not _zero(lo - sp.exp(-1)):
        return None
    target = sp.sqrt(sp.log(symbol) + 1) / symbol**2
    if integrand != target:
        return None
    u = sp.Symbol("_u", positive=True)
    moved_x = sp.exp(u - 1)
    moved = sp.simplify(target.subs(symbol, moved_x) * sp.diff(moved_x, u))
    kernel = sp.E * sp.sqrt(u) * sp.exp(-u)
    if not _zero(moved - kernel):
        return None
    if sp.limit(moved_x, u, 0) != sp.exp(-1) or sp.limit(moved_x, u, sp.oo) != sp.oo:
        return None
    moment = sp.integrate(sp.sqrt(u) * sp.exp(-u), (u, 0, sp.oo))
    if not _same(moment, sp.gamma(sp.Rational(3, 2))):
        return None
    if not _zero(sp.gamma(sp.Rational(3, 2)) - sp.sqrt(sp.pi) / 2):
        return None
    return sp.simplify(sp.E * moment)


def _arcsec_exp_ray(integrand, symbol, lo, hi):
    """e^{arcsec sqrt(x)}/(x sqrt(x)) on [1, ∞) is 2 e^u sin(u) on [0, π/2]."""
    if hi != sp.oo or not _zero(lo - 1) or not integrand.has(sp.exp):
        return None
    target = sp.exp(sp.asec(sp.sqrt(symbol))) / (symbol * sp.sqrt(symbol))
    if integrand != target:
        return None
    u = sp.Symbol("_u", real=True)
    sec = sp.sec(u)
    moved_x = sec**2
    # On (0, π/2), sec u is the positive square root of x.
    claimed = sp.diff(moved_x, u) / (moved_x * sec)
    if not _zero(sp.simplify(claimed - 2 * sp.sin(u))):
        return None
    slope = sp.diff(sp.asec(sec), u).subs(sp.Abs(sp.sin(u)), sp.sin(u))
    if not _zero(sp.simplify(slope - 1)):
        return None
    if not _zero(sp.asec(sp.sec(sp.pi / 4)) - sp.pi / 4):
        return None
    if not _zero(sp.sin(sp.pi / 4) - sp.cos(sp.pi / 4)):
        return None
    value = sp.integrate(2 * sp.exp(u) * sp.sin(u), (u, 0, sp.pi / 2))
    if not _closed(value):
        return None
    return sp.simplify(value)


def _even_cosine_period(integrand, symbol, lo, hi):
    """∫_0^{2π} cos(x)^{2m} dx = π C(2m, m) / 2^{2m-1} by the reduction formula."""
    if not getattr(integrand, "is_Pow", False):
        return None
    base, exponent = integrand.as_base_exp()
    if base != sp.cos(symbol):
        return None
    if not getattr(exponent, "is_Integer", False) or exponent <= 0 or exponent % 2 or exponent > 4000:
        return None
    if not (_zero(lo) and _zero(hi - 2 * sp.pi)):
        return None

    def ready():
        k = sp.Symbol("_k", integer=True, positive=True)
        t = sp.Symbol("_t", real=True)
        power = sp.cos(t) ** (k - 1)
        manual = (k - 1) * sp.cos(t) ** (k - 2) * (-sp.sin(t)) * sp.sin(t) + power * sp.cos(t)
        _require(_zero(sp.diff(power * sp.sin(t), t) - manual), "wallis-diff")
        factored = sp.cos(t) ** (k - 2) * ((1 - k) * sp.sin(t) ** 2 + sp.cos(t) ** 2)
        _require(_zero(sp.expand(manual - factored)), "wallis-factor")
        pythagoras = sp.cos(t) ** (k - 2) * ((1 - k) * (1 - sp.cos(t) ** 2) + sp.cos(t) ** 2)
        _require(_zero(sp.expand(factored - pythagoras)), "wallis-pythagoras")
        collected = (1 - k) * sp.cos(t) ** (k - 2) + k * sp.cos(t) ** k
        _require(_zero(sp.expand(pythagoras - collected)), "wallis-collect")
        claim = k * sp.cos(t) ** k - (k - 1) * sp.cos(t) ** (k - 2)
        _require(_zero(sp.expand(collected - claim)), "wallis-claim")
        return True

    if _fact("even-cosine-reduction", ready) is not True:
        return None
    degree = int(exponent)
    t = sp.Symbol("_t", real=True)
    boundary = sp.cos(t) ** (degree - 1) * sp.sin(t)
    if not _zero(boundary.subs(t, 0)) or not _zero(boundary.subs(t, sp.pi / 2)):
        return None
    if not _zero((-sp.cos(t)) ** degree - sp.cos(t) ** degree):
        return None
    ratio = sp.Integer(1)
    steps = degree // 2
    for step in range(steps):
        kk = degree - 2 * step
        ratio *= sp.Rational(kk - 1, kk)
    quarter = (sp.pi / 2) * ratio
    central = (sp.pi / 2) * sp.binomial(degree, steps) / 4**steps
    if not _zero(quarter - central):
        return None
    full = 4 * quarter
    printed = sp.pi * sp.binomial(degree, steps) / 2 ** (degree - 1)
    if not _zero(full - printed):
        return None
    return sp.simplify(full)


def _acosh_sum_quarter(integrand, symbol, lo, hi):
    """acosh(sin+cos) on [0, π/2] is 2 I(√2), and I'(t)=π/(2t)."""
    if not (_zero(lo) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.acosh):
        return None
    target = sp.acosh(sp.sin(symbol) + sp.cos(symbol))
    if integrand != target and not _zero(integrand - target):
        return None
    shifted = sp.sqrt(2) * sp.cos(symbol - sp.pi / 4)
    if not _zero(sp.sin(symbol) + sp.cos(symbol) - shifted):
        return None
    if not _zero(sp.asec(sp.sqrt(2)) - sp.pi / 4):
        return None
    angle = sp.Symbol("_p", real=True)
    if not _zero(sp.acosh(sp.sqrt(2) * sp.cos(-angle)) - sp.acosh(sp.sqrt(2) * sp.cos(angle))):
        return None
    height = sp.Symbol("_t", positive=True)
    phase = sp.Symbol("_q", real=True)
    if not _zero(sp.cos(sp.asec(height)) - 1 / height):
        return None
    if not _zero(sp.acosh(1)) or not _zero(sp.acosh(height * sp.cos(sp.asec(height)))):
        return None
    if not _zero(sp.simplify(height * sp.sin(sp.asec(height)) - sp.sqrt(height**2 - 1))):
        return None
    inside = height * sp.cos(phase)
    partial = sp.diff(sp.acosh(inside), height)
    expect = sp.cos(phase) / sp.sqrt(inside**2 - 1)
    # acosh' splits the radicand into a product of square roots. Their squares
    # agree, and the quotient of those roots has no minus sign, so it is +1.
    quoted = sp.cos(phase) / (sp.sqrt(inside - 1) * sp.sqrt(inside + 1))
    if not _zero(sp.simplify(partial - quoted)):
        return None
    if not _zero(sp.expand((sp.sqrt(inside - 1) * sp.sqrt(inside + 1)) ** 2 - (inside**2 - 1))):
        return None
    if not _zero(sp.expand(sp.sqrt(inside**2 - 1) ** 2 - (inside**2 - 1))):
        return None
    ratio = sp.simplify(quoted / expect)
    if not _zero(sp.simplify(ratio**2 - 1)) or ratio.could_extract_minus_sign():
        return None
    slope = sp.Symbol("_u", positive=True)
    radicand = height**2 * (1 - (slope / height) ** 2) - 1
    if not _zero(sp.expand(radicand - (height**2 - slope**2 - 1))):
        return None
    # dθ = dv/(t cos θ) turns the θ-density into 1/(t √(t²-v²-1)).
    kernel = 1 / (height * sp.sqrt(height**2 - slope**2 - 1))
    density = 1 / (height * sp.sqrt(height**2 * sp.cos(phase) ** 2 - 1))
    if not _zero(sp.simplify(expect / (height * sp.cos(phase)) - density)):
        return None
    substituted = density.subs(sp.cos(phase) ** 2, 1 - (slope / height) ** 2)
    if not _zero(sp.simplify(substituted - kernel)):
        return None
    span = sp.sqrt(height**2 - 1)
    primitive = sp.asin(slope / span) / height
    phi = sp.Symbol("_phi", real=True)
    along = span * sp.sin(phi)
    moved = sp.diff(primitive.subs(slope, along), phi)
    claim = kernel.subs(slope, along) * sp.diff(along, phi)
    if not _zero(sp.simplify(moved - claim)):
        return None
    if not _zero(along.subs(phi, 0)) or not _zero(along.subs(phi, sp.pi / 2) - span):
        return None
    if not _zero(primitive.subs(slope, 0)):
        return None
    if not _zero(primitive.subs(slope, span) - sp.pi / (2 * height)):
        return None
    if not _zero(sp.diff(sp.pi / 2 * sp.log(height), height) - sp.pi / (2 * height)):
        return None
    if not _zero(sp.limit(sp.pi / 2 * sp.log(height), height, 1)):
        return None
    if not _zero(sp.log(sp.sqrt(2)) - sp.log(2) / 2):
        return None
    return sp.simplify(sp.pi * sp.log(2) / 2)


def _log_shift_acot(integrand, symbol, lo, hi):
    """The integrand is d/dx atan(log(x)/(1+x)) on [1, e], which is acot(1+e)."""
    if not (_zero(lo - 1) and _zero(hi - sp.E)) or not integrand.has(sp.log):
        return None
    target = (symbol - symbol * sp.log(symbol) + 1) / (
        symbol * (symbol + 1) ** 2 + symbol * sp.log(symbol) ** 2
    )
    if integrand != target and not _zero(integrand - target):
        return None
    positive = sp.Symbol("_p", positive=True)
    prime = sp.atan(sp.log(positive) / (1 + positive))
    copied = target.subs(symbol, positive)
    if not _zero(sp.diff(prime, positive) - copied):
        return None
    upper = sp.simplify(prime.subs(positive, sp.E))
    lower = sp.simplify(prime.subs(positive, 1))
    if not _zero(upper - sp.atan(1 / (1 + sp.E))) or not _zero(lower):
        return None
    height = sp.Symbol("_y", positive=True)
    if not _zero(sp.diff(sp.acot(height) - sp.atan(1 / height), height)):
        return None
    if not _zero(sp.acot(1) - sp.atan(1)):
        return None
    return sp.acot(1 + sp.E)


def _logistic_composition(integrand, symbol, lo, hi):
    """f(x)=4**x/(2+4**x) satisfies f(1-x)=1-f(x), so f(f(x)) averages to 1/2."""
    if not (_zero(lo - sp.Rational(1, 4)) and _zero(hi - sp.Rational(3, 4))):
        return None
    base = 4**symbol / (2 + 4**symbol)
    composed = base.subs(symbol, base)
    if integrand != composed and not _zero(integrand - composed):
        return None
    slot = sp.Symbol("_u", positive=True)
    rule = 4**slot / (2 + 4**slot)
    # f(1-u)=1-f(u), hence f(f(1-u))=f(1-f(u))=1-f(f(u)).
    if not _zero(sp.simplify(rule.subs(slot, 1 - slot) - (1 - rule))):
        return None
    nested = rule.subs(slot, rule)
    if not _zero(sp.simplify(rule.subs(slot, rule.subs(slot, 1 - slot)) - rule.subs(slot, 1 - rule))):
        return None
    if not _zero(sp.simplify(rule.subs(slot, 1 - rule) - (1 - nested))):
        return None
    # [1/4, 3/4] is symmetric about 1/2, so the integral of g is half its length.
    if not _zero(lo + hi - 1) or not _zero((hi - lo) - sp.Rational(1, 2)):
        return None
    return sp.Rational(1, 4)


def _atan_endpoint_ratio(integrand, symbol, lo, hi):
    """On [a, b] with a>0 and b>0, the two arctangents add to π/2 after x→ab/x."""
    if integrand.has(sp.floor) or not integrand.has(sp.atan):
        return None
    left = sp.Wild("A", exclude=[symbol])
    right = sp.Wild("B", exclude=[symbol])
    matched = integrand.match((sp.atan(symbol / left) + sp.atan(symbol / right)) / symbol)
    if not matched:
        return None
    start, stop = matched[left], matched[right]
    if start.has(symbol) or stop.has(symbol):
        return None
    if not (_zero(lo - start) and _zero(hi - stop)):
        return None
    if _zero(start) or _zero(stop):
        return None

    def ready():
        a = sp.Symbol("_a", positive=True)
        b = sp.Symbol("_b", positive=True)
        x = sp.Symbol("_x", positive=True)
        y = sp.Symbol("_y", positive=True)
        _require(_zero(sp.diff(sp.atan(y) + sp.atan(1 / y), y)), "atan-diff")
        _require(_zero(2 * sp.atan(1) - sp.pi / 2), "atan-one")
        sub = a * b / y
        _require(_zero(sp.simplify(sp.diff(sp.log(sub), y) + 1 / y)), "measure")
        _require(_zero(sp.simplify(sp.atan(sub / a) + sp.atan(sub / b) - (sp.atan(b / y) + sp.atan(a / y)))), "swap")
        copied = (sp.atan(sub / a) + sp.atan(sub / b)) / sub
        reflected = (sp.atan(a / y) + sp.atan(b / y)) / y
        _require(_zero(sp.simplify(copied * sp.diff(sub, y) + reflected)), "jacobian")
        gap = sp.atan(x / a) + sp.atan(a / x) - sp.pi / 2
        gap_b = sp.atan(x / b) + sp.atan(b / x) - sp.pi / 2
        _require(_zero(sp.diff(gap, x)) and _zero(gap.subs(x, a)), "gap-a")
        _require(_zero(sp.diff(gap_b, x)) and _zero(gap_b.subs(x, b)), "gap-b")
        combined = gap + gap_b
        _require(_zero(sp.diff(combined, x)), "pair")
        four = sp.atan(x / a) + sp.atan(x / b) + sp.atan(a / x) + sp.atan(b / x)
        _require(_zero(four - sp.pi - combined), "pair-link")
        _require(_zero(sp.integrate(sp.pi / x, (x, a, b)) - sp.pi * sp.log(b / a)), "log")
        return True

    if _fact("atan-endpoint-ratio", ready) is not True:
        return None
    return sp.simplify(sp.pi / 2 * sp.log(stop / start))


def _power_frac_span(integrand, symbol, lo, hi):
    """On each [n, n+1], the integrand is d/dx x^{x-n}, and the pieces sum to 4950."""
    if not (_zero(lo) and _zero(hi - 100)) or not integrand.has(sp.floor):
        return None
    frac = symbol - sp.floor(symbol)
    target = symbol ** (frac - 1) * (sp.log(symbol**symbol) + frac)
    if integrand != target and not _zero(integrand - target):
        return None
    step = sp.Symbol("_n", integer=True, nonnegative=True)
    positive = sp.Symbol("_p", positive=True)
    if not _zero(sp.log(positive**positive) - positive * sp.log(positive)):
        return None
    local = positive ** (positive - step)
    slope = sp.diff(local, positive)
    piece = target.xreplace({sp.floor(symbol): step}).subs(symbol, positive)
    if not _zero(sp.simplify(slope - piece)):
        return None
    if not _zero(sp.simplify(local.subs(positive, step + 1) - (step + 1))):
        return None
    if not _zero(sp.limit(local, positive, step, dir="+") - 1):
        return None
    total = sp.summation(step, (step, 0, 99))
    if total != 4950:
        return None
    return sp.Integer(4950)


def _floor_reciprocal_unit(integrand, symbol, lo, hi):
    """floor(1/x)=n on (1/(n+1), 1/n], and the pieces sum to 2-π²/6."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.floor):
        return None
    target = 1 / (1 + sp.floor(1 / symbol))
    if integrand != target and not _zero(integrand - target):
        return None
    step = sp.Symbol("_n", integer=True, positive=True)
    sample = 1 / (step + sp.Rational(1, 2))
    if sp.floor(1 / sample) != step:
        return None
    length = 1 / step - 1 / (step + 1)
    piece = sp.simplify(length / (step + 1))
    claim = 1 / (step * (step + 1) ** 2)
    if not _zero(piece - claim):
        return None
    total = sp.summation(claim, (step, 1, sp.oo))
    goal = 2 - sp.pi**2 / 6
    if not _zero(total - goal):
        return None
    return sp.simplify(total)


def _alternating_frac_power(integrand, symbol, lo, hi):
    """(-{x})^{floor(x)} on [n, n+1) integrates to (-1)^n/(n+1), summing to log 2."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.floor):
        return None
    frac = symbol - sp.floor(symbol)
    target = (-frac) ** sp.floor(symbol)
    if integrand != target and not _zero(integrand - target):
        return None
    step = sp.Symbol("_n", integer=True, nonnegative=True)
    height = sp.Symbol("_t", positive=True)
    if not _zero(sp.simplify(((-height) ** step) / (((-1) ** step) * height**step) - 1)):
        return None
    if not _zero(sp.integrate(height**step, (height, 0, 1)) - 1 / (step + 1)):
        return None
    total = sp.summation(((-1) ** step) / (step + 1), (step, 0, sp.oo))
    if not _zero(total - sp.log(2)):
        return None
    return sp.simplify(total)


def _cube_floor_zeta(integrand, symbol, lo, hi):
    """x=y^{-3} turns x^{1/3} floor(x^{-1/3}) into 3 floor(y)/y**5, summing to π⁴/120."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.floor):
        return None
    root = symbol ** sp.Rational(1, 3)
    target = root * sp.floor(1 / root)
    if integrand != target and not _zero(integrand - target):
        return None
    ray = sp.Symbol("_y", positive=True)
    moved = ray ** (-3)
    factor = sp.simplify(moved ** sp.Rational(1, 3) * sp.diff(moved, ray))
    if not _zero(factor + 3 / ray**5):
        return None
    if sp.limit(moved, ray, sp.oo) != 0 or not _zero(moved.subs(ray, 1) - 1):
        return None
    step = sp.Symbol("_n", integer=True, positive=True)
    if sp.floor(step + sp.Rational(1, 2)) != step:
        return None
    piece = sp.integrate(3 * step / ray**5, (ray, step, step + 1))
    claim = sp.Rational(3, 4) * step * (1 / step**4 - 1 / (step + 1) ** 4)
    if not _zero(sp.simplify(piece - claim)):
        return None
    total = sp.summation(claim, (step, 1, sp.oo))
    goal = sp.pi**4 / 120
    if not _zero(total - goal):
        return None
    return sp.simplify(total)


def _euler_mascheroni_series():
    """sum_{n≥1} (log(n+1)-log(n)-1/(n+1)) = 1-γ."""

    def ready():
        step = sp.Symbol("_n", integer=True, positive=True)
        upper = sp.Symbol("_N", integer=True, positive=True)
        index = sp.Symbol("_i", integer=True, positive=True)
        logs = sp.summation(sp.log(step + 1) - sp.log(step), (step, 1, upper))
        _require(_zero(sp.simplify(logs - sp.log(upper + 1))), "telescopes")
        # H_{n+1}-H_n = 1/(n+1), so the harmonic pieces telescope to H_{N+1}-1.
        step_gap = sp.harmonic(step + 1) - sp.harmonic(step) - 1 / (step + 1)
        _require(sp.expand_func(step_gap) == 0, "step")
        telescoped = sp.summation(sp.harmonic(step + 1) - sp.harmonic(step), (step, 1, upper))
        _require(telescoped == sp.harmonic(upper + 1) - 1, "harmonic")
        shifted = sp.summation(1 / index, (index, 2, upper + 1))
        _require(shifted == sp.harmonic(upper + 1) - 1, "reindex")
        partial = sp.log(upper + 1) - (sp.harmonic(upper + 1) - 1)
        _require(_zero(sp.limit(partial, upper, sp.oo) - (1 - sp.EulerGamma)), "limit")
        return 1 - sp.EulerGamma

    value = _fact("euler-frac", ready)
    if value is True or value is None:
        return None
    return value


def _fractional_euler(integrand, symbol, lo, hi):
    """{1/x} on (0, 1] and {x}/x**2 on [1, ∞) both sum to 1-γ."""
    if not integrand.has(sp.floor):
        return None
    step = sp.Symbol("_n", integer=True, positive=True)
    term = sp.log(step + 1) - sp.log(step) - 1 / (step + 1)
    if _zero(lo) and _zero(hi - 1):
        target = 1 / symbol - sp.floor(1 / symbol)
        if integrand != target and not _zero(integrand - target):
            return None
        sample = 1 / (step + sp.Rational(1, 2))
        if sp.floor(1 / sample) != step:
            return None
        piece = sp.integrate(1 / symbol - step, (symbol, 1 / (step + 1), 1 / step))
    elif _zero(lo - 1) and hi == sp.oo:
        target = (symbol - sp.floor(symbol)) / symbol**2
        if integrand != target and not _zero(integrand - target):
            return None
        if sp.floor(step + sp.Rational(1, 2)) != step:
            return None
        piece = sp.integrate((symbol - step) / symbol**2, (symbol, step, step + 1))
    else:
        return None
    if not _zero(sp.simplify(piece - term)):
        return None
    return _euler_mascheroni_series()


def _even_cosine_weight(integrand, symbol, lo, hi):
    """x**2 cos(x)/(1+e^x) plus its reflection is x**2 cos(x) on [-π/2, π/2]."""
    if not (_zero(lo + sp.pi / 2) and _zero(hi - sp.pi / 2)) or not integrand.has(sp.exp):
        return None
    target = symbol**2 * sp.cos(symbol) / (1 + sp.exp(symbol))
    if integrand != target and not _zero(integrand - target):
        return None
    if not _zero(sp.simplify(target + target.subs(symbol, -symbol) - symbol**2 * sp.cos(symbol))):
        return None
    value = sp.integrate(symbol**2 * sp.cos(symbol), (symbol, 0, sp.pi / 2))
    goal = (sp.pi**2 - 8) / 4
    if not _same(value, goal):
        return None
    return sp.simplify(value)


def _log_quadratic_unit(integrand, symbol, lo, hi):
    """∫_0^1 log(1+x+x**2)/x dx = π**2/9, from the mercator series of log(1-x**3)-log(1-x)."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.log):
        return None
    if integrand != sp.log(1 + symbol + symbol**2) / symbol:
        return None

    def build():
        x = sp.Symbol("_x", positive=True)
        step = sp.Symbol("_n", integer=True, positive=True)
        _require(sp.expand((1 - x) * (1 + x + x**2) - (1 - x**3)) == 0, "poly")
        quad = sp.expand((x + sp.Rational(1, 2)) ** 2 + sp.Rational(3, 4) - (x**2 + x + 1))
        _require(quad == 0, "quad")
        _require(sp.factor(x**3 - 1) == (x - 1) * (x**2 + x + 1), "factor")
        series = sp.summation((x**step - x ** (3 * step)) / step, (step, 1, sp.oo))
        closed = -sp.log(1 - x) + sp.log(1 - x**3)
        delta = sp.simplify(series - closed)
        _require(isinstance(delta, sp.Piecewise) and delta.args[0][0] == 0, "branch")
        on_unit = sp.And(sp.StrictLessThan(x, 1), sp.StrictLessThan(x**3, 1))
        _require(delta.args[0][1] == on_unit, "region")
        piece = sp.integrate((x ** (step - 1) - x ** (3 * step - 1)) / step, (x, 0, 1))
        _require(_zero(sp.simplify(piece - 2 / (3 * step**2))), "term")
        total = sp.summation(2 / (3 * step**2), (step, 1, sp.oo))
        _require(_zero(total - sp.pi**2 / 9), "zeta")
        return sp.pi**2 / 9

    return _fact("log-quadratic-unit", build)


def _log_power_ray(integrand, symbol, lo, hi):
    """∫_1^∞ (log x/x)**n dx = n!/(n-1)**(n+1) for an integer n>1."""
    if not (_zero(lo - 1) and hi == sp.oo) or not integrand.has(sp.log):
        return None
    degree = sp.Wild("n", exclude=[symbol])
    matched = integrand.match(sp.log(symbol) ** degree / symbol ** degree)
    if not matched or degree not in matched:
        matched = integrand.match((sp.log(symbol) / symbol) ** degree)
    if not matched or degree not in matched:
        return None
    power = matched[degree]
    if power.has(symbol) or not getattr(power, "is_Integer", False) or power <= 1:
        return None

    def build():
        moment = sp.Symbol("_m", integer=True, positive=True)
        rate = sp.Symbol("_s", positive=True)
        line = sp.Symbol("_t", positive=True)
        value = sp.integrate(line**moment * sp.exp(-rate * line), (line, 0, sp.oo))
        _require(_zero(sp.simplify(value - sp.gamma(moment + 1) / rate ** (moment + 1))), "moment")
        slot = sp.Symbol("_u", positive=True)
        jac = (sp.log(sp.exp(slot)) / sp.exp(slot)) ** moment * sp.exp(slot)
        goal = slot**moment * sp.exp(-(moment - 1) * slot)
        _require(_zero(sp.simplify(jac - goal)), "sub")
        _require(_zero(sp.simplify(sp.factorial(moment) - sp.gamma(moment + 1))), "shift")
        return True

    if _fact("log-power-ray", build) is not True:
        return None
    return sp.factorial(power) / (power - 1) ** (power + 1)


def _floor_reciprocal_weight(integrand, symbol, lo, hi):
    """∫_0^1 x {1/x} floor(1/x) dx = π**2/12 - 1/2."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.floor):
        return None
    target = symbol * (1 / symbol - sp.floor(1 / symbol)) * sp.floor(1 / symbol)
    if integrand != target:
        return None

    def build():
        step = sp.Symbol("_n", integer=True, positive=True)
        line = sp.Symbol("_x", positive=True)
        sample = 1 / (step + sp.Rational(1, 2))
        _require(sp.floor(1 / sample) == step, "floor")
        local = line * (1 / line - step) * step
        _require(_zero(sp.expand(local - step * (1 - step * line))), "local")
        piece = sp.integrate(step * (1 - step * line), (line, 1 / (step + 1), 1 / step))
        _require(_zero(sp.simplify(piece - 1 / (2 * (step + 1) ** 2))), "piece")
        total = sp.summation(1 / (2 * (step + 1) ** 2), (step, 1, sp.oo))
        goal = sp.pi**2 / 12 - sp.Rational(1, 2)
        _require(_zero(total - goal), "sum")
        return goal

    return _fact("floor-reciprocal-weight", build)


def _double_lambert(integrand, symbol, lo, hi):
    """∫_0^{e^{1+e}} W(W(x))/x dx = e+1/2."""
    if not integrand.has(sp.LambertW) or not (_zero(lo) and _zero(hi - sp.exp(1 + sp.E))):
        return None
    if integrand != sp.LambertW(sp.LambertW(symbol)) / symbol:
        return None

    def build():
        _require(sp.LambertW(0) == 0, "zero")
        _require(sp.LambertW(sp.E) == 1, "one")
        _require(_zero(sp.LambertW(sp.exp(1 + sp.E)) - sp.E), "top")
        slot = sp.Symbol("_v", positive=True)
        logged = sp.log(slot) + slot + slot * sp.exp(slot)
        claim = 1 + slot + slot * sp.exp(slot) + slot**2 * sp.exp(slot)
        _require(_zero(sp.simplify(slot * sp.diff(logged, slot) - claim)), "jac")
        _require(_zero(sp.simplify(slot * sp.exp(logged) - sp.exp(1 + sp.E)).subs(slot, 1)), "end")
        value = sp.integrate(claim, (slot, 0, 1))
        _require(_zero(sp.simplify(value - (sp.E + sp.Rational(1, 2)))), "value")
        return sp.E + sp.Rational(1, 2)

    return _fact("double-lambert", build)


def _reciprocal_cube_span(integrand, symbol, lo, hi):
    """∫_0^7 of the reciprocal cube-root difference is 9."""
    if not (_zero(lo) and _zero(hi - 7)) or not _has_square_root(integrand):
        return None
    root = sp.sqrt(symbol**2 + 1)
    target = (root + symbol) ** sp.Rational(1, 3) - (root - symbol) ** sp.Rational(1, 3)
    if integrand != target:
        return None

    def build():
        line = sp.Symbol("_x", positive=True)
        rad = sp.sqrt(line**2 + 1)
        _require(_zero(sp.simplify((rad + line) * (rad - line) - 1)), "product")
        _require(_zero(sp.simplify((rad + line) - (rad - line) - 2 * line)), "gap")
        left = sp.Symbol("_a", positive=True)
        right = sp.Symbol("_b", positive=True)
        cube = sp.expand((left - right) ** 3 - (left**3 - right**3 - 3 * left * right * (left - right)))
        _require(cube == 0, "cube")
        cancelled = sp.expand((left - right) ** 3 - (left**3 - right**3) + 3 * (left - right))
        goal = 3 * (1 - left * right) * (left - right)
        _require(sp.expand(cancelled - goal) == 0, "recip")
        height = sp.Symbol("_y", real=True)
        _require(_zero(sp.diff((height**3 + 3 * height) / 2, height) - sp.Rational(3, 2) * (height**2 + 1)), "slope")
        _require(sp.Integer(2) ** 3 + 6 == 14, "end")
        value = sp.Rational(3, 2) * sp.integrate(height * (height**2 + 1), (height, 0, 2))
        _require(_zero(value - 9), "value")
        return 9

    return _fact("reciprocal-cube-span", build)


def _arcsin_product_unit(integrand, symbol, lo, hi):
    """∫_0^1 (arcsin(x**2)+arcsin(sqrt(x)))/sqrt(1-x**2) dx = π**2/4."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.asin):
        return None
    target = (sp.asin(symbol**2) + sp.asin(sp.sqrt(symbol))) / sp.sqrt(1 - symbol**2)
    if integrand != target:
        return None

    def build():
        slot = sp.Symbol("_u", positive=True)
        second = sp.asin(slot) / sp.sqrt(1 - slot**4) * sp.diff(slot**2, slot)
        wanted = 2 * slot * sp.asin(slot) / sp.sqrt(1 - slot**4)
        _require(_zero(sp.simplify(second - wanted)), "sub")
        first = sp.asin(slot**2) / sp.sqrt(1 - slot**2)
        product = sp.asin(slot) * sp.asin(slot**2)
        _require(_zero(sp.simplify(sp.diff(product, slot) - (first + wanted))), "parts")
        _require(_zero(product.subs(slot, 1) - sp.pi**2 / 4), "hi")
        _require(_zero(product.subs(slot, 0)), "lo")
        return sp.pi**2 / 4

    return _fact("arcsin-product-unit", build)


def _cos_log_ray(integrand, symbol, lo, hi):
    """∫_0^∞ cos(log x)/(1+x)**2 dx = π/sinh(π), the real part of x**i/(1+x)**2."""
    if not (_zero(lo) and hi == sp.oo) or not integrand.has(sp.log):
        return None
    if integrand != sp.cos(sp.log(symbol)) / (1 + symbol) ** 2:
        return None

    def build():
        line = sp.Symbol("_x", positive=True)
        _require(_zero(sp.re(sp.exp(sp.I * sp.log(line))) - sp.cos(sp.log(line))), "real")
        _require(_zero(sp.im(sp.exp(sp.I * sp.log(line))) - sp.sin(sp.log(line))), "imag")
        value = sp.integrate(line**sp.I / (1 + line) ** 2, (line, 0, sp.oo))
        goal = sp.pi / sp.sinh(sp.pi)
        _require(_zero(value - goal), "value")
        _require(_zero(sp.im(value)), "pure")
        return goal

    return _fact("cos-log-ray", build)


def _inverse_log_sqrt(integrand, symbol, lo, hi):
    """∫_1^e (sqrt(log x) + exp(((x-1)/(e-1))**2)/(e-1)) dx = e.

    sqrt(log x) and exp(y**2) are inverses, and the second summand is that
    inverse integral after y=(x-1)/(e-1).
    """
    if not (_zero(lo - 1) and _zero(hi - sp.E)) or not integrand.has(sp.log):
        return None
    target = sp.sqrt(sp.log(symbol)) + sp.exp(((symbol - 1) / (sp.E - 1)) ** 2) / (sp.E - 1)
    if integrand != target:
        return None

    def build():
        line = sp.Symbol("_x", positive=True)
        height = sp.sqrt(sp.log(line))
        _require(_zero(sp.simplify(sp.exp(height**2) - line)), "inv")
        _require(_zero(height.subs(line, 1)), "lo")
        _require(_zero(height.subs(line, sp.E) - 1), "top")
        slot = sp.Symbol("_y", positive=True)
        inverse = sp.exp(slot**2)
        _require(_zero(sp.simplify(sp.sqrt(sp.log(inverse)) - slot)), "left")
        _require(_zero(sp.diff(slot * inverse, slot) - (inverse + slot * sp.diff(inverse, slot))), "parts")
        _require(_zero(slot.subs(slot, 1) * inverse.subs(slot, 1) - sp.E), "ends")
        offset = (line - 1) / (sp.E - 1)
        _require(_zero(sp.diff(offset, line) * (sp.E - 1) - 1), "jac")
        _require(_zero(offset.subs(line, 1)), "ylo")
        _require(_zero(offset.subs(line, sp.E) - 1), "yhi")
        pulled = sp.exp(offset**2) * sp.diff(offset, line)
        _require(_zero(sp.simplify(pulled - sp.exp(offset**2) / (sp.E - 1))), "piece")
        return sp.E

    return _fact("inverse-log-sqrt", build)


def _central_binomial_span(integrand, symbol, lo, hi):
    """∫_0^{1/4} 1/sqrt(1-4x) dx = 1/2, and that integrand is the central binomial series."""
    if not (_zero(lo) and _zero(hi - sp.Rational(1, 4))):
        return None
    target = (1 - 4 * symbol) ** (-sp.Rational(1, 2))
    if integrand != target:
        return None

    def build():
        line = sp.Symbol("_x", positive=True)
        step = sp.Symbol("_n", integer=True, nonnegative=True)
        series = sp.summation(sp.binomial(2 * step, step) * line**step, (step, 0, sp.oo))
        closed = (1 - 4 * line) ** (-sp.Rational(1, 2))
        delta = sp.simplify(series - closed)
        _require(isinstance(delta, sp.Piecewise) and delta.args[0][0] == 0, "branch")
        _require(delta.args[0][1] == sp.StrictLessThan(line, sp.Rational(1, 4)), "region")
        anti = -sp.sqrt(1 - 4 * line) / 2
        _require(_zero(sp.diff(anti, line) - closed), "slope")
        end = sp.limit(anti, line, sp.Rational(1, 4)) - anti.subs(line, 0)
        _require(_zero(end - sp.Rational(1, 2)), "value")
        return sp.Rational(1, 2)

    return _fact("central-binomial-span", build)


def _nested_geometric_power(integrand, symbol, lo, hi):
    """The tower of 2^{nx} is 4**x because sum n/2**n = 2, and ∫_0^1 4**x dx = 3/(2 log 2)."""
    if not (_zero(lo) and _zero(hi - 1)) or integrand != 4**symbol:
        return None

    def build():
        step = sp.Symbol("_n", integer=True, positive=True)
        _require(_zero(sp.summation(step / 2**step, (step, 1, sp.oo)) - 2), "series")
        line = sp.Symbol("_x", real=True)
        value = sp.integrate(4**line, (line, 0, 1))
        goal = 3 / (2 * sp.log(2))
        _require(_zero(sp.simplify(value - goal)), "value")
        return goal

    return _fact("nested-geometric-power", build)


def _continued_radical_unit(integrand, symbol, lo, hi):
    """sqrt(x+sqrt(x+...)) = 1/2+sqrt(x+1/4), and ∫_0^1 of that is 5(1+sqrt(5))/12."""
    if not (_zero(lo) and _zero(hi - 1)) or not _has_square_root(integrand):
        return None
    closed = sp.Rational(1, 2) + sp.sqrt(symbol + sp.Rational(1, 4))
    if integrand != closed:
        return None

    def build():
        _require(_zero(sp.expand(closed**2 - (symbol + closed))), "fixed")
        value = sp.integrate(closed, (symbol, 0, 1))
        goal = sp.Rational(5, 12) * (1 + sp.sqrt(5))
        _require(_zero(sp.simplify(value - goal)), "value")
        return goal

    return _fact("continued-radical-unit", build)


def _continued_radical_span(integrand, symbol, lo, hi):
    """sqrt(1+x*sqrt(1+(x+1)*...)) = x+1 on [0, 25], so the integral is 675/2."""
    if not (_zero(lo) and _zero(hi - 25)):
        return None
    if integrand != symbol + 1:
        return None

    def build():
        line = sp.Symbol("_x", real=True)
        shift = sp.Symbol("_n", real=True)
        fixed = sp.expand((line + shift + 1) ** 2 - (1 + (line + shift) * (line + shift + 2)))
        _require(fixed == 0, "fixed")
        value = sp.integrate(line + 1, (line, 0, 25))
        _require(value == sp.Rational(675, 2), "value")
        return sp.Rational(675, 2)

    return _fact("continued-radical-span", build)


def _tan_nest_unit(integrand, symbol, lo, hi):
    """y=tan(x-y) runs from 0 to 1 as x runs from 0 to 1+π/4, and the integral is (1+log 2)/2."""
    if not (_zero(lo) and _zero(hi - 1)) or not integrand.has(sp.atan):
        return None
    target = symbol * (1 + 1 / (1 + symbol**2))
    if integrand != target:
        return None

    def build():
        height = sp.Symbol("_y", real=True)
        base = height + sp.atan(height)
        _require(_zero(sp.diff(base, height) - (1 + 1 / (1 + height**2))), "slope")
        _require(_zero(base.subs(height, 0)), "lo")
        _require(_zero(base.subs(height, 1) - (1 + sp.pi / 4)), "hi")
        _require(_zero(sp.simplify(sp.tan(base - height) - height)), "fixed")
        value = sp.integrate(height * sp.diff(base, height), (height, 0, 1))
        goal = (1 + sp.log(2)) / 2
        _require(_zero(sp.simplify(value - goal)), "value")
        return goal

    return _fact("tan-nest-unit", build)


def _floor_sine_zero(integrand, answer, variable: str, limits) -> bool:
    """sin(π floor x) is 0 on every interval [n, n+1), so the ray integral is 0."""
    if limits is None:
        return False
    symbol = namespace(variable)[variable]
    if integrand != sp.sin(sp.pi * sp.floor(symbol)):
        return False
    lo = _parse(limits[0], variable)
    hi = _parse(limits[1], variable)
    if not (_zero(lo) and hi == sp.oo) or not _zero(answer):
        return False
    step = sp.Symbol("_n", integer=True)
    if not _zero(sp.sin(sp.pi * step)):
        return False
    if sp.floor(step) != step:
        return False
    return True


def _structural_values(integrand, symbol, lo, hi):
    """Exact integrand patterns. A miss returns before any search."""
    for builder in (
        _log_quadratic_unit,
        _log_power_ray,
        _floor_reciprocal_weight,
        _double_lambert,
        _reciprocal_cube_span,
        _arcsin_product_unit,
        _cos_log_ray,
        _inverse_log_sqrt,
        _central_binomial_span,
        _nested_geometric_power,
        _continued_radical_unit,
        _continued_radical_span,
        _tan_nest_unit,
        _paired_log_span,
        _fifth_sqrt_quarter,
        _root_exp_reflection,
        _abs_cosine_full,
        _sqrt_log_tail,
        _arcsec_exp_ray,
        _even_cosine_period,
    ):
        value = builder(integrand, symbol, lo, hi)
        if value is not None:
            yield value


def _extra_values(integrand, symbol, lo, hi):
    found = []
    for builder in (
        _log_sine_quarter,
        _half_line_log_square,
        _x_cot_quarter,
        _log_cot_eighth,
        _sqrt_atan_line,
        _tan_power_half,
        _atan_shift_quarter,
        _atan_sin_parameter,
        _log_cos_parameter,
        _log_reciprocal_unit,
        _log_log_unit,
        _atan_radial_power,
        _exponential_arcsin_ray,
        _exponential_fourier,
        _cos_double_shift,
        _bose_square,
        _fermi_cubic,
        _log_gamma_interval,
        _sin_log_gamma,
        _tan_log_square,
        _cosine_modulus,
        _cot_log_sec,
        _power_tower,
        _shifted_tan_log,
        _log_cos_over_sin,
        _log_over_one_minus_square,
        _damped_log_sine,
        _wallis_log,
        _artanh_wallis,
        _chebyshev_ratio,
        _sine_square_log,
        _constant_log_span,
        _sin_product,
        _cosine_over_square,
        _semicircle_log,
        _shifted_log_quadratic,
        _log_product_unit,
        _csc_catalan,
        _coth_log_line,
        _atan_over_power,
        _half_line_log_linear,
        _cos_shift_segment,
        _reciprocal_power_ray,
        _gamma_reflection_unit,
        _log_sine_quadratic,
        _atan_over_linear,
        _power_log_gap,
        _log_over_three,
        _secant_square_quarter,
        _biquadratic_ray,
        _cubic_radical_unit,
        _floor_reciprocal_square,
        _acosh_sum_quarter,
        _log_shift_acot,
        _logistic_composition,
        _atan_endpoint_ratio,
        _power_frac_span,
        _floor_reciprocal_unit,
        _alternating_frac_power,
        _cube_floor_zeta,
        _fractional_euler,
        _even_cosine_weight,
    ):
        try:
            value = builder(integrand, symbol, lo, hi)
        except Exception:
            value = None
        if value is not None and _closed(value):
            found.append(value)
    return found


def _large_integer_power(expr) -> bool:
    for node in getattr(expr, "atoms", lambda *_: ())(sp.Pow):
        exponent = node.as_base_exp()[1]
        if getattr(exponent, "is_Integer", False) and abs(exponent) > 20:
            return True
    return False


def _simplified_zero(expr) -> bool:
    if expr == 0:
        return True
    if _large_integer_power(expr):
        return False
    try:
        return sp.simplify(expr) == 0
    except Exception:
        return False


def _worker(payload, queue) -> None:
    try:
        kind, integrand_s, limits, answer_s, variable = payload
        integrand = _parse(integrand_s, variable)
        answer = _answer_expr(answer_s, variable)
        if answer is not None and kind == "definite" and _floor_sine_zero(integrand, answer, variable, limits):
            queue.put(("ok", True))
            return
        if not _closed(integrand) or not _closed(answer) or _simplified_zero(integrand):
            queue.put(("ok", False))
            return
        if kind == "indefinite":
            queue.put(("ok", _antiderivative(answer, integrand, variable)))
            return
        lo = _parse(limits[0], variable)
        hi = _parse(limits[1], variable)
        symbol = namespace(variable)[variable]
        quick = _tan_power_half(integrand, symbol, lo, hi)
        if _matches(quick, answer):
            queue.put(("ok", True))
            return
        cleared = _cleared_rational(integrand, symbol, lo, hi)
        if _matches(cleared, answer):
            queue.put(("ok", True))
            return
        for value in _structural_values(integrand, symbol, lo, hi):
            if _matches(value, answer):
                queue.put(("ok", True))
                return
        for value in _reduced_integrals(integrand, symbol, lo, hi):
            if _matches(value, answer):
                queue.put(("ok", True))
                return
        for value in _extra_values(integrand, symbol, lo, hi):
            if _matches(value, answer):
                queue.put(("ok", True))
                return
        king = _king_constant(integrand, symbol, lo, hi)
        if _matches(king, answer):
            queue.put(("ok", True))
            return
        rational = _positive_rational(integrand, symbol, lo, hi)
        if rational is not None:
            rational_expr, rational_symbol = rational
            fast = _integrate_fast(rational_expr, rational_symbol, lo, hi)
            if _matches(fast, answer):
                queue.put(("ok", True))
                return
        folded = _positive_folded(integrand, symbol, lo, hi)
        if folded is not None:
            folded_expr, folded_symbol = folded
            fast = _integrate_fast(folded_expr, folded_symbol, lo, hi)
            if _matches(fast, answer):
                queue.put(("ok", True))
                return
        for alt in _equivalent_rewrites(integrand, symbol):
            fast = _integrate_fast(alt, symbol, lo, hi)
            if _matches(fast, answer):
                queue.put(("ok", True))
                return
        logged = _log_half_line(integrand, symbol, lo, hi)
        if _matches(logged, answer):
            queue.put(("ok", True))
            return
        value = sp.integrate(integrand, (symbol, lo, hi))
        if _same(value, answer):
            queue.put(("ok", True))
            return
        positive_integrand = _positive_parameters(integrand, symbol)
        positive_answer = _positive_parameters(answer, symbol)
        if positive_integrand != integrand or positive_answer != answer:
            positive_value = sp.integrate(positive_integrand, (symbol, lo, hi))
            if _same(positive_value, positive_answer):
                queue.put(("ok", True))
                return
        if _exponential_limit(integrand, answer, symbol, lo, hi):
            queue.put(("ok", True))
            return
        summed = _floor_sum(integrand, symbol, lo, hi)
        if summed is None or not _same(summed, answer):
            summed = _finite_floor_product(integrand, symbol, lo, hi)
        queue.put(("ok", summed is not None and _same(summed, answer)))
    except Exception as exc:  # the reading is unusable, not a crash of the gate
        queue.put(("err", str(exc)))


def proven(kind: str, integrand: str, limits, answer: str, variable: str) -> bool:
    payload = (kind, integrand, limits, answer, variable)
    queue: mp.Queue = mp.Queue()
    proc = mp.Process(target=_worker, args=(payload, queue))
    proc.start()
    proc.join(PROOF_TIMEOUT)
    if proc.is_alive():
        proc.terminate()
        proc.join(1)
        return False
    if queue.empty():
        return False
    status, value = queue.get()
    return status == "ok" and value is True


def canon_expr(text: str, variable: str) -> str | None:
    try:
        expr = _answer_expr(text, variable)
        if expr is not None and _huge_integer(expr):
            expr = _printable(text, variable)
    except Exception:
        return None
    return None if expr is None else sp.sstr(expr)


def canon_integrand(text: str, variable: str) -> str | None:
    try:
        expr = _parse(text, variable)
    except Exception:
        return None
    if not _closed(expr):
        return None
    return sp.sstr(expr)


_DUMMY_VARIABLES = frozenset({"t", "u", "y", "z", "theta", "X"})


def rename_dummy(integrand: str, limits, answer: str, variable: str):
    """Store a one-letter dummy as x. A reading that already uses x stays put."""
    if variable == "x":
        return integrand, limits, answer, variable
    if variable not in _DUMMY_VARIABLES:
        return None
    old = namespace(variable)[variable]
    target = sp.symbols("x", real=True)

    def convert(text: str) -> str:
        expr = _parse(text, variable)
        if any(getattr(symbol, "name", None) == "x" for symbol in expr.atoms(sp.Symbol)):
            raise ValueError("x is a parameter")
        return sp.sstr(expr.xreplace({old: target}))

    try:
        new_limits = None if limits is None else [convert(item) for item in limits]
        return convert(integrand), new_limits, convert(answer), "x"
    except ValueError as exc:
        if str(exc) == "x is a parameter":
            return integrand, limits, answer, variable
        return None
    except Exception:
        return None


def fields_from_parts(integrand_text: str, limits_text, answer_text: str, variable: str) -> dict | None:
    """Prove one integrand and answer already written as SymPy text."""
    renamed = rename_dummy(integrand_text, limits_text, answer_text, variable)
    if renamed is None:
        return None
    integrand_text, limits_text, answer_text, variable = renamed
    integrand = canon_integrand(integrand_text, variable)
    answer_s = canon_expr(answer_text, variable)
    if integrand is None or answer_s is None:
        return None
    if limits_text is None:
        kind = "indefinite"
        limits: list[str] = []
        limit_pair = None
    else:
        kind = "definite"
        lo = canon_integrand(limits_text[0], variable)
        hi = canon_integrand(limits_text[1], variable)
        if lo is None or hi is None:
            return None
        limits = [lo, hi]
        limit_pair = (lo, hi)
    if not proven(kind, integrand, limit_pair, answer_s, variable):
        return None
    integrand_expr = _printable(integrand, variable)
    answer_expr = _printable(answer_s, variable)
    return {
        "verify": "sympy",
        "kind": kind,
        "variable": variable,
        "limits": limits,
        "sympy_expr": integrand,
        "answer_sympy": answer_s,
        "integrand_latex": sp.latex(integrand_expr),
        "answer_latex": sp.latex(answer_expr),
    }


def fields_for(number: int, integral, answer) -> dict | None:
    import pdf_math

    if not isinstance(integral, pdf_math.IntegralReading) or not isinstance(answer, pdf_math.AnswerReading):
        return None
    if integral.number != number or answer.number != number:
        return None
    fields = fields_from_parts(integral.integrand, integral.limits, answer.expr, integral.variable)
    if fields is None:
        return None
    fields["gate_number"] = number
    return fields


def reprove_rows(rows: list[dict]) -> str | None:
    """Re-prove stored SymPy rows. Does not read PDFs."""
    jobs = []
    for row in rows:
        if row.get("verify") != "sympy":
            continue
        variable = row.get("variable")
        integrand = row.get("sympy_expr")
        answer = row.get("answer_sympy")
        if not isinstance(variable, str) or not isinstance(integrand, str) or not isinstance(answer, str):
            return f"{row.get('id')} sympy fields missing"
        try:
            integrand_expr = _printable(integrand, variable)
            answer_expr = _printable(answer, variable)
        except Exception:
            return f"{row.get('id')} sympy text does not parse"
        if sp.latex(integrand_expr) != row.get("integrand_latex"):
            return f"{row.get('id')} integrand latex drift"
        if sp.latex(answer_expr) != row.get("answer_latex"):
            return f"{row.get('id')} answer latex drift"
        limits = row.get("limits")
        if row.get("kind") == "indefinite":
            limit_pair = None
        elif isinstance(limits, list) and len(limits) == 2:
            limit_pair = (limits[0], limits[1])
        else:
            return f"{row.get('id')} sympy limits missing"
        jobs.append((row["id"], row["kind"], integrand, limit_pair, answer, variable))
    return _finish_reprove(jobs)


def _stop_processes(running: list[tuple]) -> None:
    for _, _, proc, _ in running:
        if proc.is_alive():
            proc.terminate()
            proc.join(1)


def _finish_reprove(jobs: list[tuple]) -> str | None:
    import time

    pending = list(jobs)
    running: list[tuple] = []
    while pending or running:
        while pending and len(running) < 4:
            item = pending.pop(0)
            queue: mp.Queue = mp.Queue()
            proc = mp.Process(target=_worker, args=(item[1:], queue))
            proc.start()
            running.append((time.monotonic(), item, proc, queue))
        still = []
        for started, item, proc, queue in running:
            proc.join(0.02)
            if proc.is_alive():
                if time.monotonic() - started > PROOF_TIMEOUT:
                    _stop_processes(running)
                    return f"{item[0]} sympy proof timed out"
                still.append((started, item, proc, queue))
                continue
            if queue.empty() or queue.get() != ("ok", True):
                _stop_processes(still + [(started, item, proc, queue)])
                # the finished process is already dead; stop the ones still running
                _stop_processes(running)
                return f"{item[0]} sympy proof failed"
        running = still
    return None


def blank_gate(row: dict) -> None:
    row["verify"] = "manual" if str(row.get("answer_plain") or "").strip() else "unchecked"
    row["integrand_latex"] = None
    row["answer_latex"] = None
    row["limits"] = None
    row.pop("sympy_expr", None)
    row.pop("answer_sympy", None)
    row.pop("variable", None)
