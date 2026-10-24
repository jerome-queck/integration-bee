# Mutation cases (must fail)

1. **Wrong integral answer** — `check_math.py --mutate-wrong` corrupts the first loaded drill answer; process must exit non-zero.
2. **Past-papers-before-drills** — if `units/*/meta.yaml` has `past_paper: true` with no concept unit, `unit_order_check.py` fails. Concept units are `past_paper: false` with Yang tags.
3. **Missing drills JSON** — each `units/NN-*/` requires `verify/drills_unitN.json`.
4. **Early solid tick.** `SessionFlow.tick-early.cfg` must make TLC violate `TwoCorrectBeforeSolid`.
5. **Ungated mock.** `SessionFlow.mock-ungated.cfg` must violate `MockGate`. `TrackerWrites.drop-gate.cfg` must do the same for the file model.
6. **Photo miss drops the weak tag.** `SessionFlow.forget-weak.cfg` must violate `MistakeQueuesWeak`.
7. **Score with no open mock.** `SessionFlow.score-without-open.cfg` must violate `ScoreAfterOpen`.
8. **Second open mock.** `TrackerWrites.second-open.cfg` must violate `AtMostOneOpen`.
9. **Shared data directory.** `TrackerWrites.lost-attempt.cfg`, `torn-heat.cfg`, `stale-progress.cfg`, and `lost-mock.cfg` must violate the matching invariant. `verify/formal/repro_tracker.py` shows the same breaks on the CLI writer.
