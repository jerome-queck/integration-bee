# R3-2024-Dichotomy-S1-Q07b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_1_2024_Round_3_UK_University_Integration_Bee_(4).pdf` (problem 7b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 1, problem 7b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 2/Segment 1, problem 7b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\frac{1}{(1+x^{2})\bigl(1+\arctan x\operatorname{arccot} x\bigr)}\,dx.\]

## Solution

With \(u=\arctan x\) the integral becomes \(\int_{0}^{\pi/4} du/(1+(\pi/2)u-u^{2})\). Completing the square, the solutions PDF evaluates it as \[\frac{4}{\sqrt{16+\pi^{2}}}\operatorname{artanh}\frac{\pi}{\sqrt{16+\pi^{2}}}.\]

The answers sheet also prints the logarithmic form \[\frac{2}{\sqrt{16+\pi^{2}}}\ln\frac{\sqrt{16+\pi^{2}}+\pi}{\sqrt{16+\pi^{2}}-\pi}.\]

## Final answer

\[\dfrac{4}{\sqrt{16+\pi^{2}}}\operatorname{artanh}\dfrac{\pi}{\sqrt{16+\pi^{2}}}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s1_q07b`. SymPy checks the completed square, the logarithm for \(\operatorname{artanh}\), and that the two printed arguments agree.
