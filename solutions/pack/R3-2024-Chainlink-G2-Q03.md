# R3-2024-Chainlink-G2-Q03

- Problem: `sources/past/r3/2024/Chainlink_Game_2_2024_Round_3_UK_University_Integration_Bee_(5).pdf` (problem 3)
- Printed answer: `sources/past/r3/2024/Chainlink_Answers_2024_Round_3_UK_University_Integration_Bee_(7).pdf` (Game 2, problem 3)
- Worked source: `sources/past/r3/2024/Chainlink_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Game 2, problem 3)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[
\int_{0}^{\pi/2}\sec x\csc x\sin(\tan x)\,dx.
\]

## Solution

The substitution \(u=\tan x\) runs from \(0\) to \(\infty\), with \(dx=du/(1+u^{2})\), \(\sec x=\sqrt{1+u^{2}}\) and \(\csc x=\sqrt{1+u^{2}}/u\). The rational factors cancel and the integral becomes

\[
\int_{0}^{\infty}\frac{\sin u}{u}\,du=\frac{\pi}{2}.
\]

## Final answer

\[
\dfrac{\pi}{2}.
\]

## SymPy self-check

The gate checks the tangent substitution and both improper endpoints. SymPy evaluates the resulting Dirichlet integral exactly.
