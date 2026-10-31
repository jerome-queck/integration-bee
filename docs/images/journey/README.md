# Learner journey chart

The README picture. It is a statechart made with the pstack `statechart` skill and rendered with Pele 1.9.0.

| File | What it is |
| --- | --- |
| `LearnerJourney.tla`, `LearnerJourney.cfg` | TLA+ model of the journey. TLC checks the rules `LessonsAfterPlacement` and `SkipsOnlyOnce`, and that nothing deadlocks. |
| `view.mjs` | Plain-word labels, phase groups, colours and the title. |
| `journey.mmd` | Mermaid source written by the skill (10 states, 14 arrows). |
| `journey.svg` | Pele render with the theme from `theme.css` and `defs.svg`. |
| `journey.png` | 1760×1886 PNG of the SVG, shown at 880 px wide in the README. |

The chart hides one step: staying at "Round 1 ready" once you finish.

Make it again from a scratch folder outside the repo:

```bash
statechart LearnerJourney.tla --config LearnerJourney.cfg --view view.mjs --out out
node render.mjs out/chart.mmd out/chart.svg theme.css defs.svg   # needs pele@1.9.0
```

Then take an 880×943 screenshot of the SVG at device scale 2 for the PNG.
