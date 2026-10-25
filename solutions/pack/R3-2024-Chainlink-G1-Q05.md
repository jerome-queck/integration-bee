# R3-2024-Chainlink-G1-Q05

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 5)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 5)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 5)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\frac{\ln(1+x+x^{2})}{x}\,dx.
\]

## Solution

The solutions PDF inserts \(\ln(1-x)\) so that the numerator is \(\ln(1-x^{3})-\ln(1-x)\). The series \(\ln(1-z)=-\sum_{n\ge 1}z^{n}/n\) then gives

\[
\int_{0}^{1}\frac{\ln(1-x^{3})-\ln(1-x)}{x}\,dx=\sum_{n=1}^{\infty}\int_{0}^{1}\frac{x^{n-1}-x^{3n-1}}{n}\,dx=\frac23\sum_{n=1}^{\infty}\frac{1}{n^{2}}=\frac{\pi^{2}}{9}.
\]

## Final answer

\[
\dfrac{\pi^{2}}{9}.
\]

## SymPy self-check

SymPy checks \((1-x)(1+x+x^{2})=1-x^{3}\). Each term integrates to \((2/3)/n^{2}\), and the sum of that series is \(\pi^{2}/9\).
