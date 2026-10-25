# R3-2024-Dichotomy-S2-Q06b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 6b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 6b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 6b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{\cos x-\cos^{2}x}{x^{2}}\,dx.\]

## Solution

The same split, without the logarithm, is \[\int_{0}^{\infty}\frac{\sin^{2}x}{x^{2}}\,dx-\int_{0}^{\infty}\frac{2\sin^{2}(x/2)}{x^{2}}\,dx.\]

The substitution \(x=2u\) identifies the two integrals, so the value is \(0\).

## Final answer

\[0.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q06b`. SymPy checks that \(x=2u\) carries \(2\sin^{2}(x/2)/x^{2}\) onto \(\sin^{2}u/u^{2}\).
