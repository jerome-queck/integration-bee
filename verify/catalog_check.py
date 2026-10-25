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
        rows[0]["answer_sympy"] = "1"
        return
    if name == "missing-cite":
        for row in rows:
            if row.get("verify") == "manual":
                row["answer_source_pdf"] = None
                return
        raise SystemExit("no manual row")
    if name == "yang-invented":
        for row in rows:
            if row.get("id") == "YANG-1.1-P01":
                row["answer_plain"] = "x"
                row["answer_source_pdf"] = row["pdf_path"]
                row["verify"] = "manual"
                return
        raise SystemExit("missing YANG-1.1-P01")
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
        check(show_doc["verify"] == "manual" and "sin(1)" in show_doc["answer_plain"], "show keeps the mark-scheme cite")
        check(show_doc["answer_source_pdf"].endswith("Mark_Scheme_2024_Round_1_UK_University_Integration_Bee.pdf"), "show names the mark scheme")
        selected = run_cli(data, ["problems", "select", "--id", "YANG-1.1-P01", "--format", "json"])
        check(selected.returncode == 0, "select exit")
        select_doc = json.loads(selected.stdout)
        check(select_doc["verify"] == "unchecked" and select_doc["has_answer"] is False, "yang practice stays unanswered")
        check("answer_plain" not in selected.stdout and select_doc.get("integrand_plain"), "select hides the answer")
        wide = run_cli(data, ["problems", "select", "--round", "r1", "--format", "json"])
        check(wide.returncode == 2 and "matched" in wide.stderr, "select refuses many matches")
        missing = run_cli(data, ["problems", "show", "--id", "NO-SUCH", "--format", "json"])
        check(missing.returncode == 1 and "unknown problem" in missing.stderr, "show misses an unknown id")
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
    print(f"OK catalog {problem_catalog.EXPECTED_COUNT} records")
    fail = drive()
    if fail:
        print("FAIL catalog drive")
        return 1
    print("PASS catalog")
    return 0


if __name__ == "__main__":
    sys.exit(main())
