# R2-2025-SG-Relay-Q28

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 28). The same integral is relay 18 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 18)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{x^{2}-1}{x^{2}+1}\cdot\frac{\sin x}{x}\,dx.
\]

## Solution

Rewrite
\[
\frac{x^{2}-1}{x^{2}+1}=1-\frac{2}{x^{2}+1}.
\]
The Dirichlet integral \(\int_{0}^{\infty}\sin x/x\,dx=\pi/2\). For \(b>0\),
\[
\int_{0}^{\infty}\frac{\cos(bx)}{x^{2}+1}\,dx=\frac{\pi}{2}e^{-b},
\]
so
\[
\int_{0}^{\infty}\frac{\sin x}{x(x^{2}+1)}\,dx=\int_{0}^{1}\frac{\pi}{2}e^{-b}\,db=\frac{\pi}{2}\bigl(1-e^{-1}\bigr).
\]
The original integral is
\[
\frac{\pi}{2}-\pi\bigl(1-e^{-1}\bigr)=\frac{\pi}{e}-\frac{\pi}{2}.
\]
The mark scheme prints \(\pi/e-\pi/2\).

## Final answer

\[
\frac{\pi}{e}-\frac{\pi}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q28`. SymPy checks the same rational identity and Laplace integral as the UK relay 18 note.
