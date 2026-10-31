# 🐝 Integration Bee

[![check](https://github.com/jerome-queck/integration-bee/actions/workflows/check.yml/badge.svg)](https://github.com/jerome-queck/integration-bee/actions/workflows/check.yml)
![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)
![macOS · Linux · Windows](https://img.shields.io/badge/os-macOS%20%C2%B7%20Linux%20%C2%B7%20Windows-lightgrey)

A free practice and coaching pack for the UK University Integration Bee. ∫

You chat with an AI coach. It finds what you already know, teaches what you don't, gives you real contest integrals, and marks your working (even a photo of it). Every answer in the pack has been checked by a computer. You never need to run a command yourself.

## ✨ What's inside

- 📚 **The pack**: past contest problems from Rounds 1–3, each with a checked answer and a solution note.
- 📖 **The Yang set**: every problem from the Yang Topics Guide (2nd edition), with worked solutions.
- ✅ **The checker**: SymPy proves every stored answer, and `make check` runs on every change.
- 🤖 **The coach**: an agent skill that teaches, drills, and marks, and remembers your progress.

## 🗺️ Your journey

<p align="center"><img src="docs/images/journey/journey.png" width="880" alt="Statechart of the learner journey: clone the repo, the agent runs setup, a placement drill, the coach marks your working, you pick what to skip, lessons, real contest integrals, gaps captured and retaught, a mock exam, and Round 1 ready"></p>

Clone, let your agent set up, find your level, then loop through lessons and real contest integrals. Every miss becomes a captured gap that the coach reteaches, until the mock exam says you're Round 1 ready. Source: [journey.mmd](docs/images/journey/journey.mmd) ([how it's made](docs/images/journey/README.md)).

<details>
<summary>Mermaid source of the chart</summary>

```mermaid
---
title: "Your Integration Bee journey"
---
stateDiagram-v2
  state "Legend" as legend {
    lg0: Get set up
    lg1: Find your level
    lg2: Practise
    lg3: Learn
    lg4: Prove it
  }
  class lg0 blue
  class lg1 purple
  class lg2 teal
  class lg3 yellow
  class lg4 pink
  s0: #128229; Repo cloned
  s1: #129302; Agent runs setup
  s2: #127919; Placement drill
  s3: #9997;#65039; Coach marks your working
  s4: #9197;#65039; You pick what to skip
  s5: #128214; Lesson from the notes
  s6: #8747; Real contest integral
  s7: #129513; Gap captured
  s8: #9201;#65039; Mock exam
  s9: #127942; Round 1 ready
  [*] --> s0
  s0 --> s1: you paste the setup prompt
  s1 --> s2: setup prints READY
  s2 --> s3: you send your working
  s3 --> s2: one more probe
  s3 --> s4: coach offers skips
  s4 --> s5: you confirm
  s5 --> s6: you try one
  s6 --> s3: you send your working
  s3 --> s6: correct: next integral
  s3 --> s7: a miss shows a gap
  s3 --> s8: every Round 1 node solid
  s7 --> s5: coach reteaches it
  s8 --> s7: the mock finds a gap
  s8 --> s9: you pass
  class s0 blue
  class s1 blue
  class s2 purple
  class s3 teal
  class s4 purple
  class s5 yellow
  class s6 teal
  class s7 yellow
  class s8 pink
  class s9 pink
```

</details>

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
