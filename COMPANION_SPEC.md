# Companion product shape (Jerome, 24 Oct 22:56)

The repo is for any LLM pointed at it.

## Pieces

1. **Turn command** — `scripts/control-integration-bee turn apply` accepts one JSON turn. The kinds are `empty`, `teach`, `mark`, `mock-start`, and `mock-finish`. The CLI owns the session transition, the SymPy grade, the heatmap, and the mock gate.
2. **Agent skill** (`SKILL.md`) — thin interface. Call `turn apply`, then obey the JSON. Do not reimplement prep logic in prose.
3. **Empty ask** — `{"kind":"empty"}` returns `say` and the coach's next node.
4. **Tracker** — durable state in the data directory. The CLI projects `progress.local.json`. Personal files stay gitignored.

Schemas live in `contracts/`. The session example is `trackers/session.example.json`.

Portable markdown + CLI. Grok Pages are an optional view.
