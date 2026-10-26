# R3-2024-Chainlink-G2-Q08

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 8)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 8)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 8)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

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

The gate retains the limit outside the original integral. With \(t=x^{2025}\), the weight is \(w(t)=t^{1/2025-1}/2025\). For \(h(u)=2025\sin u\cos u\), it computes the mean \(M=\int_0^1h\) and the cell primitive \(H(u)=2025\sin^2u/2-Mu\), checking \(H(0)=H(1)=0\). The resulting periodic primitive is bounded by 2025. Integration by parts above \(\delta\), and direct integration of the singular weight below it, bound the weighted averaging error by \(4050\delta^{1/2025}+4050w(\delta)/n\). Taking \(\delta=1/n\) gives \(4052n^{-1/2025}\to0\). Thus the limit is the checked cell mean \(2025\sin^2(1)/2\).
