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
    ("All-rounds indexes match, and the reference PDFs match", "verify/all_rounds_check.py"),
    ("Official reference PDFs stay in git", "scripts/check_structure.py"),
    ("The Yang PDF stays in git", "sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf"),
    ("The check workflow still runs the pack targets", "scripts/check_ci.py"),
]

SKILL_NAMES = (
    "integration-bee-companion",
    "verify-integration-bee",
    "formal-verify-integration-bee",
)
CANONICAL_SKILL_ROOT = ".agents/skills"
ADAPTER_ROOTS = (".cursor/skills", ".claude/skills")

HARNESS_MD = """## Harness

Canonical skill files are `.agents/skills/<name>/SKILL.md`. Codex loads that directory. `.cursor/skills/<name>` and `.claude/skills/<name>` are symlinks to the same directory. Cursor and Claude Code load that text. Edit `.agents/skills`. Git must store the symlinks (`core.symlinks=true`, the default on Linux and macOS).

Claude Code reads this file when the repository has no `CLAUDE.md`.

A new person follows one getting-started section in `README.md`: Codex, Claude, or Cursor. Each section lists the Python packages, the TeX and Java packages for `make check`, `scripts/control-integration-bee`, and the pstack plugin install for that harness. The plugin repository is https://github.com/michael-denyer/pstack-claude.

When a row below names a pstack skill, open `skills/<name>/SKILL.md` in the cache for the harness you are running. The version directory is the one the installer created.

| Harness | Skill cache |
|---|---|
| Codex | `${CODEX_HOME:-$HOME/.codex}/plugins/cache/pstack-claude/pstack/<version>/skills` |
| Claude | `${CLAUDE_CODE_PLUGIN_CACHE_DIR:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins}/cache/pstack-claude/pstack/<version>/skills` |
| Cursor | `~/.cursor/plugins/cache/<marketplace>/<plugin>/<version>/skills` |

An installed Codex copy at version 0.9.102 keeps its skills in `~/.codex/plugins/cache/pstack-claude/pstack/0.9.102/skills`. If that file is missing, the person running the agent installs the plugin from the matching `README.md` section and starts a new session.
"""

SCENARIOS = [
    ("You change what doctor, practice, drills, problems, progress, turn, or verify prints or records", f"{CANONICAL_SKILL_ROOT}/verify-integration-bee"),
    ("You change unit order, mock readiness, or tracker writes", f"{CANONICAL_SKILL_ROOT}/formal-verify-integration-bee"),
    ("You teach, mark a photo, or answer an empty message", f"{CANONICAL_SKILL_ROOT}/integration-bee-companion"),
    ("The same mistake shows up twice", "pstack skill `correct` from the harness plugin cache"),
    ("You add a learner-facing command", "pstack skill `create-verification-skill`, then `maintain-verification-skill`, from the harness plugin cache"),
    ("You change `verify/model.py`", "pstack skill `maintain-formal-verification-skill` from the harness plugin cache"),
    ("The work is large or easy to get wrong", "pstack skill `poteto-mode` from the harness plugin cache"),
    ("You make a one-way design choice", "`docs/decisions/`"),
]


def features() -> list[str]:
    folder = ROOT / CANONICAL_SKILL_ROOT / "verify-integration-bee" / "features"
    return sorted(path.name for path in folder.glob("*.md") if path.name != "README.md")


def commands() -> list[dict]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "control-integration-bee"), "--commands-json"],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def catalog_count() -> int:
    path = ROOT / "problems" / "records.jsonl"
    return sum(1 for line in path.read_text().splitlines() if line.strip())


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

Install Python 3.11 or newer, SymPy, and PyYAML.

```bash
python3 -m pip install sympy pyyaml
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

`verify/all_rounds_check.py` passes when the Round 1, Round 2, and Round 3 PDFs match `past/inventory.json`. The check requires the committed PDFs.

{coverage()}

`problems/records.jsonl` holds {catalog_count()} contest, Yang, and sample problems. `problems list` hides answers. `problems show` prints a stored cite.

{HARNESS_MD}
## Feature map

The map is `{CANONICAL_SKILL_ROOT}/verify-integration-bee/features/`.

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
| `{CANONICAL_SKILL_ROOT}/verify-integration-bee` | Drive the CLI and keep a transcript. |
| `{CANONICAL_SKILL_ROOT}/formal-verify-integration-bee` | Check unit order, Round 1 readiness, and tracker records. |

## Pstack skills

| Situation | Run |
|---|---|
{scene_lines}

## Boundaries

- Open a pull request for changes. Do not merge it, and do not force-push, unless the operator authorizes that merge.
- Do not commit `progress.local.json`, `trackers/live/`, or `.venv/`.
- The unpacked contest PDFs and the site PDFs are committed reference copies under `sources/past/` and `sources/`. `sources/fetch.sh` can still verify checksums. Do not commit `Resource_pack.zip`.
- Do not commit a plaintext copy of the Yang guide. The committed copy is `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`.
- Do not edit `AGENTS.md` by hand.

## Rule to enforcer

| Rule | Enforced by |
|---|---|
{rule_lines}

## Isolation

Set `IB_DATA_DIR` or pass `--data-dir` so two runs do not share tracker files. `IB_USER` names the `submissions/` folder for a photo mark and defaults to `default`. There is no port. `doctor` does not write. A second learner needs a separate data directory.

## Decisions

One-way choices are in `docs/decisions/`.

Before editing pack manuals, read the [source conflicts registry](docs/decisions/0016-pack-source-holds.md). Preserve conflicting source marks in the notes, certify the printed problem with an exact gate-accepted answer, and update answer citations, grading fixtures, and counts together. Do not invent agreement with a wrong mark.
"""


def main() -> None:
    path = ROOT / "AGENTS.md"
    path.write_text(render())
    print(f"wrote {path}")


if __name__ == "__main__":
    main()
