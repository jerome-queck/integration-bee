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
    return transcribed(row)


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
