#!/usr/bin/env python3
"""Reprove the source-backed certificates and reject corrupted readings."""

from __future__ import annotations

import copy
import sys

import sympy as sp

import pack_gate
import pack_handoff_f_check
import pack_handoff_m_check
import pack_handoff_q_check
import pack_grid_check
import problem_catalog
import turn_contract


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


def check_handoff_l(rows):
    # The printed +/-pi/2 endpoints determine the graded value, despite
    # sin(1) in the three 2022 marks. The identical 2020 Q01 supports 1.
    x = sp.Symbol("x", real=True)
    logistic = sp.cos(x) / (1 + sp.exp(x))
    require(sp.simplify(logistic + logistic.subs(x, -x) - sp.cos(x)) == 0,
            "2022 Q01 reflection identity")
    require(sp.integrate(sp.cos(x), (x, -sp.pi / 2, sp.pi / 2)) / 2 == 1,
            "2022 Q01 printed limits give one")
    require(sp.sin(1) < 1, "2022 Q01 printed mark differs")
    ids = ("R1-2022-MIT-TB-Q01", "R1-2022-Oxford-Q01", "R1-2022-TB2022-Q01")
    selected = [rows[ident] for ident in ids]
    for row in selected:
        ident = row["id"]
        require(row["verify"] == "sympy" and row["kind"] == "definite"
                and row["variable"] == "x", ident + " symbolic definite integral")
        require(pack_gate._parse(row["sympy_expr"], "x") == logistic
                and row["limits"] == ["-pi/2", "pi/2"], ident + " printed problem")
        require(all(row[field] == "1" for field in ("answer_plain", "answer_sympy", "answer_latex")),
                ident + " consistent graded final")
        require(row["answer_source_pdf"] == "sources/past/r1/2020/Virtual_integration_competition_answers.pdf"
                and "source discrepancy" in row["notes"] and "sin(1)" in row["notes"],
                ident + " answer authority and conflicting mark")
        require(pack_gate.reprove_rows([row]) is None, ident + " stored reproof")
        require(turn_contract.answer_matches(row, "1"), ident + " learner final")
        for wrong in ("sin(1)", "0", "2", "pi/2"):
            require(not pack_gate.proven(row["kind"], row["sympy_expr"], row["limits"], wrong, "x"),
                    ident + " wrong answer " + wrong)
            require(not turn_contract.answer_matches(row, wrong), ident + " learner wrong answer " + wrong)

    probe(2 * logistic, (-sp.pi / 2, sp.pi / 2), sp.Integer(1), False, "2022 Q01 numerator mutation")
    probe(logistic, (-1, 1), sp.Integer(1), False, "2022 Q01 endpoint mutation")
    probe(logistic, (-1, 1), sp.sin(1), True, "2022 mark matches different endpoints")
    sys.path.insert(0, str(problem_catalog.ROOT / "scripts"))
    import recover_pack_math

    recovered, gated = recover_pack_math.recover(copy.deepcopy(selected))
    require(recovered == selected and set(gated) == set(ids),
            "2022 Q01 recovery preserves the resolved source reading and answer")


def check_source_discrepancy(rows):
    row = rows["R2-2023-Relay-Q19"]
    require(row["verify"] == "sympy", "Relay-Q19 clarified reading is certified")
    require("source discrepancy" in row["notes"], "Relay-Q19 source note")
    require("sqrt(n)-bound clarification" in row["notes"], "Relay-Q19 chosen reading is explicit")
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


def check_hard_open_forms(rows):
    ids = (
        "R2-2024-Relay-Q04",
        "R2-2023-Group-Q07",
        "R2-2025-SG-Group-Q12",
        "R2-2025-UK-Group-Q09",
        "R2-2025-SG-Relay-Q14",
    )
    parsed = {}
    x = sp.Symbol("x", real=True)

    def reject_shape(expr, limits, answer, label):
        require(pack_gate.canon_integrand(sp.srepr(expr), "x") is None,
                label + " canonical integrand")
        probe(expr, limits, answer, False, label + " proof")

    for ident in ids:
        row = rows[ident]
        require(row["verify"] == "sympy", ident + " stored status")
        expr = pack_gate._parse(row["sympy_expr"], row["variable"])
        answer = pack_gate._parse(row["answer_sympy"], row["variable"])
        limits = tuple(pack_gate._parse(bound, row["variable"]) for bound in row["limits"])
        parsed[ident] = expr, limits, answer
        require(expr.free_symbols == {x}, ident + " bound index stays bound")
        fields = pack_gate.fields_from_parts(
            row["sympy_expr"], row["limits"], row["answer_sympy"], row["variable"]
        )
        require(fields is not None, ident + " fields round-trip")
        require(pack_gate._parse(fields["sympy_expr"], fields["variable"]) == expr,
                ident + " literal expression round-trip")
        require(pack_gate._parse(fields["answer_sympy"], fields["variable"]) == answer,
                ident + " answer round-trip")
        require(fields["kind"] == row["kind"] and fields["limits"] == row["limits"],
                ident + " integration bounds round-trip")
        probe(expr, limits, answer, True, ident + " stored proof")
        probe(expr, limits, answer + 1, False, ident + " wrong answer")
        probe(expr, (limits[0] + sp.Rational(1, 3), limits[1]), answer, False,
              ident + " changed lower bound")
        changed_upper = sp.Integer(2) if limits[1] == sp.oo else limits[1] + 1
        probe(expr, (limits[0], changed_upper), answer, False, ident + " changed upper bound")
        reject_shape(expr + 1, limits, answer, ident + " added term")
        reject_shape(2 * expr, limits, answer, ident + " outer scale")

    fraction, limits, answer = parsed["R2-2024-Relay-Q04"]
    first, denominators, numerators, start = fraction.args
    for label, changed in (
        ("continued-fraction denominator", fraction.func(
            first, sp.Lambda(denominators.variables, denominators.expr + 1), numerators, start
        )),
        ("continued-fraction numerator", fraction.func(
            first, denominators, sp.Lambda(numerators.variables, 2 * numerators.expr), start
        )),
        ("continued-fraction starting index", fraction.func(first, denominators, numerators, start + 1)),
    ):
        reject_shape(changed, limits, answer, label)

    maximum, limits, answer = parsed["R2-2023-Group-Q07"]
    function, domain = maximum.args
    reject_shape(maximum.func(sp.Lambda(function.variables, function.expr + 1), domain),
                 limits, answer, "indexed-maximum body")
    reject_shape(maximum.func(function, sp.S.Naturals),
                 limits, answer, "indexed-maximum positive-index domain")

    for ident in ("R2-2025-SG-Group-Q12", "R2-2025-SG-Relay-Q14"):
        series, limits, answer = parsed[ident]
        index, start, stop = series.limits[0]
        reject_shape(sp.Sum(series.function, (index, start + 1, stop)),
                     limits, answer, ident + " changed summation range")
        reject_shape(sp.Sum(series.function + 1, (index, start, stop)),
                     limits, answer, ident + " changed summand")

    for expr, label in ((fraction, "continued fraction"), (maximum, "indexed maximum")):
        require(not pack_gate._closed(expr), label + " remains unevaluated")
        require(pack_gate.fields_from_parts("x", ("0", "1"), sp.srepr(expr), "x") is None,
                label + " rejected as stored answer")
        probe(x, (0, 1), expr, False, label + " rejected as answer")

    row = rows["R3-2024-Chainlink-G3-Q08"]
    expr = pack_gate._parse(row["sympy_expr"], row["variable"])
    answer = pack_gate._parse(row["answer_sympy"], row["variable"])
    limits = tuple(pack_gate._parse(bound, row["variable"]) for bound in row["limits"])
    probe(expr, limits, answer + 1, False, "log-cosine Laplace wrong answer")


def check_handoff_d(rows):
    """Reprove all scalar D rows without erasing their source operations."""
    expected = {
        "R2-2021-Relay-A01": "4",
        "R2-2021-Relay-A02": "2*sqrt(2)",
        "R2-2021-Relay-A03": "pi",
        "R2-2021-Relay-B02": "0",
        "R2-2021-Relay-C01": "0",
        "R2-2021-Relay-C02": "2",
        "R2-2021-Relay-C03": "2",
        "R2-2021-Relay-D02": "1",
        # The input keeps a>0; the displayed output uses the same plain name
        # a that the learner parser receives, without losing that input guard.
        "R2-2022-Relay-Q10": "log(1+a)/a",
        "R2-2022-Relay-Q11": "log(2)",
        "R2-2022-Relay-Q20": "1",
        "R2-2023-Relay-Q02": "pi",
        "R2-2023-Relay-Q05": "17",
        "R2-2023-Relay-Q13": "log(2)",
        "R2-2024-Relay-Q02": "log(2)",
        "R2-2024-Relay-Q03": "Rational(1,2)",
        "R2-2024-Relay-Q06": "2",
        "R2-2024-Relay-Q07": "Rational(1,2)",
        "R2-2024-Relay-Q14": "Rational(2025,2)",
        "R2-2025-SG-Group-Q11": "20",
        "R2-2025-SG-Group-Q13": "1",
        "R2-2025-SG-Group-Q15": "pi/2-1",
        "R2-2025-SG-Relay-Q16": "1999",
        "R2-2025-UK-Relay-Q20": "1999",
    }
    # F proves the answer-schema deferrals, I the Group alias, and M explicitly
    # clarifies/certifies D03 and Q20 in its separate source-bound checks.
    required_shapes = {
        "R2-2022-Relay-Q10": (sp.Integral,),
        "R2-2022-Relay-Q11": (sp.Limit, sp.Integral),
        "R2-2022-Relay-Q20": (sp.Limit, sp.Integral),
        "R2-2023-Relay-Q02": (sp.Limit, sp.Sum),
        "R2-2023-Relay-Q05": (sp.Limit, sp.Integral),
        "R2-2023-Relay-Q13": (sp.Limit, sp.Integral),
        "R2-2024-Relay-Q02": (sp.Limit, sp.Integral, sp.Sum),
        "R2-2024-Relay-Q03": (sp.Sum, sp.KroneckerDelta, sp.floor),
        "R2-2024-Relay-Q06": (sp.Limit, sp.Integral),
        "R2-2024-Relay-Q07": (sp.exp, sp.Integral),
        "R2-2024-Relay-Q14": (sp.Abs, sp.frac),
        "R2-2025-SG-Group-Q11": (sp.Subs, sp.floor, sp.Integral, sp.Sum),
        "R2-2025-SG-Group-Q13": (sp.Subs, sp.ceiling, sp.Integral),
        "R2-2025-SG-Group-Q15": (sp.Sum, sp.Limit, sp.Derivative),
        "R2-2025-SG-Relay-Q16": (sp.Subs, sp.floor, sp.Integral),
        "R2-2025-UK-Relay-Q20": (sp.Subs, sp.floor, sp.Integral),
    }
    modules = {
        "2021": pack_gate.pack_handoff_d_2021,
        "2022": pack_gate.pack_handoff_d_2022,
        "2023": pack_gate.pack_handoff_d_2023,
        "2024": pack_gate.pack_handoff_d_2024_2025,
        "2025": pack_gate.pack_handoff_d_2024_2025,
    }
    selected = [rows[ident] for ident in expected]
    require(len(selected) == 24 and all(row["verify"] == "sympy" for row in selected),
            "Handoff D 24 scalar rows")
    require(pack_gate.reprove_rows(selected) is None, "Handoff D stored-row reproof")
    parsed = {}
    for row in selected:
        ident, variable = row["id"], row["variable"]
        symbol = pack_gate.namespace(variable)[variable]
        expr = pack_gate._parse(row["sympy_expr"], variable)
        answer = pack_gate._parse(expected[ident], variable)
        limits = tuple(pack_gate._parse(part, variable) for part in row["limits"])
        module = modules[ident.split("-")[1]]
        parsed[ident] = (row, expr, symbol, limits, answer, module)
        require(row["kind"] == "definite", ident + " retains scalar answer semantics")
        require(pack_gate._certificate_same(pack_gate._parse(row["answer_sympy"], variable), answer),
                ident + " expected source answer")
        shapes = required_shapes.get(ident, (sp.Subs, sp.Integral))
        require(all(expr.has(shape) for shape in shapes), ident + " original source operations")
        canonical = pack_gate.canon_integrand(row["sympy_expr"], variable)
        require(canonical is not None and pack_gate._parse(canonical, variable) == expr,
                ident + " source shape survives canonicalization")
        require(pack_gate.proven("definite", canonical, row["limits"], expected[ident], variable),
                ident + " positive proof")
        wrong = pack_gate._canonical_text(answer + 1, variable)
        require(not pack_gate.proven("definite", canonical, row["limits"], wrong, variable),
                ident + " wrong answer rejected")
        require(turn_contract.answer_matches(row, expected[ident]), ident + " learner accepts source answer")
        require(not turn_contract.answer_matches(row, wrong), ident + " learner rejects wrong answer")
        # A miss must be rejected before doing certificate work. Direct matcher
        # checks avoid spending a whole proof timeout on unrelated generic
        # integration, especially for the compiled 2025-cell triangle.
        require(module.definite_value(expr, symbol, limits[0] + 1, limits[1]) is None,
                ident + " changed bound metadata")
        require(module.definite_value(2 * expr, symbol, *limits) is None,
                ident + " changed whole expression")
        if expr.has(sp.Subs) and isinstance(expr, sp.Subs):
            if expr.expr.has(sp.floor, sp.ceiling, sp.Mod):
                changed = sp.Subs(expr.expr + 1, expr.variables, expr.point)
                for label, candidate in (("changed rounding", changed),
                                         ("removed rounding", expr.point[0])):
                    require(not pack_gate.proven("definite", sp.srepr(candidate), row["limits"],
                                                 expected[ident], variable), ident + " " + label)
        # All unbounded n families require a positive integer index. Finite
        # sums with explicit integer endpoints need no extra assumptions.
        for index in expr.atoms(sp.Symbol):
            if index.name == "n" and index.is_integer is True and index.is_positive is True:
                changed = expr.xreplace({index: sp.Symbol("n", positive=True)})
                require(not module.open_integrand(changed, symbol), ident + " missing integer assumption")
                break

    row, expr, symbol, limits, answer, module = parsed["R2-2022-Relay-Q10"]
    parameter = next(item for item in expr.free_symbols if item != symbol)
    changed = expr.xreplace({parameter: sp.Symbol(parameter.name)})
    require(not module.open_integrand(changed, symbol), "2022 Q10 keeps positive input parameter")
    require(not pack_gate.proven("definite", sp.srepr(changed), row["limits"], "log(1+a)/a", row["variable"]),
            "2022 Q10 plain output does not weaken input-domain gate")
    require(turn_contract.answer_matches(row, "ln(1+a)/a"), "2022 Q10 natural logarithm alias")

    row, expr, symbol, limits, answer, module = parsed["R2-2023-Relay-Q02"]
    series = next(iter(expr.atoms(sp.Sum)))
    index = series.limits[0][0]
    changed = expr.xreplace({2**index: 2 * index})
    require(changed != expr and not module.open_integrand(changed, symbol),
            "2023 Q02 rejects linear-frequency OCR in place of exponential frequency")
    require(not pack_gate.proven("definite", sp.srepr(changed), row["limits"], "pi", row["variable"]),
            "2023 Q02 linear-frequency reading cannot reuse doubling proof")

    row, expr, symbol, limits, answer, module = parsed["R2-2023-Relay-Q13"]
    require(isinstance(expr, sp.Limit) and isinstance(expr.args[0], sp.Integral),
            "2023 Q13 keeps the full limit of its moving integral")
    integral, endpoint, destination, direction = expr.args
    require(str(direction) == "+-", "2023 Q13 source limit is two-sided")
    variants = (
        ("direction", sp.Limit(integral, endpoint, destination, dir="+"), limits),
        ("power", sp.Limit(sp.Integral(integral.function * sp.sin(symbol),
                                      *integral.limits), endpoint, destination, dir="+-"), limits),
        ("moving bound", sp.Limit(sp.Integral(integral.function, (symbol, endpoint, 3 * endpoint)),
                                  endpoint, destination, dir="+-"), (endpoint, 3 * endpoint)),
    )
    for label, candidate, bounds in variants:
        require(module.definite_value(candidate, symbol, *bounds) is None,
                "2023 Q13 rejects changed " + label)
        require(not module.open_integrand(candidate, symbol), "2023 Q13 closed whitelist for " + label)

    row, expr, symbol, limits, answer, module = parsed["R2-2024-Relay-Q07"]
    integral = expr.point[0] if isinstance(expr, sp.Subs) else expr.args[0]
    require(isinstance(integral, sp.Integral) and module._d25_outer_shape(expr, symbol)[0] == "product",
            "2024 Q07 keeps exp of the literal logarithmic integral")
    require(not pack_gate.proven("definite", sp.srepr(integral), row["limits"], "1/2", row["variable"]),
            "2024 Q07 cannot drop product-integral exponentiation")
    _, triangle, symbol, _, _, _ = parsed["R2-2024-Relay-Q14"]
    require(triangle == sp.Abs(2 * sp.frac(symbol / 2) - 1),
            "2024 Q14 retains the independently checked triangle compilation")


def check_handoff_h_ceiling(rows):
    row = rows["R2-2025-UK-Group-Q10"]
    require(row["verify"] == "sympy" and row["answer_plain"] == "1",
            "UK Group Q10 uses its own mark, not the Relay Q10 OCR")
    expr = pack_gate._parse(row["sympy_expr"], "x")
    x = pack_gate.namespace("x")["x"]
    f = 1 / sp.atan(x) - (1 + x**2) / (1 + sp.atan(x) + x**2 * sp.atan(x))
    require(isinstance(expr, sp.Subs) and expr.expr == sp.ceiling(expr.variables[0]),
            "UK Group Q10 retains the outer ceiling")
    require(expr.point == (sp.Integral(f, (x, 1, sp.oo)),),
            "UK Group Q10 retains the printed integrand and bounds")
    require(row["limits"] == ["1", "oo"], "UK Group Q10 bound metadata")
    fields = pack_gate.fields_from_parts(row["sympy_expr"], row["limits"], "1", "x")
    require(fields is not None and all(row[key] == value for key, value in fields.items()),
            "UK Group Q10 fields round-trip")
    require(pack_gate.reprove_rows([row]) is None, "UK Group Q10 stored proof")
    require(turn_contract.answer_matches(row, "1"), "UK Group Q10 learner answer")
    for answer in ("0", "2", "2/pi", "2025**x*gamma(x+Rational(2026,2025))"):
        require(not pack_gate.proven("definite", row["sympy_expr"], row["limits"], answer, "x"),
                "UK Group Q10 wrong answer: " + answer)
        require(not turn_contract.answer_matches(row, answer),
                "UK Group Q10 learner wrong answer: " + answer)
    module = pack_gate.pack_handoff_d_2024_2025
    placeholder = expr.variables[0]
    for changed, limits in (
        (expr, (0, sp.oo)),
        (sp.Subs(sp.floor(placeholder), placeholder, expr.point[0]), (1, sp.oo)),
        (sp.Subs(sp.ceiling(placeholder), placeholder, sp.Integral(f, (x, 2, sp.oo))), (2, sp.oo)),
        (sp.Subs(sp.ceiling(placeholder), placeholder, sp.Integral(2*f, (x, 1, sp.oo))), (1, sp.oo)),
        (expr.point[0], (1, sp.oo)),
    ):
        require(module.definite_value(changed, x, *limits) is None,
                "UK Group Q10 rejects changed source shape or bounds")


def check_handoff_i(rows):
    """Prove the Group alias; source-conflict manuals are cleared by L–Q."""
    def same_recovery(before, after):
        if len(before) != len(after):
            return False
        for stored, recovered in zip(before, after):
            # Cached equal Symbols can reorder srepr's assumption keywords.
            # Exact parsed equality preserves every operator, bound and
            # assumption; all other catalog fields must be byte-for-byte equal.
            if pack_gate._parse(stored["sympy_expr"], stored["variable"]) != pack_gate._parse(
                recovered["sympy_expr"], recovered["variable"]
            ):
                return False
            if dict(stored, sympy_expr=recovered["sympy_expr"]) != recovered:
                return False
        return True

    group_ids = ("R2-2023-Group-Q01", "R2-2023-Group-Q01-v2")
    x = sp.Symbol("x", real=True)
    group_expr = sp.cos(sp.cos(x)**2)**2 + sp.sin(sp.sin(x)**2)**2
    for ident in group_ids:
        row = rows[ident]
        require(row["verify"] == "sympy" and row["answer_sympy"] == "pi",
                ident + " source-consistent final")
        require(pack_gate._parse(row["sympy_expr"], "x") == group_expr
                and row["limits"] == ["0", "pi"], ident + " printed problem")
        require(pack_gate.reprove_rows([row]) is None, ident + " stored reproof")
        require(turn_contract.answer_matches(row, "pi"), ident + " learner final")
        for wrong in ("0", "1", "2", "pi/2"):
            require(not pack_gate.proven(row["kind"], row["sympy_expr"], row["limits"], wrong, "x"),
                    ident + " wrong answer " + wrong)
            require(not turn_contract.answer_matches(row, wrong), ident + " learner wrong answer " + wrong)

    require(not problem_catalog.MANUAL_INPUT_KINDS,
            "L–Q cleared every pack MANUAL_INPUT_KINDS transcription")
    require(problem_catalog.catalog_problem(list(rows.values())) is None, "Handoff I counts and schema")
    sys.path.insert(0, str(problem_catalog.ROOT / "scripts"))
    import recover_pack_math

    selected = [rows[ident] for ident in group_ids]
    recovered, gated = recover_pack_math.recover(copy.deepcopy(selected))
    require(same_recovery(selected, recovered) and set(gated) == set(group_ids),
            "recovery re-proves both Group twins without inventing manuals")



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
    check_hard_open_forms(rows)
    check_handoff_d(rows)
    pack_handoff_f_check.check(rows)
    pack_handoff_m_check.check(rows)
    pack_grid_check.check_all(list(rows.values()))
    check_handoff_h_ceiling(rows)
    check_handoff_i(rows)
    check_handoff_l(rows)
    pack_handoff_q_check.check(rows)
    print(
        "PASS pack certificates (symbolic families, literal operators, "
        "24 Handoff D rows, 10 Handoff F contracts, Handoff G grids, "
        "Handoff H ceiling, Handoff I Group alias, Handoff L printed limits, "
        "Handoff M clarified Relay readings, Handoff N crossnumber maps, Handoff Q derived final, mutations, source discrepancies)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
