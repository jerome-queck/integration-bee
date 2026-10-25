# R3-2024-Dichotomy-S3-Q03b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 3b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 3b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 3b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{x^{1/3}}{1+x^{4}}\,dx.\]

## Solution

The same formula with \(b=4\) gives \[\frac{\pi}{4}\csc\frac{\pi}{3}=\frac{\pi}{2\sqrt{3}}.\]

## Final answer

\[\dfrac{\pi}{2\sqrt{3}}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q03b`. SymPy simplifies \((\pi/4)\csc(\pi/3)\) to \(\pi/(2\sqrt{3})\).
