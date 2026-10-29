# YANG-1.15-P09

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 09, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int (\cos^{4} x-\sin^{4} x)\,dx.
\]

## Solution

The difference of squares is \(\cos 2x\). Its antiderivative is \(\tfrac12\sin 2x\).

## Final answer

\[
\frac{\sin{\left(2 x \right)}}{2}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `-sin(x)**4 + cos(x)**4` against `sin(2*x)/2` (indefinite). The check differentiates the stored antiderivative.
