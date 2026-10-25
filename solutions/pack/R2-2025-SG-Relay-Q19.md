# R2-2025-SG-Relay-Q19

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 19). The same limit is relay 19 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 19)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\lim_{n\to\infty}n\int_{0}^{1}\frac{1+x^{3}}{n+x+x^{3}+x^{5}}\,dx.
\]

## Solution

On \([0,1]\) the integrand is dominated by \(1+x^{3}\) and converges pointwise to \(1+x^{3}\). The limit is
\[
\int_{0}^{1}(1+x^{3})\,dx=\frac54.
\]
The UK mark scheme prints \(5/4\) for this limit.

## Final answer

\[
\dfrac{5}{4}.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{1}(1+x^{3})\,dx=5/4\).
