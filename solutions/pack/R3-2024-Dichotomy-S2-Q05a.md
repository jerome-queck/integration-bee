# R3-2024-Dichotomy-S2-Q05a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 5a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 5a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 5a)
- The catalog row is not changed.

## Problem

\[\int_{0}^{1}\ln\left(1+\sqrt{1+\left(\frac{x^{4}-1}{2x^{2}}\right)^{2}}\right)dx.\]

## Solution

The solutions PDF simplifies the expression under the logarithm to \(\tfrac12(x+1/x)^{2}\). The integrand is therefore \(-\ln 2+2\ln(x+1/x)\). Integration by parts gives \(\int_{0}^{1}\ln(x+1/x)\,dx=\ln 2-1+\pi/2\), and the definite integral is \(\ln 2+\pi-2\).

## Final answer

\[\ln 2+\pi-2.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q05a`. SymPy checks that the squared radicand is \(((x^{4}+1)/(2x^{2}))^{2}\) and evaluates the logarithm integral.
