# R3-2024-Chainlink-G4-Q07

- Problem: `sources/past/r3/2024/Chainlink_Game_4_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 7)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 4, problem 7)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 4, problem 7)
- The catalog row is not changed.

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

The iterates \(g_{n}(y)\) decrease to the fixed point \(0\). Dominated convergence passes the limit inside, and the integral tends to \(1/4\).

## Final answer

\[
\dfrac{1}{4}.
\]

## SymPy self-check

SymPy checks \(f_{1}(g(x))=x\), together with \(g(0)=0\) and \(g(1/2)=1/2\). The boundary term in the integration by parts is \(\frac12\cdot\frac12=1/4\).
