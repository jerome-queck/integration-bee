# R2-2025-SG-Relay-Q26

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 26)
- Printed answer: none in the pack. The value below is derived in this note.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{0}^{\pi/2}\frac{dx}{1+\sin^{2}x\cos^{2}x}.
\]

## Solution

Use \(\sin^{2}x\cos^{2}x=(1-\cos 4x)/8\). The integrand is \(8/(9-\cos 4x)\). Set \(\phi=4x\). Then \(x\in[0,\pi/2]\) sends \(\phi\) over \([0,2\pi]\), and the integral equals
\[
2\int_{0}^{2\pi}\frac{d\phi}{9-\cos\phi}.
\]
For \(a>1\), the Weierstrass substitution gives \(\int_{0}^{2\pi}d\phi/(a-\cos\phi)=2\pi/\sqrt{a^{2}-1}\). Here \(a=9\) and \(\sqrt{80}=4\sqrt{5}\), so the value is \(\pi/\sqrt{5}\).

## Final answer

\[
\dfrac{\pi}{\sqrt{5}}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q26`. SymPy checks the double-angle reduction and the period integral at \(a=9\).
