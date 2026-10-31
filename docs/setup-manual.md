# Manual setup

The quick path is `python3 scripts/setup.py` (Windows: `py scripts\setup.py`); see the [setup skill](../.agents/skills/setup-integration-bee/SKILL.md). It creates `.venv/` and installs the pinned packages in `requirements.txt` (SymPy 1.14.0, mpmath 1.3.0, PyYAML 6.0.3, tzdata 2026.6). After that script, `make` and `verify/formal/run.sh` run `.venv`'s Python when that interpreter is present. `make PYTHON=...` still selects another interpreter, and a checkout with no virtualenv still uses `python3`. This page is the full manual path, including the TeX, Java, and pstack steps that maintainers need for `make check`.

tzdata is pinned because the CLI clock is `Asia/Singapore`, and Windows Python does not ship the timezone database. `sources/fetch.sh` and `verify/formal/run.sh` call `sha256sum`. macOS does not ship that command; install GNU coreutils so `sha256sum` is on PATH. The verify timeouts use `signal.SIGALRM`, which Windows Python does not provide, so a full `make check` is the Linux and macOS run.

## One skill text

Codex loads `.agents/skills/<name>/SKILL.md`. That directory is the only copy.

- `.agents/skills/integration-bee-companion/SKILL.md`
- `.agents/skills/verify-integration-bee/SKILL.md`
- `.agents/skills/formal-verify-integration-bee/SKILL.md`

`.cursor/skills/<name>` and `.claude/skills/<name>` are symlinks to `../../.agents/skills/<name>`. Cursor and Claude Code follow those links. Edit the file under `.agents/skills/`. Git must store the symlinks (`core.symlinks=true`, the default on Linux and macOS).


## Getting started by harness

Follow the section for the harness you run. Each section is enough on its own: packages, the companion CLI, and the pstack plugin.

### Codex

Install the Codex CLI and confirm that `codex` runs.

Install Python 3.11 or newer. CI uses Python 3.12.

Clone the pack and install the pinned packages from `requirements.txt`. The CLI is `scripts/control-integration-bee` in the clone.

```bash
git clone https://github.com/jerome-queck/integration-bee.git
cd integration-bee
python3 -m pip install -r requirements.txt
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

Clone the pack and install the pinned packages from `requirements.txt`. The CLI is `scripts/control-integration-bee` in the clone.

```bash
git clone https://github.com/jerome-queck/integration-bee.git
cd integration-bee
python3 -m pip install -r requirements.txt
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

Clone the pack and install the pinned packages from `requirements.txt`. The CLI is `scripts/control-integration-bee` in the clone.

```bash
git clone https://github.com/jerome-queck/integration-bee.git
cd integration-bee
python3 -m pip install -r requirements.txt
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


## Maintainer

People changing this pack use the checks below. Learners do not.

1. Follow the Getting started by harness section above for Codex, Claude, or Cursor. That section installs Python and the pinned packages (`python3 -m pip install -r requirements.txt`), the TeX and Java packages, and the pstack plugin.
2. Point Git at the drift hook once with `make hooks`.
3. Run `make check` before a pull request. CI runs the same command. Details are in `AGENTS.md`.
4. The unpacked contest PDFs and the site PDFs are committed reference copies under `sources/past/` and `sources/`. The contest list is `past/inventory.json`. Do not commit `Resource_pack.zip`.
5. Teach from `units/` with the files in `templates/`. The six contest gaps also have notes in `docs/techniques/`. A study session does not edit a teaching note.
6. The Yang Topics Guide, 2nd edition, is `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`. Attribution is in `sources/user/README.md`.
7. Contest, Yang, and sample problems are `problems/records.jsonl`. `problems list` hides answers. A mark still goes through `turn apply`. Sample worked notes are `solutions/sample/`.
8. `scripts/recover_pack_math.py` rereads the committed Round 1, Round 2, and Round 3 PDFs and rewrites a row only when SymPy proves the layout reading. `--write` is the whole catalog. Rows that do not prove stay `manual` or `unchecked`. PyMuPDF is required for that script. `make check` re-proves stored rows and does not open the PDFs.
9. `scripts/build_yang_ch3_to_ch6.py` is retired. Running it exits 2 and does not rewrite units, drills, or indexes. The old generator called unrestricted `sympify` and accepted a numeric shortcut.

Syllabus links are in `syllabus-map.md`. The skill tree is `skill-tree.md`.
