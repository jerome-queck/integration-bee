# Doctor

Doctor reports whether this checkout can run. It does not write tracker files.

## Sub-features

- `doctor-ready` prints `READY integration-bee` and exits 0 when the Yang PDF, the 36 numbered unit directories, a drill file for each of those directories, the 300-drill feed, and SymPy are present.
- `doctor-official-optional` still exits 0 when a reference PDF is missing. The line is then `official_pdfs=missing`.

## How to get to it (user POV)

- The verifier asks whether the checkout can run before a drive.
- The companion teaching flow sends `turn apply`. It does not call `doctor`. The person running the agent runs `doctor` once during setup, before study.

## Driving it with control-integration-bee

Preconditions:

- `IB_DATA_DIR` is an empty directory created for this run.
- SymPy imports.
- The reference PDFs named by `sources/sha256sums` and `past/inventory.json` are non-empty files in the tree.

- **Ask doctor.** Run `scripts/control-integration-bee doctor >"$IB_EVIDENCE/doctor.txt" 2>"$IB_EVIDENCE/doctor.err"`. The exit code is 0. `doctor.txt` contains `READY integration-bee`, `yang_pdf=ok`, `official_pdfs=ok`, `units=36`, and `drills=300`. `doctor.err` is empty.
- **Confirm no write.** Run `find "$IB_DATA_DIR" -type f >"$IB_EVIDENCE/doctor-files.txt"`. That file is empty.

## Gotchas

- A missing Yang PDF, or a numbered unit with no `verify/drills_unitN.json`, prints `NOT_READY integration-bee` and exits 1.
- `official_pdfs` is `ok` only when every `.pdf` name in `sources/sha256sums` is a non-empty file under `sources/` and every `past/inventory.json` artifact with `present` not false is a non-empty file. Doctor does not look at `Resource_pack.zip`. A missing reference PDF leaves the exit code at 0 and prints `official_pdfs=missing`.
- `units` counts every `units/[0-9][0-9]-*` directory. Chapters 3 to 6 are units 19 to 36 on that list. The line is `units=36`.
- `drills` is the combined length of `verify/drills_unit*.json`. The line is `drills=300`. That feed includes unit 11 floor drills `U11-D09` through `U11-D12` and DUTIS drills `U11-D13` through `U11-D15`.
- Doctor reads `IB_DATA_DIR` only as a label. `doctor --data-dir` does not change that label. With the variable unset, the printed label is the absolute path of `trackers/live`. Doctor still creates no files.
- `--format json` prints the same fields and omits the `READY integration-bee` line.
- If SymPy cannot be imported, the math checker import prints `FAIL: sympy missing. Use /workspace/integration-bee/.venv` and the process exits 2 before doctor prints a report.
