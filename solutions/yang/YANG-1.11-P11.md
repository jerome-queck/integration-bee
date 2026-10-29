# YANG-1.11-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 11, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ x^2 √(x−1) dx

## Solution

Set u = √(x−1). Then x = u^2+1 and the integral is 2 ∫ (u^2+1)^2 u^2 du.

## Final answer

\[
\frac{2 x^{3} \sqrt{x - 1}}{7} - \frac{2 x^{2} \sqrt{x - 1}}{35} - \frac{8 x \sqrt{x - 1}}{105} - \frac{16 \sqrt{x - 1}}{105}
\]

Stored `answer_sympy`: `2*x**3*sqrt(x - 1)/7 - 2*x**2*sqrt(x - 1)/35 - 8*x*sqrt(x - 1)/105 - 16*sqrt(x - 1)/105`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
