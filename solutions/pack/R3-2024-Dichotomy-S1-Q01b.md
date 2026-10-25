# R3-2024-Dichotomy-S1-Q01b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 1b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 1b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 1b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\sqrt{2}}\sqrt{4-x^{2}}\,dx.\]

## Solution

The same semicircle splits into a sector and a triangle. The solutions PDF records \[\int_{0}^{a}\sqrt{4-x^{2}}\,dx=2\arcsin\frac{a}{2}+\frac{a\sqrt{4-a^{2}}}{2}.\]

At \(a=\sqrt{2}\) this is \(\pi/2+1\).

## Final answer

\[\dfrac{\pi}{2}+1.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q01b`. SymPy simplifies the sector-and-triangle formula at \(a=\sqrt{2}\) to \(\pi/2+1\).
