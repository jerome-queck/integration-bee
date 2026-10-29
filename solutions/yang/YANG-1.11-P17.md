# YANG-1.11-P17

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 17, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ dx/(√x(1+2√x+x))

## Solution

The factor 1+2√x+x is (1+√x)^2. Set u = √x. Then the integral is 2 ∫ du/(1+u)^2.

## Final answer

\[
- \frac{2}{\sqrt{x} + 1}
\]

Stored `answer_sympy`: `-2/(sqrt(x) + 1)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
