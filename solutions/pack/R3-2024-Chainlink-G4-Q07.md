# R3-2024-Chainlink-G4-Q07

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 7)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 7)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 7)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[
\lim_{n\to\infty}\int_{0}^{1/2}f_{n}(x)\,dx,\quad f_{1}(x)=2x-2x^{2},\quad f_{n}=f_{1}^{\circ n}.
\]

## Solution

On \([0,1/2]\) the map \(f_{1}(x)=2x(1-x)\) is invertible. The solutions PDF takes the branch of the inverse that stays in the interval,

\[
g(y)=\frac{1-\sqrt{1-2y}}{2}.
\]

The endpoints \(0\) and \(1/2\) are fixed. Integration by parts with \(x=g_{n}(y)\) gives

\[
\int_{0}^{1/2}f_{n}(x)\,dx=\frac14-\int_{0}^{1/2}g_{n}(y)\,dy.
\]

For \(0\le y<1/2\), the iterates \(g_{n}(y)\) decrease to the fixed point \(0\). At \(y=1/2\) they remain \(1/2\). This single endpoint does not affect the integral, so dominated convergence gives the limit \(1/4\).

## Final answer

\[
\dfrac{1}{4}.
\]

## SymPy self-check

The transcript uses the exact nth iterate \(f_n(x)=(1-(1-2x)^{2^n})/2\), inside the original limit of an integral. The gate checks the first iterate and the conjugacy \(1-2f_1(x)=(1-2x)^2\), proving the formula by induction. Substitution \(z=1-2x\) gives the exact finite-n integral \(1/4-1/[4(2^n+1)]\), whose checked limit is \(1/4\).
