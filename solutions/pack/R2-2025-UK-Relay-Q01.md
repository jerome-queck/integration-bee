# R2-2025-UK-Relay-Q01

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 1)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 1)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}x^{44}\ln x\,dx.
\]

## Solution

The antiderivative of \(x^{a}\ln x\) at \(a=44\) is
\[
\frac{x^{45}\ln x}{45}-\frac{x^{45}}{45^{2}}.
\]
As \(x\downarrow 0\), \(x^{45}\ln x\to 0\). At \(x=1\) the logarithm vanishes, and the value of the integral is \(-1/45^{2}=-1/2025\).

## Final answer

\[
-\dfrac{1}{2025}.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{1}x^{44}\ln x\,dx=-1/2025\).
