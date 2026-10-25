# R3-2024-Dichotomy-S2-Q01a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 1a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 1a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 1a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\frac{\ln(x^{4}+1)}{x^{3}}\,dx.\]

## Solution

Integration by parts gives \[\left[-\frac{\ln(x^{4}+1)}{2x^{2}}\right]_{0}^{1}+\int_{0}^{1}\frac{2x}{x^{4}+1}\,dx=-\frac{\ln 2}{2}+\arctan(1)=\frac{\pi}{4}-\frac{\ln 2}{2}.\]

The boundary term at \(0\) vanishes.

## Final answer

\[\dfrac{\pi}{4}-\dfrac{\ln 2}{2}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q01a`. SymPy differentiates \(-\ln(x^{4}+1)/(2x^{2})\) and evaluates \(\int_{0}^{1}2x/(x^{4}+1)\,dx=\pi/4\).
