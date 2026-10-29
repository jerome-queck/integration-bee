# YANG-1.11-P19

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 19, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ √(x/(1−x^3)) dx

## Solution

Set x = t^2 with t > 0. The integral becomes (2/3) ∫ ds/√(1−s^2) after s = t^3, which is (2/3) asin(x^(3/2)).

## Final answer

\[
\frac{2 \operatorname{asin}{\left(x^{\frac{3}{2}} \right)}}{3}
\]

Stored `answer_sympy`: `2*asin(x**(3/2))/3`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
