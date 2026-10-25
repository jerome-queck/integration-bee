# SAMPLE-Q04

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 4)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 4)
- Catalog row `SAMPLE-Q04` is `verify: sympy`.

## Problem

\[
\int_0^\infty \frac{\ln x}{x^2+1}\,dx.
\]

## Solution

The solutions PDF substitutes \(u=1/x\). The limits reverse and

\[
I=\int_\infty^0 \frac{\ln(1/u)}{1+1/u^2}\left(-\frac{du}{u^2}\right)=-\int_0^\infty \frac{\ln u}{1+u^2}\,du=-I.
\]

Hence \(I=0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs the stored integrand on \([0,\infty)\) through the pack gate and gets \(0\).
