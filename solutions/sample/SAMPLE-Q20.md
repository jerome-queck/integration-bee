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
\int \frac{u^3+u^2}{u^2+1}\,du=\int\Bigl(u+1-\frac{u+1}{u^2+1}\Bigr)\,du=\int\Bigl(u+1-\frac{u}{u^2+1}-\frac{1}{u^2+1}\Bigr)\,du.
\]

The printed step that drops only \(1/(u^2+1)\) omits \(u/(u^2+1)\). Integrating the corrected quotient gives \(u^2/2+u-\frac12\log(u^2+1)-\arctan u\). With \(u=e^x\) this matches the catalog antiderivative up to a constant. The printed secant form equals that antiderivative plus \(1/2\).

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
