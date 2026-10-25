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
Further checked forms are a constant sum of reciprocal square roots of
logarithms on a finite interval, the beta evaluation of a power of tangent,
a cosine modulus through the half-angle
substitution, geometric series for x**n/(exp(x)±1), a shift of log gamma, a
sine weight on log gamma, a product of sines, cot(x) log(sec x), the
derivative of a polylog in x**x, log(1+tan x) on [0, π/4], odd-zeta series,
a damped (t-sin t)/t**2 integral, a sine-square substitution, the Wallis
product, an artanh series reduced to the Wallis integral, and a Chebyshev
reduction. A logarithm of an absolute value differentiates as the logarithm
of its argument. Numeric agreement is not a proof.
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


def _antiderivative(answer, integrand, variable: str) -> bool:
    symbol = namespace(variable)[variable]
    plain = _drop_log_abs(answer)
    if plain != answer and _zero(sp.diff(plain, symbol) - integrand):
        return True
    delta = sp.diff(answer, symbol) - integrand
    return _zero(delta)


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


_DUMMY_VARIABLES = frozenset({"t", "u", "y", "z", "theta"})


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
    except Exception:
        return None


def fields_for(number: int, integral, answer) -> dict | None:
    import pdf_math

    if not isinstance(integral, pdf_math.IntegralReading) or not isinstance(answer, pdf_math.AnswerReading):
        return None
    if integral.number != number or answer.number != number:
        return None
    renamed = rename_dummy(integral.integrand, integral.limits, answer.expr, integral.variable)
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
    ns = namespace(variable)
    integrand_expr = _parse(integrand, variable)
    answer_expr = _parse(answer_s, variable)
    return {
        "verify": "sympy",
        "kind": kind,
        "variable": variable,
        "limits": limits,
        "sympy_expr": integrand,
        "answer_sympy": answer_s,
        "integrand_latex": sp.latex(integrand_expr),
        "answer_latex": sp.latex(answer_expr),
        "gate_number": number,
    }


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
            integrand_expr = _parse(integrand, variable)
            answer_expr = _parse(answer, variable)
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
