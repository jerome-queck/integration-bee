#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = (
    "ci",
    "agents",
    "structure",
    "templates",
    "invariants",
    "mutations",
    "verify",
    "doctor",
    "latex",
)


def makefile_missing(text: str) -> list[str]:
    lines = text.splitlines()
    buf: list[str] = []
    grabbing = False
    for line in lines:
        if not grabbing:
            if line.startswith("check:"):
                grabbing = True
                buf.append(line.split(":", 1)[1])
            continue
        buf.append(line)
        if not line.rstrip().endswith("\\"):
            break
    deps = " ".join(part.replace("\\", " ") for part in buf).split()
    return [name for name in REQUIRED if name not in deps]


def workflow_runs_make_check(text: str) -> bool:
    return "run: make check" in text


def sample_guard(text: str) -> str | None:
    if "mktemp -d" not in text or "units/01-foundations-substitution/teaching.tex" not in text:
        return (
            "FAIL scripts/compile-tex.sh must compile "
            "units/01-foundations-substitution/teaching.tex from a temporary directory."
        )
    return None


def self_test() -> None:
    old = "check: agents structure templates invariants mutations verify doctor\n"
    missing = makefile_missing(old)
    if "latex" not in missing or "ci" not in missing:
        print(f"FAIL makefile self-test returned {missing!r}", file=sys.stderr)
        sys.exit(1)
    if makefile_missing("check: " + " ".join(REQUIRED) + "\n"):
        print("FAIL makefile self-test rejected a complete target", file=sys.stderr)
        sys.exit(1)
    if workflow_runs_make_check("run: echo ok\n"):
        print("FAIL workflow self-test accepted a job that skips make check", file=sys.stderr)
        sys.exit(1)
    if not workflow_runs_make_check("        run: make check\n"):
        print("FAIL workflow self-test rejected make check", file=sys.stderr)
        sys.exit(1)
    if sample_guard("latexmk -r templates/latexmkrc teaching.tex\n") is None:
        print("FAIL sample self-test accepted a compile with no off-root sample", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    self_test()
    fail = 0
    makefile = (ROOT / "Makefile").read_text()
    for name in makefile_missing(makefile):
        print(f"FAIL Makefile check target is missing {name}. Put it back on the check: line.")
        fail = 1
    workflow_path = ROOT / ".github" / "workflows" / "check.yml"
    if not workflow_path.is_file() or not workflow_runs_make_check(workflow_path.read_text()):
        print("FAIL .github/workflows/check.yml does not run make check.")
        fail = 1
    guard = sample_guard((ROOT / "scripts" / "compile-tex.sh").read_text())
    if guard:
        print(guard)
        fail = 1
    if fail:
        sys.exit(1)
    print("PASS ci")


if __name__ == "__main__":
    main()
