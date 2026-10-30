# Integration Bee

This repository is the public study pack for the UK University Integration Bee. A learner talks to the companion. The companion uses the CLI. The learner does not run commands.

## Setup

Run `python3 scripts/setup.py` (Windows: `py scripts\setup.py`). It is the setup skill `.agents/skills/setup-integration-bee/SKILL.md`: it makes `.venv/` from the pinned `requirements.txt` and runs `doctor`. Manual steps, TeX, Java, and pstack are in `docs/setup-manual.md`. Point Git at the drift hook once with `make hooks`. Install Python 3.11 or newer, SymPy, and PyYAML by hand only if the script cannot run.

## Gates

- Run `make check` before every pull request. CI runs the same command. On a shared box, run it through `/home/box/box-ops/heavy --bot <bot> --class test -- make check`, which queues heavy work so at most two full checks run at once.
- `make docs` is part of `make check`: every path or skill named in repo markdown must exist (`scripts/check_doc_paths.py`), and code that changes without its docs fails (`scripts/check_docs_drift.py`).
- `make sanity` is the fast numeric check for solutions. The rule is under Decisions below.
- `verify/all_rounds_check.py` passes when the Round 1, Round 2, and Round 3 PDFs match `past/inventory.json`. The check requires the committed PDFs.

Architecture and the learner turn flow are in `docs/architecture.md`. Every skill is listed in `docs/skills.md`.

Concept units `01-foundations-substitution` through `36-unique-tricks` (36 directories) have machine drills in `verify/drills_unit*.json` (300 drills).

`problems/records.jsonl` holds 969 contest, Yang, and sample problems. `problems list` hides answers. `problems show` prints a stored cite.

## Harness

Canonical skill files are `.agents/skills/<name>/SKILL.md`. Codex loads that directory. `.cursor/skills/<name>` and `.claude/skills/<name>` are symlinks to the same directory. Cursor and Claude Code load that text. Edit `.agents/skills`. Git must store the symlinks (`core.symlinks=true`, the default on Linux and macOS).

Claude Code reads this file when the repository has no `CLAUDE.md`.

A new person clones the repo and asks their agent to set it up. The agent follows `.agents/skills/setup-integration-bee/SKILL.md`, which runs `scripts/setup.py` (macOS, Linux, and Windows; it creates `.venv/` from the pinned `requirements.txt`). `README.md` links that skill. The manual path is one getting-started section in `docs/setup-manual.md`: Codex, Claude, or Cursor. Each section lists the Python packages, the TeX and Java packages for `make check`, `scripts/control-integration-bee`, and the pstack plugin install for that harness. The plugin repository is https://github.com/michael-denyer/pstack-claude.

When a row below names a pstack skill, open `skills/<name>/SKILL.md` in the cache for the harness you are running. The version directory is the one the installer created.

| Harness | Skill cache |
|---|---|
| Codex | `${CODEX_HOME:-$HOME/.codex}/plugins/cache/pstack-claude/pstack/<version>/skills` |
| Claude | `${CLAUDE_CODE_PLUGIN_CACHE_DIR:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins}/cache/pstack-claude/pstack/<version>/skills` |
| Cursor | `~/.cursor/plugins/cache/<marketplace>/<plugin>/<version>/skills` |

An installed Codex copy at version 0.9.102 keeps its skills in `~/.codex/plugins/cache/pstack-claude/pstack/0.9.102/skills`. If that file is missing, the person running the agent installs the plugin from the matching `docs/setup-manual.md` section and starts a new session.

## Feature map

The map is `.agents/skills/verify-integration-bee/features/`.

- `doctor.md`
- `drills.md`
- `practice.md`
- `problems.md`
- `progress.md`
- `turn.md`
- `verify.md`

## Agent CLI

`scripts/control-integration-bee` is the only program that writes learner state.

| Command | What it does |
|---|---|
| `doctor` | Report whether this checkout can run. |
| `practice list` | List drills without answers. |
| `practice next` | Print one due drill or the next unit drill. |
| `practice check` | Compare one answer with SymPy and record the attempt. |
| `progress show` | Print ticks, attempts, due reviews, streak, and weak topics. |
| `progress tick` | Set a skill-tree node to learning, solid, or skipped. |
| `progress mistake` | Record a diagnosed miss. |
| `progress mock-start` | Open a timed mock when Round 1 nodes are solid, or with --cold. |
| `progress mock-finish` | Store a mock score. |
| `progress journal` | Store a technique note. |
| `progress streak` | Count today as a study day. |
| `drills list` | List drill ids. Includes the display answer. |
| `problems list` | List contest, Yang, and sample problems without answers. |
| `problems show` | Print one stored problem, including a cited answer when the extract has one. |
| `problems select` | Print one problem prompt. Omits the answer and any worked solution. |
| `turn schema` | Print the teach, mark, and mock turn schemas. |
| `turn show` | Print the session and the coach report. |
| `turn apply` | Apply one teach, mark, mock, aptitude, confirm, or cover turn and write the session. |
| `verify` | Run verify/run.sh. |

Regenerate this file with `python3 scripts/generate_agents_md.py` after you add a command or a feature file.

## Verifier skills

| Skill | When |
|---|---|
| `.agents/skills/setup-integration-bee` | Set up a fresh clone with `scripts/setup.py`. |
| `.agents/skills/verify-integration-bee` | Drive the CLI and keep a transcript. |
| `.agents/skills/formal-verify-integration-bee` | Check unit order, Round 1 readiness, and tracker records. |

## Pstack skills

| Situation | Run |
|---|---|
| You change what doctor, practice, drills, problems, progress, turn, or verify prints or records | .agents/skills/verify-integration-bee |
| You change unit order, mock readiness, or tracker writes | .agents/skills/formal-verify-integration-bee |
| You teach, mark a photo, or answer an empty message | .agents/skills/integration-bee-companion |
| You teach a concept, give an integral solution, or correct wrong pack mathematics | `docs/learning-capture.md` |
| The same mistake shows up twice | pstack skill `correct` from the harness plugin cache |
| You add a learner-facing command | pstack skill `create-verification-skill`, then `maintain-verification-skill`, from the harness plugin cache |
| You change `verify/model.py` | pstack skill `maintain-formal-verification-skill` from the harness plugin cache |
| The work is large or easy to get wrong | pstack skill `poteto-mode` from the harness plugin cache |
| You make a one-way design choice | `docs/decisions/` |

## Boundaries

- Open a pull request for changes. Do not merge it unless the operator authorizes that merge. A merge needs `make check` passing, green CI, and a squash-merge. Never force-push or rewrite pushed history.
- Do not commit `progress.local.json`, `trackers/live/`, or `.venv/`.
- The unpacked contest PDFs and the site PDFs are committed reference copies under `sources/past/` and `sources/`. `sources/fetch.sh` can still verify checksums. Do not commit `Resource_pack.zip`.
- Do not commit a plaintext copy of the Yang guide. The committed copy is `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`.
- Do not edit `AGENTS.md` by hand.

## Rule to enforcer

| Rule | Enforced by |
|---|---|
| Learner state stays uncommitted | `.gitignore` |
| AGENTS.md matches the generator | `scripts/check_agents_md.py` |
| Published commands match the parser | `scripts/check_agents_md.py` |
| Unit notes use the shared templates | `scripts/check_templates.py` |
| A unit sample compiles outside the repo root | `scripts/compile-tex.sh` |
| Drill answers match SymPy, and a wrong answer fails | `verify/run.sh` |
| Pack records and worked notes do not claim a problem is impossible | `verify/never_impossible_check.py` |
| Past papers do not precede concept units | `verify/unit_order_check.py` |
| Tracker and readiness invariants hold | `verify/invariants.py` |
| All-rounds indexes match, and the reference PDFs match | `verify/all_rounds_check.py` |
| Official reference PDFs stay in git | `scripts/check_structure.py` |
| The Yang PDF stays in git | `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf` |
| The check workflow still runs the pack targets | `scripts/check_ci.py` |

## Isolation

Set `IB_DATA_DIR` or pass `--data-dir` so two runs do not share tracker files. `IB_USER` names the `submissions/` folder for a photo mark and defaults to `default`. There is no port. `doctor` does not write. A second learner needs a separate data directory.

## Decisions

One-way choices are in `docs/decisions/`.

Before editing pack manuals, read the [source conflicts registry](docs/decisions/0016-pack-source-holds.md). Preserve conflicting source marks in the notes, certify the printed problem with an exact gate-accepted answer, and update answer citations, grading fixtures, and counts together. Do not invent agreement with a wrong mark.

A study turn writes learner state only. When teaching or a solved integral should change the pack, follow [learning capture](docs/learning-capture.md).

Solution skepticism: any agent that touches a solution may question it. Run `make sanity` (or `make sanity IDS="<id> ..."`) as a quick numeric check. It does not block the learner reply or the current pull request. A `MISMATCH` is checked against the problem source and fixed in a follow-up pull request; `UNCONFIRMED` stays listed, never labelled impossible.
