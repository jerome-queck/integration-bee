# YANG-1.15-P19

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.15 Intermediate Trig Integrals, practice item 19, printed p. 26 (PDF p. 27).
- Printed answer: absent. Worked source: derived in this note.

## Problem

\[
\int \frac{1+4\cot x}{4-\cot x}\,dx.
\]

## Solution

Clearing the cotangent gives \((\sin x+4\cos x)/(4\sin x-\cos x)\). The numerator is the derivative of the denominator, so the integrand is the derivative of \(\ln(4\sin x-\cos x)\).

## Final answer

\[
\log{\left(4 \sin{\left(x \right)} - \cos{\left(x \right)} \right)}.
\]

## SymPy self-check

`verify/pack_gate.py` proves `(4*cot(x) + 1)/(4 - cot(x))` against `log(4*sin(x) - cos(x))` (indefinite). The check differentiates the stored antiderivative.
