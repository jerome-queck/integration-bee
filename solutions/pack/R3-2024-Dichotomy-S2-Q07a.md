# R3-2024-Dichotomy-S2-Q07a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 7a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 7a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 7a)
- The catalog row is not changed.

## Problem

\[\lim_{n\to\infty}\int_{1}^{n}\ln\left(1+\frac{e}{n}+\frac{1}{\sqrt[e]{nx}}\right)dx.\]

## Solution

The solutions PDF treats \(\int_{1}^{n}\ln\bigl(a_{n,p}+1/\sqrt[p]{nx}\bigr)\,dx\) by the substitution \(x=1/(n y^{p})\). For \(p=e\) and \(a_{n,e}=1+e/n\), the boundary term \(n\ln\bigl(1+e/n+n^{-2/e}\bigr)\) tends to \(+\infty\), and the remaining integral is positive. The limit is \(+\infty\). The answers sheet also accepts \(\infty\).

## Final answer

\[+\infty.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q07a`. SymPy takes the limit of \(n\ln\bigl(1+e/n+n^{-2/e}\bigr)\) and gets \(+\infty\).
