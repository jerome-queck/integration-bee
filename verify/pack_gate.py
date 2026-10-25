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
Numeric agreement is not a proof.
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
    if expr is None or expr.has(sp.Integral) or expr.has(sp.Sum) or expr.has(sp.Product):
        return False
    return True


def _zero(expr) -> bool:
    candidates = [expr, check_math._without_abs_sign(expr)]
    expanded: list = []
    for item in candidates:
        expanded.append(item)
        try:
            expanded.append(sp.expand_log(item, force=True))
        except Exception:
            pass
        try:
            expanded.append(item.rewrite(sp.log))
        except Exception:
            pass
        try:
            expanded.append(sp.expand(item))
        except Exception:
            pass
        try:
            expanded.append(sp.trigsimp(item))
        except Exception:
            pass
    for item in expanded:
        try:
            if sp.simplify(item) == 0:
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
    if _zero(lo + hi):
        half = sp.simplify((integrand + integrand.subs(symbol, -symbol)) / 2)
        if _closed(half) and _simpler(half, integrand):
            found.append(sp.integrate(half, (symbol, lo, hi)))
    if _zero(lo) and _closed(hi) and not hi.has(sp.oo):
        reflected = sp.simplify(integrand.subs(symbol, hi - symbol))
        average = sp.simplify((integrand + reflected) / 2)
        if _closed(average) and _simpler(average, integrand):
            found.append(sp.integrate(average, (symbol, lo, hi)))
    if _zero(lo) and hi == sp.oo:
        flipped = integrand.subs(symbol, 1 / symbol) / symbol**2
        average = sp.simplify((integrand + flipped) / 2)
        if _closed(average) and _simpler(average, integrand):
            found.append(sp.integrate(average, (symbol, lo, hi)))
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


def _antiderivative(answer, integrand, variable: str) -> bool:
    delta = sp.diff(answer, namespace(variable)[variable]) - integrand
    return _zero(delta)


def _worker(payload, queue) -> None:
    try:
        kind, integrand_s, limits, answer_s, variable = payload
        integrand = _parse(integrand_s, variable)
        answer = _answer_expr(answer_s, variable)
        if not _closed(integrand) or not _closed(answer) or sp.simplify(integrand) == 0:
            queue.put(("ok", False))
            return
        if kind == "indefinite":
            queue.put(("ok", _antiderivative(answer, integrand, variable)))
            return
        lo = _parse(limits[0], variable)
        hi = _parse(limits[1], variable)
        symbol = namespace(variable)[variable]
        king = _king_constant(integrand, symbol, lo, hi)
        if king is not None and _same(king, answer):
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
        for reduced in _reduced_integrals(integrand, symbol, lo, hi):
            if _same(reduced, answer):
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


def fields_for(number: int, integral, answer) -> dict | None:
    import pdf_math

    if not isinstance(integral, pdf_math.IntegralReading) or not isinstance(answer, pdf_math.AnswerReading):
        return None
    if integral.number != number or answer.number != number:
        return None
    variable = integral.variable
    integrand = canon_integrand(integral.integrand, variable)
    answer_s = canon_expr(answer.expr, variable)
    if integrand is None or answer_s is None:
        return None
    if integral.limits is None:
        kind = "indefinite"
        limits: list[str] = []
        limit_pair = None
    else:
        kind = "definite"
        lo = canon_integrand(integral.limits[0], variable)
        hi = canon_integrand(integral.limits[1], variable)
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
