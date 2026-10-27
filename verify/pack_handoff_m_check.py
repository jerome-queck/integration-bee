"""Handoff M clarified Relay sources, automatic grades, and negative controls.

Malformed source shapes are checked against the narrow matchers directly;
the literal Q19 print also exercises the public expression proof path.
"""

from __future__ import annotations

import copy
import sys

import sympy as sp

import pack_answer_contracts
import pack_gate
import pack_handoff_m as handoff
import problem_catalog
import turn_contract


IDS = ("R2-2021-Relay-D03", "R2-2023-Relay-Q19", "R2-2023-Relay-Q20")


def _require(condition, label):
    if not condition:
        raise AssertionError("handoff M: " + label)


def _answer(row, submitted, expected):
    ident = row["id"]
    _require(pack_gate.proven(row["kind"], row["sympy_expr"], row["limits"],
                             submitted, row["variable"]) is expected,
             ident + " proof of " + submitted)
    result, error = turn_contract.grade_problem(ident, submitted, None, [], [], [row])
    _require(error is None and result is not None,
             ident + " well-formed automatic answer: " + submitted)
    _require(result["correct"] is expected and result["manual"] is False,
             ident + " automatic grade of " + submitted)


def _stored_and_recovered(rows):
    x = sp.Symbol("x", real=True)
    n = sp.Symbol("n", integer=True, positive=True)
    expected = {
        IDS[0]: ("definite", handoff.MinimalLogPassOn(
            sp.Integral((1 - x) / (2*x + 1), (x, 0, 1))), ["0", "1"],
            (1 + sp.sqrt(5)) / 2),
        IDS[1]: ("expression", sp.Limit(sp.Integral(
            sp.cos(x / sp.sqrt(n))**n, (x, 0, sp.sqrt(n))), n, sp.oo), [],
            sp.sqrt(sp.pi / 2)),
        IDS[2]: ("definite", sp.log(1 + x**2) / 4, ["-1", "1"],
            (sp.pi + sp.log(4) - 4) / 4),
    }
    readings = pack_answer_contracts.transcripts()
    _require(set(handoff.transcripts()) == set(IDS), "exactly three M transcripts")
    _require(set(IDS) <= set(readings), "M transcripts registered for recovery")
    _require(IDS[1] not in problem_catalog.MANUAL_INPUT_KINDS,
             "Q19 removed from manual-input exception")
    for ident, (kind, expr, bounds, answer) in expected.items():
        row = rows[ident]
        _require(row["verify"] == "sympy" and row["kind"] == kind
                 and row["variable"] == "x" and row["limits"] == bounds,
                 ident + " checked kind, variable, and bounds")
        _require(pack_gate._parse(row["sympy_expr"], "x") == expr,
                 ident + " full clarified source shape")
        _require(sp.simplify(pack_gate._parse(row["answer_sympy"], "x") - answer) == 0,
                 ident + " independently expected final")
        fields = pack_gate.fields_from_contract(*readings[ident])
        _require(fields is not None, ident + " transcript reconstructs checked fields")
        for key, value in fields.items():
            if key in {"sympy_expr", "answer_sympy"}:
                # Cached equal Symbols may reorder srepr assumption keywords.
                # Exact parsed equality still retains every operator and bound.
                _require(pack_gate._parse(row[key], "x") == pack_gate._parse(value, "x"),
                         ident + " round-trip " + key)
            else:
                _require(row[key] == value, ident + " round-trip " + key)

    selected = [rows[ident] for ident in IDS]
    _require(pack_gate.reprove_rows(selected) is None, "all three stored rows reprove")
    sys.path.insert(0, str(problem_catalog.ROOT / "scripts"))
    import recover_pack_math

    recovered, gated = recover_pack_math.recover(copy.deepcopy(selected))
    _require(len(recovered) == 3 and set(gated) == set(IDS),
             "targeted recovery re-proves exactly these three rows")
    for stored, restored in zip(selected, recovered):
        comparable = dict(restored)
        for key in ("sympy_expr", "answer_sympy"):
            _require(pack_gate._parse(stored[key], "x")
                     == pack_gate._parse(restored[key], "x"),
                     stored["id"] + " recovery preserves " + key)
            comparable[key] = stored[key]
        _require(comparable == stored,
                 stored["id"] + " recovery preserves prompts, notes, extracts, and status")
    return x, n, expected


def _clarified_prompts(rows):
    required = {
        IDS[0]: ("c=1", "gcd(r,s)=1", "u minimal", "Pass on (r+sqrt(r+s))/u"),
        IDS[1]: ("positive integers n", "from 0 to sqrt(n)", "printed PDF has upper bound n"),
        IDS[2]: ("real and differentiable", "f(x)>0 for every 0<|x|<=1", "both sides of zero"),
    }
    for ident, phrases in required.items():
        row = rows[ident]
        prompt = problem_catalog.prompt_view(row)["integrand_plain"]
        _require(all(phrase in prompt for phrase in phrases),
                 ident + " learner sees the grading clarification")
        _require("source discrepancy" in row["notes"] and "clarification" in row["notes"],
                 ident + " source conflict stays explicit")
        _require(bool(row["extraction"]["raw_snippet"])
                 and prompt != row["extraction"]["raw_snippet"],
                 ident + " preserves a separate unamended extract")


def _answer_controls(rows):
    correct = {
        IDS[0]: ("(1+sqrt(5))/2", "2/(sqrt(5)-1)"),
        IDS[1]: ("sqrt(pi/2)", "sqrt(2*pi)/2"),
        IDS[2]: ("(pi+log(4)-4)/4", "pi/4+ln(2)/2-1"),
    }
    wrong = {
        IDS[0]: ("1", "(log(27)-2)/4"),
        IDS[1]: ("0", "1", "sqrt(pi)", "pi/2"),
        IDS[2]: ("0", "(pi+log(4)-4)/8"),
    }
    for ident in IDS:
        for submitted in correct[ident]:
            _answer(rows[ident], submitted, True)
        for submitted in wrong[ident]:
            _answer(rows[ident], submitted, False)


def _source_controls(x, n, expected):
    cosine = expected[IDS[1]][1]
    literal = sp.Limit(sp.Integral(sp.cos(x/sp.sqrt(n))**n, (x, 0, n)), n, sp.oo)
    bad_cosines = (
        literal,
        cosine.xreplace({n: sp.Symbol("n", positive=True)}),
        cosine.xreplace({n: sp.Symbol("n", integer=True)}),
        sp.Limit(sp.Integral(sp.cos(x/sp.sqrt(n))**n, (x, 1, sp.sqrt(n))), n, sp.oo),
        sp.Limit(sp.Integral(sp.sin(x/sp.sqrt(n))**n, (x, 0, sp.sqrt(n))), n, sp.oo),
        sp.Limit(cosine.args[0], n, 1),
    )
    for expr in bad_cosines:
        _require(not handoff.open_expression("expression", expr, x),
                 "Q19 rejects changed limit, kernel, bound, or integer assumptions")
        _require(handoff.answer_value("expression", expr, x, None) is None,
                 "Q19 cannot derive an answer from an altered source")
    _require(not handoff.open_expression("definite", cosine, x),
             "Q19 retains its complete expression kind")
    _require(handoff.answer_value("expression", cosine, x, (0, sp.sqrt(n))) is None,
             "Q19 rejects spurious outer bound metadata")
    _require(not handoff.open_expression("expression", cosine, sp.Symbol("x")),
             "Q19 requires a real integration variable")
    for answer in ("sqrt(pi/2)", "oo"):
        _require(not pack_gate.proven("expression", sp.srepr(literal), [], answer, "x"),
                 "literal n-bound Q19 rejected by public proof: " + answer)

    shuttle = expected[IDS[0]][1]
    bad_shuttles = (
        shuttle.args[0],
        handoff.MinimalLogPassOn(sp.Integral((1+x)/(2*x+1), (x, 0, 1))),
        handoff.MinimalLogPassOn(sp.Integral((1-x)/(2*x+1), (x, 0, 2))),
        handoff.MinimalLogPassOn((sp.log(27)-2)/4),
    )
    for expr in bad_shuttles:
        _require(not handoff.open_integrand(expr, x),
                 "D03 requires the complete normalized pass-on and original integral")
        _require(handoff.definite_value(expr, x, 0, 1) is None,
                 "D03 rejects changed wrapper, kernel, or inner bounds")
    for bounds in ((0, 2), (-1, 1)):
        _require(handoff.definite_value(shuttle, x, *bounds) is None,
                 "D03 inner and metadata bounds must agree")
    _require(not handoff.open_integrand(shuttle, sp.Symbol("x")),
             "D03 requires a real integration variable")

    branch = expected[IDS[2]][1]
    for expr in (sp.Integer(0), branch + 1, branch**2):
        _require(handoff.definite_value(expr, x, -1, 1) is None,
                 "Q20 only certifies the selected logarithmic branch")
    for bounds in ((0, 1), (-1, 2)):
        _require(handoff.definite_value(branch, x, *bounds) is None,
                 "Q20 requires the complete two-sided interval")
    _require(handoff.definite_value(branch, sp.Symbol("x"), -1, 1) is None,
             "Q20 requires a real integration variable")


def check(rows):
    x, n, expected = _stored_and_recovered(rows)
    _clarified_prompts(rows)
    _answer_controls(rows)
    _source_controls(x, n, expected)


if __name__ == "__main__":
    check({row["id"]: row for row in problem_catalog.load_records()})
    print("PASS Handoff M (3 clarified Relay proofs, grading, recovery, source and answer controls)")
