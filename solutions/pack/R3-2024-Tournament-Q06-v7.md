# R3-2024-Tournament-Q06-v7

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 2, problem 6, answer slide 132)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 132)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.2, problem 3)
- The catalog row is not changed.

## Problem

The catalog text of this row is the word Answer. Slide 132 prints the final value of Battle 3, Fight 2, problem 6:

\[
\int_{1}^{\sqrt{2}}\frac{\sqrt{x^{2}+2\sqrt{x^{2}-1}}}{x}\,dx.
\]

The integral itself is the previous slide, catalogued as `R3-2024-Tournament-Q06-v6`.

## Solution

Set \(x=\sec u\), so \(u\) runs from \(0\) to \(\pi/4\) and \(dx=\sec u\tan u\,du\). The expression under the outer square root becomes

\[
\sec^{2}u+2\tan u=(1+\tan u)^{2}.
\]

On \([0,\pi/4]\) one has \(1+\tan u\ge 1\), so the integrand simplifies to \(\tan u+\tan^{2}u\). An antiderivative is

\[
-\ln|\cos u|+\tan u-u.
\]

Evaluating from \(0\) to \(\pi/4\) gives

\[
-\ln\frac{\sqrt{2}}{2}+1-\frac{\pi}{4}=\frac12\ln 2+1-\frac{\pi}{4}.
\]

The answer slide prints \(\frac12\ln 2+1-\pi/4\).

## Final answer

\[
\dfrac{1}{2}\ln 2+1-\dfrac{\pi}{4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q06_v7`. That check runs `check_r3_2024_tournament_q06_v6` for `R3-2024-Tournament-Q06-v6`. SymPy checks \(\sec^{2}u+2\tan u=(1+\tan u)^{2}\), differentiates the antiderivative, and evaluates it from \(0\) to \(\pi/4\).
