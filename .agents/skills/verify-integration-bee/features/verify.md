# Verify

`verify` runs `verify/run.sh`. The run checks the pack and rejects one corrupted drill answer. It does not write learner state.

Record the sha256 of `.agents/skills/verify-integration-bee/features/verify.md`, of the verify command string, and of the inputs `verify/run.sh` and `verify/e_false_pass_check.py` in `$IB_EVIDENCE/binding.txt`. Recompute those hashes from the bytes just read. If one differs, the transcript does not count.

## Sub-features

- `verify-pass` exits 0 when the source files, the 36 unit shapes, Yang 1.1–1.20 in the syllabus map, unit order, the 300 drill answers, the past-paper indexes, the sample answers and worked notes, the Yang practice-seed smoke, the round PDFs, the problem catalog, the Yang worked-step checks, the never-impossible lint, the finding E false-pass regressions, the gap index, the CLI behavior checks, and the turn contract all pass.
- `verify-mutation` prints a math failure for the corrupted answer, then records that the failure happened.

## How to get to it (user POV)

- The verifier runs this before a pull request. The learner does not run it. The companion teaching flow does not call it.

## Driving it with control-integration-bee

Preconditions:

- Doctor has printed `READY integration-bee`.
- The reference PDFs are in the tree.

- **Run verify.** Run `scripts/control-integration-bee verify >"$IB_EVIDENCE/verify.out" 2>"$IB_EVIDENCE/verify.err"`. The exit code is 0. Stdout contains `PASS check_math (300 drills + spotchecks)`, `PASS sample_self_check (20 sample rows)`, `PASS mutation (wrong answer rejected)`, `PASS catalog`, three lines of the form `PASS <count> yang worked solutions` (one per worked-solution lane; `<count>` is however many rows that lane checks), `PASS never-impossible`, `PASS mutation notes-impossible`, `PASS mutation pack-note`, `PASS gap index`, `PASS mutation extra-file`, `PASS cli behavior`, `PASS turn contract`, and `PASS integration-bee verify (multi-unit gates)`. Stderr contains `# 17 drills (tags=`.
- **Confirm no learner write.** Run `find "$IB_DATA_DIR" -type f >"$IB_EVIDENCE/verify-files.txt"`. That file is empty. `verify` does not read `IB_DATA_DIR`.

## Gotchas

- The mutation probe prints `FAIL math:` and then `PASS mutation (wrong answer rejected)`. The command still exits 0. A real math failure also prints `FAIL math:`. `verify/run.sh` continues, and the mutation probe still prints `PASS mutation (wrong answer rejected)` when that probe exits non-zero. The command then prints `FAIL integration-bee verify` and exits 1.
- A broken gap index prints `FAIL gap index` from that step. `verify/run.sh` continues. The command prints `FAIL integration-bee verify` and exits 1. `verify/gap_index.py --expect-fail extra-file` on a healthy index injects a fake path and prints `PASS mutation extra-file`. It does not create a file. A healthy `verify` run still reaches `PASS integration-bee verify`.
- `verify/never_impossible_check.py --expect-fail notes-impossible` plants a forbidden label in memory and prints `PASS mutation notes-impossible`. It does not edit `problems/records.jsonl` or a worked note. A clean tree prints `PASS never-impossible`. A real label prints `FAIL never-impossible` and the command then prints `FAIL integration-bee verify` and exits 1.
- A normal run does not print `WARN` lines or `SKIP round PDFs absent`. `verify/all_rounds_check.py` fails when the reference PDFs are absent from `sources/past/`.
- The `# 17 drills (tags=` line is the practice-seed smoke for `yang:1.1`, `yang:1.5`, `yang:1.18`, and `yang:1.19`. It goes to stderr. The 300-drill line is every row in `verify/drills_unit*.json`. Unit 11 adds floor `U11-D09` through `U11-D12` and DUTIS `U11-D13` through `U11-D15`, all tagged `yang:1.20`. Those rows stay out of the 17-drill smoke.
- `make check` also runs LaTeX, `scripts/check_agents_md.py`, and the invariant mutations. `verify` runs only `verify/run.sh`.
