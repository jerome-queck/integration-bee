# R2-2025-UK-Relay-Q18

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (PDF p. 5, relay 18)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (PDF p. 4, relay 18)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog gate checks the Dirichlet reduction and rational cosine transform against this printed final.

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

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q18`. SymPy checks the rational identity, evaluates \(\int_{0}^{\infty}\cos(bx)/(x^{2}+1)\,dx\), and checks the resulting combination.
