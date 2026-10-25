# R3-2024-Dichotomy-S2-Q04a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 4a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 4a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 4a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\frac{1}{\bigl(x+\sqrt{x^{2}+1}\bigr)(1+x^{2})}\,dx.\]

## Solution

Multiplying numerator and denominator by \(\sqrt{x^{2}+1}-x\) uses \(\bigl(x+\sqrt{x^{2}+1}\bigr)\bigl(\sqrt{x^{2}+1}-x\bigr)=1\). The integrand becomes \[\frac{1}{\sqrt{x^{2}+1}}-\frac{x}{x^{2}+1}.\]

The solutions PDF evaluates the improper integral as \(\ln 2\).

## Final answer

\[\ln 2.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q04a`. SymPy checks the rationalized integrand, differentiates \(\operatorname{arsinh} x-\tfrac12\ln(x^{2}+1)\), and evaluates the limit as \(\ln 2\).
