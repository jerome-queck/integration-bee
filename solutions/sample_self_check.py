#!/usr/bin/env python3
"""Check the UK sample-problem catalog rows and their worked notes.

The pack rows in problems/records.jsonl are not rewritten. ``--write-records``
splices only SAMPLE-* lines. Run from the repository root:

    python3 solutions/sample_self_check.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp
import sympy as sp

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))

import pack_gate  # noqa: E402
import problem_catalog  # noqa: E402

SAMPLE = Path(__file__).resolve().parent / "sample"
RECORDS = problem_catalog.RECORDS
FEED = ROOT / "past" / "samples" / "answers_feed.json"
PROBLEMS = problem_catalog.SAMPLE_PROBLEM_PDF
ANSWERS = problem_catalog.SAMPLE_ANSWERS_PDF
SOLUTIONS = problem_catalog.SAMPLE_SOLUTIONS_PDF

# Printed Q15 final. The minus covers the arctan term, and that expression is not an antiderivative.
Q15_PRINTED = "log(x + 1)/3 - (log(x**2 - x + 1) + 2*sqrt(3)*atan((2*x - 1)/sqrt(3)))/6"

ROWS = [
    {
        "id": "SAMPLE-Q01",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "(x**5 - 1)/log(x)",
        "limits": ["0", "1"],
        "answer": "log(6)",
        "integrand_plain": "∫_0^1 (x^5 − 1)/ln x dx",
        "answer_plain": "ln 6",
        "technique_tags": ["dutis"],
        "yang": ["yang:1.20"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints ln 6.",
    },
    {
        "id": "SAMPLE-Q02",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "sin(x)/x",
        "limits": ["0", "oo"],
        "answer": "pi/2",
        "integrand_plain": "∫_0^∞ sin(x)/x dx",
        "answer_plain": "π/2",
        "technique_tags": ["dirichlet"],
        "yang": ["yang:1.20"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints π/2.",
    },
    {
        "id": "SAMPLE-Q03",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "sqrt(sin(x))/(sqrt(sin(x))+sqrt(cos(x)))",
        "limits": ["0", "pi/2"],
        "answer": "pi/4",
        "integrand_plain": "∫_0^(π/2) √(sin x)/(√(sin x)+√(cos x)) dx",
        "answer_plain": "π/4",
        "technique_tags": ["kings-rule", "reflection"],
        "yang": ["yang:1.18"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints π/4.",
    },
    {
        "id": "SAMPLE-Q04",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "log(x)/(x**2+1)",
        "limits": ["0", "oo"],
        "answer": "0",
        "integrand_plain": "∫_0^∞ ln(x)/(x^2+1) dx",
        "answer_plain": "0",
        "technique_tags": ["u-sub", "odd-even"],
        "yang": ["yang:1.11"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints 0.",
    },
    {
        "id": "SAMPLE-Q05",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "log(x)/(x**2-2*x+2)",
        "limits": ["1", "2"],
        "answer": "pi*log(2)/8",
        "integrand_plain": "∫_1^2 ln(x)/(x^2 − 2x + 2) dx",
        "answer_plain": "(π ln 2)/8",
        "technique_tags": ["trig-sub"],
        "yang": ["yang:1.7"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF p. 1 prints (π ln 2)/8. The gate proves the shift and rational reflection equivalent to the tangent reflection in the solutions PDF p. 6.",
    },
    {
        "id": "SAMPLE-Q06",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "log(1-x)/x",
        "limits": ["0", "1"],
        "answer": "-pi**2/6",
        "integrand_plain": "∫_0^1 ln(1−x)/x dx",
        "answer_plain": "−π^2/6",
        "technique_tags": ["series"],
        "yang": ["yang:1.14"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints −π^2/6.",
    },
    {
        "id": "SAMPLE-Q07",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "x**(n-1)*exp(-x)",
        "limits": ["0", "oo"],
        "answer": "gamma(n)",
        "integrand_plain": "∫_0^∞ x^(n−1) e^(−x) dx for positive integers n",
        "answer_plain": "Γ(n) = (n−1)!",
        "technique_tags": ["gamma", "parts"],
        "yang": ["yang:1.6"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints Γ(n)=(n−1)! for positive integers n.",
    },
    {
        "id": "SAMPLE-Q08",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "x**(Symbol('sigma', positive=True)+I*Symbol('tau', real=True))/(exp(x)-1)",
        "limits": ["0", "oo"],
        "answer": "gamma(1+Symbol('sigma', positive=True)+I*Symbol('tau', real=True))*zeta(1+Symbol('sigma', positive=True)+I*Symbol('tau', real=True))",
        "integrand_plain": "∫_0^∞ x^(s−1)/(e^x − 1) dx, Re(s)>1",
        "raw_snippet": "∫_0^∞ x^(s−1)/(e^x − 1) dx",
        "answer_plain": "Γ(s)ζ(s)",
        "technique_tags": ["series", "gamma-zeta"],
        "yang": ["yang:1.14"],
        "answer_source_pdf": ANSWERS,
        "note": (
            "Answers PDF p. 1 prints Γ(s)ζ(s); solutions PDF p. 9 gives the geometric-series/Gamma derivation. "
            "The integral converges absolutely for Re(s)>1. The symbolic fields encode the whole half-plane by "
            "s=1+sigma+i*tau, with sigma>0 and tau real; the gate checks this domain and the series certificate."
        ),
    },
    {
        "id": "SAMPLE-Q09",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "(x-floor(x))/x**4",
        "limits": ["1", "oo"],
        "answer": "Rational(1,2)-zeta(3)/3",
        "integrand_plain": "∫_1^∞ (x − ⌊x⌋)/x^4 dx",
        "answer_plain": "1/2 − ζ(3)/3",
        "technique_tags": ["floor"],
        "yang": ["yang:1.20"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF p. 1 prints 1/2 − ζ(3)/3. The gate proves the floor-piece sum from the solutions PDF p. 10, using the printed problem's lower endpoint 1 throughout.",
    },
    {
        "id": "SAMPLE-Q10",
        "kind": "definite",
        "verify": "sympy",
        "integrand": "(x**3*cos(x/2)+Rational(1,2))*sqrt(4-x**2)",
        "limits": ["-2", "2"],
        "answer": "pi",
        "integrand_plain": "∫_{-2}^{2} (x^3 cos(x/2) + 1/2) √(4−x^2) dx",
        "answer_plain": "π",
        "technique_tags": ["odd-even", "partial-circle"],
        "yang": ["yang:1.3", "yang:1.9"],
        "answer_source_pdf": ANSWERS,
        "note": "The problems PDF multiplies the whole parenthesis by √(4−x^2). Answers PDF prints π.",
    },
    {
        "id": "SAMPLE-Q11",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "1/(1+tan(x))",
        "answer": "x/2 + log(Abs(sin(x) + cos(x)))/2",
        "integrand_plain": "∫ dx/(1+tan x)",
        "answer_plain": "(1/2)(x + ln(sin x + cos x)) + C",
        "technique_tags": ["trig-identities"],
        "yang": ["yang:1.5"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints (1/2)(x + ln(sin x + cos x)) + c.",
    },
    {
        "id": "SAMPLE-Q12",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "sqrt(tan(x))/sin(2*x)",
        "answer": "sqrt(tan(x))",
        "integrand_plain": "∫ √(tan x)/sin(2x) dx",
        "answer_plain": "√(tan x) + C",
        "technique_tags": ["reverse-product", "trig"],
        "yang": ["yang:1.13", "yang:1.5"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints √(tan x), up to a constant.",
    },
    {
        "id": "SAMPLE-Q13",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "1/(1+exp(x))",
        "answer": "-log(1+exp(-x))",
        "integrand_plain": "∫ dx/(1+e^x)",
        "answer_plain": "−ln(1+e^(−x)) + C",
        "technique_tags": ["basic-exp"],
        "yang": ["yang:1.4"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints −ln(1+e^(−x)), up to a constant.",
    },
    {
        "id": "SAMPLE-Q14",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "1/(x*(1+sin(log(x))**2))",
        "answer": "sqrt(2)*atan(sqrt(2)*tan(log(x)))/2 + sqrt(2)*pi*floor(log(x)/pi + 1/2)/2",
        "integrand_plain": "∫ dx/(x (1 + sin(ln x)^2))",
        "answer_plain": "sqrt(2)*atan(sqrt(2)*tan(log(x)))/2 + sqrt(2)*pi*floor(log(x)/pi + 1/2)/2",
        "technique_tags": ["intermediate-u-sub"],
        "yang": ["yang:1.11"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints (1/√2) arctan(√2 tan(ln x)) + c. That formula jumps by -pi/sqrt(2) where ln x = (k+1/2)*pi. The catalog stores the continuous primitive.",
    },
    {
        "id": "SAMPLE-Q15",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "1/(x**3+1)",
        "answer": "-log(x**2 - x + 1)/6 + log(Abs(x + 1))/3 + sqrt(3)*atan(2*sqrt(3)*x/3 - sqrt(3)/3)/3",
        "integrand_plain": "∫ dx/(x^3+1)",
        "answer_plain": "(1/3) ln(x+1) − (1/6) ln(x^2−x+1) + arctan((2x−1)/√3)/√3 + C",
        "technique_tags": ["partial-fractions"],
        "yang": ["yang:1.8"],
        "answer_source_pdf": SOLUTIONS,
        "note": (
            "The answers PDF and the last line of the solutions PDF print a minus sign in front of the arctan term. "
            "That printed expression is not an antiderivative. The previous line of the solutions PDF is the correct split; "
            "finishing its positive arctan integral is the graded answer, marked authored+verified."
        ),
    },
    {
        "id": "SAMPLE-Q16",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "1/(2+sin(x))",
        "answer": "2*sqrt(3)*atan(2*sqrt(3)*tan(x/2)/3 + sqrt(3)/3)/3 + 2*sqrt(3)*pi*floor(x/(2*pi) + 1/2)/3",
        "integrand_plain": "∫ dx/(2+sin x)",
        "answer_plain": "2*sqrt(3)*atan(2*sqrt(3)*tan(x/2)/3 + sqrt(3)/3)/3 + 2*sqrt(3)*pi*floor(x/(2*pi) + 1/2)/3",
        "technique_tags": ["weierstrass"],
        "yang": ["yang:1.16"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints (2/√3) arctan((2 tan(x/2)+1)/√3) + c. That formula jumps by -2*pi/sqrt(3) at odd multiples of pi. The catalog stores the continuous primitive.",
    },
    {
        "id": "SAMPLE-Q17",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "x**(1/log(x))",
        "answer": "E*x",
        "integrand_plain": "∫ x^(1/ln x) dx",
        "answer_plain": "e x + C",
        "technique_tags": ["rewrite-exponent"],
        "yang": [],
        "answer_source_pdf": ANSWERS,
        "note": (
            "The problems PDF prints x^(1/ln x). The solutions PDF shows that this equals e, so the integral is e*x + C. "
            "The answers sheet prints ex+c on one baseline, the product e*x, not e^x. "
            "An earlier feed read the integrand as 1/(x ln x); that reading is withdrawn."
        ),
    },
    {
        "id": "SAMPLE-Q18",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "1/(1-sin(x))",
        "answer": "sec(x)+tan(x)",
        "integrand_plain": "∫ dx/(1−sin x)",
        "answer_plain": "sec x + tan x + C",
        "technique_tags": ["trig-identities"],
        "yang": ["yang:1.5", "yang:1.15"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints sec x + tan x + c.",
    },
    {
        "id": "SAMPLE-Q19",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "x*sqrt((1-x**2)/(1+x**2))",
        "answer": "(sin(acos(x**2))-acos(x**2))/2",
        "integrand_plain": "∫ x √((1−x^2)/(1+x^2)) dx",
        "answer_plain": "(1/2)(sin(arccos(x^2)) − arccos(x^2)) + C",
        "technique_tags": ["trig-sub"],
        "yang": ["yang:1.7"],
        "answer_source_pdf": ANSWERS,
        "note": (
            "Answers PDF p. 1 prints (1/2)(sin(arccos(x^2)) − arccos(x^2)) + c; solutions PDF p. 20 derives it. "
            "The gate proves the derivative identity on the real interior −1<x<1 with the nonnegative square-root branches."
        ),
    },
    {
        "id": "SAMPLE-Q20",
        "kind": "indefinite",
        "verify": "sympy",
        "integrand": "(exp(2*x)+exp(3*x))/(exp(x)+exp(-x))",
        "answer": "exp(x)-atan(exp(x))+sec(atan(exp(x)))**2/2+log(Abs(cos(atan(exp(x)))))",
        "integrand_plain": "∫ (e^(2x)+e^(3x))/(e^x + e^(−x)) dx",
        "answer_plain": "e^x − arctan(e^x) + (1/2) sec^2(arctan(e^x)) + ln|cos(arctan(e^x))| + C",
        "technique_tags": ["basic-exp", "algebra"],
        "yang": ["yang:1.4"],
        "answer_source_pdf": ANSWERS,
        "note": "Answers PDF prints e^x − arctan(e^x) + (1/2) sec^2(arctan(e^x)) + ln|cos(arctan(e^x))| + c.",
    },
]


def _eq(left, right) -> None:
    if sp.simplify(left - right) != 0:
        raise AssertionError(f"{left} != {right}")


def sympy_fields(row: dict) -> dict:
    variable = "x"
    integrand = pack_gate.canon_integrand(row["integrand"], variable)
    answer = pack_gate.canon_expr(row["answer"], variable)
    if integrand is None or answer is None:
        raise AssertionError(f"{row['id']}: canon failed")
    if row["kind"] == "indefinite":
        limits: list[str] = []
        limit_pair = None
    else:
        limits = []
        for item in row["limits"]:
            canon = pack_gate.canon_integrand(item, variable)
            if canon is None:
                raise AssertionError(f"{row['id']}: limit {item}")
            limits.append(canon)
        limit_pair = (limits[0], limits[1])
    if not pack_gate.proven(row["kind"], integrand, limit_pair, answer, variable):
        raise AssertionError(f"{row['id']}: not proved")
    integrand_expr = pack_gate._parse(integrand, variable)
    answer_expr = pack_gate._parse(answer, variable)
    return {
        "verify": "sympy",
        "kind": row["kind"],
        "variable": variable,
        "limits": limits,
        "sympy_expr": integrand,
        "answer_sympy": answer,
        "integrand_latex": sp.latex(integrand_expr),
        "answer_latex": sp.latex(answer_expr),
    }


def build_record(row: dict) -> dict:
    notes = f"Worked solution: solutions/sample/{row['id']}.md. {row['note']}"
    record = {
        "id": row["id"],
        "round": "sample",
        "year": None,
        "region": None,
        "source": "uk_sample",
        "pdf_path": PROBLEMS,
        "pdf_role": "problems",
        "problem_id": row["id"].removeprefix("SAMPLE-"),
        "kind": row["kind"],
        "integrand_plain": row["integrand_plain"],
        "integrand_latex": None,
        "limits": None,
        "answer_plain": row["answer_plain"],
        "answer_latex": None,
        "answer_source_pdf": row["answer_source_pdf"],
        "verify": row["verify"],
        "technique_tags": list(row["technique_tags"]),
        "yang": list(row["yang"]),
        "worked_solution_plain": None,
        "worked_solution_latex": None,
        "worked_solution_origin": "missing",
        "notes": notes,
        "extraction": {
            "confidence": "high",
            "method": "pymupdf",
            "raw_snippet": row.get("raw_snippet", row["integrand_plain"]),
        },
    }
    if row["verify"] == "sympy":
        record.update(sympy_fields(row))
    return record


def build_feed(row: dict, fields: dict | None) -> dict:
    feed = {
        "id": row["id"],
        "verify": row["verify"],
        "kind": row["kind"],
        "answer_display": row["answer_plain"],
        "source": "Integration_bee_sample_problems_answers.pdf",
        "technique_tags": list(row["technique_tags"]),
        "yang": list(row["yang"]),
        "note": row["note"],
    }
    if row["verify"] == "sympy" and fields is not None:
        feed["sympy_expr"] = fields["sympy_expr"]
        feed["answer_sympy"] = fields["answer_sympy"]
        if row["kind"] == "definite":
            feed["limits"] = fields["limits"]
    if row["id"] == "SAMPLE-Q15":
        feed["pdf_answer_suspect"] = True
        feed["answer_pdf_sympy"] = Q15_PRINTED
        feed["answer_display_pdf"] = (
            "(1/3) ln(x+1) − (1/6)(ln(x^2−x+1) + 2√3 arctan((2x−1)/√3)) + C"
        )
        feed["source"] = "UK_University_integration_bee_sample_problems_solutions.pdf"
    return feed


def splice_records(records: list[dict]) -> None:
    text = RECORDS.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        raise AssertionError("catalog file must end with a newline")
    original = text.splitlines()
    kept = [line for line in original if not json.loads(line)["id"].startswith("SAMPLE-")]
    payload = [json.dumps(row, ensure_ascii=False, sort_keys=True) for row in records]
    insert_at = len(kept)
    for index, line in enumerate(kept):
        if json.loads(line)["id"] >= "SAMPLE-Q01":
            insert_at = index
            break
    out = kept[:insert_at] + payload + kept[insert_at:]
    RECORDS.write_text("\n".join(out) + "\n", encoding="utf-8")
    reread = RECORDS.read_text(encoding="utf-8").splitlines()
    pack_after = [line for line in reread if not json.loads(line)["id"].startswith("SAMPLE-")]
    if pack_after != kept:
        raise AssertionError("pack lines changed")


def write_records() -> None:
    records = []
    feed = []
    for row in ROWS:
        fields = sympy_fields(row) if row["verify"] == "sympy" else None
        records.append(build_record(row))
        feed.append(build_feed(row, fields))
    splice_records(records)
    FEED.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    err = problem_catalog.catalog_problem(problem_catalog.load_records())
    if err:
        raise AssertionError(err)
    print(f"spliced {len(records)} sample rows")


def _near(got, target, tol) -> None:
    err = abs(mp.mpf(got) - mp.mpf(target))
    if err >= tol:
        raise AssertionError(f"{got} vs {target}, err {err}")


def _reject_answers(ident: str, answers: tuple[str, ...]) -> None:
    row = next(row for row in ROWS if row["id"] == ident)
    limits = tuple(row["limits"]) if row["kind"] == "definite" else None
    for answer in answers:
        if pack_gate.proven(row["kind"], row["integrand"], limits, answer, "x"):
            raise AssertionError(f"{ident} accepted wrong answer: {answer}")


def check_q05() -> None:
    t = sp.symbols("t", real=True)
    tangent = sp.tan(t)
    half = (1 - tangent) / (1 + tangent)
    # tan(pi/4 - t) rewrites to cot(t + pi/4); the subtraction formula is the identity that closes.
    _eq(sp.simplify(sp.tan(sp.pi / 4 - t) - half), 0)
    _eq(sp.simplify(sp.log(1 + half) - sp.log(2 / (1 + tangent))), 0)
    mp.mp.dps = 20

    def integrand(x):
        return mp.log(x) / (x * x - 2 * x + 2)

    _near(mp.quad(integrand, [1, 2]), mp.pi * mp.log(2) / 8, mp.mpf("1e-12"))
    _reject_answers("SAMPLE-Q05", ("0", "pi/4", "pi*log(2)/4"))


def check_q08() -> None:
    s, k = sp.symbols("s k", positive=True)
    x = sp.symbols("x", positive=True)
    term = sp.integrate(x ** (s - 1) * sp.exp(-k * x), (x, 0, sp.oo))
    _eq(term, sp.gamma(s) / k ** s)
    row = next(row for row in ROWS if row["id"] == "SAMPLE-Q08")
    answer = row["answer"]
    _reject_answers("SAMPLE-Q08", ("0", f"2*({answer})", f"({answer})+1"))


def check_q09() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    x = sp.symbols("x", positive=True)
    piece = sp.simplify(sp.integrate((x - k) / x ** 4, (x, k, k + 1)))
    total = sp.summation(piece, (k, 1, sp.oo))
    _eq(total, sp.Rational(1, 2) - sp.zeta(3) / 3)
    _reject_answers("SAMPLE-Q09", ("0", "Rational(1,2)+zeta(3)/3", "zeta(3)/3"))


def check_q15_printed() -> None:
    variable = "x"
    if pack_gate.proven("indefinite", "1/(x**3+1)", None, Q15_PRINTED, variable):
        raise AssertionError("SAMPLE-Q15 printed final is an antiderivative")


def check_q17_old_reading() -> None:
    x = sp.symbols("x", real=True)
    power = x ** (1 / sp.log(x))
    _eq(sp.simplify(power - sp.E), 0)
    if pack_gate.proven("indefinite", "1/(x*log(x))", None, "E*x", "x"):
        raise AssertionError("e*x differentiates to 1/(x ln x)")
    if pack_gate.proven("indefinite", "x**(1/log(x))", None, "log(Abs(log(x)))", "x"):
        raise AssertionError("ln|ln x| is an antiderivative of x^(1/ln x)")
    if pack_gate.proven("indefinite", "x**(1/log(x))", None, "exp(x)", "x"):
        raise AssertionError("e^x is an antiderivative of x^(1/ln x)")


def check_q19() -> None:
    x = sp.symbols("x", real=True)
    printed = sp.sqrt(1 - x ** 4) / 2 - sp.acos(x ** 2) / 2
    integrand = x * sp.sqrt((1 - x ** 2) / (1 + x ** 2))
    # Sanity probes include both signs and zero; the gate's symbolic
    # certificate, required below, supplies the proof on the full interval.
    for value in (-sp.Rational(4, 5), -sp.Rational(1, 2), sp.S.Zero,
                  sp.Rational(1, 5), sp.Rational(1, 2), sp.Rational(4, 5)):
        gap = sp.diff(printed, x).subs(x, value) - integrand.subs(x, value)
        if abs(complex(sp.N(gap))) > 1e-9:
            raise AssertionError(f"SAMPLE-Q19 derivative gap at {value}")
    if not pack_gate.proven(
        "indefinite",
        "x*sqrt((1-x**2)/(1+x**2))",
        None,
        "sqrt(1-x**4)/2 - acos(x**2)/2",
        "x",
    ):
        raise AssertionError("SAMPLE-Q19 symbolic derivative certificate failed")
    if not pack_gate.proven(
        "indefinite",
        "x*sqrt((1-x**2)/(1+x**2))",
        None,
        "(sin(acos(x**2))-acos(x**2))/2 + C",
        "x",
    ):
        raise AssertionError("SAMPLE-Q19 printed answer with additive C failed")
    _reject_answers("SAMPLE-Q19", (
        "0", "sqrt(1-x**4)/2 + acos(x**2)/2", "sqrt(1-x**4)-acos(x**2)",
    ))


def check() -> None:
    import piecewise_primitive

    piecewise_primitive.must_fail()
    if [row["id"] for row in ROWS] != [f"SAMPLE-Q{i:02d}" for i in range(1, 21)]:
        raise AssertionError("sample table ids")
    records = problem_catalog.load_records()
    err = problem_catalog.catalog_problem(records)
    if err:
        raise AssertionError(err)
    by_id = {row["id"]: row for row in records if row.get("round") == "sample"}
    feed_rows = json.loads(FEED.read_text(encoding="utf-8"))
    feed_by_id = {row["id"]: row for row in feed_rows}
    if len(by_id) != 20 or len(feed_by_id) != 20:
        raise AssertionError("sample count")
    for row in ROWS:
        path = SAMPLE / f"{row['id']}.md"
        text = path.read_text(encoding="utf-8")
        if row["id"] not in text or "SymPy self-check" not in text:
            raise AssertionError(f"{path.name} missing the self-check note")
        stored = by_id[row["id"]]
        if stored.get("verify") != row["verify"]:
            raise AssertionError(f"{row['id']} verify drift")
        if stored.get("answer_plain") != row["answer_plain"]:
            raise AssertionError(f"{row['id']} answer drift")
        if stored.get("integrand_plain") != row["integrand_plain"]:
            raise AssertionError(f"{row['id']} integrand drift")
        feed = feed_by_id[row["id"]]
        if feed.get("verify") != row["verify"]:
            raise AssertionError(f"{row['id']} feed verify drift")
        if row["verify"] == "sympy":
            fields = sympy_fields(row)
            for key, value in fields.items():
                if stored.get(key) != value:
                    raise AssertionError(f"{row['id']} field {key}")
            if feed.get("answer_sympy") != fields["answer_sympy"] or feed.get("sympy_expr") != fields["sympy_expr"]:
                raise AssertionError(f"{row['id']} feed math drift")
        else:
            for key in ("answer_sympy", "sympy_expr", "variable"):
                if key in stored:
                    raise AssertionError(f"{row['id']} stored {key}")
    suspects = [row["id"] for row in feed_rows if row.get("pdf_answer_suspect")]
    if suspects != ["SAMPLE-Q15"]:
        raise AssertionError(f"pdf suspects {suspects}")
    check_q05()
    check_q08()
    check_q09()
    check_q15_printed()
    check_q17_old_reading()
    check_q19()


def main() -> int:
    if "--write-records" in sys.argv:
        write_records()
        return 0
    try:
        check()
    except AssertionError as exc:
        print(f"FAIL sample_self_check {exc}")
        return 1
    print("PASS sample_self_check (20 sample rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
