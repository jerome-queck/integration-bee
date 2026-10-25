# R3-2024-Chainlink-G3-Q05

- Problem: `sources/past/r3/2024/Chainlink_Game_3_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 5)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 3, problem 5)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 3, problem 5)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/2}\ln(\sin x)\tan x\,dx.
\]

## Solution

The substitution \(u=\cos x\) gives

\[
\int_{0}^{1}\frac{\ln\sqrt{1-u^{2}}}{u}\,du=\frac12\int_{0}^{1}\frac{\ln(1-u^{2})}{u}\,du.
\]

The series for \(\ln(1-u^{2})\) integrates term by term:

\[
-\frac12\sum_{n=1}^{\infty}\int_{0}^{1}\frac{u^{2n-1}}{n}\,du=-\frac14\sum_{n=1}^{\infty}\frac{1}{n^{2}}=-\frac{\pi^{2}}{24}.
\]

## Final answer

\[
-\dfrac{\pi^{2}}{24}.
\]

## SymPy self-check

SymPy checks \(\ln\sqrt{1-u^{2}}=\frac12\ln(1-u^{2})\). Each series term contributes \(-1/(4n^{2})\), and the sum is \(-\pi^{2}/24\).
