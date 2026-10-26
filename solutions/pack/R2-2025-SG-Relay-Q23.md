# R2-2025-SG-Relay-Q23

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (page 6, relay 23). The same integral is relay 5 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (page 3, UK relay 5)
- Worked source: derived in this note.
- The transcript retains the source assumptions that both parameters are positive integers.

## Problem

\[
\int_{0}^{1}\frac{\bigl(\ln(1-x^{n})\bigr)^{m}}{x}\,dx
\]
for positive integers \(m\) and \(n\).

## Solution

The substitutions \(u=x^{n}\) and \(s=-\ln(1-e^{-t})\) turn the integral into
\[
\frac{(-1)^{m}}{n}\sum_{k\ge 1}\int_{0}^{\infty}s^{m}e^{-ks}\,ds=\frac{(-1)^{m}m!}{n}\,\zeta(m+1).
\]
The UK mark scheme prints that value for this integral.

## Final answer

\[
\dfrac{(-1)^{m}\,m!}{n}\,\zeta(m+1).
\]

## SymPy self-check

For a positive integer \(m\) and \(k\ge 1\), SymPy evaluates \(\int_{0}^{\infty}s^{m}e^{-ks}\,ds=m!/k^{m+1}\), and sums the series as \(m!\,\zeta(m+1)\).

The same checked substitution, geometric-series, and Gamma certificate as UK relay 5 proves this transcript. It rejects parameters without the printed positive-integer assumptions.
