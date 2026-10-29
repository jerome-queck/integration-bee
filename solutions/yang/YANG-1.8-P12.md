# YANG-1.8-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 12, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ e^(2x)/(e^(2x)+3e^x+2) dx

## Solution

Set u = e^x. Then du = e^x dx and the integrand becomes u/((u+1)(u+2)) du, which splits as −1/(u+1) + 2/(u+2).

## Final answer

\[
- \log{\left(e^{x} + 1 \right)} + 2 \log{\left(e^{x} + 2 \right)}
\]

Stored `answer_sympy`: `-log(exp(x) + 1) + 2*log(exp(x) + 2)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
