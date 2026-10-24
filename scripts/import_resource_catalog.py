#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "verify"))

import problem_catalog  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract", required=True, type=Path)
    parser.add_argument("--out", type=Path, default=problem_catalog.RECORDS)
    args = parser.parse_args()
    raw = json.loads(args.extract.read_text(encoding="utf-8"))
    rows = problem_catalog.normalize_extract(raw)
    err = problem_catalog.catalog_problem(rows)
    if err:
        print(err, file=sys.stderr)
        return 1
    problem_catalog.dump_records(rows, args.out)
    print(f"wrote {len(rows)} {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
