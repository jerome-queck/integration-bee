#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPECT = {
    "teaching.tex": "\\input{technique-note.tex}",
    "drills.tex": "\\input{drill-sheet.tex}",
    "solutions.tex": "\\input{solution-sheet.tex}",
}
def article_class(unit: Path) -> bool:
    meta = unit / "meta.yaml"
    if not meta.exists():
        return False
    for line in meta.read_text().splitlines():
        if line.startswith("latex_note:") and "article-class" in line:
            return True
    return False


fail = 0
for unit in sorted((ROOT / "units").glob("[0-9][0-9]-*")):
    plain = article_class(unit)
    for name, first in EXPECT.items():
        path = unit / name
        text = path.read_text()
        line = text.splitlines()[0]
        if plain:
            if "\\documentclass" not in text or "\\begin{document}" not in text or "\\end{document}" not in text:
                print(f"FAIL {path.relative_to(ROOT)} is not a self-contained article")
                fail = 1
            continue
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
