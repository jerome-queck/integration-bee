# R3-2024-Chainlink-G1-Q01

- Problem: `sources/past/r3/2024/Chainlink_Game_1_2024_Round_3_UK_University_Integration_Bee_(6).pdf` (problem 1)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 1, problem 1)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 1, problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{1}^{4}\{x\}^{\lfloor x\rfloor}\,dx.
\]

## Solution

On each interval \([n,n+1]\) with \(n=1,2,3\), one has \(\lfloor x\rfloor=n\) and \(\{x\}=x-n\), so the integrand is \((x-n)^{n}\). The solutions PDF shifts each piece to \([0,1]\):

\[
\int_{1}^{4}\{x\}^{\lfloor x\rfloor}\,dx=\sum_{n=1}^{3}\int_{0}^{1}u^{n}\,du=\frac12+\frac13+\frac14=\frac{13}{12}.
\]

## Final answer

\[
\dfrac{13}{12}.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{1}u^{n}\,du=1/(n+1)\) and sums \(1/2+1/3+1/4\) to \(13/12\).
