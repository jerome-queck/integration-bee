# YANG-1.8-P13

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 13, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ (x^2−x)/(1+x+x^2+x^3) dx

## Solution

Factor the denominator as (x+1)(x^2+1). The numerator splits as 1/(x+1) − 1/(x^2+1).

## Final answer

\[
\log{\left(\left|{x + 1}\right| \right)} - \operatorname{atan}{\left(x \right)}
\]

Stored `answer_sympy`: `log(Abs(x + 1)) - atan(x)`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
