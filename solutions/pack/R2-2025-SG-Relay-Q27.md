# R2-2025-SG-Relay-Q27

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 27)
- Printed answer: none in the pack. The value below is derived in this note.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{-1}^{1}\exp(\operatorname{erf}^{-1}x)\,dx.
\]

## Solution

Set \(u=\operatorname{erf}^{-1}x\), where \(\operatorname{erf}u=(2/\sqrt{\pi})\int_{0}^{u}e^{-t^{2}}\,dt\). Then \(u\) runs over \(\mathbb{R}\) and \(dx=(2/\sqrt{\pi})e^{-u^{2}}\,du\). The integral becomes
\[
\frac{2}{\sqrt{\pi}}\int_{-\infty}^{\infty}e^{u-u^{2}}\,du=\frac{2}{\sqrt{\pi}}e^{1/4}\int_{-\infty}^{\infty}e^{-(u-1/2)^{2}}\,du=2e^{1/4}.
\]

## Final answer

\[
2e^{1/4}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q27`. SymPy checks the completed square and the translated Gaussian integral.
