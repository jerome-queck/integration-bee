# R2-2025-SG-Relay-Q04

- Problem: `sources/past/r2/2025/sg/2025_R2_Relay_problems_SG.pdf` (p. 1, relay 4). The same integral is relay 4 of `sources/past/r2/2025/uk/2025_Relay_Round_2.pdf`.
- Printed answer: `sources/past/r2/2025/uk/2025_Round_2_Mark_Scheme.pdf` (p. 3, UK relay 4)
- Worked source: derived in this note.

## Problem

\[
\int_{0}^{\infty}\int_{0}^{\infty}\sin(x^{2}+y^{2})\,dx\,dy.
\]

## Solution

For each fixed \(y\), the angle-addition identity gives
\[
\sin(x^{2}+y^{2})=\sin(x^{2})\cos(y^{2})+\cos(x^{2})\sin(y^{2}).
\]
The two ordinary Fresnel improper integrals converge and have the common value
\[
S=\int_{0}^{\infty}\sin(x^{2})\,dx
=C=\int_{0}^{\infty}\cos(x^{2})\,dx
=\frac{\sqrt{2\pi}}{4}.
\]
Consequently the inner integral is
\(S\cos(y^{2})+C\sin(y^{2})\). Both terms have convergent outer
improper integrals, so the printed iterated integral is
\[
SC+CS=2\left(\frac{\sqrt{2\pi}}{4}\right)^{2}=\frac{\pi}{4}.
\]
This argument respects the printed order \(dx\,dy\). A polar-coordinate
integral with an added Gaussian damping also tends to \(\pi/4\), but that
Abel limit alone would not establish the value of the ordinary iterated
integral. The UK mark scheme prints \(\pi/4\).

## Final answer

\[
\dfrac{\pi}{4}.
\]

## SymPy self-check

The pack-gate certificate retains the literal inner `Integral`, checks the
angle-addition identity, and evaluates both convergent one-dimensional
Fresnel integrals. It returns their two cross-products; it does not replace
the source with a damped double integral.
