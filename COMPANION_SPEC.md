# Companion product shape (Jerome, 24 Oct 22:56)

The repo is for any LLM pointed at it.

## Pieces
1. **Main CLI** — single entrypoint for practice, syllabus progress, drills, checks.
2. **Agent skill** (`SKILL.md`) — thin interface: call the CLI, never reimplement prep logic in prose.
3. **Empty ask** — if the user gives no task, ask what they want, then suggest next steps from progress state.
4. **Tracker** — durable state: done units, techniques learned, weak spots, suggested next drill.

Portable markdown + CLI; Grok Pages optional view only.

## Public framework
See PUBLIC_FRAMEWORK.md — progress/session local; skill-tree concepts committed.
