# Techniques the Yang guide does not teach alone

Yang Topics Guide is one source. The UK University Integration Bee techniques guide and the resource-pack papers use moves and formats that the unit notes either meet late or do not name. This note is the list spotted while extracting those papers. It is not a worked syllabus.

## Moves the contest uses earlier than the Yang order

Recurrence relations for a family, including Wallis-style reductions, sit in the official techniques guide at section 1.3. `units/20-wallis` is the in-repo Wallis note, and it is a later unit. Setting up `I_n` and reducing it is not an early Round 1 track in the Yang order.

Introducing a constant, or differentiating under the integral sign, is a basic move in the official guide at section 1.9. `units/34-frullani-feynman` is the later Feynman note. The early move is smaller than that chapter.

Floor-function integrals are section 1.7 of the official guide. Yang folds them into a wildcard section rather than an early drill track. No current unit is a floor-function chapter.

The contest treats the substitution `t = tan(x/2)` as an ordinary Round 1 tool. The official guide puts it at section 1.6. `units/26-weierstrass` is the in-repo note, and it is late for Round 1.

Reflection substitutions are a named toolkit in the official guide at section 1.2. King's rule overlaps that idea. `units/10-inverse-kings` and `units/25-advanced-kings` cover King's rule. The official guide treats reflection earlier and more broadly than those units.

## Formats Yang does not teach as formats

Round 2 papers include relay, crossnumber, and group rounds. Answers are often a digit or a filled grid, not a simplified antiderivative written out per clue.

Round 3 papers include chainlink, dichotomy, and tournament slides. Questions are parts of a game. A single integral's answer can depend on the previous part.

## What the catalog will not pretend

Pack and Yang integrands in `problems/records.jsonl` are the PDF text layer. `integrand_latex` is null. An answer with `verify` set to `manual` is a mark-scheme cite, or a short equality already printed in a Yang example. It is not a SymPy result. Yang practice rows with `verify` set to `unchecked` have no printed answer in the extract. Do not invent one.
