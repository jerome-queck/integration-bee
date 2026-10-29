# YANG-1.11-P18

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.11 Intermediate U-Substitution, practice item 18, printed p. 20 (PDF p. 21).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ sec^2(x)/(8+sec^2(x)) dx

## Solution

Set u = tan x. Then du = sec^2(x) dx and 8+sec^2(x) = 9+u^2, so the integral is (1/3) atan(u/3).

## Final answer

\[
\frac{\operatorname{atan}{\left(\frac{\tan{\left(x \right)}}{3} \right)}}{3}
\]

Stored `answer_sympy`: `atan(tan(x)/3)/3`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
