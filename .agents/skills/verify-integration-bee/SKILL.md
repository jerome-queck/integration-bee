---
name: verify-integration-bee
description: Drive the Integration Bee CLI the way the companion does, and save a transcript. Use before claiming a change to doctor, practice, drills, problems, progress, turn, or verify.
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

Follow `features/README.md` in this skill directory. Drive one feature file end to end. Every path from `scripts/control-integration-bee --commands-json` is named in that index. Do not mark a skipped entry point as verified through a different command.

`verify/run.sh` runs `verify/turn_contract_check.py`. That script is the CI proof of the turn contract. A feature drive still has to save its own transcript under `$IB_EVIDENCE`.

## Evidence

A transcript counts only when `$IB_EVIDENCE/binding.txt` matches a fresh hash of the source text and of the inputs.

`FEATURE` is the feature stem: `doctor`, `drills`, `practice`, `problems`, `progress`, `turn`, or `verify`. `IB_CMD` is the exact command string. `IB_INPUTS` is the input files that feature names. From the repository root, before the drive:

```bash
{
  sha256sum .agents/skills/verify-integration-bee/SKILL.md
  sha256sum ".agents/skills/verify-integration-bee/features/${FEATURE}.md"
  printf '%s\n' "$IB_CMD" | sha256sum
  sha256sum $IB_INPUTS
} | tee "$IB_EVIDENCE/binding.txt"
```

After the drive, run the same block and compare it with `$IB_EVIDENCE/binding.txt`. If the skill hash, the feature hash, the command hash, or an input hash differs, the transcript does not count. Do not reuse a transcript whose input hash differs.

Also save the command, stdout, stderr, and exit code under `$IB_EVIDENCE`. The proof is the action plus the stored state. For a recorded attempt, `progress show` must mention the drill id after `practice check`.

## Cleanup

```bash
rm -rf "$IB_DATA_DIR"
```

Do not delete `$IB_EVIDENCE`. Do not kill processes by name.

## Helpers

`scripts/control-integration-bee` is the only helper. `scripts/control-integration-bee --commands-json` lists commands.
