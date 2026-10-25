# SAMPLE-Q13

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 13)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 13)
- Catalog row `SAMPLE-Q13` is `verify: sympy`.

## Problem

\[
\int \frac{dx}{1+e^x}.
\]

## Solution

The solutions PDF divides numerator and denominator by \(e^x\):

\[
\int \frac{dx}{1+e^x}=\int \frac{e^{-x}}{1+e^{-x}}\,dx=-\ln(1+e^{-x})+C.
\]

## Final answer

\[
-\ln(1+e^{-x})+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the stored antiderivative through the pack gate and recovers \(1/(1+e^x)\).
