# R3-2024-Tournament-Q04-v5

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 2, Fight 2, problem 4, answer slide 73)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 73)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 2.2, problem 1)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 73 prints the final value of Battle 2, Fight 2, problem 4:

\[
\int\frac{x^{2}-1}{x^{3}+x}\ln\left(x^{3}+\frac{1}{x^{3}}+3\left(x+\frac{1}{x}\right)\right)dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q04-v4`.

## Solution

The logarithm argument is \(\bigl(x+1/x\bigr)^{3}\), so the integral is

\[
3\int\frac{x^{2}-1}{x^{3}+x}\ln\left(x+\frac{1}{x}\right)dx.
\]

The substitution \(u=\ln(x+1/x)\) has \(du=(x^{2}-1)/(x^{3}+x)\,dx\), and the antiderivative is

\[
\frac32\left(\ln\left(x+\frac{1}{x}\right)\right)^{2}+C.
\]

Slide 73 prints that antiderivative.

## Final answer

\[
\dfrac{3}{2}\left(\ln\left(x+\dfrac{1}{x}\right)\right)^{2}+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q04_v5`. That check runs the cube identity and the derivative check for `R3-2024-Tournament-Q04-v4`.
