# YANG-1.15-P04

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 04, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \sin(2x)\cos(3x)\,dx.
\]

## Solution

The product-to-sum identity writes the integrand as \((\sin 5x-\sin x)/2\). The antiderivative is \(\tfrac12\cos x-\tfrac1{10}\cos 5x\).

## Final answer

\[
\frac{\cos{\left(x \right)}}{2} - \frac{\cos{\left(5 x \right)}}{10}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `sin(2*x)*cos(3*x)` against `cos(x)/2 - cos(5*x)/10` (indefinite). The check differentiates the stored antiderivative.
