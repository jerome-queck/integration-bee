# R3-2024-Chainlink-G2-Q08

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 8)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 8)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 8)
- The catalog row is not changed.

## Problem

\[
\lim_{n\to\infty}\int_{0}^{1}2025\sin(\{nx^{2025}\})\cos(\{nx^{2025}\})\,dx.
\]

## Solution

The solutions PDF proves, for integrable \(f\) and \(k>0\),

\[
\lim_{n\to\infty}\int_{0}^{1}f(\{nx^{k}\})\,dx=\int_{0}^{1}f(t)\,dt.
\]

The interval \([0,1]\) splits at the points \((m/n)^{1/k}\). The substitution \(t=nx^{k}-m\) turns the integral into an average of Riemann sums for \(\int_{0}^{1}k^{-1}u^{1/k-1}\,du=1\). Dominated convergence passes the limit inside.

The problem is the case \(k=2025\) and \(f(t)=2025\sin t\cos t\), so the limit equals

\[
\int_{0}^{1}2025\sin t\cos t\,dt=\frac{2025}{2}\sin^{2}1.
\]

## Final answer

\[
\dfrac{2025}{2}\sin^{2}1.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{1}2025\sin t\cos t\,dt=\frac{2025}{2}\sin^{2}1\).
