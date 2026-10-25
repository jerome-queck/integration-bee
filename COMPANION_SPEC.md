# Companion product shape

The companion is the skill `.agents/skills/integration-bee-companion/SKILL.md`. Codex loads that directory. `.cursor/skills/integration-bee-companion` and `.claude/skills/integration-bee-companion` are symlinks to it. Cursor and Claude Code load the same file.

A new person follows the Codex, Claude, or Cursor section in `README.md`. Each section is the clone, the packages, `scripts/control-integration-bee`, and the pstack plugin for that harness. The skill repeats those steps so the agent can onboard that person.

## Pieces

1. **Turn command.** `scripts/control-integration-bee turn apply` accepts one JSON turn. The kinds are `empty`, `teach`, `mark`, `mock-start`, `mock-finish`, `aptitude`, `confirm`, and `cover`. The CLI owns the session transition, the SymPy grade, the heatmap, and the mock gate.
2. **Agent skill.** Call `turn apply`, then obey the JSON. Do not reimplement prep logic in prose.
3. **Empty ask.** `{"kind":"empty"}` returns `say` and the coach's next node.
4. **Tracker.** Durable state in the data directory. The CLI projects `progress.local.json`. Personal files stay gitignored.

Schemas live in `contracts/`. The session example is `trackers/session.example.json`.

Portable markdown + CLI. Grok Pages are an optional view.
