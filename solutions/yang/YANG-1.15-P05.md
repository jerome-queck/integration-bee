# YANG-1.15-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 05, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \cos(5x)\cos(7x)\,dx.
\]

## Solution

\(\cos 5x\cos 7x=(\cos 12x+\cos 2x)/2\). Integrating termwise gives \(\tfrac14\sin 2x+\tfrac1{24}\sin 12x\).

## Final answer

\[
\frac{\sin{\left(2 x \right)}}{4} + \frac{\sin{\left(12 x \right)}}{24}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `cos(5*x)*cos(7*x)` against `sin(2*x)/4 + sin(12*x)/24` (indefinite). The check differentiates the stored antiderivative.
