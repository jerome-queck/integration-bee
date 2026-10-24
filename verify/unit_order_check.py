#!/usr/bin/env python3
"""Fail if STATE claims a past-paper unit before concept drill units exist."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from model import classify_meta, concept_gap, unit01_problem

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "STATE.md"
UNITS = ROOT / "units"
VERIFY = ROOT / "verify"


def main() -> int:
    state = STATE.read_text() if STATE.exists() else ""
    meta01 = UNITS / "01-foundations-substitution" / "meta.yaml"
    if not meta01.exists():
        print("FAIL unit_order: missing units/01-foundations-substitution/meta.yaml")
        return 1
    meta_txt = meta01.read_text()
    problem = unit01_problem(meta_txt)
    if problem:
        print(f"FAIL unit_order: {problem}")
        return 1

    past_units = []
    concept_units = []
    for m in sorted(UNITS.glob("*/meta.yaml")):
        t = m.read_text()
        uid = m.parent.name
        kind = classify_meta(t)
        if kind == "past":
            past_units.append(uid)
        elif kind == "concept":
            concept_units.append(uid)

    if concept_gap(past_units, concept_units):
        print(f"FAIL unit_order: past-paper units {past_units} before any concept unit")
        return 1

    if re.search(r"past.papers.only|PAST_PAPERS_BEFORE_DRILLS", state, re.I):
        print("FAIL unit_order: STATE claims past-papers-before-drills")
        return 1

    drills = sorted(VERIFY.glob("drills_unit*.json"))
    if not drills:
        print("FAIL unit_order: missing verify/drills_unit*.json")
        return 1

    for uid in concept_units:
        m = re.match(r"^(\d+)-", uid)
        if not m:
            continue
        n = int(m.group(1))
        expected = VERIFY / f"drills_unit{n}.json"
        if not expected.exists():
            print(f"FAIL unit_order: concept unit {uid} missing {expected.name}")
            return 1
        umeta = (UNITS / uid / "meta.yaml").read_text()
        if re.search(r"past_paper:\s*true", umeta):
            print(f"FAIL unit_order: {uid} marked past_paper")
            return 1

    print(f"PASS unit_order (concept={concept_units}, past={past_units}, drills={[p.name for p in drills]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
