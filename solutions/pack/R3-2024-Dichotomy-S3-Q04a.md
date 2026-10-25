# R3-2024-Dichotomy-S3-Q04a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 4a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 4a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 4a)
- The catalog row is not changed.

## Problem

\[\int_{1}^{\infty}\frac{\arctan(1/x^{2})}{x}\,dx.\]

## Solution

The solutions PDF expands \(\arctan(1/x^{2})\) and integrates term by term: \[\sum_{n\ge 0}\frac{(-1)^{n}}{2n+1}\int_{1}^{\infty}x^{-4n-3}\,dx=\frac12\sum_{n\ge 0}\frac{(-1)^{n}}{(2n+1)^{2}}=\frac{G}{2},\]

where \(G\) is Catalan's constant.

## Final answer

\[\dfrac{G}{2}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s3_q04a`. SymPy checks the term integral \(1/(4n+2)\) and sums the series to Catalan's constant.
