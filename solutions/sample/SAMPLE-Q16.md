# SAMPLE-Q16

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 16)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 16)
- Catalog row `SAMPLE-Q16` is `verify: sympy`.

## Problem

\[
\int \frac{dx}{2+\sin x}.
\]

## Solution

The solutions PDF uses the Weierstrass substitution \(t=\tan(x/2)\), so \(\sin x=2t/(1+t^2)\) and \(dx=2\,dt/(1+t^2)\). The integral becomes

\[
\int \frac{dt}{(t+1/2)^2+3/4}=\frac{2}{\sqrt{3}}\arctan\left(\frac{2t+1}{\sqrt{3}}\right)+C.
\]

Restoring \(t\) gives the printed answer.

## Final answer

\[
\frac{2}{\sqrt{3}}\arctan\left(\frac{2\tan(x/2)+1}{\sqrt{3}}\right)+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the stored antiderivative through the pack gate and recovers \(1/(2+\sin x)\).
