# R3-2024-Tournament-Q01-v9

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 1, problem 1, answer slide 106)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 106)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.1, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 106, not the integral. Slide 106 is the answer reveal for Battle 3, Fight 1, problem 1:

\[
\int\frac{\ln x+2}{(xe)^{-x}+2}\,dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q01-v7`.

## Solution

Multiply the numerator and the denominator by \((xe)^{x}\):

\[
\frac{\ln x+2}{(xe)^{-x}+2}=\frac{(xe)^{x}(\ln x+2)}{1+2(xe)^{x}}.
\]

The derivative of \(u=(xe)^{x}\) is \(u(\ln x+2)\), so the integrand is

\[
\frac{u'}{1+2u}.
\]

Its antiderivative is

\[
\frac12\ln\bigl(1+2(xe)^{x}\bigr)+C.
\]

The answer slide prints the same expression.

## Final answer

\[
\dfrac{1}{2}\ln\bigl(1+2(xe)^{x}\bigr)+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q01_v9`. That check runs `check_r3_2024_tournament_q01_v7` for `R3-2024-Tournament-Q01-v7`. SymPy checks that the derivative of \((xe)^{x}\) is \((xe)^{x}(\ln x+2)\) and differentiates the logarithmic antiderivative.
