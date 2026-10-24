#!/usr/bin/env python3
import argparse
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

from generate_agents_md import SCENARIOS, render

ROOT = Path(__file__).resolve().parent.parent


def leaf_paths(parser: argparse.ArgumentParser, prefix: str = "") -> list[str]:
    sub = next(
        (action for action in parser._actions if isinstance(action, argparse._SubParsersAction)),
        None,
    )
    if sub is None:
        return [prefix] if prefix else []
    found = []
    for name, child in sub.choices.items():
        path = f"{prefix} {name}".strip()
        nested = any(isinstance(action, argparse._SubParsersAction) for action in child._actions)
        found.extend(leaf_paths(child, path) if nested else [path])
    return found


def command_drift(published: list[str], parsed: list[str]) -> str | None:
    if set(published) == set(parsed):
        return None
    missing = sorted(set(parsed) - set(published))
    extra = sorted(set(published) - set(parsed))
    parts = []
    if missing:
        parts.append("parser has " + ", ".join(missing) + " but COMMANDS does not")
    if extra:
        parts.append("COMMANDS has " + ", ".join(extra) + " but the parser does not")
    return (
        "FAIL command list drifted. "
        + "; ".join(parts)
        + ". Update COMMANDS in scripts/control-integration-bee, then run python3 scripts/generate_agents_md.py."
    )


def missing_scenarios(rows: list[tuple[str, str]], root: Path) -> list[str]:
    missing = []
    for _when, skill in rows:
        text = skill.strip().strip("`")
        if text.startswith("pstack "):
            continue
        if not (text.startswith(".") or text.startswith("docs/")):
            continue
        if not (root / text).exists():
            missing.append(text)
    return missing


def self_test() -> None:
    drifted = command_drift(["doctor"], ["doctor", "practice list"])
    if drifted is None or "practice list" not in drifted:
        print("FAIL command drift self-test did not name practice list", file=sys.stderr)
        sys.exit(1)
    if command_drift(["doctor"], ["doctor"]) is not None:
        print("FAIL command drift self-test rejected a matching list", file=sys.stderr)
        sys.exit(1)
    with tempfile.TemporaryDirectory() as tmp:
        got = missing_scenarios([("x", "docs/nope/"), ("y", "pstack skill `correct`")], Path(tmp))
    if got != ["docs/nope/"]:
        print(f"FAIL scenario self-test returned {got!r}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    self_test()
    try:
        expected = render()
    except subprocess.CalledProcessError as exc:
        print("FAIL AGENTS.md check could not read the command list.", file=sys.stderr)
        err = (exc.stderr or "").strip()
        if err:
            print(err, file=sys.stderr)
        print("Install SymPy, then run python3 scripts/generate_agents_md.py.", file=sys.stderr)
        sys.exit(1)

    cli = runpy.run_path(str(ROOT / "scripts" / "control-integration-bee"))
    published = [row["path"] for row in cli["COMMANDS"]]
    parsed = leaf_paths(cli["build_parser"]())
    fail = 0
    drift = command_drift(published, parsed)
    if drift:
        print(drift, file=sys.stderr)
        fail = 1
    for rel in missing_scenarios(SCENARIOS, ROOT):
        print(
            f"FAIL missing scenario path {rel}. It is listed in scripts/generate_agents_md.py SCENARIOS.",
            file=sys.stderr,
        )
        fail = 1
    current = (ROOT / "AGENTS.md").read_text()
    if current != expected:
        print("AGENTS.md drifted. Run python3 scripts/generate_agents_md.py", file=sys.stderr)
        fail = 1
    if fail:
        sys.exit(1)
    print("PASS AGENTS.md")


if __name__ == "__main__":
    main()
