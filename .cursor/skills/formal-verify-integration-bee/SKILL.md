---
name: formal-verify-integration-bee
description: Check Integration Bee unit order, Round 1 mock readiness, and tracker record invariants. Use when editing verify/model.py, unit meta files, the skill-tree catalog, or tracker writes.
---

# Formal checks for Integration Bee

These checks cover finite catalogs and tracker records. They are not a TLA+ model, so `/statechart` does not apply. The predicates live in `verify/model.py` and the file checker `verify/unit_order_check.py` calls `unit01_problem` and `concept_gap`.

## Properties

- Unit 01 is a concept unit tagged `yang:1.1` and `yang:1.2`. A past-paper unit 01 blocks the pack.
- A catalog with past-paper units and no concept unit is rejected.
- A timed Round 1 mock is blocked until every `gate: round1` node is `solid`, unless the caller passes `--cold`.
- A tick name must be in `trackers/catalog.json`. An attempt interval cannot be negative. Heatmap fails cannot exceed attempts. Streak days cannot repeat.

## Run

```bash
python3 verify/invariants.py
python3 verify/invariants.py --expect-fail past-before-concept
python3 verify/invariants.py --expect-fail unit01-is-past
python3 verify/invariants.py --expect-fail unit01-missing-yang
python3 verify/invariants.py --expect-fail unknown-tick
python3 verify/invariants.py --expect-fail negative-interval
python3 verify/invariants.py --expect-fail heatmap-fails-exceed
python3 verify/invariants.py --expect-fail mock-before-ready
python3 verify/invariants.py --expect-fail duplicate-streak-day
```

The plain command exits 0 on the real tree. Each `--expect-fail` exits 0 only when the planted break is caught.

## Coverage

| Predicate | File |
|---|---|
| `unit01_problem`, `concept_gap` | `verify/model.py`, called from `verify/unit_order_check.py` |
| `mock_block_reason` | `verify/model.py`, called from `scripts/control-integration-bee` |
| `tick_problem`, `attempt_problem`, `heatmap_problem`, `streak_problem` | `verify/model.py` |

last_confirmed: uncommitted

Move `last_confirmed` to the current `git log -1 --format=%H -- verify/model.py` only after you rerun the commands above and they still describe that file. If `verify/model.py` changes and the hash does not, rerun the checks before trusting them.

`/maintain-formal-verification-skill` is the update path when the code moves and this file was not rechecked.
