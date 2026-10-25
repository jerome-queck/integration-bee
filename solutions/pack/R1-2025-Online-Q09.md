# R1-2025-Online-Q09

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 9)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 9)
- The catalog row is not changed.

## Problem

\[
\int_{-\pi/4}^{\pi/4}\frac{7x^{7}-5x^{5}+3x^{3}-x+1}{\cos^{2}x}\,dx.
\]

## Solution

For each odd positive integer \(n\), \(x^{n}/\cos^{2}x\) is odd. On an interval symmetric about \(0\), the solutions PDF drops those terms and keeps
\[
\int_{-\pi/4}^{\pi/4}\sec^{2}x\,dx=\tan x\Big|_{-\pi/4}^{\pi/4}=2.
\]
The mark scheme prints \(2\).

## Final answer

\[
2.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q09`. SymPy checks that \((7x^{7}-5x^{5}+3x^{3}-x)/\cos^{2}x\) is odd and evaluates \(\int_{-\pi/4}^{\pi/4}\sec^{2}x\,dx=2\).
