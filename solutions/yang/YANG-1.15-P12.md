# YANG-1.15-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 12, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \bigl(\sin(x-\sin x)-\sin(x+\sin x)\bigr)\,dx.
\]

## Solution

The sine difference is \(-2\cos x\sin(\sin x)\). Differentiating \(2\cos(\sin x)\) recovers that integrand.

## Final answer

\[
2 \cos{\left(\sin{\left(x \right)} \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sin(x - sin(x)) - sin(x + sin(x))` against `2*cos(sin(x))` (indefinite). The check differentiates the stored antiderivative.
