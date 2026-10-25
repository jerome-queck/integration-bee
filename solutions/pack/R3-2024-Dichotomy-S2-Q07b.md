# R3-2024-Dichotomy-S2-Q07b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 7b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 7b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 7b)
- The catalog row is not changed.

## Problem

\[\lim_{n\to\infty}\int_{1}^{n}\ln\left(1+\frac{2}{n}+\frac{1}{\sqrt{nx}}\right)dx.\]

## Solution

The same antiderivative, now with square root and \(a_{n,2}=1+2/n\), has boundary term \(n\ln(1+2/n+1/n)\), which tends to \(3\). The solutions PDF evaluates the remaining integral by partial fractions; its limit is \(1\). The sum is \(4\).

## Final answer

\[4.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q07b`. SymPy evaluates \(\lim n\ln(1+3/n)=3\) and \(\lim 1/(1+2/n)=1\).
