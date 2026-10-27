# Series

Coach card. Original examples on this page were checked with SymPy, including the summed series. They are not catalog rows. Stored drills are cited by id. A contest row is not a source for a new number. A series that the unit leaves as a named constant stays that constant. This page does not evaluate a zeta value.

## Adaptive

| Node | Difficulty | Prerequisites | Lesson |
|---|---|---|---|
| `basic-series` | 2 | `basic-integration` | `units/08-basic-series/teaching.tex` |
| `infinite-functions` | 3 | `basic-series` | `units/17-infinite-functions/teaching.tex` |
| `taylor-series` | 4 | `basic-series`, `basic-integration-by-parts` | `units/32-taylor-complex/teaching.tex` |

`complexifying` shares unit 32. The unit replaces \(e^{ax}\cos bx\) by the real part of a complex exponential. Teach that file's stored drill. The scaled fence is `habits.md`. This card does not add a zeta value.

Read `pedagogy/round1-coach.md` for how a tick selects the worked example or the next drill.

### Miss to the next drill

| Miss | Next drill |
|---|---|
| A polynomial was expanded as an infinite series | `U08-D01`, stored \(25/12\). A shorter polynomial is `U08-D04`, stored \(5/6\). |
| The closed form was skipped on a safe geometric interval | `U08-D02`, stored \(\ln 2\) on \([0,1/2]\). `U08-D05` stores \(\ln(4/3)\) on \([0,1/3]\). |
| The interval was pushed to the pole at \(1\) | Refuse the value. Return to `U08-D02`. |
| Three terms were treated as an infinite sum | After `basic-series` is solid, `U17-D09`, stored \(11/6\). |
| A geometric kernel was expanded term by term when the closed form is one integral | `U17-D01`, stored \(\ln 2\). The shorter interval is `U17-D08`, stored \(\ln(3/2)\). A coefficient \(n\) is `U17-D07`, stored \(1\). |
| A substitution was replaced by a series | `U17-D02`, stored \(\ln 2\). In unit 32, `U32-D03` stores \(\frac12 e^{x^2}\). |
| The endpoint \(x=1\) of an alternating series was the worry | `U32-D01`, stored \(\ln 2\), after the unit 08 drills are solid. |
| A named constant was replaced, or a new zeta value was written | Refuse. Unit 35 keeps the series it already prints. This card does not quote a zeta value. The ready optional `zeta` lesson is `docs/techniques/concepts/zeta.md`. |
| A four-term polynomial in unit 32 was treated as an infinite series | `U32-D02`, stored \(26/35\). Bare `U32-D04` stores \(1/4\). |
| The value \(1/2\) was written for \(\int e^x\cos x\,dx\) | `U32-D07`, stored \(\frac12 e^x(\sin x+\cos x)\). The sine antiderivative is bare `U32-D08`. |

## A finite sum

Integrate a polynomial term by term. Unit 08 stores

\[
\int_0^1(1+x+x^2+x^3)\,dx=1+\frac12+\frac13+\frac14=\frac{25}{12}
\]

as `U08-D01`. Three terms are still a finite sum. Unit 17 says to integrate a finite truncation directly.

## A geometric closed form

On an interval where \(|x|\) stays below 1, \(\sum_{n=0}^{\infty} x^n=1/(1-x)\). Integrate the closed form.

Unit 08 stores \(\int_0^{1/2} dx/(1-x)=\ln 2\) as `U08-D02`, the same value as summing \(\int_0^{1/2} x^n\,dx\).

On \([0,1/2]\),

\[
\sum_{n=0}^{\infty} x^{2n}=\frac{1}{1-x^2},
\]

\[
\int_0^{1/2}\frac{dx}{1-x^2}=\operatorname{artanh}\frac12=\frac12\ln 3.
\]

The endpoint \(x=1\) is not in this interval. \(1/(1-x)\) is not integrable through \(x=1\).

## A logarithm by parts, then by series

On \([0,1]\),

\[
\int_0^1\ln(1+x)\,dx=2\ln 2-1.
\]

Parts with \(u=\ln(1+x)\) and \(dv=dx\) gives \([x\ln(1+x)]_0^1-\int_0^1 x/(1+x)\,dx\). The remaining fraction is \(1-1/(1+x)\), so the integral is \(\ln 2-(1-\ln 2)\).

The series \(\ln(1+x)=\sum_{n=1}^{\infty}(-1)^{n+1} x^n/n\) holds on \([0,1)\), and the endpoint \(x=1\) is \(\ln 2\). Integrating term by term,

\[
\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n(n+1)}=2\ln 2-1.
\]

The sum is the partial-fraction telescope of \(1/(n(n+1))\). It is the same number as the parts evaluation. It is not a zeta value.

## Faded step

Integrate \(\sum_{n=0}^{3} x^n\) from 0 to 1 by terms. That is `U08-D01` without the series language. Then say which closed form would replace the sum if the upper index were infinite, and on which interval that replacement is legal. The legal interval in the stored drill is \([0,1/2]\), not \([0,1]\).

## Later series

Unit 17 differentiates a geometric sum when the coefficient carries an \(n\), and it replaces the sum by its closed form before integrating. Open it when `basic-series` is solid.

Unit 32 integrates a geometric series on \([0,1)\) and takes the endpoint as a limit. If one substitution already produces the antiderivative, use the substitution. The series explains the number. Unit 35 expands \(1/(1\pm x)\) toward values the unit treats as known. Leave a zeta number as the unit leaves it. This card does not quote one.

## Where this goes wrong

Termwise integration was used up to an endpoint where the closed form blows up. Shorten the interval to one the unit already uses, or take a limit and check it.

A three-term polynomial was expanded as an infinite series. Integrate the polynomial.

A named constant from a later unit was replaced by a decimal or by a logarithm. Keep the name the unit uses.

## On a miss

Teach this file, then unit 08. Use the miss table. Set `U08-D01`, then `U08-D02`. Taylor and complex exponentials wait until unit 32. That unit works `U32-D01`, fades `U32-D02`, and sets bare `U32-D04`. A right closed form on an interval where the series diverges still needs the interval named.
