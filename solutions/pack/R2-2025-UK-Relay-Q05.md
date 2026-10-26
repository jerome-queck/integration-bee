# R2-2025-UK-Relay-Q05

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (page 2, relay 5)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (page 3, relay 5)
- Worked source: derived in this note; the mark scheme prints the final value.
- The transcript retains the source assumptions that both parameters are positive integers.

## Problem

\[
\int_{0}^{1}\frac{\bigl(\ln(1-x^{n})\bigr)^{m}}{x}\,dx
\]
for positive integers \(m\) and \(n\).

## Solution

The substitution \(u=x^{n}\) produces a factor \(1/n\):
\[
\frac1n\int_{0}^{1}\frac{(\ln(1-u))^{m}}{u}\,du.
\]
Then \(u=e^{-t}\) gives
\[
\frac1n\int_{0}^{\infty}\bigl(\ln(1-e^{-t})\bigr)^{m}\,dt=\frac{(-1)^{m}}{n}\int_{0}^{\infty}\bigl(-\ln(1-e^{-t})\bigr)^{m}\,dt.
\]
Set \(s=-\ln(1-e^{-t})\), so \(t=-\ln(1-e^{-s})\) and
\[
dt=-\frac{e^{-s}}{1-e^{-s}}\,ds=-\sum_{k\ge 1}e^{-ks}\,ds.
\]
Reversing the limits from \(s=\infty\) to \(s=0\), the integral becomes
\[
\frac{(-1)^{m}}{n}\sum_{k\ge 1}\int_{0}^{\infty}s^{m}e^{-ks}\,ds=\frac{(-1)^{m}}{n}\sum_{k\ge 1}\frac{m!}{k^{m+1}}=\frac{(-1)^{m}m!}{n}\,\zeta(m+1).
\]

## Final answer

\[
\dfrac{(-1)^{m}\,m!}{n}\,\zeta(m+1).
\]

## SymPy self-check

For a positive integer \(m\) and \(k\ge 1\), SymPy evaluates \(\int_{0}^{\infty}s^{m}e^{-ks}\,ds=m!/k^{m+1}\), and sums that series as \(m!\,\zeta(m+1)\).

The gate checks both substitutions, the finite geometric sum and its limit, the Gamma moment, and the zeta sum. After removing the constant sign \((-1)^m\), Tonelli applies to nonnegative terms; \(m\ge1\) gives convergence.
