"""End-to-end Handoff F answer kinds and source-shape regression controls.

Invalid source shapes are tested directly against the narrow certificate
modules, so they cannot consume an ordinary integrator's proof timeout.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import sympy as sp

import pack_answer_contracts
import pack_gate
import pack_handoff_f_domain as domain
import pack_handoff_f_expressions as expressions
import pack_handoff_f_integrals as integrals
import turn_contract


KINDS = {
    "R2-2021-Relay-B03": "definite",
    "R2-2021-Relay-D01": "prime_factors",
    "R2-2022-Relay-Q01": "comparison",
    "R2-2022-Relay-Q09": "function",
    "R2-2022-Relay-Q12": "expression",
    "R2-2022-Relay-Q13": "root_count",
    "R2-2022-Relay-Q15": "domain",
    "R2-2023-Relay-Q11": "expression",
    "R2-2025-SG-Relay-Q17": "product_indefinite",
    "R3-2024-Dichotomy-S2-Q07a": "definite",
}

DEFERRED = (
    "R2-2021-Relay-D03",
    "R2-2023-Relay-Q20",
    "R3-2024-Tournament-Q04-v10",
    "R3-2024-Tournament-Q04-v11",
    "R3-2024-Tournament-Q04-v12",
)


def _require(condition, label):
    if not condition:
        raise AssertionError("handoff F: " + label)


def _grade(row, submitted, expected):
    result, error = turn_contract.grade_problem(row["id"], submitted, None, [], [], [row])
    _require(error is None and result is not None,
             f"{row['id']} well-formed answer has a grade: {submitted!r}")
    accepted = error is None and result is not None and result["correct"] is True
    _require(accepted is expected, f"{row['id']} grading {submitted!r}")
    if expected:
        _require(result["manual"] is False, row["id"] + " automatic kind-aware mark")


def _stored_and_recovered(rows):
    # Exercise the srepr cache-order regression even in a fresh process:
    # the source builder supplies these same assumptions in the other order.
    _prewarmed_power = sp.Symbol("x", real=True) ** sp.Symbol(
        "n", integer=True, positive=True
    )
    readings = pack_answer_contracts.transcripts()
    _require(set(readings) == set(KINDS), "exactly the ten F promotion transcripts")
    parsed = {}
    for ident, expected_kind in KINDS.items():
        row = rows[ident]
        kind, text, bounds, answer, variable = readings[ident]
        _require(kind == row["kind"] == expected_kind and row["verify"] == "sympy",
                 ident + " stored kind")
        fields = pack_gate.fields_from_contract(kind, text, bounds, answer, variable)
        _require(fields is not None, ident + " recovered source proves")
        for key, value in fields.items():
            if key in {"sympy_expr", "answer_sympy"}:
                # SymPy may reuse a cached Pow with an equal Symbol whose
                # constructor assumptions were supplied in a different order.
                # That changes srepr's keyword order, not the expression.
                # Strict parsed equality still checks every bound, operator
                # and symbol assumption; no algebraic simplification is used.
                _require(pack_gate._parse(row.get(key), variable)
                         == pack_gate._parse(value, variable),
                         ident + " recovered " + key)
            else:
                _require(row.get(key) == value, ident + " recovered " + key)
        _require(pack_gate.proven(kind, row["sympy_expr"], row["limits"],
                                 row["answer_sympy"], row["variable"]),
                 ident + " stored fields prove")
        symbol = pack_gate.namespace(variable)[variable]
        expr = pack_gate._parse(row["sympy_expr"], variable)
        parsed_bounds = tuple(pack_gate._parse(b, variable) for b in (row["limits"] or []))
        parsed[ident] = (expr, symbol, parsed_bounds)
        _grade(row, row["answer_sympy"], True)
    for ident in DEFERRED:
        _require(rows[ident]["verify"] == "manual", ident + " source discrepancy stays manual")
    return parsed


def _answer_controls(rows):
    product = "x**(x**2/2)*exp(-x**2/4)"
    positives = {
        "R2-2021-Relay-D01": ("2,3", "3,2"),
        "R2-2022-Relay-Q01": ("I=J",),
        "R2-2022-Relay-Q09": ("exp(x)", "cosh(x)+sinh(x)"),
        "R2-2025-SG-Relay-Q17": (
            product, "2*(" + product + ")", "C*(" + product + ")",
            "exp(x**2*log(x)/2-x**2/4)",
        ),
        "R2-2022-Relay-Q15": (
            "Piecewise((pi/(2*cos(pi/n)), n>2), (oo, True))",
        ),
    }
    negatives = {
        "R2-2021-Relay-B03": ("0", "pi*log(2)/4", "oo", "atan(1)"),
        "R2-2021-Relay-D01": ("1/6", "2", "6", "3,2,1", "2,2,3", "{2,2,3}"),
        "R2-2022-Relay-Q01": ("I>J", "J>I", "0", "1"),
        "R2-2022-Relay-Q09": (
            "1", "exp(-x)", "x+1", "0", "E",
            "Piecewise((exp(x), x<1), (2*exp(x), True))",
            "Piecewise((2, Eq(x,1)), (exp(x), True))",
        ),
        "R2-2022-Relay-Q12": ("1", "log(3)", "1/2", "harmonic(n)"),
        "R2-2022-Relay-Q13": ("0", "2", "oo", "2*pi"),
        "R2-2022-Relay-Q15": (
            "pi/(2*cos(pi/n))", "pi/2", "0", "oo",
            "Piecewise((pi/(2*cos(pi/n)), n>=2), (oo, True))",
            "Piecewise((pi/(2*cos(pi/n)), n>3), (oo, True))",
            "Piecewise((pi/(2*cos(pi/n)), n>2), (0, True))",
        ),
        "R2-2023-Relay-Q11": ("2/E", "4", "E/4", "2"),
        "R2-2025-SG-Relay-Q17": (
            "0", "-(" + product + ")", product + "+1", product + "+C",
            "-C*(" + product + ")", "Symbol('C',negative=True)*(" + product + ")", "x**x",
            product + "*exp(atan(tan(x))-x)",
            product + "*exp(atan(tan(log(x)))-log(x))",
        ),
        "R3-2024-Dichotomy-S2-Q07a": ("0", "E", "1", "-oo", "atan(1)"),
    }
    for ident, answers in positives.items():
        for answer in answers:
            _grade(rows[ident], answer, True)
    for ident, answers in negatives.items():
        for answer in answers:
            _grade(rows[ident], answer, False)

    # Extended values must be compared before subtraction.  Neither NaN nor
    # complex infinity is a valid signed-infinity or finite-scalar answer.
    for answer, submitted, correct in (
        ("oo", "oo", True), ("-oo", "-oo", True), ("oo", "-oo", False),
        ("oo", "0", False), ("nan", "nan", False), ("zoo", "zoo", False),
        ("pi/4", "atan(1)", True), ("pi/4", "0", False), ("pi/4", "oo", False),
    ):
        _require(turn_contract.expressions_match(answer, submitted, False) is correct,
                 "scalar comparator " + answer + " versus " + submitted)
    _require(turn_contract.expressions_match("x**2/2", "x**2/2+C", True),
             "ordinary primitive keeps additive constant")
    _require(not turn_contract.expressions_match("x**2/2", "x**2", True),
             "ordinary primitive rejects multiplicative scaling")


def _parse_errors(rows):
    for ident, kind in KINDS.items():
        if kind not in pack_answer_contracts.KINDS:
            continue
        result, error = turn_contract.grade_problem(ident, "broken(", None, [], [], [rows[ident]])
        _require(result is None and error and error.startswith("answer did not parse:"),
                 ident + " malformed answer remains a parse error")
    root = Path(__file__).resolve().parent.parent
    with tempfile.TemporaryDirectory(prefix="ib-f-parse-") as tmp:
        temporary = Path(tmp)
        data = temporary / "data"
        data.mkdir()
        payload = temporary / "turn.json"
        env = dict(os.environ, IB_DATA_DIR=str(data))
        for ident in ("R2-2022-Relay-Q01", "R2-2021-Relay-D01"):
            payload.write_text(json.dumps({
                "kind": "mark", "problem_id": ident, "source": "typed",
                "extract": {"final_answer": "broken("},
            }))
            result = subprocess.run(
                [sys.executable, str(root / "scripts/control-integration-bee"),
                 "turn", "apply", "--file", str(payload), "--format", "json"],
                cwd=root, env=env, text=True, capture_output=True,
            )
            _require(result.returncode == 2 and "answer did not parse" in result.stderr,
                     ident + " CLI parse failure exits 2")
            _require(not list(data.iterdir()), ident + " parse failure writes no learner state")


def _integral_shapes(parsed):
    for ident in ("R2-2021-Relay-B03", "R2-2021-Relay-D01", "R3-2024-Dichotomy-S2-Q07a"):
        expr, symbol, bounds = parsed[ident]
        _require(isinstance(expr, sp.Limit) and isinstance(expr.args[0], sp.Integral),
                 ident + " retains full limit of integral")
        inner, parameter, endpoint, side = expr.args
        changed = sp.Limit(sp.Integral(inner.function + 1, *inner.limits),
                           parameter, endpoint, dir=str(side))
        _require(not integrals.open_integrand(changed, symbol), ident + " changed integrand")
        _require(integrals.answer_value(KINDS[ident], expr, symbol,
                                       (bounds[0] + 1, bounds[1])) is None,
                 ident + " changed bound metadata")
        changed = expr.xreplace({parameter: sp.Symbol(parameter.name)})
        _require(not integrals.open_integrand(changed, symbol), ident + " missing parameter assumptions")
    expr, symbol, bounds = parsed["R2-2021-Relay-B03"]
    inner, parameter, endpoint, _ = expr.args
    changed = sp.Limit(inner, parameter, endpoint, dir="-")
    _require(not integrals.open_integrand(changed, symbol), "B03 keeps positive-parameter approach")
    changed = expr.xreplace({parameter: sp.Symbol(parameter.name, positive=True, integer=True)})
    _require(not integrals.open_integrand(changed, symbol), "B03 rejects a discrete parameter approaching zero")
    expr, symbol, bounds = parsed["R2-2021-Relay-D01"]
    _require(integrals.answer_value("definite", expr, symbol, bounds) is None,
             "D01 is a prime-factor answer rather than a scalar limit answer")
    expr, symbol, bounds = parsed["R3-2024-Dichotomy-S2-Q07a"]
    n = expr.args[1]
    changed = sp.Limit(sp.Integral(sp.log(1 + sp.E/n + 1/sp.sqrt(n*symbol)),
                                 (symbol, 1, n)), n, sp.oo)
    _require(not integrals.open_integrand(changed, symbol), "Dichotomy rejects changed root power")
    expr, symbol, bounds = parsed["R2-2025-SG-Relay-Q17"]
    _require(expr == symbol**symbol and not bounds, "product question and indefinite bounds")
    _require(integrals.answer_value("product_indefinite", expr, symbol, (0, 1)) is None,
             "product primitive cannot gain definite bounds")
    _require(integrals.answer_value("product_indefinite", symbol, symbol, None) is None,
             "product certificate rejects changed integrand")


def _expression_shapes(parsed):
    for ident in ("R2-2022-Relay-Q01", "R2-2022-Relay-Q09", "R2-2022-Relay-Q12",
                  "R2-2022-Relay-Q13", "R2-2023-Relay-Q11"):
        expr, symbol, bounds = parsed[ident]
        kind = KINDS[ident]
        _require(not bounds and expressions.open_expression(kind, expr, symbol),
                 ident + " typed original expression")
        _require(expressions.answer_value(kind, expr, symbol, (0, 1)) is None,
                 ident + " rejects unrelated outer integral metadata")
    expr, symbol, _ = parsed["R2-2022-Relay-Q01"]
    _require(isinstance(expr, sp.Tuple) and all(isinstance(v, sp.Integral) for v in expr),
             "comparison keeps both original integrals")
    left, right = expr
    changed = sp.Tuple(left, sp.Integral(right.function, (symbol, 0, 2)))
    _require(not expressions.open_expression("comparison", changed, symbol), "comparison wrong upper bound")
    a = next(iter(left.free_symbols))
    _require(not expressions.open_expression("comparison", expr.xreplace({a: sp.Symbol(a.name)}), symbol),
             "comparison missing positive-root assumption")
    expr, symbol, _ = parsed["R2-2022-Relay-Q09"]
    _require(isinstance(expr, sp.Equality) and expr.has(sp.Integral), "function keeps integral equation")
    changed = sp.Eq(expr.lhs, 2, evaluate=False)
    _require(not expressions.open_expression("function", changed, symbol), "function altered initial datum")
    expr, symbol, _ = parsed["R2-2022-Relay-Q13"]
    _require(isinstance(expr, expressions.RootCount), "root count has explicit operator")
    for interval in (sp.Interval(0, 2*sp.pi), sp.Interval.open(0, 2*sp.pi)):
        changed = expressions.RootCount(expr.args[0], symbol, interval)
        _require(not expressions.open_expression("root_count", changed, symbol),
                 "root count preserves endpoint inclusion")
    for ident, cls in (("R2-2022-Relay-Q12", sp.Sum), ("R2-2023-Relay-Q11", sp.Product)):
        expr, symbol, _ = parsed[ident]
        _require(isinstance(expr, sp.Limit) and expr.has(cls) and not expr.has(sp.Integral),
                 ident + " keeps scalar sum/product limit without invented integral")
        finite = next(iter(expr.atoms(cls)))
        k, lo, hi = finite.limits[0]
        changed = expr.xreplace({finite: cls(finite.function, (k, lo + 1, hi))})
        _require(not expressions.open_expression("expression", changed, symbol), ident + " changed index range")
        n = expr.args[1]
        changed = expr.xreplace({n: sp.Symbol(n.name, positive=True)})
        _require(not expressions.open_expression("expression", changed, symbol), ident + " integer index required")


def _domain_shapes(rows, parsed):
    ident = "R2-2022-Relay-Q15"
    expr, symbol, bounds = parsed[ident]
    _require(isinstance(expr, sp.Integral) and domain.open_expression(expr, symbol),
             "domain keeps original improper integral")
    n = next(iter(expr.free_symbols))
    _require(n == sp.Symbol(n.name, real=True), "domain includes every real n")
    answer = pack_gate._parse(rows[ident]["answer_sympy"], rows[ident]["variable"])
    _require(isinstance(answer, sp.Piecewise), "domain answer keeps both branches")
    for value in (-2, 0, 1, 2):
        _require(answer.subs(n, value) == sp.oo, "domain divergent branch at n=" + str(value))
    _require(sp.simplify(answer.subs(n, 4) - sp.pi/sp.sqrt(2)) == 0,
             "domain convergent sample")
    changed = sp.Integral(expr.function, (symbol, 1, sp.oo))
    _require(not domain.open_expression(changed, symbol), "domain wrong original lower bound")
    changed = expr.xreplace({n: sp.Symbol(n.name, positive=True)})
    _require(not domain.open_expression(changed, symbol), "domain cannot silently restrict n")
    changed = sp.Integral(sp.acot(symbol**n), (symbol, 0, sp.oo))
    _require(not domain.open_expression(changed, symbol), "domain changed exponent")
    _require(domain.answer_value("domain", expr, symbol, (1, sp.oo)) is None,
             "domain bound metadata agreement")


def check(rows):
    parsed = _stored_and_recovered(rows)
    _answer_controls(rows)
    _parse_errors(rows)
    _integral_shapes(parsed)
    _expression_shapes(parsed)
    _domain_shapes(rows, parsed)


if __name__ == "__main__":
    import problem_catalog

    check({row["id"]: row for row in problem_catalog.load_records()})
    print("PASS Handoff F (10 typed proofs, grading, original shapes, domains, 5 source deferrals)")
