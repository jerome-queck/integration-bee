# R3-2024-Chainlink-G3-Q01

- Problem: `sources/past/r3/2024/Chainlink_Game_3_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 1)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 3, problem 1)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 3, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}e^{-x^{1/2025}}\,dx.
\]

## Solution

Set \(y=x^{1/2025}\), so \(x=y^{2025}\) and \(dx=2025 y^{2024}\,dy\). The integral is the gamma value

\[
2025\int_{0}^{\infty}y^{2024}e^{-y}\,dy=2025!.
\]

## Final answer

\[
2025!.
\]

## SymPy self-check

For a positive integer \(n\), SymPy differentiates \(y^{n}\) to \(n y^{n-1}\) and evaluates \(n\int_{0}^{\infty}y^{n-1}e^{-y}\,dy=n!\). The case \(n=2025\) is \(2025!\).
