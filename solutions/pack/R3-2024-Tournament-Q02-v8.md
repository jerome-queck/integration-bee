# R3-2024-Tournament-Q02-v8

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 1, problem 2, answer slide 111)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 111)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.1, problem 2)
- The catalog row is not changed.

## Problem

The catalog text of this row is the line printed on slide 111, not the integral. Slide 111 is the answer reveal for Battle 3, Fight 1, problem 2:

\[
\int_{0}^{\infty}\frac{1}{x}\left(\arctan\frac{x}{1+2x^{2}}-\arctan\frac{x}{1+12x^{2}}\right)dx.
\]

The integral itself is catalogued as `R3-2024-Tournament-Q02-v6`.

## Solution

The tangent-subtraction formula gives, for \(x>0\),

\[
\arctan(2x)-\arctan x=\arctan\frac{x}{1+2x^{2}},
\]
\[
\arctan(4x)-\arctan(3x)=\arctan\frac{x}{1+12x^{2}}.
\]

The integral is therefore the difference of two Frullani integrals of arctangents. For \(a>0\),

\[
\int_{0}^{\infty}\frac{\arctan(ax)}{x}\,dx
\]

is evaluated by writing \(\arctan(ax)=\int_{0}^{a}x/(1+(tx)^{2})\,dt\) and switching the order, which produces \((\pi/2)\ln a\) up to the same divergent constant in each term. The difference is

\[
\frac{\pi}{2}\left(\ln 2-\ln\frac{4}{3}\right)=\frac{\pi}{2}(\ln 3-\ln 2).
\]

The answer slide prints \(\frac{\pi}{2}(\ln 3-\ln 2)\).

## Final answer

\[
\dfrac{\pi}{2}(\ln 3-\ln 2).
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q02_v8`. That check runs `check_r3_2024_tournament_q02_v6` for `R3-2024-Tournament-Q02-v6`. SymPy checks the two arctangent differences and \(\int_{0}^{\infty}dx/(1+(ax)^{2})=\pi/(2a)\), then simplifies the logarithm combination.
