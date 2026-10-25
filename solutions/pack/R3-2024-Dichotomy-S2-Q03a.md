# R3-2024-Dichotomy-S2-Q03a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 3a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 3a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 3a)
- The catalog row is not changed.

## Problem

\[\int\frac{5x^{2}+3x-2}{x^{3}+2x^{2}}\,dx.\]

## Solution

Partial fractions, as written in the solutions PDF, give \[\frac{3}{x+2}+\frac{2}{x}-\frac{1}{x^{2}}.\]

Integrating term by term produces the printed antiderivative.

## Final answer

\[3\ln|x+2|+2\ln|x|+\dfrac{1}{x}+C.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q03a`. SymPy checks the partial-fraction identity and differentiates the printed antiderivative.
