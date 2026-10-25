# SAMPLE-Q18

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 18)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 18)
- Catalog row `SAMPLE-Q18` is `verify: sympy`.

## Problem

\[
\int \frac{dx}{1-\sin x}.
\]

## Solution

The solutions PDF multiplies numerator and denominator by \(1+\sin x\):

\[
\int \frac{1+\sin x}{\cos^2 x}\,dx=\int \sec^2 x\,dx+\int \sec x\tan x\,dx=\sec x+\tan x+C.
\]

## Final answer

\[
\sec x+\tan x+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the stored antiderivative through the pack gate and recovers \(1/(1-\sin x)\).
