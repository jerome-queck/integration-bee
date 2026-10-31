# 🐝 Integration Bee

[![check](https://github.com/jerome-queck/integration-bee/actions/workflows/check.yml/badge.svg)](https://github.com/jerome-queck/integration-bee/actions/workflows/check.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![macOS · Linux · Windows](https://img.shields.io/badge/os-macOS%20%C2%B7%20Linux%20%C2%B7%20Windows-lightgrey)

A free practice and coaching pack for the UK University Integration Bee. ∫

You chat with an AI coach. It finds what you already know, teaches what you don't, gives you real contest integrals, and marks your working (even a photo of it). Every answer in the pack has been checked by a computer. You never need to run a command yourself.

## ✨ What's inside

- 📚 **The pack**: past contest problems from Rounds 1–3, each with a checked answer and a solution note.
- 📖 **The Yang set**: integral rows from the Yang Topics Guide (2nd edition), with worked notes. `YANG-1.14-P10` is a formula and is not graded. Inventory section 4.3 has no unit.
- ✅ **The checker**: `make check` re-checks each stored `verify: sympy` answer. It does not grade an unchecked row, and a note can keep a printed mark the gate did not accept.
- 🤖 **The coach**: an agent skill that teaches, drills, and marks, and remembers your progress.

## 🗺️ How it fits together

```mermaid
flowchart TD
    You([🙋 You]) --> Coach[🤖 Coach agent]
    Coach --> CLI[⚙️ Pack CLI]
    CLI --> Problems[(📚 Contest pack + 📖 Yang set)]
    Checker[✅ Checker] -. checks sympy rows .-> Problems
```

More detail: [docs/architecture.md](docs/architecture.md).

## 🚀 Get started

1. Clone the repo:

   ```bash
   git clone https://github.com/jerome-queck/integration-bee.git
   cd integration-bee
   ```

2. Open it in your AI agent (Codex, Claude Code, or Cursor) and paste this:

   > Set up this repo using the setup-integration-bee skill: run `scripts/setup.py`, confirm it prints SETUP OK and READY integration-bee, then start the integration-bee-companion so I can study.

That's it. 🎉 Setup is one script, `scripts/setup.py`, that works the same on macOS, Linux, and Windows and is safe to run again. Your agent follows the [setup skill](.agents/skills/setup-integration-bee/SKILL.md).

Prefer doing it by hand, or maintaining the pack? See [docs/setup-manual.md](docs/setup-manual.md).

Contributing? Agents start with [AGENTS.md](AGENTS.md); people with [docs/setup-manual.md](docs/setup-manual.md).
