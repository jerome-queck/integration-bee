from __future__ import annotations

import json
from pathlib import Path

import pack_answer_contracts

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
YANG_WITH_ANSWER = frozenset({
    "YANG-1.1-P01",
    "YANG-1.1-P02",
    "YANG-1.1-P03",
    "YANG-1.1-P04",
    "YANG-1.1-P05",
    "YANG-1.1-P06",
    "YANG-1.11-P01",
    "YANG-1.11-P02",
    "YANG-1.11-P03",
    "YANG-1.11-P04",
    "YANG-1.11-P05",
    "YANG-1.11-P06",
    "YANG-1.11-P07",
    "YANG-1.11-P08",
    "YANG-1.11-P09",
    "YANG-1.11-P10",
    "YANG-1.11-P11",
    "YANG-1.11-P12",
    "YANG-1.11-P13",
    "YANG-1.11-P14",
    "YANG-1.11-P15",
    "YANG-1.11-P16",
    "YANG-1.11-P17",
    "YANG-1.11-P18",
    "YANG-1.11-P19",
    "YANG-1.11-P20",
    "YANG-1.12-P01",
    "YANG-1.12-P02",
    "YANG-1.12-P03",
    "YANG-1.12-P04",
    "YANG-1.12-P05",
    "YANG-1.12-P06",
    "YANG-1.12-P07",
    "YANG-1.12-P08",
    "YANG-1.12-P09",
    "YANG-1.12-P10",
    "YANG-1.15-P01",
    "YANG-1.15-P02",
    "YANG-1.15-P03",
    "YANG-1.15-P04",
    "YANG-1.15-P05",
    "YANG-1.15-P06",
    "YANG-1.15-P07",
    "YANG-1.15-P08",
    "YANG-1.15-P09",
    "YANG-1.15-P10",
    "YANG-1.15-P11",
    "YANG-1.15-P12",
    "YANG-1.15-P13",
    "YANG-1.15-P14",
    "YANG-1.15-P15",
    "YANG-1.15-P16",
    "YANG-1.15-P17",
    "YANG-1.15-P18",
    "YANG-1.15-P19",
    "YANG-1.15-P20",
    "YANG-1.17-P01",
    "YANG-1.18-P02",
    "YANG-1.2-P01",
    "YANG-1.2-P02",
    "YANG-1.2-P03",
    "YANG-1.2-P04",
    "YANG-1.2-P05",
    "YANG-1.2-P06",
    "YANG-1.2-P07",
    "YANG-1.2-P08",
    "YANG-1.2-P09",
    "YANG-1.2-P10",
    "YANG-1.2-P11",
    "YANG-1.2-P12",
    "YANG-1.2-P13",
    "YANG-1.2-P14",
    "YANG-1.2-P15",
    "YANG-1.2-P16",
    "YANG-1.2-P17",
    "YANG-1.2-P18",
    "YANG-1.2-P19",
    "YANG-1.2-P20",
    "YANG-1.20-P01",
    "YANG-1.20-P02",
    "YANG-1.20-P03",
    "YANG-1.20-P04",
    "YANG-1.20-P05",
    "YANG-1.20-P06",
    "YANG-1.20-P07",
    "YANG-1.3-Ex01",
    "YANG-1.3-Ex02",
    "YANG-1.3-Ex03",
    "YANG-1.4-P01",
    "YANG-1.4-P02",
    "YANG-1.4-P03",
    "YANG-1.4-P04",
    "YANG-1.4-P05",
    "YANG-1.4-P06",
    "YANG-1.4-P07",
    "YANG-1.4-P08",
    "YANG-1.4-P09",
    "YANG-1.4-P10",
    "YANG-1.4-P11",
    "YANG-1.4-P12",
    "YANG-1.4-P13",
    "YANG-1.4-P14",
    "YANG-1.4-P15",
    "YANG-1.4-P16",
    "YANG-1.4-P17",
    "YANG-1.4-P18",
    "YANG-1.5-P01",
    "YANG-1.5-P02",
    "YANG-1.5-P03",
    "YANG-1.5-P04",
    "YANG-1.5-P05",
    "YANG-1.5-P06",
    "YANG-1.5-P07",
    "YANG-1.5-P08",
    "YANG-1.5-P09",
    "YANG-1.5-P10",
    "YANG-1.5-P11",
    "YANG-1.5-P12",
    "YANG-1.5-P13",
    "YANG-1.5-P14",
    "YANG-1.5-P15",
    "YANG-1.5-P16",
    "YANG-1.5-P17",
    "YANG-1.5-P18",
    "YANG-1.5-P19",
    "YANG-1.5-P20",
    "YANG-1.6-P01",
    "YANG-1.6-P02",
    "YANG-1.6-P03",
    "YANG-1.6-P04",
    "YANG-1.6-P05",
    "YANG-1.6-P06",
    "YANG-1.6-P07",
    "YANG-1.6-P08",
    "YANG-1.6-P09",
    "YANG-1.6-P10",
    "YANG-1.6-P11",
    "YANG-1.6-P12",
    "YANG-1.6-P13",
    "YANG-1.6-P14",
    "YANG-1.6-P15",
    "YANG-1.6-P16",
    "YANG-1.6-P17",
    "YANG-1.6-P18",
    "YANG-1.6-P19",
    "YANG-1.6-P20",
    "YANG-1.7-P01",
    "YANG-1.7-P02",
    "YANG-1.7-P03",
    "YANG-1.7-P04",
    "YANG-1.7-P05",
    "YANG-1.7-P06",
    "YANG-1.7-P07",
    "YANG-1.7-P08",
    "YANG-1.7-P09",
    "YANG-1.7-P10",
    "YANG-1.8-P01",
    "YANG-1.8-P02",
    "YANG-1.8-P03",
    "YANG-1.8-P04",
    "YANG-1.8-P05",
    "YANG-1.8-P06",
    "YANG-1.8-P07",
    "YANG-1.8-P08",
    "YANG-1.8-P09",
    "YANG-1.8-P10",
    "YANG-1.8-P11",
    "YANG-1.8-P12",
    "YANG-1.8-P13",
    "YANG-1.8-P14",
    "YANG-1.8-P15",
    "YANG-1.8-P16",
    "YANG-1.8-P17",
    "YANG-1.9-P01a",
    "YANG-1.9-P01b",
    "YANG-1.9-P01c",
    "YANG-1.9-P04a",
    "YANG-1.9-P04b",
    "YANG-2.3-P01",
    "YANG-2.3-P02",
    "YANG-2.3-P03",
    "YANG-2.3-P04",
    "YANG-2.3-P05",
    "YANG-2.3-P06",
    "YANG-2.3-P07",
    "YANG-2.3-P08",
    "YANG-2.3-P09",
    "YANG-2.3-P10",
    "YANG-2.3-P11",
    "YANG-2.3-P12",
    "YANG-2.3-P13",
    "YANG-2.3-P14",
    "YANG-2.3-P15",
    "YANG-2.3-P16",
    "YANG-2.3-P17",
    "YANG-2.3-P18",
    "YANG-2.4-P01",
    "YANG-2.4-P02",
    "YANG-2.4-P03",
    "YANG-2.4-P04",
    "YANG-2.4-P05",
    "YANG-2.4-P06",
    "YANG-2.4-P07",
    "YANG-2.4-P08",
    "YANG-2.4-P09",
    "YANG-2.4-P10",
    "YANG-2.4-P11",
    "YANG-2.4-P12",
    "YANG-2.5-P01",
    "YANG-2.5-P02",
    "YANG-2.5-P03",
    "YANG-2.5-P04",
    "YANG-2.5-P05",
    "YANG-2.5-P06",
    "YANG-2.5-P07",
    "YANG-2.5-P08",
    "YANG-2.5-P09",
    "YANG-2.5-P10",
    "YANG-2.5-P11",
    "YANG-2.5-P12",
    "YANG-2.5-P13",
    "YANG-2.5-P14",
    "YANG-2.5-P15",
    "YANG-2.5-P16",
    "YANG-2.5-P17",
    "YANG-2.5-P18",
    "YANG-2.6-P01",
    "YANG-2.6-P02",
    "YANG-2.6-P03",
    "YANG-2.6-P04",
    "YANG-2.6-P05",
    "YANG-2.6-P06",
    "YANG-2.6-P07",
    "YANG-2.6-P08",
    "YANG-2.6-P09",
    "YANG-2.6-P10",
    "YANG-2.6-P11",
    "YANG-2.6-P12",
    "YANG-2.6-P13",
    "YANG-2.6-P14",
    "YANG-2.6-P15",
    "YANG-2.6-P16",
    "YANG-2.7-P01",
    "YANG-2.7-P02",
    "YANG-2.7-P03",
    "YANG-2.7-P04",
    "YANG-2.7-P05",
    "YANG-2.7-P06",
    "YANG-2.7-P07",
    "YANG-2.7-P08",
    "YANG-2.7-P09",
    "YANG-2.7-P10",
    "YANG-2.7-P11",
    "YANG-2.7-P12",
    "YANG-2.7-P13",
    "YANG-3.4-P06",
    "YANG-3.8-P01",
    "YANG-3.8-P02",
    "YANG-3.8-P03",
    "YANG-3.8-P04",
    "YANG-3.8-P05",
    "YANG-3.8-P06",
    "YANG-3.8-P07",
    "YANG-3.8-P08",
    "YANG-3.8-P09",
    "YANG-3.8-P10",
    "YANG-3.8-P11",
    "YANG-3.8-P12",
    "YANG-3.8-P13",
    "YANG-3.8-P14",
    "YANG-4.4-P01",
    "YANG-4.6-P04",
    "YANG-6.1-P04",
    "YANG-6.7-P03",
})
EXPECTED_COUNT = 948
EXPECTED_MANUAL = 0
# 674 resource-pack rows, plus 274 proved Yang rows.
# L5 left 942. The §1.9 split adds five proved examples in place of two
# bundled rows, and YANG-1.20-P01 adds one proved row. YANG-1.14-P10 is a
# reference formula in REFERENCE_IDS, omitted from pack_rows.
EXPECTED_SYMPY = 948
EXPECTED_PDF_COPY = 195
EXPECTED_ROUNDS = {"r1": 280, "r2": 204, "r3": 190, "yang": 274}
# Printed guide identities that are not integrals. They stay in the JSONL
# and are omitted from pack_rows, the same exclusion samples use.
REFERENCE_IDS = frozenset({"YANG-1.14-P10"})
PINNED_CITE = {
    "id": "R1-2024-Q01",
    "answer_has": "sin(1)",
    "mark_scheme_suffix": "Mark_Scheme_2024_Round_1_UK_University_Integration_Bee.pdf",
}
# Source-checked inputs whose printed answers still conflict with the problem.
# Transcribing the question does not authorize a symbolic answer or grading.
MANUAL_INPUT_KINDS = {
}


def first_unchecked_yang(rows: list[dict] | None = None) -> str:
    """First Yang row that still has no proved final. Stable under id order."""
    data = rows if rows is not None else load_records()
    for row in data:
        if row.get("source") == "yang_book" and row.get("verify") == "unchecked":
            ident = row.get("id")
            if isinstance(ident, str) and ident:
                return ident
    raise ValueError("no unchecked yang row")


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


def manual_input_problem(row: dict) -> str | None:
    """Validate the remaining display-only transcriptions without proving a final."""
    ident = row.get("id")
    kind = MANUAL_INPUT_KINDS.get(ident)
    if kind is None or row.get("source") != "resource_pack" or row.get("verify") != "manual":
        return f"{ident} unrecognized manual input"
    if row.get("kind") != kind or row.get("variable") not in SYMPY_VARIABLES:
        return f"{ident} manual input kind or variable"
    for key in ("sympy_expr", "integrand_latex"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            return f"{ident} missing manual {key}"
    limits = row.get("limits")
    if kind == "expression":
        if limits != []:
            return f"{ident} expression has outer limits"
    elif not isinstance(limits, list) or len(limits) != 2 or any(
        not isinstance(item, str) or not item.strip() for item in limits
    ):
        return f"{ident} manual definite limits"
    if "answer_sympy" in row or row.get("answer_latex") is not None or row.get("worked_solution_latex") is not None:
        return f"{ident} invented manual answer"
    return None


def _sympy_shape(row: dict) -> str | None:
    ident = row.get("id")
    if row.get("round") == "yang":
        if row.get("source") != "yang_book" or ident not in YANG_WITH_ANSWER:
            return f"{ident} sympy outside the answered Yang examples"
    elif row.get("source") != "resource_pack":
        return f"{ident} sympy outside the resource pack"
    if row.get("kind") == "grid":
        import pack_grid

        error = pack_grid.row_problem(row)
        return f"{ident} {error}" if error else None
    if row.get("variable") not in SYMPY_VARIABLES:
        return f"{ident} unsupported sympy variable"
    if row.get("kind") not in {"definite", "indefinite", "discrete_multiplicative"} | pack_answer_contracts.KINDS:
        return f"{ident} sympy kind"
    for key in ("sympy_expr", "answer_sympy", "integrand_latex", "answer_latex"):
        if _blank(row.get(key)) or not isinstance(row.get(key), str):
            return f"{ident} missing {key}"
    limits = row.get("limits")
    if row.get("kind") not in pack_answer_contracts.BOUNDED_KINDS:
        if limits not in ([],):
            return f"{ident} non-bounded kind has limits"
    elif not isinstance(limits, list) or len(limits) != 2 or any(_blank(item) or not isinstance(item, str) for item in limits):
        return f"{ident} definite limits"
    worked_latex = row.get("worked_solution_latex")
    if worked_latex is not None:
        plain = row.get("worked_solution_plain")
        if (
            row.get("worked_solution_origin") != "missing"
            or _blank(plain)
            or not isinstance(worked_latex, str)
            or _blank(worked_latex)
        ):
            return f"{ident} invented worked latex"
    return None


def _is_sample(row: dict) -> bool:
    ident = str(row.get("id") or "")
    return row.get("round") == SAMPLE_ROUND or row.get("source") == SAMPLE_SOURCE or ident.startswith("SAMPLE-")


def _is_reference(row: dict) -> bool:
    """A printed formula that is not an integral. Excluded from pack counts."""
    return row.get("id") in REFERENCE_IDS


def _reference_catalog(rows: list[dict]) -> str | None:
    """Keep the formula row out of the pack without storing an integrand."""
    if [row.get("id") for row in rows] != ["YANG-1.14-P10"]:
        return "reference ids"
    row = rows[0]
    ident = row["id"]
    if row.get("source") != "yang_book" or row.get("round") != "yang":
        return f"{ident} reference source"
    if row.get("section") != "1.14" or row.get("kind") != "reference":
        return f"{ident} reference kind"
    if row.get("verify") != "unchecked":
        return f"{ident} reference is not an unchecked formula"
    if not _blank(row.get("answer_plain")) or not _blank(row.get("answer_source_pdf")):
        return f"{ident} reference invented an answer"
    if "answer_sympy" in row or "sympy_expr" in row or "variable" in row:
        return f"{ident} reference invented an integral"
    if row.get("integrand_latex") is not None or row.get("answer_latex") is not None:
        return f"{ident} reference invented latex"
    if row.get("worked_solution_latex") is not None:
        return f"{ident} reference worked latex"
    if row.get("worked_solution_origin") != "missing" or not _blank(row.get("worked_solution_plain")):
        return f"{ident} reference worked field"
    plain = str(row.get("integrand_plain") or "")
    folded = plain.lower().replace(" ", "")
    if "1/n" not in folded or "pi" not in folded:
        return f"{ident} reference formula"
    if any(token in plain for token in ("dx", "\\int", "∫", "Geometric", "Z ")):
        return f"{ident} reference bundled an integral"
    notes = str(row.get("notes") or "")
    if "not an integral" not in notes or "excluded" not in notes or "formula" not in notes.lower():
        return f"{ident} reference reason"
    return None


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
    references = [row for row in rows if _is_reference(row)]
    pack_rows = [row for row in rows if not _is_sample(row) and not _is_reference(row)]
    sample_err = _sample_catalog(samples)
    if sample_err:
        return sample_err
    reference_err = _reference_catalog(references)
    if reference_err:
        return reference_err
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
            if row.get("id") in MANUAL_INPUT_KINDS:
                shape = manual_input_problem(row)
                if shape:
                    return shape
            elif "sympy_expr" in row or "variable" in row or row.get("integrand_latex") is not None:
                return f"{row.get('id')} invented manual input"
            if "answer_sympy" in row:
                return f"{row.get('id')} invented answer_sympy"
            if row.get("answer_latex") is not None or row.get("worked_solution_latex") is not None:
                return f"{row.get('id')} invented latex answer"
            if has_answer and row.get("verify") != "manual":
                return f"{row.get('id')} answered row is not manual"
            if not has_answer and row.get("verify") != "unchecked":
                return f"{row.get('id')} unanswered row is not unchecked"
        plain_filled = not _blank(row.get("worked_solution_plain"))
        worked_latex = row.get("worked_solution_latex")
        latex_filled = isinstance(worked_latex, str) and not _blank(worked_latex)
        origin = row.get("worked_solution_origin")
        if origin == "pdf_copy":
            if not plain_filled or worked_latex is not None:
                return f"{row.get('id')} worked text and origin diverged"
        elif plain_filled != latex_filled or (worked_latex is not None and not latex_filled):
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
