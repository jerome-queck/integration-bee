# R2-2025-SG-Relay-Q07

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (relay 7)
- Printed answer: no Singapore mark scheme is in this tree. The value below is derived from the problem sheet.
- Worked source: derived in this note.
- `verify/pack_gate.py` checks this reduction before the catalog row is marked `sympy`.

## Problem

\[
\int_{0}^{\pi/2}\ln|\sin(2025!\,x)|\,\ln|\sin(2026!\,x)|\,dx.
\]

## Solution

For \(|z|<1\), \(-\log(1-z)=\sum_{k\geq 1}z^{k}/k\). Taking \(z=re^{i\phi}\) and letting \(r\to 1^{-}\) gives, for \(\phi\) not a multiple of \(2\pi\),

\[
\sum_{k\geq 1}\frac{\cos(k\phi)}{k}=-\log|1-e^{i\phi}|=-\log\bigl(2\bigl|\sin(\phi/2)\bigr|\bigr),
\]

because \(|1-e^{i\phi}|^{2}=4\sin^{2}(\phi/2)\). With \(\phi=2\theta\),

\[
\log|\sin\theta|=-\log 2-\sum_{k\geq 1}\frac{\cos(2k\theta)}{k}
\]

away from integer multiples of \(\pi\). Use Abel regularisations with coefficients \(r^k/k\), \(0<r<1\), before multiplying the series. The coefficients are square summable and cosine modes are orthogonal, so the regularisations converge in \(L^2\). Their products therefore converge in \(L^1\) by Cauchy–Schwarz. This justifies the termwise calculation below; the logarithmic singularities also have finite square integrals.

The product of the two series contributes only when the frequencies agree. Since \(2026!=(2026)\,2025!\), the condition \(k\cdot 2025!=m\cdot 2026!\) says \(k=2026m\). For positive integers \(p\neq q\),

\[
\int_{0}^{\pi/2}\cos(2px)\cos(2qx)\,dx=0,
\]

while the diagonal value is \(\pi/4\). Every cosine integrated against the constant \(-\log 2\) vanishes. The constant term is \((\pi/2)(\log 2)^{2}\), and the diagonal is

\[
\frac{\pi}{4}\sum_{m\geq 1}\frac{1}{(2026m)\,m}=\frac{\pi}{4}\cdot\frac{1}{2026}\cdot\frac{\pi^{2}}{6}=\frac{\pi^{3}}{48624}.
\]

## Final answer

\[
\frac{\pi}{2}(\ln 2)^{2}+\frac{\pi^{3}}{48624}.
\]

## SymPy self-check

`solutions/self_check.py` runs `check_r2_2025_sg_relay_q07`. SymPy checks \(2026!=(2026)\,2025!\), the modulus identity, the cosine product and its integrals, and the arithmetic \(\pi^{3}/48624\).
