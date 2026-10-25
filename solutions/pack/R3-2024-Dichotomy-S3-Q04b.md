# R3-2024-Dichotomy-S3-Q04b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 4b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 4b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 4b)
- The catalog row is not changed.

## Problem

\[\int_{1}^{\infty}\frac{\arctan(1/x)}{x^{2}}\,dx.\]

## Solution

The substitution \(y=1/x\) turns the integral into \(\int_{0}^{1}\arctan y\,dy\). Integration by parts gives \[\bigl[y\arctan y\bigr]_{0}^{1}-\int_{0}^{1}\frac{y}{1+y^{2}}\,dy=\frac{\pi}{4}-\frac{\ln 2}{2}.\]

## Final answer

\[\dfrac{\pi}{4}-\dfrac{\ln 2}{2}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q04b`. SymPy evaluates the integral as \(\pi/4-(\ln 2)/2\).
