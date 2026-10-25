---
name: formal-verify-integration-bee
description: Check Integration Bee unit order, Round 1 mock readiness, tracker record invariants, and the learner-session TLA+ model. Use when editing verify/model.py, verify/formal, unit meta files, the skill-tree catalog, or tracker writes.
---

# Formal checks for Integration Bee

Two checks. `verify/model.py` is a set of Python predicates over catalogs and tracker records. `verify/formal/` is a TLA+ model of one study session and of two writers sharing one data directory. TLC 1.7.4 checks the model. Read `/statechart` when you read a TLC result or redraw the chart. Do not copy that skill's commands into this file.

## Catalog predicates

These predicates are not a state machine. `verify/unit_order_check.py` calls `unit01_problem` and `concept_gap`.

- Unit 01 is a concept unit tagged `yang:1.1` and `yang:1.2`. A past-paper unit 01 blocks the pack.
- A catalog with past-paper units and no concept unit is rejected.
- A timed Round 1 mock is blocked until every `gate: round1` node is `solid`, unless the caller passes `--cold`.
- A tick name must be in `trackers/catalog.json`. An attempt interval cannot be negative. Heatmap fails cannot exceed attempts. Streak days cannot repeat.
- A session phase is `idle`, `awaiting_answer`, `mock_open`, `mock_awaiting`, `aptitude`, or `proposing`. Idle has no open problem or mock. An answer phase names a problem. A mock phase names a mock. `aptitude` names a problem. `proposing` waits for confirm and names an offer.
- A mark is one row per id with bool `answer_ok`, bool `method_ok`, and a technique. The key `correct` is rejected.
- A sticky is one card per technique with a note and a touched day. The key `strength` is rejected. Strength is computed from the touched day.

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
python3 verify/invariants.py --expect-fail mark-one-bool
python3 verify/invariants.py --expect-fail mark-has-correct
python3 verify/invariants.py --expect-fail sticky-stored-strength
```

The plain command exits 0 on the real tree. Each `--expect-fail` exits 0 only when the planted break is caught.

| Predicate | File |
|---|---|
| `unit01_problem`, `concept_gap` | `verify/model.py`, called from `verify/unit_order_check.py` |
| `mock_block_reason` | `verify/model.py`, called from `scripts/control-integration-bee` |
| `tick_problem`, `attempt_problem`, `heatmap_problem`, `streak_problem` | `verify/model.py` |
| `session_problem` | `verify/model.py`, called before `scripts/control-integration-bee` writes `session.json` |
| `mark_problem`, `sticky_problem` | `verify/model.py`, called before `turn apply` writes `marks.json` and `stickies.json` |

last_confirmed: 292ff5c8a2ac9cb84d373cdb83e28a2ba5fa444c

Move `last_confirmed` to `git rev-parse HEAD:verify/model.py` only after you rerun the commands above and they still describe that file. That command prints the blob id of `verify/model.py`. A shallow pull-request checkout and a later merge keep the same id when the file bytes do not change. If `verify/model.py` changes and the id does not, rerun the checks before trusting them.

## Learner session model

`SessionFlow.tla` is one companion session for one Round 1 node. `TrackerWrites.tla` is two writers in one data directory. The pass configs describe the code. A `Break` value deletes one guard so TLC can show the property fail.

Run both from the repo root.

```bash
make formal
```

That is `bash verify/formal/run.sh`. It downloads TLC 1.7.4 into `verify/formal/.cache/` when the jar is missing, checks the pinned sha256, and needs Java 11 or newer. CI installs `default-jre-headless` before `make check`.

### Properties that hold

A solid tick in `SessionFlow` follows two correct drills for that node. A stored mock was started with the node solid, or with `--cold`. A photo miss appends a mistake and marks the tag weak and due. An incorrect check does the same for the spaced queue. A stored score follows an opened mock.

In `TrackerWrites`, with `Break = "none"`, a mock file is gated, the file holds at most one open session, a score follows a start, heatmap fails do not exceed heatmap attempts, and incorrect rows do not exceed attempt rows.

### Properties the current writer breaks

These are findings. Do not delete them to make TLC pass. `make formal` expects each one to fail.

- `NoLostAttempt`. `record_attempt` reads `attempts.json`, appends in memory, and `write_json` replaces the file. Two checks that both read an empty list each write one row. One row remains. A drill drops out of the spaced queue. The two writes also share `attempts.json.tmp`, so one `replace` can raise `FileNotFoundError`.
- `IdleFilesAgree`. The attempts write and the heatmap write are separate. If the process stops after `write_json` of attempts and before the heatmap write, the attempt row is there and the weak tag is not.
- `ProjectionMatches`. `project` in `record_attempt` and `mock-start` writes the tick object captured at the start of the command. A solid tick that lands in between is missing from `progress.local.json`. The same split happens if `progress tick` writes `skill-ticks.json` and the process stops before `project`. `verify/formal/repro_tracker.py` forces the tick clobber without a crash.
- `NoLostMock`. Two `mock-start` commands that both read no open session each replace `mocks.json` with one session. One mock remains.

`verify/formal/repro_tracker.py` shows the lost attempt, the tick clobber, and the stop after the attempts write on `scripts/control-integration-bee`. A sequential pair of checks still keeps both rows.

### Planted breaks

| Config | Invariant that must fail |
|---|---|
| `SessionFlow.tick-early.cfg` | `TwoCorrectBeforeSolid` |
| `SessionFlow.mock-ungated.cfg` | `MockGate` |
| `SessionFlow.forget-weak.cfg` | `MistakeQueuesWeak` |
| `SessionFlow.score-without-open.cfg` | `ScoreAfterOpen` |
| `TrackerWrites.drop-gate.cfg` | `MockGate` |
| `TrackerWrites.second-open.cfg` | `AtMostOneOpen` |
| `TrackerWrites.lost-attempt.cfg` | `NoLostAttempt` |
| `TrackerWrites.torn-heat.cfg` | `IdleFilesAgree` |
| `TrackerWrites.stale-progress.cfg` | `ProjectionMatches` |
| `TrackerWrites.lost-mock.cfg` | `NoLostMock` |

### Charts

`verify/formal/charts/session-flow.mmd` is the session. `verify/formal/charts/tracker-writes.mmd` is the tracker, and `charts/bug-1.mmd` through `charts/bug-5.mmd` are the shortest paths TLC found. `charts/tracker-stories.md` is those paths in sentences. `make formal` checks that each chart names the current blob of its spec. After you change a spec and rerun TLC, redraw with `/statechart` and put the new `tla-blob` line back. The last session drawing had 33 states from 128 model states. The last tracker drawing had 45 states from 810 model states.

### Bounds

One node stands in for the Round 1 gate. `mock_block_reason` is all or nothing, so a second node would not change the gate shape. SymPy is an input, pass or miss. The model does not check algebra. Each writer begins at most one command. Finishing a mock that writer opened is a later step. Counts stop at 2. The streak write between the heatmap write and `project` is omitted. `learning` and `skipped` ticks are omitted. Journal notes are omitted. The model does not read gitignored learner files. `session.json` phases stay with `session_problem`. `turn apply` records a mark by calling `record_attempt`, then writes the phase in `write_session`. The chart does not add a phase the CLI does not already store.

### Coverage

| Spec | Code |
|---|---|
| `SessionFlow.tla` | `verify/turn_contract.py` `distinct_correct`, `.cursor/skills/integration-bee-companion/SKILL.md` teach, photo, and mock sections, `scripts/control-integration-bee` `practice check`, `progress mistake`, `turn apply`, `mock-start`, `mock-finish` |
| `TrackerWrites.tla` | `record_attempt`, `write_json`, `project`, `cmd_tick`, `cmd_mock_start`, `cmd_mock_finish`, `finish_plan` in `scripts/control-integration-bee` |

session_flow_blob: fcb8397f65fe9bcd2f15fc54acf50c0b13987742
tracker_writes_blob: eb39ca7919c658137f0c57af267560cd2e026877

Move a blob only after `make formal` passes on that file. `git hash-object` prints it. If the spec changes and the blob line does not, `make formal` fails.

`/maintain-formal-verification-skill` is the update path when covered code moves and this file was not rechecked.
