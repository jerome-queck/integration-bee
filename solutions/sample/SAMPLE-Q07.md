# SAMPLE-Q07

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 7)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 7)
- Catalog row `SAMPLE-Q07` is `verify: sympy`. The graded value is \(\Gamma(n)\). The answers PDF also records \(\Gamma(n)=(n-1)!\) for positive integers \(n\).

## Problem

\[
\int_0^\infty x^{n-1}e^{-x}\,dx,\qquad n\in\mathbb{Z}^+.
\]

## Solution

The solutions PDF integrates by parts. With \(I_n=\int_0^\infty x^{n-1}e^{-x}\,dx\),

\[
I_n=(n-1)I_{n-1}.
\]

The base \(I_1=1\) gives \(I_n=(n-1)!\). The same integral is \(\Gamma(n)\), and the recurrence is \(\Gamma(n)=(n-1)\Gamma(n-1)\) for \(n>1\).

## Final answer

\[
\Gamma(n)=(n-1)!.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs the stored integrand on \([0,\infty)\) through the pack gate and gets \(\Gamma(n)\). A submitted \((n-1)!\) matches that value.
