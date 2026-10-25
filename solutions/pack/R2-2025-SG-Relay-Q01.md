# R2-2025-SG-Relay-Q01

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 1). The same integral is relay 1 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 1)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{1}x^{44}\ln x\,dx.
\]

## Solution

Integrating \(x^{44}\ln x\) by parts, the boundary term \(x^{45}\ln x\) vanishes at both ends, and the integral equals \(-1/45^{2}=-1/2025\). The UK mark scheme prints \(-1/2025\) for this integral.

## Final answer

\[
-\dfrac{1}{2025}.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{1}x^{44}\ln x\,dx=-1/2025\).
