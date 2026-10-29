# YANG-1.11-P08

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 8, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ √x sin(x√x) dx

## Solution

Set u = x^(3/2). Then du = (3/2) √x dx, so the integral is (2/3) ∫ sin u du.

## Final answer

\[
- \frac{2 \cos{\left(x^{\frac{3}{2}} \right)}}{3}
\]

Stored `answer_sympy`: `-2*cos(x**(3/2))/3`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
