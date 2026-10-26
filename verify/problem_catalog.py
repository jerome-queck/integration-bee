from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"

ROUNDS = frozenset({"r1", "r2", "r3", "yang", "sample"})
SOURCES = frozenset({"resource_pack", "yang_book", "uk_sample"})
SAMPLE_ROUND = "sample"
SAMPLE_SOURCE = "uk_sample"
SAMPLE_COUNT = 20
SAMPLE_PROBLEM_PDF = "sources/Integration_Competition_Sample_problems.pdf"
SAMPLE_ANSWERS_PDF = "sources/Integration_bee_sample_problems_answers.pdf"
SAMPLE_SOLUTIONS_PDF = "sources/UK_University_integration_bee_sample_problems_solutions.pdf"
VERIFIES = frozenset({"manual", "unchecked", "sympy"})
SYMPY_VARIABLES = frozenset({"x", "t", "X", "e"})
ORIGINS = frozenset({"missing", "pdf_copy"})
YANG_WITH_ANSWER = frozenset({"YANG-1.3-Ex01", "YANG-1.3-Ex03"})
EXPECTED_COUNT = 946
EXPECTED_MANUAL = 37
EXPECTED_SYMPY = 639
EXPECTED_PDF_COPY = 195
EXPECTED_ROUNDS = {"r1": 280, "r2": 204, "r3": 190, "yang": 272}
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
    if row.get("variable") not in SYMPY_VARIABLES:
        return f"{ident} unsupported sympy variable"
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


def _is_sample(row: dict) -> bool:
    ident = str(row.get("id") or "")
    return row.get("round") == SAMPLE_ROUND or row.get("source") == SAMPLE_SOURCE or ident.startswith("SAMPLE-")


def _sample_sympy_shape(row: dict) -> str | None:
    ident = row.get("id")
    if row.get("source") != SAMPLE_SOURCE or row.get("round") != SAMPLE_ROUND:
        return f"{ident} sample sympy source"
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


def _sample_catalog(rows: list[dict]) -> str | None:
    if len(rows) != SAMPLE_COUNT:
        return f"sample count {len(rows)}"
    expected = [f"SAMPLE-Q{i:02d}" for i in range(1, SAMPLE_COUNT + 1)]
    if [row.get("id") for row in rows] != expected:
        return "sample ids"
    for row in rows:
        ident = row["id"]
        if row.get("round") != SAMPLE_ROUND or row.get("source") != SAMPLE_SOURCE:
            return f"{ident} sample source"
        if row.get("pdf_path") != SAMPLE_PROBLEM_PDF or row.get("pdf_role") != "problems":
            return f"{ident} sample problem pdf"
        if row.get("problem_id") != ident.removeprefix("SAMPLE-"):
            return f"{ident} sample problem id"
        if row.get("kind") not in {"definite", "indefinite"}:
            return f"{ident} sample kind"
        if _blank(row.get("integrand_plain")):
            return f"{ident} missing integrand"
        if _blank(row.get("answer_plain")) or _blank(row.get("answer_source_pdf")):
            return f"{ident} sample answer cite"
        cite = str(row.get("answer_source_pdf"))
        if cite not in {SAMPLE_ANSWERS_PDF, SAMPLE_SOLUTIONS_PDF}:
            return f"{ident} sample answer pdf"
        if row.get("verify") not in {"manual", "sympy"}:
            return f"{ident} sample verify"
        if row.get("worked_solution_origin") != "missing" or not _blank(row.get("worked_solution_plain")):
            return f"{ident} sample worked field"
        if row.get("worked_solution_latex") is not None:
            return f"{ident} sample worked latex"
        solution = f"solutions/sample/{ident}.md"
        if solution not in str(row.get("notes") or ""):
            return f"{ident} sample solution path"
        if not isinstance(row.get("technique_tags"), list) or not isinstance(row.get("yang"), list):
            return f"{ident} sample tags"
        if row.get("verify") == "sympy":
            shape = _sample_sympy_shape(row)
            if shape:
                return shape
        else:
            if "answer_sympy" in row or "sympy_expr" in row or "variable" in row:
                return f"{ident} invented answer_sympy"
            if row.get("integrand_latex") is not None or row.get("answer_latex") is not None:
                return f"{ident} invented latex answer"
            if row.get("limits") is not None:
                return f"{ident} manual limits"
        if ident == "SAMPLE-Q15" and "sign" not in str(row.get("notes") or "").lower():
            return "SAMPLE-Q15 note must record the printed sign"
        if ident == "SAMPLE-Q17":
            expr = str(row.get("sympy_expr") or "").replace(" ", "")
            plain = str(row.get("integrand_plain") or "")
            if row.get("verify") != "sympy" or row.get("answer_sympy") != "E*x":
                return "SAMPLE-Q17 grades e*x"
            if expr not in {"E", "x**(1/log(x))"}:
                return "SAMPLE-Q17 integrand"
            if "1/ln" not in plain and "1/\\ln" not in plain:
                return "SAMPLE-Q17 plain integrand"
    return None


def catalog_problem(rows: list[dict]) -> str | None:
    ids = [row.get("id") for row in rows]
    if any(not isinstance(item, str) or not item for item in ids):
        return "catalog id missing"
    if len(set(ids)) != len(ids):
        return "catalog duplicate id"
    if ids != sorted(ids):
        return "catalog not sorted by id"
    samples = [row for row in rows if _is_sample(row)]
    pack_rows = [row for row in rows if not _is_sample(row)]
    sample_err = _sample_catalog(samples)
    if sample_err:
        return sample_err
    if len(pack_rows) != EXPECTED_COUNT:
        return f"catalog count {len(pack_rows)}"
    rows = pack_rows
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
    if pinned.get("verify") != "sympy":
        return "R1-2024-Q01 is not sympy"
    return None
