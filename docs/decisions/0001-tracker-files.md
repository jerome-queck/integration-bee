# Tracker files

Learner state is one directory of JSON files. The CLI is the only writer. Examples live in `trackers/*.example.json`. Live files live in `trackers/live/` and are gitignored.

Round 1 mock readiness is a predicate over skill ticks, not a second copy of the skill tree. `skill-tree.md` stays a curriculum map. `trackers/catalog.json` is the id list the CLI accepts.

A second run sets `IB_DATA_DIR` instead of sharing `trackers/live`.
