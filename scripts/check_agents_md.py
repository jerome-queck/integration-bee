#!/usr/bin/env python3
import argparse
import os
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

from generate_agents_md import (
    ADAPTER_ROOTS,
    CANONICAL_SKILL_ROOT,
    SCENARIOS,
    SKILL_NAMES,
    render,
    render_skills,
)

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


HARNESS_HEADINGS = ("Codex", "Claude", "Cursor")

SECTION_MARKERS = (
    "python3 -m pip install -r requirements.txt",
    "git clone https://github.com/jerome-queck/integration-bee.git",
    "scripts/control-integration-bee doctor",
    "sudo apt-get install -y latexmk texlive-latex-recommended texlive-fonts-recommended default-jre-headless",
    "pdflatex",
    "Java 11",
    "https://github.com/michael-denyer/pstack-claude",
    "poteto-mode",
    "skills/<skill-name>/SKILL.md",
)

HARNESS_MARKERS = {
    "Codex": (
        "codex plugin marketplace add michael-denyer/pstack-claude",
        "codex plugin add pstack@pstack-claude",
        ".codex/plugins/cache/pstack-claude/pstack",
        "$integration-bee-companion",
    ),
    "Claude": (
        "/plugin marketplace add michael-denyer/pstack-claude",
        "/plugin install pstack@pstack-claude",
        ".claude/plugins",
        "/integration-bee-companion",
    ),
    "Cursor": (
        "Cursor marketplace",
        ".cursor/plugins/cache",
        "integration-bee-companion",
    ),
}

FILE_MARKERS = {
    "README.md": (
        ".agents/skills/setup-integration-bee/SKILL.md",
        "scripts/setup.py",
        "docs/setup-manual.md",
        "docs/architecture.md",
        "mermaid",
    ),
    "docs/setup-manual.md": (
        ".agents/skills/integration-bee-companion/SKILL.md",
        ".agents/skills/verify-integration-bee/SKILL.md",
        ".agents/skills/formal-verify-integration-bee/SKILL.md",
        ".cursor/skills/",
        ".claude/skills/",
    ),
    "COMPANION_SPEC.md": (
        ".agents/skills/integration-bee-companion/SKILL.md",
        ".cursor/skills/integration-bee-companion",
        ".claude/skills/integration-bee-companion",
        "scripts/control-integration-bee turn apply",
        "README.md",
        "symlink",
    ),
}

AGENTS_MARKERS = (
    ".agents/skills/",
    ".cursor/skills/",
    ".claude/skills/",
    "symlinks",
    "https://github.com/michael-denyer/pstack-claude",
    ".codex/plugins/cache/pstack-claude/pstack",
    ".claude}/plugins}/cache/pstack-claude/pstack",
    "~/.cursor/plugins/cache/",
    "README.md",
    "docs/setup-manual.md",
    ".agents/skills/setup-integration-bee/SKILL.md",
    "poteto-mode",
    "core.symlinks",
    "heavy",
    "make sanity",
    "learning-capture.md",
    "force-push",
    "docs/architecture.md",
)

FORBIDDEN = (
    "out of scope",
    "open in Cursor",
    "/statechart",
    "/poteto-mode",
    "/maintain-formal-verification-skill",
)


def harness_sections(text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for name in HARNESS_HEADINGS:
        marker = f"### {name}\n"
        start = text.find(marker)
        if start < 0:
            found[name] = ""
            continue
        rest = text[start + len(marker) :]
        cuts = [pos for pos in (rest.find("\n## "), rest.find("\n### ")) if pos >= 0]
        end = min(cuts) if cuts else len(rest)
        found[name] = rest[:end]
    return found


def section_gaps(text: str) -> list[str]:
    gaps = []
    sections = harness_sections(text)
    for name in HARNESS_HEADINGS:
        body = sections[name]
        if not body:
            gaps.append(f"missing section ### {name}")
            continue
        for marker in SECTION_MARKERS + HARNESS_MARKERS[name]:
            if marker not in body:
                gaps.append(f"### {name} missing {marker}")
    return gaps


def file_gaps(text: str, markers: tuple[str, ...]) -> list[str]:
    return [marker for marker in markers if marker not in text]


def forbidden_hits(text: str) -> list[str]:
    return [phrase for phrase in FORBIDDEN if phrase in text]


def adapter_errors(root: Path) -> list[str]:
    errors = []
    expect_link = f"../../{CANONICAL_SKILL_ROOT}"
    for name in SKILL_NAMES:
        canon = root / CANONICAL_SKILL_ROOT / name
        if canon.is_symlink():
            errors.append(f"{CANONICAL_SKILL_ROOT}/{name} must be the real directory")
        if not (canon / "SKILL.md").is_file():
            errors.append(f"missing {CANONICAL_SKILL_ROOT}/{name}/SKILL.md")
        for adapter in ADAPTER_ROOTS:
            link = root / adapter / name
            rel = f"{adapter}/{name}"
            if not link.is_symlink():
                errors.append(f"{rel} must be a symlink")
                continue
            raw = os.readlink(link)
            if raw != f"{expect_link}/{name}":
                errors.append(f"{rel} points at {raw}")
            elif not link.resolve().samefile(canon):
                errors.append(f"{rel} does not resolve to the canonical skill")
    return errors


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
    sample = "### Codex\npython3 -m pip install sympy pyyaml\n### Claude\n### Cursor\n"
    gaps = section_gaps(sample)
    if not any(gap.startswith("### Codex missing") for gap in gaps):
        print(f"FAIL section self-test ignored a thin Codex section: {gaps!r}", file=sys.stderr)
        sys.exit(1)
    if not any("### Claude missing" in gap for gap in gaps):
        print(f"FAIL section self-test kept a thin Claude section: {gaps!r}", file=sys.stderr)
        sys.exit(1)
    if "missing section ### Claude" not in section_gaps("### Codex\nnope\n"):
        print("FAIL section self-test missed a missing heading", file=sys.stderr)
        sys.exit(1)
    if file_gaps("hello", ("hello", "missing")) != ["missing"]:
        print("FAIL file marker self-test", file=sys.stderr)
        sys.exit(1)
    if forbidden_hits("open in Cursor") != ["open in Cursor"]:
        print("FAIL forbidden self-test", file=sys.stderr)
        sys.exit(1)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        canon = root / CANONICAL_SKILL_ROOT / "integration-bee-companion"
        canon.mkdir(parents=True)
        (canon / "SKILL.md").write_text("skill\n")
        adapter = root / ".cursor/skills"
        adapter.mkdir(parents=True)
        os.symlink(f"../../{CANONICAL_SKILL_ROOT}/integration-bee-companion", adapter / "integration-bee-companion")
        # The full adapter check expects every skill. One link must still resolve.
        link = adapter / "integration-bee-companion"
        if os.readlink(link) != f"../../{CANONICAL_SKILL_ROOT}/integration-bee-companion":
            print("FAIL symlink self-test stored the wrong target", file=sys.stderr)
            sys.exit(1)
        if not link.resolve().samefile(canon):
            print("FAIL symlink self-test did not resolve", file=sys.stderr)
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
    if (ROOT / "docs" / "skills.md").read_text() != render_skills():
        print("docs/skills.md drifted. Run python3 scripts/generate_agents_md.py", file=sys.stderr)
        fail = 1
    for marker in file_gaps(expected, AGENTS_MARKERS):
        print(f"FAIL AGENTS.md missing harness marker {marker}", file=sys.stderr)
        fail = 1
    for rel, markers in FILE_MARKERS.items():
        text = (ROOT / rel).read_text()
        for marker in file_gaps(text, markers):
            print(f"FAIL {rel} missing {marker}", file=sys.stderr)
            fail = 1
    onboarding = (
        ROOT / "docs" / "setup-manual.md",
        ROOT / CANONICAL_SKILL_ROOT / "integration-bee-companion" / "SKILL.md",
    )
    for path in onboarding:
        gaps = section_gaps(path.read_text())
        for gap in gaps:
            print(f"FAIL {path.relative_to(ROOT)} {gap}", file=sys.stderr)
            fail = 1
    scanned = [ROOT / "README.md", ROOT / "docs" / "setup-manual.md", ROOT / "COMPANION_SPEC.md", ROOT / "AGENTS.md"]
    scanned.extend((ROOT / CANONICAL_SKILL_ROOT).rglob("*.md"))
    for path in scanned:
        for phrase in forbidden_hits(path.read_text()):
            print(f"FAIL {path.relative_to(ROOT)} contains {phrase!r}", file=sys.stderr)
            fail = 1
    for error in adapter_errors(ROOT):
        print(f"FAIL {error}", file=sys.stderr)
        fail = 1
    if fail:
        sys.exit(1)
    print("PASS AGENTS.md")


if __name__ == "__main__":
    main()
