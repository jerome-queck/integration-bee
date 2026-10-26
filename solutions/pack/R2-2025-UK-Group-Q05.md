# R2-2025-UK-Group-Q05

- Problem: `sources/past/r2/2025/uk/2025_Group_Round_2_Integration_Bee.pdf` (p. 2, group 5)
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (p. 2, group 5)
- Worked source: derived in this note; the mark scheme prints the final value.
- Catalog proof: the source integral and final are checked by `verify/pack_gate.py`.

## Problem

\[
\int_{0}^{\pi/2}(\sin x+\cos x)\arctan(\sin x)\,dx.
\]

## Solution

Integrate by parts with \(v=\sin x-\cos x\). The boundary term is \(\pi/4\), and the remaining integral is
\[
\int_{0}^{\pi/2}\frac{(\sin x-\cos x)\cos x}{1+\sin^{2}x}\,dx.
\]
The first part, in \(t=\sin x\), is \(\int_{0}^{1}t/(1+t^{2})\,dt=(\ln 2)/2\). The second is
\[
\int_{0}^{\pi/2}\frac{\cos^{2}x}{1+\sin^{2}x}\,dx=2\int_{0}^{\pi/2}\frac{d x}{1+\sin^{2}x}-\frac{\pi}{2}.
\]
The tangent substitution turns \(1/(1+\sin^{2}x)\) into \(1/(1+2t^{2})\), whose integral on \([0,\infty)\) is \(\pi/(2\sqrt{2})\). Combining these pieces gives
\[
\frac{\pi}{\sqrt{2}}-\frac{\pi}{4}-\frac{\ln 2}{2}.
\]
The mark scheme prints that value.

## Final answer

\[
\dfrac{\pi}{\sqrt{2}}-\dfrac{\pi}{4}-\dfrac{\ln 2}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_uk_group_q05`. SymPy checks the integration by parts, the tangent substitution, and the final arithmetic.
