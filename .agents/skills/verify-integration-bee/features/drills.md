# Drills

`drills list` returns ids and includes the display answer. `practice list` does not.

## Sub-features

- `drills-unit` lists Unit 01 and includes `answer_display`.
- `drills-one` returns one id and exits 0.
- `drills-later-unit` lists a Chapter 3 unit on the same path. Units 19 to 36 are `drills list --unit 19` through `--unit 36`.
- `drills-empty` exits 1 when the filter matches nothing.

## How to get to it (user POV)

- The companion looks up the worked answer after the learner has attempted the drill.

## Driving it with control-integration-bee

Preconditions:

- Doctor has printed `READY integration-bee`.

- **List a unit.** Run `scripts/control-integration-bee drills list --unit 1 --format json >"$IB_EVIDENCE/drills-unit.json" 2>"$IB_EVIDENCE/drills-unit.err"`. The exit code is 0. Stdout contains `U01-D01`, `U01-D08`, and `answer_display`. Stderr is empty.
- **One id.** Run `scripts/control-integration-bee drills list --id U01-D08 --format json >"$IB_EVIDENCE/drills-one.json" 2>"$IB_EVIDENCE/drills-one.err"`. The exit code is 0. Stdout contains `U01-D08` and `answer_display`. Stdout does not contain `U01-D01`.
- **Later unit.** Run `scripts/control-integration-bee drills list --unit 19 --format json >"$IB_EVIDENCE/drills-later-unit.json" 2>"$IB_EVIDENCE/drills-later-unit.err"`. The exit code is 0. Stdout contains `U19-D01` and `answer_display`.
- **Empty filter.** Run `scripts/control-integration-bee drills list --unit 37 --format json >"$IB_EVIDENCE/drills-empty.json" 2>"$IB_EVIDENCE/drills-empty.err"`. The exit code is 1. Stdout contains `"drills": []`. Stderr is empty.
- **Practice list hides the answer.** Run `scripts/control-integration-bee practice list --unit 37 --format json >"$IB_EVIDENCE/practice-empty.json" 2>"$IB_EVIDENCE/practice-empty.err"`. The exit code is 0. Stdout contains `"drills": []` and does not contain `answer_display`. Stderr is empty.

## Gotchas

- `practice list` hides answers and exits 0 when the filter matches nothing. `drills list` shows `answer_display` and exits 1 when the list is empty.
- `practice check` copies the same display string into `expected_display`. That key is not `answer_display`.
