#!/usr/bin/env python3
"""Recover pack integrand and answer readings from the committed PDFs.

The script rewrites problems/records.jsonl only for rows whose layout reading
is proved by SymPy. Every other row stays manual or unchecked. Run it again
after a parser change. It is deterministic. R1-2024-Q01 stays manual: it is
the cited example of a mark-scheme verdict.

PyMuPDF is required for this script. The catalog check does not import it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))

import pack_gate  # noqa: E402
import pdf_math  # noqa: E402
import problem_catalog  # noqa: E402


def problem_number(row: dict) -> int | None:
    label = str(row.get("problem_id") or "")
    if len(label) < 2 or not label[1:].isdigit():
        return None
    return int(label[1:])


def load_pair(cache: dict, pdf: str, kind: str):
    key = (kind, pdf)
    if key not in cache:
        path = ROOT / pdf
        if not path.is_file():
            cache[key] = None
        elif kind == "problem":
            cache[key] = pdf_math.integral_readings(str(path))
        else:
            cache[key] = pdf_math.answer_readings(str(path))
    return cache[key]


GATED_ROUNDS = frozenset({"r1", "r2", "r3"})
# The turn contract and the catalog pin use this row as the manual mark example.
HELD_MANUAL = frozenset({"R1-2024-Q01"})
# Layout readings that do not prove. Each triple is the printed integrand, its
# limits (None when indefinite), and the printed final, taken from the worked
# note that cites the mark scheme. proven() still has to accept the triple.
TRANSCRIPTS = {
    "R1-2020-Q10": ("sqrt(log(9-x))/(sqrt(log(9-x))+sqrt(log(x+3)))", ("2", "4"), "1"),
    "R1-2020-Q11": (
        "(3*x**10+2*x**8-2)*(x**10+x**8+1)**(Rational(1,4))/x**6",
        None,
        "2*(x**6+x**4+x**(-4))**(Rational(5,4))/5",
    ),
    "R1-2020-Q13": (
        "sqrt(1+exp(x))",
        None,
        "log(Abs((sqrt(1+exp(x))-1)/(sqrt(1+exp(x))+1)))+2*sqrt(1+exp(x))",
    ),
    "R1-2020-Q15": (
        "1/sqrt(1+exp(2*x))",
        None,
        "log((sqrt(1+exp(2*x))-1)/(sqrt(1+exp(2*x))+1))/2",
    ),
    "R1-2020-Q18": (
        "1/(2+2*sin(x)+cos(x))",
        None,
        "log(Abs((tan(x/2)+1)/(tan(x/2)+3)))",
    ),
    "R1-2020-Q31": ("sqrt(1+sin(x/2))", None, "4*(sin(x/4)-cos(x/4))"),
    "R1-2021-Q15": ("1/(csc(x)+1)", None, "x - 2*sin(x/2)/(sin(x/2)+cos(x/2))"),
    "R1-2021-Q37": ("sin(x)*cos(x)*(cos(x)-sin(x))", ("0", "pi/2"), "0"),
    "R1-2021-Q39": ("1/(sin(x)**4+cos(x)**4)", None, "atan(tan(2*x)/sqrt(2))/sqrt(2)"),
    "R1-2022-MIT-TB-Q22": ("cos(x)**2022", ("0", "2*pi"), "pi*binomial(2022, 1011)/2**2021"),
    "R1-2022-Q21": ("sqrt(log(x)+1)/x**2", ("exp(-1)", "oo"), "E*sqrt(pi)/2"),
    "R1-2022-Q23": ("(1/x-1)**(Rational(1,4))", ("0", "1"), "pi/(2*sqrt(2))"),
    "R1-2023-Q17": ("exp(asec(sqrt(x)))/(x*sqrt(x))", ("1", "oo"), "exp(pi/2)+1"),
    "R1-2023-Q21": (
        "2023**x/(2023**x+2024**x)",
        None,
        "x - log(1+(2024/2023)**x)/log(2024/2023)",
    ),
    "R1-2024-Q09": ("1/(1+sqrt(1-sin(x)**2))", ("0", "2*pi"), "4"),
    "R1-2025-Online-Q05": ("cos(x)/(1+exp(1/x))", ("-pi/2", "pi/2"), "1"),
    "R1-2025-Online-Q06": ("sqrt(-log(x))", ("0", "1"), "sqrt(pi)/2"),
    "R1-2021-Q03": (
        "sqrt(cos(x))/(sqrt(cos(x))+sqrt(sin(x)))**5",
        ("0", "pi/2"),
        "1/6",
    ),
    "R1-2020-Q05": (
        "sqrt(tan(x))",
        None,
        "sqrt(2)/4*(log(Abs((tan(x)-sqrt(2*tan(x))+1)/(tan(x)+sqrt(2*tan(x))+1)))+2*atan(sqrt(2*tan(x))-1)+2*atan(sqrt(2*tan(x))+1))",
    ),
    "R1-2021-Q02": ("cos(x)**420", ("0", "2*pi"), "pi*binomial(420, 210)/2**419"),
    "R1-2021-Q26": (
        "(x-x*log(x)+1)/(x*(x+1)**2+x*log(x)**2)",
        ("1", "E"),
        "acot(1+E)",
    ),
    "R1-2021-Q31": ("1/(1+floor(1/x))", ("0", "1"), "2-pi**2/6"),
    "R1-2022-Oxford-Q15": (
        "x**(2*n)*exp(-x**2)",
        ("0", "oo"),
        "factorial(2*n)*sqrt(pi)/(4**n*factorial(n)*2)",
    ),
    "R1-2022-Oxford-Q16": ("(sqrt(x)-x)**(Rational(3, 2))", ("0", "1"), "3*pi/128"),
    "R1-2022-Q05": ("1/x-floor(1/x)", ("0", "1"), "1-EulerGamma"),
    "R1-2022-Q15": (
        "cos(x)**2*(1+cos(x))/(1+cos(x)+sin(x))**2",
        ("0", "pi/2"),
        "(pi-2)/4",
    ),
    "R1-2022-Q16": ("(x-floor(x))/x**2", ("1", "oo"), "1-EulerGamma"),
    "R1-2022-TB2022-Q12": (
        "x**(2*n)*exp(-x**2)",
        ("0", "oo"),
        "factorial(2*n)*sqrt(pi)/(4**n*factorial(n)*2)",
    ),
    "R1-2023-Q09": ("(-(x-floor(x)))**floor(x)", ("0", "oo"), "log(2)"),
    "R1-2023-Q20": (
        "4**(4**x/(2+4**x))/(2+4**(4**x/(2+4**x)))",
        ("Rational(1, 4)", "Rational(3, 4)"),
        "Rational(1, 4)",
    ),
    "R1-2024-Q07": (
        "x**(Rational(1, 3))*floor(1/x**(Rational(1, 3)))",
        ("0", "1"),
        "pi**4/120",
    ),
    "R1-2024-Q20": (
        "x**(x-floor(x)-1)*(log(x**x)+(x-floor(x)))",
        ("0", "100"),
        "4950",
    ),
    "R1-2024-Q22": (
        "(atan(x/a)+atan(x/b))/x",
        ("a", "b"),
        "pi*log(b/a)/2",
    ),
    "R1-2024-Q27": ("exp(-x-1/x)/sqrt(x)", ("0", "oo"), "sqrt(pi)/exp(2)"),
    "R1-2024-Q30": ("acosh(sin(x)+cos(x))", ("0", "pi/2"), "pi*log(2)/2"),
    "R1-2025-Online-Q10": ("atan(b*sin(x))/sin(x)", ("0", "pi/2"), "pi*asinh(b)/2"),
    "R1-2025-Online-Q27": (
        "2**x/((1+sqrt(3))**x+(2+sqrt(3))**x)",
        None,
        "((sqrt(3)-1)**x-log(1+(sqrt(3)-1)**x))/log(sqrt(3)-1)",
    ),
    "R2-2021-Group-Q03": ("1/(2+cos(x))**3", ("0", "pi"), "pi/(2*sqrt(3))"),
    "R2-2021-Group-Q10": ("sin(x**2)", ("0", "oo"), "sqrt(pi/2)/2"),
    "R2-2022-Group-Q04": ("1/(sin(x)+cos(x))**2", ("0", "pi/2"), "1"),
    "R2-2022-Group-Q06": ("1/(x+sqrt(1+x**2))**2", ("0", "oo"), "Rational(2, 3)"),
    "R2-2023-Relay-Q14": ("exp(x+exp(x))", ("0", "1"), "exp(E)-E"),
    "R2-2024-Group-Q04": ("atan(sin(x))/sin(x)", ("0", "pi/2"), "pi*log(1+sqrt(2))/2"),
    "R2-2024-Relay-Q01": (
        "x**2*cos(x)/(1+exp(x))",
        ("-pi/2", "pi/2"),
        "(pi**2-8)/4",
    ),
    "R2-2025-SG-Group-Q14": (
        "((x+1)**2+(3*x+1)*sqrt(x+log(x)))/(x*sqrt(x+log(x))*(x+sqrt(x+log(x))))",
        None,
        "2*sqrt(x+log(x))+2*log(Abs(x+sqrt(x+log(x))))",
    ),
    "R3-2024-Tournament-Q02-v9": (
        "x**3*sin(log(x))**2*cos(log(x))**2",
        ("0", "1"),
        "Rational(1, 64)",
    ),
    "R3-2024-Tournament-Q03": (
        "(2-sqrt(tan(x))+tan(x))/(1+tan(x)**(Rational(3, 2)))",
        ("0", "pi/2"),
        "pi/2",
    ),
    "R3-2024-Tournament-Q04": (
        "(x-1)/((x-2)*(x-3))+(x-2)/((x-3)*(x-1))+(x-3)/((x-1)*(x-2))",
        None,
        "Rational(5, 2)*log(Abs(x-3))+Rational(5, 2)*log(Abs(x-1))-2*log(Abs(x-2))",
    ),
    "R3-2024-Tournament-Q05": ("1/(x*(x**log(2048)+1))", ("1", "oo"), "Rational(1, 11)"),
    "R3-2024-Tournament-Q07": (
        "(2025+exp(x)+exp(-x))/(1+2025**x)",
        ("-1", "1"),
        "2025+E-1/E",
    ),
    "R3-2024-Tournament-Q09-v4": (
        "sec(x)*(sec(x)+tan(x))**2025",
        None,
        "(sec(x)+tan(x))**2025/2025",
    ),
    "R3-2024-Tournament-Q09-v7": (
        "1/(sin(x)*(log(sin(x))-log(1+cos(x))))",
        None,
        "log(Abs(log(sin(x))-log(1+cos(x))))",
    ),
    "R3-2024-Tournament-Q09-v10": ("log(x)/(x**2+3)", ("1", "3"), "pi*log(3)/(12*sqrt(3))"),
    # Wave 5i. Each triple is the printed integrand, or the closed form the
    # gate proves equal to the printed nest or series, and the printed final.
    "R1-2020-Q23": ("x*(1/x-floor(1/x))*floor(1/x)", ("0", "1"), "pi**2/12-Rational(1,2)"),
    "R1-2020-Q24": (
        "-Rational(1,2)+sqrt(4*x-3)/2",
        None,
        "(4*x-3)**Rational(3,2)/12-x/2",
    ),
    "R1-2021-Q01": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2021-Q11": ("(log(x)/x)**2011", ("1", "oo"), "factorial(2011)/2010**2012"),
    "R1-2021-Q40": ("cos(log(x))/(1+x)**2", ("0", "oo"), "pi/sinh(pi)"),
    "R1-2022-MIT-TB-Q02": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2022-Oxford-Q02": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2022-Q04": (
        "Rational(1,2)+sqrt(x+Rational(1,4))",
        ("0", "1"),
        "Rational(5,12)*(1+sqrt(5))",
    ),
    "R1-2022-Q11": ("1/sqrt(1-4*x)", ("0", "Rational(1,4)"), "Rational(1,2)"),
    "R1-2022-Q20": ("log(1+x+x**2)/x", ("0", "1"), "pi**2/9"),
    "R1-2022-TB2022-Q02": ("x**(E-2)", None, "x**(E-1)/(E-1)"),
    "R1-2023-Q08": ("4**x", ("0", "1"), "3/(2*log(2))"),
    "R1-2023-Q25": ("LambertW(LambertW(x))/x", ("0", "exp(1+E)"), "E+Rational(1,2)"),
    "R1-2023-Q28": (
        "(sqrt(x**2+1)+x)**Rational(1,3)-(sqrt(x**2+1)-x)**Rational(1,3)",
        ("0", "7"),
        "9",
    ),
    "R1-2024-Q17": ("x*(1+1/(1+x**2))", ("0", "1"), "(1+log(2))/2"),
    "R1-2024-Q28": (
        "(asin(x**2)+asin(sqrt(x)))/sqrt(1-x**2)",
        ("0", "1"),
        "pi**2/4",
    ),
    "R1-2025-Online-Q02": ("sin(pi*floor(x))", ("0", "oo"), "0"),
    "R1-2025-Online-Q23": (
        "sqrt(log(x))+exp(((x-1)/(E-1))**2)/(E-1)",
        ("1", "E"),
        "E",
    ),
    "R1-2025-Online-Q25": ("x+1", ("0", "25"), "Rational(675,2)"),
    "R2-2021-Group-Q04": ("log(sin(x))*cos(x)**3", ("0", "pi"), "0"),
    "R2-2021-Relay-B01": ("sin(sin(x)-x)", ("0", "2*pi"), "0"),
    "R2-2022-Group-Q08": ("sin(24*x)/sin(x)", ("0", "2*pi"), "0"),
    "R3-2024-Chainlink-G1-Q02": (
        "(sinh(x)+cosh(x))/(sinh(exp(x))+cosh(exp(x)))",
        None,
        "-exp(-exp(x))",
    ),
    "R3-2024-Chainlink-G1-Q03": ("(1+log(x))/sqrt(x**(-2*x)-1)", None, "asin(x**x)"),
    "R3-2024-Chainlink-G1-Q04": ("1/(x*sqrt(x)*sqrt(x-1))", ("1", "oo"), "2"),
    "R3-2024-Chainlink-G1-Q05": ("log(1+x+x**2)/x", ("0", "1"), "pi**2/9"),
    "R3-2024-Chainlink-G2-Q01": ("5*(x**6+x)**4", ("-1", "0"), "Rational(1,5)"),
    "R3-2024-Chainlink-G2-Q02": (
        "exp(exp(exp(x)))*exp(exp(x))*exp(exp(x))*exp(x)",
        None,
        "exp(exp(exp(x)))*(exp(exp(x))-1)",
    ),
    "R3-2024-Chainlink-G3-Q04": (
        "sin(2*x)/(sin(x)+cos(x)+1)",
        ("0", "pi/4"),
        "1-pi/4",
    ),
    "R3-2024-Chainlink-G4-Q01": ("sin(x)**2/cos(x)**4", None, "tan(x)**3/3"),
    "R3-2024-Chainlink-G4-Q04": (
        "sqrt(log(x+sqrt(1+x**2))/(1+x**2))",
        None,
        "Rational(2,3)*asinh(x)**Rational(3,2)",
    ),
    "R3-2024-Chainlink-G5-Q01": ("atan(x)/(x**2+1)", ("0", "oo"), "pi**2/8"),
    "R3-2024-Chainlink-G5-Q02": (
        "sec(x)**2*csc(x)**2/(tan(x)**2+cot(x)**2+2)",
        None,
        "x",
    ),
    "R3-2024-Chainlink-G5-Q06": ("1/(x**4+1)**2", ("-oo", "oo"), "3*sqrt(2)*pi/8"),
    "R3-2024-Dichotomy-S1-Q01a": ("sqrt(4-x**2)", ("0", "2"), "pi"),
    "R3-2024-Dichotomy-S1-Q01b": ("sqrt(4-x**2)", ("0", "sqrt(2)"), "pi/2+1"),
    "R3-2024-Dichotomy-S1-Q02b": ("tan(x)/tan(2*x)", None, "x-tan(x)/2"),
    "R3-2024-Dichotomy-S1-Q05b": (
        "log(x**(log(1-log(x))+1-log(x)))",
        ("0", "1"),
        "-4",
    ),
    "R3-2024-Dichotomy-S2-Q02a": ("1/((x+1)*sqrt(x)+2*x)", None, "-2/(sqrt(x)+1)"),
    "R3-2024-Dichotomy-S2-Q03a": (
        "(5*x**2+3*x-2)/(x**3+2*x**2)",
        None,
        "3*log(Abs(x+2))+2*log(Abs(x))+1/x",
    ),
    "R3-2024-Dichotomy-S2-Q03b": (
        "(x+1)**2/((x+2)*(x**2+x+1))",
        None,
        "log(Abs(1+(x+1)**3))/3",
    ),
    "R3-2024-Dichotomy-S3-Q01a": ("(x**4+1)/(x**6+1)", ("0", "1"), "pi/3"),
    "R3-2024-Dichotomy-S3-Q01b": (
        "(x**2+1)/(x**3+1)",
        ("0", "1"),
        "(2*log(2)+sqrt(3)*pi/3)/3",
    ),
}


def transcribed(row: dict) -> dict | None:
    item = TRANSCRIPTS.get(row.get("id"))
    if item is None:
        return None
    integrand, limits, answer = item
    return pack_gate.fields_from_parts(integrand, limits, answer, "x")


def gate_row(row: dict, cache: dict) -> dict | None:
    if row.get("round") not in GATED_ROUNDS or row.get("source") != "resource_pack":
        return None
    if row.get("id") in HELD_MANUAL:
        return None
    if not str(row.get("answer_plain") or "").strip():
        return None
    # An id-specific transcript wins over the shared problem number. Tournament
    # sheets repeat a number for a different integral, and for an answer slide.
    known = transcribed(row)
    if known is not None:
        return known
    number = problem_number(row)
    problem_pdf = row.get("pdf_path")
    answer_pdf = row.get("answer_source_pdf")
    if number is not None and problem_pdf and answer_pdf:
        integrals = load_pair(cache, problem_pdf, "problem")
        answers = load_pair(cache, answer_pdf, "answer")
        if integrals is not None and answers is not None:
            integral = integrals.get(number)
            answer = answers.get(number)
            if integral is not None and answer is not None:
                fields = pack_gate.fields_for(number, integral, answer)
                if fields is not None:
                    return fields
    return None


def apply_fields(row: dict, fields: dict) -> None:
    row["verify"] = "sympy"
    row["kind"] = fields["kind"]
    row["variable"] = fields["variable"]
    row["limits"] = fields["limits"]
    row["sympy_expr"] = fields["sympy_expr"]
    row["answer_sympy"] = fields["answer_sympy"]
    row["integrand_latex"] = fields["integrand_latex"]
    row["answer_latex"] = fields["answer_latex"]


def recover(rows: list[dict]) -> tuple[list[dict], list[str]]:
    cache: dict = {}
    gated: list[str] = []
    for row in rows:
        if row.get("round") not in GATED_ROUNDS:
            continue
        fields = gate_row(row, cache)
        if fields is not None:
            apply_fields(row, fields)
            gated.append(row["id"])
        elif row.get("verify") == "sympy" and row.get("source") == "resource_pack":
            pack_gate.blank_gate(row)
    return rows, gated


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--id", action="append", default=[])
    args = parser.parse_args()
    rows = problem_catalog.load_records()
    before = sum(1 for row in rows if row.get("verify") == "sympy")
    rows, gated = recover(rows)
    if args.id:
        wanted = set(args.id)
        gated = [item for item in gated if item in wanted]
        print("\n".join(gated))
    else:
        print(f"sympy {before} -> {len(gated)}")
        for item in gated:
            row = next(row for row in rows if row["id"] == item)
            print(f"{item}\t{row['kind']}\t{row['sympy_expr']}\t{row['limits']}\t{row['answer_sympy']}")
    if args.write:
        if args.id:
            print("refusing a partial write", file=sys.stderr)
            return 2
        err = problem_catalog.catalog_problem(rows)
        if err:
            print(err, file=sys.stderr)
            return 1
        problem_catalog.dump_records(rows)
        print(f"wrote {problem_catalog.RECORDS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
