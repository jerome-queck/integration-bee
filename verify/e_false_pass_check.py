#!/usr/bin/env python3
"""Must-fail regressions for audit finding E.

Each case calls the checker that owns the false pass. Exit 1 while that
checker still accepts the bad input. Exit 0 once the checker rejects it.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [
    str(ROOT / "verify"),
    str(ROOT / "verify" / "audit" / "confirm125"),
    str(ROOT / "solutions"),
    str(ROOT / "scripts"),
]


def fail(message: str) -> int:
    print(f"FAIL {message}")
    return 1


def ok(message: str) -> int:
    print(f"PASS {message}")
    return 0


def test_pack_gate_abs_primitive() -> int:
    import pack_gate

    if pack_gate.proven("indefinite", "Abs(x)", None, "x**2/2", "x"):
        return fail("pack_gate.proven accepted x**2/2 as a primitive of Abs(x)")
    if not pack_gate.proven("indefinite", "Abs(x)", None, "x*Abs(x)/2", "x"):
        return fail("pack_gate.proven rejected x*Abs(x)/2")
    return ok("pack_gate primitive of |x|")


def test_indefinite_sample_zeros() -> int:
    import sympy as sp

    import pack_gate

    x = pack_gate.namespace("x")["x"]
    # (1-sign(x)) is 0 for x>0. The polynomial is 0 at the six fixed probes
    # ±1/2, ±1, ±2, so those samples are 0 = 0 for the answer 0.
    integrand = (1 - sp.sign(x)) * (
        (x + 2) * (x + 1) * (x + sp.Rational(1, 2))
        * (x - sp.Rational(1, 2)) * (x - 1) * (x - 2)
    )
    if pack_gate._positive_domain_derivative(sp.Integer(0), integrand, x):
        return fail("indefinite sample check accepted 0 at the six rational roots")
    text = (
        "(1-sign(x))*((x+2)*(x+1)*(x+Rational(1,2))"
        "*(x-Rational(1,2))*(x-1)*(x-2))"
    )
    if pack_gate.proven("indefinite", text, None, "0", "x"):
        return fail("pack_gate.proven accepted 0 for the sign-polynomial integrand")
    poly = (
        (x + 2) * (x + 1) * (x + sp.Rational(1, 2))
        * (x - sp.Rational(1, 2)) * (x - 1) * (x - 2)
    )
    primitive = sp.integrate(poly, x)
    if not pack_gate._positive_domain_derivative(primitive, poly, x):
        return fail("symbolic derivative path rejected a polynomial antiderivative")
    if pack_gate._positive_domain_derivative(sp.Integer(0), poly, x):
        return fail("sample zeros accepted 0 for a polynomial that is not identically 0")
    q09 = None
    for line in (ROOT / "problems" / "records.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row["id"] == "R1-2021-Q09":
            q09 = row
            break
    if q09 is None:
        return fail("R1-2021-Q09 missing")
    q09_integrand = pack_gate._parse(q09["sympy_expr"], "x")
    q09_answer = pack_gate._answer_expr(q09["answer_sympy"], "x", allow_constant=True)
    if not pack_gate._positive_domain_derivative(q09_answer, q09_integrand, x):
        return fail("positive-domain samples rejected R1-2021-Q09")
    if pack_gate._positive_domain_derivative(x**2 / 2, sp.Abs(x), x):
        return fail("positive-domain samples accepted x**2/2 for Abs(x)")
    return ok("indefinite samples do not pass on zeros")


def test_q32_real_coeff() -> int:
    import sympy as sp

    import pack_gate

    x = pack_gate.namespace("x")["x"]

    def one_sided(coeff):
        return pack_gate._cosine_over_square((1 - sp.cos(coeff * x)) / x**2, x, 0, sp.oo)

    bare = sp.symbols("a")
    got = one_sided(bare)
    if got is not None and (
        got == sp.pi * sp.Abs(bare) / 2 or sp.simplify(got - sp.pi * sp.Abs(bare) / 2) == 0
    ):
        return fail("Q32 certificate accepted pi*Abs(a)/2 when a is not known to be real")
    if got is not None:
        return fail(f"Q32 certificate returned {got} for a symbol with no reality assumption")
    complex_a = sp.symbols("ac", complex=True)
    if one_sided(complex_a) is not None:
        return fail("Q32 certificate accepted a complex coefficient")
    real = sp.symbols("ar", real=True)
    got = one_sided(real)
    if got is None or sp.simplify(got - sp.pi * sp.Abs(real) / 2) != 0:
        return fail("Q32 certificate rejected pi*Abs(a)/2 for a real coefficient")
    positive = sp.symbols("ap", positive=True)
    got = one_sided(positive)
    if got is None or sp.simplify(got - sp.pi * positive / 2) != 0:
        return fail("Q32 certificate rejected pi*a/2 for a positive coefficient")
    negative = sp.symbols("an", negative=True)
    got = one_sided(negative)
    if got is None or sp.simplify(got - sp.pi * (-negative) / 2) != 0:
        return fail("Q32 certificate rejected pi*|a|/2 for a negative coefficient")
    if pack_gate._cosine_over_square(sp.Integer(0), x, 0, sp.oo) != 0:
        return fail("Q32 certificate rejected the zero integrand")
    return ok("Q32 certificate requires a real coefficient")


def test_worked_log_square_step() -> int:
    import sympy as sp

    import yang_worked_check as ywc

    negative = {"kind": "definite", "limits": ["-2", "-1"], "variable": "x"}
    try:
        ywc.run_step("REGRESS", ("eq", "log(x**2)", "2*log(x)"), sp.Integer(1), negative)
    except AssertionError:
        pass
    else:
        return fail("run_step accepted log(x**2) = 2*log(x) on [-2, -1]")
    positive = {"kind": "definite", "limits": ["1", "2"], "variable": "x"}
    try:
        ywc.run_step("REGRESS", ("eq", "log(x**2)", "2*log(x)"), sp.Integer(1), positive)
    except AssertionError:
        return fail("run_step rejected log(x**2) = 2*log(x) on [1, 2]")
    return ok("run_step log square respects the interval")


def test_logs_equivalent_square() -> int:
    import sympy as sp

    import pack_gate

    real = sp.Symbol("x", real=True)
    if pack_gate._logs_equivalent(sp.log(real**2), 2 * sp.log(real)):
        return fail("_logs_equivalent accepted log(x**2) = 2*log(x) for real x")
    positive = sp.Symbol("p", positive=True)
    if not pack_gate._logs_equivalent(sp.log(positive**2), 2 * sp.log(positive)):
        return fail("_logs_equivalent rejected log(p**2) = 2*log(p) for positive p")
    return ok("_logs_equivalent log square")


def test_grader_stated_assumptions() -> int:
    import json

    import turn_contract

    rows = {}
    for line in (ROOT / "problems" / "records.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[row["id"]] = row
    q32 = rows["R1-2021-Q32"]
    q27 = rows["R1-2021-Q27"]
    if "grading-assumptions:" not in q32["notes"] or "grading-assumptions:" not in q27["notes"]:
        return fail("Q27 or Q32 does not state grading assumptions")
    if not turn_contract.answer_matches(q32, "pi*(b-a)/2"):
        return fail("grader rejected pi*(b-a)/2 for Q32 under a>0, b>0")
    if not turn_contract.answer_matches(q32, "-pi*Abs(a)/2 + pi*Abs(b)/2"):
        return fail("grader rejected the stored Q32 value")
    if turn_contract.answer_matches(q32, "pi*(a-b)/2"):
        return fail("grader accepted the negated Q32 value")
    if not turn_contract.answer_matches(q27, "pi*exp(-a*b)/(2*b)"):
        return fail("grader rejected pi*exp(-a*b)/(2*b) for Q27 under a>0, b>0")
    if not turn_contract.answer_matches(q27, "pi*exp(-Abs(a*b))/(2*Abs(b))"):
        return fail("grader rejected the stored Q27 value")
    if turn_contract.answer_matches(q27, "pi*exp(a*b)/(2*b)"):
        return fail("grader accepted the sign-flipped Q27 value")
    bare = dict(q32)
    bare["notes"] = "Real parameters: pi*(Abs(b)-Abs(a))/2."
    if turn_contract.answer_matches(bare, "pi*(b-a)/2"):
        return fail("grader assumed positivity the row did not state")
    return ok("grader uses stated assumptions")


def test_numeric_fallback_tol() -> int:
    import check_math

    loose = {
        "id": "REGRESS-TOL",
        "kind": "definite",
        "sympy_expr": "1",
        "answer_sympy": "1 + Rational(1, 2000000)",
        "limits": ["0", "1"],
    }
    try:
        check_math.check_drill(loose)
    except AssertionError:
        pass
    else:
        return fail("numeric fallback accepted an answer off by 5e-7")
    exact = dict(loose)
    exact["answer_sympy"] = "1"
    try:
        check_math.check_drill(exact)
    except AssertionError as exc:
        return fail(f"numeric fallback rejected the exact value: {exc}")
    return ok("numeric fallback rejects 5e-7")


def test_primitive_abs() -> int:
    import sympy as sp

    import check_math

    x = check_math.NS["x"]
    if check_math.is_antiderivative(x**2 / 2, sp.Abs(x)):
        return fail("primitive of |x|: x**2/2 was accepted")
    if not check_math.is_antiderivative(x * sp.Abs(x) / 2, sp.Abs(x)):
        return fail("primitive of |x|: the real primitive was rejected")
    return ok("primitive of |x|")


def test_exp_2pii() -> int:
    import sympy as sp

    import pack_gate

    if pack_gate._logs_equivalent(sp.Integer(0), 2 * sp.pi * sp.I):
        return fail("exp shortcut accepted a difference of 2*pi*I")
    x = sp.symbols("x", positive=True)
    if pack_gate._log_identity(sp.log(x), sp.log(x) + 2 * sp.pi * sp.I):
        return fail("exp shortcut accepted log(x) and log(x)+2*pi*I")
    if not pack_gate._logs_equivalent(sp.log(x) - sp.log(x + 1), sp.log(x / (x + 1))):
        return fail("exp shortcut rejected a real logarithm identity")
    if pack_gate._log_identity(sp.log(3), sp.log(3) + 2 * sp.pi * sp.I):
        return fail("exp shortcut accepted constants log(3) and log(3)+2*pi*I")
    if not pack_gate._log_identity(sp.log(2) / 2 + sp.log(sp.Rational(3, 2)) / 2, sp.log(sp.sqrt(3))):
        return fail("exp shortcut rejected a real constant logarithm identity")
    return ok("exp shortcut 2*pi*I")


def test_zero_log_square() -> int:
    import sympy as sp

    import pack_gate

    # log(x**2) = 2*log(x) is false for real x < 0: at x = -1 the left side
    # is 0 and the right side is 2*pi*I.
    x = sp.Symbol("x", real=True)
    if pack_gate._zero(sp.log(x**2) - 2 * sp.log(x)):
        return fail("_zero accepted log(x**2) = 2*log(x) for real x")
    p = sp.Symbol("p", positive=True)
    if not pack_gate._zero(sp.log(p**2) - 2 * sp.log(p)):
        return fail("_zero rejected log(p**2) = 2*log(p) for positive p")
    return ok("_zero log square on real x")


def test_worked_log_split_domain() -> int:
    import sympy as sp

    import pack_gate
    import yang_worked_check as ywc

    x = pack_gate.namespace("x")["x"]
    left, right = sp.log(x**2), 2 * sp.log(x)
    negative = {"kind": "definite", "limits": ["-2", "-1"], "variable": "x"}
    if ywc._log_split_on_interval(left, right, negative):
        return fail("worked check split log(x**2) = 2*log(x) on (-2, -1)")
    positive = {"kind": "definite", "limits": ["1", "2"], "variable": "x"}
    if not ywc._log_split_on_interval(left, right, positive):
        return fail("worked check rejected log(x**2) = 2*log(x) on (1, 2)")
    return ok("worked-step log split needs positive bases")


def test_symmetry_pv() -> int:
    import pack_gate

    x = pack_gate.namespace("x")["x"]
    values = pack_gate._reduced_integrals(1 / x, x, -1, 1)
    if any(value == 0 for value in values):
        return fail("symmetry reduction accepted the Cauchy principal value of 1/x on [-1, 1]")
    return ok("symmetry PV 1/x")


def test_floor_cell() -> int:
    import sympy as sp

    import pack_gate

    x = pack_gate.namespace("x")["x"]
    integrand = sp.sign(x - sp.floor(x) - sp.Rational(1, 2))
    got = pack_gate._floor_sum(integrand, x, 0, sp.oo)
    if got == 0:
        return fail("floor whole-cell sum accepted a non-convergent integral as 0")
    return ok("floor whole-cell sum")


def test_arctan_square() -> int:
    import sympy as sp

    import pack_gate

    z = sp.symbols("z")
    folded = pack_gate._fold_inverse_complements(sp.atan(z**2) + sp.atan(1 / z**2))
    if folded == sp.pi / 2 or sp.simplify(folded - sp.pi / 2) == 0:
        return fail("complex square was folded to +pi/2")
    real = sp.symbols("xr", real=True)
    kept = sp.simplify(pack_gate._fold_inverse_complements(sp.atan(real**2) + sp.atan(1 / real**2)))
    if kept != sp.pi / 2:
        return fail("real square lost the positive arctangent complement")
    # cot(t)**2 for real t is real off its poles (R1-2020-Q27 needs this).
    pole = sp.simplify(pack_gate._fold_inverse_complements(sp.atan(sp.cot(real) ** 2) + sp.atan(1 / sp.cot(real) ** 2)))
    if pole != sp.pi / 2:
        return fail("extended-real square lost the positive arctangent complement")
    if pack_gate._even_power(sp.Pow(sp.S(0), 2, evaluate=False)) or pack_gate._even_power((sp.I * real) ** 2):
        return fail("zero or imaginary base counted as a positive square")
    return ok("complex-square arctan sign")


def test_display() -> int:
    import answer_plain_check as plain

    points = plain.POINTS
    vanish = f"(x-({points[0]}))*(x-({points[1]}))*(x-({points[2]}))"
    rows = {
        "blank": {"answer_plain": "   ", "answer_sympy": "1", "kind": "definite"},
        "1=2": {"answer_plain": "1=2", "answer_sympy": "1", "kind": "definite"},
        "a+b": {"answer_plain": "a + b", "answer_sympy": "2*a", "kind": "definite"},
        "sample-point": {
            "answer_plain": f"x + {vanish}",
            "answer_sympy": "x",
            "kind": "definite",
        },
        "abs-mixed": {
            "answer_plain": "pi*exp(-a*b)/(2*b)",
            "answer_sympy": "pi*exp(-Abs(a*b))/(2*Abs(b))",
            "kind": "definite",
        },
    }
    for name, row in rows.items():
        if not plain.check_row(row):
            return fail(f"display checker accepted {name}")
    kept = {
        "answer_plain": "pi*exp(-Abs(a*b))/(2*Abs(b))",
        "answer_sympy": "pi*exp(-Abs(a*b))/(2*Abs(b))",
        "kind": "definite",
    }
    if plain.check_row(kept):
        return fail("display checker rejected the absolute-value spelling")
    return ok("display checker")


def test_yang_sampler() -> int:
    import yang_worked_check as yang

    bad = yang.real_domain_failures(
        {"variable": "x", "sympy_expr": "log(-1-x**2)", "answer_sympy": "999"}
    )
    if not bad:
        return fail("Yang sampler accepted zero valid samples")
    return ok("Yang sampler zero valid samples")


def test_worked_999() -> int:
    import sympy as sp

    import yang_worked_check as yang

    try:
        yang.run_step("REGRESS", ("eq", "999", "999"), sp.Integer(1))
    except AssertionError:
        return ok("worked-step 999=999")
    return fail("worked step accepted 999=999")


def test_near_nan() -> int:
    import mpmath as mp

    modules = [
        "pack_checks",
        "pack_checks_r1_rem",
        "pack_checks_r1_wave3",
        "pack_checks_r3_dichotomy",
        "pack_checks_wave",
        "sample_self_check",
        "self_check",
    ]
    accepted = []
    for name in modules:
        module = __import__(name)
        try:
            module._near(mp.nan, mp.nan, mp.mpf("1e-6"))
            module._near(mp.nan, 1, mp.mpf("1e-6"))
        except AssertionError:
            continue
        accepted.append(name)
    if accepted:
        return fail("_near accepted NaN in " + ", ".join(accepted))
    return ok("seven _near reject NaN")


def test_sanity_real() -> int:
    import sympy as sp

    import solution_sanity

    x = sp.symbols("x", real=True)
    status, _why, _free = solution_sanity.definite(
        {
            "kind": "definite",
            "variable": "x",
            "sympy_expr": "1",
            "answer_sympy": "1+I",
            "limits": ["0", "1"],
        },
        x,
    )
    if status == "CONFIRMED":
        return fail("solution_sanity confirmed an answer whose imaginary part is 1")
    return ok("solution_sanity real-part only")


def test_confirm125() -> int:
    import confirm125

    rows = {}
    for line in (ROOT / "problems" / "records.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[row["id"]] = row
    ident = "R1-2020-Q16"
    swapped = dict(rows[ident])
    swapped["sympy_expr"] = "0"
    rejected = False
    if hasattr(confirm125, "rejects_unbound_expression"):
        rejected = bool(confirm125.rejects_unbound_expression(ident, swapped))
    if not rejected:
        return fail("confirm125 accepted an id-keyed check after sympy_expr was replaced")
    if confirm125.rejects_unbound_expression(ident, rows[ident]):
        return fail("confirm125 rejected the stored expression for its id")
    return ok("confirm125 expression binding")


def test_inventory_ci() -> int:
    spec = importlib.util.spec_from_file_location("check_ci", ROOT / "scripts" / "check_ci.py")
    if spec is None or spec.loader is None:
        return fail("could not load scripts/check_ci.py")
    check_ci = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check_ci)
    if check_ci.workflow_runs_make_check("# run: make check\n"):
        return fail("CI comment was treated as a make check step")
    import all_rounds_check

    if not hasattr(all_rounds_check, "inventory_problem"):
        return fail("empty inventory, invalid status, and schema are not checked")
    if not all_rounds_check.inventory_problem({"artifacts": [], "counts": {}}):
        return fail("empty inventory accepted")
    invalid_status = {
        "artifacts": [
            {
                "round": "r1",
                "year": "2020",
                "region": None,
                "file": "a.pdf",
                "path": "sources/past/a.pdf",
                "bytes": 1,
                "role": "problems",
                "present": "missing",
                "source": "x",
            }
        ],
        "counts": {"total_pdfs": 1, "by_round": {"r1": 1, "r2": 0, "r3": 0}},
    }
    if not all_rounds_check.inventory_problem(invalid_status):
        return fail("invalid inventory status accepted")
    if not all_rounds_check.inventory_problem({"artifacts": [{"present": True}], "counts": {}}):
        return fail("inventory schema accepted a row with missing fields")
    real = json.loads((ROOT / "past" / "inventory.json").read_text(encoding="utf-8"))
    if all_rounds_check.inventory_problem(real):
        return fail(f"real inventory rejected: {all_rounds_check.inventory_problem(real)}")
    return ok("inventory and CI comments")


def test_empty_notes() -> int:
    import never_impossible_check as notes

    planted = [(f"solutions/pack/empty-{i}.md", "") for i in range(549)]
    planted += [(f"solutions/yang/empty-{i}.md", "") for i in range(3)]
    found = notes.scan([], planted)
    if not found:
        return fail("549 empty pack notes and 3 empty Yang notes passed")
    return ok("empty pack and Yang notes")

CASES = {
    "pack-gate-abs": test_pack_gate_abs_primitive,
    "indefinite-sample-zeros": test_indefinite_sample_zeros,
    "q32-real-coeff": test_q32_real_coeff,
    "worked-log-square-step": test_worked_log_square_step,
    "logs-equivalent-square": test_logs_equivalent_square,
    "grader-assumptions": test_grader_stated_assumptions,
    "numeric-fallback": test_numeric_fallback_tol,
    "primitive-abs": test_primitive_abs,
    "exp-2pii": test_exp_2pii,
    "zero-log-square": test_zero_log_square,
    "worked-log-split": test_worked_log_split_domain,
    "symmetry-pv": test_symmetry_pv,
    "floor-cell": test_floor_cell,
    "arctan-square": test_arctan_square,
    "display": test_display,
    "yang-sampler": test_yang_sampler,
    "worked-999": test_worked_999,
    "near-nan": test_near_nan,
    "sanity-real": test_sanity_real,
    "confirm125-id": test_confirm125,
    "inventory-ci": test_inventory_ci,
    "empty-notes": test_empty_notes,
}


def main(argv: list[str]) -> int:
    names = argv or list(CASES)
    unknown = [name for name in names if name not in CASES]
    if unknown:
        print("unknown " + ", ".join(unknown), file=sys.stderr)
        return 2
    status = 0
    for name in names:
        status = CASES[name]() or status
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
