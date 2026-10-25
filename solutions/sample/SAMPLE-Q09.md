# SAMPLE-Q09

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 9)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 9)
- Catalog row `SAMPLE-Q09` stays `verify: manual`. The pack gate does not close the floor integrand.

## Problem

\[
\int_1^\infty \frac{x-\lfloor x\rfloor}{x^4}\,dx.
\]

## Solution

On each interval \(k\le x<k+1\) the floor is \(k\). The solutions PDF splits the integrand as \(x^{-3}-\lfloor x\rfloor x^{-4}\):

\[
\int_1^\infty x^{-3}\,dx=\frac12,
\]

and

\[
\int_1^\infty \frac{\lfloor x\rfloor}{x^4}\,dx=\sum_{k\ge 1}\int_k^{k+1}\frac{k}{x^4}\,dx.
\]

Summing the pieces leaves \(1/2-\zeta(3)/3\).

## Final answer

\[
\frac12-\frac{\zeta(3)}{3}.
\]

## SymPy self-check

`solutions/sample_self_check.py` runs `check_q09`. SymPy sums \(\int_k^{k+1}(x-k)/x^4\,dx\) from \(k=1\) to \(\infty\) and gets \(1/2-\zeta(3)/3\).
