# R2-2025-SG-Relay-Q13

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 13)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{1}^{\infty}x\sqrt{x^{2}-1}\,e^{-x^{2}}\,dx.
\]

## Solution

Set \(v=x^{2}-1\). Then \(dv=2x\,dx\) and \(x^{2}=v+1\), so the integral is
\[
\frac{e^{-1}}{2}\int_{0}^{\infty}\sqrt{v}\,e^{-v}\,dv=\frac{\Gamma(3/2)}{2e}.
\]
Since \(\Gamma(3/2)=\sqrt{\pi}/2\),
\[
\frac{\sqrt{\pi}}{4e}.
\]

## Final answer

\[
\dfrac{\sqrt{\pi}}{4e}.
\]

## SymPy self-check

SymPy evaluates \(\int_{0}^{\infty}\sqrt{v}\,e^{-v}\,dv=\Gamma(3/2)\) and simplifies \(\Gamma(3/2)/(2e)\) to \(\sqrt{\pi}/(4e)\).
