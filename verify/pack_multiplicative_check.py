#!/usr/bin/env python3
"""Source-form and grading regressions for the discrete product twins."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import sympy as sp

import pack_gate
import pack_multiplicative
import problem_catalog
import turn_contract


def run() -> None:
    x = sp.Symbol("x", real=True)
    factor = 2025 * x + 2026
    answer = "2025**x*gamma(x+Rational(2026,2025))"
    alternative = "2025**x*(x+Rational(1,2025))*gamma(x+Rational(1,2025))"
    accepted = (
        answer,
        alternative,
        "C*(" + answer + ")",
        "C*(" + alternative + ")",
        "-3*(" + answer + ")",
        "Rational(2,7)*(" + alternative + ")",
        # The problem specifies an inverse of a shift quotient. A nonzero
        # one-periodic factor therefore also satisfies its definition.
        "exp(sin(2*pi*x))*(" + answer + ")",
    )
    rejected = (
        "(" + answer + ")+1",
        "(" + answer + ")+C",
        "2025**x*gamma((x+2026)/2025)",
        "2025**x",
        "gamma(x+Rational(2026,2025))",
        "0",
        "0*(" + answer + ")",
        "nan",
        "oo",
        "zoo",
        "gamma(0)*(" + answer + ")",
        "Integral(exp(x),x)",
    )
    for ident in ("R2-2025-UK-Relay-Q10", "R2-2025-SG-Relay-Q29"):
        row = {
            "id": ident,
            "verify": "sympy",
            "kind": pack_multiplicative.KIND,
            "variable": "x",
            "limits": [],
            "sympy_expr": "2025*x+2026",
            "answer_sympy": answer,
        }
        for expression in accepted + rejected:
            expected = expression in accepted
            parsed = turn_contract.parse_expr(expression)
            assert pack_multiplicative.answer_ok(factor, parsed, x) is expected, expression
            assert turn_contract.answer_matches(row, expression) is expected, expression
            grade, error = turn_contract.grade_problem(ident, expression, "correct", [], [], [row])
            assert error is None, error
            assert grade["correct"] is expected and grade["manual"] is False, expression
            # The stored grading row must retain its factor for retries.
            assert turn_contract.answer_matches(grade["row"], expression) is expected, expression

    canonical = turn_contract.parse_expr(answer)
    other_form = turn_contract.parse_expr(alternative)
    assert sp.simplify(sp.expand_func(canonical - other_form)) == 0
    assert not pack_multiplicative.answer_ok(factor + 1, canonical, x)
    assert not pack_multiplicative.answer_ok(factor, sp.true, x)
    zero_c = sp.Symbol("C", zero=True)
    assert not pack_multiplicative.answer_ok(factor, zero_c * canonical, x)
    # Catalog construction must opt into this kind; it cannot silently
    # reinterpret ordinary indefinite-integral records as products.
    for expression in (answer, alternative, "C*(" + answer + ")"):
        fields = pack_gate.fields_from_parts(
            "2025*x+2026", None, expression, "x", kind=pack_multiplicative.KIND
        )
        assert fields is not None and fields["limits"] == []
        assert fields["kind"] == pack_multiplicative.KIND
        assert pack_gate.reprove_rows([{"id": "product-contract", **fields}]) is None
    assert pack_gate.fields_from_parts("2025*x+2026", None, answer, "x") is None
    assert pack_gate.fields_from_parts(
        "2025*x+2026", ("0", "1"), answer, "x", kind=pack_multiplicative.KIND
    ) is None
    for expression in ("0", answer + "+1", "2025**x*gamma((x+2026)/2025)", "2025**x"):
        assert not pack_gate.proven(pack_multiplicative.KIND, "2025*x+2026", None, expression, "x")
    assert not pack_gate.proven(pack_multiplicative.KIND, "2025*x+2027", None, answer, "x")
    assert not pack_gate.proven(pack_multiplicative.KIND, "2025*x+2026", ("0", "1"), answer, "x")
    # The new kind cannot change ordinary additive-C marking.
    ordinary = {"kind": "indefinite", "limits": [], "answer_sympy": "x**2", "variable": "x"}
    assert turn_contract.answer_matches(ordinary, "x**2+7")
    assert turn_contract.answer_matches(ordinary, "x**2+C")
    assert not turn_contract.answer_matches(ordinary, "3*x**2")
    assert not turn_contract.answer_matches(ordinary, "C*x**2")
    ordinary["answer_sympy"] = answer
    assert turn_contract.answer_matches(ordinary, "(" + answer + ")+C")
    assert not turn_contract.answer_matches(ordinary, "3*(" + answer + ")")
    assert not turn_contract.answer_matches({"kind": "definite", "limits": ["0", "1"], "answer_sympy": "1"}, "1+C")
    # The canonical field writer must regenerate all three H promotions.
    # This is a read-only recovery on copies, not a catalog rewrite.
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    import recover_pack_math

    ids = {"R2-2025-UK-Relay-Q10", "R2-2025-SG-Relay-Q29", "R2-2025-UK-Group-Q10"}
    stored = [row for row in problem_catalog.load_records() if row["id"] in ids]
    assert len(stored) == 3
    recovered, gated = recover_pack_math.recover(copy.deepcopy(stored))
    assert set(gated) == ids and recovered == stored
    print("PASS discrete multiplicative source forms, wrong answers, and additive regressions")


if __name__ == "__main__":
    run()
