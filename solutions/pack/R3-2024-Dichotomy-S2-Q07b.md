# R3-2024-Dichotomy-S2-Q07b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 7b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 7b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 7b)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[\lim_{n\to\infty}\int_{1}^{n}\ln\left(1+\frac{2}{n}+\frac{1}{\sqrt{nx}}\right)dx.\]

## Solution

The same antiderivative, now with square root and \(a_{n,2}=1+2/n\), has boundary term \(n\ln(1+2/n+1/n)\), which tends to \(3\). The solutions PDF evaluates the remaining integral by partial fractions; its limit is \(1\). The sum is \(4\).

## Final answer

\[4.\]

## SymPy self-check

The gate retains the complete `Limit(Integral(...),n,oo)`. Set \(u_n(x)=2/n+1/\sqrt{nx}\). Derivative checks prove \(u-u^2/2\le\log(1+u)\le u\) for nonnegative u. It then integrates both bounds exactly: \(\int_1^n u_n\to4\), while \(\int_1^n u_n^2/2\to0\). The squeeze theorem gives the printed value 4 without relying on cancellation in an improper antiderivative.
