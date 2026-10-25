# R2-2025-SG-Group-Q02

- Problem: `sources/past/r2/2025/sg/2025_R2_Group_Round_SG.pdf` (group 2). The same integral is group 1 of `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK group 1)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi}\ln\bigl(\cos x+\sqrt{1+\cos^{2}x}\bigr)\,dx.
\]

## Solution

The factors \(\cos x+\sqrt{1+\cos^{2}x}\) and \(-\cos x+\sqrt{1+\cos^{2}x}\) multiply to \(1\), and both are positive. Their logarithms sum to \(0\). The reflection \(x\mapsto\pi-x\) changes the sign of \(\cos x\), so the integrand and its reflection cancel. The integral over \([0,\pi]\) is \(0\). The UK mark scheme prints \(0\) for this integral.

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
