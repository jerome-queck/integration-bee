# R3-2024-Dichotomy-S2-Q01b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 1b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 1b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 1b)
- The catalog row is not changed.

## Problem

\[\int_{-1}^{1}\frac{\ln(x^{4}+1)}{x^{3}}\,dx.\]

## Solution

The integrand is odd. Near the origin, \(\ln(1+x^{4})\sim x^{4}\), so the singularity is integrable. The solutions PDF concludes that the integral is \(0\).

## Final answer

\[0.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q01b`. SymPy simplifies \(f(x)+f(-x)\) to \(0\).
