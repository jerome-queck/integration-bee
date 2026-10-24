#!/usr/bin/env python3
"""Run unit-order, readiness, and tracker invariants. Mutations must be caught."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import model

ROOT = Path(__file__).resolve().parent.parent
VERIFY = ROOT / "verify"


def catalog() -> list[dict]:
    return json.loads((ROOT / "trackers" / "catalog.json").read_text())["nodes"]


def catalog_ids() -> set[str]:
    return {node["id"] for node in catalog()}


def round1_ids() -> list[str]:
    return [node["id"] for node in catalog() if node.get("gate") == "round1"]


def skill_tree_ids(text: str) -> set[str]:
    found = set()
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cell = line.strip().strip("|").split("|")[0].strip()
        if cell and cell.replace("-", "").isalnum() and cell != "Node" and not cell.startswith("-"):
            if cell[0].isalpha():
                found.add(cell)
    return found


def live_problems() -> list[str]:
    problems = []
    tree = (ROOT / "skill-tree.md").read_text()
    ids = catalog_ids()
    in_tree = skill_tree_ids(tree)
    if ids != in_tree:
        problems.append(f"catalog ids != skill-tree ids: {sorted(ids ^ in_tree)}")
    chapters = {
        1: range(1, 21),
        2: range(1, 11),
        3: range(1, 9),
        4: (1, 2, 4, 5, 6),
        5: range(1, 5),
        6: range(1, 10),
    }
    for major, minors in chapters.items():
        for minor in minors:
            token = f"| {major}.{minor} |"
            if token not in tree:
                problems.append(f"skill-tree missing {token}")
    for phrase in ("DUTIS", "Weierstrass", "King", "Gamma", "Beta", "zeta", "floor", "Wallis", "Catalan", "vector"):
        if phrase not in tree:
            problems.append(f"skill-tree missing syllabus word {phrase}")
    unit01 = (ROOT / "units" / "01-foundations-substitution" / "meta.yaml").read_text()
    hit = model.unit01_problem(unit01)
    if hit:
        problems.append(hit)
    proc = subprocess.run([sys.executable, str(VERIFY / "unit_order_check.py")], capture_output=True, text=True)
    if proc.returncode != 0:
        problems.append(proc.stdout.strip() or proc.stderr.strip() or "unit_order_check failed")
    src = (VERIFY / "unit_order_check.py").read_text()
    if "concept_gap(" not in src or "unit01_problem(" not in src:
        problems.append("unit_order_check no longer calls the shared predicates")
    rounds = subprocess.run(
        [sys.executable, str(VERIFY / "all_rounds_check.py")],
        capture_output=True,
        text=True,
    )
    if rounds.returncode != 0:
        problems.append(rounds.stdout.strip() or "all_rounds_check failed")
    examples = {
        "attempts": ("items", model.attempt_problem),
        "heatmap": ("topics", None),
        "streaks": ("days", None),
        "skill-ticks": ("ticks", None),
        "journal": ("notes", None),
        "mocks": ("sessions", None),
        "session": ("phase", None),
    }
    for name in examples:
        doc = json.loads((ROOT / "trackers" / f"{name}.example.json").read_text())
        if doc.get("example") is not True:
            problems.append(f"{name} example missing example:true")
        err = validate_doc(name, doc, ids)
        if err:
            problems.append(f"{name} example: {err}")
    return problems


def validate_doc(name: str, doc: dict, ids: set[str]) -> str | None:
    if name == "attempts":
        for item in doc.get("items", []):
            err = model.attempt_problem(item)
            if err:
                return err
    elif name == "heatmap":
        return model.heatmap_problem(doc.get("topics", {}))
    elif name == "streaks":
        return model.streak_problem(doc.get("days", []))
    elif name == "skill-ticks":
        return model.tick_problem(doc.get("ticks", {}), ids)
    elif name == "journal":
        for note in doc.get("notes", []):
            err = model.journal_problem(note)
            if err:
                return err
    elif name == "mocks":
        for session in doc.get("sessions", []):
            err = model.mock_session_problem(session)
            if err:
                return err
    elif name == "session":
        return model.session_problem(doc)
    return None


def caught(name: str) -> str | None:
    ids = {"basic-integration"}
    if name == "past-before-concept":
        if model.concept_gap(["past-2020"], []):
            return "concept_gap rejects a past-only list"
    elif name == "unit01-is-past":
        err = model.unit01_problem("past_paper: true\nyang:1.1\nyang:1.2\n")
        if err:
            return err
    elif name == "unit01-missing-yang":
        err = model.unit01_problem("past_paper: false\nkind: concept\n")
        if err:
            return err
    elif name == "unknown-tick":
        err = model.tick_problem({"no-such-node": {"status": "solid"}}, ids)
        if err:
            return err
    elif name == "negative-interval":
        err = model.attempt_problem({"problem_id": "U01-D01", "interval_days": -1, "next_due": "2026-10-25"})
        if err:
            return err
    elif name == "heatmap-fails-exceed":
        err = model.heatmap_problem({"u-sub": {"attempts": 1, "fails": 2}})
        if err:
            return err
    elif name == "mock-before-ready":
        err = model.mock_block_reason({}, ["basic-integration"], cold=False)
        if err:
            return err
    elif name == "duplicate-streak-day":
        err = model.streak_problem(["2026-10-24", "2026-10-24"])
        if err:
            return err
    elif name == "bad-session-phase":
        err = model.session_problem({"phase": "teaching", "node": None, "problem_id": None, "mock_id": None})
        if err:
            return err
    else:
        return None
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect-fail", default=None)
    args = parser.parse_args()
    if args.expect_fail:
        msg = caught(args.expect_fail)
        if not msg:
            print(f"FAIL mutation {args.expect_fail} was not caught")
            return 1
        print(f"PASS mutation {args.expect_fail}: {msg}")
        return 0
    problems = live_problems()
    if problems:
        for item in problems:
            print(f"FAIL invariant: {item}")
        return 1
    print("PASS invariants")
    return 0


if __name__ == "__main__":
    sys.exit(main())
