# Public framework rule (Jerome, 24 Oct 2026)

## On GitHub (committed)
- Entire framework + architecture, usable by anyone who clones.
- Scaffolded folders for session / progress / skill-tree ticks (empty or example fixtures only).
- Skill-tree-adjacent map of every Integration Bee concept (Yang + Round 1); tickable as a learner progresses.
- Pedagogy units, LaTeX templates, verify harness, CLI, companion skill — shared product surface.
- More learner-framework patterns welcome (design freedom).

## Never commit
- Personal progress, session state, ticks, companion history, local DB.
- Anything that makes the repo look like Jerome’s half-used workspace.

## Bar
A fresh clone must look ready for a new learner, not mid-run for one person.

## More trackers (invent)
Beyond skill-tree ticks, design local-only trackers for other learner data, e.g.:
- drill attempt history / spaced-repetition queues
- weak-topic heatmaps from verify failures
- timed mock Round-1 sessions (score, pace, problem IDs)
- technique sticky-notes learned (companion journal)
- streak / study-session logs
Scaffold folders + schemas in git; real data gitignored.

## Verifiability (poteto)
Every committed behaviour: feature map entry, verify/run.sh (or skill) proves it, mutations fail on wrong math/answers. Formal verifier where costly. No "trust me" pedagogy.

## Human UX (simple)
Human never touches the repo. Only talks to the LLM (Integration Bee bot / companion skill).
Two primary flows:
1. Learn a new concept (LLM teaches from unit packs / skill-tree).
2. Get an integral → solve on paper → send photo of solution → LLM checks, teaches gaps, records mistakes into local trackers.
All trackers, verify, skill-tree, CLI are agent/behind-the-scenes. Keep the clone simple; no human "run these 12 commands" ritual.
