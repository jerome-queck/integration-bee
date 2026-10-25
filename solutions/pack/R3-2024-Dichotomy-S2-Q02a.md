# R3-2024-Dichotomy-S2-Q02a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 2a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 2a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 2a)
- The catalog row is not changed.

## Problem

\[\int\frac{1}{(x+1)\sqrt{x}+2x}\,dx.\]

## Solution

Set \(y=\sqrt{x}\). The solutions PDF obtains \[\int\frac{2}{(y+1)^{2}}\,dy=-\frac{2}{y+1}+C=-\frac{2}{\sqrt{x}+1}+C.\]

## Final answer

\[-\dfrac{2}{\sqrt{x}+1}+C.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q02a`. SymPy simplifies the substituted integrand to \(2/(y+1)^{2}\) and differentiates \(-2/(y+1)\).
