# SAMPLE-Q08

- Problem: `sources/Integration_Competition_Sample_problems.pdf` (question 8)
- Printed answer: `sources/Integration_bee_sample_problems_answers.pdf`
- Worked source: `sources/UK_University_integration_bee_sample_problems_solutions.pdf` (question 8)
- Catalog row `SAMPLE-Q08` stays `verify: manual`. The pack gate does not close the full integral.

## Problem

\[
\int_0^\infty \frac{x^{s-1}}{e^x-1}\,dx.
\]

## Solution

The solutions PDF divides numerator and denominator by \(e^x\) and expands the geometric series:

\[
\frac{x^{s-1}}{e^x-1}=\sum_{k\ge 1} x^{s-1}e^{-kx}.
\]

The substitution \(u=kx\) on each term produces

\[
\int_0^\infty x^{s-1}e^{-kx}\,dx=\frac{1}{k^s}\int_0^\infty u^{s-1}e^{-u}\,du=\frac{\Gamma(s)}{k^s}.
\]

Summing over \(k\) gives \(\Gamma(s)\zeta(s)\).

## Final answer

\[
\Gamma(s)\zeta(s).
\]

## SymPy self-check

`solutions/sample_self_check.py` runs `check_q08`. For positive \(s\) and \(k\), SymPy evaluates \(\int_0^\infty x^{s-1}e^{-kx}\,dx\) as \(\Gamma(s)/k^s\).
