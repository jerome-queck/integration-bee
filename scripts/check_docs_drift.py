#!/usr/bin/env python3
"""Fail when code changes on this branch without the matching docs markdown.

Compares HEAD with the merge base of DOCS_DRIFT_BASE (default origin/main).
Each rule says: if any file under `code` changed, at least one file under
`docs` must change too. A commit in the range whose message contains a line
`Docs-unchanged: <reason>` waives the check. With no base ref (shallow clone)
it prints SKIP and passes; CI fetches full history so it runs there.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RULES = [
    (
        "setup entry point and pinned deps",
        ("scripts/setup.py", "requirements.txt"),
        ("docs/setup-manual.md", ".agents/skills/setup-integration-bee/", "README.md"),
    ),
    (
        "companion CLI and turn contract",
        ("scripts/control-integration-bee", "verify/turn_contract.py", "verify/model.py"),
        ("docs/architecture.md", "COMPANION_SPEC.md", ".agents/skills/", "docs/decisions/"),
    ),
    (
        "check targets and CI",
        ("Makefile", ".github/workflows/"),
        ("docs/setup-manual.md", "docs/architecture.md", "scripts/generate_agents_md.py"),
    ),
]


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


def hits(changed: list[str], prefixes: tuple[str, ...]) -> list[str]:
    return [f for f in changed if f.startswith(prefixes)]


def violations(changed: list[str]) -> list[str]:
    out = []
    for name, code, docs in RULES:
        touched = hits(changed, code)
        if touched and not hits(changed, docs):
            out.append(f"{name}: {', '.join(touched)} changed but none of {', '.join(docs)} did")
    return out


def self_test() -> None:
    if not violations(["scripts/setup.py"]):
        sys.exit("FAIL docs-drift self-test accepted setup.py without docs")
    if violations(["scripts/setup.py", "docs/setup-manual.md"]):
        sys.exit("FAIL docs-drift self-test rejected setup.py with docs")
    if violations(["units/01-foundations-substitution/teaching.tex"]):
        sys.exit("FAIL docs-drift self-test flagged an unrelated file")


def main() -> int:
    self_test()
    base_ref = os.environ.get("DOCS_DRIFT_BASE", "origin/main")
    base = git("merge-base", base_ref, "HEAD")
    if base.returncode != 0:
        print(f"SKIP docs drift: no {base_ref} in this clone")
        return 0
    base_sha = base.stdout.strip()
    changed = git("diff", "--name-only", base_sha).stdout.split()
    changed += git("diff", "--name-only", "--cached").stdout.split()
    log = git("log", "--format=%B", f"{base_sha}..HEAD").stdout
    if "\nDocs-unchanged:" in "\n" + log:
        print("PASS docs drift (waived by Docs-unchanged trailer)")
        return 0
    errors = violations(sorted(set(changed)))
    for err in errors:
        print("FAIL docs drift " + err)
    if errors:
        print("Update the docs, or add a commit trailer `Docs-unchanged: <reason>`.")
        return 1
    print("PASS docs drift")
    return 0


if __name__ == "__main__":
    sys.exit(main())
