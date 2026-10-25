# R2-2025-UK-Relay-Q08

- Problem: `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf` (relay 8)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (relay 8)
- Worked source: derived in this note; the mark scheme prints the final value.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{2\pi}\frac{\sin^{67}x}{2026-\cos x}\,dx.
\]

## Solution

Let \(f(x)=\sin^{67}x/(2026-\cos x)\). Then \(\sin(2\pi-x)=-\sin x\) and \(67\) is odd, while cosine is unchanged, so \(f(2\pi-x)=-f(x)\). The integral of this odd function about \(x=\pi\) is \(0\). The mark scheme prints \(0\).

## Final answer

\[
0.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_relay_q08`. SymPy simplifies \(f(2\pi-x)+f(x)\) to \(0\).
