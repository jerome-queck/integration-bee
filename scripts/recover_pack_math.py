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
        if kind == "problem":
            cache[key] = pdf_math.integral_readings(str(path))
        else:
            cache[key] = pdf_math.answer_readings(str(path))
    return cache[key]


GATED_ROUNDS = frozenset({"r1", "r2", "r3"})
# The turn contract and the catalog pin use this row as the manual mark example.
HELD_MANUAL = frozenset({"R1-2024-Q01"})


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
    if number is None or not problem_pdf or not answer_pdf:
        return None
    integrals = load_pair(cache, problem_pdf, "problem")
    answers = load_pair(cache, answer_pdf, "answer")
    integral = integrals.get(number)
    answer = answers.get(number)
    if integral is None or answer is None:
        return None
    return pack_gate.fields_for(number, integral, answer)


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
