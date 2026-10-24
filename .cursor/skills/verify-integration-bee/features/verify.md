# Verify

`verify` runs `verify/run.sh`. The run checks the pack and rejects one corrupted drill answer. It does not write learner state.

## Sub-features

- `verify-pass` exits 0 when unit files, SymPy answers, the past-paper indexes, and the committed reference PDFs match.
- `verify-mutation` prints a math failure for the corrupted answer, then records that the failure happened.

## How to get to it (user POV)

- The verifier runs this before a pull request. The learner does not run it. The companion teaching flow does not call it.

## Driving it with control-integration-bee

Preconditions:

- Doctor has printed `READY integration-bee`.
- The reference PDFs are in the tree.

- **Run verify.** Run `scripts/control-integration-bee verify >"$IB_EVIDENCE/verify.out" 2>"$IB_EVIDENCE/verify.err"`. The exit code is 0. Stdout contains `PASS mutation (wrong answer rejected)` and `PASS integration-bee verify (multi-unit gates)`. Stderr contains `# 17 drills (tags=`.
- **Confirm no learner write.** Run `find "$IB_DATA_DIR" -type f >"$IB_EVIDENCE/verify-files.txt"`. That file is empty. `verify` does not read `IB_DATA_DIR`.

## Gotchas

- The mutation probe prints `FAIL math:` and then `PASS mutation (wrong answer rejected)`. The command still exits 0. A real math failure prints `FAIL math:` and is not followed by `PASS mutation`. The exit code is then 1.
- A normal run does not print `WARN` lines or `SKIP round PDFs absent`. `verify/all_rounds_check.py` fails when the reference PDFs are absent from `sources/past/`.
- `make check` also runs LaTeX, `scripts/check_agents_md.py`, and the invariant mutations. `verify` runs only `verify/run.sh`.
