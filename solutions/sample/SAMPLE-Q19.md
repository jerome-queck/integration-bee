# SAMPLE-Q19

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 19)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 19)
- Catalog row `SAMPLE-Q19` stays `verify: manual`. The printed antiderivative matches the integrand at sample points. The pack gate does not close that derivative.

## Problem

\[
\int x\sqrt{\frac{1-x^2}{1+x^2}}\,dx.
\]

## Solution

The solutions PDF sets \(u=x^2\), then \(u=\cos 2v\). Using \(1-u=2\sin^2 v\) and \(1+u=2\cos^2 v\), the integral reduces to

\[
\frac12\bigl(\sin 2v-2v\bigr)+C=\frac12\bigl(\sin(\arccos(x^2))-\arccos(x^2)\bigr)+C.
\]

The PDF notes that another method can produce an equivalent expression that looks different.

## Final answer

\[
\frac12\bigl(\sin(\arccos(x^2))-\arccos(x^2)\bigr)+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs `check_q19`. At \(x=1/5\), \(1/2\), and \(4/5\), the derivative of the printed answer matches the integrand within \(10^{-9}\). The pack gate still returns false for that antiderivative, so the catalog row stays manual.
