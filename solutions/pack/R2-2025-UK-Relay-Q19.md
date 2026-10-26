# R2-2025-UK-Relay-Q19

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (PDF page 5, relay 19)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (PDF page 4, relay 19)
- Worked source: derived in this note; the mark scheme prints the final value.
- The SymPy transcript retains the finite rational integrand under its limit.

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

The gate also checks the error identity, with \(P(x)=x+x^3+x^5\):
\[
0\le(1+x^3)-\frac{n(1+x^3)}{n+P(x)}
=\frac{(1+x^3)P(x)}{n+P(x)}\le\frac6n.
\]
On \([0,1]\), \(0\le P(x)\le3\) and \(1\le1+x^3\le2\); exact polynomial factorizations certify these bounds. Thus the error tends uniformly to zero, justifying the stored exchange of the outer limit with the integral.
