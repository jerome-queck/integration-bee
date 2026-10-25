# R1-2025-Online-Q15

- Problem: `sources/past/r1/2025/2025_Online_Round_1.pdf` (problem 15)
- Printed answer: `sources/past/r1/2025/2025_Online_Round_1_Mark_Scheme.pdf`
- Worked source: `sources/past/r1/2025/2025_Round_1_Solutions.pdf` (problem 15)
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi}\sqrt{1+\sin 2x}\,dx.
\]

## Solution

The solutions PDF uses \(1+\sin 2x=(\sin x+\cos x)^{2}\), so the square root is \(|\sin x+\cos x|\). That linear combination is nonnegative on \([0,3\pi/4]\) and nonpositive on \([3\pi/4,\pi]\):
\[
\int_{0}^{\pi}\sqrt{1+\sin 2x}\,dx=\int_{0}^{3\pi/4}(\sin x+\cos x)\,dx-\int_{3\pi/4}^{\pi}(\sin x+\cos x)\,dx=2\sqrt{2}.
\]
The mark scheme prints \(2\sqrt{2}\).

## Final answer

\[
2\sqrt{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r1_2025_online_q15`. SymPy checks \(1+\sin 2x=(\sin x+\cos x)^{2}\) and evaluates the split integrals as \(2\sqrt{2}\).
