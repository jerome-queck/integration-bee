# YANG-1.15-P10

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 10, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \sqrt{\csc x-\sin x}\,dx.
\]

## Solution

The identity \(\csc x-\sin x=\cos^{2}x/\sin x\) holds where \(\sin x\neq 0\). The right-hand side is nonnegative exactly when \(\sin x>0\), which is the domain of the printed square root. On that domain both \(\sqrt{\csc x-\sin x}\) and \(|\cos x|/\sqrt{\sin x}\) are nonnegative and have the same square, so the integrand is \(|\cos x|/\sqrt{\sin x}\).

Where \(\cos x\ge 0\), that is \(\cos x/\sqrt{\sin x}\), and the derivative of \(2\sqrt{\sin x}\) is that expression. Where \(\cos x<0\), it is \(-\cos x/\sqrt{\sin x}\), and the derivative of \(4-2\sqrt{\sin x}\) is that expression. The two formulas both equal \(2\) at \(x=\pi/2\), so they meet on the boundary \(\cos x=0\). The same pair is the derivative on every later interval where \(\sin x>0\).

## Final answer

\[
\begin{cases} 2 \sqrt{\sin{\left(x \right)}} & \text{for}\: \cos{\left(x \right)} \geq 0 \\4 - 2 \sqrt{\sin{\left(x \right)}} & \text{otherwise} \end{cases}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sqrt(-sin(x) + csc(x))` against `Piecewise((2*sqrt(sin(x)), cos(x) >= 0), (4 - 2*sqrt(sin(x)), True))` (indefinite). The check differentiates each piece on the sign of \(\cos x\) where \(\sin x>0\). The reduction is `verify/yang_certificates.py`.
