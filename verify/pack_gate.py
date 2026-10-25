"""Prove a layout reading against a mark-scheme reading.

A row is gated only when SymPy differentiates an indefinite answer back to the
integrand, or evaluates a definite integral to the printed answer. Numeric
agreement is not a proof.
"""

from __future__ import annotations

import multiprocessing as mp

import sympy as sp

import check_math

PROOF_TIMEOUT = 20.0


def namespace(variable: str) -> dict:
    ns = dict(check_math.NS)
    ns["ln"] = ns["log"]
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
        value = sp.integrate(integrand, (symbol, lo, hi))
        if _same(value, answer):
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
