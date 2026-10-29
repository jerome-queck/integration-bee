# YANG-1.8-P11

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 11, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ (x+1)(x+4)/((x+2)(x+3)) dx

## Solution

Divide first. The quotient is 1 and the remainder is −2, so the integrand is 1 − 2/((x+2)(x+3)).

## Final answer

\[
x - 2 \log{\left(\left|{x + 2}\right| \right)} + 2 \log{\left(\left|{x + 3}\right| \right)}
\]

Stored `answer_sympy`: `x - 2*log(Abs(x + 2)) + 2*log(Abs(x + 3))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
