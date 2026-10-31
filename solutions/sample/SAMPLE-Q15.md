# SAMPLE-Q15

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 15)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 15)
- Catalog row `SAMPLE-Q15` is `verify: sympy` on the corrected antiderivative. The printed final has the wrong sign. That correction is authored+verified.

## Problem

\[
\int \frac{dx}{x^3+1}.
\]

## Solution

The factor \(\log(x+1)\) in the real antiderivative is \(\log|x+1|\). The quadratic \(x^2-x+1\) stays positive. The solutions PDF factors \(x^3+1=(x+1)(x^2-x+1)\) and finds

\[
\frac{1}{x^3+1}=\frac{1}{3(x+1)}+\frac{2-x}{3(x^2-x+1)}.
\]

It then splits the second numerator against the derivative \(2x-1\):

\[
\int \frac{dx}{x^3+1}=\frac13\ln(x+1)-\frac16\int\frac{2x-1}{x^2-x+1}\,dx+\frac12\int\frac{dx}{(x-1/2)^2+3/4}.
\]

The last integral is a positive arctangent. Completing it gives

\[
\frac13\ln(x+1)-\frac16\ln(x^2-x+1)+\frac{1}{\sqrt{3}}\arctan\left(\frac{2x-1}{\sqrt{3}}\right)+C.
\]

The last displayed line of that PDF, and the answers PDF, put a minus sign in front of the arctan term by folding it into the \(-\frac16\) parentheses. Differentiating that printed expression does not recover \(1/(x^3+1)\).

## Final answer

\[
\frac13\ln(x+1)-\frac16\ln(x^2-x+1)+\frac{1}{\sqrt{3}}\arctan\left(\frac{2x-1}{\sqrt{3}}\right)+C.
\]

## SymPy self-check

`solutions/sample_self_check.py` differentiates the graded antiderivative through the pack gate and recovers \(1/(x^3+1)\). The same call rejects the printed final.
