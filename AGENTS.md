# Integration Bee

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

Concept units `01-foundations-substitution` through `36-unique-tricks` (36 directories) have machine drills in `verify/drills_unit*.json` (284 drills).

`problems/records.jsonl` holds 949 contest and Yang problems. `problems list` hides answers. `problems show` prints a stored cite.

## Feature map

The map is `.cursor/skills/verify-integration-bee/features/`.

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
| `problems list` | List contest and Yang problems without answers. |
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
| `.cursor/skills/verify-integration-bee` | Drive the CLI and keep a transcript. |
| `.cursor/skills/formal-verify-integration-bee` | Check unit order, Round 1 readiness, and tracker records. |

## Pstack skills

| Situation | Run |
|---|---|
| You change what doctor, practice, drills, problems, progress, turn, or verify prints or records | .cursor/skills/verify-integration-bee |
| You change unit order, mock readiness, or tracker writes | .cursor/skills/formal-verify-integration-bee |
| You teach, mark a photo, or answer an empty message | .cursor/skills/integration-bee-companion |
| The same mistake shows up twice | pstack skill `correct` |
| You add a learner-facing command | pstack skill `create-verification-skill`, then `maintain-verification-skill` |
| You change `verify/model.py` | pstack skill `maintain-formal-verification-skill` |
| The work is large or easy to get wrong | pstack skill `poteto-mode` |
| You make a one-way design choice | `docs/decisions/` |

## Boundaries

- Open a pull request for changes. Do not merge it, and do not force-push, unless the operator authorizes that merge.
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
| Past papers do not precede concept units | `verify/unit_order_check.py` |
| Tracker and readiness invariants hold | `verify/invariants.py` |
| All-rounds indexes match, and the reference PDFs match | `verify/all_rounds_check.py` |
| Official reference PDFs stay in git | `scripts/check_structure.py` |
| The Yang PDF stays in git | `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf` |
| The check workflow still runs the pack targets | `scripts/check_ci.py` |

## Isolation

Set `IB_DATA_DIR` or pass `--data-dir` so two runs do not share tracker files. There is no port. `doctor` does not write. A second writer needs its own data directory.

## Decisions

One-way choices are in `docs/decisions/`.
