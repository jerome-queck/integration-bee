# R3-2024-Chainlink-G1-Q02

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 2)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 2)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 2)
- The catalog row is not changed.

## Problem

\[
\int\frac{\sinh x+\cosh x}{\sinh(e^{x})+\cosh(e^{x})}\,dx.
\]

## Solution

The solutions PDF rewrites the hyperbolic sums as exponentials. The numerator is \(e^{x}\) and the denominator is \(e^{e^{x}}\), so

\[
\int\frac{e^{x}}{e^{e^{x}}}\,dx=-e^{-e^{x}}+C.
\]

## Final answer

\[
-e^{-e^{x}}+C.
\]

## SymPy self-check

SymPy simplifies \((\sinh x+\cosh x)/(\sinh(e^{x})+\cosh(e^{x}))\) to \(e^{x-e^{x}}\) and differentiates \(-e^{-e^{x}}\) back to that integrand.
