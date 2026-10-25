# SAMPLE-Q01

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 1)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 1)
- Catalog row `SAMPLE-Q01` is `verify: sympy`.

## Problem

\[
\int_0^1 \frac{x^5-1}{\ln x}\,dx.
\]

## Solution

The solutions PDF differentiates under the integral sign. Set

\[
I(t)=\int_0^1 \frac{x^t-1}{\ln x}\,dx.
\]

Then

\[
I'(t)=\int_0^1 x^t\,dx=\frac{1}{t+1},
\]

so \(I(t)=\ln(t+1)+C\). The case \(t=0\) is \(I(0)=0\), hence \(C=0\) and \(I(5)=\ln 6\).

The same PDF also writes the integral as a double integral and swaps the order:

\[
\int_0^1\int_0^5 x^y\,dy\,dx=\int_0^5 \frac{dy}{y+1}=\ln 6.
\]

## Final answer

\[
\ln 6.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs the stored integrand \((x^5-1)/\ln x\) on \([0,1]\) through the pack gate and gets \(\ln 6\).
