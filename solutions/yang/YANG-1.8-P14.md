# YANG-1.8-P14

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 14, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ 3x/(x^2+2x−8) dx

## Solution

Factor x^2+2x−8 as (x+4)(x−2) and split 3x as 2/(x+4) + 1/(x−2).

## Final answer

\[
\log{\left(\left|{x - 2}\right| \right)} + 2 \log{\left(\left|{x + 4}\right| \right)}
\]

Stored `answer_sympy`: `log(Abs(x - 2)) + 2*log(Abs(x + 4))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
