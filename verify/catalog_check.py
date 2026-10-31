#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))

import pack_gate  # noqa: E402
import problem_catalog  # noqa: E402

CLI = ROOT / "scripts" / "control-integration-bee"


def mutate(rows: list[dict], name: str) -> None:
    if name == "invented-sympy":
        for row in rows:
            if row.get("verify") != "sympy":
                row["answer_sympy"] = "1"
                return
        raise SystemExit("no unproved row")
    if name == "missing-cite":
        # Handoff O cleared remaining manuals; any cited answer still proves cite/answer coupling.
        for row in rows:
            if row.get("answer_plain") and row.get("answer_source_pdf"):
                row["answer_source_pdf"] = None
                return
        raise SystemExit("no cited answer")
    if name == "yang-invented":
        ident = problem_catalog.first_unchecked_yang(rows)
        for row in rows:
            if row.get("id") == ident:
                row["answer_plain"] = "x"
                row["answer_source_pdf"] = row["pdf_path"]
                row["verify"] = "manual"
                return
        raise SystemExit(f"missing {ident}")
    if name == "dropped-record":
        rows.pop()
        return
    raise SystemExit(f"unknown mutation {name}")


def run_cli(data: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["IB_DATA_DIR"] = str(data)
    return subprocess.run(
        [sys.executable, str(CLI), *args],
        text=True,
        capture_output=True,
        env=env,
        cwd=ROOT,
    )


def drive() -> int:
    fail = 0

    def check(cond: bool, label: str) -> None:
        nonlocal fail
        if cond:
            print(f"OK {label}")
        else:
            print(f"FAIL {label}")
            fail = 1

    with tempfile.TemporaryDirectory() as tmp:
        data = Path(tmp)
        listed = run_cli(data, ["problems", "list", "--round", "r1", "--format", "json"])
        check(listed.returncode == 0, "list exit")
        payload = json.loads(listed.stdout)
        ids = [row["id"] for row in payload["problems"]]
        check(payload["count"] == 280 and "R1-2024-Q01" in ids, "round 1 list")
        check("answer_plain" not in listed.stdout and "worked_solution" not in listed.stdout, "list hides answers")
        shown = run_cli(data, ["problems", "show", "--id", "R1-2024-Q01", "--format", "json"])
        check(shown.returncode == 0, "show exit")
        show_doc = json.loads(shown.stdout)
        check(show_doc["verify"] == "sympy" and "sin(1)" in show_doc["answer_plain"], "show keeps the mark-scheme cite")
        check(show_doc["answer_source_pdf"].endswith("Mark_Scheme_2024_Round_1_UK_University_Integration_Bee.pdf"), "show names the mark scheme")
        for problem_id in ("R1-2022-MIT-TB-Q01", "R1-2022-Oxford-Q01", "R1-2022-TB2022-Q01"):
            resolved = run_cli(data, ["problems", "show", "--id", problem_id, "--format", "json"])
            resolved_doc = json.loads(resolved.stdout)
            check(
                resolved.returncode == 0 and resolved_doc["verify"] == "sympy"
                and all(resolved_doc[field] == "1" for field in ("answer_plain", "answer_sympy", "answer_latex")),
                f"{problem_id} shows the proved value 1 for the printed limits",
            )
        proved = run_cli(data, ["problems", "select", "--id", "YANG-1.1-P01", "--format", "json"])
        check(proved.returncode == 0, "select proved yang exit")
        proved_doc = json.loads(proved.stdout)
        check(proved_doc["verify"] == "sympy" and proved_doc["has_answer"] is True, "YANG-1.1-P01 is proved")
        check("answer_plain" not in proved.stdout and proved_doc.get("integrand_plain"), "select hides the proved answer")
        unchecked_id = problem_catalog.first_unchecked_yang()
        selected = run_cli(data, ["problems", "select", "--id", unchecked_id, "--format", "json"])
        check(selected.returncode == 0, "select exit")
        select_doc = json.loads(selected.stdout)
        check(select_doc["verify"] == "unchecked" and select_doc["has_answer"] is False, "yang practice stays unanswered")
        check("answer_plain" not in selected.stdout and select_doc.get("integrand_plain"), "select hides the answer")
        wide = run_cli(data, ["problems", "select", "--round", "r1", "--format", "json"])
        check(wide.returncode == 2 and "matched" in wide.stderr, "select refuses many matches")
        missing = run_cli(data, ["problems", "show", "--id", "NO-SUCH", "--format", "json"])
        check(missing.returncode == 1 and "unknown problem" in missing.stderr, "show misses an unknown id")
        listed_sample = run_cli(data, ["problems", "list", "--round", "sample", "--format", "json"])
        check(listed_sample.returncode == 0, "sample list exit")
        sample_payload = json.loads(listed_sample.stdout)
        sample_ids = [row["id"] for row in sample_payload["problems"]]
        check(sample_payload["count"] == 20 and sample_ids[0] == "SAMPLE-Q01" and sample_ids[-1] == "SAMPLE-Q20", "sample list")
        check("answer_plain" not in listed_sample.stdout and "answer_sympy" not in listed_sample.stdout, "sample list hides answers")
        shown_sample = run_cli(data, ["problems", "show", "--id", "SAMPLE-Q17", "--format", "json"])
        check(shown_sample.returncode == 0, "sample show exit")
        sample_doc = json.loads(shown_sample.stdout)
        check(sample_doc["verify"] == "sympy" and sample_doc["answer_sympy"] == "E*x", "SAMPLE-Q17 grades e*x")
        check("x^(1/ln x)" in sample_doc["integrand_plain"], "SAMPLE-Q17 shows the power")
        mock_meta = (ROOT / "past" / "mocks" / "mock01-meta.yaml").read_text(encoding="utf-8")
        q17_note = mock_meta.split("id: SAMPLE-Q17", 1)[1].split("- id:", 1)[0]
        check("mark e*x+C as correct" in q17_note and "ln|ln x|+C as correct" not in q17_note,
              "mock01 SAMPLE-Q17 note marks e*x+C (audit A8)")
        selected_sample = run_cli(data, ["problems", "select", "--id", "SAMPLE-Q05", "--format", "json"])
        check(selected_sample.returncode == 0, "sample select exit")
        selected_doc = json.loads(selected_sample.stdout)
        check(selected_doc["verify"] == "sympy" and selected_doc["has_answer"] is True, "proved sample keeps a cited answer")
        check("answer_plain" not in selected_sample.stdout, "sample select hides the answer")
        check(list(data.glob("*")) == [], "catalog commands write nothing")
    return fail


def main() -> int:
    args = sys.argv[1:]
    rows = problem_catalog.load_records()
    if args[:1] == ["--expect-fail"]:
        if len(args) != 2:
            print("usage: catalog_check.py --expect-fail NAME", file=sys.stderr)
            return 2
        mutate(rows, args[1])
        err = problem_catalog.catalog_problem(rows)
        if not err:
            print(f"FAIL mutation {args[1]} was accepted")
            return 1
        print(f"PASS mutation {args[1]} ({err})")
        return 0
    if args:
        print(f"unknown args {args}", file=sys.stderr)
        return 2
    err = problem_catalog.catalog_problem(rows)
    if err:
        print(f"FAIL catalog {err}")
        return 1
    proof = pack_gate.reprove_rows(rows)
    if proof:
        print(f"FAIL catalog {proof}")
        return 1
    tampered = [dict(row) for row in rows]
    for row in tampered:
        if row.get("verify") == "sympy":
            row["answer_sympy"] = "999"
            row["answer_latex"] = "999"
            lied = pack_gate.reprove_rows([row])
            if not lied:
                print("FAIL tampered sympy row was accepted")
                return 1
            print(f"PASS tampered sympy row ({lied})")
            break
    print(
        f"OK catalog {problem_catalog.EXPECTED_COUNT} pack records, "
        f"{problem_catalog.SAMPLE_COUNT} sample records"
    )
    fail = drive()
    if fail:
        print("FAIL catalog drive")
        return 1
    print("PASS catalog")
    return 0


if __name__ == "__main__":
    sys.exit(main())
