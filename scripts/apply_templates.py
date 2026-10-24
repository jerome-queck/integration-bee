#!/usr/bin/env python3
"""Point unit tex files at templates/ and drop a personal author name."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KINDS = {
    "teaching.tex": "technique-note.tex",
    "drills.tex": "drill-sheet.tex",
    "solutions.tex": "solution-sheet.tex",
}


def rewrite(path: Path, template: str) -> None:
    text = path.read_text().replace(" (Jerome)", "")
    lines = text.splitlines(keepends=True)
    if lines and lines[0].startswith(f"\\input{{{template}}}"):
        path.write_text(text)
        return
    kept = []
    started = False
    for line in lines:
        if not started:
            if line.startswith("%") or line.startswith("\\documentclass") or line.startswith("\\usepackage"):
                continue
            if line.startswith("\\title") or line.startswith("\\author") or line.startswith("\\date") or line.startswith("\\begin{document}"):
                started = True
            else:
                continue
        kept.append(line)
    path.write_text(f"\\input{{{template}}}\n" + "".join(kept))


def main() -> None:
    for unit in sorted((ROOT / "units").glob("[0-9][0-9]-*")):
        for name, template in KINDS.items():
            rewrite(unit / name, template)
        meta = unit / "meta.yaml"
        if meta.exists():
            rows = []
            for line in meta.read_text().splitlines():
                if line.startswith("latex_note:"):
                    rows.append('latex_note: "Uses templates/ via TEXINPUTS. See templates/README.md."')
                else:
                    rows.append(line)
            meta.write_text("\n".join(rows) + "\n")


if __name__ == "__main__":
    main()
