# R2-2025-SG-Relay-Q30

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 30). The same integral is relay 11 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 11)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\frac{\sin x\ln x}{x}\,dx.
\]

## Solution

For \(0<a<2\),
\[
\int_{0}^{\infty}x^{a-1}\sin x\,dx=\Gamma(a)\sin\frac{\pi a}{2}=\frac{\Gamma(a+1)}{a}\sin\frac{\pi a}{2}.
\]
The right-hand side extends through \(a=0\) with value \(\pi/2\), which is \(\int_{0}^{\infty}\sin x/x\,dx\). Differentiating in \(a\) and then setting \(a=0\) inserts a factor \(\ln x\) and produces
\[
-\frac{\pi\gamma}{2},
\]
where \(\gamma\) is the Euler-Mascheroni constant. The mark scheme prints \(-\pi\gamma/2\).

## Final answer

\[
-\frac{\pi\gamma}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q30`. SymPy checks the same gamma expansion as the UK relay 11 note.
