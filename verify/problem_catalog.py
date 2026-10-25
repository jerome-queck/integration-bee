from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"

ROUNDS = frozenset({"r1", "r2", "r3", "yang"})
SOURCES = frozenset({"resource_pack", "yang_book"})
VERIFIES = frozenset({"manual", "unchecked", "sympy"})
ORIGINS = frozenset({"missing", "pdf_copy"})
YANG_WITH_ANSWER = frozenset({"YANG-1.3-Ex01", "YANG-1.3-Ex03"})
EXPECTED_COUNT = 949
EXPECTED_MANUAL = 422
EXPECTED_SYMPY = 52
EXPECTED_PDF_COPY = 195
EXPECTED_ROUNDS = {"r1": 280, "r2": 207, "r3": 190, "yang": 272}
PINNED_CITE = {
    "id": "R1-2024-Q01",
    "answer_has": "sin(1)",
    "mark_scheme_suffix": "Mark_Scheme_2024_Round_1_UK_University_Integration_Bee.pdf",
}


def load_records(path: Path | None = None) -> list[dict]:
    target = path or RECORDS
    text = target.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        raise ValueError("catalog file must end with a newline")
    rows = []
    for line in text.splitlines():
        if not line.strip():
            raise ValueError("catalog file has a blank line")
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ValueError("catalog line is not an object")
        rows.append(row)
    return rows


def dump_records(rows: list[dict], path: Path | None = None) -> None:
    target = path or RECORDS
    target.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    target.write_text(body, encoding="utf-8")


def normalize_extract(raw: list) -> list[dict]:
    if not isinstance(raw, list):
        raise ValueError("extract is not a list")
    rows = []
    for row in raw:
        if not isinstance(row, dict) or not row.get("id"):
            raise ValueError("extract row is missing id")
        rows.append(dict(row))
    rows.sort(key=lambda row: row["id"])
    return rows


def index_view(row: dict) -> dict:
    return {
        "id": row.get("id"),
        "round": row.get("round"),
        "year": row.get("year"),
        "region": row.get("region"),
        "source": row.get("source"),
        "pdf_path": row.get("pdf_path"),
        "problem_id": row.get("problem_id"),
        "kind": row.get("kind"),
        "verify": row.get("verify"),
        "has_answer": bool(row.get("answer_plain")),
        "has_worked": row.get("worked_solution_origin") == "pdf_copy",
    }


def prompt_view(row: dict) -> dict:
    view = {
        "id": row.get("id"),
        "round": row.get("round"),
        "year": row.get("year"),
        "region": row.get("region"),
        "source": row.get("source"),
        "pdf_path": row.get("pdf_path"),
        "pdf_role": row.get("pdf_role"),
        "problem_id": row.get("problem_id"),
        "kind": row.get("kind"),
        "integrand_plain": row.get("integrand_plain"),
        "verify": row.get("verify"),
        "has_answer": bool(row.get("answer_plain")),
        "has_worked": row.get("worked_solution_origin") == "pdf_copy",
        "yang": list(row.get("yang") or []),
    }
    if row.get("section"):
        view["section"] = row.get("section")
        view["section_title"] = row.get("section_title")
    return view


def spec_problem(spec: dict) -> str | None:
    if spec.get("round") and spec["round"] not in ROUNDS:
        return f"unknown round {spec['round']}"
    if spec.get("source") and spec["source"] not in SOURCES:
        return f"unknown source {spec['source']}"
    if spec.get("verify") and spec["verify"] not in VERIFIES:
        return f"unknown verify {spec['verify']}"
    return None


def matching(rows: list[dict], spec: dict) -> list[dict]:
    found = []
    for row in rows:
        if spec.get("id") and row.get("id") != spec["id"]:
            continue
        if spec.get("round") and row.get("round") != spec["round"]:
            continue
        if spec.get("year") is not None and str(row.get("year")) != str(spec["year"]):
            continue
        if spec.get("source") and row.get("source") != spec["source"]:
            continue
        if spec.get("verify") and row.get("verify") != spec["verify"]:
            continue
        if spec.get("problem_id") and row.get("problem_id") != spec["problem_id"]:
            continue
        found.append(row)
    return found


def _blank(value) -> bool:
    return value is None or value == ""


def _sympy_shape(row: dict) -> str | None:
    ident = row.get("id")
    if row.get("round") == "yang" or row.get("source") != "resource_pack":
        return f"{ident} sympy outside the resource pack"
    if row.get("variable") != "x":
        return f"{ident} sympy variable is not x"
    if row.get("kind") not in {"definite", "indefinite"}:
        return f"{ident} sympy kind"
    for key in ("sympy_expr", "answer_sympy", "integrand_latex", "answer_latex"):
        if _blank(row.get(key)) or not isinstance(row.get(key), str):
            return f"{ident} missing {key}"
    limits = row.get("limits")
    if row.get("kind") == "indefinite":
        if limits not in ([],):
            return f"{ident} indefinite limits"
    elif not isinstance(limits, list) or len(limits) != 2 or any(_blank(item) or not isinstance(item, str) for item in limits):
        return f"{ident} definite limits"
    if row.get("worked_solution_latex") is not None:
        return f"{ident} invented worked latex"
    return None


def catalog_problem(rows: list[dict]) -> str | None:
    if len(rows) != EXPECTED_COUNT:
        return f"catalog count {len(rows)}"
    ids = [row.get("id") for row in rows]
    if any(not isinstance(item, str) or not item for item in ids):
        return "catalog id missing"
    if len(set(ids)) != len(ids):
        return "catalog duplicate id"
    if ids != sorted(ids):
        return "catalog not sorted by id"
    manual = 0
    sympy_n = 0
    pdf_copy = 0
    rounds = {key: 0 for key in EXPECTED_ROUNDS}
    yang_answered = []
    pinned = None
    for row in rows:
        if row.get("round") not in ROUNDS:
            return f"{row.get('id')} bad round"
        if row.get("source") not in SOURCES:
            return f"{row.get('id')} bad source"
        if row.get("verify") not in VERIFIES:
            return f"{row.get('id')} bad verify"
        if row.get("worked_solution_origin") not in ORIGINS:
            return f"{row.get('id')} bad worked origin"
        if _blank(row.get("pdf_path")) or not str(row.get("pdf_path")).startswith("sources/"):
            return f"{row.get('id')} missing source cite"
        if _blank(row.get("integrand_plain")):
            return f"{row.get('id')} missing integrand"
        has_answer = not _blank(row.get("answer_plain"))
        has_cite = not _blank(row.get("answer_source_pdf"))
        if has_answer != has_cite:
            return f"{row.get('id')} answer and cite diverged"
        if row.get("verify") == "sympy":
            if not has_answer:
                return f"{row.get('id')} sympy row has no cited answer"
            shape = _sympy_shape(row)
            if shape:
                return shape
            sympy_n += 1
        else:
            if "answer_sympy" in row or "sympy_expr" in row or "variable" in row:
                return f"{row.get('id')} invented answer_sympy"
            if row.get("integrand_latex") is not None:
                return f"{row.get('id')} invented integrand_latex"
            if row.get("answer_latex") is not None or row.get("worked_solution_latex") is not None:
                return f"{row.get('id')} invented latex answer"
            if has_answer and row.get("verify") != "manual":
                return f"{row.get('id')} answered row is not manual"
            if not has_answer and row.get("verify") != "unchecked":
                return f"{row.get('id')} unanswered row is not unchecked"
        worked = not _blank(row.get("worked_solution_plain"))
        origin = row.get("worked_solution_origin")
        if worked != (origin == "pdf_copy"):
            return f"{row.get('id')} worked text and origin diverged"
        pack = row.get("source") == "resource_pack"
        if pack == (row.get("round") == "yang"):
            return f"{row.get('id')} source and round diverged"
        if row.get("round") == "yang":
            if _blank(row.get("section")) or _blank(row.get("section_title")):
                return f"{row.get('id')} missing yang section"
            if has_answer:
                yang_answered.append(row["id"])
        elif row.get("section") or row.get("section_title"):
            return f"{row.get('id')} pack row has a yang section"
        rounds[row["round"]] += 1
        if has_answer and row.get("verify") == "manual":
            manual += 1
        if origin == "pdf_copy":
            pdf_copy += 1
        if row.get("id") == PINNED_CITE["id"]:
            pinned = row
    if manual != EXPECTED_MANUAL:
        return f"manual count {manual}"
    if sympy_n != EXPECTED_SYMPY:
        return f"sympy count {sympy_n}"
    if pdf_copy != EXPECTED_PDF_COPY:
        return f"pdf_copy count {pdf_copy}"
    if rounds != EXPECTED_ROUNDS:
        return f"round counts {rounds}"
    if frozenset(yang_answered) != YANG_WITH_ANSWER:
        return f"yang answers {sorted(yang_answered)}"
    if pinned is None:
        return "missing R1-2024-Q01"
    answer = str(pinned.get("answer_plain") or "")
    if PINNED_CITE["answer_has"] not in answer:
        return "R1-2024-Q01 answer cite changed"
    cite = str(pinned.get("answer_source_pdf") or "")
    if not cite.endswith(PINNED_CITE["mark_scheme_suffix"]):
        return "R1-2024-Q01 mark scheme cite changed"
    if pinned.get("worked_solution_origin") != "pdf_copy":
        return "R1-2024-Q01 lost its worked solution"
    if pinned.get("verify") != "manual":
        return "R1-2024-Q01 is not manual"
    return None
