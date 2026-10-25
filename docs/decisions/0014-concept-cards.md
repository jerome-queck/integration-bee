# Concept cards are not gap ids

The gap index in `docs/techniques/beyond-yang.md` has exactly six headings. `verify/gap_index.py` rejects a seventh heading, and it rejects an extra file placed directly in `docs/techniques/`.

Round 1 technique families need coach cards anyway. The cards live in `docs/techniques/concepts/`, which the index does not scan. `pedagogy/concept-map.md` is the node inventory. `pedagogy/round1-coach.md` is how a tick chooses a card.

A card is not an `extract.gap` value. A mark still uses one of the six headings. A card does not tick `floor` or `dutis`, and it does not store a contest answer.
