# R3-2024-Chainlink-G5-Q08

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 8)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 8)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 8)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[
\int\frac{\cos x+1-x^{2}}{(x\sin x+1)\sqrt{1-x^{2}}}\,dx.
\]

## Solution

Set

\[
y=\frac{x+\sin x}{x\sin x+1}.
\]

The solutions PDF computes

\[
y'=\frac{(\cos x+1-x^{2})\cos x}{(x\sin x+1)^{2}}.
\]

Comparing this with the integrand leaves the factor

\[
\frac{x\sin x+1}{\sqrt{(1-\sin^{2}x)(1-x^{2})}}=\frac{1}{\sqrt{1-y^{2}}}.
\]

The integral is therefore \(\int dy/\sqrt{1-y^{2}}=\arcsin y+C\).

## Final answer

\[
\arcsin\left(\dfrac{x+\sin x}{x\sin x+1}\right)+C.
\]

## SymPy self-check

The gate checks the derivative of the arcsine argument and its radicand identity. On the real domain \(-1<x<1\), both \(\cos x\) and \(1+x\sin x\) are positive, which fixes the square-root sign. Finite additive constants are accepted; variable-dependent errors and unevaluated offsets are rejected.
