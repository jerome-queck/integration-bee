# SAMPLE-Q20

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 20)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 20)
- Catalog row `SAMPLE-Q20` is `verify: sympy`.

## Problem

\[
\int \frac{e^{2x}+e^{3x}}{e^x+e^{-x}}\,dx.
\]

## Solution

The solutions PDF factors \(e^x\) from the numerator and sets \(u=e^x\):

\[
\int \frac{u^3+u^2}{u^2+1}\,du=\int u\,du+\int 1\,du-\int \frac{du}{u^2+1}.
\]

The remaining rational piece is handled with \(u=\tan v\). The printed antiderivative is

\[
e^x-\arctan(e^x)+\frac12\sec^2(\arctan(e^x))+\ln\bigl|\cos(\arctan(e^x))\bigr|+C.
\]

## Final answer

\[
e^x-\arctan(e^x)+\frac12\sec^2\bigl(\arctan(e^x)\bigr)+\ln\bigl|\cos(\arctan(e^x))\bigr|+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the stored antiderivative through the pack gate and recovers the integrand.
