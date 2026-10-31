#!/usr/bin/env python3
"""Reprove answered Yang rows and reject their extraction errors."""

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
    _check_section_26(rows, x)

    symbol = pack_gate.namespace("x")["x"]
    certificate_ids = (
        "YANG-1.12-P03",
        "YANG-1.12-P05",
        "YANG-1.12-P06",
        "YANG-1.12-P08",
        "YANG-1.12-P09",
        "YANG-1.12-P10",
        "YANG-1.15-P17",
        "YANG-1.17-P01",
        "YANG-1.18-P02",
        "YANG-1.20-P02",
        "YANG-1.20-P03",
        "YANG-1.20-P05",
        "YANG-1.20-P07",
    )
    for ident in certificate_ids:
        row = rows[ident]
        integrand = pack_gate._parse(row["sympy_expr"], "x")
        lo = pack_gate._parse(row["limits"][0], "x")
        hi = pack_gate._parse(row["limits"][1], "x")
        answer = pack_gate._parse(row["answer_sympy"], "x")
        require(yang_certificates.definite_value(integrand, symbol, lo, hi) == answer,
                ident + " certificate")
        require(yang_certificates.definite_value(2 * integrand, symbol, lo, hi) is None,
                ident + " rejects a scaled integrand")

    sine = rows["YANG-1.12-P05"]
    require(pack_gate.proven("definite", sine["sympy_expr"], sine["limits"], "8", "x"),
            "absolute sine on four periods is 8")
    require(not pack_gate.proven("definite", sine["sympy_expr"], sine["limits"], "4", "x"),
            "absolute sine rejects the integrator value 4")
    antiderivative = sp.integrate(sp.Abs(sp.sin(symbol)), symbol)
    slope = sp.diff(antiderivative, symbol)
    # The integrator stops after one kink: its derivative is -sin for every x <= 0.
    # On [-2π, -π], sin is nonnegative, so |sin| = sin and the formula is the wrong sign.
    require(slope.args[0][0] == -sp.sin(symbol) and slope.args[0][1] == (symbol <= 0),
            "integrator derivative is -sin for x <= 0")
    gap = sp.simplify(slope.subs(symbol, -3 * sp.pi / 2) - sp.Abs(sp.sin(-3 * sp.pi / 2)))
    require(gap == -2, "integrator derivative misses |sin| by -2 at -3π/2")
    require(sp.integrate(sp.Abs(sp.sin(symbol)), (symbol, -2 * sp.pi, -sp.pi)) == -2,
            "integrator value on [-2π, -π]")
    require(yang_certificates.definite_value(sp.Abs(sp.sin(symbol)), symbol, -2 * sp.pi, 2 * sp.pi) == 8,
            "certificate keeps 8")

    for ident in ("YANG-1.15-P10", "YANG-1.15-P11"):
        row = rows[ident]
        integrand = pack_gate._parse(row["sympy_expr"], "x")
        answer = pack_gate._parse(row["answer_sympy"], "x")
        require(row["kind"] == "indefinite" and row["limits"] == [], ident + " kind")
        require(yang_certificates.indefinite_ok(answer, integrand, symbol) is True, ident + " pieces")
        require(yang_certificates.indefinite_ok(sp.Integer(0), integrand, symbol) is False,
                ident + " rejects a constant")
        require(yang_certificates.indefinite_ok(answer, 2 * integrand, symbol) is None,
                ident + " rejects a scaled integrand")
        require(pack_gate.proven("indefinite", row["sympy_expr"], None, row["answer_sympy"], "x"),
                ident + " proof")

    sec = sp.exp(-sp.tan(x)) * sp.sec(x) ** 6
    sec_row = rows["YANG-2.4-P12"]
    require(sec_row["verify"] == "sympy" and sec_row["kind"] == "definite", "YANG-2.4-P12 status")
    require(sec_row["limits"] == ["0", "pi/2"] and sec_row["variable"] == "x", "YANG-2.4-P12 endpoints")
    require(pack_gate._parse(sec_row["sympy_expr"], "x") == sec, "YANG-2.4-P12 integrand")
    require(pack_gate._parse(sec_row["answer_sympy"], "x") == 29, "YANG-2.4-P12 value")
    require(yang_certificates.definite_value(sec, x, sp.S(0), sp.pi / 2) == 29, "sec-tan certificate")
    require(pack_gate.proven("definite", sec_row["sympy_expr"], sec_row["limits"], "29", "x"),
            "YANG-2.4-P12 proof")
    for wrong in ("0", "28", "30", "24"):
        require(not pack_gate.proven("definite", sec_row["sympy_expr"], sec_row["limits"], wrong, "x"),
                "YANG-2.4-P12 rejects " + wrong)
    require(yang_certificates.definite_value(sp.sec(x) ** 5 * sp.exp(-sp.tan(x)), x, 0, sp.pi / 2) is None,
            "sec-tan rejects a lower power")
    require(yang_certificates.definite_value(sec, x, 0, sp.pi) is None, "sec-tan rejects other limits")
    require(yang_certificates._sec_tan_sixth(sec, complex_variable, 0, sp.pi / 2) is None,
            "sec-tan requires a real variable")

    power = (2**x + 3**x) / 5**x
    power_value = 1 / sp.log(sp.Rational(5, 2)) + 1 / sp.log(sp.Rational(5, 3))
    power_row = rows["YANG-1.4-P03"]
    require(power_row["verify"] == "sympy" and power_row["kind"] == "definite", "YANG-1.4-P03 status")
    require(power_row["limits"] == ["0", "oo"] and power_row["variable"] == "x", "YANG-1.4-P03 endpoints")
    require(pack_gate._parse(power_row["sympy_expr"], "x") == power, "YANG-1.4-P03 integrand")
    require(sp.simplify(pack_gate._parse(power_row["answer_sympy"], "x") - power_value) == 0,
            "YANG-1.4-P03 value")
    require(yang_certificates.definite_value(power, x, sp.S(0), sp.oo) == power_value,
            "two-five power certificate")
    require(pack_gate.proven("definite", power_row["sympy_expr"], power_row["limits"],
                             power_row["answer_sympy"], "x"),
            "YANG-1.4-P03 proof")
    for wrong in ("0", "1", "2", "log(5/2) + log(5/3)"):
        require(not pack_gate.proven("definite", power_row["sympy_expr"], power_row["limits"], wrong, "x"),
                "YANG-1.4-P03 rejects " + wrong)
    require(yang_certificates.definite_value((3**x + 4**x) / 5**x, x, 0, sp.oo) is None,
            "power ray rejects other bases")
    require(yang_certificates.definite_value(power, x, 0, 1) is None, "power ray rejects other limits")
    require(yang_certificates._two_five_power_ray(power, complex_variable, 0, sp.oo) is None,
            "power ray requires a real variable")



def _check_section_26(rows, x):
    specs = (
        ("YANG-2.6-P10", "indefinite", []),
        ("YANG-2.6-P14", "definite", ["0", "pi/4"]),
    )
    for ident, kind, limits in specs:
        row = rows[ident]
        require(row["verify"] == "sympy" and row["kind"] == kind, ident + " status")
        require(row["limits"] == limits, ident + " endpoints")
        pair = None if kind == "indefinite" else limits
        require(pack_gate.proven(kind, row["sympy_expr"], pair, row["answer_sympy"], "x"),
                ident + " proof")
        require(not pack_gate.proven(kind, row["sympy_expr"], pair, "0", "x"),
                ident + " rejects 0")
    nested = pack_gate._parse(rows["YANG-2.6-P10"]["sympy_expr"], "x")
    # Audit A1: YANG-2.6-P12 prints sqrt(3)*sin(x) + cos(x) with no radical, so the
    # elliptic certificate is exercised on the radical itself, not on a row.
    radical = pack_gate._parse("1/sqrt(3*sin(x) + cos(x))", "x")
    quarter = pack_gate._parse(rows["YANG-2.6-P14"]["sympy_expr"], "x")
    require(yang_certificates.indefinite_ok(sp.Integer(0), nested, x) is False,
            "nested radical rejects a zero final")
    require(yang_certificates.indefinite_ok(sp.sec(x), 2 * nested, x) is None,
            "nested radical rejects a scaled integrand")
    require(yang_certificates.indefinite_ok(sp.Integer(0), radical, x) is False,
            "elliptic radical rejects a zero final")
    require(yang_certificates.indefinite_ok(sp.sec(x), radical + 1, x) is None,
            "elliptic radical rejects an extra summand")
    require(yang_certificates.definite_value(quarter, x, 0, sp.pi / 2) is None,
            "log-cosine quarter rejects a longer interval")
    require(yang_certificates.definite_value(2 * quarter, x, 0, sp.pi / 4) is None,
            "log-cosine quarter rejects a scaled integrand")


if __name__ == "__main__":
    check({row["id"]: row for row in problem_catalog.load_records()})
    print("PASS Yang answered rows, parity, sec-tan, §1.4 power-ray, and §2.6 certificates, and wrong answers")
