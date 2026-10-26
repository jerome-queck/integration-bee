# R2-2025-SG-Relay-Q19

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (PDF page 5, relay 19). The same limit is relay 19 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (PDF page 5).
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (PDF page 4, UK relay 19)
- Worked source: derived in this note.
- The SymPy transcript retains the finite rational integrand under its limit.

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

The gate also checks the error identity, with \(P(x)=x+x^3+x^5\):
\[
0\le(1+x^3)-\frac{n(1+x^3)}{n+P(x)}
=\frac{(1+x^3)P(x)}{n+P(x)}\le\frac6n.
\]
On \([0,1]\), \(0\le P(x)\le3\) and \(1\le1+x^3\le2\); exact polynomial factorizations certify these bounds. Thus the error tends uniformly to zero, justifying the stored exchange of the outer limit with the integral.
