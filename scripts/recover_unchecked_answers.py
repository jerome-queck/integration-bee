#!/usr/bin/env python3
"""Fill unchecked resource-pack rows from printed finals in committed PDFs.

The strings below were read off the mark-scheme and answer slides (pymupdf
text plus the rendered page). A row stays unchecked when no sheet states that
problem's final. Writes problems/records.jsonl only with --write, and then
the catalog manual count so verify/problem_catalog.py still accepts the file.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / "problems" / "records.jsonl"
sys.path.insert(0, str(ROOT / "verify"))

import problem_catalog  # noqa: E402

SLIDES = "sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf"
TB_SCHEME = "sources/past/r1/2022/Tiebreaker_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(6).pdf"
R2_2021_SCHEME = "sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf"
R2_2025_SCHEME = "sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf"

# 2021 Round 2 mark scheme, page 4, Shuttle A–D. These are the values the
# scheme tells markers to accept (including the pass-on instruction).
SHUTTLE = {
    "A01": "4",
    "A02": "2√2",
    "A03": "π",
    "A04": "−1/(2π² ln(2))",
    "B01": "0",
    "B02": "0",
    "B03": "−∞",
    "B04": "ln(π)/2",
    "C01": "0",
    "C02": "2",
    "C03": "2",
    "C04": "π/4",
    "D01": "2,3 or 3,2 - any order is fine.",
    "D02": "1",
    "D03": "φ = (1 + √5)/2",
    "D04": "2π²",
}

# 2022 Round 1 tiebreaker mark scheme, numbered 1–20, same order as the
# tiebreaker problem sheet.
TIEBREAKER_2022 = {
    1: "sin(1)",
    2: "x^{e−1}/(e − 1)",
    3: "e",
    4: "e^{e^x}",
    5: "ln(4)",
    6: "ln 2 / a",
    7: "0",
    8: "π/4",
    9: "π²/4",
    10: "(π/4) ln(3)",
    11: "ln x + ln 2 log log x",
    12: "(2n)! √π / (4^n n! · 2)",
    13: "√π / 2",
    14: "π²/12",
    15: "2ζ(3)",
    16: "π ln 2",
    17: "arctan(a)",
    18: "1/2",
    19: "π³/8",
    20: "π/4",
}

# 2025 UK Round 2 mark scheme, Group Round items 1–10. Same order as
# 2025_Group_Round_2_Integration_Bee.pdf. Singapore copies of those
# integrands take the same final. Stored UK group answers are not copied:
# they were filled from the relay list.
GROUP_2025 = {
    1: "0",
    2: "π/√3",
    3: "π/2",
    4: "2 − π²/6",
    5: "π/√2 − π/4 − ln(2)/2",
    6: "π",
    7: "π/(2e√2)",
    8: "π",
    9: "ln(2) − 1",
    10: "1",
}

# 2025 UK Round 2 mark scheme, Relay Round items 1–20. Same order as
# 2025_Relay_Round_2.pdf.
RELAY_2025 = {
    1: "−1/2025",
    2: "ln(2) − π/4 + π²/32",
    3: "2(n + 2026)²/(2n + 53) when m = n; 0 when m ≠ n. (Reject partial answers.)",
    4: "π/4",
    5: "((−1)^m m! / n) ζ(m + 1)",
    6: "(1/φ) ln|1 + xφ| + C",
    7: "1 − 1/√2",
    8: "0",
    9: "π/4",
    10: "C · 2025^x · Γ((x + 2026)/2025), or C · 2025^x · (x + 1/2025) · Γ(x + 1/2025)",
    11: "−πγ/2",
    12: "1/2",
    13: "√π",
    14: "π/e",
    15: "π/3",
    16: "(1/e) ln(√2 + 1)",
    17: "π²/24",
    18: "π/e − π/2",
    19: "5/4",
    20: "1999",
}


def norm(text: str) -> str:
    value = (text or "").lower()
    value = value.replace("ln", "log").replace("π", "pi").replace("−", "-").replace("–", "-")
    value = value.replace("ˆ", "").replace("∫", "")
    value = re.sub(r"\s+", "", value)
    value = re.sub(r"[^a-z0-9+\-]", "", value)
    return value


def fingerprint(text: str) -> str:
    """Integrand identity with page furniture removed. Used only to pair a
    Singapore copy with the UK problem it reprints."""
    value = (text or "").lower()
    value = value.replace("π", "pi").replace("φ", "phi").replace("γ", "gamma")
    value = value.replace("−", "-").replace("–", "-").replace("—", "-")
    value = re.sub(r"round two \(relay round\)", "", value)
    value = re.sub(r"round two \(group round\)", "", value)
    value = re.sub(r"the uk university integration bee 2025/2026", "", value)
    value = re.sub(r"page \d+", "", value)
    value = re.sub(r"[^a-z0-9]", "", value)
    return value


def page_text(path: str) -> list[str]:
    doc = pymupdf.open(ROOT / path)
    return [page.get_text("text") for page in doc]


def clean_slide(text: str) -> str:
    kept = []
    for line in text.splitlines():
        item = line.strip()
        if not item or item == "Answer" or re.fullmatch(r"Problem \d+", item):
            continue
        if item.startswith("THE UK") or item.startswith("Tiebreaker") or item.startswith("TIEBREAK"):
            continue
        kept.append(item)
    return "\n".join(kept).strip()


def has_integral(text: str) -> bool:
    return "ˆ" in text or "∫" in text or "dx" in text or "dθ" in text or "dθ" in text


def tournament_pairs() -> list[tuple[str, str]]:
    """Each fight slide is the integral, the next slide says Answer, and the
    slide after that is the printed final."""
    pages = page_text(SLIDES)
    pairs = []
    for index, text in enumerate(pages):
        if not has_integral(text):
            continue
        if index + 2 >= len(pages) or "Answer" not in pages[index + 1]:
            continue
        answer = clean_slide(pages[index + 2])
        if answer:
            pairs.append((text, answer))
    return pairs


def best_pair(row_text: str, pairs: list[tuple[str, str]]) -> str | None:
    row_norm = norm(row_text)
    # Short integrands still count when the whole string sits in exactly one slide.
    if len(row_norm) < 8:
        return None
    scores = []
    for problem, answer in pairs:
        page_norm = norm(problem)
        if row_norm and row_norm in page_norm:
            scores.append((len(row_norm), answer))
        elif page_norm and len(page_norm) >= 12 and page_norm in row_norm:
            scores.append((len(page_norm), answer))
    if not scores:
        return None
    scores.sort(key=lambda item: item[0], reverse=True)
    top = scores[0][0]
    answers = {answer for score, answer in scores if score == top}
    if len(answers) != 1:
        return None
    return scores[0][1]


def r3_tiebreakers(rows: list[dict]) -> dict[str, tuple[str, str]]:
    found = {}
    for row in rows:
        if not str(row["id"]).startswith("R3-2024-TB"):
            continue
        path = row["pdf_path"]
        pages = page_text(path)
        answer = ""
        for index, text in enumerate(pages):
            stripped = text.strip()
            if stripped.endswith("Answer") and index + 1 < len(pages):
                answer = clean_slide(pages[index + 1])
        if answer:
            found[row["id"]] = (answer, path)
    return found


def match_same_integrand(source_rows: list[dict], target_rows: list[dict], answers: dict[int, str]) -> dict[str, str]:
    by_print = {}
    for row in source_rows:
        digits = re.search(r"(\d+)$", str(row.get("id") or ""))
        if not digits:
            continue
        number = int(digits.group(1))
        if number not in answers:
            continue
        key = fingerprint(row.get("integrand_plain") or "")
        if len(key) < 6:
            continue
        by_print.setdefault(key, set()).add(number)
    found = {}
    for row in target_rows:
        key = fingerprint(row.get("integrand_plain") or "")
        if len(key) < 6:
            continue
        numbers = by_print.get(key)
        if not numbers or len(numbers) != 1:
            continue
        found[row["id"]] = answers[next(iter(numbers))]
    return found


def collect(rows: list[dict]) -> dict[str, tuple[str, str]]:
    by_id = {row["id"]: row for row in rows}
    assignments: dict[str, tuple[str, str]] = {}

    pairs = tournament_pairs()
    for row in rows:
        if row.get("verify") != "unchecked" or "Tournament_slides" not in str(row.get("pdf_path")):
            continue
        plain = row.get("integrand_plain") or ""
        if has_integral(plain):
            answer = best_pair(plain, pairs)
            if answer:
                assignments[row["id"]] = (answer, SLIDES)
            continue
        cleaned = clean_slide(plain)
        if not cleaned or cleaned.lower() == "answer":
            continue
        if not re.search(r"\d|π|ln|log|√|e|φ|γ", cleaned, re.I):
            continue
        assignments[row["id"]] = (cleaned, SLIDES)

    assignments.update(r3_tiebreakers(rows))

    for number, answer in TIEBREAKER_2022.items():
        row_id = f"R1-2022-TB2022-Q{number:02d}"
        row = by_id.get(row_id)
        if row and row.get("verify") == "unchecked":
            assignments[row_id] = (answer, TB_SCHEME)

    for row in rows:
        if not str(row["id"]).startswith("R2-2021-Relay-"):
            continue
        key = row["id"].removeprefix("R2-2021-Relay-")
        if key in SHUTTLE and row.get("verify") == "unchecked":
            assignments[row["id"]] = (SHUTTLE[key], R2_2021_SCHEME)

    uk_group = [row for row in rows if str(row["id"]).startswith("R2-2025-UK-Group-")]
    sg_group = [row for row in rows if str(row["id"]).startswith("R2-2025-SG-Group-") and row.get("verify") == "unchecked"]
    for row_id, answer in match_same_integrand(uk_group, sg_group, GROUP_2025).items():
        assignments[row_id] = (answer, R2_2025_SCHEME)
    uk_relay = [row for row in rows if str(row["id"]).startswith("R2-2025-UK-Relay-")]
    sg_relay = [row for row in rows if str(row["id"]).startswith("R2-2025-SG-Relay-") and row.get("verify") == "unchecked"]
    for row_id, answer in match_same_integrand(uk_relay, sg_relay, RELAY_2025).items():
        assignments[row_id] = (answer, R2_2025_SCHEME)

    return {
        row_id: (answer, source)
        for row_id, (answer, source) in assignments.items()
        if answer
        and by_id[row_id].get("verify") == "unchecked"
        and not str(by_id[row_id].get("answer_plain") or "").strip()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    rows = [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines()]
    assignments = collect(rows)
    by_pdf = Counter(source for _answer, source in assignments.values())
    print(f"assignments {len(assignments)}")
    for source, count in by_pdf.most_common():
        print(f"{count}\t{source}")
    for row_id, (answer, source) in sorted(assignments.items()):
        flat = answer.replace("\n", " / ")
        print(f"{row_id}\t{flat[:180]}\t{Path(source).name}")

    if not args.write:
        return 0
    for row in rows:
        item = assignments.get(row["id"])
        if item is None:
            continue
        answer, source = item
        row["answer_plain"] = answer
        row["answer_source_pdf"] = source
        row["verify"] = "manual"
    pack = [row for row in rows if row.get("source") == "resource_pack"]
    answered = sum(1 for row in pack if row.get("verify") in {"manual", "sympy"})
    unchecked = sum(1 for row in pack if row.get("verify") == "unchecked")
    print(f"resource answered {answered}/677 unchecked {unchecked}")
    manual = sum(
        1
        for row in rows
        if not str(row.get("id", "")).startswith("SAMPLE-")
        and row.get("source") != "uk_sample"
        and row.get("verify") == "manual"
        and str(row.get("answer_plain") or "").strip()
    )
    old = problem_catalog.EXPECTED_MANUAL
    problem_catalog.EXPECTED_MANUAL = manual
    err = problem_catalog.catalog_problem(rows)
    problem_catalog.EXPECTED_MANUAL = old
    if err:
        print(f"CATALOG {err}", file=sys.stderr)
        return 1
    problem_catalog.dump_records(rows)
    catalog_path = ROOT / "verify" / "problem_catalog.py"
    text = catalog_path.read_text(encoding="utf-8")
    updated = text.replace(f"EXPECTED_MANUAL = {old}", f"EXPECTED_MANUAL = {manual}", 1)
    if updated == text:
        print("catalog constant was not updated", file=sys.stderr)
        return 1
    catalog_path.write_text(updated, encoding="utf-8")
    print(f"wrote records and EXPECTED_MANUAL {old} -> {manual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
