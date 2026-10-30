---
name: setup-integration-bee
description: Set up a fresh clone of the Integration Bee pack. Use when someone has just cloned the repo and asks you to set it up, or when doctor does not print READY integration-bee.
---

# Set up Integration Bee

1. From the repo root, run the one setup entry point. It is safe to run again.
   - macOS / Linux: `python3 scripts/setup.py`
   - Windows: `py scripts\setup.py`
2. Verify: the last line is `SETUP OK` and the output includes `READY integration-bee`. If it prints `FAIL`, fix the named step (usually: install Python 3.11+) and run it again.
3. Use `.venv` Python for later commands (`.venv/bin/python` or `.venv\Scripts\python.exe`).
4. Tell the person it is ready, then invoke the `integration-bee-companion` skill to start studying.

Only maintainers who run `make check` need TeX, Java, and the pstack plugin. Those steps are in `docs/setup-manual.md`.
