# YANG-1.8-P15

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 15, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ (x+5)/(x^2+x−2) dx

## Solution

Factor x^2+x−2 as (x+2)(x−1) and split as −1/(x+2) + 2/(x−1).

## Final answer

\[
2 \log{\left(\left|{x - 1}\right| \right)} - \log{\left(\left|{x + 2}\right| \right)}
\]

Stored `answer_sympy`: `2*log(Abs(x - 1)) - log(Abs(x + 2))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
