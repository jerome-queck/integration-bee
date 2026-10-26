#!/usr/bin/env python3
"""Reprove the source-backed certificates and reject corrupted readings."""

from __future__ import annotations

import sys

import sympy as sp

import pack_gate
import problem_catalog


IDS = (
    "R2-2023-Group-Q05",
    "R2-2025-SG-Group-Q07",
    "R2-2025-SG-Relay-Q03",
    "R2-2025-UK-Group-Q06",
    "R2-2025-UK-Relay-Q03",
)


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def probe(expr, limits, answer, expected, label):
    actual = pack_gate.proven(
        "definite", sp.srepr(expr), tuple(map(sp.sstr, limits)), sp.srepr(answer), "x"
    )
    require(actual is expected, label)


def check_sphere():
    x = sp.Symbol("x", real=True)
    t = sp.Symbol("t")
    inner = sp.Integral(sp.exp(sp.sin(x) * (sp.cos(t) - sp.sin(t))), (t, 0, 2 * sp.pi))
    expr = sp.sin(x) * inner
    answer = 2 * sp.sqrt(2) * sp.pi * sp.sinh(sp.sqrt(2))
    probe(expr, (0, sp.pi), answer, True, "sphere original")
    for label, changed, limits, final in (
        ("sphere scale", 2 * expr, (0, sp.pi), answer),
        ("sphere outer bound", expr, (0, 2 * sp.pi), answer),
        ("sphere inner bound", expr.xreplace({2 * sp.pi: sp.pi}), (0, sp.pi), answer),
        ("sphere exponent", expr.xreplace({sp.cos(t): 2 * sp.cos(t)}), (0, sp.pi), answer),
        ("sphere final", expr, (0, sp.pi), answer + 1),
        ("sphere radical scope", expr, (0, sp.pi), 2 * sp.sqrt(2 * sp.pi) * sp.sinh(sp.sqrt(2))),
    ):
        probe(changed, limits, final, False, label)


def check_grid():
    x = sp.Symbol("x", real=True)
    m, n = sp.symbols("m n", integer=True, positive=True)
    k = sp.Symbol("k", integer=True)

    def grid(index, degree=26, count=2026, frequency=1, start=0, radicand=-1):
        return sp.Sum(
            (x + sp.sqrt(x**2 + radicand) * sp.cos(2 * sp.pi * frequency * k / (index + count)))
            ** (index + degree),
            (k, start, index + count - 1),
        )

    expr = grid(m) * grid(n)
    diagonal = 2 * (n + 2026)**2 / (2 * n + 53)
    answer = sp.Piecewise((diagonal, sp.Eq(m, n)), (0, True))
    probe(expr, (-1, 1), answer, True, "grid original")
    for label, changed in (
        ("grid one degree", grid(m, degree=27) * grid(n)),
        ("grid both degrees, stale final", grid(m, degree=27) * grid(n, degree=27)),
        ("grid size, stale final", grid(m, count=2027) * grid(n, count=2027)),
        ("grid aliasing", grid(m, count=26) * grid(n, count=26)),
        ("grid frequency", grid(m, frequency=2) * grid(n)),
        ("grid lower index", grid(m, start=1) * grid(n)),
        ("grid radicand", grid(m, radicand=1) * grid(n)),
        ("grid scale", 2 * expr),
        ("grid extra term", expr + 1),
        ("grid integer assumption", expr.xreplace({n: sp.Symbol("n", positive=True)})),
        ("grid positive assumption", expr.xreplace({n: sp.Symbol("n", integer=True)})),
        ("grid bound-index collision", expr.xreplace({k: n})),
    ):
        probe(changed, (-1, 1), answer, False, label)
    for label, changed in (
        ("grid final", answer + 1),
        ("grid diagonal only", diagonal),
        ("grid zero only", sp.Integer(0)),
        ("grid wrong off-diagonal", sp.Piecewise((diagonal, sp.Eq(m, n)), (1, True))),
        ("grid signed off-diagonal", sp.Piecewise(
            (diagonal, sp.Eq(m, n)), (sp.Abs(m - n) - (m - n), True)
        )),
    ):
        probe(expr, (-1, 1), changed, False, label)
    probe(expr, (0, 1), answer, False, "grid lower bound")
    probe(expr, (-1, 2), answer, False, "grid upper bound")

    adjusted = grid(m, degree=0, count=1) * grid(n, degree=0, count=1)
    adjusted_answer = sp.Piecewise((2 * (n + 1)**2 / (2 * n + 1), sp.Eq(m, n)), (0, True))
    probe(adjusted, (-1, 1), adjusted_answer, True, "grid certificate is all-degree")
    fields = pack_gate.fields_from_parts(sp.srepr(expr), ("-1", "1"), sp.srepr(answer), "x")
    require(fields is not None, "grid canonical fields")
    require(pack_gate._parse(fields["sympy_expr"], "x") == expr, "grid assumptions round-trip")
    require(pack_gate._parse(fields["answer_sympy"], "x") == answer, "grid answer round-trip")
    t = sp.Symbol("t", real=True)
    renamed = pack_gate.fields_from_parts(
        sp.srepr(expr.xreplace({x: t})), ("-1", "1"), sp.srepr(answer), "t"
    )
    require(renamed == fields, "renamed grid keeps explicit parameter assumptions")


def check_tangent():
    x = sp.Symbol("x", real=True)
    expr = sp.cos(x)**2 / (sp.cos(x)**2 + (x * sp.cos(x) + sp.sin(x) + 1)**2)
    probe(expr, (-sp.oo, sp.oo), sp.pi, True, "tangent original")
    probe(expr, (-sp.oo, sp.oo), sp.pi + 1, False, "tangent final")
    a = sp.Symbol("a")
    branch_sensitive = sp.pi + sp.log(a**2) - 2 * sp.log(a)
    probe(expr, (-sp.oo, sp.oo), branch_sensitive, False, "tangent logarithm branch")
    probe(2 * expr, (-sp.oo, sp.oo), sp.pi, False, "tangent numerator")
    probe(expr, (0, sp.oo), sp.pi, False, "tangent lower bound")


def check_closed_answers():
    x = sp.Symbol("x", real=True)
    k = sp.Symbol("k", integer=True, positive=True)
    for answer in (
        sp.Integral(x, (x, 0, 1)),
        sp.Sum(1 / k**2, (k, 1, sp.oo)),
        sp.Product(1 + 1 / k**2, (k, 1, sp.oo)),
        sp.Limit(1 + 1 / k, k, sp.oo),
    ):
        probe(x, (0, 1), answer, False, "unevaluated answer")
    unsupported = sp.Integral(sp.exp(x * k), (k, 0, 1))
    probe(unsupported, (0, 1), sp.Integer(1), False, "unsupported inner integral")
    require(pack_gate.canon_integrand(sp.srepr(unsupported), "x") is None,
            "unsupported canonical inner integral")


def check_answer_preprocessing(rows):
    relay = rows["R2-2025-UK-Relay-Q03"]
    tangent = rows["R2-2025-UK-Group-Q06"]
    m, n = sp.symbols("m n", integer=True, positive=True)
    a = sp.Symbol("a")
    diagonal = 2 * (n + 2026)**2 / (2 * n + 53)
    correct = sp.Piecewise((diagonal, sp.Eq(m, n)), (0, True))
    wrong = sp.Piecewise((diagonal, sp.Eq(m, n)), (sp.Abs(m - n) - (m - n), True))
    abs_link = f"Eq({sp.srepr(wrong)},{sp.srepr(correct)},evaluate=False)"
    log_link = f"Eq({sp.srepr(sp.pi + sp.log(a**2) - 2 * sp.log(a))},pi,evaluate=False)"

    def check_reading(row, reading, expected, label, variable="x"):
        integrand = row["sympy_expr"]
        if variable != "x":
            expr = pack_gate._parse(integrand, "x")
            integrand = sp.srepr(expr.xreplace({sp.Symbol("x", real=True): sp.Symbol(variable, real=True)}))
        require(pack_gate.proven("definite", integrand, row["limits"], reading, variable) is expected,
                label + " proven")
        fields = pack_gate.fields_from_parts(integrand, row["limits"], reading, variable)
        require((fields is not None) is expected, label + " fields")

    check_reading(relay, abs_link, False, "false absolute-value equality")
    check_reading(tangent, log_link, False, "false logarithm equality")
    check_reading(relay, f"Eq({abs_link},{sp.srepr(correct)},evaluate=False)", False,
                  "false nested equality")
    check_reading(relay, abs_link, False, "false equality before dummy renaming", variable="t")
    truthful = "Eq(Eq(pi,2*pi/2,evaluate=False),pi,evaluate=False)"
    check_reading(tangent, truthful, True, "truthful nested equality")
    check_reading(tangent, truthful, True, "truthful equality before dummy renaming", variable="t")
    check_reading(tangent, "pi+C", False, "definite integration constant")
    check_reading(tangent, "Eq(pi+C,pi+C,evaluate=False)", False, "constant in truthful equality")
    require(pack_gate.canon_expr("pi+C", "x", allow_constant=False) is None,
            "definite canonicalization rejects C")
    require(pack_gate.proven("indefinite", "x", None, "x**2/2+C", "x"),
            "indefinite integration constant proven")
    fields = pack_gate.fields_from_parts("x", None, "x**2/2+C", "x")
    require(fields is not None and fields["answer_sympy"] == "x**2/2",
            "indefinite integration constant fields")


def check_source_discrepancy(rows):
    row = rows["R2-2023-Relay-Q19"]
    require(row["verify"] == "manual", "Relay-Q19 must remain manual")
    require("source discrepancy" in row["notes"], "Relay-Q19 source note")
    u = sp.Symbol("u", real=True)
    a = sp.Symbol("a", nonnegative=True)
    n = sp.Symbol("n", integer=True, positive=True)
    remainder = sp.cos(u) - 1 + u**2 / 2
    require(remainder.subs(u, 0) == 0 and sp.diff(remainder, u).subs(u, 0) == 0,
            "cosine bound initial data")
    require(sp.diff(remainder, u, 2) == 1 - sp.cos(u), "cosine bound convexity")
    require(sp.expand((1 - a) * (1 - n * a) - (1 - (n + 1) * a)) == n * a**2,
            "Bernoulli induction")
    require((1 - n * a).subs(a, 1 / (2 * n)) == sp.Rational(1, 2),
            "cosine peak lower bound")
    require(sp.simplify((-sp.cos(u))**(2 * n) - sp.cos(u)**(2 * n)) == 0,
            "even cosine powers")
    require(sp.trigsimp(sp.cos(u + sp.pi) + sp.cos(u)) == 0,
            "cosine peak shift")
    require(sp.limit((2 * n - 1) / (sp.pi * sp.sqrt(2 * n)) - 1, n, sp.oo) == sp.oo,
            "Relay-Q19 even subsequence lower bound")
    require(sp.trigsimp(sp.diff(sp.tan(u) - u, u) - sp.tan(u)**2) == 0,
            "odd subsequence Gaussian domination")
    gaussian = sp.sqrt(n) * sp.integrate(sp.exp(-n * u**2 / 2), (u, 0, sp.oo))
    require(sp.simplify(gaussian - sp.sqrt(sp.pi / 2)) == 0,
            "odd subsequence Gaussian bound")


def main():
    rows = {row["id"]: row for row in problem_catalog.load_records()}
    selected = [rows[ident] for ident in IDS]
    require(all(row["verify"] == "sympy" for row in selected), "five certificate rows")
    require(pack_gate.reprove_rows(selected) is None, "stored certificate rows")
    renamed = dict(selected[0], id="independent-of-catalog-id")
    require(pack_gate.reprove_rows([renamed]) is None, "certificate does not trust the id")
    check_sphere()
    check_grid()
    check_tangent()
    check_closed_answers()
    check_answer_preprocessing(rows)
    check_source_discrepancy(rows)
    print("PASS pack certificates (5 rows, symbolic families, mutations, source discrepancy)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
