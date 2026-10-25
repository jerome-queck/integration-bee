# Partial fractions

Coach card. Original examples on this page were checked with SymPy. They are not catalog rows. Stored drills are cited by id. A contest row is not a source for a new number.

Divide first when the numerator's degree is at least the denominator's. That division is `algebra.md` and `docs/techniques/introduce-constant.md`. Partial fractions start on the proper remainder.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `basic-partial-fractions` | 2 | `basic-integration`, `algebra-manipulation` | `units/05-partial-fractions/teaching.tex` |
| `intermediate-partial-fractions` | 3 | `basic-partial-fractions` | `units/22-awkward-parts-pf/teaching.tex` |

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

### Miss to the next drill

| Miss | Next drill |
|---|---|
| Distinct linear factors, and the cover-up step was skipped | `U05-D01`, stored \(\ln(4/3)\). |
| A logarithm was quoted on an interval that meets a pole | Refuse the number. `U05-D02` keeps both endpoints off the poles, on \([1,2]\), stored \(\ln(4/3)\). `U05-D03` does the same on \([3,4]\), stored \(\ln(4/3)\). |
| The numerator was not \(1\) | `U05-D05`, stored \(\ln(9/2)\). Then `U05-D06`, stored \(\ln(128/27)\). |
| \(x^2-1\) was left as one fraction | `U05-D04`, stored \(\frac12\ln\lvert(x-1)/(x+1)\rvert\). |
| A repeated factor was given one coefficient | After `basic-partial-fractions` is solid, `U22-D07`, then `U22-D08` on \([1,2]\), stored \(\frac12+\ln(3/4)\). |
| Three distinct linear factors | `U22-D06`, after the same prerequisite. |

## Distinct linear factors

Cover a factor and read the coefficient. On \([0,1]\),

\[
\frac{1}{(x+1)(x+3)}=\frac{1}{2}\left(\frac{1}{x+1}-\frac{1}{x+3}\right),
\]

\[
\int_0^1\frac{dx}{(x+1)(x+3)}=\frac12\ln\frac{3}{2}.
\]

Unit 05 stores \(\int_0^1 dx/((x+1)(x+2))=\ln(4/3)\) as `U05-D01`, and \(\int_1^2 dx/(x(x+1))=\ln(4/3)\) as `U05-D02`, from \(1/x-1/(x+1)\).

## A repeated factor

A squared linear factor needs two terms.

\[
\frac{2x+3}{(x+1)^2}=\frac{2}{x+1}+\frac{1}{(x+1)^2},
\]

because \(2x+3=2(x+1)+1\). On \([0,1]\),

\[
\int_0^1\frac{2x+3}{(x+1)^2}\,dx=2\ln 2+\frac12.
\]

Unit 22's rule is the same. A squared factor is \(A/(x-r)+B/(x-r)^2\), not a single term. Open that unit when the distinct-linear drills are solid.

## An irreducible quadratic

A quadratic factor \(x^2+1\) produces a logarithm from the \(x\) in the numerator and an arctangent from the constant.

On \([0,1]\),

\[
\int_0^1\frac{x+1}{x^2+1}\,dx=\frac12\ln 2+\frac{\pi}{4}.
\]

Split into \(\frac12\int_0^1 2x/(x^2+1)\,dx\) and \(\int_0^1 dx/(x^2+1)\). The first is half of `U01-D01`, value \((\ln 2)/2\). The second is `U01-D08`, value \(\pi/4\).

## Faded step

Decompose \(1/(x(x+2))\) and integrate from 0 to 1. The decomposition is \(\frac12(1/x-1/(x+2))\). Watch the endpoint at 0. The integral \(\int_0^1 dx/(x(x+2))\) diverges. The faded lesson is to check the interval before quoting a logarithm. `U05-D02` keeps both endpoints away from the poles, on \([1,2]\).

## Where this goes wrong

The fraction was improper and was decomposed anyway. Divide, or add and subtract, until the numerator is shorter than the denominator.

A repeated factor was given one coefficient. Count the power and write that many terms.

The numerator \(x\) on \(x^2+1\) was sent to an arctangent. That piece is a logarithm. The constant piece is the arctangent.

A pole sat inside the interval, or on an endpoint, and a log difference was quoted. Split at the pole and see whether each improper piece converges.

## On a miss

Teach this file, then unit 05. Use the miss table. The first drill is `U05-D01`. Repeated factors and three-factor decompositions are unit 22, after `basic-partial-fractions` is solid. A correct value from an undivided improper fraction still needs the division named.
