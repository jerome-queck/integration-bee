# Mutation cases (must fail)

1. **Wrong integral answer** — `check_math.py --mutate-wrong` corrupts the first loaded drill answer; process must exit non-zero.
2. **Past-papers-before-drills** — if `units/*/meta.yaml` has `past_paper: true` with no concept unit, `unit_order_check.py` fails. Concept units are `past_paper: false` with Yang tags.
3. **Missing drills JSON** — each `units/NN-*/` requires `verify/drills_unitN.json`.
