# SAMPLE-Q03

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 3)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 3)
- Catalog row `SAMPLE-Q03` is `verify: sympy`.

## Problem

\[
\int_0^{\pi/2}\frac{\sqrt{\sin x}}{\sqrt{\sin x}+\sqrt{\cos x}}\,dx.
\]

## Solution

The solutions PDF uses the reflection \(u=\pi/2-x\). The integral equals

\[
\int_0^{\pi/2}\frac{\sqrt{\cos x}}{\sqrt{\sin x}+\sqrt{\cos x}}\,dx.
\]

Adding the two copies produces

\[
2I=\int_0^{\pi/2} 1\,dx=\pi/2,
\]

so \(I=\pi/4\).

## Final answer

\[
\pi/4.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs the stored integrand on \([0,\pi/2]\) through the pack gate and gets \(\pi/4\).
