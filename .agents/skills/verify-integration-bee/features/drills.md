# Drills

`drills list` returns ids and includes the display answer. `practice list` does not.

Record the sha256 of `.agents/skills/verify-integration-bee/features/drills.md` and of the drills command in `$IB_EVIDENCE` before the transcript counts. Recompute both from the bytes just read.

## Sub-features

- `drills-unit` lists Unit 01 and includes `answer_display`.
- `drills-one` returns one id and exits 0.
- `drills-later-unit` lists a Chapter 3 unit on the same path. Units 19 to 36 are `drills list --unit 19` through `--unit 36`.
- `drills-floor-dutis` lists unit 11. Floor is `U11-D09` through `U11-D12`. DUTIS is `U11-D13` through `U11-D15`. Both include `answer_display`.
- `drills-empty` exits 1 when the filter matches nothing.

## How to get to it (user POV)

- The companion looks up the worked answer after the learner has attempted the drill.
- Floor and DUTIS answers are on unit 11. `skill-tree.md` marks `floor` and `dutis` content ready. The coach serves those drills on `special-wildcard`.

## Driving it with control-integration-bee

Preconditions:

- Doctor has printed `READY integration-bee`.

- **List a unit.** Run `scripts/control-integration-bee drills list --unit 1 --format json >"$IB_EVIDENCE/drills-unit.json" 2>"$IB_EVIDENCE/drills-unit.err"`. The exit code is 0. Stdout contains `U01-D01`, `U01-D08`, and `answer_display`. Stderr is empty.
- **Text table.** Run `scripts/control-integration-bee drills list --unit 1 --limit 1 >"$IB_EVIDENCE/drills-table.txt" 2>"$IB_EVIDENCE/drills-table.err"`. The exit code is 0. The first line is `count=8 shown=1`. The next line is `id	unit	technique	kind	answer_display`. Stdout contains `U01-D01`.
- **One id.** Run `scripts/control-integration-bee drills list --id U01-D08 --format json >"$IB_EVIDENCE/drills-one.json" 2>"$IB_EVIDENCE/drills-one.err"`. The exit code is 0. Stdout contains `U01-D08` and `answer_display`. Stdout does not contain `U01-D01`.
- **Later unit.** Run `scripts/control-integration-bee drills list --unit 19 --format json >"$IB_EVIDENCE/drills-later-unit.json" 2>"$IB_EVIDENCE/drills-later-unit.err"`. The exit code is 0. Stdout contains `U19-D01` and `answer_display`.
- **Unit 11 table.** Run `scripts/control-integration-bee drills list --unit 11 >"$IB_EVIDENCE/drills-unit11.txt" 2>"$IB_EVIDENCE/drills-unit11.err"`. The exit code is 0. The first line is `count=15`. Stdout contains `U11-D09`, `U11-D12`, `U11-D13`, `U11-D15`, `floor`, `dutis`, and `\ln 4`. Stderr is empty.
- **Unit 11 JSON.** Run `scripts/control-integration-bee drills list --unit 11 --format json >"$IB_EVIDENCE/drills-unit11.json" 2>"$IB_EVIDENCE/drills-unit11-json.err"`. The exit code is 0. Stdout contains `U11-D09`, `"technique": "floor"`, `"answer_display": "6"`, `U11-D12`, `"answer_display": "-3"`, `U11-D13`, `"technique": "dutis"`, `"answer_display": "-1/25"`, `U11-D15`, `"answer_display": "\\ln 4"`, `11-gaussian-wildcard`, and `yang:1.20`. Stderr is empty.
- **One floor id.** Run `scripts/control-integration-bee drills list --id U11-D09 --format json >"$IB_EVIDENCE/drills-floor.json" 2>"$IB_EVIDENCE/drills-floor.err"`. The exit code is 0. Stdout contains `U11-D09` and `"answer_display": "6"`. Stdout does not contain `U11-D01` or `U11-D13`.
- **Empty filter.** Run `scripts/control-integration-bee drills list --unit 37 --format json >"$IB_EVIDENCE/drills-empty.json" 2>"$IB_EVIDENCE/drills-empty.err"`. The exit code is 1. Stdout contains `"drills": []`. Stderr is empty.
- **Practice list hides the answer.** Run `scripts/control-integration-bee practice list --unit 37 --format json >"$IB_EVIDENCE/practice-empty.json" 2>"$IB_EVIDENCE/practice-empty.err"`. The exit code is 0. Stdout contains `"drills": []` and does not contain `answer_display`. Stderr is empty.

## Gotchas

- `practice list` hides answers and exits 0 when the filter matches nothing. `drills list` shows `answer_display` and exits 1 when the list is empty.
- `practice check` copies the same display string into `expected_display`. That key is not `answer_display`.
- Text format is that count line and a tab-separated table. The columns add `answer_display` to the practice-list columns. JSON is the recorded result.
- Unit 11 has 15 drills. `U11-D09` through `U11-D12` use technique `floor`. `U11-D13` through `U11-D15` use technique `dutis`. Every new row has yang tag `yang:1.20` and unit `11-gaussian-wildcard`. Display answers are `6`, `3/2`, `2`, `-3`, `-1/25`, `1/4`, and `\ln 4`. `skill-tree.md` marks the catalog rows `floor` and `dutis` content ready. Their catalog homes are unit 11 for `floor` and unit 34 for `dutis`. Explicit catalog drill lists also select the relevant floor/DUTIS evidence without changing the wildcard route.
