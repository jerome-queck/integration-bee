# Round 1 coach

The companion reads ticks and chooses a page. This note does not change session machinery. A tick is `learning`, `solid`, or `skipped`, on a catalog node id. A missing tick means the node has not been placed.

## Choose the dose

1. Name the node from the integrand, using the shape table in `docs/techniques/concepts/README.md`.
2. Open that node's row in `pedagogy/concept-map.md`.
3. If a prerequisite on the coach card is missing or `learning`, teach that earlier card's worked example and set one of its drills. Stop the turn there.
4. If this node is missing or `learning`, teach the card's worked example, then the faded step, then one drill named on the card. The unit `teaching.tex` is the drill-tied lesson beside the card.
5. If this node is `solid`, skip the lecture. Set the next due drill in the same unit.
6. If this node is `skipped`, a non-cold mock still waits until the node is solid. A later miss on that node's drill returns the tick to `learning`. Teach the card at the difficulty in its table.

Past-paper integrals are not the lesson. The practice rows in the concept map are indexes.

## Difficulty

| Band | What the learner is doing |
|---|---|
| 1 | One standard antiderivative, or one substitution whose derivative is already visible. |
| 2 | A choice. Parts or substitution, a split, a reflection, a proper partial fraction. |
| 3 | A reduction, a half-angle substitution, a repeated factor, or a parameter on a fixed interval. |
| 4 | A named improper integral, a moving endpoint, or a series taken to an endpoint as a limit. |

Teach at the learner's highest solid band, plus one step. A band 4 card waits until the prerequisites on that card are solid, unless the learner brought that integrand.

## What may be quoted

Quote a stored drill id and the value printed in the unit note or the drill feed. Quote an original example in `docs/techniques/concepts/` that the card says was checked. Quote the six gap notes.

Leave a pack final alone. Leave a Yang practice final alone when the extract does not print it. Quote a zeta value only when unit 35 already prints it. `pedagogy/concept-map.md` records a thin count of 0. `floor` and `dutis` stay unticked. Leave \(G\) as \(G\).

## After a miss

The six headings in `docs/techniques/beyond-yang.md` are the only `extract.gap` values. `pedagogy/contest-gaps.md` is the script for those ids. A Round 1 miss with no gap id opens the coach card for the node's unit, then `units/<unit>/teaching.tex`.

Worked, faded, and bare follow `pedagogy/README.md`. A study session does not edit a teaching note.
