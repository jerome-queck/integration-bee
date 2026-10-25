# Progress

Progress stores ticks, misses, mocks, journal notes, and the study streak. `progress show` reads ticks, attempts, due reviews, the streak, and weak topics.

## Sub-features

- `progress-tick` sets `basic-integration` to `learning`.
- `progress-show` returns that tick.
- `progress-mock-blocked` refuses a mock before Round 1 nodes are solid.
- `progress-mistake` records a diagnosed miss for `U01-D01`.
- `progress-mock-cold` opens a mock with `--cold`.
- `progress-mock-finish` stores the score for that mock.
- `progress-journal` stores a technique note that `progress show` does not echo.
- `progress-streak` counts today once.

## How to get to it (user POV)

- The companion marks a concept after practice, records a diagnosed miss, stores a technique note, and does not start a timed mock early.
- A cold paper is `progress mock-start --cold`. The score is `progress mock-finish`.

## Driving it with control-integration-bee

Preconditions:

- `IB_DATA_DIR` has no `basic-integration` tick yet.
- They share that directory.

- **Tick.** Run `scripts/control-integration-bee progress tick --node basic-integration --status learning --format json >"$IB_EVIDENCE/tick.json" 2>"$IB_EVIDENCE/tick.err"`. The exit code is 0. Stdout contains `basic-integration` and `learning`.
- **Show.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/show-after-tick.json" 2>"$IB_EVIDENCE/show-after-tick.err"`. The exit code is 0. Stdout contains `basic-integration`, `learning`, and `"next_node": "basic-integration"`. `attempts` and `due` are empty. `streak.current` is 0.
- **Blocked mock.** Run `scripts/control-integration-bee progress mock-start --format json >"$IB_EVIDENCE/mock.out" 2>"$IB_EVIDENCE/mock.err"`. The exit code is 2. Stdout is empty. Stderr contains `round1 nodes not solid`. `$IB_DATA_DIR/mocks.json` is absent.
- **Mistake.** Run `scripts/control-integration-bee progress mistake --id U01-D01 --tag u-sub --note "sign error" --format json >"$IB_EVIDENCE/mistake.json" 2>"$IB_EVIDENCE/mistake.err"`. The exit code is 0. Stdout contains `U01-D01` and `"recorded": true`.
- **Show the miss.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/show-after-mistake.json"`. The exit code is 0. Stdout contains `U01-D01` and `u-sub`. `streak.current` is 1. `due` is empty on that same Asia/Singapore day.
- **Cold mock.** Run `scripts/control-integration-bee progress mock-start --cold --id cold-1 --format json >"$IB_EVIDENCE/cold.json" 2>"$IB_EVIDENCE/cold.err"`. The exit code is 0. Stdout contains `"id": "cold-1"`, `"cold": true`, and `"score": null`.
- **Bad score.** Run `scripts/control-integration-bee progress mock-finish --id cold-1 --score 31 --out-of 30 --format json >"$IB_EVIDENCE/bad-score.out" 2>"$IB_EVIDENCE/bad-score.err"`. The exit code is 1. Stderr contains `mock score out of range`. The stored session still has `"score": null`.
- **Finish.** Run `scripts/control-integration-bee progress mock-finish --id cold-1 --score 1 --out-of 30 --format json >"$IB_EVIDENCE/finish.json"`. The exit code is 0. Stdout contains `"score": 1`.
- **Journal.** Run `scripts/control-integration-bee progress journal --technique u-sub --note "watch the limits" --format json >"$IB_EVIDENCE/journal.json"`. The exit code is 0. Stdout contains `watch the limits`. `$IB_DATA_DIR/journal.json` contains that note.
- **Show omits the note.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/show-after-journal.json"`. The exit code is 0. Stdout does not contain `watch the limits`.
- **Streak.** Run `scripts/control-integration-bee progress streak --format json >"$IB_EVIDENCE/streak.json"`. The exit code is 0. Stdout contains today's Asia/Singapore date and `"current": 1`. Run the same command again. The exit code is 0 and `current` stays 1.

## Gotchas

- `mock-start --cold` bypasses the Round 1 gate. The blocked proof must omit `--cold`.
- An unknown node exits 1, stderr contains `unknown node`, and `skill-ticks.json` is unchanged.
- `progress show` does not include journal notes or mock scores. Read `journal.json` and `mocks.json`.
- A second `progress streak` on the same Asia/Singapore day does not add another day.
