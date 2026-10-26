# R2-2025-UK-Group-Q08

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (group 8)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (group 8)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\Bigl(\frac{\sin^{6}x}{x^{2}}+\frac{\sin^{5}x}{x}+\frac{\sin^{4}x}{x^{2}}+\frac{\sin^{3}x}{x^{3}}\Bigr)\,dx.
\]

## Solution

Expand the powers into multiple angles. For \(k>0\),
\[
\int_{0}^{\infty}\frac{\sin(kx)}{x}\,dx=\frac{\pi}{2},\qquad
\int_{0}^{\infty}\frac{1-\cos(kx)}{x^{2}}\,dx=\frac{\pi k}{2},
\]
the second by differentiating the first in \(k\). A further differentiation gives
\[
\int_{0}^{\infty}\frac{bx-\sin(bx)}{x^{3}}\,dx=\frac{\pi b^{2}}{4}.
\]
The four pieces evaluate to \(3\pi/16\), \(3\pi/16\), \(\pi/4\), and \(3\pi/8\). Their sum is \(\pi\). The mark scheme prints \(\pi\). The earlier catalog plain \(0\) was the misaligned relay line, not group 8.

## Final answer

\[
\pi.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_group_q08`. SymPy checks the multiple-angle reductions, the Dirichlet integral, and the coefficient sum.
