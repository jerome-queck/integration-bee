#!/usr/bin/env python3
"""Reprove the two answered Yang rows and reject their extraction errors."""

from __future__ import annotations

import sympy as sp

import pack_gate
import problem_catalog
import yang_certificates


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def check(rows):
    x = sp.Symbol("x", real=True)
    source = "sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf"
    examples = (
        ("YANG-1.3-Ex01", (x + 1) * (x**2 + 1), ["-1", "1"], sp.Rational(8, 3),
         ("8", "0", "11/3", "8/3+C")),
        ("YANG-1.3-Ex03", ((x - 2) * (x - 3) * (x - 4) + 1) / (x**2 - 6*x + 10),
         ["0", "6"], 2 * sp.atan(3),
         ("0", "atan(3)", "2*atan(3)+1", "2*atan(3)+C")),
    )
    for ident, expression, limits, value, wrong_answers in examples:
        row = rows[ident]
        require(row["verify"] == "sympy" and row["kind"] == "definite", ident + " status")
        require(row["variable"] == "x" and row["limits"] == limits, ident + " endpoints")
        require(row["pdf_path"] == source and row["answer_source_pdf"] == source,
                ident + " printed guide provenance")
        require(pack_gate._parse(row["sympy_expr"], "x") == expression, ident + " source form")
        require(pack_gate._parse(row["answer_sympy"], "x") == value, ident + " printed answer")
        require(bool(row["integrand_latex"]) and bool(row["answer_latex"]), ident + " display fields")
        require(row["answer_plain"] not in ("8", "Z x", None), ident + " extraction repaired")
        require(pack_gate.proven("definite", row["sympy_expr"], limits, row["answer_sympy"], "x"),
                ident + " proof")
        for wrong in wrong_answers:
            require(not pack_gate.proven("definite", row["sympy_expr"], limits, wrong, "x"),
                    ident + " rejects " + wrong)

    expression = examples[1][1]
    require(yang_certificates.definite_value(expression, x, sp.S(0), sp.S(6)) == 2 * sp.atan(3),
            "Yang shifted parity certificate")
    for changed, bounds, label in (
        (2 * expression, (0, 6), "scaled integrand"),
        (expression + 1, (0, 6), "extra summand"),
        (expression, (1, 6), "shifted lower bound"),
        (expression, (0, 5), "shifted upper bound"),
        (expression, (6, 0), "reversed endpoints"),
    ):
        require(yang_certificates.definite_value(changed, x, *bounds) is None,
                "Yang rejects " + label)
    complex_variable = sp.Symbol("z")
    require(yang_certificates.definite_value(expression.subs(x, complex_variable),
                                           complex_variable, 0, 6) is None,
            "Yang requires real substitution variable")


if __name__ == "__main__":
    check({row["id"]: row for row in problem_catalog.load_records()})
    print("PASS Yang answered rows, exact parity certificate, and wrong answers")
