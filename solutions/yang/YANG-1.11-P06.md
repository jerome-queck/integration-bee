# YANG-1.11-P06

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 6, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ e^(1/x)/x^2 dx

## Solution

Set u = 1/x. Then du = −dx/x^2, so the integral is −∫ e^u du.

## Final answer

\[
- e^{\frac{1}{x}}
\]

Stored `answer_sympy`: `-exp(1/x)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
