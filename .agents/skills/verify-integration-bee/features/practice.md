# Practice

Practice serves a drill without the answer, then records a SymPy check.

## Sub-features

- `practice-list` lists drills and hides `answer_display`.
- `practice-next` prints one public drill and writes nothing.
- `practice-check` records a correct attempt for `U01-D08`.
- `practice-unparsed` exits 2 and writes nothing.
- `practice-wrong` records a miss and exits 1.
- `practice-readback` shows the correct attempt from `progress show`.

## How to get to it (user POV)

- The companion sets one integral from `practice next` or `practice list`, reads the learner's answer, and records it with `practice check`.

## Driving it with control-integration-bee

Preconditions:

- Doctor has already printed `READY integration-bee` for this `IB_DATA_DIR`.
- No attempt is stored in that directory.
- Create a second empty directory with `mkdir -p "$IB_WRONG"`. Do not point it at `trackers/live`.
- Create `$IB_INDEF`, `$IB_CONST`, and `$IB_INDEF_BAD` the same way for the indefinite checks.

- **List.** Run `scripts/control-integration-bee practice list --unit 1 --format json >"$IB_EVIDENCE/practice-list.json" 2>"$IB_EVIDENCE/practice-list.err"`. The exit code is 0. Stdout contains `U01-D01` and `U01-D08`. Stdout does not contain `answer_display` or `\pi/4`. The data directory stays empty.
- **Text table.** Run `scripts/control-integration-bee practice list --unit 1 --limit 1 >"$IB_EVIDENCE/practice-table.txt" 2>"$IB_EVIDENCE/practice-table.err"`. The exit code is 0. The first line is `count=8 shown=1`. The next line is `id	unit	technique	kind	latex`. Stdout contains `U01-D01` and does not contain `answer_display`.
- **Next.** Run `scripts/control-integration-bee practice next --format json >"$IB_EVIDENCE/practice-next.json" 2>"$IB_EVIDENCE/practice-next.err"`. The exit code is 0. Stdout contains `"id": "U01-D01"` and does not contain `answer_display`. The data directory stays empty.
- **Unparsed answer.** Run this before any other `practice check` in this directory. Run `scripts/control-integration-bee practice check --id U01-D08 --answer '?' --format json >"$IB_EVIDENCE/practice-unparsed.out" 2>"$IB_EVIDENCE/practice-unparsed.err"`. The exit code is 2. Stdout is empty. Stderr contains `answer did not parse:`. `attempts.json` is absent.
- **Check.** Run `scripts/control-integration-bee practice check --id U01-D08 --answer "pi/4" --format json >"$IB_EVIDENCE/practice-check.json" 2>"$IB_EVIDENCE/practice-check.err"`. The exit code is 0. Stdout contains `"correct": true` and `"expected_display": "\\pi/4"`. `next_due` is the next Asia/Singapore date.
- **Read back.** Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/progress-show.json" 2>"$IB_EVIDENCE/progress-show.err"`. The exit code is 0. Stdout contains `U01-D08` and `"correct": true`. `due` is empty.
- **Wrong answer.** Run `IB_DATA_DIR="$IB_WRONG" scripts/control-integration-bee practice check --id U01-D08 --answer 0 --format json >"$IB_EVIDENCE/practice-wrong.json" 2>"$IB_EVIDENCE/practice-wrong.err"`. The exit code is 1. Stdout contains `"correct": false` and `"expected_display": "\\pi/4"`. Then run `IB_DATA_DIR="$IB_WRONG" scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/progress-show-wrong.json" 2>"$IB_EVIDENCE/progress-show-wrong.err"`. The exit code is 0. Stdout contains `U01-D08` and `"correct": false`.
- **Indefinite constant.** Run `IB_DATA_DIR="$IB_INDEF" scripts/control-integration-bee practice check --id U01-D06 --answer "log(x**2+3*x+2)+C" --format json >"$IB_EVIDENCE/practice-indef.json" 2>"$IB_EVIDENCE/practice-indef.err"`. The exit code is 0. Stdout contains `"correct": true` and `"id": "U01-D06"`. Run `IB_DATA_DIR="$IB_CONST" scripts/control-integration-bee practice check --id U01-D06 --answer "log(x**2+3*x+2)+1" --format json >"$IB_EVIDENCE/practice-const.json"`. The exit code is 0. Stdout contains `"correct": true`. Run `IB_DATA_DIR="$IB_INDEF_BAD" scripts/control-integration-bee practice check --id U01-D06 --answer "log(x)" --format json >"$IB_EVIDENCE/practice-indef-bad.json"`. The exit code is 1. Stdout contains `"correct": false`. `progress show` for that directory contains `U01-D06`.

## Gotchas

- A wrong answer exits 1 and still records the miss. The first correct attempt on a fresh directory has `reps` 1, `interval_days` 1, and `ease` 2.5. The first miss has `reps` 0, `interval_days` 1, and `ease` 2.3.
- `atan(1)` is also correct for `U01-D08`. A bare word such as `foo` parses as a symbol, records a miss, and exits 1. Only a syntax error such as `?` exits 2 and writes nothing.
- `practice check` prints the display answer as `expected_display`. `practice list` and `practice next` omit it.
- Text format for `practice list` is the count line and a tab-separated table. The columns are `id`, `unit`, `technique`, `kind`, and `latex`. JSON is the recorded result.
- `U01-D06` is indefinite. A constant difference is correct, including a trailing `+C`. `log(x)` is a miss: exit 1, and the attempt is stored.
- Forgetting `IB_DATA_DIR` writes `trackers/live` and `progress.local.json` at the repository root.
