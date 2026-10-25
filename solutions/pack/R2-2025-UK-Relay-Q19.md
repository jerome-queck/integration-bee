# R2-2025-UK-Relay-Q19

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 19)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 19)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\lim_{n\to\infty}n\int_{0}^{1}\frac{1+x^{3}}{n+x+x^{3}+x^{5}}\,dx.
\]

## Solution

On \([0,1]\) the fraction without the outer factor of \(n\) is at most \((1+x^{3})/n\), so the integrand is dominated by the integrable function \(1+x^{3}\). Pointwise,
\[
\frac{n(1+x^{3})}{n+x+x^{3}+x^{5}}\to 1+x^{3}.
\]
Dominated convergence gives
\[
\int_{0}^{1}(1+x^{3})\,dx=\Bigl[x+\frac{x^{4}}{4}\Bigr]_{0}^{1}=\frac54.
\]

## Final answer

\[
\dfrac{5}{4}.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{1}(1+x^{3})\,dx=5/4\).
