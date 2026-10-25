# SAMPLE-Q06

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 6)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 6)
- Catalog row `SAMPLE-Q06` is `verify: sympy`.

## Problem

\[
\int_0^1 \frac{\ln(1-x)}{x}\,dx.
\]

## Solution

The solutions PDF expands \(\ln(1-x)=-\sum_{n\ge 1} x^n/n\) and integrates term by term:

\[
\int_0^1 \frac{\ln(1-x)}{x}\,dx=-\sum_{n\ge 1}\frac{1}{n}\int_0^1 x^{n-1}\,dx=-\sum_{n\ge 1}\frac{1}{n^2}=-\frac{\pi^2}{6}.
\]

## Final answer

\[
-\pi^2/6.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs the stored integrand on \([0,1]\) through the pack gate and gets \(-\pi^2/6\).
