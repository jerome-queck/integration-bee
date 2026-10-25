# R3-2024-Dichotomy-S3-Q01b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 1b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 1b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 1b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\frac{x^{2}+1}{x^{3}+1}\,dx.\]

## Solution

Partial fractions produce \[\frac13\int_{0}^{1}\left(\frac{2}{x+1}+\frac{x+1}{x^{2}-x+1}\right)dx.\]

The solutions PDF integrates this as \[\frac13\left[2\ln|x+1|+\frac12\ln|x^{2}-x+1|+\sqrt{3}\arctan\frac{2x-1}{\sqrt{3}}\right]_{0}^{1}=\frac13\left(2\ln 2+\frac{\sqrt{3}\,\pi}{3}\right).\]

## Final answer

\[\dfrac13\left(2\ln 2+\dfrac{\sqrt{3}\,\pi}{3}\right).\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q01b`. SymPy differentiates that antiderivative back to \((x^{2}+1)/(x^{3}+1)\) and evaluates the endpoints.
