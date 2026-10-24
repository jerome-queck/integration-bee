# Drills

Drills lists ids for the companion. Unlike practice, the list includes the display answer.

## Sub-features

- `drills-unit` lists Unit 01 and includes `answer_display`.
- `drills-one` returns a single id.
- `drills-later-unit` lists a Chapter 3 unit on the same path. Units 19–36 are `drills list --unit 19` through `--unit 36`.

## How to get to it (user POV)

- The companion looks up the worked answer after the learner has attempted the drill.

## Driving it with control-integration-bee

Preconditions:

- Doctor has printed `READY integration-bee`.

- **List a unit.** Run `scripts/control-integration-bee drills list --unit 1 --format json | tee "$IB_EVIDENCE/drills-unit.json"`. Exit code is 0. Stdout contains `U01-D01` and `answer_display`.
- **One id.** Run `scripts/control-integration-bee drills list --id U01-D08 --format json | tee "$IB_EVIDENCE/drills-one.json"`. Stdout contains `U01-D08` and does not contain `U01-D01`.
- **Later unit.** Run `scripts/control-integration-bee drills list --unit 19 --format json | tee "$IB_EVIDENCE/drills-later-unit.json"`. Exit code is 0. Stdout contains `U19-D01` and `answer_display`.

## Gotchas

- `practice list` hides answers. `drills list` shows `answer_display`. Do not treat them as the same command.
