# SAMPLE-Q11

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 11)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 11)
- Catalog row `SAMPLE-Q11` is `verify: sympy`.

## Problem

\[
\int \frac{dx}{1+\tan x}.
\]

## Solution

The solutions PDF multiplies numerator and denominator by \(\cos x\) and sets

\[
I=\int\frac{\cos x}{\sin x+\cos x}\,dx,\qquad J=\int\frac{\sin x}{\sin x+\cos x}\,dx.
\]

Then \(I+J=x+C\) and \(I-J=\ln(\sin x+\cos x)+C\), so

\[
I=\frac12\bigl(x+\ln|\sin x+\cos x|\bigr)+C.
\]

The answers PDF prints the logarithm without the absolute value. That expression is non-real on intervals where \(\sin x+\cos x<0\), while the integrand is real. The catalog stores the absolute value.

## Final answer

\[
\frac12\bigl(x+\ln|\sin x+\cos x|\bigr)+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the stored antiderivative through the pack gate and recovers \(1/(1+\tan x)\).
