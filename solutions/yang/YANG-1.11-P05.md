# YANG-1.11-P05

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 5, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ cos(√x)/√x dx

## Solution

Set u = √x. Then du = dx/(2√x), so the integral is 2 ∫ cos u du.

## Final answer

\[
2 \sin{\left(\sqrt{x} \right)}
\]

Stored `answer_sympy`: `2*sin(sqrt(x))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
