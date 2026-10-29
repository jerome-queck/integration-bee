# YANG-1.11-P12

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 12, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ (x+5)/√((x+2)(x+8)) dx

## Solution

Set u = x+5. Then (x+2)(x+8) = u^2−9, and ∫ u/√(u^2−9) du = √(u^2−9).

## Final answer

\[
\sqrt{x^{2} + 10 x + 16}
\]

Stored `answer_sympy`: `sqrt(x**2 + 10*x + 16)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
