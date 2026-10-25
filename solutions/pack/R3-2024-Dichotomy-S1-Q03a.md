# R3-2024-Dichotomy-S1-Q03a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 3a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 3a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 3a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{1}{1+e^{\sqrt{x}}}\,dx.\]

## Solution

The solutions PDF sets \(u=\sqrt{x}\). Then \[\int_{0}^{\infty}\frac{2u}{1+e^{u}}\,du=2\sum_{n\ge 0}(-1)^{n}\int_{0}^{\infty}u e^{-(n+1)u}\,du=2\sum_{n\ge 0}\frac{(-1)^{n}}{(n+1)^{2}}=\frac{\pi^{2}}{6}.\]

## Final answer

\[\dfrac{\pi^{2}}{6}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q03a`. SymPy sums \(2\sum_{n\ge 0}(-1)^{n}/(n+1)^{2}\) to \(\pi^{2}/6\).
