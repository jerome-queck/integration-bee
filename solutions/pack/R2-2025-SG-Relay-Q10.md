# R2-2025-SG-Relay-Q10

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 10). The same integral is relay 8 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 8)
- Worked source: derived in this note; the UK mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{2\pi}\frac{\sin^{67}x}{2026-\cos x}\,dx.
\]

## Solution

The denominator is at least \(2025>0\), so the integrand is continuous. The substitution \(x\mapsto 2\pi-x\) leaves \(\cos x\) fixed and sends \(\sin x\) to \(-\sin x\). An odd power changes the sign of the numerator, so the integral equals its negative and must be \(0\). The UK mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q10`. SymPy checks that an odd power of \(-\sin x\) cancels the same power of \(\sin x\), and that cosine is unchanged by \(x\mapsto 2\pi-x\).
