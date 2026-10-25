# CLI reading view

`scripts/control-integration-bee` is the companion's writer. `--format json` stays the stable record for every command that returns a result.

`problems list`, `practice list`, and `drills list` print a table when the format is text. The table hides answers on `problems list` and `practice list`. `drills list` still shows `answer_display`. A missing `--format` used to dump the same JSON as `--format json`, including a 949-row catalog.

`practice check` calls the mark grader. An indefinite answer that differs by a constant, including `+C`, matches. A definite answer that adds a constant does not.

`practice next` serves a due drill first. Otherwise it serves the next drill in the coach queue that is not already correct. When every Round 1 node is done and nothing is due, it returns no drill.

An empty turn during `mock_open` continues that mock. A second `mock-start` keeps the open pack. `mock-finish` does not close a session that is waiting on an integral or a skip offer.

`doctor` still reports `IB_DATA_DIR` and ignores `--data-dir`.
