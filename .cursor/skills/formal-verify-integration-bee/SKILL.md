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
- A session phase is `idle`, `awaiting_answer`, `mock_open`, or `mock_awaiting`. Idle has no open problem or mock. An answer phase names a problem. A mock phase names a mock.

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
python3 verify/invariants.py --expect-fail bad-session-phase
```

The plain command exits 0 on the real tree. Each `--expect-fail` exits 0 only when the planted break is caught.

## Coverage

| Predicate | File |
|---|---|
| `unit01_problem`, `concept_gap` | `verify/model.py`, called from `verify/unit_order_check.py` |
| `mock_block_reason` | `verify/model.py`, called from `scripts/control-integration-bee` |
| `tick_problem`, `attempt_problem`, `heatmap_problem`, `streak_problem` | `verify/model.py` |
| `session_problem` | `verify/model.py`, called before `scripts/control-integration-bee` writes `session.json` |

last_confirmed: 8ef99ddff0fadf3363dae65c978abd4154952178

Move `last_confirmed` to `git rev-parse HEAD:verify/model.py` only after you rerun the commands above and they still describe that file. That command prints the blob id of `verify/model.py`. A shallow pull-request checkout and a later merge keep the same id when the file bytes do not change. If `verify/model.py` changes and the id does not, rerun the checks before trusting them.

`/maintain-formal-verification-skill` is the update path when the code moves and this file was not rechecked.
