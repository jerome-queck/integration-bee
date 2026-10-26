# Coach cards

These pages teach Round 1 technique families from the unit notes already in the repo, plus original examples checked with SymPy. They are not gap ids. A mark still uses one of the six headings in `docs/techniques/beyond-yang.md`. The node-by-node map is `pedagogy/concept-map.md`. How a tick chooses the page is `pedagogy/round1-coach.md`.

The deferred recognition notes below also explain syllabus names through cited definitions and derivations. They add no unit, stored drill, or readiness credit. Their catalog ids stay unticked.

A contest row is not a source for a new number. A stored drill id is a source. An example with no drill id is original exposition. Yang is one writeup of the same moves. The lesson is the unit file named on the card.

The gap index admits exactly six headings, and it rejects an extra file placed directly in `docs/techniques/`. These cards live in this subdirectory for that reason. See `docs/decisions/0014-concept-cards.md`.

## Which card

Read the integrand, then open one card. If two seem to fit, open the earlier one in this list and try it. Stop when the integral is finished. A Round 1 paper uses the same shapes. The route from a paper shape to a unit is `pedagogy/past-paper-routing.md`. That note does not quote a pack final.

| You see | Open |
|---|---|
| A factor that is a constant times the derivative of an inside function, a pure power, or \(e^{ax}\) | `u-substitution.md` |
| A polynomial times an exponential, a logarithm, or an inverse function | `integration-by-parts.md` |
| A symmetric interval, a reflection \(x \mapsto a+b-x\), or an inverse with no extra factor | `symmetry-kings.md` |
| Sine or cosine powers, a radical \(a^2-x^2\), \(a^2+x^2\), \(x^2-a^2\), or a rational function of sine and cosine | `trigonometric.md` |
| A ratio of polynomials | `partial-fractions.md`, after the division in `algebra.md` |
| A sum you can integrate term by term, or a geometric closed form | `series.md` |
| \(e^{-x^2}\), or \((\sin x)/x\) on a half-line | `gaussian-dirichlet.md` |
| An absolute value, a floor, or a fractional part | `piecewise.md` and, for the floor, `docs/techniques/floor.md` |
| A numerator that is almost a denominator or almost its derivative | `algebra.md` and `docs/techniques/introduce-constant.md` |
| A textbook form with one extra factor, a cancelled radical, a shift to an odd product, a hidden product, a sum of textbook terms, \(e^{ax}\cos bx\), \(1+x^2\) beside a logarithm, or \(x\mapsto 1/x\) | `habits.md`, after the earlier row that also fits |

## Wildcard drills

`special-wildcard` is not one technique. The unit 11 drills route as follows. The coach does not tick `floor` or `dutis`.

| Drill | Teach |
|---|---|
| `U11-D01` through `U11-D04`, `U11-D08` | `gaussian-dirichlet.md` |
| `U11-D05` | arctangent, unit 01, `u-substitution.md` |
| `U11-D06` | absolute value, then the exponential, `piecewise.md` |
| `U11-D07` | reflection on \([0,\pi/2]\), `symmetry-kings.md` |
| `U11-D09` through `U11-D12` | `docs/techniques/floor.md` |
| `U11-D13` through `U11-D15` | fixed-interval parameter, `algebra.md` and `docs/techniques/introduce-constant.md` |

## Round 2 and Round 3

A relay, a crossnumber, a chain, a chosen pair, or a boxed tournament line is not a new integrand card. Open `docs/techniques/formats.md`, then `pedagogy/round2-coach.md` or `pedagogy/round3-coach.md`. The integral stays a stored unit drill.

## Deferred syllabus recognition

Open one of these only when its name or pattern needs explanation. Each is `deferred-noted` in the concept map. They are optional background for Round 1; none is a requirement for the Round 1 gate. Leave all five catalog ids unticked. `floor` and `dutis` remain separately `deferred-taught` with their existing note and unit 11 drills, also unticked.

| Name or question | Open | Stop at |
|---|---|---|
| Why does the Gaussian use a polar double integral? | [Vector calculus background](vector-calc.md) | Unit 30's optional sketch; return to one-variable scaling. |
| Two endpoint powers on \([0,1]\) | [Beta](beta.md) | The Beta–Gamma identity with its convergence conditions. |
| A convergent reciprocal-power sum or a zeta symbol | [Zeta](zeta.md) | The justified named expression; no invented zeta evaluation. |
| A harmonic sum minus a logarithm, or \(\Gamma'(1)\) | [Euler–Mascheroni](euler-mascheroni.md) | \(\gamma\), with the sign from the derivation. |
| The odd alternating square sum or unit 36's `U36-D03` | [Catalan](catalan.md) | \(G\); no guessed logarithm or rational replacement. |

## On a miss

Teach the one file the mark names when the mark carries a gap id. Otherwise teach the card for the node, then the unit `teaching.tex`. Do not invent a contest answer.
