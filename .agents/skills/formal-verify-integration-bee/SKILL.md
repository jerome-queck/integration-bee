---
name: formal-verify-integration-bee
description: Check Integration Bee unit order, Round 1 mock readiness, tracker record invariants, and the learner-session TLA+ model. Use when editing verify/model.py, verify/formal, unit meta files, the skill-tree catalog, or tracker writes.
---

# Formal checks for Integration Bee

Two checks. `verify/model.py` is a set of Python predicates over catalogs and tracker records. `verify/formal/` is a TLA+ model of one study session and of two writers sharing one data directory. TLC 1.7.4 checks the model. Read the pstack skill `statechart` when you read a TLC result or redraw the chart. Open it from the harness plugin cache named in `docs/setup-manual.md`. Do not copy that skill's commands into this file.

## Catalog predicates

These predicates are not a state machine. `verify/unit_order_check.py` calls `unit01_problem` and `concept_gap`.

- Unit 01 is a concept unit tagged `yang:1.1` and `yang:1.2`. A past-paper unit 01 blocks the pack.
- A catalog with past-paper units and no concept unit is rejected.
- A timed Round 1 mock is blocked until every `gate: round1` node is `solid`, unless the caller passes `--cold`.
- A tick name must be in `trackers/catalog.json`. An attempt interval cannot be negative. Heatmap fails cannot exceed attempts. Streak days cannot repeat.
- A session phase is `idle`, `awaiting_answer`, `mock_open`, `mock_awaiting`, `aptitude`, or `proposing`. Idle has no open problem or mock. An answer phase names a problem. A mock phase names a mock. `aptitude` names a problem. `proposing` waits for confirm and names an offer. `confirm` writes `skipped` only for ids in that offer. An empty list writes no skip. `cover` sets `aptitude.full_coverage` and does not change the phase. A skipped node stays out of the coach queue until full coverage is on or a miss sets the tick back to `learning`. The mock still needs every Round 1 node `solid`.
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
python3 verify/invariants.py --expect-fail aptitude-needs-problem
python3 verify/invariants.py --expect-fail proposing-needs-offer
python3 verify/invariants.py --expect-fail proposing-still-open
python3 verify/invariants.py --expect-fail aptitude-bad-coverage
python3 verify/invariants.py --expect-fail mark-one-bool
python3 verify/invariants.py --expect-fail mark-has-correct
python3 verify/invariants.py --expect-fail sticky-stored-strength
```

The plain command exits 0 on the real tree. Each `--expect-fail` exits 0 only when the planted break is caught.

Bind each of those runs with the evidence block under Learner session model. The inputs are `.agents/skills/formal-verify-integration-bee/SKILL.md`, `verify/model.py`, and the command string. A result counts only when a fresh hash of those bytes matches `$IB_EVIDENCE/binding.txt`. Do not reuse a transcript whose input hash differs. Move `last_confirmed` only under the rule below; a matching evidence hash does not by itself move that line.

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

A formal transcript counts only when `$IB_EVIDENCE/binding.txt` matches a fresh hash of the source text and of the inputs. `IB_CMD` is the exact command string. When the command is one planted break, set `IB_CFG` to that config under `verify/formal/` and include it in the block. From the repository root:

```bash
{
  sha256sum .agents/skills/formal-verify-integration-bee/SKILL.md
  sha256sum verify/model.py
  sha256sum verify/formal/run.sh
  sha256sum verify/formal/SessionFlow.tla
  sha256sum verify/formal/TrackerWrites.tla
  sha256sum verify/formal/SessionFlow.cfg
  sha256sum verify/formal/TrackerWrites.cfg
  if [ -n "${IB_CFG:-}" ]; then sha256sum "$IB_CFG"; fi
  printf '%s\n' "$IB_CMD" | sha256sum
} | tee "$IB_EVIDENCE/binding.txt"
```

Recompute the block after the run. If the skill hash, a spec hash, a config hash, or the command hash differs, the transcript does not count. Do not reuse a transcript whose input hash differs. Move `last_confirmed` and the blob lines only under the rules below.

### Properties that hold

A solid tick in `SessionFlow` follows two correct drills for that node. A stored mock was started with the node solid, or with `--cold`. A photo miss appends a mistake and marks the tag weak and due. An incorrect check does the same for the spaced queue. A stored score follows an opened mock. A skip is stored only after a proposing offer. That skip is not the solid gate. Full coverage does not open the mock.

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
| `SessionFlow.confirm-anytime.cfg` | `SkipFollowsProposal` |
| `SessionFlow.skip-as-solid.cfg` | `SkipIsNotSolid` |
| `TrackerWrites.drop-gate.cfg` | `MockGate` |
| `TrackerWrites.second-open.cfg` | `AtMostOneOpen` |
| `TrackerWrites.lost-attempt.cfg` | `NoLostAttempt` |
| `TrackerWrites.torn-heat.cfg` | `IdleFilesAgree` |
| `TrackerWrites.stale-progress.cfg` | `ProjectionMatches` |
| `TrackerWrites.lost-mock.cfg` | `NoLostMock` |

### Charts

`verify/formal/charts/session-flow.mmd` is the session. `verify/formal/charts/tracker-writes.mmd` is the tracker, and `charts/bug-1.mmd` through `charts/bug-5.mmd` are the shortest paths TLC found. `charts/tracker-stories.md` is those paths in sentences. `make formal` checks that each chart names the current blob of its spec. After you change a spec and rerun TLC, redraw with the pstack skill `statechart` and put the new `tla-blob` line back. The last session drawing had 92 states from 857 model states. The last tracker drawing had 45 states from 810 model states. Comment line numbers in both specs moved to the current CLI. Neither state graph changed, so both drawings are the previous ones with a new `tla-blob`.

### Bounds

The machine feed is 300 drills. All 63 concept nodes are content ready. `floor` is hosted by unit 11 and `dutis` by unit 34; explicit catalog `drill_ids` restrict their automatic evidence to relevant stored drills, including the fixed-interval bridge in unit 11. The original `special-wildcard` route for `U11-D09` through `U11-D15`, tag `yang:1.20`, is unchanged. The five optional syllabus cards have ready unit lessons and explicit empty drill lists: their oral recognition exercises stay outside the automatic queue and award no automatic ticks from host-unit drills. All seven nodes have `gate: null`. `mock_block_reason` still reads the same 20 Round 1 gates. `verify/teaching_catalog_check.py` checks these boundaries, inventory counts, and mutations. `SessionFlow` and `TrackerWrites` still describe the same session phases and tracker writes.

One node stands in for the Round 1 gate. `mock_block_reason` is all or nothing, so a second node would not change the gate shape. SymPy is an input, pass or miss. The model does not check algebra. Each writer begins at most one command. Finishing a mock that writer opened is a later step. Counts stop at 2. The streak write between the heatmap write and `project` is omitted. `learning` ticks are omitted. Journal notes are omitted. Policy rows are omitted. The model does not read gitignored learner files. `session_problem` still checks the stored phase. `SessionFlow` also stores `aptitude` and `proposing`, one placement cycle from the opening idle screen. That cycle is one drill id and one manual contest row, so it does not reach two distinct drills and does not tick solid. A later aptitude is the same action. `plan_cover` keeps the current phase. The spec takes the flag from `idle`, `aptitude`, and `proposing`. Cover during a drill or a mock is the same flag and does not change the gate. `turn apply` records a mark by calling `record_attempt`, then writes the phase in `write_session`. `confirm` writes a skipped tick in `apply_tick` and then calls `write_session`. `TrackerWrites` does not take that pair. A stop between those two writes leaves `skill-ticks.json` ahead of `session.json`. The chart labels phases the CLI stores. A second `mock-start` keeps an unscored mock. `SessionFlow` starts only from no mock, and `TrackerWrites` has that early return. `progress mock-finish` refuses while the session phase is `awaiting_answer`, `aptitude`, or `proposing`. `turn mock-finish` refuses an id other than the open mock. `TrackerWrites` has no session phase, so those refuses are not steps. A photo mark copies `image` into `submissions/<IB_USER>/` before `record_attempt`. A missing file writes no attempt. That copy is outside both specs. `project` also lists pictures from the attempts snapshot it already read.

### Coverage

| Spec | Code |
|---|---|
| `SessionFlow.tla` | `verify/turn_contract.py` `distinct_correct`, `plan_aptitude`, `plan_confirm`, `plan_cover`, `.agents/skills/integration-bee-companion/SKILL.md` teach, photo, mock, aptitude, confirm, and cover sections, `scripts/control-integration-bee` `practice check`, `progress mistake`, `turn apply`, `mock-start`, `mock-finish` |
| `TrackerWrites.tla` | `record_attempt`, `write_json`, `project`, `cmd_tick`, `cmd_mock_start`, `cmd_mock_finish`, `finish_plan` in `scripts/control-integration-bee` |

session_flow_blob: d9fe03829b1cf613445743932298139301c7278f
tracker_writes_blob: beda9eabb9b852eee1729c2e77e615d820ac3c6e

Move a blob only after `make formal` passes on that file. `git hash-object` prints it. If the spec changes and the blob line does not, `make formal` fails.

The pstack skill `maintain-formal-verification-skill` is the update path when covered code moves and this file was not rechecked. Read it from the harness plugin cache in `docs/setup-manual.md`.
