# R3-2024-Dichotomy-S2-Q05b

- Problem: `sources/past/r3/2024/Dichotomy_Segment_2_2024_Round_3_UK_University_Integration_Bee_(3).pdf` (problem 5b)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 2, problem 5b)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 1/Segment 2, problem 5b)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[\int_{0}^{\infty}\exp\left(-1-\sqrt{1+\left(\frac{x^{4}-1}{2x^{2}}\right)^{2}}\right)dx.\]

## Solution

The same simplification makes the exponent \(-\tfrac12(x+1/x)^{2}\). That square is \((x-1/x)^{2}+4\), so the integrand is \(e^{-2}\exp\bigl(-\tfrac12(x-1/x)^{2}\bigr)\). The solutions PDF applies Glasser's master theorem and obtains \(\sqrt{2\pi}/(2e^{2})\).

## Final answer

\[\dfrac{\sqrt{2\pi}}{2e^{2}}.\]

## SymPy self-check

The gate identifies the positive radical, checks its inversion symmetry, and uses \(y=x-1/x\). Averaging supplies half the Jacobian. SymPy evaluates the resulting Gaussian integral exactly, without numerical quadrature.
