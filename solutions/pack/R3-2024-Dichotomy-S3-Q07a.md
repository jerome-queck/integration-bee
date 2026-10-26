# R3-2024-Dichotomy-S3-Q07a

- Problem: `sources/past/r3/2024/Dichotomy_Segment_3_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (problem 7a)
- Printed answer: `sources/past/r3/2024/Dichotomy_answers_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Segment 3, problem 7a)
- Worked source: `sources/past/r3/2024/Dichotomy_Solutions_2024_Round_3_UK_University_Integration_Bee_(2).pdf` (Set 3/Segment 3, problem 7a)
- Catalog verification: `sympy`. The exact certificate is in `verify/pack_handoff_b.py`.

## Problem

\[\int_{0}^{1}\sqrt{\frac{x}{1-x}}\ln\frac{x}{1-x}\,dx.\]

## Solution

The substitution \(x=\sin^{2}u\) produces \(4\int_{0}^{\pi/2}\sin^{2}u\ln(\tan u)\,du\). King's rule replaces this by \(-4\int_{0}^{\pi/2}\cos^{2}u\ln(\tan u)\,du\). Averaging gives \(-2\int_{0}^{\pi/2}\cos(2u)\ln(\tan u)\,du\). Integration by parts, with vanishing endpoint terms, leaves \(\pi\).

## Final answer

\[\pi.\]

## SymPy self-check

The gate checks \(x=t^2/(1+t^2)\), averages the transformed integral with its reciprocal, and differentiates the integration-by-parts boundary term. Both boundary limits vanish. The remaining integral is evaluated symbolically.
