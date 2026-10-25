# R3-2024-Tournament-Q04-v2

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 2, problem 4, answer slide 24)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 24)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.2, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 24 prints the final value of Battle 1, Fight 2, problem 4:

\[
\int\left(\frac{x-1}{(x-2)(x-3)}+\frac{x-2}{(x-3)(x-1)}+\frac{x-3}{(x-1)(x-2)}\right)dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q04`.

## Solution

Partial fractions, as written in the solutions PDF, give

\[
\frac{5/2}{x-3}+\frac{5/2}{x-1}-\frac{2}{x-2}.
\]

Integrating term by term produces

\[
\frac52\ln|x-3|+\frac52\ln|x-1|-2\ln|x-2|+C.
\]

The answer slide prints the same antiderivative.

## Final answer

\[
\dfrac{5}{2}\ln|x-3|+\dfrac{5}{2}\ln|x-1|-2\ln|x-2|+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q04_v2`. That check runs `check_r3_2024_tournament_q04` for `R3-2024-Tournament-Q04`. SymPy checks the partial-fraction split and differentiates the logarithmic antiderivative.
