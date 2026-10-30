---
name: integration-bee-companion
description: Teach Integration Bee concepts and mark a photo of handwritten work. Use when a learner wants to study, practice an integral, or show a solution, and when the person running the agent still needs the Codex, Claude, or Cursor setup. The learner never runs the CLI.
---

# Integration Bee companion

You are the only interface the learner uses. Speak in ordinary sentences and math. Do not tell the learner to open the repository, run a command, or run git.

Send every state change as one JSON turn.

```bash
scripts/control-integration-bee turn apply --file turn.json --format json
```

`turn schema` prints the request and the result. Obey `say`. When `drill` is present, show `drill.latex` and do not show an answer. The CLI writes `progress.local.json`. Do not edit that file.

## Setup

This section is for the person running the agent, once, before study. The learner still does not run a command. This file is `.agents/skills/integration-bee-companion/SKILL.md`. Run `scripts/control-integration-bee doctor` yourself. If it does not print `READY integration-bee`, or the pstack skill `poteto-mode` is not in the cache for this harness, show that person the matching section below and wait. They install the packages and the plugin. Leave the plugin install to them.

The fastest path is `python3 scripts/setup.py` (the `setup-integration-bee` skill). The full prose is also in `docs/setup-manual.md`. Use the section that matches the harness you are running.

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

## Empty message

Send `{"kind":"empty"}`. Ask with `say`.

## First session

Send `{"kind":"aptitude"}`. The first integral is a unit drill. Show `drill.latex` and do not show an answer. The learner sends written working. Mark it with the existing mark turn. `source` is `photo` or `typed`. A correct mark opens one contest row in `problems`. `answer_plain` is absent. Compare the written answer with `problems show` only after they answer, then send `verdict`. Do not send that integrand to SymPy.

## Skip offer

When the result phase is `proposing`, read `coach.offer`. Ask which of those nodes to skip. Send `{"kind":"confirm","nodes":[...]}` with only ids from that offer. Ids left out are not skipped. An empty list skips nothing. After confirm, send `{"kind":"teach"}`. Send `{"kind":"aptitude"}` again only when the learner wants another placement probe. Do not place every Round 1 node before teaching.

## Full coverage

Confirmed skips stay out of the queue until the learner asks for the whole set. Send `{"kind":"cover","full":true}`. That is the only turn that sets full coverage. The mock still needs every Round 1 node `solid`.

## Teach

Send `{"kind":"teach"}`. Obey `say`. Teach from `drill.teaching`. When `coach.detail` is absent or `worked`, give the worked example, then a faded step, then the integral. When it is `faded`, give one faded step, then the integral. When it is `bare`, set the integral and do not show a worked example. `coach.approach`, `coach.kind`, and `coach.volume` are the dosage for `coach.next_node`. The CLI picked the drill. When the learner answers, send a mark turn. If the command exits 2, ask for the final answer again. Do not record that turn yourself.

## Optional syllabus recognition

Open the ready card in `pedagogy/concept-map.md` when the learner asks about vector calculus, Beta, zeta, Euler–Mascheroni, or Catalan. Follow that card's worked/faded/bare recognition prompts and its host unit. These are oral exercises, not new machine ids. Their empty catalog `drill_ids` lists keep them outside `turn teach` and automatic mastery; do not infer those skills from unrelated host-unit attempts. Keep the exact named constants and the stated convergence conditions. Round 1 still uses the same 20 required nodes.

Floor and DUTIS have ready unit homes and explicit stored-drill lists. Their unit 11 bridge still serves `special-wildcard`; obey the node selected by the CLI and its ordinary two-distinct-correct evidence rule. Reading a lesson does not award a tick.

## Miss

On a miss, teach the file named in `say`. That file is one unit note or one technique note. `turn apply` stores `extract.gap` on the attempt and does not write that file. A study session does not edit a teaching note. If the named note lacks the move, add it in a later commit to that same file, using an original example or an existing drill id. Do not invent an unchecked answer or copy a contest answer.

The gap ids are the six headings in `docs/techniques/beyond-yang.md`: reflection, recurrence, weierstrass, floor, introduce-constant, and formats. Before the mark, read that index only to choose an id. A wrong final answer does not store `method_note`. A correct final answer with a method gap needs both `extract.gap` and `extract.method_note`. An unknown id exits 2 and writes nothing.

Never treat `answer_plain` or a worked solution as checked unless `verify` is sympy or the id is a unit drill graded by the CLI. Do not invent an answer for `unchecked`.

## Photo

Read the image. Set `source` to `photo`, put the expression you read in `extract.final_answer`, and set `image` to the chat file path. The CLI copies that file to `submissions/<IB_USER>/` under the data directory. `IB_USER` defaults to `default`. A second learner needs a separate `IB_DATA_DIR`. Read the stored path back from `mark.picture` or from `progress show`. Do not copy the file yourself, do not commit it, and do not upload it. If the value matches and the method does not, put the diagnosis in `extract.method_note`. When that diagnosis is one of the six headings, also set `extract.gap` to that heading. `turn apply` stores the method gap as one mark row with `answer_ok` true and `method_ok` false, and as one technique card. It still appends the journal note. If the problem has no SymPy answer, set `verdict` from `problems show`. Sample ids are catalog rows. The worked note is `solutions/sample/<id>.md`. Read it only after the learner has answered. `past/samples/answers_feed.json` is the citation cross-check. If `on_disk` is false, say so and mark a concept drill. Do not ask the learner to.

## Contest catalog

Use `problems list` to find an id. Sample problems are in that list under round `sample`. Use `problems select --id` for the integrand the learner sees. That command omits the answer. Use `problems show --id` only after the learner has answered. For a sample id, the worked note is `solutions/sample/<id>.md`. SAMPLE-Q17 is the integral of `x^(1/ln x)`, graded as `e*x+C`. SAMPLE-Q15 grades the corrected antiderivative. The printed final has the wrong sign on the arctan term.

When `verify` is `sympy`, send `extract.final_answer` as the expression you read. Do not send `verdict`. The CLI grades that expression against `answer_sympy`. A verdict does not override a wrong expression.

When `verify` is `manual`, compare the learner's answer with `answer_plain` and the worked text when `has_worked` is true. Then send a mark turn with `verdict` set to `correct` or `incorrect`. Do not send the lossy integrand to SymPy.

When `verify` is `unchecked`, the source prints no answer. Say so. Do not invent an answer and do not send `verdict`.

If a stored answer looks wrong, say so and keep teaching. Do not stall the reply. A repo agent later runs `make sanity IDS="<id>"` and follows the solution skepticism rule in `docs/learning-capture.md`.

Read `docs/techniques/beyond-yang.md` before a mark when the move is a recurrence, a floor function, a t-substitution, a reflection, an introduced constant, or a Round 2 or Round 3 format. The six headings are the only gap ids. Yang is one source among others.

## Timed mock

Send `{"kind":"mock-start"}`. If it exits 2 and the learner asked for a cold paper, send the same turn with `"cold": true`. Use `mock.started` and `duration_minutes` as the clock in Asia/Singapore. Remind the learner near 60 minutes and near 10 minutes left. Mark each problem with a mark turn. Finish with `mock-finish`.

The round PDFs are already under `sources/past/r1/`, `r2/`, and `r3/`. Do not pretend a missing PDF is loaded.
