#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPECT = {
    "teaching.tex": "\\input{technique-note.tex}",
    "drills.tex": "\\input{drill-sheet.tex}",
    "solutions.tex": "\\input{solution-sheet.tex}",
}
fail = 0
for unit in sorted((ROOT / "units").glob("[0-9][0-9]-*")):
    for name, first in EXPECT.items():
        path = unit / name
        line = path.read_text().splitlines()[0]
        if line != first:
            print(f"FAIL {path.relative_to(ROOT)} starts with {line!r}")
            fail = 1
sim = (ROOT / "templates" / "round1-sim.tex").read_text()
if "\\input{ib-common.tex}" not in sim or "30 problems" not in sim:
    print("FAIL templates/round1-sim.tex")
    fail = 1
if fail:
    sys.exit(1)
print("PASS templates")
