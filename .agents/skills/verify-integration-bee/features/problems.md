# Problems

The contest catalog lists resource-pack and Yang integrals. List and select hide answers. Show prints the stored cite.

## Sub-features

- `problems-round` lists Round 1 ids and hides answers.
- `problems-show` returns `R1-2024-Q01` with the mark-scheme cite.
- `problems-select` returns unanswered Yang practice `YANG-1.1-P01` with the integrand and without an answer.
- `problems-ambiguous` refuses a select that matches more than one id.
- `problems-sample` lists `SAMPLE-Q01` through `SAMPLE-Q20` and hides answers.

## How to get to it (user POV)

- The companion looks up a contest integral or a Yang practice integral before setting it. The learner does not run the CLI.

## Driving it with control-integration-bee

Preconditions:

- Doctor has printed `READY integration-bee`.
- `IB_DATA_DIR` is empty.

- **Round list.** Run `scripts/control-integration-bee problems list --round r1 --format json >"$IB_EVIDENCE/problems-round.json"`. Exit code is 0. Stdout contains `R1-2024-Q01` and `"count": 280`. Stdout does not contain `answer_plain` or `answer_sympy`.
- **Show one.** Run `scripts/control-integration-bee problems show --id R1-2024-Q01 --format json >"$IB_EVIDENCE/problems-show.json"`. Exit code is 0. Stdout contains `sin(1)`, `"verify": "sympy"`, and `Mark_Scheme_2024_Round_1_UK_University_Integration_Bee.pdf`.
- **Show a proved row.** Run `scripts/control-integration-bee problems show --id R1-2020-Q08 --format json >"$IB_EVIDENCE/problems-show-sympy.json"`. Exit code is 0. Stdout contains `"verify": "sympy"`, `answer_sympy`, and `Virtual_integration_competition_answers.pdf`.
- **Select one.** Run `scripts/control-integration-bee problems select --id YANG-1.1-P01 --format json >"$IB_EVIDENCE/problems-select.json"`. Exit code is 0. Stdout contains `unchecked` and `integrand_plain`. Stdout does not contain `answer_plain`.
- **Ambiguous select.** Run `scripts/control-integration-bee problems select --round r1 --format json >"$IB_EVIDENCE/problems-ambiguous.txt" 2>"$IB_EVIDENCE/problems-ambiguous.err"`. Exit code is 2. Stderr contains `matched`.
- **Sample list.** Run `scripts/control-integration-bee problems list --round sample --format json >"$IB_EVIDENCE/problems-sample.json"`. Exit code is 0. Stdout contains `SAMPLE-Q01`, `SAMPLE-Q20`, and `"count": 20`. Stdout does not contain `answer_plain` or `answer_sympy`.
- **Sample table.** Run `scripts/control-integration-bee problems list --round sample --limit 1 >"$IB_EVIDENCE/problems-sample-table.txt" 2>"$IB_EVIDENCE/problems-sample-table.err"`. Exit code is 0. The first line is `count=20 shown=1`. The next line is `id	round	year	problem_id	verify	kind	source	has_answer`. Stdout contains `SAMPLE-Q01` and `uk_sample`. Stdout does not contain `answer_plain`.
- **Sample show.** Run `scripts/control-integration-bee problems show --id SAMPLE-Q17 --format json >"$IB_EVIDENCE/problems-sample-show.json"`. Exit code is 0. Stdout contains `"verify": "sympy"`, `E*x`, and `x^(1/ln x)`.
- **Sample select.** Run `scripts/control-integration-bee problems select --id SAMPLE-Q05 --format json >"$IB_EVIDENCE/problems-sample-select.json"`. Exit code is 0. Stdout contains `manual` and `integrand_plain`. Stdout does not contain `answer_plain`.
- **Confirm no write.** Run `find "$IB_DATA_DIR" -type f >"$IB_EVIDENCE/problems-files.txt"`. That file is empty.

## Gotchas

- `problems list` and `problems select` omit `answer_plain` and `worked_solution_plain`. `problems show` prints both when the extract stored them.
- Text format for `problems list` is the count line and a tab-separated table. The columns are `id`, `round`, `year`, `problem_id`, `verify`, `kind`, `source`, and `has_answer`. `problems show` and `problems select` print JSON when the format is text.
- A select with no filter, or with a filter that matches many ids, exits 2. An unknown id on show or select exits 1.
- These commands do not write learner state. A mark still goes through `turn apply`.
- A pack row with `verify` `sympy` was proved from the committed PDF. `problems list` still omits `answer_sympy`. `problems show` prints it. A `manual` row is a cited answer that has not been proved. Do not treat its `answer_plain` as a SymPy expression.
- Yang practice with `verify` `unchecked` has no printed answer. Do not fill one in.
