# Doctor

Doctor reports whether this checkout can teach. It does not write tracker files.

## Sub-features

- `doctor-ready` prints READY and exits 0 when the Yang PDF, units, and SymPy are present.
- `doctor-official-optional` still exits 0 when contest PDFs have not been fetched.

## How to get to it (user POV)

- The companion asks the CLI whether the pack is usable before teaching.

## Driving it with control-integration-bee

Preconditions:

- `IB_DATA_DIR` is an empty directory created for this run.
- SymPy imports.

- **Ask doctor.** Run `scripts/control-integration-bee doctor | tee "$IB_EVIDENCE/doctor.txt"`. Exit code is 0. Stdout contains `READY integration-bee` and `yang_pdf=ok`.
- **Confirm no write.** Run `find "$IB_DATA_DIR" -type f | tee "$IB_EVIDENCE/doctor-files.txt"`. The file is empty.

## Gotchas

- A missing Yang PDF is a failure. Missing official contest PDFs are not.
- Doctor reads `IB_DATA_DIR` only as a label. It must not create files there.
