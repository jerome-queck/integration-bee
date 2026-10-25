# SAMPLE-Q10

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 10)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 10)
- Catalog row `SAMPLE-Q10` is `verify: sympy`.

## Problem

\[
\int_{-2}^{2}\left(x^3\cos\frac{x}{2}+\frac12\right)\sqrt{4-x^2}\,dx.
\]

## Solution

The solutions PDF separates the integrand. The factor \(x^3\cos(x/2)\sqrt{4-x^2}\) is odd, so its integral on \([-2,2]\) is \(0\). The remaining piece is

\[
\int_{-2}^{2}\frac12\sqrt{4-x^2}\,dx.
\]

The graph of \(y=\sqrt{4-x^2}\) is the upper half of the circle \(x^2+y^2=4\), a semicircle of radius \(2\) and area \(2\pi\). Half of that area is \(\pi\).

## Final answer

\[
\pi.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs the stored integrand on \([-2,2]\) through the pack gate and gets \(\pi\).
