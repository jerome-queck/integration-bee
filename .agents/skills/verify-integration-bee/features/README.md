# Integration Bee verification map

Read this index, then follow one feature file. The operator is the companion agent. The learner does not run these commands.

## Baseline preconditions

- Repository root is the working directory.
- SymPy imports.
- `IB_DATA_DIR=/tmp/ib-verify-$RUN_ID` and that directory is empty.
- `scripts/control-integration-bee doctor` prints `READY integration-bee`.
- Do not use `trackers/live` for a verification run.

## Driving conventions

- Start from the baseline unless the feature says otherwise.
- Treat each command as literal.
- `--format json` is the stable output for a recorded result.
- `practice list`, `drills list`, and `problems list` print a text table when the format is text. The first line is `count=<n>`. A `--limit` that cuts the rows adds `shown=<k>`. The next line is a tab-separated header. `problems show` and `problems select` stay JSON either way.
- Redirect stdout and stderr into `$IB_EVIDENCE`. Record the CLI exit code from that process. A pipe into `tee` reports `tee`'s status.
- Bind that transcript to source text and inputs. Write `$IB_EVIDENCE/binding.txt` with the sha256 of `.agents/skills/verify-integration-bee/SKILL.md`, of this file, of the feature file, of the command string, and of each input file that feature names. Recompute the hashes after the drive. A transcript whose hashes differ does not count.

## Proof and skip reporting

- Capture the command and the resulting state.
- A save status is not enough. Read the value back with `progress show`, or read the JSON file the command writes when `progress show` does not echo it.
- Record the feature id with the artifact.
- If a precondition is missing, report the command and the gap. Do not swap in another path and call it verified.

## Features

Each command from `scripts/control-integration-bee --commands-json` belongs to one file.

- [Doctor](./doctor.md) is `doctor`.
- [Practice](./practice.md) is `practice list`, `practice next`, and `practice check`.
- [Drills](./drills.md) is `drills list`.
- [Problems](./problems.md) is `problems list`, `problems show`, and `problems select`.
- [Progress](./progress.md) is `progress show`, `progress tick`, `progress mistake`, `progress mock-start`, `progress mock-finish`, `progress journal`, and `progress streak`.
- [Turn](./turn.md) is `turn schema`, `turn show`, and `turn apply`.
- [Verify](./verify.md) is `verify`.
