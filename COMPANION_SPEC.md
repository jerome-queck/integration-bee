# Companion product shape

The companion is the skill `.agents/skills/integration-bee-companion/SKILL.md`. Codex loads that directory. `.cursor/skills/integration-bee-companion` and `.claude/skills/integration-bee-companion` are symlinks to it. Cursor and Claude Code load the same file.

A new person clones the repo and asks their agent to set it up (`README.md`, setup skill `.agents/skills/setup-integration-bee/SKILL.md`, entry point `scripts/setup.py`). The manual path is the Codex, Claude, or Cursor section in `docs/setup-manual.md`. Each section is the clone, the packages, `scripts/control-integration-bee`, and the pstack plugin for that harness. The skill repeats those steps so the agent can onboard that person.

## Pieces

1. **Turn command.** `scripts/control-integration-bee turn apply` accepts one JSON turn. The kinds are `empty`, `teach`, `mark`, `mock-start`, `mock-finish`, `aptitude`, `confirm`, and `cover`. The CLI owns the session transition, the SymPy grade, the heatmap, and the mock gate.
2. **Agent skill.** Call `turn apply`, then obey the JSON. Do not reimplement prep logic in prose.
3. **Empty ask.** `{"kind":"empty"}` returns `say` and the coach's next node.
4. **Tracker.** Durable state in the data directory. The CLI projects `progress.local.json`. Personal files stay gitignored.
5. **Same grader.** `practice check` uses the same SymPy match as a mark. An indefinite answer may include `+C`. A definite answer may not.
6. **Open mock.** An empty turn while phase is `mock_open` continues that mock. `say` names the open mock. A second `mock-start` keeps the open pack until `mock-finish`. `mock-finish` on `turn apply` and on `progress` refuses while phase is `awaiting_answer`, `aptitude`, or `proposing`. A mock problem in phase `mock_awaiting` still ends with the paper.
7. **Reading view.** `--format json` is the stable record. `problems list`, `practice list`, and `drills list` print a table when the format is text. `problems select` names ids and exits 2 when more than one row matches. `--help` lists every command.
8. **Photo file.** A mark with `source` `photo` may set `image` to a filesystem path. The CLI copies that file to `submissions/<IB_USER>/` under the data directory. The attempt, `mark.picture`, `progress show`, and the `pictures` list in `progress.local.json` record the relative path. `IB_USER` defaults to `default`. Another learner uses another `IB_DATA_DIR`. The copy stays on this machine.

Schemas live in `contracts/`. The session example is `trackers/session.example.json`.

Portable markdown + CLI. Grok Pages are an optional view.
