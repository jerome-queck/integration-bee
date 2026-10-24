# Turn

The companion sends one JSON turn. The CLI teaches, marks a photo extract, and opens a mock.

## Sub-features

- `turn-teach` serves `U01-D07` with the answer hidden and stores phase `awaiting_answer`.
- `turn-mark` records a wrong photo extract, then a correct one, and reads both from `progress show`.
- `turn-mock-blocked` refuses a mock before Round 1 nodes are solid.
- `turn-sample` grades `SAMPLE-Q03` and accepts `SAMPLE-Q17` as `ln|ln x|+C`.
- `turn-method-gap` stores a correct final answer with a wrong method as a mark row and a technique card.

## How to get to it (user POV)

- The learner asks for a concept, sends a photo of a solution, or asks for a timed mock. The companion sends the turn. The learner does not run the CLI.

## Driving it with control-integration-bee

Preconditions:

- Doctor has already printed `READY integration-bee` for this `IB_DATA_DIR`.
- The directory has no session file yet.

- **Schema.** Run `scripts/control-integration-bee turn schema --format json | tee "$IB_EVIDENCE/turn-schema.json"`. Exit code is 0. Stdout contains `mark` and `awaiting_answer`.
- **Teach.** Write `{"kind":"teach"}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json | tee "$IB_EVIDENCE/turn-teach.json"`. Exit code is 0. Stdout contains `U01-D07` and `awaiting_answer`, and does not contain `answer_display`.
- **Wrong mark.** Write `{"kind":"mark","problem_id":"U01-D07","source":"photo","extract":{"final_answer":"1"}}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json >"$IB_EVIDENCE/turn-wrong.json"`. Exit code is 1. Stdout contains `"correct": false`.
- **Read back.** Run `scripts/control-integration-bee progress show --format json | tee "$IB_EVIDENCE/turn-show.json"`. Stdout contains `U01-D07`.
- **Blocked mock.** Write `{"kind":"mock-start"}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json >"$IB_EVIDENCE/turn-mock.txt" 2>"$IB_EVIDENCE/turn-mock.err"`. Exit code is 2. Stderr contains `round1 nodes not solid`.

## Gotchas

- A second `teach` while a drill is open repeats that drill.
- An unparsable answer and a manual problem with no `verdict` exit 2 and write nothing.
- `mock-start` with `"cold": true` bypasses the Round 1 gate. The blocked proof must omit `cold`.
- `verify/turn_contract_check.py` drives this contract, including sample grades. `make check` runs it from `verify/run.sh`.
- A correct mark with `method_note` writes `marks.json` (`method_ok` false) and `stickies.json` (one card, no stored strength). A repeat of that same answer while the problem is still open does not append a second attempt. A wrong final answer does not invent `method_ok`.
