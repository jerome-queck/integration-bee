# YANG-1.15-P20

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 20, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{\sin x\cos x}{\sin^{4} x+\cos^{4} x}\,dx.
\]

## Solution

With \(u=\sin^{2} x\), the integrand becomes \(\tfrac12 du/(2u^{2}-2u+1)\). Completing the square produces \(\tfrac12\arctan(2\sin^{2} x-1)\).

## Final answer

\[
\frac{\operatorname{atan}{\left(2 \sin^{2}{\left(x \right)} - 1 \right)}}{2}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sin(x)*cos(x)/(sin(x)**4 + cos(x)**4)` against `atan(2*sin(x)**2 - 1)/2` (indefinite). The check differentiates the stored antiderivative.
