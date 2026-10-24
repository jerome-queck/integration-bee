#!/usr/bin/env python3
"""Seed practice generator from all unit drills (yang / technique tags).

Not the main CLI (Code owns that). Emits a shuffled drill list for a tag filter.
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

VERIFY = Path(__file__).resolve().parent


def load_all() -> list[dict]:
    files = sorted(VERIFY.glob("drills_unit*.json"))
    out: list[dict] = []
    for f in files:
        out.extend(json.loads(f.read_text()))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="List/seed drills by technique or yang tag")
    ap.add_argument("--tag", action="append", default=[], help="Filter tag, e.g. yang:1.2 or u-sub")
    ap.add_argument("--shuffle", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    drills = load_all()
    tags = args.tag or ["yang:1.1", "yang:1.2"]
    out = []
    for d in drills:
        bag = set(d.get("technique_tags") or [])
        bag.add(d.get("technique", ""))
        for y in d.get("yang") or []:
            bag.add(y)
        if any(t in bag for t in tags):
            out.append(d)
    if args.shuffle:
        rng = random.Random(args.seed)
        rng.shuffle(out)
    if not out:
        print("FAIL: no drills matched", tags, file=sys.stderr)
        return 1
    for d in out:
        print(f"{d['id']}\t{d['technique']}\t{','.join(d.get('yang') or [])}\t{d['latex']}")
    print(f"# {len(out)} drills (tags={tags})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
