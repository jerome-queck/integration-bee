# R2-2025-SG-Relay-Q14

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 14)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- The catalog row is not changed.

## Problem

\[
\int_{1}^{\infty}\sum_{k=1}^{\infty}\frac{1}{k+1}\left\lfloor\frac{k+1}{\{x\}}\right\rfloor^{-\lfloor x\rfloor}\,dx.
\]

## Solution

Write \(x=n+t\) with an integer \(n\geq 1\) and \(t\in(0,1]\). The fractional part is \(t\), and the inner power is \(M^{-n}\) where \(M=\lfloor(k+1)/t\rfloor\geq k+1\geq 2\). Every term is positive, so the sums and the integral may be rearranged. The geometric series is

\[
\sum_{n\geq 1}M^{-n}=\frac{1}{M-1}.
\]

Set \(M=k+1\). The factor \(1/(k+1)\) is \(1/M\), and the integral over \(t\) is

\[
\frac{1}{M}\int_{0}^{1}\frac{dt}{\lfloor M/t\rfloor-1}.
\]

On the interval where \(\lfloor M/t\rfloor=j\), namely \(t\in(M/(j+1),M/j]\) for each integer \(j\geq M\), the length is \(M/(j(j+1))\). The integral becomes

\[
\sum_{j\geq M}\frac{1}{j(j-1)(j+1)}.
\]

Summing over \(M\geq 2\) counts the pair \((j,M)\) once for each \(M\) from \(2\) to \(j\), which is \(j-1\) times:

\[
\sum_{j\geq 2}\frac{j-1}{j(j-1)(j+1)}=\sum_{j\geq 2}\frac{1}{j(j+1)}=\frac12.
\]

## Final answer

\[
\frac{1}{2}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q14`. SymPy checks the finite geometric sum, the slice length, the cancellation \((j-1)/(j(j-1)(j+1))\), and \(\sum_{j\geq 2}1/(j(j+1))=1/2\).
