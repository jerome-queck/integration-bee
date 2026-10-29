# Integration Bee

Public study pack for the UK University Integration Bee.

A learner talks to the companion. The companion reads `.agents/skills/integration-bee-companion/SKILL.md` and sends a JSON turn to `scripts/control-integration-bee`. The learner does not run commands.

## One skill text

Codex loads `.agents/skills/<name>/SKILL.md`. That directory is the only copy.

- `.agents/skills/integration-bee-companion/SKILL.md`
- `.agents/skills/verify-integration-bee/SKILL.md`
- `.agents/skills/formal-verify-integration-bee/SKILL.md`

`.cursor/skills/<name>` and `.claude/skills/<name>` are symlinks to `../../.agents/skills/<name>`. Cursor and Claude Code follow those links. Edit the file under `.agents/skills/`. Git must store the symlinks (`core.symlinks=true`, the default on Linux and macOS).

## Getting started

Follow the section for the harness you run. Each section is enough on its own: packages, the companion CLI, and the pstack plugin.

### Codex

Install the Codex CLI and confirm that `codex` runs.

Install Python 3.11 or newer. CI uses Python 3.12.

```bash
python3 -m pip install sympy pyyaml
```

Clone the pack and run the companion CLI. The CLI is `scripts/control-integration-bee` in the clone.

```bash
git clone https://github.com/jerome-queck/integration-bee.git
cd integration-bee
scripts/control-integration-bee doctor
```

`doctor` prints `READY integration-bee` and exits 0 when the checkout can run.

`make check` needs `latexmk`, `pdflatex`, and Java 11 or newer. On Debian or Ubuntu, CI installs them with:

```bash
sudo apt-get update
sudo apt-get install -y latexmk texlive-latex-recommended texlive-fonts-recommended default-jre-headless
```

On macOS, install Python 3.11 or newer, run the same pip command, install a TeX distribution that provides `latexmk` and `pdflatex`, and install a JDK 11 or newer so `java` runs.

Install the pstack skill stack yourself from https://github.com/michael-denyer/pstack-claude:

```bash
codex plugin marketplace add michael-denyer/pstack-claude
codex plugin add pstack@pstack-claude
```

Skills land at `${CODEX_HOME:-$HOME/.codex}/plugins/cache/pstack-claude/pstack/<version>/skills/<skill-name>/SKILL.md`. With `CODEX_HOME` unset, that directory is `~/.codex/plugins/cache/pstack-claude/pstack/<version>/skills`. Version 0.9.102 is one installed example: `~/.codex/plugins/cache/pstack-claude/pstack/0.9.102/skills`.

Start Codex in this repository. Codex reads `AGENTS.md` and loads `.agents/skills/`. Invoke `$integration-bee-companion`.

When the pack names a pstack skill, open `skills/<skill-name>/SKILL.md` in that cache. The names used here are `poteto-mode`, `correct`, `statechart`, `setup-pstack`, `create-verification-skill`, `maintain-verification-skill`, and `maintain-formal-verification-skill`. Use the version directory the installer created.

### Claude

Install Claude Code 2.1.292 or later and confirm that `claude` runs.

Install Python 3.11 or newer. CI uses Python 3.12.

```bash
python3 -m pip install sympy pyyaml
```

Clone the pack and run the companion CLI. The CLI is `scripts/control-integration-bee` in the clone.

```bash
git clone https://github.com/jerome-queck/integration-bee.git
cd integration-bee
scripts/control-integration-bee doctor
```

`doctor` prints `READY integration-bee` and exits 0 when the checkout can run.

`make check` needs `latexmk`, `pdflatex`, and Java 11 or newer. On Debian or Ubuntu, CI installs them with:

```bash
sudo apt-get update
sudo apt-get install -y latexmk texlive-latex-recommended texlive-fonts-recommended default-jre-headless
```

On macOS, install Python 3.11 or newer, run the same pip command, install a TeX distribution that provides `latexmk` and `pdflatex`, and install a JDK 11 or newer so `java` runs.

Install the pstack skill stack yourself from https://github.com/michael-denyer/pstack-claude. Inside Claude Code:

```text
/plugin marketplace add michael-denyer/pstack-claude
/plugin install pstack@pstack-claude
```

Start a new Claude Code session so the plugin loads. `/reload-plugins` reloads plugins in the session you already have.

The plugins root is `~/.claude/plugins` unless `CLAUDE_CODE_PLUGIN_CACHE_DIR` or `CLAUDE_CONFIG_DIR` is set. Skills land at `${CLAUDE_CODE_PLUGIN_CACHE_DIR:-${CLAUDE_CONFIG_DIR:-$HOME/.claude}/plugins}/cache/pstack-claude/pstack/<version>/skills/<skill-name>/SKILL.md`.

Start Claude Code in this repository. Claude Code reads `AGENTS.md`. `.claude/skills/` points at `.agents/skills/`. Invoke `/integration-bee-companion`.

When the pack names a pstack skill, open `skills/<skill-name>/SKILL.md` in that cache. The names used here are `poteto-mode`, `correct`, `statechart`, `setup-pstack`, `create-verification-skill`, `maintain-verification-skill`, and `maintain-formal-verification-skill`. Use the version directory the installer created.

### Cursor

Install Cursor. Open this repository as the project folder.

Install Python 3.11 or newer. CI uses Python 3.12.

```bash
python3 -m pip install sympy pyyaml
```

Clone the pack and run the companion CLI. The CLI is `scripts/control-integration-bee` in the clone.

```bash
git clone https://github.com/jerome-queck/integration-bee.git
cd integration-bee
scripts/control-integration-bee doctor
```

`doctor` prints `READY integration-bee` and exits 0 when the checkout can run.

`make check` needs `latexmk`, `pdflatex`, and Java 11 or newer. On Debian or Ubuntu, CI installs them with:

```bash
sudo apt-get update
sudo apt-get install -y latexmk texlive-latex-recommended texlive-fonts-recommended default-jre-headless
```

On macOS, install Python 3.11 or newer, run the same pip command, install a TeX distribution that provides `latexmk` and `pdflatex`, and install a JDK 11 or newer so `java` runs.

Install the `pstack` plugin from the Cursor marketplace yourself. Codex and Claude install the port of that same skill stack from https://github.com/michael-denyer/pstack-claude. The skill names match.

Skills land at `~/.cursor/plugins/cache/<marketplace>/<plugin>/<version>/skills/<skill-name>/SKILL.md`. The `<plugin>` segment is the marketplace id and may be a number.

Cursor reads `AGENTS.md` and loads `.agents/skills/`. `.cursor/skills/` points at that directory. Invoke `integration-bee-companion` from the skill menu.

When the pack names a pstack skill, open `skills/<skill-name>/SKILL.md` in that cache. The names used here are `poteto-mode`, `correct`, `statechart`, `setup-pstack`, `create-verification-skill`, `maintain-verification-skill`, and `maintain-formal-verification-skill`. Use the version directory the installer created.

## Start

The learner talks to the companion and does not run the CLI. The companion reads `.agents/skills/integration-bee-companion/SKILL.md` and writes one JSON turn.

```bash
scripts/control-integration-bee turn apply --file turn.json --format json
```

Begin with `{"kind":"aptitude"}`. The first integral is a unit drill. The learner sends written working. The companion marks it with `{"kind":"mark",...}`. A correct mark opens one contest integral from the catalog. That contest verdict stores an attempt and does not tick a node.

When the result phase is `proposing`, ask which nodes in `coach.offer` to skip. Send `{"kind":"confirm","nodes":[...]}` with only those ids. An empty list skips nothing and declines the offer, so those ids are not offered again. A confirm before that offer, or a confirm that names an id outside it, exits 2 and writes nothing.

After confirm, continue with `{"kind":"teach"}`. `coach.detail`, `coach.approach`, `coach.kind`, and `coach.volume` are the dosage for `coach.next_node`. A miss moves that dosage back toward a worked example. Send `{"kind":"aptitude"}` again only for another placement probe. The learner does not finish every Round 1 probe before coaching.

`{"kind":"cover","full":true}` turns full coverage on and puts confirmed skips back in the coach queue. The default leaves them out. The mock still needs every Round 1 node `solid`.

## How it works

`turn apply` is the only writer of learner state. Kinds are empty, teach, mark, mock-start, mock-finish, aptitude, confirm, and cover. `confirm` is the only new writer of `skipped`, and only for ids in the open offer. `progress tick` can still set `skipped` by hand.

A mark may set `extract.gap` to a heading in `docs/techniques/beyond-yang.md`, and `say` names that file. `turn apply` stores the id on the attempt and does not write the file. The lesson is that file: a unit `teaching.tex`, or one note under `docs/techniques/`. The Yang Topics Guide is one source among the syllabus, the Techniques Guide, and these notes.

The session file is `session.json` in the data directory. One replace holds the phase, the skip offer, declined ids, the coverage flag, and the per-node dosage. Set `IB_DATA_DIR`, or leave the files in `trackers/live`. `IB_USER` names the photo folder inside that directory and defaults to `default`. A second learner uses a separate data directory. `progress.local.json` and `trackers/live/` are gitignored, including `submissions/`.

`problems/records.jsonl` is the contest, Yang, and sample catalog. `problems list` and `problems select` hide answers. A `sympy` row is graded from `extract.final_answer`. The companion does not send `verdict` for it. A pack `sympy` row has a gate-checked answer for its encoded source problem; documented mark conflicts retain both the printed mark and the evidence for the graded answer. A sample `sympy` row was proved from the sample problems and answers. A `manual` row is a cited answer the pack gate has not proved, and the companion judges it. An `unchecked` row has no printed answer and must not be invented. Unit drills are SymPy-checked too. Sample worked notes are `solutions/sample/`.

`scripts/control-integration-bee --help` lists every command. `--format json` is the stable record. `problems list`, `practice list`, and `drills list` print a table unless you pass `--format json`. `problems select` names matching ids and exits 2 when the filter is not one row. `practice check` accepts an indefinite `+C` the same way a mark does. `mock-finish` on `turn apply` and on `progress` exits 2 while phase is `awaiting_answer`, `aptitude`, or `proposing`. `doctor` prints `IB_DATA_DIR` and ignores `--data-dir`. Other commands honor `--data-dir`. A photo mark may set `image` to a file path. The CLI copies it under `submissions/<IB_USER>/` and lists that relative path from `progress show` and `mark.picture`.

`make check` runs `verify/run.sh`. That script drives the turn contract, including aptitude, confirm, cover, and the gap index.

## Pack status

At tip `770c6e4`, the Resource pack is **674 SymPy / 0 manual / 0 unchecked**, with a note for all 674 rows. Handoffs L through Q resolved the twelve source holds in the [pack source conflicts registry](docs/decisions/0016-pack-source-holds.md): the 2022 Q01 trio grades **1**, and the Relay, Crossnumber, and Tournament rows are `verify: sympy`. Handoff O certified `SAMPLE-Q05`, `SAMPLE-Q08`, `SAMPLE-Q09`, and `SAMPLE-Q19`, plus `YANG-1.3-Ex01` and `YANG-1.3-Ex03`. At that tip the verifier's `EXPECTED_SYMPY=676` / `EXPECTED_MANUAL=0` was those 674 pack rows plus the two answered Yang examples. Lane L1 proves 27 further Yang rows. Lane L3 proves the thirty §1.6 and §1.7 integrals, lane L6 proves the thirty §2.3 and §2.4 practice rows, lane L2 proves the 38 §1.4 and §1.5 integrals, and lane L7 proves the 34 §2.5 and §2.6 integrals, so the live pair is `EXPECTED_SYMPY=835` / `EXPECTED_MANUAL=0`. SAMPLE is **20 SymPy / 0 manual** and sits outside that pair. 111 Yang rows stay `unchecked`. This pack does not store a final the gate did not prove. Dated mid-chain snapshots, including K's `6ac8f7d` baseline of 661 SymPy / 13 manual, stay in the registry as history.

A `sympy` row grades from `extract.final_answer`. The 2022 Q01 notes still preserve the conflicting `sin(1)` marks and cite the 2020 answer for the same printed integral. A synthetic fixture keeps the manual-verdict path. Pack manuals are 0 and sample manuals are 0.

Pack solution notes cover **674/674** rows, including I's `R2-2023-Group-Q01-v2` note. K's historical baseline covered 673/674. The historical “19 honest note skips” list is a past missing-notes count; the registry keeps that baseline beside the current 674/674 coverage.

The [concept map](pedagogy/concept-map.md) records teaching deferred **0**: 63 ready concept nodes and 9 practice indexes, 72 nodes in all. `floor`, `dutis`, vector calculus, Beta, zeta, Euler–Mascheroni, and Catalan are ready. They stay unticked until a learner has evidence, and they are not Round 1 requirements.

The companion and maintainer use this readiness checklist:

- `scripts/control-integration-bee doctor` reports `READY integration-bee`.
- `make check` passes on the proposed revision; `doctor` alone is not the proof gate.
- Every Resource pack row is `verify: sympy` with a cited answer. Pack manuals are 0 and unchecked pack rows are 0.
- The registry records the twelve resolved holds. 111 Yang rows remain `unchecked`. A proved Yang row is `verify: sympy`.
- Teaching deferred is 0. The seven syllabus nodes are ready and stay unticked until learner evidence.

## Learner

Ask the companion for a concept, or send a photo of a solution.

## Maintainer

People changing this pack use the checks below. Learners do not.

1. Follow the Getting started section for Codex, Claude, or Cursor. That section installs Python, SymPy, PyYAML (`python3 -m pip install sympy pyyaml`), the TeX and Java packages, and the pstack plugin.
2. Point Git at the drift hook once with `make hooks`.
3. Run `make check` before a pull request. CI runs the same command. Details are in `AGENTS.md`.
4. The unpacked contest PDFs and the site PDFs are committed reference copies under `sources/past/` and `sources/`. The contest list is `past/inventory.json`. Do not commit `Resource_pack.zip`.
5. Teach from `units/` with the files in `templates/`. The six contest gaps also have notes in `docs/techniques/`. A study session does not edit a teaching note.
6. The Yang Topics Guide, 2nd edition, is `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`. Attribution is in `sources/user/README.md`.
7. Contest, Yang, and sample problems are `problems/records.jsonl`. `problems list` hides answers. A mark still goes through `turn apply`. Sample worked notes are `solutions/sample/`.
8. `scripts/recover_pack_math.py` rereads the committed Round 1, Round 2, and Round 3 PDFs and rewrites a row only when SymPy proves the layout reading. `--write` is the whole catalog. Rows that do not prove stay `manual` or `unchecked`. PyMuPDF is required for that script. `make check` re-proves stored rows and does not open the PDFs.

Syllabus links are in `syllabus-map.md`. The skill tree is `skill-tree.md`.
