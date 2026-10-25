# SAMPLE-Q02

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 2)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 2)
- Catalog row `SAMPLE-Q02` is `verify: sympy`.

## Problem

\[
\int_0^\infty \frac{\sin x}{x}\,dx.
\]

## Solution

The solutions PDF introduces

\[
I(t)=\int_0^\infty e^{-tx}\frac{\sin x}{x}\,dx
\]

and differentiates under the integral sign:

\[
I'(t)=-\int_0^\infty e^{-tx}\sin x\,dx=-\frac{1}{t^2+1}.
\]

Integrating gives \(I(t)=C-\arctan t\). As \(t\to\infty\), \(I(t)\to 0\), so \(C=\pi/2\). The required value is \(I(0)=\pi/2\).

## Final answer

\[
\pi/2.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs the stored integrand \(\sin x/x\) on \([0,\infty)\) through the pack gate and gets \(\pi/2\).
