# Concept map

Catalog `trackers/catalog.json` has 72 nodes. The skill-tree tables list the same ids. `wallis` and `weierstrass` each appear twice on `skill-tree.md`, once in a chapter table and once in the syllabus table, so a raw row count reads higher than 72.

This page is the inventory of what an agent can teach from the repo. Coach cards live in `docs/techniques/concepts/`. They are not gap ids. The dose for a tick is `pedagogy/round1-coach.md`.

Depth means one of the following.

| Depth | What to teach |
|---|---|
| card | A coach card states when to use the move, one worked example, and the usual failure. The unit file holds the stored drills. |
| unit | The unit `teaching.tex` already states the move and a stored drill. The card only points there. No new example was added. |
| thin | Empty after the habit card. A node landed here when its unit had not yet taught the stored drills. Those eleven nodes are `habits.md`. |
| deferred-taught | The catalog id has no unit, so it stays deferred. A note and drills exist. Leave the id unticked. |
| deferred-open | No drill and no checked value. Name the syllabus entry. Do not invent a value. |
| index | A paper or a mock. Not a technique. |

## Round 1 nodes

These 20 nodes have `gate: round1`. Each one has a coach card.

| Node | Yang | Card | Unit lesson |
|---|---|---|---|
| `basic-integration` | 1.1 | `u-substitution.md` | `units/01-foundations-substitution/teaching.tex` |
| `basic-u-substitution` | 1.2 | `u-substitution.md` | the same file |
| `symmetry` | 1.3 | `symmetry-kings.md` | `units/02-symmetry-basic-trig/teaching.tex` |
| `basic-exponential` | 1.4 | `u-substitution.md` | `units/03-exponential-parts/teaching.tex` |
| `basic-trig-integrals` | 1.5 | `trigonometric.md` | `units/02-symmetry-basic-trig/teaching.tex` |
| `basic-integration-by-parts` | 1.6 | `integration-by-parts.md` | `units/03-exponential-parts/teaching.tex` |
| `basic-trig-substitution` | 1.7 | `trigonometric.md` | `units/04-trig-sub-circle/teaching.tex` |
| `basic-partial-fractions` | 1.8 | `partial-fractions.md` | `units/05-partial-fractions/teaching.tex` |
| `area-partial-circle` | 1.9 | `trigonometric.md` | `units/04-trig-sub-circle/teaching.tex` |
| `algebra-manipulation` | 1.10 | `algebra.md` | `units/01-foundations-substitution/teaching.tex` (light in the unit; the card holds the moves) |
| `intermediate-u-substitution` | 1.11 | `u-substitution.md` | `units/06-intermediate-u-sub/teaching.tex` |
| `absolute-values` | 1.12 | `piecewise.md` | `units/07-abs-reverse-product/teaching.tex` |
| `reverse-product-rule` | 1.13 | `integration-by-parts.md` | `units/07-abs-reverse-product/teaching.tex` |
| `basic-series` | 1.14 | `series.md` | `units/08-basic-series/teaching.tex` |
| `intermediate-trig-integrals` | 1.15 | `trigonometric.md` | `units/09-intermediate-trig/teaching.tex` |
| `intermediate-trig-substitution` | 1.16 | `trigonometric.md` | the same file |
| `inverse-functions` | 1.17 | `symmetry-kings.md` | `units/10-inverse-kings/teaching.tex` |
| `kings-queens-rule` | 1.18 | `symmetry-kings.md` | the same file |
| `gaussian-integrals` | 1.19 | `gaussian-dirichlet.md` | `units/11-gaussian-wildcard/teaching.tex` |
| `special-wildcard` | 1.20 | `concepts/README.md` routes each drill | `units/11-gaussian-wildcard/teaching.tex` |

`special-wildcard` is a router. Floor, a fixed-interval parameter, a reflection, and Gaussian cousins share the node. The route table is the card.

`algebra-manipulation` was the thin Round 1 node in the unit file. `algebra.md` is the lesson for completing the square, rationalizing, and the decision to open `docs/techniques/introduce-constant.md`.

## Later nodes with a coach card

The card states the move. Stored numbers stay in the unit.

| Node | Yang | Card | What the card adds |
|---|---|---|---|
| `forced-u-sub` | 2.3 | `u-substitution.md` | Solve for \(x\) when \(du\) is missing. Original \(\int_0^1 e^{\sqrt{x}}\,dx=2\). Unit 13 keeps its drills. |
| `power-substitution` | 3.1 | `u-substitution.md` | Clear a root by \(x=u^n\), then divide. Original \(\int_0^1 \sqrt{x}/(1+x)\,dx=2-\pi/2\). |
| `gamma` | 2.4 | `integration-by-parts.md` | \(J_n=n J_{n-1}\) with \(J_0=1\). Values stay the unit 14 drills. |
| `parts-regular` | 2.5 | `integration-by-parts.md` | One step, then the cyclic stop. `U15-D04` is the faded definite case. |
| `awkward-parts` | 3.5 | `integration-by-parts.md` | Pointer to unit 22 after ordinary parts is solid. |
| `semi-parts` | 5.1 | `integration-by-parts.md` | Match coefficients on \(p(x)e^x\). Longer drills stay in unit 28. |
| `reverse-quotient` | 4.6 | `integration-by-parts.md` | \((f/g)'\). The antiderivative of `U27-D01`, then the limit \(2/\pi-1\) on \((0,\pi/2]\). |
| `trig-identities` | 2.6 | `trigonometric.md` | Odd and even powers, then unit 16. |
| `intermediate-trig-sub-ch2` | 2.7 | `trigonometric.md` | The three-row radical table. |
| `advanced-trig-integrals` | 5.2 | `trigonometric.md` | Same powers. Unit 29 keeps secant. |
| `advanced-trig-substitution` | 3.4 | `trigonometric.md` | \(\sec\), \(\sinh\), or \(\tan\) after the basic table is solid. |
| `weierstrass` | 4.5 | `trigonometric.md` | The three replacements and an original \(\int_0^{\pi/2} dx/(2+\cos x)=\pi\sqrt{3}/9\). Unit 26 is the miss file. |
| `wallis` | 3.3 | `trigonometric.md` | \(I_n=((n-1)/n)I_{n-2}\). `U20-D01` is \(I_4=3\pi/16\). |
| `periodicity` | 3.7 | `trigonometric.md` | Full-period products. `U23-D01` is the stored pair. |
| `advanced-kings-queens` | 4.4 | `symmetry-kings.md` | The identity is on the card. Further copies stay in unit 25. |
| `infinite-functions` | 2.8 | `series.md` | Closed form before integrating. Differentiating the sum is unit 17. |
| `taylor-series` | 6.2 | `series.md` | Termwise log series equaling the parts value \(2\ln 2-1\). Endpoint limits stay in unit 32. |
| `advanced-gaussian` | 5.3 | `gaussian-dirichlet.md` | Quote \(\sqrt{\pi}\), then scale. Original \(\int_0^{\infty} e^{-4x^2}\,dx=\sqrt{\pi}/4\). |
| `dirichlet` | 5.4 | `gaussian-dirichlet.md` | Quote `U30-D05`, then scale by \(u=bx\). |
| `intermediate-partial-fractions` | 3.6 | `partial-fractions.md` | A repeated factor needs two terms. |
| `feynman` | 6.7 | `algebra.md` | Fixed interval versus a moving endpoint. The unit 34 case \(I'(2)=6\) stays the unit's example. |
| `modified-textbook` | 2.1 | `habits.md` | Scale of `U12-D01` on \([0,1]\), value \(e^e-e\). The four textbook drills stay in unit 12. |
| `sneaky-algebra` | 2.2 | `habits.md` | Scale of `U12-D05` with \(3\) in place of \(2\), value \(11/3\). |
| `sneaky-u-sub` | 3.2 | `habits.md` | Numerator form of the `U19-D05` substitution on \([0,3]\), value \(4\sqrt{3}\). |
| `sneaky-symmetry` | 2.9 | `habits.md` | Three-factor shift on \([1,3]\), value \(0\). `U18-D04` stays the even warning, value \(\pi^3/96\). |
| `sneaky-product-rule` | 2.10 | `habits.md` | Half the coefficient of `U18-D06` on \([1,4]\), value \(2e^4-e\). |
| `speed-bashing` | 3.8 | `habits.md` | Two-term split on \([0,1]\), value \(\frac12+\ln 2\). `U23-D06` and `U23-D07` stay in the unit. |
| `complexifying` | 6.3 | `habits.md` | Decay \(2\) in place of the stored decay \(1\), value \(2/5\). `U32-D05` stays \(1/2\). |
| `ninja-substitution` | 6.4 | `habits.md` | \(\int_0^1 \arctan x/(1+x^2)\,dx=\pi^2/32\). `U33-D04` stays the stored logarithm. |
| `inversion` | 6.5 | `habits.md` | Finite copy of `U33-D08` on \([0,1]\), value \(1/4\). |
| `modified-famous` | 6.8 | `habits.md` | Gaussian scale \(e^{-9x^2}\) equals \(\sqrt{\pi}/6\), and \(\sin(3x)/x\) equals \(\pi/2\). Series values stay the ones unit 35 prints. |
| `unique-tricks` | 6.9 | `habits.md` | Parameter from \(0\) to \(4\), value \(\ln 5\). `U36-D03` stays \(G\). |

## Unit lessons, no new example

Open the unit file. The move is already there.

| Node | Yang | Lesson | Move the unit states |
|---|---|---|---|
| `undertow` | 4.1 | `units/24-undertow-square/teaching.tex` | Divide by a power of \(x\) until the numerator is the derivative of the denominator. `U24-D01`. |
| `square-square` | 4.2 | the same file | \((\sqrt{x}\pm 1/\sqrt{x})^2\) under the radical. `U24-D07` stores \(20/3\). |
| `inverse-jailbreaking` | 6.1 | `units/31-inverse-jailbreak/teaching.tex` | Inverse in the \(u\) slot. The area identity is the symmetry card. |
| `frullani` | 6.6 | `units/34-frullani-feynman/teaching.tex` | Difference of exponentials as an integral in a parameter. `U34-D01`. |

## Still thin

None. The eleven habits that were thin are rows of `docs/techniques/concepts/habits.md` above. Each unit file teaches the stored drills. Each fence on that card is a scale of one of those drills, checked with SymPy, and is not a drill id.

Yang inventory 4.3 has no node. It stays skipped.

## Deferred in the catalog

| Node | Depth | Teach | Tick |
|---|---|---|---|
| `floor` | deferred-taught | `docs/techniques/floor.md`, drills `U11-D09` through `U11-D12` | Leave unticked. The id has no unit. |
| `dutis` | deferred-taught | `docs/techniques/introduce-constant.md` for a fixed interval, unit 34 for a moving endpoint. Drills `U11-D13` through `U11-D15`. | Leave unticked. |
| `vector-calc` | deferred-open | Syllabus §1 lists it and does not require it for Round 1. The polar sketch of the Gaussian is optional background in unit 30. | No tick. |
| `beta` | deferred-open | Syllabus §2 names the Beta function. No unit and no drill. | No value. |
| `zeta` | deferred-open | Syllabus §2 names zeta. The series card refuses a new zeta evaluation. | No value. |
| `euler-mascheroni` | deferred-open | Syllabus §2 names the constant. No unit. | No value. |
| `catalan` | deferred-open | Unit 36 tells the coach to leave \(G\) as \(G\). | No replacement by a logarithm or a rational. |

## Practice indexes

These nine nodes are not concepts. Round formats are `docs/techniques/formats.md`. Per-question tags are not a lesson, and this map does not add any.

| Node | What the tree already says |
|---|---|
| `sample-bridge` | Sample list after the concept units. |
| `timed-mock-01` | Mock meta, after the bridge. |
| `past-paper-pdf-mock` | Local Round 1 PDFs, 2020 through 2025. |
| `past-paper-2025` | PDF local. No per-question tag catalogue yet. |
| `past-paper-2024` | PDF local. No per-question tag catalogue yet. |
| `past-paper-2023` | PDF local. |
| `past-paper-2022` | PDF local, with tiebreakers. |
| `past-paper-2021` | PDF local, 40 questions. |
| `past-paper-2020` | PDF local, 40 questions. |

## Counts

| Depth | Nodes |
|---|---|
| card, Round 1 gate | 20 |
| card, later chapter or syllabus technique | 32 |
| unit lesson, no new example | 4 |
| thin | 0 |
| deferred-taught | 2 (`floor`, `dutis`) |
| deferred-open | 5 |
| index | 9 |
| Total | 72 |

The thin count was 11 before the habit card. It is 0. The 20 Round 1 nodes and the 32 later card rows are what an agent can teach without a Yang answer key. The 5 deferred-open rows are the remaining gap. `floor` and `dutis` stay unticked.
