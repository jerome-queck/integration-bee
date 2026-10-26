# R3-2024-Chainlink-G5-Q05

- Problem: `sources/past/r3/2024/Chainlink_Game_5_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 5)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 5, problem 5)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 5, problem 5)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[
\int_{0}^{1}\sqrt{1+(x-1)^{1/3}}\,dx.
\]

## Solution

The solutions PDF inverts \(y=\sqrt{1+(x-1)^{1/3}}\). Then \(x=(y^{2}-1)^{3}+1\), with \(y(0)=0\) and \(y(1)=1\). The area identity for an increasing graph from \((0,0)\) to \((1,1)\) gives

\[
1-\int_{0}^{1}\bigl((y^{2}-1)^{3}+1\bigr)\,dy=1-\int_{0}^{1}(y^{6}-3y^{4}+3y^{2})\,dy=\frac{16}{35}.
\]

## Final answer

\[
\dfrac{16}{35}.
\]

## SymPy self-check

The transcript uses `real_root(x-1,3)`, preserving the printed real cube root. The gate checks the substitution \(x=1-u^3\), its orientation, and the real branch. SymPy evaluates the remaining beta-type integral.
