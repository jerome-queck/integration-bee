# R3-2024-Dichotomy-S3-Q01a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 1a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 1a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 1a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\frac{x^{4}+1}{x^{6}+1}\,dx.\]

## Solution

The solutions PDF uses \(x^{6}+1=(x^{2}+1)(x^{4}-x^{2}+1)\) and rewrites the integrand so that \[\frac{x^{4}+1}{x^{6}+1}=\frac{1}{1+x^{2}}+\frac{x^{2}}{1+x^{6}}.\]

An antiderivative is \(\arctan x+\tfrac13\arctan(x^{3})\). From \(0\) to \(1\) the value is \(\pi/3\).

## Final answer

\[\dfrac{\pi}{3}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q01a`. SymPy differentiates \(\arctan x+\tfrac13\arctan(x^{3})\) back to the integrand and evaluates it from \(0\) to \(1\).
