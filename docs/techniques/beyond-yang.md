# Techniques the Yang guide does not teach alone

The six headings below are the gap index. `verify/gap_index.py` is the only parser. A mark may set `extract.gap` to one of these ids. `say` names that row's file. The study session does not write the file.

Yang is one source among others. These notes are original exposition for moves the Topics Guide files late or omits: reflection, a recurrence \(I_n\), the half-angle substitution the Techniques Guide teaches as T-sub in section 1.6, floor integrals, introducing a constant and a small parameter derivative, and the Round 2 and Round 3 formats. The other sources are the syllabus, the Techniques Guide, and the SymPy-checked drills named in each note. A contest row is not a source of a new answer. Do not invent one.

## reflection
- note: units/10-inverse-kings/teaching.tex
- cite: Techniques Guide section 1.2
- catalog: kings-queens-rule
- contains: Worked reflection, U10-D07, a+b-x
- examples: 0

## recurrence
- note: units/20-wallis/teaching.tex
- cite: Techniques Guide section 1.3
- catalog: wallis
- contains: I_n, U20-D01, U20-D02, 1.3
- examples: 0

## weierstrass
- note: units/26-weierstrass/teaching.tex
- cite: Techniques Guide section 1.6
- catalog: weierstrass
- contains: U26-D01, U26-D02, 1.6, tan(x/2), rational
- examples: 0

## floor
- note: docs/techniques/floor.md
- cite: Techniques Guide section 1.7
- catalog: floor
- contains: 1.7, split at integers, U11-D09, U11-D10
- examples: 7

## introduce-constant
- note: docs/techniques/introduce-constant.md
- cite: Techniques Guide section 1.9
- catalog:
- contains: add and subtract, This move is not dutis, 34-frullani-feynman, smaller parameter, U11-D13
- examples: 6

## formats
- note: docs/techniques/formats.md
- cite: 2024 participant guides
- catalog:
- contains: group, crossnumber, relay, Shuttle, chainlink, dichotomy, tournament, Crossword, 2024_Participant_Guide_R2, Round_3_Integration_Bee_Participant_Guide
- examples: 0

Pack and Yang integrands in `problems/records.jsonl` start from the PDF text layer. A pack row with `verify` set to `sympy` also stores the proved `integrand_latex` and `answer_latex`. At tip `770c6e4` the resource pack is 674 SymPy / 0 manual / 0 unchecked. Lanes L1, L2, L3, L4, L5, L6, L7, and L8 set the live pair to `EXPECTED_SYMPY=940` / `EXPECTED_MANUAL=0`, counting the proved Yang rows through §1.3, §1.4–§1.5, §1.6–§1.8, §1.11, §2.3–§2.4, the §2.5 and §2.6 rows the gate accepted, the checked rows in sections 2.7, 3.4, 3.8, 4.4, 4.6, 6.1, and 6.7, and the Lane L5 rows in §§1.12, 1.15, 1.17, 1.18, and 1.20. SAMPLE is 20 SymPy / 0 manual. A `manual` flag marks a cited answer the gate has not proved. Pack manuals are 0 and sample manuals are 0. A Yang row with `verify` set to `unchecked` has no stored final. 6 of those rows remain. Do not store a final the gate did not prove.

On a miss, teach the one file `say` names. Read that note and work its displayed example. Do not edit the note in the study session. A later commit is what fills a missing move, with an original example or a stored drill id.

Round 1 families also have coach cards in `docs/techniques/concepts/`. Those cards are not gap ids. A mark still uses one of the six headings above. The map from a catalog node to a card is `pedagogy/concept-map.md`. Habit nodes are `docs/techniques/concepts/habits.md`.

A formats miss still teaches `docs/techniques/formats.md`. The session order around that note is `pedagogy/round2-coach.md` for group, crossnumber, and relay, and `pedagogy/round3-coach.md` for chainlink, dichotomy, and tournament.
