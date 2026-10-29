# YANG-1.11-P07

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 7, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ dx/√(x−x^2)

## Solution

Complete the square: x−x^2 = 1/4−(x−1/2)^2. The derivative of asin(2x−1) is 1/√(x−x^2).

## Final answer

\[
\operatorname{asin}{\left(2 x - 1 \right)}
\]

Stored `answer_sympy`: `asin(2*x - 1)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
