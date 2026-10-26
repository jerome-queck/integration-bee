# Pack source holds and ready-to-use audit

Audit date: 27 October 2026. Source snapshot: [`6ac8f7d1552e32b6007bed7e8206ab3c284ab10b`](https://github.com/jerome-queck/integration-bee/commit/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b), after Handoff H. Handoff K adds documentation and teaching pointers; it does not release these holds.

## Purpose

Twelve resource-pack catalog rows remain `verify: manual` because the printed problem, assumptions, or mark need clarification. They are source holds, not claims that a problem is impossible or has no closed form. Some notes prove the value of the printed integral; others exhibit two admissible answers. Neither is permission to invent agreement with the mark.

At the audited snapshot there is also one manual encoding task, `R2-2023-Group-Q01-v2`, owned by Handoff I. It is **not** a thirteenth source hold. Yang practice and sample problems have separate scopes below.

## Policy: t541u and manual grading

Preserve the distinction between a cited answer and a proved answer. Under t541u, never invent a final, silently repair the problem to fit the mark, or describe a held row as impossible. Read both original PDFs and the worked note. Quote an authoritative correction before proposing a release, and carry it into the follow-up PR body. An exact mathematical diagnosis of a source conflict does not itself authorize a `manual` → `sympy` flip.

The [companion skill](../../.agents/skills/integration-bee-companion/SKILL.md) and [turn contract](../../verify/turn_contract.py) distinguish these cases:

| Catalog status | Companion action | CLI behavior |
|---|---|---|
| `sympy` | Send the learner's `extract.final_answer`; omit `verdict`. | Compare against `answer_sympy`. An agent's verdict cannot override a wrong expression. |
| `manual` | After the learner answers, read `problems show`, the cited mark, and the relevant worked note/PDF; send `verdict: correct` or `verdict: incorrect`. Explain any source hold. | Record the supplied verdict and display the stored `answer_plain`; it does not prove or parse the lossy printed integrand. A missing verdict is rejected without writing an attempt. |
| `unchecked` | Explain that the source supplies no answer. | Do not invent a final or send a verdict. There are no such resource-pack rows at this snapshot. |

For a held manual, `answer_plain` is the **cited-mark grading reference**, not a theorem about the printed problem. For example, `R1-2022-Oxford-Q01` displays `sin(1)` even though its note derives $1$ for the printed endpoints. [The manual-mark fixture](../../verify/turn_contract_check.py) deliberately checks this behavior. MIT-TB and TB2022 have the same source conflict. Keep the displayed mark and the mathematical diagnosis explicit when coaching; do not silently substitute the note's derived value for the catalog's cited mark.

No authoritative erratum resolving these twelve holds is documented in the audited repository sources as of 27 October 2026. This is an audit of the committed evidence, not a claim that every external publication has been searched. Existing notes retain their separately dated external rechecks.

## Registry: twelve held catalog rows

The problem and mark links below use the immutable source snapshot. All linked PDF paths were checked with `git cat-file -e <snapshot>:<path>`; all twelve note paths exist. The notes preserve the detailed arguments and, for crossnumbers, the complete printed answer maps. Tournament aliases are catalog rows for the same underlying integral, not independent problems.

| Id | Conflict | Problem PDF path and location | Mark PDF path and location | Worked note | Suggested next research |
|---|---|---|---|---|---|
| `R1-2022-MIT-TB-Q01` | Printed limits \(-\pi/2,\pi/2\) give \(1\); mark says \(\sin(1)\). | [`sources/past/r1/2022/MIT_Tiebreaker_2022_Round_1_UK_University_Integration_Bee_(3).pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r1/2022/MIT_Tiebreaker_2022_Round_1_UK_University_Integration_Bee_%283%29.pdf) (p. 2, Q1) | [`sources/past/r1/2022/MIT_Tiebreaker_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(4).pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r1/2022/MIT_Tiebreaker_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_%284%29.pdf) (p. 2, Q1) | [R1-2022-MIT-TB-Q01.md](../../solutions/pack/R1-2022-MIT-TB-Q01.md) | Seek an organiser correction to the endpoints or mark; the 2020 answer alone does not amend the 2022 source. |
| `R1-2022-Oxford-Q01` | The same printed integral gives \(1\), while its mark and the manual fixture display \(\sin(1)\). | [`sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_(1).pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r1/2022/Oxford_2022_Round_1_UK_University_Integration_Bee_%281%29.pdf) (p. 2, Q1) | [`sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(5).pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r1/2022/Oxford_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_%285%29.pdf) (p. 2, Q1) | [R1-2022-Oxford-Q01.md](../../solutions/pack/R1-2022-Oxford-Q01.md) | Resolve the 2022 source discrepancy before changing the load-bearing manual fixture. |
| `R1-2022-TB2022-Q01` | The third copy has the same \(1\) versus \(\sin(1)\) conflict. | [`sources/past/r1/2022/Tiebreaker_2022_Round_1_UK_University_Integration_Bee_(7).pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r1/2022/Tiebreaker_2022_Round_1_UK_University_Integration_Bee_%287%29.pdf) (p. 2, Q1) | [`sources/past/r1/2022/Tiebreaker_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_(6).pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r1/2022/Tiebreaker_Mark_Scheme_2022_Round_1_UK_University_Integration_Bee_%286%29.pdf) (p. 2, Q1) | [R1-2022-TB2022-Q01.md](../../solutions/pack/R1-2022-TB2022-Q01.md) | Check any correction against this tiebreaker copy as well as MIT and Oxford. |
| `R2-2023-Relay-Q19` | The printed upper bound \(n\) gives an unbounded even subsequence; the mark is \(\sqrt{\pi/2}\). | [`sources/past/r2/2023/Relay_2023_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Relay_2023_R2_UK_University_Integration_Bee.pdf) (p. 2, Q19) | [`sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf) (p. 4, Q19) | [R2-2023-Relay-Q19.md](../../solutions/pack/R2-2023-Relay-Q19.md) | Obtain an authoritative corrected bound or final; do not silently substitute a Gaussian-friendly interval. |
| `R2-2021-Relay-D03` | Two allowed \((r,s,t,u)\) representations give pass-ons \(\varphi\) and \(1\); the mark selects \(\varphi\). | [`sources/past/r2/2021/Shuttle_2021_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Shuttle_2021_R2_UK_University_Integration_Bee.pdf) (p. 5, D3) | [`sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf) (p. 4, D3) | [R2-2021-Relay-D03.md](../../solutions/pack/R2-2021-Relay-D03.md) | Ask for the missing normalization of the logarithmic representation; coprimality alone is insufficient. |
| `R2-2023-Relay-Q20` | Both \(f=0\) and \(f=\tfrac14\log(1+x^2)\) satisfy the equation; the latter yields the marked \((\pi+\log4-4)/4\). | [`sources/past/r2/2023/Relay_2023_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Relay_2023_R2_UK_University_Integration_Bee.pdf) (p. 3, Q20) | [`sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf) (p. 4, Q20) | [R2-2023-Relay-Q20.md](../../solutions/pack/R2-2023-Relay-Q20.md) | Obtain a branch-selecting hypothesis from the setter; do not cancel an unknown function that may vanish. |
| `R3-2024-Tournament-Q04-v10` | The integral gives \(\pi/2^m\); the answer slide and worked PDF print \(\pi/2^{m-2n}\). | [`sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf) (slide 169, Battle 4 / Fight 2 / Q4) | [`sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf) (slide 171) | [R3-2024-Tournament-Q04-v10.md](../../solutions/pack/R3-2024-Tournament-Q04-v10.md) | Seek a correction to the substitution factor or printed final, with both slide and worked PDF identified. |
| `R3-2024-Tournament-Q04-v11` | Answer-slide alias of v10; its printed \(\pi/2^{m-2n}\) inherits the same conflict. | [`sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf) (slide 169; alias text on slide 171) | [`sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf) (slide 171) | [R3-2024-Tournament-Q04-v11.md](../../solutions/pack/R3-2024-Tournament-Q04-v11.md) | Apply any authoritative v10 correction consistently to the answer-slide alias; OCR cleanup alone does not release the hold. |
| `R3-2024-Tournament-Q04-v12` | Mark-text alias of v10; its printed \(\pi/2^{m-2n}\) inherits the same conflict. | [`sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf) (slide 169; alias text on slide 171) | [`sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf) (slide 171) | [R3-2024-Tournament-Q04-v12.md](../../solutions/pack/R3-2024-Tournament-Q04-v12.md) | Apply any authoritative v10 correction consistently to the mark-text alias. |
| `R2-2021-Crossnumber-Across-1` | A8 asks for first publication: the grid gives 1868, while the note cites a primary 1867 standalone edition. | [`sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf) (pp. 2–3, A8) | [`sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf) (p. 3, completed grid) | [R2-2021-Crossnumber-Across-1.md](../../solutions/pack/R2-2021-Crossnumber-Across-1.md) | Ask whether the clue meant the 1868 journal volume; retain both primary bibliographical records in the note. |
| `R2-2021-Crossnumber-Down-1` | D3 needs different modulus grouping to obtain 28 rather than 36; D4 also confuses equality of a digit sum with congruence. | [`sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Crossnumber_2021_R2_UK_University_Integration_Bee_Round_Two.pdf) (p. 3, D3–D4) | [`sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2021/Mark_Scheme_2021_R2_UK_University_Integration_Bee.pdf) (p. 3, completed grid) | [R2-2021-Crossnumber-Down-1.md](../../solutions/pack/R2-2021-Crossnumber-Down-1.md) | Resolve both D3 parentheses and D4 equality-versus-congruence; fixing D3 alone does not certify the full map. |
| `R2-2023-Crossnumber-Down-1` | D7 marks \(f(0)=250\), but changing only \(f(0)\) preserves the integral limit without continuity. | [`sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Crossnumber_2023_R2_UK_University_Integration_Bee.pdf) (p. 3, D7) | [`sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r2/2023/Mark_Scheme_2023_R2_UK_University_Integration_Bee.pdf) (p. 3, completed grid) | [R2-2023-Crossnumber-Down-1.md](../../solutions/pack/R2-2023-Crossnumber-Down-1.md) | Find an explicit continuity assumption or setter clarification; grid crossings do not supply the missing analytic hypothesis. |

### Reading cautions retained by this audit

All twelve `answer_plain` fields retain the cited marks, including the complete crossnumber maps. The Relay Q19 field explicitly flags the print conflict. Relay Q20 and Tournament v10/v12 retain multiline OCR rather than a clean mathematical display; their notes and PDF layouts disambiguate the fraction/exponent. K does not replace those fields with derived values.

The Tournament rows' `worked_solution_plain` at this snapshot is an unrelated Chainlink floor-integral extract, despite `worked_solution_origin: pdf_copy`. Do not treat that extract or `has_worked` alone as authority for the Tournament problem. The correct worked source is [`sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf`](https://github.com/jerome-queck/integration-bee/blob/6ac8f7d1552e32b6007bed7e8206ab3c284ab10b/sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_%282%29.pdf), p. 15, §4.2, problem 1, as cited in each note. Consult that PDF and the note after the learner answers. Extraction cleanup belongs to Handoff J; it does not resolve the exponent conflict.

### Escalation / unlock template

Use this in a follow-up when new source authority changes a hold; no unlock is asserted in K.

```markdown
### Escalation / unlock: <id>
- What changed: <authoritative erratum URL and exact correction>
- PDF problem / mark: <immutable blob URLs and pages>
- Proposed follow-up encode prompt:
  1. Preserve the quoted correction and identify every affected alias.
  2. Read the corrected problem and cited final independently.
  3. Encode the stated domains, endpoints, and branch assumptions.
  4. Add an exact SymPy-checkable certificate tied to the corrected reading.
  5. Verify the catalog answer against the cited final, then update counts.
  6. Run doctor, make check, and review; open a separate PR.
- Do not mark impossible.
```

## EXPECTED story and scope

[`verify/problem_catalog.py`](../../verify/problem_catalog.py) calls all **non-sample** rows `pack_rows`. Its `EXPECTED_COUNT = 946` includes 674 resource-pack rows plus 272 Yang rows. Therefore `EXPECTED_MANUAL` is not the number of manual contest rows alone.

| State | Resource-pack `sympy` | Resource-pack `manual` | Answered Yang `manual` | `EXPECTED_SYMPY` | `EXPECTED_MANUAL` |
|---|---:|---:|---:|---:|---:|
| Audited `6ac8f7d`; unchanged by K | 661 | 13: twelve holds + Q01-v2 | 2 | 661 | 15 |
| After I, **if only** Q01-v2 flips | 662 | 12: these holds | 2 | 662 | 14 |

The two answered Yang rows are `YANG-1.3-Ex01` and `YANG-1.3-Ex03`. The other 270 Yang rows remain unchecked. No Yang finals are created here. The separate sample catalog has 20 rows: 16 `sympy` and 4 `manual`; these are excluded from the EXPECTED pair above. The complete JSONL has 966 rows.

All 674 resource-pack rows have a nonempty `answer_plain` and `answer_source_pdf`; zero are unchecked. Catalog answers being present makes them available for grading, not all mathematically proved. Do not change EXPECTED pre-emptively. Recount after rebasing onto I/J; additional encodes, if any, must be reflected in the actual catalog rather than guessed from this conditional table.

## Worked-note coverage: retire the “19 skips” count

At `6ac8f7d`, the tracked `solutions/pack/<id>.md` coverage is **673/674**. The sole absent note is `R2-2023-Group-Q01-v2.md`, assigned to I. All twelve source holds have notes, and all 661 currently SymPy-gated resource-pack rows have notes. Source-hold status is not missing-note status.

The K handoff reports that 18 of the former 19 “honest note skips” already gained notes. The historical `SOLUTIONS_SKIPPED_HONEST.json` was outside the repository and is unavailable in this checkout, so this decision does not reconstruct or invent its nineteen ids. The measured current snapshot is:

| Resource-pack class | Rows | Tracked notes | Missing notes |
|---|---:|---:|---|
| `sympy` | 661 | 661 | None |
| Source holds in this registry | 12 | 12 | None |
| I's remaining manual encode | 1 | 0 | `R2-2023-Group-Q01-v2` |
| Total | 674 | 673 | One |

The accurate statement is “notes complete except for I's twin note,” not “19 notes missing.” After I adds the twin note, coverage should be 674/674; measure that state before reporting it as complete. A note's existence alone does not imply a SymPy proof or remove a source hold.

## Ready-to-use checklist

The learner talks to the [companion](../../.agents/skills/integration-bee-companion/SKILL.md); the companion operates the CLI. Readiness of the checkout means the following checks, not resolution of every source dispute:

- Run `scripts/control-integration-bee doctor` and require `READY integration-bee`.
- Run `make check` on the PR head. It includes catalog and certificate checks, manual/symbolic turn fixtures, readiness invariants, TeX compilation, and formal checks. Record the actual result and any omitted gate in the PR's `## Pre-review self-check`.
- Confirm every resource-pack row has a cited grading answer and none is unchecked. Use automatic grading for `sympy`, an explicit companion verdict for `manual`, and open this registry for a hold.
- Confirm all twelve notes retain their `## Status: source hold (print-vs-math)` block and the problem/mark distinction.
- Confirm the five formerly `deferred-open` syllabus nodes have the notes linked by the [concept map](../../pedagogy/concept-map.md). They stay unticked and are not Round 1 requirements.
- Preserve `floor` and `dutis` as deferred-taught and unticked. Units 01–36 and their 300 drills are already the established teaching path.

The PR body carries the run-specific READY line and check summary. The owner re-runs pstack and `make check` before deciding whether to merge. K opens one PR; it does not merge or mix in I's encodes or J's bulk OCR changes.
