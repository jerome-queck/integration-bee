# YANG-1.8-P03

- Guide: `sources/user/Integration_Bee_Topics_Guide_Yang_2nd_Ed.pdf`, §1.8 Basic Partial Fractions, practice item 3, printed p. 15 (PDF p. 16).
- Printed answer: absent.
- Worked source: derived in this note.

## Problem

∫ dx/((x+1)(x+2))

## Solution

Split 1/((x+1)(x+2)) as 1/(x+1) − 1/(x+2).

## Final answer

\[
\log{\left(\left|{x + 1}\right| \right)} - \log{\left(\left|{x + 2}\right| \right)}
\]

Stored `answer_sympy`: `log(Abs(x + 1)) - log(Abs(x + 2))`.

## SymPy self-check

`verify/pack_gate.py` proves this row by `indefinite` comparison of the stored fields. The stored antiderivative omits a constant. Differentiation recovers the stored integrand. `make check` re-proves those fields. Numeric agreement is not the proof.
