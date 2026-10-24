#!/usr/bin/env python3
"""Write AGENTS.md from the CLI registry and the feature map."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ENFORCERS = [
    ("Learner state stays uncommitted", ".gitignore"),
    ("AGENTS.md matches the generator", "scripts/check_agents_md.py"),
    ("Published commands match the parser", "scripts/check_agents_md.py"),
    ("Unit notes use the shared templates", "scripts/check_templates.py"),
    ("A unit sample compiles outside the repo root", "scripts/compile-tex.sh"),
    ("Drill answers match SymPy, and a wrong answer fails", "verify/run.sh"),
    ("Past papers do not precede concept units", "verify/unit_order_check.py"),
    ("Tracker and readiness invariants hold", "verify/invariants.py"),
    ("All-rounds indexes match, and PDFs match when fetched", "verify/all_rounds_check.py"),
    ("Official contest PDFs stay out of git", ".gitignore"),
    ("The Yang PDF stays in git", "sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf"),
    ("The check workflow still runs the pack targets", "scripts/check_ci.py"),
]

SCENARIOS = [
    ("You change what doctor, practice, drills, progress, or verify prints or records", ".cursor/skills/verify-integration-bee"),
    ("You change unit order, mock readiness, or tracker writes", ".cursor/skills/formal-verify-integration-bee"),
    ("You teach, mark a photo, or answer an empty message", ".cursor/skills/integration-bee-companion"),
    ("The same mistake shows up twice", "pstack skill `correct`"),
    ("You add a learner-facing command", "pstack skill `create-verification-skill`, then `maintain-verification-skill`"),
    ("You change `verify/model.py`", "pstack skill `maintain-formal-verification-skill`"),
    ("The work is large or easy to get wrong", "pstack skill `poteto-mode`"),
    ("You make a one-way design choice", "`docs/decisions/`"),
]


def features() -> list[str]:
    folder = ROOT / ".cursor" / "skills" / "verify-integration-bee" / "features"
    return sorted(path.name for path in folder.glob("*.md") if path.name != "README.md")


def commands() -> list[dict]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "control-integration-bee"), "--commands-json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def coverage() -> str:
    units = sorted(path.name for path in (ROOT / "units").glob("[0-9][0-9]-*") if path.is_dir())
    drills = sorted((ROOT / "verify").glob("drills_unit*.json"))
    count = 0
    for path in drills:
        count += len(json.loads(path.read_text()))
    return (
        f"Concept units `{units[0]}` through `{units[-1]}` "
        f"({len(units)} directories) have machine drills in `verify/drills_unit*.json` ({count} drills)."
    )


def render() -> str:
    feat_lines = "\n".join(f"- `{name}`" for name in features())
    cmd_lines = "\n".join(f"| `{row['path']}` | {row['summary']} |" for row in commands())
    rule_lines = "\n".join(f"| {rule} | `{path}` |" for rule, path in ENFORCERS)
    scene_lines = "\n".join(f"| {when} | {skill} |" for when, skill in SCENARIOS)
    return f"""# Integration Bee

This repository is the public study pack for the UK University Integration Bee. A learner talks to the companion. The companion uses the CLI. The learner does not run commands.

## Setup

Install Python 3.11 or newer and SymPy.

```bash
python3 -m pip install sympy
```

Install `latexmk` and `pdflatex` when you build PDFs. Point Git at the drift hook once.

```bash
make hooks
```

## Check

Run this before every pull request. CI runs the same command.

```bash
make check
```

`verify/all_rounds_check.py` passes when the fetched Round 1, Round 2, and Round 3 PDFs match `past/inventory.json`. When those PDFs are absent it skips the binary check and still checks the committed indexes.

{coverage()}

## Feature map

The map is `.cursor/skills/verify-integration-bee/features/`.

{feat_lines}

## Agent CLI

`scripts/control-integration-bee` is the only program that writes learner state.

| Command | What it does |
|---|---|
{cmd_lines}

Regenerate this file with `python3 scripts/generate_agents_md.py` after you add a command or a feature file.

## Verifier skills

| Skill | When |
|---|---|
| `.cursor/skills/verify-integration-bee` | Drive the CLI and keep a transcript. |
| `.cursor/skills/formal-verify-integration-bee` | Check unit order, Round 1 readiness, and tracker records. |

## Pstack skills

| Situation | Run |
|---|---|
{scene_lines}

## Boundaries

- Open a pull request for changes. Do not merge it, and do not force-push, unless the operator authorizes that merge.
- Do not commit `progress.local.json`, `trackers/live/`, or `.venv/`.
- Do not commit official contest PDFs. `sources/fetch.sh` downloads them into `sources/past/r1/`, `sources/past/r2/`, and `sources/past/r3/`.
- Do not commit a plaintext copy of the Yang guide. The committed copy is `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`.
- Do not edit `AGENTS.md` by hand.

## Rule to enforcer

| Rule | Enforced by |
|---|---|
{rule_lines}

## Isolation

Set `IB_DATA_DIR` or pass `--data-dir` so two runs do not share tracker files. There is no port. `doctor` does not write. A second writer needs its own data directory.

## Decisions

One-way choices are in `docs/decisions/`.
"""


def main() -> None:
    path = ROOT / "AGENTS.md"
    path.write_text(render())
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
