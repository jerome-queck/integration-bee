# Turn

The companion sends one JSON turn. The CLI teaches, marks a photo extract, and opens a mock.

## Sub-features

- `turn-teach` serves `U01-D07` with the answer hidden and stores phase `awaiting_answer`.
- `turn-mark` records a wrong photo extract, then a correct one, and reads both from `progress show`.
- `turn-mock-blocked` refuses a mock before Round 1 nodes are solid.
- `turn-sample` grades `SAMPLE-Q03` and accepts `SAMPLE-Q17` as `ln|ln x|+C`.
- `turn-method-gap` stores a correct final answer with a wrong method as a mark row and a technique card.
- `turn-catalog-mark` records a manual pack problem only when the turn includes `verdict`, and refuses an unanswered Yang practice problem.
- `turn-aptitude` opens `U01-D07` in phase `aptitude` and hides the answer.
- `turn-aptitude-drill` stores a correct `0` and opens `R1-2020-Q01` without a skip.
- `turn-catalog-probe` stores a verdict for that contest row, writes no skip, and proposes `basic-integration`.
- `turn-confirm-early` refuses `confirm` before that offer exists.
- `turn-confirm-decline` accepts an empty node list and writes no skip.

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
- **Catalog mark refused.** Write `{"kind":"mark","problem_id":"R1-2024-Q01","source":"typed","extract":{"final_answer":"sin(1)"}}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json >"$IB_EVIDENCE/turn-catalog-refused.txt" 2>"$IB_EVIDENCE/turn-catalog-refused.err"`. Exit code is 2. Stderr contains `manual problem needs verdict`. Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/turn-catalog-before.json"`. That file does not contain `R1-2024-Q01`.
- **Catalog mark stored.** Write `{"kind":"mark","problem_id":"R1-2024-Q01","source":"typed","verdict":"correct","extract":{"final_answer":"not-a-sympy-expression"}}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json >"$IB_EVIDENCE/turn-catalog-mark.json"`. Exit code is 0. Stdout contains `"correct": true` and `sin(1)`. Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/turn-catalog-show.json"`. That file contains `R1-2024-Q01`.
- **Unanswered Yang.** Write `{"kind":"mark","problem_id":"YANG-1.1-P01","source":"typed","verdict":"correct","extract":{"final_answer":"x"}}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json >"$IB_EVIDENCE/turn-yang-refused.txt" 2>"$IB_EVIDENCE/turn-yang-refused.err"`. Exit code is 2. Stderr contains `no printed answer`. `turn-catalog-show.json` is unchanged, and a fresh `progress show` does not contain `YANG-1.1-P01`.
- **Aptitude start.** Use a new `IB_DATA_DIR` with no session file. Write `{"kind":"aptitude"}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json | tee "$IB_EVIDENCE/turn-aptitude.json"`. Exit code is 0. Stdout contains `U01-D07` and `aptitude`, and does not contain `answer_display`.
- **Confirm refused.** Write `{"kind":"confirm","nodes":["basic-integration"]}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json >"$IB_EVIDENCE/turn-confirm-early.txt" 2>"$IB_EVIDENCE/turn-confirm-early.err"`. Exit code is 2. Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/turn-confirm-early-show.json"`. That file does not contain `skipped`.
- **Drill mark.** Write `{"kind":"mark","problem_id":"U01-D07","source":"typed","extract":{"final_answer":"0"}}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json | tee "$IB_EVIDENCE/turn-aptitude-drill.json"`. Exit code is 0. Stdout contains `R1-2020-Q01` and does not contain `answer_plain` or `skipped`.
- **Catalog probe writes no skip.** Write `{"kind":"mark","problem_id":"R1-2020-Q01","source":"typed","verdict":"correct","extract":{"final_answer":"1"}}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json | tee "$IB_EVIDENCE/turn-aptitude-mark.json"`. Exit code is 0. Stdout contains `proposing` and `basic-integration`. Run `scripts/control-integration-bee progress show --format json >"$IB_EVIDENCE/turn-aptitude-show.json"`. That file contains `R1-2020-Q01` and does not contain `skipped`.
- **Decline.** Write `{"kind":"confirm","nodes":[]}` to `$IB_DATA_DIR/turn.json`. Run `scripts/control-integration-bee turn apply --file "$IB_DATA_DIR/turn.json" --format json | tee "$IB_EVIDENCE/turn-confirm-decline.json"`. Exit code is 0. Stdout contains `idle`. A fresh `progress show` does not contain `skipped`.
- **Rest of the pass.** `verify/turn_contract_check.py` places the next drill, confirms that offered id, and checks that `mock-start` without `cold` still exits 2 with `round1 nodes not solid`. A miss on that drill writes `learning`.

## Gotchas

- A second `teach` while a drill is open repeats that drill.
- An unparsable answer and a manual problem with no `verdict` exit 2 and write nothing. `R1-2024-Q01` is manual. A verdict stores the companion's judgment and does not send the lossy integrand to SymPy.
- `YANG-1.1-P01` has no printed answer. A verdict on that id exits 2 and adds no attempt.
- `mock-start` with `"cold": true` bypasses the Round 1 gate. The blocked proof must omit `cold`.
- `mock-start` with `pack` `pdf-round1` and `year` 2021 reports `count` 40 and `on_disk` true. The problems PDF is `sources/past/r1/2021/2021_Round_1_UK_University_Integration_Bee.pdf`.
- `verify/turn_contract_check.py` drives this contract, including sample grades. `make check` runs it from `verify/run.sh`.
- A correct mark with `method_note` writes `marks.json` (`method_ok` false) and `stickies.json` (one card, no stored strength). A repeat of that same answer while the problem is still open does not append a second attempt. A wrong final answer does not invent `method_ok`.
