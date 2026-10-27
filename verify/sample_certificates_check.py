#!/usr/bin/env python3
"""Domain, source-shape, and symbolic-proof regressions for SAMPLE rows."""

from __future__ import annotations

import sympy as sp

import pack_gate
import problem_catalog
import sample_certificates


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def check(rows):
    x = sp.Symbol("x", real=True)
    for ident in ("SAMPLE-Q05", "SAMPLE-Q08", "SAMPLE-Q09"):
        row = rows[ident]
        expression = pack_gate._parse(row["sympy_expr"], "x")
        answer = pack_gate._parse(row["answer_sympy"], "x")
        lo, hi = (pack_gate._parse(bound, "x") for bound in row["limits"])
        value = sample_certificates.definite_value(expression, x, lo, hi)
        require(value is not None and sp.simplify(value - answer) == 0,
                ident + " exact certificate")
        for changed, bounds, label in (
            (2 * expression, (lo, hi), "scaled integrand"),
            (expression, (lo + 1, hi), "changed lower bound"),
            (expression, (hi, lo), "reversed bounds"),
        ):
            require(sample_certificates.definite_value(changed, x, *bounds) is None,
                    ident + " rejects " + label)

    row = rows["SAMPLE-Q08"]
    expression = pack_gate._parse(row["sympy_expr"], "x")
    answer = pack_gate._parse(row["answer_sympy"], "x")
    sigma = sp.Symbol("sigma", positive=True)
    tau = sp.Symbol("tau", real=True)
    s = 1 + sigma + sp.I * tau
    require(sample_certificates.s_parameter(expression, x, 0, sp.oo) == s,
            "sample zeta printed parameter")
    fields = pack_gate.fields_from_parts(
        row["sympy_expr"], ("0", "oo"), row["answer_sympy"], "x"
    )
    require(fields is not None, "sample zeta canonical fields")
    require(pack_gate._parse(fields["sympy_expr"], "x") == expression
            and pack_gate._parse(fields["answer_sympy"], "x") == answer,
            "sample zeta assumptions round-trip")
    require(expression.free_symbols == {x, sigma, tau}
            and answer.free_symbols == {sigma, tau}, "sample zeta explicit assumptions")

    for exponent, label in (
        (sp.Symbol("sigma") + sp.I * tau, "missing sigma positivity"),
        (sp.Symbol("sigma", nonnegative=True) + sp.I * tau, "sigma may be zero"),
        (sigma + sp.I * sp.Symbol("tau"), "missing tau reality"),
        (sp.S.Zero, "s equals one"),
        (-sp.Rational(1, 2), "s below one"),
    ):
        changed = x**exponent / (sp.exp(x) - 1)
        continued_answer = sp.gamma(1 + exponent) * sp.zeta(1 + exponent)
        require(sample_certificates.s_parameter(changed, x, 0, sp.oo) is None,
                "sample zeta mapping rejects " + label)
        require(not pack_gate.proven("definite", sp.srepr(changed), ["0", "oo"],
                                     sp.srepr(continued_answer), "x"),
                "sample zeta proof rejects " + label)
    require(sample_certificates.s_parameter(expression, x, 1, sp.oo) is None,
            "sample zeta mapping requires original bounds")
    require(sample_certificates.s_parameter(2 * expression, x, 0, sp.oo) is None,
            "sample zeta mapping requires original integrand")

    row = rows["SAMPLE-Q19"]
    expression = pack_gate._parse(row["sympy_expr"], "x")
    answer = pack_gate._parse(row["answer_sympy"], "x")
    require(sample_certificates.indefinite_ok(answer, expression, x) is True,
            "sample radical exact derivative")
    require(sample_certificates.indefinite_ok(answer, 2 * expression, x) is None,
            "sample radical requires original integrand")
    # The added term has zero derivative on x>0 but derivative -2 on
    # x<0.  A positive-only check or a forced Abs(x)->x rewrite misses it.
    positive_only = answer + sp.Abs(x) - x
    discrepancy = sp.diff(positive_only, x) - sp.diff(answer, x)
    require(discrepancy.subs(x, sp.Rational(1, 2)) == 0
            and discrepancy.subs(x, -sp.Rational(1, 2)) == -2,
            "sample radical branch control has a negative-side error")
    require(not pack_gate.proven("indefinite", row["sympy_expr"], None,
                                 sp.srepr(positive_only), "x"),
            "sample radical rejects positive-only primitive")

    jump = sp.Piecewise((0, x < 0), (1, True))
    require(sp.diff(jump, x) == 0 and jump.subs(x, 0) == 1
            and sp.limit(jump.args[0].expr, x, 0, dir="-") == 0,
            "sample radical jump is hidden by piecewise differentiation")
    require(not pack_gate.proven("indefinite", row["sympy_expr"], None,
                                 sp.srepr(answer + jump), "x"),
            "sample radical rejects a discontinuous primitive")

    # Match every sanity probe in sample_self_check while changing the
    # derivative elsewhere. This must fail even though all finite probes
    # agree exactly; the certificate requires a symbolic identity.
    probes = (-sp.Rational(4, 5), -sp.Rational(1, 2), sp.S.Zero,
              sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(4, 5))
    correction = sp.prod((x - point)**2 for point in probes)
    derivative = sp.diff(correction, x)
    require(all(derivative.subs(x, point) == 0 for point in probes),
            "sample radical impostor agrees on finite probes")
    require(derivative.subs(x, sp.Rational(1, 3)) != 0,
            "sample radical impostor is not an antiderivative")
    require(not pack_gate.proven("indefinite", row["sympy_expr"], None,
                                 sp.srepr(answer + correction), "x"),
            "sample radical rejects finite-probe impostor")


if __name__ == "__main__":
    check({row["id"]: row for row in problem_catalog.load_records()})
    print("PASS sample certificate domains, source shapes, and symbolic derivatives")
