# R2-2025-SG-Relay-Q04

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 4). The same integral is relay 4 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (UK relay 4)
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\infty}\int_{0}^{\infty}\sin(x^{2}+y^{2})\,dx\,dy.
\]

## Solution

Polar coordinates in the first quadrant, damped by \(e^{-\varepsilon r^{2}}\) and with \(u=r^{2}\), give
\[
\frac{\pi}{4}\int_{0}^{\infty}e^{-\varepsilon u}\sin u\,du=\frac{\pi}{4(1+\varepsilon^{2})}.
\]
Letting \(\varepsilon\downarrow 0\) produces \(\pi/4\). The UK mark scheme prints \(\pi/4\) for this integral.

## Final answer

\[
\dfrac{\pi}{4}.
\]

## SymPy self-check

For \(\varepsilon>0\), SymPy evaluates \(\int_{0}^{\infty}e^{-\varepsilon u}\sin u\,du=1/(\varepsilon^{2}+1)\). The limit of \((\pi/4)/(1+\varepsilon^{2})\) as \(\varepsilon\to 0\) is \(\pi/4\).
