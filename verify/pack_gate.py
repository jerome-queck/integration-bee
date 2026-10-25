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
already a parameter. Numeric agreement is not a proof.
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
    ns[variable] = sp.symbols(variable, real=True)
    ns["C"] = sp.Symbol("C")
    return ns


def _parse(text: str, variable: str):
    return sp.sympify(text, locals=namespace(variable))


def _answer_expr(text: str, variable: str):
    expr = _parse(text, variable)
    if isinstance(expr, sp.Equality):
        if sp.simplify(expr.lhs - expr.rhs) != 0:
            return None
        expr = expr.rhs
    expr = sp.expand(expr).subs(sp.Symbol("C"), 0)
    if expr.has(sp.Symbol("C")):
        return None
    return expr


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


def _antiderivative(answer, integrand, variable: str) -> bool:
    delta = sp.diff(answer, namespace(variable)[variable]) - integrand
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
