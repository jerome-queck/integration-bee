---
name: verify-integration-bee
description: Drive the Integration Bee CLI the way the companion does, and save a transcript. Use before claiming a change to doctor, practice, drills, progress, or verify.
---

# Verify Integration Bee

The scripted surface is `scripts/control-integration-bee`. A learner does not run it. You do.

## Launch

There is no server. From the repository root, with SymPy installed:

```bash
python3 -c 'import sympy'
```

Each drive uses its own data directory.

```bash
export RUN_ID=$(date +%s)
export IB_DATA_DIR=/tmp/ib-verify-$RUN_ID
export IB_EVIDENCE=/tmp/ib-verify-evidence-$RUN_ID
mkdir -p "$IB_DATA_DIR" "$IB_EVIDENCE"
```

Ready means `scripts/control-integration-bee doctor` prints `READY integration-bee` and exits 0.

## Doctor

```bash
scripts/control-integration-bee doctor >"$IB_EVIDENCE/doctor.txt" 2>"$IB_EVIDENCE/doctor.err"
echo "doctor_exit:$?"
```

Require `doctor_exit:0`, `READY integration-bee`, `yang_pdf=ok`, and an empty `doctor.err`. `official_pdfs` is `ok` when every `.pdf` name in `sources/sha256sums` and every present artifact in `past/inventory.json` is a non-empty file. A missing reference PDF does not change the exit code. Do not pipe doctor into `tee`. That pipe reports `tee`'s status.

## Drive

Follow `.cursor/skills/verify-integration-bee/features/README.md`. Drive one feature file end to end. Every path from `scripts/control-integration-bee --commands-json` is named in that index. Do not mark a skipped entry point as verified through a different command.

`verify/run.sh` runs `verify/turn_contract_check.py`. That script is the CI proof of the turn contract. A feature drive still has to save its own transcript under `$IB_EVIDENCE`.

## Evidence

Save the command, stdout, stderr, and exit code under `$IB_EVIDENCE`. The proof is the action plus the stored state. For a recorded attempt, `progress show` must mention the drill id after `practice check`.

## Cleanup

```bash
rm -rf "$IB_DATA_DIR"
```

Do not delete `$IB_EVIDENCE`. Do not kill processes by name.

## Helpers

`scripts/control-integration-bee` is the only helper. `scripts/control-integration-bee --commands-json` lists commands.
