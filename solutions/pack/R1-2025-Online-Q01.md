# R1-2025-Online-Q01

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 1)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 1)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/4}\frac{1}{1+x^{2}}\,dx.
\]

## Solution

The solutions PDF integrates directly:
\[
\int_{0}^{\pi/4}\frac{dx}{1+x^{2}}=\arctan x\Big|_{0}^{\pi/4}=\arctan\frac{\pi}{4}.
\]
It warns against simplifying that value further. The mark scheme prints \(\arctan(\pi/4)\).

## Final answer

\[
\arctan\dfrac{\pi}{4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q01`. SymPy evaluates \(\int_{0}^{\pi/4}dx/(1+x^{2})\) as \(\arctan(\pi/4)\).
