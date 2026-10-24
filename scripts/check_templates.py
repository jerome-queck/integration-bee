#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPECT = {
    "teaching.tex": "\\input{technique-note.tex}",
    "drills.tex": "\\input{drill-sheet.tex}",
    "solutions.tex": "\\input{solution-sheet.tex}",
}


def first_code_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("%"):
            continue
        return stripped
    return ""


def wired(line: str, expected: str) -> bool:
    if line == expected:
        return True
    if not line.startswith(expected):
        return False
    nxt = line[len(expected):len(expected) + 1]
    return nxt == "" or not nxt.isalnum()


fail = 0
for unit in sorted((ROOT / "units").glob("[0-9][0-9]-*")):
    for name, expected in EXPECT.items():
        path = unit / name
        line = first_code_line(path.read_text())
        if not wired(line, expected):
            print(f"FAIL {path.relative_to(ROOT)} starts with {line!r}")
            fail = 1
sim = (ROOT / "templates" / "round1-sim.tex").read_text()
if "\\input{ib-common.tex}" not in sim or "30 problems" not in sim:
    print("FAIL templates/round1-sim.tex")
    fail = 1
if fail:
    sys.exit(1)
print("PASS templates")
