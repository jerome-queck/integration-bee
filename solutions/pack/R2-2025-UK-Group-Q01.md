# R2-2025-UK-Group-Q01

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (group 1)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (group 1)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi}\ln\bigl(\cos x+\sqrt{1+\cos^{2}x}\bigr)\,dx.
\]

## Solution

The two factors
\[
\cos x+\sqrt{1+\cos^{2}x},\qquad -\cos x+\sqrt{1+\cos^{2}x}
\]
multiply to \(1\), and both are positive because the square root is larger than \(|\cos x|\). Their logarithms therefore sum to \(0\). Replacing \(x\) by \(\pi-x\) changes the sign of \(\cos x\), so the integrand \(f\) satisfies \(f(x)+f(\pi-x)=0\). The interval \([0,\pi]\) is symmetric under that reflection, and the integral is \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

SymPy simplifies
\[
\bigl(\cos x+\sqrt{1+\cos^{2}x}\bigr)\bigl(-\cos x+\sqrt{1+\cos^{2}x}\bigr)
\]
to \(1\).
