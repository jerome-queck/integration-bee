# R3-2024-Tournament-Q01

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 1, Fight 1, problem 1, slide 6)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 8)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 1.1, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{\lfloor x\rfloor}{1+\lfloor x\rfloor^{2}+\lfloor x\rfloor^{4}}\,dx.
\]

## Solution

On each interval \([n,n+1)\) the integrand is the constant \(n/(1+n^{2}+n^{4})\). Partial fractions give

\[
\frac{n}{1+n^{2}+n^{4}}=\frac12\left(\frac{1}{n^{2}-n+1}-\frac{1}{n^{2}+n+1}\right).
\]

The second denominator is the first shifted by one, \(n^{2}+n+1=(n+1)^{2}-(n+1)+1\), so the series telescopes:

\[
\sum_{n=0}^{\infty}\frac{n}{1+n^{2}+n^{4}}=\frac12.
\]

The answer slide prints \(1/2\).

## Final answer

\[
\dfrac{1}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q01`. SymPy checks the partial-fraction identity and sums the telescoping series to \(1/2\).
