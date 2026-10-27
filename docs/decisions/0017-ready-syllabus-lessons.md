# Ready syllabus lessons can share units

The seven syllabus nodes `floor`, `dutis`, `vector-calc`, `beta`, `zeta`,
`euler-mascheroni`, and `catalan` have ready lessons in existing concept units.
No new unit, contest answer, or Round 1 gate is needed. Their cards and unit
lessons are inventoried in `pedagogy/concept-map.md`.

Readiness describes the teaching material. A learner tick describes evidence
from that learner. Assigning a ready node to a unit must not turn every drill
in that unit into evidence for the new node: Gamma drills do not assess Beta,
and Gaussian drills do not assess floor functions.

## Stored practice

An optional catalog field `drill_ids` declares the node's automatic practice
and mastery evidence. When it is absent, the existing unit/Yang-tag selection
continues unchanged. An explicit nonempty list selects those stored ids in
the declared order, including a bridge in another unit. Every id must exist
and appear only once in the list.

- `floor` is hosted by unit 11 and selects `U11-D09` through `U11-D12`.
- `dutis` is hosted by unit 34 and selects `U11-D13` through `U11-D15`,
  `U34-D04`, and `U34-D05`. The moving-endpoint exercise is taught alongside
  that evidence; method-refusal drills are comparisons rather than direct
  DUTIS evidence.

The unit 11 `special-wildcard` selection and all 300 stored drills remain
unchanged. Two distinct correct eligible drills are still required for an
automatic solid tick. Merely reading a card awards no tick.

The catalog's optional `teaching` field names an authoritative gap note when
the unit delegates its detailed lesson to that note. Floor keeps
`docs/techniques/floor.md`, linked from unit 11, as the file a floor gap names.
Without this override, the gap index still requires the unit's `teaching.tex`.
The six gap ids and their checked examples are unchanged.

## Optional recognition

An explicit empty `drill_ids` list means a ready oral recognition lesson,
outside the automatic drill queue and its tick evidence. The five optional
nodes use this form. Their cards and unit notes include worked, faded, and
bare prompts, expected reasoning, and failure cases. The coach opens them
when requested. The automatic queue skips them rather than serving unrelated
host-unit drills or failing with `no drill`.

Supporting stored Gaussian, Gamma, series, and Catalan practice keeps its
existing node routes. Recognition of zeta does not authorize a new zeta
evaluation. Catalan's exact value remains G. None of these nodes is a Round 1
gate; the existing 20 required ids remain the readiness contract.

`verify/teaching_catalog_check.py` checks the inventory and exercises these
selection and mastery boundaries, including mutations. `verify/run.sh` runs
it as part of `make check`.
