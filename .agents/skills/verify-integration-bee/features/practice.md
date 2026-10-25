# Practice

Practice serves a drill without the answer, then records a SymPy check.

## Sub-features

- `practice-list` lists drills and hides `answer_display`.
- `practice-next` prints one public drill and writes nothing.
- `practice-check` records a correct attempt for `U01-D08`.
- `practice-unparsed` exits 2 and writes nothing.
- `practice-wrong` records a miss and exits 1.
- `practice-readback` shows the correct attempt from `progress show`.
- `practice-floor` lists `U11-D09` through `U11-D12` without answers and records `U11-D09` and `U11-D12`.
- `practice-dutis` lists `U11-D13` through `U11-D15` without answers and records `U11-D13` and `U11-D15`.

## How to get to it (user POV)

- The companion sets one integral from `practice next` or `practice list`, reads the learner's answer, and records it with `practice check`.
- A floor or DUTIS integral is a unit 11 drill. `practice list --tag floor` and `practice list --tag dutis` hide the answer. The skill-tree rows for `floor` and `dutis` are content ready, and the served node is `special-wildcard`.

## Driving it with control-integration-bee

Preconditions:

- Doctor has already printed `READY integration-bee` for this `IB_DATA_DIR`.
- No attempt is stored in that directory.
- Create a second empty directory with `mkdir -p "$IB_WRONG"`. Do not point it at `trackers/live`.
- Create `$IB_INDEF`, `$IB_CONST`, and `$IB_INDEF_BAD` the same way for the indefinite checks.
- Create `$IB_FLOOR` and `$IB_DUTIS` the same way for the unit 11 checks.

- **List.** Run `scripts/control-integration-bee practice list --unit 1 --format json >"$IB_EVIDENCE/practice-list.json" 2>"$IB_EVIDENCE/practice-list.err"`. The exit code is 0. Stdout contains `U01-D01` and `U01-D08`. Stdout does not contain `answer_display` or `\pi/4`. The data directory stays empty.
- **Text table.** Run `scripts/control-integration-bee practice list --unit 1 --limit 1 >"$IB_EVIDENCE/practice-table.txt" 2>"$IB_EVIDENCE/practice-table.err"`. The exit code is 0. The first line is `count=8 shown=1`. The next line is `id	unit	technique	kind	latex`. Stdout contains `U01-D01` and does not contain `answer_display`.
- **Next.** Run `scripts/control-integration-bee practice next --format json >"$IB_EVIDENCE/practice-next.json" 2>"$IB_EVIDENCE/practice-next.err"`. The exit code is 0. Stdout contains `"id": "U01-D01"` and does not contain `answer_display`. The data directory stays empty.
- **Unparsed answer.** Run this before any other `practice check` in this directory. Run `scripts/control-integration-bee practice check --id U01-D08 --answer '?' --format json >"$IB_EVIDENCE/practice-unparsed.out" 2>"$IB_EVIDENCE/practice-unparsed.err"`. The exit code is 2. Stdout is empty. Stderr contains `answer did not parse:`. `attempts.json` is absent.
- **Check.** Run `scripts/control-integration-bee practice check --id U01-D08 --answer "pi/4" --format json >"$IB_EVIDENCE/practice-check.json" 2>"$IB_EVIDENCE/practice-check.err"`. The exit code is 0. Stdout contains `"correct": true` and `"expected_display": "\\pi/4"`. `next_due` is the next Asia/Singapore date.
- **Read back.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/progress-show.json" 2>"$IB_EVIDENCE/progress-show.err"`. The exit code is 0. Stdout contains `U01-D08` and `"correct": true`. `due` is empty.
- **Wrong answer.** Run `IB_DATA_DIR="$IB_WRONG" scripts/control-integration-bee practice check --id U01-D08 --answer 0 --format json >"$IB_EVIDENCE/practice-wrong.json" 2>"$IB_EVIDENCE/practice-wrong.err"`. The exit code is 1. Stdout contains `"correct": false` and `"expected_display": "\\pi/4"`. Then run `IB_DATA_DIR="$IB_WRONG" scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/progress-show-wrong.json" 2>"$IB_EVIDENCE/progress-show-wrong.err"`. The exit code is 0. Stdout contains `U01-D08` and `"correct": false`.
- **Indefinite constant.** Run `IB_DATA_DIR="$IB_INDEF" scripts/control-integration-bee practice check --id U01-D06 --answer "log(x**2+3*x+2)+C" --format json >"$IB_EVIDENCE/practice-indef.json" 2>"$IB_EVIDENCE/practice-indef.err"`. The exit code is 0. Stdout contains `"correct": true` and `"id": "U01-D06"`. Run `IB_DATA_DIR="$IB_CONST" scripts/control-integration-bee practice check --id U01-D06 --answer "log(x**2+3*x+2)+1" --format json >"$IB_EVIDENCE/practice-const.json"`. The exit code is 0. Stdout contains `"correct": true`. Run `IB_DATA_DIR="$IB_INDEF_BAD" scripts/control-integration-bee practice check --id U01-D06 --answer "log(x)" --format json >"$IB_EVIDENCE/practice-indef-bad.json"`. The exit code is 1. Stdout contains `"correct": false`. `progress show` for that directory contains `U01-D06`.
- **Floor list.** Run `scripts/control-integration-bee practice list --tag floor >"$IB_EVIDENCE/practice-floor.txt" 2>"$IB_EVIDENCE/practice-floor.err"`. The exit code is 0. The first line is `count=4`. Stdout contains `U11-D09`, `U11-D12`, and `floor`. Stdout does not contain `answer_display`. Run `scripts/control-integration-bee practice list --tag floor --format json >"$IB_EVIDENCE/practice-floor.json"`. The exit code is 0. Stdout contains `U11-D09`, `U11-D10`, `U11-D11`, `U11-D12`, `"technique": "floor"`, `11-gaussian-wildcard`, and `yang:1.20`. Stdout does not contain `answer_display`. The list command writes nothing.
- **DUTIS list.** Run `scripts/control-integration-bee practice list --tag dutis >"$IB_EVIDENCE/practice-dutis.txt" 2>"$IB_EVIDENCE/practice-dutis.err"`. The exit code is 0. The first line is `count=3`. Stdout contains `U11-D13`, `U11-D15`, and `dutis`. Stdout does not contain `answer_display`. Run `scripts/control-integration-bee practice list --unit 11 --format json >"$IB_EVIDENCE/practice-unit11.json"`. The exit code is 0. Stdout contains `U11-D09` and `U11-D15`. Stdout does not contain `answer_display`. `scripts/control-integration-bee practice list --unit 11` starts with `count=15`.
- **Floor check.** Run `IB_DATA_DIR="$IB_FLOOR" scripts/control-integration-bee practice check --id U11-D09 --answer 6 --format json >"$IB_EVIDENCE/practice-floor-check.json" 2>"$IB_EVIDENCE/practice-floor-check.err"`. The exit code is 0. Stdout contains `"id": "U11-D09"`, `"correct": true`, and `"expected_display": "6"`. Run `IB_DATA_DIR="$IB_FLOOR" scripts/control-integration-bee practice check --id U11-D12 --answer -3 --format json >"$IB_EVIDENCE/practice-floor-neg.json"`. The exit code is 0. Stdout contains `"expected_display": "-3"`. Run `IB_DATA_DIR="$IB_FLOOR" scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/practice-floor-show.json"`. The exit code is 0. Stdout contains `U11-D09`, `U11-D12`, and `"correct": true`.
- **DUTIS check.** Run `IB_DATA_DIR="$IB_DUTIS" scripts/control-integration-bee practice check --id U11-D13 --answer "(-1)/25" --format json >"$IB_EVIDENCE/practice-dutis-check.json" 2>"$IB_EVIDENCE/practice-dutis-check.err"`. The exit code is 0. Stdout contains `"id": "U11-D13"`, `"correct": true`, and `"expected_display": "-1/25"`. Run `IB_DATA_DIR="$IB_DUTIS" scripts/control-integration-bee practice check --id U11-D15 --answer "log(4)" --format json >"$IB_EVIDENCE/practice-dutis-ln.json"`. The exit code is 0. Stdout contains `"expected_display": "\\ln 4"`. Run `IB_DATA_DIR="$IB_DUTIS" scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/practice-dutis-show.json"`. The exit code is 0. Stdout contains `U11-D13` and `U11-D15`.

## Gotchas

- A wrong answer exits 1 and still records the miss. The first correct attempt on a fresh directory has `reps` 1, `interval_days` 1, and `ease` 2.5. The first miss has `reps` 0, `interval_days` 1, and `ease` 2.3.
- `atan(1)` is also correct for `U01-D08`. A bare word such as `foo` parses as a symbol, records a miss, and exits 1. Only a syntax error such as `?` exits 2 and writes nothing.
- `practice check` prints the display answer as `expected_display`. `practice list` and `practice next` omit it.
- Text format for `practice list` is the count line and a tab-separated table. The columns are `id`, `unit`, `technique`, `kind`, and `latex`. JSON is the recorded result.
- `U01-D06` is indefinite. A constant difference is correct, including a trailing `+C`. `log(x)` is a miss: exit 1, and the attempt is stored.
- Floor drills `U11-D09` through `U11-D12` and DUTIS drills `U11-D13` through `U11-D15` are definite rows on unit 11. `practice list --tag floor` returns four rows. `practice list --tag dutis` returns three. `practice list --unit 11` returns `count=15`. `6` and `-3` match `U11-D09` and `U11-D12`. `(-1)/25` matches `U11-D13` and the display is `-1/25`. `log(4)` matches `U11-D15` and the display is `\ln 4`. `--answer -1/25` is read as a flag: argparse prints `expected one argument`, the exit code is 2, and `attempts.json` stays absent.
- Forgetting `IB_DATA_DIR` writes `trackers/live` and `progress.local.json` at the repository root.
