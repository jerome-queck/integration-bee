# Learner session TLA+

Catalog checks stay in `verify/model.py`. They answer whether a finite record has the right shape.

Session order and torn tracker writes are a different question. Two commands can interleave, and one command writes several files. TLC checks those orders on a small model in `verify/formal/`.

The actions are TLA+. PlusCal is not used. A PlusCal translation would collapse the writes into one algorithm step, and the statechart names each TLA+ action.

The pass configs describe the code. A config that deletes a guard must fail. Four properties fail on the current writer. Those failures stay in the suite. This change does not edit the CLI.

Receipt: `integration-bee-vicious-run-2026-10-25`.
