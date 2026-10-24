# Learner trackers

Committed files are examples. Live files are written by `scripts/control-integration-bee` under `trackers/live/` and are gitignored.

| Example | Live file | What it stores |
|---|---|---|
| `attempts.example.json` | `trackers/live/attempts.json` | Drill attempts and spaced-repetition fields |
| `heatmap.example.json` | `trackers/live/heatmap.json` | Fail counts by technique tag |
| `mocks.example.json` | `trackers/live/mocks.json` | Timed mock sessions |
| `journal.example.json` | `trackers/live/journal.json` | Technique notes |
| `streaks.example.json` | `trackers/live/streaks.json` | Study days |
| `skill-ticks.example.json` | `trackers/live/skill-ticks.json` | Skill-tree ticks |
| `session.example.json` | `trackers/live/session.json` | Teach, mark, and mock phase |

`catalog.json` lists every skill-tree node. Personal ticks are not stored in `skill-tree.md`.

Set `IB_DATA_DIR` to keep a second run off `trackers/live`.
