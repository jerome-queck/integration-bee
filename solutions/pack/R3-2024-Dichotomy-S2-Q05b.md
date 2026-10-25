# R3-2024-Dichotomy-S2-Q05b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 5b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 5b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 5b)
- The catalog row is not changed.

## Problem

\[\int_{0}^{\infty}\exp\left(-1-\sqrt{1+\left(\frac{x^{4}-1}{2x^{2}}\right)^{2}}\right)dx.\]

## Solution

The same simplification makes the exponent \(-\tfrac12(x+1/x)^{2}\). That square is \((x-1/x)^{2}+4\), so the integrand is \(e^{-2}\exp\bigl(-\tfrac12(x-1/x)^{2}\bigr)\). The solutions PDF applies Glasser's master theorem and obtains \(\sqrt{2\pi}/(2e^{2})\).

## Final answer

\[\dfrac{\sqrt{2\pi}}{2e^{2}}.\]

## SymPy self-check

`solutions/self_check.py` runs `check_r3_2024_dichotomy_s2_q05b`. SymPy checks the reduction of the exponent and the Gaussian factor \(e^{-2}\sqrt{2\pi}/2\). A quadrature of \(\exp\bigl(-\tfrac12(x+1/x)^{2}\bigr)\) matches the printed value within \(10^{-12}\).
