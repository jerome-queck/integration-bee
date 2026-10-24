#!/usr/bin/env python3
"""Presence checks for past/ pedagogy pack + progress example schema."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NEED = [
    ROOT / "past" / "README.md",
    ROOT / "past" / "index.md",
    ROOT / "past" / "samples" / "problems.md",
    ROOT / "past" / "samples" / "answers_feed.json",
    ROOT / "past" / "mocks" / "mock01-meta.yaml",
    ROOT / "past" / "mocks" / "mock-pdf-round1.yaml",
    ROOT / "progress.local.example.json",
    ROOT / "CHAT_FLOWS.md",
]


def main() -> int:
    fail = 0
    for p in NEED:
        if not p.exists():
            print(f"FAIL missing: {p.relative_to(ROOT)}")
            fail = 1
        else:
            print(f"OK {p.relative_to(ROOT)}")

    feed = json.loads((ROOT / "past" / "samples" / "answers_feed.json").read_text())
    if len(feed) < 20:
        print(f"FAIL answers_feed has {len(feed)} < 20")
        fail = 1

    ex = json.loads((ROOT / "progress.local.example.json").read_text())
    if "mistakes" not in ex or not isinstance(ex["mistakes"], list):
        print("FAIL progress.local.example.json missing mistakes[]")
        fail = 1
    else:
        m0 = ex["mistakes"][0]
        for k in ("ts", "problem_id", "tags", "note"):
            if k not in m0:
                print(f"FAIL example mistake missing {k}")
                fail = 1

    chat = (ROOT / "CHAT_FLOWS.md").read_text()
    for needle in ("Flow 2", "Flow 3", "timed mock", "photo", "progress.local.json"):
        if needle.lower() not in chat.lower():
            print(f"FAIL CHAT_FLOWS.md missing mention of {needle!r}")
            fail = 1

    st = (ROOT / "skill-tree.md").read_text()
    if "past-paper" not in st.lower() and "sample-bridge" not in st.lower():
        print("FAIL skill-tree.md missing past-paper / sample-bridge practice nodes")
        fail = 1

    if not (ROOT / "units" / "01-foundations-substitution" / "meta.yaml").exists():
        print("FAIL concept unit 01 missing (past pack requires concept-before-papers)")
        fail = 1

    if fail:
        print("FAIL past_presence_check")
        return 1
    print("PASS past_presence_check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
