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

## Proof and skip reporting

- Capture the command and the resulting state.
- A save status is not enough. Read the value back with `progress show`.
- Record the feature id with the artifact.
- If a precondition is missing, report the command and the gap. Do not swap in another path and call it verified.

## Features

- [Doctor](./doctor.md) checks the checkout without writing learner state.
- [Practice](./practice.md) serves a drill and records a SymPy check.
- [Drills](./drills.md) lists ids and display answers.
- [Progress](./progress.md) stores a tick and shows it back.
