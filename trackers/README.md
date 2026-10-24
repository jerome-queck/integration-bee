# Learner trackers

Committed files are examples. Live files under `trackers/live/` are gitignored. `turn apply` writes the session, attempts, the heatmap, mocks, the journal, streaks, skill ticks, marks, and stickies.

| Example | Live file | What it stores |
|---|---|---|
| `attempts.example.json` | `trackers/live/attempts.json` | Drill attempts and spaced-repetition fields |
| `heatmap.example.json` | `trackers/live/heatmap.json` | Fail counts by technique tag |
| `mocks.example.json` | `trackers/live/mocks.json` | Timed mock sessions |
| `journal.example.json` | `trackers/live/journal.json` | Technique notes |
| `streaks.example.json` | `trackers/live/streaks.json` | Study days |
| `skill-ticks.example.json` | `trackers/live/skill-ticks.json` | Skill-tree ticks |
| `session.example.json` | `trackers/live/session.json` | Teach, mark, and mock phase |
| `marks.example.json` | `trackers/live/marks.json` | `answer_ok` and `method_ok` on one row per id |
| `stickies.example.json` | `trackers/live/stickies.json` | One card per technique. Strength is computed from the touched day |

`catalog.json` lists every skill-tree node. Personal ticks are not stored in `skill-tree.md`.

Set `IB_DATA_DIR` to keep a second run off `trackers/live`.
