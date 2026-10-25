# R3-2024-Chainlink-G5-Q01

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 1)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 1)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{\arctan x}{x^{2}+1}\,dx.
\]

## Solution

The integrand is the derivative of \(\frac12(\arctan x)^{2}\):

\[
\int_{0}^{\infty}\frac{\arctan x}{x^{2}+1}\,dx=\frac12\bigl[(\arctan x)^{2}\bigr]_{0}^{\infty}=\frac{\pi^{2}}{8}.
\]

## Final answer

\[
\dfrac{\pi^{2}}{8}.
\]

## SymPy self-check

SymPy differentiates \(\frac12(\arctan x)^{2}\) to \(\arctan x/(1+x^{2})\) and evaluates the limits \(0\) and \(\infty\) as \(\pi^{2}/8\).
