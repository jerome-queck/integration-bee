# R3-2024-Tournament-Q09-v7

- Problem: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (Battle 3, Fight 3, problem 9, slide 146)
- Printed answer: `sources/past/r3/2024/Tournament_slides_2024_Round_3_UK_University_Integration_Bee.pdf` (slide 148)
- Worked source: `sources/past/r3/2024/Tournament_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (section 3.3, problem 3)
- The catalog row is not changed.

## Problem

\[
\int\frac{1}{\sin x\bigl(\ln(\sin x)-\ln(1+\cos x)\bigr)}\,dx.
\]

## Solution

Set \(u=\ln(\sin x)-\ln(1+\cos x)\). The solutions PDF differentiates this and simplifies:

\[
u'=\frac{\cos x}{\sin x}-\frac{-\sin x}{1+\cos x}=\frac{1}{\sin x}.
\]

The integrand is \(u'/u\), so

\[
\int\frac{1}{u}\,du=\ln\bigl|\ln(\sin x)-\ln(1+\cos x)\bigr|+C.
\]

The answer slide prints the same antiderivative.

## Final answer

\[
\ln\bigl|\ln(\sin x)-\ln(1+\cos x)\bigr|+C.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_tournament_q09_v7`. SymPy checks \(u'=1/\sin x\) and differentiates \(\ln u\).
