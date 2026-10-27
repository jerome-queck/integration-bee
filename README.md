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

After Handoffs I/J and L, all 674 Resource pack rows have cited answers: **665 SymPy-proved, 9 manual, and 0 unchecked**. L resolves `R1-2022-MIT-TB-Q01`, `R1-2022-Oxford-Q01`, and `R1-2022-TB2022-Q01` to the proved answer **1** for their printed limits. The nine remaining manual rows belong to the Relay, Crossnumber, and Tournament follow-ups; their source conflicts remain documented in the [pack source conflicts registry](docs/decisions/0016-pack-source-holds.md). The verifier's `EXPECTED_SYMPY=665` / `EXPECTED_MANUAL=11` includes two answered Yang manuals; SAMPLE rows have separate counts. The registry preserves K's historical `6ac8f7d` baseline of 661 SymPy / 13 manual and the subsequent I/J state of 662 / 12.

A manual mark requires the companion's explicit `verdict`; the CLI does not compare its final answer with SymPy. Its displayed answer remains the cited catalog `answer_plain`, and the companion reads the linked note before judging the working. The resolved 2022 Q01 trio now grades **1** automatically and rejects `sin(1)`, even with a supplied correct verdict. Each note preserves the conflicting 2022 mark and cites the 2020 answer and worked calculation for the identical printed integral. A synthetic fixture retains manual-verdict coverage as source rows become proved.

Pack solution notes now cover **674/674** rows, including I's `R2-2023-Group-Q01-v2` note. K's historical baseline covered 673/674. The historical “19 honest note skips” list is no longer a missing-notes count; the registry preserves the measured baseline and current coverage.

The [concept map](pedagogy/concept-map.md) routes all five formerly open syllabus topics to teachable recognition notes: vector calculus, Beta, zeta, Euler–Mascheroni, and Catalan. These catalog nodes stay unticked and are not required for Round 1. `floor` and `dutis` keep their existing notes and drills and also stay unticked.

The companion and maintainer use this readiness checklist:

- `scripts/control-integration-bee doctor` reports `READY integration-bee`.
- `make check` passes on the proposed revision; `doctor` alone is not the proof gate.
- Every Resource pack row has a cited answer: SymPy rows grade automatically and manual rows require a verdict.
- The registry and note Status blocks distinguish the three conflicts resolved by L from the nine remaining manual rows; no Resource pack row is `unchecked`.
- The five syllabus recognition notes are available through the concept map; their nodes and `floor` / `dutis` stay unticked.

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
