# Progress

Progress stores ticks, misses, mocks, journal notes, and the study streak. `progress show` reads ticks, attempts, due reviews, the streak, and weak topics.

Record the sha256 of `.agents/skills/verify-integration-bee/features/progress.md`, of each progress command string, and of `trackers/catalog.json` in `$IB_EVIDENCE/binding.txt`. Recompute those hashes from the bytes just read. If one differs, the transcript does not count.

## Sub-features

- `progress-tick` sets `basic-integration` to `learning`.
- `progress-show` returns that tick.
- `progress-mock-blocked` refuses a mock before Round 1 nodes are solid.
- `progress-mistake` records a diagnosed miss for `U01-D01`.
- `progress-mock-cold` opens a mock with `--cold`.
- `progress-mock-finish` stores the score for that mock.
- `progress-journal` stores a technique note that `progress show` does not echo.
- `progress-streak` counts today once.
- `progress-syllabus` stores a tick for `floor` and for `dutis`. `next_node` stays `basic-integration`.

## How to get to it (user POV)

- The companion marks a concept after practice, records a diagnosed miss, stores a technique note, and does not start a timed mock early.
- A cold paper is `progress mock-start --cold`. The score is `progress mock-finish`.
- `floor` and `dutis` are ready catalog nodes hosted by units 11 and 34, with `gate: null`. Their explicit stored-drill evidence is listed in `pedagogy/round1-coach.md`; unit 11 still serves the same bridge on `special-wildcard`. The top-level `progress show` field `next_node` remains the first unmet Round 1 gate, independently of the wider `coach.next_node` queue.

## Driving it with control-integration-bee

Preconditions:

- `IB_DATA_DIR` has no `basic-integration` tick yet.
- They share that directory.
- `$IB_PHASE`, `$IB_OFFER`, and `$IB_SYLLABUS` are other empty directories. Do not point them at `trackers/live`.

- **Tick.** Run `scripts/control-integration-bee progress tick --node basic-integration --status learning --format json >"$IB_EVIDENCE/tick.json" 2>"$IB_EVIDENCE/tick.err"`. The exit code is 0. Stdout contains `basic-integration` and `learning`.
- **Show.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/show-after-tick.json" 2>"$IB_EVIDENCE/show-after-tick.err"`. The exit code is 0. Stdout contains `basic-integration`, `learning`, and `"next_node": "basic-integration"`. `attempts` and `due` are empty. `streak.current` is 0.
- **Blocked mock.** Run `scripts/control-integration-bee progress mock-start --format json >"$IB_EVIDENCE/mock.out" 2>"$IB_EVIDENCE/mock.err"`. The exit code is 2. Stdout is empty. Stderr contains `round1 nodes not solid`. `$IB_DATA_DIR/mocks.json` is absent.
- **Mistake.** Run `scripts/control-integration-bee progress mistake --id U01-D01 --tag u-sub --note "sign error" --format json >"$IB_EVIDENCE/mistake.json" 2>"$IB_EVIDENCE/mistake.err"`. The exit code is 0. Stdout contains `U01-D01` and `"recorded": true`.
- **Show the miss.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/show-after-mistake.json"`. The exit code is 0. Stdout contains `U01-D01` and `u-sub`. `streak.current` is 1. `due` is empty on that same Asia/Singapore day.
- **Cold mock.** Run `scripts/control-integration-bee progress mock-start --cold --id cold-1 --format json >"$IB_EVIDENCE/cold.json" 2>"$IB_EVIDENCE/cold.err"`. The exit code is 0. Stdout contains `"id": "cold-1"`, `"cold": true`, and `"score": null`.
- **Open mock stays.** Run `scripts/control-integration-bee progress mock-start --cold --id cold-2 --format json >"$IB_EVIDENCE/cold-again.json" 2>"$IB_EVIDENCE/cold-again.err"`. The exit code is 0. Stdout contains `"id": "cold-1"` and does not contain `cold-2`. `$IB_DATA_DIR/mocks.json` has one session and that id is `cold-1`.
- **Bad score.** Run `scripts/control-integration-bee progress mock-finish --id cold-1 --score 31 --out-of 30 --format json >"$IB_EVIDENCE/bad-score.out" 2>"$IB_EVIDENCE/bad-score.err"`. The exit code is 1. Stderr contains `mock score out of range`. The stored session still has `"score": null`.
- **Finish.** Run `scripts/control-integration-bee progress mock-finish --id cold-1 --score 1 --out-of 30 --format json >"$IB_EVIDENCE/finish.json"`. The exit code is 0. Stdout contains `"score": 1`.
- **Journal.** Run `scripts/control-integration-bee progress journal --technique u-sub --note "watch the limits" --format json >"$IB_EVIDENCE/journal.json"`. The exit code is 0. Stdout contains `watch the limits`. `$IB_DATA_DIR/journal.json` contains that note.
- **Show omits the note.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/show-after-journal.json"`. The exit code is 0. Stdout does not contain `watch the limits`.
- **Streak.** Run `scripts/control-integration-bee progress streak --format json >"$IB_EVIDENCE/streak.json"`. The exit code is 0. Stdout contains today's Asia/Singapore date and `"current": 1`. Run the same command again. The exit code is 0 and `current` stays 1.
- **Finish while a drill is open.** Use a new empty directory `$IB_PHASE`. Run `IB_DATA_DIR="$IB_PHASE" scripts/control-integration-bee progress mock-start --cold --id phase-1 --format json >"$IB_EVIDENCE/phase-start.json"`. The exit code is 0. Write `{"kind":"teach"}` to `$IB_PHASE/turn.json`. Run `IB_DATA_DIR="$IB_PHASE" scripts/control-integration-bee turn apply --file "$IB_PHASE/turn.json" --format json >"$IB_EVIDENCE/phase-teach.json"`. The exit code is 0. Stdout contains `awaiting_answer`. Run `IB_DATA_DIR="$IB_PHASE" scripts/control-integration-bee progress mock-finish --id phase-1 --score 1 --out-of 30 --format json >"$IB_EVIDENCE/phase-finish.out" 2>"$IB_EVIDENCE/phase-finish.err"`. The exit code is 2. Stderr contains `an integral is still open`. The stored session still has `"score": null`.
- **Finish during a skip offer.** Use a new empty directory `$IB_OFFER`. Repeat the aptitude start, the `U01-D07` mark of `0`, and the automatic `R1-2022-MIT-TB-Q01` mark of `1` from the turn feature until the phase is `proposing`. Run `IB_DATA_DIR="$IB_OFFER" scripts/control-integration-bee progress mock-start --cold --id offer-1 --format json >"$IB_EVIDENCE/offer-start.json"`. The exit code is 0. Run `IB_DATA_DIR="$IB_OFFER" scripts/control-integration-bee progress mock-finish --id offer-1 --score 1 --out-of 30 --format json >"$IB_EVIDENCE/offer-finish.out" 2>"$IB_EVIDENCE/offer-finish.err"`. The exit code is 2. Stderr contains `confirm the skip offer first`. The stored score is still `null`.
- **Syllabus ticks.** Use the empty directory `$IB_SYLLABUS`. Run `IB_DATA_DIR="$IB_SYLLABUS" scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/syllabus-empty.json"`. The exit code is 0. Stdout contains `"next_node": "basic-integration"` and `"ticks": {}`. Run `IB_DATA_DIR="$IB_SYLLABUS" scripts/control-integration-bee progress tick --node floor --status learning --format json >"$IB_EVIDENCE/tick-floor.json" 2>"$IB_EVIDENCE/tick-floor.err"`. The exit code is 0. Stdout contains `floor` and `learning`. Run `IB_DATA_DIR="$IB_SYLLABUS" scripts/control-integration-bee progress tick --node dutis --status learning --format json >"$IB_EVIDENCE/tick-dutis.json" 2>"$IB_EVIDENCE/tick-dutis.err"`. The exit code is 0. Stdout contains `dutis` and `learning`. Run `IB_DATA_DIR="$IB_SYLLABUS" scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/syllabus-show.json"`. The exit code is 0. Stdout contains `floor`, `dutis`, `learning`, and `"next_node": "basic-integration"`.

## Gotchas

- `mock-start --cold` bypasses the Round 1 gate. The blocked proof must omit `--cold`.
- A second `mock-start` while a session has `"score": null` returns that session and does not append another. `mock-finish` exits 2 while the session phase is `awaiting_answer` or `aptitude` (`an integral is still open`) or `proposing` (`confirm the skip offer first`). The mock file is unchanged.
- An unknown node exits 1, stderr contains `unknown node`, and `skill-ticks.json` is unchanged.
- `trackers/catalog.json` gives `floor` and `dutis` `status: ready`, real unit homes, and `gate: null`. Content readiness itself writes no learner ticks. `progress tick` still accepts the ids, and top-level `progress show.next_node` still reads the Round 1 gates, so the isolated syllabus-tick drive keeps `basic-integration`. The wider coach queue uses the explicit floor/DUTIS drill lists. The five optional recognition nodes have empty drill lists and receive no automatic mastery from unrelated host-unit attempts.
- `progress show` does not include journal notes or mock scores. Read `journal.json` and `mocks.json`.
- A second `progress streak` on the same Asia/Singapore day does not add another day.
