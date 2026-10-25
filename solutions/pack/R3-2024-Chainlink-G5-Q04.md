# R3-2024-Chainlink-G5-Q04

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 4)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 4)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 4)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}\left(\frac{1}{x}-\left\lfloor\frac{1}{x}\right\rfloor-\frac{1}{x^{2}}\left\lfloor\frac{1}{x}\right\rfloor^{-2}\right)\,dx.
\]

## Solution

The substitution \(x=1/y\) sends the interval to \([1,\infty)\) and the integrand to

\[
\frac{1}{y}-\frac{\lfloor y\rfloor}{y^{2}}-\frac{1}{\lfloor y\rfloor^{2}}.
\]

On \([n,n+1]\) the first two terms have antiderivative \(\ln y+n/y\), and the definite piece is \(\ln(n+1)-\ln n-1/(n+1)\). Summing to \(N\) produces \(\ln(N+1)-H_{N+1}+1\), whose limit is \(1-\gamma\). The remaining terms contribute \(-\sum 1/n^{2}=-\pi^{2}/6\). The value is \(1-\gamma-\pi^{2}/6\).

## Final answer

\[
1-\gamma-\dfrac{\pi^{2}}{6}.
\]

## SymPy self-check

SymPy checks the change of variables on each interval \([n,n+1]\) and the antiderivative \(\ln y+n/y\). The limit \(\ln(N+1)-H_{N+1}+1\) is \(1-\gamma\), and \(\sum_{n\ge 1}1/n^{2}=\pi^{2}/6\).
