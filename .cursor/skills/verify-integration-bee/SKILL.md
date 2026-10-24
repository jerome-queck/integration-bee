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
scripts/control-integration-bee doctor | tee "$IB_EVIDENCE/doctor.txt"
```

Require exit 0, `READY integration-bee`, and `yang_pdf=ok`. Official contest PDFs may be missing. That is a warning, not a failure.

## Drive

Follow `.cursor/skills/verify-integration-bee/features/README.md`. Drive one feature file end to end. Do not mark a skipped entry point as verified through a different command.

## Evidence

Save the command, stdout, stderr, and exit code under `$IB_EVIDENCE`. The proof is the action plus the stored state. For a recorded attempt, `progress show` must mention the drill id after `practice check`.

## Cleanup

```bash
rm -rf "$IB_DATA_DIR"
```

Do not delete `$IB_EVIDENCE`. Do not kill processes by name.

## Helpers

`scripts/control-integration-bee` is the only helper. `scripts/control-integration-bee --commands-json` lists commands.
