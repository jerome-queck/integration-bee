#!/usr/bin/env python3
"""Verify all-rounds Resource pack extract matches committed inventory + expected list."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INV = ROOT / "past" / "inventory.json"
EXPECTED = ROOT / "verify" / "all_rounds_expected.txt"
PAST = ROOT / "sources" / "past"

KEY_FILES = [
    "sources/past/r1/2020/2020_Integration_Competition_Problems.pdf",
    "sources/past/r1/2021/2021_Round_1_UK_University_Integration_Bee.pdf",
    "sources/past/r1/2022/2022_Round_1_UK_University_Integration_Bee.pdf",
    "sources/past/r1/2023/2023_Round_1_UK_University_Integration_Bee.pdf",
    "sources/past/r1/2024/2024_Round_1_UK_University_Integration_Bee.pdf",
    "sources/past/r1/2025/2025_Online_Round_1.pdf",
    "sources/past/r2/2021/Group_Round_2021_R2_UK_University_Integration_Bee_Round_Two.pdf",
    "sources/past/r2/2022/Group_Round_R2_2022_UK_University_Integration_Bee_(1).pdf",
    "sources/past/r2/2023/Group_Round_2023_R2_UK_University_Integration_Bee.pdf",
    "sources/past/r2/2024/Group_Round_R2_2024_UK_University_Integration_Bee.pdf",
    "sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf",
    "sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf",
    "sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf",
    "sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf",
    "sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf",
]


def main() -> int:
    fail = 0

    for p in (INV, EXPECTED, ROOT / "past" / "index.md", ROOT / "past" / "README.md"):
        if not p.exists():
            print(f"FAIL missing: {p.relative_to(ROOT)}")
            fail = 1
        else:
            print(f"OK {p.relative_to(ROOT)}")

    if fail:
        print("FAIL all_rounds_check (indexes)")
        return 1

    inv = json.loads(INV.read_text())
    arts = inv.get("artifacts") or []
    counts = inv.get("counts") or {}
    print(f"inventory artifacts={len(arts)} counts={counts.get('by_round')}")

    br = counts.get("by_round") or {}
    if br.get("r1") != 24 or br.get("r2") != 35 or br.get("r3") != 19:
        print(f"FAIL unexpected by_round counts {br} (expected r1=24 r2=35 r3=19)")
        return 1
    print("OK by_round counts r1=24 r2=35 r3=19")

    expected_lines = [ln.strip() for ln in EXPECTED.read_text().splitlines() if ln.strip()]
    present_n = 0
    for rel in expected_lines:
        pdf = ROOT / rel
        if pdf.is_file() and pdf.stat().st_size > 0:
            present_n += 1
    legacy = []
    if PAST.is_dir():
        legacy = [p for p in PAST.glob("[0-9][0-9][0-9][0-9]") if p.is_dir()]
    if legacy:
        for yd in legacy:
            print(f"FAIL legacy path still present: {yd.relative_to(ROOT)} (should be under r1/)")
        print("FAIL all_rounds_check")
        return 1
    if present_n == 0:
        print("SKIP round PDFs absent. Indexes match the committed inventory. Run sources/fetch.sh to check binaries.")
        print("PASS all_rounds_check (no local PDFs)")
        return 0
    if present_n != len(expected_lines):
        print(f"FAIL partial fetch: {present_n} of {len(expected_lines)} PDFs on disk")
        fail = 1

    for rnd in ("r1", "r2", "r3"):
        d = PAST / rnd
        if not d.is_dir():
            print(f"FAIL missing round dir: sources/past/{rnd}/")
            fail = 1
        else:
            print(f"OK sources/past/{rnd}/")

    missing = []
    for rel in expected_lines:
        p = ROOT / rel
        if not p.is_file() or p.stat().st_size == 0:
            missing.append(rel)
    if missing:
        print(f"FAIL {len(missing)} expected PDFs missing/empty (run sources/fetch.sh)")
        for m in missing[:20]:
            print(f"  missing {m}")
        if len(missing) > 20:
            print(f"  ... +{len(missing)-20} more")
        fail = 1
    else:
        print(f"OK all {len(expected_lines)} expected PDFs present")

    for rel in KEY_FILES:
        p = ROOT / rel
        if not p.is_file():
            print(f"FAIL key file missing: {rel}")
            fail = 1
        else:
            print(f"OK key {rel}")

    for a in arts:
        if not a.get("present", True):
            continue
        rel = a["path"]
        p = ROOT / rel
        if not p.is_file():
            print(f"FAIL inventory path missing on disk: {rel}")
            fail = 1

    if fail:
        print("FAIL all_rounds_check")
        return 1
    print("PASS all_rounds_check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
