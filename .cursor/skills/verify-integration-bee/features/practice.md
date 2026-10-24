# Practice

Practice serves a drill without the answer, then records a SymPy check.

## Sub-features

- `practice-list` lists drills and hides `answer_display`.
- `practice-check` records a correct attempt for `U01-D08`.
- `practice-readback` shows that attempt from `progress show`.

## How to get to it (user POV)

- The companion sets one integral, reads the learner's answer, and records it.

## Driving it with control-integration-bee

Preconditions:

- Doctor has already printed `READY integration-bee` for this `IB_DATA_DIR`.
- No attempt for `U01-D08` is stored in that directory.

- **List.** Run `scripts/control-integration-bee practice list --unit 1 --format json | tee "$IB_EVIDENCE/practice-list.json"`. Exit code is 0. Stdout contains `U01-D08` and does not contain `answer_display`.
- **Check.** Run `scripts/control-integration-bee practice check --id U01-D08 --answer "pi/4" --format json | tee "$IB_EVIDENCE/practice-check.json"`. Exit code is 0. Stdout contains `"correct": true`.
- **Read back.** Run `scripts/control-integration-bee progress show --format json | tee "$IB_EVIDENCE/progress-show.json"`. Stdout contains `U01-D08`.

## Gotchas

- A wrong answer exits 1 and still records the miss. Use `pi/4` for the proof run.
- An unparsable answer exits 2 and writes nothing.
- Forgetting `IB_DATA_DIR` writes `trackers/live`.
