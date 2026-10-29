# YANG-1.11-P01

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 1, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ x/(1+x^4) dx

## Solution

Set u = x^2. Then du = 2x dx, and the integral is (1/2) ∫ du/(1+u^2).

## Final answer

\[
\frac{\operatorname{atan}{\left(x^{2} \right)}}{2}
\]

Stored `answer_sympy`: `atan(x**2)/2`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
