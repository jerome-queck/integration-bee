# SAMPLE-Q14

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 14)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 14)
- Catalog row `SAMPLE-Q14` is `verify: sympy`.

## Problem

\[
\int \frac{dx}{x\bigl(1+\sin^2(\ln x)\bigr)}.
\]

## Solution

The solutions PDF sets \(u=\ln x\), so \(du=dx/x\), and the integral becomes

\[
\int \frac{du}{1+\sin^2 u}=\int \frac{\sec^2 u}{1+2\tan^2 u}\,du.
\]

A further substitution \(v=\tan u\) gives

\[
\int \frac{dv}{1+2v^2}=\frac{1}{\sqrt{2}}\arctan(\sqrt{2}\,v)+C=\frac{1}{\sqrt{2}}\arctan\bigl(\sqrt{2}\tan(\ln x)\bigr)+C.
\]

## Final answer

\[
\frac{1}{\sqrt{2}}\arctan\bigl(\sqrt{2}\tan(\ln x)\bigr)+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the stored antiderivative through the pack gate and recovers the integrand.
