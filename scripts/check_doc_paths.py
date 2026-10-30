#!/usr/bin/env python3
"""Fail when repo markdown names a path or skill that does not exist.

Checks every tracked *.md outside sources/ for:
- relative markdown links `[text](path)`;
- backticked repo paths that start with a top-level tracked directory or file
  (e.g. `scripts/setup.py`, `.agents/skills/x/SKILL.md`), skipping templates
  that contain <, >, *, {, $ or ...;
- `.agents/skills/<name>` skill references.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = ("sources/",)
LINK = re.compile(r"\[[^\]]*\]\(([^)\s#]+)(?:#[^)]*)?\)")
TICK = re.compile(r"`([^`\s]+)`")
TEMPLATE = re.compile(r"[<>*{}$]|\.\.\.|\\|YYYY|NNNN|unitN\b")


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.split()


def roots(files: list[str]) -> set[str]:
    tops = {f.split("/", 1)[0] for f in files}
    return {t for t in tops if not t.endswith(".md")} | {".agents", ".cursor", ".claude"}


def ignored(path: str) -> bool:
    """Gitignored runtime or fetched files (trackers/live/, caches) may be named."""
    proc = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT)
    return proc.returncode == 0


def check_text(rel: str, text: str, tops: set[str]) -> list[str]:
    errors = []
    base = (ROOT / rel).parent
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target) or TEMPLATE.search(target):
            continue
        if not (base / target).exists():
            errors.append(f"{rel}: link {target} does not exist")
    for token in TICK.findall(text):
        token = token.rstrip(".,:;")
        if TEMPLATE.search(token) or "/" not in token or "=" in token or "(" in token:
            continue
        if token.split("/", 1)[0] not in tops:
            continue
        path = token.split(":", 1)[0]
        if not (ROOT / path).exists() and not ignored(path):
            errors.append(f"{rel}: path `{token}` does not exist")
    return errors


def self_test() -> None:
    tops = {"scripts", ".agents"}
    if not check_text("README.md", "`scripts/nope.py`", tops):
        sys.exit("FAIL doc-paths self-test accepted a missing path")
    if check_text("README.md", "`scripts/setup.py` `scripts/<name>.py` [x](https://e.com)", tops):
        sys.exit("FAIL doc-paths self-test rejected a real path or template")
    if not check_text("README.md", "[x](docs/nope.md)", tops):
        sys.exit("FAIL doc-paths self-test accepted a missing link")


def main() -> int:
    self_test()
    files = tracked()
    tops = roots(files)
    errors = []
    for rel in files:
        if not rel.endswith(".md") or rel.startswith(SKIP_DIRS):
            continue
        path = ROOT / rel
        if path.is_file():
            errors.extend(check_text(rel, path.read_text(errors="replace"), tops))
    for err in errors:
        print("FAIL " + err)
    if errors:
        return 1
    print("PASS doc paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())
