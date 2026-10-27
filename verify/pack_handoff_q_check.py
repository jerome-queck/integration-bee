"""Prove the Tournament Q04 family and reject the printed Jacobian error.

Source mutations use the narrow matcher directly, so a rejected product does
not spend an ordinary integrator's timeout. Accepted answers also go through
the public proof gate, catalog field writer, learner grading, and recovery.
"""

from __future__ import annotations

import copy
from pathlib import Path
import sys

import sympy as sp

import pack_gate
import pack_handoff_q
import problem_catalog
import turn_contract


IDS = tuple(f"R3-2024-Tournament-Q04-v{suffix}" for suffix in (10, 11, 12))
PAIRS = ((2, 1), (3, 1), (4, 2), (0, -1), (-1, -2), (1, 0))


def _require(condition, label):
    if not condition:
        raise AssertionError("handoff Q: " + label)


def _source(m, d):
    x = sp.Symbol("x", real=True)
    k = sp.Symbol("k", integer=True)
    # d=m-n is positive, while m (and therefore n=m-d) may be negative.
    expr = (sp.sin((2**m + 2025 * 2**(m-d)) * x) / sp.sin(2**m * x)
            * sp.Product(sp.cos(2**(m-k) * x), (k, 1, d)))
    return expr, x, sp.S.Zero, sp.pi / 2**(m-d)


def _prove(expr, x, lo, hi, answer, expected, label):
    answer_text = answer if isinstance(answer, str) else sp.srepr(answer)
    actual = pack_gate.proven(
        "definite", sp.srepr(expr), (sp.srepr(lo), sp.srepr(hi)), answer_text, x.name
    )
    _require(actual is expected, label)


def _generic_and_concrete():
    m = sp.Symbol("m", integer=True)
    d = sp.Symbol("d", integer=True, positive=True)
    expr, x, lo, hi = _source(m, d)
    value = sp.pi / 2**m
    _require(pack_handoff_q.open_integrand(expr, x), "literal finite product is admitted")
    _require(pack_handoff_q.doubled_sine_product_value(expr, x, lo, hi) == value,
             "generic value follows the source assumptions")
    _prove(expr, x, lo, hi, value, True, "typed generic answer")
    _prove(expr, x, lo, hi, "pi/2**m", True, "ordinary learner parameter spelling")
    _require(pack_handoff_q.definite_answer_ok(expr, x, lo, hi, value) is True,
             "typed answer comparison")

    # The typed printed answer shares the input's actual m,d Symbols. Its
    # rejection cannot be caused merely by different Symbol assumptions.
    for answer, label in (
        (sp.pi / 2**(2*d-m), "typed printed Jacobian"),
        ("pi/2**(m-2*n)", "printed answer in original parameter names"),
        (2 * value, "extra factor two"),
        (value + 1, "added constant"),
        (sp.S.Zero, "zero answer"),
    ):
        _prove(expr, x, lo, hi, answer, False, label)

    for mi, ni in PAIRS:
        concrete = _source(sp.Integer(mi), sp.Integer(mi-ni))
        expected = sp.pi / sp.Integer(2)**mi
        _require(pack_handoff_q.doubled_sine_product_value(*concrete) == expected,
                 f"concrete certificate {(mi, ni)}")
        _prove(*concrete, expected, True, f"concrete proof {(mi, ni)}")
        printed = sp.pi / sp.Integer(2)**(mi-2*ni)
        _prove(*concrete, printed, ni == 0, f"printed formula control {(mi, ni)}")

    return expr, x, lo, hi, m, d


def _source_controls(expr, x, lo, hi, m, d):
    product = next(iter(expr.atoms(sp.Product)))
    k = product.limits[0][0]
    changed_sources = (
        ("overall scale", 2 * expr),
        ("even numerator frequency", expr.xreplace({sp.Integer(2025): sp.Integer(2024)})),
        ("changed source coefficient", expr.xreplace({sp.Integer(2025): sp.Integer(2027)})),
        ("product lower index", expr.xreplace({product: sp.Product(product.function, (k, 0, d))})),
        ("product upper index", expr.xreplace({product: sp.Product(product.function, (k, 1, d+1))})),
        ("product factor exponent", expr.xreplace({product: sp.Product(
            sp.cos(2**(m-k+1) * x), (k, 1, d))})),
        ("gap lacks positivity", expr.xreplace({d: sp.Symbol("d", integer=True)})),
        ("gap lacks integrality", expr.xreplace({d: sp.Symbol("d", positive=True)})),
        ("m lacks integrality", expr.xreplace({m: sp.Symbol("m")})),
    )
    for label, changed in changed_sources:
        _require(changed != expr, label + " actually changes the source")
        _require(not pack_handoff_q.open_integrand(changed, x), label + " is not admitted")
        _require(pack_handoff_q.doubled_sine_product_value(changed, x, lo, hi) is None,
                 label + " cannot inherit the certificate")
    for new_lo, new_hi in ((sp.S.One, hi), (lo, 2*hi), (lo, sp.pi / 2**m)):
        _require(pack_handoff_q.doubled_sine_product_value(expr, x, new_lo, new_hi) is None,
                 "changed outer bounds")
    for mi, di in ((2, 0), (2, -1), (sp.Rational(1, 2), 1), (2, sp.Rational(1, 2))):
        invalid = _source(sp.sympify(mi), sp.sympify(di))
        _require(pack_handoff_q.doubled_sine_product_value(*invalid) is None,
                 f"outside the printed integer domain {(mi, di)}")


def _same_fields(stored, rebuilt):
    for key, value in rebuilt.items():
        if key in {"sympy_expr", "answer_sympy"}:
            # Equal cached Symbols can reorder assumption keywords in srepr.
            if pack_gate._parse(stored.get(key), "x") != pack_gate._parse(value, "x"):
                return False
        elif key == "limits":
            if tuple(pack_gate._parse(part, "x") for part in stored.get(key, ())) != tuple(
                pack_gate._parse(part, "x") for part in value
            ):
                return False
        elif stored.get(key) != value:
            return False
    return True


def _catalog_and_recovery(rows, expr, lo, hi):
    selected = [rows[ident] for ident in IDS]
    for row in selected:
        ident = row["id"]
        _require(row["verify"] == "sympy" and row["kind"] == "definite",
                 ident + " promoted scalar integral")
        _require(pack_gate._parse(row["sympy_expr"], "x") == expr,
                 ident + " retains the literal product and parameter domain")
        _require(tuple(pack_gate._parse(part, "x") for part in row["limits"]) == (lo, hi),
                 ident + " retains the rescaled source bounds")
        _require(pack_gate._parse(row["answer_sympy"], "x") == sp.pi / 2**sp.Symbol("m"),
                 ident + " stores the derived answer in learner notation")
        _require(ident not in problem_catalog.MANUAL_INPUT_KINDS,
                 ident + " no manual-input exception")
        _require("m > n" in row["integrand_plain"] and "sin" in row["integrand_plain"],
                 ident + " shows the full printed problem")
        fields = pack_gate.fields_from_parts(
            row["sympy_expr"], row["limits"], row["answer_sympy"], row["variable"]
        )
        _require(fields is not None and _same_fields(row, fields),
                 ident + " all canonical fields round-trip")
        for answer, correct in (("pi/2**m", True), ("pi/2**(m-2*n)", False)):
            grade, error = turn_contract.grade_problem(ident, answer, None, [], [], [row])
            _require(error is None and grade is not None,
                     ident + " grades a well-formed answer")
            _require(grade["correct"] is correct and grade["manual"] is False,
                     ident + " learner grade: " + answer)
    _require(pack_gate.reprove_rows(selected) is None, "all three stored aliases re-prove")
    renamed = dict(selected[0], id="independent-tournament-q04-certificate")
    _require(pack_gate.reprove_rows([renamed]) is None, "proof does not trust a catalog id")
    wrong = dict(selected[0], answer_sympy="pi/2**(m-2*n)")
    wrong["answer_latex"] = sp.latex(pack_gate._parse(wrong["answer_sympy"], "x"))
    _require(pack_gate.reprove_rows([wrong]) is not None,
             "stored printed answer fails after matching its own latex")

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    import recover_pack_math

    recovered, gated = recover_pack_math.recover(copy.deepcopy(selected))
    _require(set(gated) == set(IDS) and len(recovered) == len(selected),
             "recovery re-proves all three source transcripts")
    for stored, rebuilt in zip(selected, recovered):
        _require(set(stored) == set(rebuilt) and _same_fields(stored, rebuilt),
                 stored["id"] + " recovery preserves every catalog field")


def check(rows):
    expr, x, lo, hi, m, d = _generic_and_concrete()
    _source_controls(expr, x, lo, hi, m, d)
    _catalog_and_recovery(rows, expr, lo, hi)


if __name__ == "__main__":
    check({row["id"]: row for row in problem_catalog.load_records()})
    print("PASS Handoff Q symbolic product, derived answer, mutations, grading, and recovery")
