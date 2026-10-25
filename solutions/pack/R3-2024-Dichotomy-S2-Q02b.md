# R3-2024-Dichotomy-S2-Q02b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 2b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 2b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 2b)
- The catalog row is not changed.

## Problem

\[\int\frac{1}{(\sqrt{x}+1)x+2\sqrt{x}}\,dx.\]

## Solution

The same substitution \(y=\sqrt{x}\) produces \[\int\frac{2}{y^{2}+y+2}\,dy=\int\frac{2}{(y+1/2)^{2}+7/4}\,dy=\frac{4}{\sqrt{7}}\arctan\frac{2y+1}{\sqrt{7}}+C.\]

## Final answer

\[\dfrac{4}{\sqrt{7}}\arctan\dfrac{2\sqrt{x}+1}{\sqrt{7}}+C.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q02b`. SymPy differentiates the arctangent antiderivative back to the substituted integrand.
