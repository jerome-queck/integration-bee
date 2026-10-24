#!/usr/bin/env python3
import sys
from pathlib import Path

from generate_agents_md import render

ROOT = Path(__file__).resolve().parent.parent
current = (ROOT / "AGENTS.md").read_text()
expected = render()
if current != expected:
    print("AGENTS.md drifted. Run python3 scripts/generate_agents_md.py", file=sys.stderr)
    sys.exit(1)
print("PASS AGENTS.md")
