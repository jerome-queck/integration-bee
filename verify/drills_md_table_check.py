"""Every row of a unit drills.md table has as many cells as its header (audit D).

An unescaped | inside a LaTeX cell (\\left| ... \\right|) splits the cell and shifts
the answer column, so the rendered table shows the wrong answer.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def cells(line: str) -> int:
    return len(re.split(r"(?<!\\)\|", line.strip().strip("|")))


def check(path: Path) -> list[str]:
    bad, width = [], None
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.lstrip().startswith("|"):
            width = None
            continue
        if width is None:
            width = cells(line)
        elif cells(line) != width:
            bad.append(f"{path.relative_to(ROOT)}:{number} has {cells(line)} cells, header has {width}")
    return bad


def main() -> int:
    bad = [b for p in sorted(ROOT.glob("units/*/drills.md")) for b in check(p)]
    sample = ROOT / "verify" / "_drills_md_sample.md"
    sample.write_text("| a | b |\n|---|---|\n| \\left|x\\right| | y |\n", encoding="utf-8")
    try:
        if not check(sample):
            bad.append("must-fail: a split LaTeX cell was accepted")
    finally:
        sample.unlink()
    for line in bad:
        print("FAIL", line)
    if not bad:
        print("PASS drills.md tables keep their column count")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
